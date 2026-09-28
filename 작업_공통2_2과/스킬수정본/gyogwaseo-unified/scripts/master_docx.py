"""Hash-bound MASTER role bank and conservative DOCX package writer.

The layout plan is a sequence of tagged blocks with role-based paragraphs/tables.
Only template run indices supply formatting. No arbitrary fonts or sizes in input.
Create copies the reference package; update replaces explicitly named blocks in
the latest file after checking its expected SHA-256. Unknown or duplicate tags fail.
Saved package parts other than document.xml are retained byte-for-byte, except
the explicitly approved cover-logo relationship migration when first inserted.
"""
import argparse
from copy import deepcopy
import hashlib
import json
import os
from pathlib import Path
import posixpath
import re
import uuid
from zipfile import ZipFile

from lxml import etree as E

W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
REL = 'http://schemas.openxmlformats.org/package/2006/relationships'
R = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
A = 'http://schemas.openxmlformats.org/drawingml/2006/main'
NS = {'w': W}
XML_SPACE = '{http://www.w3.org/XML/1998/namespace}space'
ASSETS = Path(__file__).resolve().parent.parent / 'assets'


def tag(name):
    return f'{{{W}}}{name}'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def set_property(parent, name, attrs):
    element = parent.find(tag(name))
    if element is None:
        element = E.SubElement(parent, tag(name))
    for key, value in attrs.items():
        element.set(tag(key), str(value))
    return element


PPR_ORDER = ['pStyle', 'keepNext', 'keepLines', 'pageBreakBefore', 'framePr',
             'widowControl', 'numPr', 'suppressLineNumbers', 'pBdr', 'shd', 'tabs',
             'suppressAutoHyphens', 'kinsoku', 'wordWrap', 'overflowPunct', 'topLinePunct',
             'autoSpaceDE', 'autoSpaceDN', 'bidi', 'adjustRightInd', 'snapToGrid', 'spacing',
             'ind', 'contextualSpacing', 'mirrorIndents', 'suppressOverlap', 'jc',
             'textDirection', 'textAlignment', 'textboxTightWrap', 'outlineLvl',
             'divId', 'cnfStyle', 'rPr', 'sectPr', 'pPrChange']


def order_ppr(ppr):
    children = list(ppr)
    for element in children:
        ppr.remove(element)
    for element in sorted(children, key=lambda e: PPR_ORDER.index(E.QName(e).localname)
                          if E.QName(e).localname in PPR_ORDER else len(PPR_ORDER)):
        ppr.append(element)


def read_package(path):
    with ZipFile(path) as z:
        names = z.namelist()
        if len(names) != len(set(names)):
            raise ValueError('Duplicate ZIP entry')
        if z.testzip() is not None:
            raise ValueError('Corrupt DOCX package')
        return [(entry, z.read(entry.filename)) for entry in z.infolist()]


