"""Export one ZIP of the integrated DOCX and five volumes without rendering.

The source remains the one editable book. Exact managed OOXML blocks, formatting,
relationships, assets and page fields are copied; no content is regenerated. The
manifest proves partition/preservation only, not Word pagination or release QA.
"""
import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import re
from zipfile import BadZipFile, ZIP_DEFLATED, ZipFile
from lxml import etree as E

from check_saved_docx import expected_element, extract, NS, q
from master_docx import read_package, block_index

VOLUME_KINDS = ('reading', 'analysis', 'workbook', 'mock', 'answers')
VOLUME_LABELS = ('해석지', '지문분석지', '워크북+변형문제', '실전모의', '정답해설지')
MANIFEST_NAME = '분권내보내기.json'
ANSWER_ROLES = {
    'answers_header', 'quick_answers_heading', 'quick_answers_set_heading',
    'quick_answers_row', 'workbook_answer_unit_heading',
    'workbook_answer_activity_heading', 'workbook_answer_grid',
    'workbook_key_answers_heading', 'workbook_key_answer', 'mock_answers_header',
    'question_answer', 'question_evidence', 'question_explanation',
    'correct_choice_translation', 'wrong_reasons_heading', 'wrong_reason',
    'choice_translation_heading',
}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def block_sha(element):
    return sha(E.tostring(element, method='c14n'))


def validate_base(value):
    """Validate a supplied, already-confirmed publisher/author filename base."""
    if (not isinstance(value, str) or not value.startswith('혼공독해교재_')
            or re.search(r'[<>:"/\\|?*\x00-\x1f]', value)
            or value.rstrip(' .') != value or len(value) > 160
            or not re.fullmatch(r'혼공독해교재_[^_]+_[^_]+_(?:[1-9]\d*과|SpecialLesson[1-9]\d*)', value)):
        raise ValueError('Use the confirmed base 혼공독해교재_과목_출판사(저자약칭)_1과 or SpecialLesson1; no extension or path')
    return value


def partition(plan):
    blocks = plan.get('blocks')
    if not isinstance(blocks, list) or not blocks:
        raise ValueError('A full canonical block plan is required')
    result = {kind: [] for kind in VOLUME_KINDS}
    seen = set()
    for block in blocks:
        bid = block.get('id')
        elements = block.get('elements')
        if not isinstance(bid, str) or not bid or bid in seen or not elements:
            raise ValueError('Missing/duplicate block ID or empty planned block')
        seen.add(bid)
        roles = [e.get('role') for e in elements]
        if bid == 'cover':
            kind = 'reading'
        elif bid.startswith('answers/') or bid.endswith('/answers'):
            kind = 'answers'
        elif bid.endswith('/reading'):
            kind = 'reading'
        elif bid.endswith('/analysis'):
            kind = 'analysis'
        elif bid.endswith('/workbook'):
            kind = 'workbook'
        elif roles[0] == 'mock_round_header':
            kind = 'mock'
        else:
            raise ValueError('Unknown block cannot be silently omitted: ' + bid)
        if kind != 'answers' and ANSWER_ROLES.intersection(roles):
            raise ValueError('Answer role found in student volume: ' + bid)
        result[kind].append(bid)
    if blocks[0]['id'] != 'cover' or not any(x.endswith('/reading') for x in result['reading']):
        raise ValueError('Cover must be first and reading content must exist')
    if any(not result[kind] for kind in VOLUME_KINDS):
        raise ValueError('All five nonempty volumes are required; learning-stage plans are not final split plans')
    return result


