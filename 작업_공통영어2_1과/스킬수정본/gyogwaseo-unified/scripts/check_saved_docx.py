"""Read actual saved DOCX blocks and compare them with the intended layout plan.

Content correspondence and stored-format validation are reported separately.
Actual OOXML is independently extracted; expected formatting comes from the
approved plan and current hash-bound MASTER. Word pagination and content
semantics still require their separate reviews.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
from zipfile import ZipFile
from lxml import etree as E

W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
NS = {'w': W}


def q(name):
    return '{' + W + '}' + name


def paragraph_text(p):
    fragments = []
    for node in p.iter():
        if node.tag == q('t'):
            fragments.append(node.text or '')
        elif node.tag == q('tab'):
            fragments.append('\t')
        elif node.tag in {q('br'), q('cr')}:
            if node.get(q('type'), 'textWrapping') == 'textWrapping':
                fragments.append('\n')
        elif node.tag in {q('del'), q('ins'), q('altChunk'), q('fldChar'), q('instrText')}:
            raise ValueError('Tracked changes, fields, or embedded content in a managed block need explicit review')
    return ''.join(fragments)


def element_record(element):
    if element.tag == q('p'):
        return {'kind': 'paragraph', 'text': paragraph_text(element)}
    if element.tag == q('tbl'):
        rows = []
        for row in element.findall('w:tr', NS):
            cells = []
            for cell in row.findall('w:tc', NS):
                if cell.find('w:tbl', NS) is not None:
                    raise ValueError('Nested table is not part of the common word/cover tables')
                cells.append([paragraph_text(p) for p in cell.findall('w:p', NS)])
            rows.append(cells)
        return {'kind': 'table', 'rows': rows}
    raise ValueError('Unsupported managed block element: ' + E.QName(element).localname)


def extract(path):
    path = Path(path)
    with ZipFile(path) as z:
        if len(z.namelist()) != len(set(z.namelist())) or z.testzip() is not None:
            raise ValueError('Corrupt or ambiguous DOCX package')
        root = E.fromstring(z.read('word/document.xml'))
    body = root.find('w:body', NS)
    if body is None:
        raise ValueError('Missing document body')
    blocks, unmanaged = [], []
    seen = set()
    for element in body:
        if element.tag == q('sectPr'):
            continue
        tag = element.find('w:sdtPr/w:tag', NS) if element.tag == q('sdt') else None
        name = tag.get(q('val'), '') if tag is not None else ''
        if not name.startswith('gyogwaseo:'):
            unmanaged.append(E.QName(element).localname)
            continue
        name = name[len('gyogwaseo:'):]
        if not name or name in seen:
            raise ValueError('Missing or duplicate managed block ID')
        seen.add(name)
        content = element.find('w:sdtContent', NS)
        if content is None:
            raise ValueError('Missing saved block content')
        records = [element_record(child) for child in content]
        blocks.append({'id': name, 'elements': records})
    return {'path': str(path.resolve()), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
            'blocks': blocks, 'unmanaged_body_elements': unmanaged}


def expected_element(element):
    kind = element.get('kind', 'paragraph')
    if kind == 'paragraph':
        runs = element.get('runs') or []
        return {'kind': kind, 'text': ''.join(run['text'] for run in runs)}
    if kind != 'table':
        raise ValueError('Unknown expected element kind')
    entries = element['entries']
    if element['role'] == 'cover_topic_box':
        if len(entries) != 2:
            raise ValueError('Cover requires one English and one Korean paragraph')
        return {'kind': kind, 'rows': [[list(entries)]]}
    if element['role'] == 'workbook_answer_grid':
        if not entries or any(not isinstance(item, dict) or not item.get('runs') for item in entries):
            raise ValueError('Answer grid entries require runs')
        return {'kind': kind, 'rows': [
            [[''.join(run['text'] for run in entries[index]['runs'])] if index < len(entries) else ['']
             for index in range(start, start + 3)]
            for start in range(0, len(entries), 3)]}
    if element['role'] not in {'workbook_word_table', 'workbook_relations_table'}:
        raise ValueError('Unknown expected table role')
    rows = []
    for start in range(0, len(entries), 2):
        row = []
        for index in range(start, start + 2):
            row.extend([[f'{index + 1}. {entries[index]}' if index < len(entries) else ''], ['']])
        rows.append(row)
    return {'kind': kind, 'rows': rows}


def check(plan, saved, scope='full', assets=None):
    if scope not in {'full', 'targeted'}:
        raise ValueError('scope must be full or targeted')
    planned = plan.get('blocks')
    if not isinstance(planned, list) or not planned:
        raise ValueError('Nonempty layout plan is required')
    actual = extract(saved)
    by_id = {block['id']: block for block in actual['blocks']}
    expected_ids = [block['id'] for block in planned]
    if len(expected_ids) != len(set(expected_ids)):
        raise ValueError('Duplicate expected block ID')
    errors = []
    if scope == 'full':
        if [b['id'] for b in actual['blocks']] != expected_ids:
            errors.append({'code': 'BLOCK_ORDER_OR_COVERAGE'})
        if actual['unmanaged_body_elements']:
            errors.append({'code': 'UNMANAGED_BODY_CONTENT'})
    for block in planned:
        if block['id'] not in by_id:
            errors.append({'code': 'MISSING_SAVED_BLOCK', 'block': block['id']})
            continue
        expected = [expected_element(element) for element in block['elements']]
        observed = by_id[block['id']]['elements']
        if len(expected) != len(observed):
            errors.append({'code': 'ELEMENT_COUNT', 'block': block['id'],
                           'expected': len(expected), 'actual': len(observed)})
        for index in range(min(len(expected), len(observed))):
            if expected[index] != observed[index]:
                errors.append({'code': 'SAVED_CONTENT_MISMATCH', 'block': block['id'],
                               'element': index, 'expected': expected[index], 'actual': observed[index]})
    format_path = Path(__file__).with_name('saved_format.py')
    spec = importlib.util.spec_from_file_location('_saved_format_checker', format_path)
    format_checker = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(format_checker)
    format_result = format_checker.check_format(plan, saved, scope, assets)
    content_validation = 'FAIL' if errors else 'PASS'
    errors.extend(format_result['format_errors'])
    return {'status': 'FAIL' if errors else 'SAVED_CONTENT_MATCH', 'scope': scope,
            'content_validation': content_validation, **format_result,
            'saved_sha256': actual['sha256'], 'checked_blocks': expected_ids,
            'errors': errors, 'extracted': actual,
            'layout_geometry_review': 'NOT_PERFORMED', 'semantic_review': 'NOT_PERFORMED',
            'question_answer_validity': 'NOT_PERFORMED'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('plan', type=Path)
    parser.add_argument('docx', type=Path)
    parser.add_argument('report', type=Path)
    parser.add_argument('--scope', choices=['full', 'targeted'], default='full')
    parser.add_argument('--assets', type=Path, help='Approved assets directory; default is the installed skill assets')
    args = parser.parse_args()
    if args.report.resolve() in {args.plan.resolve(), args.docx.resolve()}:
        raise ValueError('Report must not overwrite an input')
    result = check(json.loads(args.plan.read_text(encoding='utf-8-sig')), args.docx, args.scope, args.assets)
    args.report.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({k: v for k, v in result.items() if k not in {'errors', 'extracted'}}, ensure_ascii=False))
    raise SystemExit(1 if result['errors'] else 0)


if __name__ == '__main__':
    main()