class RoleBank:
    def __init__(self, assets=ASSETS):
        self.assets = Path(assets)
        self.contract = json.loads((self.assets / 'layout-contract.json').read_text(encoding='utf-8'))
        self.circled = self.contract.get('circled_number_typography')
        if self.circled is not None and self.circled != {
                'characters': '①②③④⑤',
                'font': '맑은 고딕', 'scope': 'circled-glyphs-only'}:
            raise ValueError('Unknown circled-number typography contract')
        if self.contract.get('explicit_role_size_overrides_pt'):
            raise ValueError('Approved sizes must be normalized in the executable MASTER, not runtime-only overrides')
        self.reference = self.assets / self.contract['reference']['filename']
        if sha(self.reference.read_bytes()) != self.contract['reference']['sha256']:
            raise ValueError('MASTER hash mismatch: do not guess role positions')
        self.package = read_package(self.reference)
        self.root = E.fromstring(dict((i.filename, b) for i, b in self.package)['word/document.xml'])
        self.paragraphs = self.root.findall('.//w:p', NS)
        self.tables = self.root.findall('.//w:tbl', NS)
        self.additional_paragraphs = {}
        for role, data in self.contract.get('additional_paragraph_roles', {}).items():
            path = (self.assets / data['filename']).resolve()
            if path.parent != self.assets.resolve() or sha(path.read_bytes()) != data['sha256']:
                raise ValueError('Additional role asset location/hash mismatch')
            paragraph = E.fromstring(path.read_bytes())
            if paragraph.tag != tag('p'):
                raise ValueError('Additional paragraph role must contain one w:p')
            self.additional_paragraphs[role] = paragraph
        for role, data in self.contract['roles'].items():
            p = self.paragraphs[data['locator']['zero_based_index']]
            text = ''.join(p.xpath('.//w:t/text()', namespaces=NS))
            if sha(text.encode('utf-8')) != data['source_text_sha256']:
                raise ValueError(f'Role locator mismatch: {role}')

    def paragraph(self, role, runs=None, page_break_before=None, chain=None):
        derived = self.contract.get('derived_roles', {}).get(role)
        base_role = derived.get('base_role', role) if derived else role
        if base_role not in self.contract['roles'] and base_role not in self.additional_paragraphs:
            raise ValueError(f'Unknown paragraph role: {role}')
        template = (self.additional_paragraphs[base_role] if base_role in self.additional_paragraphs
                    else self.paragraphs[self.contract['roles'][base_role]['locator']['zero_based_index']])
        if role in self.contract.get('static_paragraph_roles', []):
            if role != 'cover_logo' or runs is not None or page_break_before is not None or chain is not None:
                raise ValueError('Approved cover_logo is a static paragraph without content or layout overrides')
            return deepcopy(template)
        p = E.Element(tag('p'))
        ppr = template.find('w:pPr', NS)
        ppr = deepcopy(ppr) if ppr is not None else E.Element(tag('pPr'))
        p.append(ppr)
        if page_break_before is not None:
            set_property(ppr, 'pageBreakBefore', {'val': int(bool(page_break_before))})
        if chain is not None:
            set_property(ppr, 'keepNext', {'val': int(bool(chain))})
        if role == 'given_box':
            d = derived
            set_property(ppr, 'ind', d['indent_twips'])
            set_property(ppr, 'spacing', d['spacing_twips'])
            borders = ppr.find('w:pBdr', NS)
            if borders is not None:
                ppr.remove(borders)
            borders = E.Element(tag('pBdr'))
            # pBdr belongs before shading/spacing in CT_PPr ordering.
            at = next((i for i, el in enumerate(ppr) if E.QName(el).localname in {'shd', 'tabs', 'spacing', 'ind'}), len(ppr))
            ppr.insert(at, borders)
            b = d['border']
            for side in ('top', 'left', 'bottom', 'right'):
                set_property(borders, side, {'val': b['style'], 'sz': b['size_eighth_pt'],
                                             'space': b['space_pt'], 'color': b['color']})
        if role == 'given_label':
            set_property(ppr, 'ind', {'left': derived['left_twips']})
            set_property(ppr, 'spacing', {'after': derived['after_twips']})
        if role == 'mock_question_prompt_spaced':
            spacing = ppr.find('w:spacing', NS)
            if spacing is None:
                spacing = E.SubElement(ppr, tag('spacing'))
            spacing.set(tag('before'), str(derived['before_twips']))
        if derived and 'paragraph_spacing_twips' in derived:
            # Only the approved derived-role contract controls this override.
            # Merge before/after so the base line spacing remains unchanged.
            set_property(ppr, 'spacing', derived['paragraph_spacing_twips'])
        compact_font = derived.get('compact_font') if derived else None
        def compact_size(properties):
            if not compact_font or properties is None:
                return
            if compact_font != {'decrement_half_points': 1, 'minimum_half_points': 17}:
                raise ValueError('Compact type is limited to 0.5pt with an 8.5pt floor')
            for name in ('sz', 'szCs'):
                node = properties.find('w:' + name, NS)
                if node is not None:
                    size = int(node.get(tag('val')))
                    if size > 17:
                        node.set(tag('val'), str(size - 1))
        compact_size(ppr.find('w:rPr', NS))
        order_ppr(ppr)
        templates = template.findall('w:r', NS)
        if runs is None:
            if templates:
                raise ValueError(f'Explicit content required for nonempty role: {role}')
            return p
        if not isinstance(runs, list):
            raise ValueError('runs must be a list of {run,text}')
        for item in runs:
            index, text = item['run'], item['text']
            format_role = item.get('format_role')
            run_templates = templates
            if format_role is not None:
                if format_role not in self.contract.get('allowed_inline_format_roles', {}).get(role, []):
                    raise ValueError(f'Unapproved inline format role for {role}: {format_role}')
                if format_role in self.additional_paragraphs:
                    format_template = self.additional_paragraphs[format_role]
                else:
                    locator = self.contract['roles'][format_role]['locator']['zero_based_index']
                    format_template = self.paragraphs[locator]
                run_templates = format_template.findall('w:r', NS)
            if type(index) is not int or index < 0 or index >= len(run_templates) or not isinstance(text, str):
                raise ValueError(f'Invalid run reference/content for {role}')
            rpr = run_templates[index].find('w:rPr', NS)
            rpr = deepcopy(rpr) if rpr is not None else E.Element(tag('rPr'))
            if role == 'given_label':
                set_property(rpr, 'b', {'val': 1})
                set_property(rpr, 'color', {'val': derived['color']})
                set_property(rpr, 'sz', {'val': int(derived['size_pt'] * 2)})
                set_property(rpr, 'szCs', {'val': int(derived['size_pt'] * 2)})
            if 'underline' in item:
                if item['underline'] is not True or role not in self.contract.get('underline_permitted_roles', []):
                    raise ValueError(f'Unapproved inline underline for {role}')
                set_property(rpr, 'u', {'val': 'single'})
            compact_size(rpr)
            # Only the circled glyph uses the approved symbol font. Split runs
            # without changing text, punctuation, NBSP, emphasis or body fonts.
            segments = re.findall(r'[①-⑤]+|[^①-⑤]+', text) if self.circled and text else [text]
            for segment in segments:
                r = E.SubElement(p, tag('r'))
                properties = deepcopy(rpr)
                if self.circled and segment and segment[0] in self.circled['characters']:
                    fonts = properties.find('w:rFonts', NS)
                    if fonts is not None:
                        properties.remove(fonts)
                    fonts = E.Element(tag('rFonts'))
                    for slot in ('ascii', 'hAnsi', 'eastAsia', 'cs'):
                        fonts.set(tag(slot), self.circled['font'])
                    fonts.set(tag('hint'), 'eastAsia')
                    at = 1 if len(properties) and properties[0].tag == tag('rStyle') else 0
                    properties.insert(at, fonts)
                r.append(properties)
                # Newlines/tabs remain semantic nodes, never literal controls.
                for n, line in enumerate(segment.split('\n')):
                    if n:
                        E.SubElement(r, tag('br'))
                    for k, fragment in enumerate(line.split('\t')):
                        if k:
                            E.SubElement(r, tag('tab'))
                        t = E.SubElement(r, tag('t'))
                        t.set(XML_SPACE, 'preserve')
                        t.text = fragment
        return p

    def table(self, role, entries):
        spec = self.contract['table_roles'].get(role)
        if spec is None:
            raise ValueError('Unknown table role')
        prototype = self.tables[spec['zero_based_index']]
        if role == 'cover_topic_box':
            if len(entries) != 2:
                raise ValueError('Cover topic box needs one English and one Korean paragraph')
            result = deepcopy(prototype)
            cell = result.find('.//w:tc', NS)
            for p in cell.findall('w:p', NS):
                cell.remove(p)
            for p_role, text in zip(('cover_topic_first', 'cover_topic_korean'), entries):
                cell.append(self.paragraph(p_role, [{'run': 0, 'text': text}]))
            return result
        if role == 'workbook_answer_grid':
            if not isinstance(entries, list) or not entries:
                raise ValueError('Answer grid needs nonempty entries')
            if any(not isinstance(item, dict) or not isinstance(item.get('runs'), list)
                   or not item['runs'] for item in entries):
                raise ValueError('Answer grid entries require workbook_word_answer runs')
            result = deepcopy(prototype)
            first_row = deepcopy(result.find('w:tr', NS))
            for row in result.findall('w:tr', NS):
                result.remove(row)
            for start in range(0, len(entries), 3):
                row = deepcopy(first_row)
                for node in row.iter():
                    for name in list(node.attrib):
                        if E.QName(name).localname in {'paraId', 'textId'}:
                            del node.attrib[name]
                cells = row.findall('w:tc', NS)
                if len(cells) != 3:
                    raise ValueError('Expected three cells in answer grid prototype')
                for offset, cell in enumerate(cells):
                    for paragraph in cell.findall('w:p', NS):
                        cell.remove(paragraph)
                    index = start + offset
                    runs = entries[index]['runs'] if index < len(entries) else []
                    cell.append(self.paragraph('workbook_word_answer', runs, chain=False))
                result.append(row)
            return result
        if not isinstance(entries, list) or not entries or any(not isinstance(s, str) or not s.strip() for s in entries):
            raise ValueError('Word table entries must be nonempty strings')
        result = deepcopy(prototype)
        first_row = deepcopy(result.find('w:tr', NS))
        for row in result.findall('w:tr', NS):
            result.remove(row)
        for start in range(0, len(entries), 2):
            row = deepcopy(first_row)
            for node in row.iter():
                for name in list(node.attrib):
                    if E.QName(name).localname in {'paraId', 'textId'}:
                        del node.attrib[name]
            trpr = row.find('w:trPr', NS)
            if trpr is None:
                trpr = E.Element(tag('trPr'))
                row.insert(0, trpr)
            set_property(trpr, 'cantSplit', {})
            cells = row.findall('w:tc', NS)
            if len(cells) != 4:
                raise ValueError('Expected four cells in word table prototype')
            for offset, cell in enumerate(cells):
                for p in cell.findall('w:p', NS):
                    cell.remove(p)
                item_index = start + offset // 2
                if offset % 2 == 0:
                    value = f'{item_index + 1}. {entries[item_index]}' if item_index < len(entries) else ''
                    cell.append(self.paragraph('workbook_word_cell', [{'run': 0, 'text': value}]))
                else:
                    cell.append(self.paragraph('workbook_word_answer_space'))
            result.append(row)
        return result

    def block(self, data):
        block_id = data.get('id')
        if not isinstance(block_id, str) or not block_id or len(block_id) > 180:
            raise ValueError('Each block needs a stable ID of at most 180 characters')
        sdt = E.Element(tag('sdt'))
        pr = E.SubElement(sdt, tag('sdtPr'))
        set_property(pr, 'tag', {'val': f'gyogwaseo:{block_id}'})
        content = E.SubElement(sdt, tag('sdtContent'))
        if not data.get('elements'):
            raise ValueError('An empty replacement block is not an authorized deletion')
        for element in data['elements']:
            if element.get('kind', 'paragraph') == 'paragraph':
                content.append(self.paragraph(element['role'], element.get('runs'),
                                              element.get('page_break_before'), element.get('chain')))
            elif element['kind'] == 'table':
                content.append(self.table(element['role'], element['entries']))
            else:
                raise ValueError('Unknown element kind')
        return sdt