def read_source(source_docx, plan):
    """Check full content/order before copying original, already-saved XML."""
    groups = partition(plan)
    actual = extract(source_docx)
    expected = [{'id': b['id'], 'elements': [expected_element(e) for e in b['elements']]}
                for b in plan['blocks']]
    if actual['unmanaged_body_elements'] or actual['blocks'] != expected:
        raise ValueError('Saved integrated DOCX differs from full current plan or has unmanaged content')
    package = read_package(source_docx)
    parts = {info.filename: data for info, data in package}
    # Such parts can retain omitted answers or replay an external binding. Do not
    # silently copy a hidden manuscript; this managed format does not use them.
    for name, data in parts.items():
        if (name.startswith(('customXml/', 'word/embeddings/', 'word/comments'))
                or name.endswith('vbaProject.bin')):
            raise ValueError('Unsupported hidden/embedded content needs explicit review: ' + name)
        if name in {'word/footnotes.xml', 'word/endnotes.xml'}:
            if E.fromstring(data).xpath('.//w:t', namespaces=NS):
                raise ValueError('Content-bearing notes need an explicit volume mapping: ' + name)
    root = E.fromstring(parts['word/document.xml'])
    body = root.find('w:body', NS)
    sections = body.findall('w:sectPr', NS)
    if len(sections) != 1 or body[-1] is not sections[0]:
        raise ValueError('Exactly one final section property block is required')
    if body.xpath('.//w:pPr/w:sectPr|.//w:dataBinding', namespaces=NS):
        raise ValueError('Internal sections or data-bound controls need explicit split review')
    indexed = block_index(body)
    return groups, package, root, indexed, sections[0]


def volume_xml(root, indexed, section, ids):
    result = deepcopy(root)
    body = result.find('w:body', NS)
    for child in list(body):
        body.remove(child)
    for bid in ids:
        body.append(deepcopy(indexed[bid]))
    body.append(deepcopy(section))
    return E.tostring(result, encoding='UTF-8', xml_declaration=True, standalone=True)


def _resolve(base, name):
    path = Path(name)
    return path.resolve() if path.is_absolute() else (Path(base) / path).resolve()


def verify_split(manifest, base='.'):
    """Read-only saved-output check. Does not substitute for J/K/R reviews."""
    errors, protected = [], []
    try:
        if (manifest.get('schema_version') != 1 or manifest.get('kind') != 'INTEGRATED_PLUS_FIVE_DOCX'
                or manifest.get('delivery_mode') != 'integrated_plus_five_docx'):
            raise ValueError('Unsupported split manifest')
        name_base = validate_base(manifest['filename_base'])
        source = _resolve(base, manifest['source_docx']['path'])
        plan_path = _resolve(base, manifest['plan']['path'])
        protected.extend([str(source), str(plan_path)])
        if sha(source.read_bytes()) != manifest['source_docx']['sha256']:
            raise ValueError('Source DOCX hash changed')
        if sha(plan_path.read_bytes()) != manifest['plan']['sha256']:
            raise ValueError('Canonical plan hash changed')
        plan = json.loads(plan_path.read_text(encoding='utf-8-sig'))
        groups, package, root, indexed, section = read_source(source, plan)
        source_parts = {i.filename: data for i, data in package}
        volumes = manifest['volumes']
        if [v.get('kind') for v in volumes] != list(VOLUME_KINDS):
            raise ValueError('Five volume kinds/order must match exactly')
        if manifest.get('source_coverage') != [b['id'] for b in plan['blocks']]:
            raise ValueError('Source coverage manifest mismatch')
        integrated = manifest['integrated_docx']
        integrated_path = _resolve(base, integrated['path'])
        protected.append(str(integrated_path))
        full_filename = name_base + '_전체통합본.docx'
        if (integrated_path in {source, plan_path} or integrated_path.name != full_filename
                or integrated.get('filename') != full_filename
                or integrated.get('sha256') != manifest['source_docx']['sha256']
                or integrated_path.read_bytes() != source.read_bytes()):
            raise ValueError('Integrated delivery must be a correctly named exact saved-source copy')
        seen_paths = {source, plan_path, integrated_path}
        for number, (kind, label, volume) in enumerate(zip(VOLUME_KINDS, VOLUME_LABELS, volumes), 1):
            target = _resolve(base, volume['path'])
            protected.append(str(target))
            filename = f'{name_base}_{number:02d}_{label}.docx'
            if target in seen_paths or target.name != filename or volume.get('filename') != filename:
                raise ValueError('Volume path collision or noncanonical filename: ' + kind)
            seen_paths.add(target)
            if sha(target.read_bytes()) != volume['sha256']:
                raise ValueError('Saved volume hash mismatch: ' + kind)
            if volume.get('block_ids') != groups[kind]:
                raise ValueError('Volume block coverage mismatch: ' + kind)
            hashes = {bid: block_sha(indexed[bid]) for bid in groups[kind]}
            if volume.get('block_sha256') != hashes:
                raise ValueError('Source block hash manifest mismatch: ' + kind)
            saved = read_package(target)
            saved_parts = {i.filename: data for i, data in saved}
            if set(saved_parts) != set(source_parts):
                raise ValueError('Package parts changed: ' + kind)
            if any(saved_parts[n] != b for n, b in source_parts.items() if n != 'word/document.xml'):
                raise ValueError('Non-body formatting/assets/fields changed: ' + kind)
            # Comparing the whole body also detects added answer text or unmanaged
            # paragraphs, even if an attacker recomputes the volume file hash.
            expected_root = E.fromstring(volume_xml(root, indexed, section, groups[kind]))
            saved_root = E.fromstring(saved_parts['word/document.xml'])
            if E.tostring(saved_root, method='c14n') != E.tostring(expected_root, method='c14n'):
                raise ValueError('Preserved body XML mismatch: ' + kind)
        delivery_zip = manifest['delivery_zip']
        zip_path = _resolve(base, delivery_zip['path'])
        protected.append(str(zip_path))
        if (zip_path in seen_paths or zip_path.name != name_base + '.zip'
                or delivery_zip.get('filename') != zip_path.name
                or delivery_zip.get('sha256') != sha(zip_path.read_bytes())):
            raise ValueError('Delivery ZIP path/name/hash mismatch')
        entries = [integrated] + volumes
        expected_names = [entry['filename'] for entry in entries]
        expected_hashes = {entry['filename']: entry['sha256'] for entry in entries}
        if delivery_zip.get('docx_entry_sha256') != expected_hashes:
            raise ValueError('Delivery ZIP entry hash manifest mismatch')
        with ZipFile(zip_path) as archive:
            if archive.namelist() != expected_names or archive.testzip() is not None:
                raise ValueError('Delivery ZIP must contain exactly six ordered DOCX entries; no PDFs, duplicate or unsafe paths')
            for entry in entries:
                if archive.read(entry['filename']) != _resolve(base, entry['path']).read_bytes():
                    raise ValueError('Delivery ZIP bytes differ from checked DOCX: ' + entry['filename'])
        return {'status': 'SPLIT_CONTENT_MATCH', 'errors': [], 'protected_paths': protected,
                'checked_volumes': list(VOLUME_KINDS), 'checked_docx_count': 6,
                'integrated_copy': 'BYTE_IDENTICAL', 'source_block_count': len(indexed),
                'delivery_zip': 'SIX_DOCX_EXACT_BYTES',
                'content_and_format_preservation': 'EXACT_PARTITION',
                'visual_review': 'NOT_PERFORMED', 'release_authorization': 'NOT_PERFORMED'}
    except (ValueError, KeyError, TypeError, AttributeError, OSError, BadZipFile, E.XMLSyntaxError) as exc:
        errors.append({'code': 'SPLIT_PRESERVATION', 'message': str(exc)})
        return {'status': 'FAIL', 'errors': errors, 'protected_paths': protected,
                'visual_review': 'NOT_PERFORMED', 'release_authorization': 'NOT_PERFORMED'}