def block_index(body):
    result = {}
    for sdt in body.findall('w:sdt', NS):
        value = sdt.find('w:sdtPr/w:tag', NS)
        name = value.get(tag('val')) if value is not None else None
        if name and name.startswith('gyogwaseo:'):
            name = name[len('gyogwaseo:'):]
            if name in result:
                raise ValueError(f'Duplicate saved block ID: {name}')
            result[name] = sdt
    return result


def approved_cover_relationships(bank, package, plan):
    """Import only the approved cover-logo link; never replace existing media."""
    if not any(e.get('role') == 'cover_logo' for b in plan['blocks'] for e in b['elements']):
        return {}
    record = bank.contract.get('approved_body_images', {}).get('cover_logo')
    if not isinstance(record, dict):
        raise ValueError('Missing approved cover-logo image relationship')
    rid, target = record.get('relationship_id'), record.get('target')
    if rid != 'rIdCoverLogo' or target != 'media/image1.png':
        raise ValueError('Unapproved cover-logo relationship or target')
    media = posixpath.normpath(posixpath.join('word', target))
    parts = dict((info.filename, data) for info, data in package)
    reference = dict((info.filename, data) for info, data in bank.package)
    if (media not in parts or media not in reference or
            sha(parts[media]) != record.get('sha256') or parts[media] != reference[media]):
        raise ValueError('Existing cover-logo media hash differs from the approved original')
    relpart = 'word/_rels/document.xml.rels'
    if relpart not in parts or relpart not in reference:
        raise ValueError('Missing document relationships for approved cover logo')
    expected = E.fromstring(reference[relpart])
    candidates = [r for r in expected if r.get('Id') == rid]
    if (len(candidates) != 1 or candidates[0].get('Target') != target or
            candidates[0].get('Type') != R + '/image' or
            candidates[0].get('TargetMode', 'Internal') != 'Internal'):
        raise ValueError('MASTER cover-logo relationship differs from its approved contract')
    template = bank.paragraph('cover_logo')
    if template.xpath('.//a:blip/@r:embed', namespaces={'a': A, 'r': R}) != [rid]:
        raise ValueError('MASTER cover-logo drawing is not bound to the approved relationship')
    actual = E.fromstring(parts[relpart])
    existing = [r for r in actual if r.get('Id') == rid]
    if len(existing) > 1:
        raise ValueError('Conflicting duplicate cover-logo relationship ID')
    if existing:
        if (existing[0].get('Target') != target or existing[0].get('Type') != R + '/image' or
                existing[0].get('TargetMode', 'Internal') != 'Internal'):
            raise ValueError('Conflicting cover-logo relationship ID: existing target/type must be preserved')
        return {}
    actual.append(deepcopy(candidates[0]))
    return {relpart: E.tostring(actual, encoding='UTF-8', xml_declaration=True, standalone=True)}