def export(source_docx, plan_path, output_dir, filename_base):
    source_docx, plan_path = Path(source_docx).resolve(), Path(plan_path).resolve()
    output_dir = Path(output_dir).resolve()
    name_base = validate_base(filename_base)
    plan_bytes, source_bytes = plan_path.read_bytes(), source_docx.read_bytes()
    plan = json.loads(plan_bytes.decode('utf-8-sig'))
    groups, package, root, indexed, section = read_source(source_docx, plan)
    targets = [output_dir / f'{name_base}_{i:02d}_{label}.docx'
               for i, label in enumerate(VOLUME_LABELS, 1)]
    integrated_path = output_dir / f'{name_base}_전체통합본.docx'
    zip_path = output_dir / f'{name_base}.zip'
    manifest_path = output_dir / MANIFEST_NAME
    if any(p.exists() for p in [integrated_path, *targets, zip_path, manifest_path]):
        raise ValueError('Split export is new-only; choose a new release directory')
    if any(p in {source_docx, plan_path} for p in [integrated_path, *targets]):
        raise ValueError('Outputs must not replace an input')
    manifest = {'schema_version': 1, 'kind': 'INTEGRATED_PLUS_FIVE_DOCX',
                'delivery_mode': 'integrated_plus_five_docx', 'filename_base': name_base,
                'source_docx': {'path': str(source_docx), 'sha256': sha(source_bytes)},
                'plan': {'path': str(plan_path), 'sha256': sha(plan_bytes)},
                'integrated_docx': {'path': str(integrated_path), 'filename': integrated_path.name,
                                    'sha256': sha(source_bytes)},
                'source_coverage': [b['id'] for b in plan['blocks']],
                'cover_policy': 'PRESERVED_ONCE_IN_READING', 'volumes': [],
                'visual_review': 'NOT_PERFORMED', 'release_authorization': 'NOT_PERFORMED'}
    output_dir.mkdir(parents=True, exist_ok=True)
    created = []
    try:
        with integrated_path.open('xb') as stream:
            created.append(integrated_path)
            stream.write(source_bytes)
        for kind, target in zip(VOLUME_KINDS, targets):
            xml = volume_xml(root, indexed, section, groups[kind])
            with target.open('xb') as stream:
                created.append(target)
                with ZipFile(stream, 'w') as archive:
                    for info, original in package:
                        archive.writestr(info, xml if info.filename == 'word/document.xml' else original)
            manifest['volumes'].append({'kind': kind, 'filename': target.name, 'path': str(target),
                                       'sha256': sha(target.read_bytes()), 'block_ids': groups[kind],
                                       'block_sha256': {bid: block_sha(indexed[bid]) for bid in groups[kind]}})
        if source_docx.read_bytes() != source_bytes or plan_path.read_bytes() != plan_bytes:
            raise ValueError('An input changed during export')
        entries = [manifest['integrated_docx']] + manifest['volumes']
        with zip_path.open('xb') as stream:
            created.append(zip_path)
            with ZipFile(stream, 'w', compression=ZIP_DEFLATED) as archive:
                for entry in entries:
                    archive.writestr(entry['filename'], Path(entry['path']).read_bytes())
        manifest['delivery_zip'] = {'path': str(zip_path), 'filename': zip_path.name,
                                    'sha256': sha(zip_path.read_bytes()),
                                    'docx_entry_sha256': {entry['filename']: entry['sha256'] for entry in entries}}
        validation = verify_split(manifest)
        if validation['status'] != 'SPLIT_CONTENT_MATCH':
            raise ValueError(str(validation['errors']))
        manifest['saved_validation'] = validation
        with manifest_path.open('x', encoding='utf-8') as stream:
            created.append(manifest_path)
            json.dump(manifest, stream, ensure_ascii=False, indent=2)
    except Exception:
        # Remove only paths successfully created by this invocation in this exact
        # output directory. Existing files and authoritative inputs are untouched.
        for path in reversed(created):
            if path.parent == output_dir and path.exists():
                path.unlink()
        raise
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    make = sub.add_parser('export', help='Create six DOCX files, their delivery ZIP, and an internal manifest')
    make.add_argument('docx', type=Path)
    make.add_argument('plan', type=Path)
    make.add_argument('output_dir', type=Path)
    make.add_argument('--base', required=True)
    check = sub.add_parser('verify', help='Check manifest against actual saved inputs and volumes')
    check.add_argument('manifest', type=Path)
    args = parser.parse_args()
    if args.command == 'export':
        result = export(args.docx, args.plan, args.output_dir, args.base)
        print(json.dumps({'status': 'SPLIT_CONTENT_MATCH', 'manifest': str(args.output_dir / MANIFEST_NAME),
                          'delivery_zip': result['delivery_zip']['path'],
                          'integrated_docx': result['integrated_docx']['path'],
                          'volumes': [v['path'] for v in result['volumes']],
                          'visual_review': 'NOT_PERFORMED'}, ensure_ascii=False))
    else:
        result = verify_split(json.loads(args.manifest.read_text(encoding='utf-8-sig')), args.manifest.parent)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        raise SystemExit(0 if result['status'] == 'SPLIT_CONTENT_MATCH' else 1)


if __name__ == '__main__':
    main()