def write(plan, target, mode='create', expected_sha256=None, assets=ASSETS):
    target = Path(target).resolve()
    bank = RoleBank(assets)
    if target == bank.reference.resolve():
        raise ValueError('Cannot overwrite retained MASTER')
    if target.suffix.lower() != '.docx':
        raise ValueError('DOCX output extension required')
    if not isinstance(plan.get('blocks'), list) or not plan['blocks']:
        raise ValueError('A nonempty block plan is required')
    ids = [b['id'] for b in plan['blocks']]
    if len(ids) != len(set(ids)):
        raise ValueError('Duplicate input block ID')
    if mode == 'create':
        if target.exists():
            raise ValueError('Create refuses an existing file; use a reviewed patch')
        package = bank.package
        root = deepcopy(bank.root)
        body = root.find('w:body', NS)
        section = deepcopy(body.find('w:sectPr', NS))
        for el in list(body):
            body.remove(el)
        for b in plan['blocks']:
            body.append(bank.block(b))
        body.append(section)
        untouched = {}
    elif mode == 'patch':
        if not expected_sha256 or not target.is_file() or sha(target.read_bytes()) != expected_sha256:
            raise ValueError('Current DOCX version changed or expected SHA-256 is missing')
        package = read_package(target)
        parts = dict((i.filename, b) for i, b in package)
        root = E.fromstring(parts['word/document.xml'])
        body = root.find('w:body', NS)
        existing = block_index(body)
        untouched = {key: E.tostring(value) for key, value in existing.items() if key not in ids}
        for b in plan['blocks']:
            insert_before, insert_after = b.get('insert_before'), b.get('insert_after')
            if b['id'] in existing:
                if insert_before is not None or insert_after is not None:
                    raise ValueError('Existing block cannot be moved by a replacement patch')
                body.replace(existing[b['id']], bank.block(b))
            else:
                if (insert_before is None) == (insert_after is None):
                    raise ValueError('Unknown patch block: supply one verified insertion anchor')
                current = block_index(body)
                anchor = insert_before if insert_before is not None else insert_after
                if anchor not in current:
                    raise ValueError('Insertion anchor not found in current DOCX')
                at = body.index(current[anchor]) + (1 if insert_after is not None else 0)
                body.insert(at, bank.block(b))
        if any(E.tostring(block_index(body)[key]) != value for key, value in untouched.items()):
            raise ValueError('Untargeted block changed')
    else:
        raise ValueError('Mode must be create or patch')
    part_updates = approved_cover_relationships(bank, package, plan)
    xml = E.tostring(root, encoding='UTF-8', xml_declaration=True, standalone=True)
    target.parent.mkdir(parents=True, exist_ok=True)
    tmp = target.parent / f'gyogwaseo-{uuid.uuid4().hex}.docx'
    created = False
    try:
        # Exclusive creation, one attempt. tempfile.mkstemp can loop on Windows
        # PermissionError when an ACL denies writes but os.access says otherwise.
        with tmp.open('xb') as stream:
            created = True
            with ZipFile(stream, 'w') as z:
                for info, content in package:
                    z.writestr(info, xml if info.filename == 'word/document.xml'
                               else part_updates.get(info.filename, content))
        saved = dict((i.filename, b) for i, b in read_package(tmp))
        for info, original in package:
            if info.filename != 'word/document.xml' and saved[info.filename] != part_updates.get(info.filename, original):
                raise ValueError('Non-body package part changed')
        saved_root = E.fromstring(saved['word/document.xml'])
        saved_ids = block_index(saved_root.find('w:body', NS))
        if not set(ids) <= set(saved_ids):
            raise ValueError('Saved block missing')
        if mode == 'patch' and sha(target.read_bytes()) != expected_sha256:
            raise ValueError('Concurrent DOCX change detected before saving')
        if mode == 'create' and target.exists():
            raise ValueError('Output appeared while authoring; refusing replacement')
        os.replace(tmp, target)
    finally:
        if created and tmp.exists():
            tmp.unlink()
    return {'output': str(target), 'sha256': sha(target.read_bytes()),
            'changed_blocks': ids, 'untargeted_block_count': len(untouched),
            'other_package_parts': ('PRESERVED_EXCEPT_APPROVED_COVER_IMAGE_RELATIONSHIP' if part_updates
                                    else 'PRESERVED_BYTE_FOR_BYTE'),
            'approved_relationship_migrations': list(part_updates),
            'visual_review': 'NOT_PERFORMED', 'semantic_review': 'NOT_PERFORMED'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('plan', type=Path)
    parser.add_argument('output', type=Path)
    parser.add_argument('--mode', choices=['create', 'patch'], default='create')
    parser.add_argument('--expected-sha256')
    args = parser.parse_args()
    plan = json.loads(args.plan.read_text(encoding='utf-8-sig'))
    print(json.dumps(write(plan, args.output, args.mode, args.expected_sha256), ensure_ascii=False))


if __name__ == '__main__':
    main()
