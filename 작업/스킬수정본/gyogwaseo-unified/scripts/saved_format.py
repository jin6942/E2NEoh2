"""Compare saved OOXML formatting with the approved plan and current MASTER.

The actual document is independently extracted, including style inheritance and
character spans. This checks stored formatting, not pagination, font availability,
linguistic correctness, or the semantic suitability of the supplied approved plan.
"""
from copy import deepcopy
import hashlib
import importlib.util
import json
from pathlib import Path
import posixpath
from zipfile import ZipFile

from lxml import etree as E

W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
R = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
NS = {'w': W, 'r': R}
BOOLEAN_R = {'b', 'bCs', 'i', 'iCs', 'caps', 'smallCaps', 'strike', 'dstrike',
             'outline', 'shadow', 'emboss', 'imprint', 'vanish', 'webHidden',
             'rtl', 'cs', 'noProof', 'snapToGrid'}
BOOLEAN_P = {'keepNext', 'keepLines', 'pageBreakBefore', 'widowControl',
             'contextualSpacing', 'suppressLineNumbers', 'bidi', 'wordWrap',
             'autoSpaceDE', 'autoSpaceDN', 'snapToGrid', 'suppressAutoHyphens'}
VOLATILE_ATTRS = {'paraId', 'textId', 'rsidR', 'rsidRPr', 'rsidP', 'rsidDel',
                  'rsidRDefault', 'rsidSect'}


def q(name):
    return '{' + W + '}' + name


def canonical_hash(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                    separators=(',', ':')).encode('utf-8')).hexdigest()


def xml_value(node):
    """Order-insensitive properties, without Word editing-session identifiers."""
    if node is None:
        return {}
    value = {E.QName(k).localname: v for k, v in node.attrib.items()
             if E.QName(k).localname not in VOLATILE_ATTRS}
    for child in node:
        key = E.QName(child).localname
        if key in {'pPrChange', 'rPrChange', 'tblPrChange', 'tcPrChange', 'trPrChange'}:
            raise ValueError('Tracked formatting changes require explicit review')
        item = xml_value(child)
        if key in value:
            old = value[key]
            value[key] = old + [item] if isinstance(old, list) else [old, item]
        else:
            value[key] = item
    return value


def merge(*values):
    result = {}
    for value in values:
        for key, item in value.items():
            result[key] = (merge(result[key], item)
                           if isinstance(item, dict) and isinstance(result.get(key), dict)
                           else deepcopy(item))
    return result


def flag(value):
    return str(value.get('val', '1')).lower() not in {'0', 'false', 'off', 'no'}


def normalized(props, kind):
    result = deepcopy(props)
    for name in ('pStyle', 'rStyle', 'rPr'):
        result.pop(name, None)
    bools = BOOLEAN_R if kind == 'run' else BOOLEAN_P
    defaults_true = {'snapToGrid'} if kind == 'run' else {'widowControl', 'wordWrap',
                                                         'autoSpaceDE', 'autoSpaceDN', 'snapToGrid'}
    for name in bools:
        result[name] = flag(result[name]) if name in result else name in defaults_true
    if kind == 'run':
        result.setdefault('color', {'val': '000000'})
        if result['color'].get('val', 'auto') == 'auto':
            result['color']['val'] = '000000'
        result['color']['val'] = result['color']['val'].upper()
        result.setdefault('u', {'val': 'none'})
        result.setdefault('vertAlign', {'val': 'baseline'})
    else:
        result['spacing'] = merge({'before': '0', 'after': '0', 'line': '240',
                                   'lineRule': 'auto'}, result.get('spacing', {}))
        result.setdefault('jc', {'val': 'left'})
    return result


class Styles:
    def __init__(self, package):
        if 'word/styles.xml' not in package:
            raise ValueError('Missing styles.xml; effective formatting is unverified')
        root = E.fromstring(package['word/styles.xml'])
        self.styles = {x.get(q('styleId')): x for x in root.findall('w:style', NS)}
        self.p_default = xml_value(root.find('w:docDefaults/w:pPrDefault/w:pPr', NS))
        self.r_default = xml_value(root.find('w:docDefaults/w:rPrDefault/w:rPr', NS))
        self.default = next((x.get(q('styleId')) for x in self.styles.values()
                             if x.get(q('type')) == 'paragraph' and x.get(q('default')) == '1'), None)
        self.default_table = next((x.get(q('styleId')) for x in self.styles.values()
                                   if x.get(q('type')) == 'table' and x.get(q('default')) == '1'), None)

    def chain(self, style_id):
        result, seen = [], set()
        while style_id:
            if style_id in seen:
                raise ValueError('Cyclic style inheritance')
            if style_id not in self.styles:
                raise ValueError('Unknown style: ' + style_id)
            seen.add(style_id)
            node = self.styles[style_id]
            result.insert(0, node)
            parent = node.find('w:basedOn', NS)
            style_id = parent.get(q('val')) if parent is not None else None
        return result

    def style_props(self, chain, kind, base=None):
        # OOXML character emphasis properties in styles are toggles. Direct
        # formatting, in contrast, sets their absolute on/off state.
        result = deepcopy(base or {})
        for style in chain:
            value = xml_value(style.find('w:' + kind, NS))
            if kind == 'rPr':
                for key in BOOLEAN_R & set(value):
                    if key in {'b', 'bCs', 'i', 'iCs', 'caps', 'smallCaps', 'strike',
                               'dstrike', 'outline', 'shadow', 'emboss', 'imprint', 'vanish'}:
                        if not flag(value[key]):
                            # False in a style leaves the inherited toggle
                            # unchanged; false in direct formatting disables it.
                            del value[key]
                            continue
                        old = flag(result[key]) if key in result else False
                        value[key] = {'val': '0' if old else '1'}
            result = merge(result, value)
        return result

    def table(self, table):
        ref = table.find('w:tblPr/w:tblStyle', NS)
        chain = self.chain(ref.get(q('val')) if ref is not None else self.default_table)
        if any(x.find('w:tblStylePr', NS) is not None for x in chain):
            raise ValueError('Conditional table styles are not approved in the common role tables')
        return {kind: self.style_props(chain, kind)
                for kind in ('tblPr', 'trPr', 'tcPr', 'pPr', 'rPr')}

    def paragraph(self, p, table_context=None):
        ctx = table_context or {}
        ref = p.find('w:pPr/w:pStyle', NS)
        chain = self.chain(ref.get(q('val')) if ref is not None else self.default)
        pp = merge(self.p_default, ctx.get('pPr', {}), self.style_props(chain, 'pPr'),
                   xml_value(p.find('w:pPr', NS)))
        rp = self.style_props(chain, 'rPr', merge(self.r_default, ctx.get('rPr', {})))
        return normalized(pp, 'paragraph'), rp

    def run(self, run, base):
        ref = run.find('w:rPr/w:rStyle', NS)
        inherited = self.style_props(self.chain(ref.get(q('val'))), 'rPr', base) if ref is not None else base
        return normalized(merge(inherited, xml_value(run.find('w:rPr', NS))), 'run')


def run_text(run):
    result = []
    for node in run.iter():
        name = E.QName(node).localname
        if node.tag == q('t'):
            result.append(node.text or '')
        elif node.tag == q('tab'):
            result.append('\t')
        elif node.tag in {q('br'), q('cr')}:
            result.append('\n' if node.get(q('type'), 'textWrapping') == 'textWrapping'
                          else '<' + node.get(q('type')) + '-break>')
        elif name in {'drawing', 'pict', 'object', 'fldChar', 'instrText', 'sym'}:
            result.append('<xml:' + canonical_hash(tree_record(node)) + '>')
    return ''.join(result)


def tree_record(node):
    """Canonical ancillary XML; namespace prefixes and rsid changes are immaterial."""
    return {'tag': node.tag,
            'attributes': {k: v for k, v in sorted(node.attrib.items())
                           if E.QName(k).localname not in VOLATILE_ATTRS},
            'text': node.text if node.text and (node.text.strip() or node.tag in {q('t'), q('instrText')}) else '',
            'children': [tree_record(x) for x in node
                         if E.QName(x).localname not in {'proofErr', 'lastRenderedPageBreak'}]}


def paragraph_record(p, styles, table_context=None):
    pp, base = styles.paragraph(p, table_context)
    spans = []
    for run in p.findall('.//w:r', NS):
        text = run_text(run)
        if not text:
            continue
        props = styles.run(run, base)
        if spans and spans[-1]['format'] == props:
            spans[-1]['text'] += text
        else:
            spans.append({'text': text, 'format': props})
    # The paragraph mark can affect line height even when the text is nonempty.
    mark = normalized(merge(base, xml_value(p.find('w:pPr/w:rPr', NS))), 'run')
    return {'kind': 'paragraph', 'properties': pp, 'spans': spans, 'paragraph_mark': mark}


def element_record(element, styles):
    if element.tag == q('p'):
        return paragraph_record(element, styles)
    if element.tag != q('tbl'):
        raise ValueError('Unsupported layout element: ' + E.QName(element).localname)
    ctx = styles.table(element)
    table_props = merge(ctx['tblPr'], xml_value(element.find('w:tblPr', NS)))
    table_props.pop('tblStyle', None)
    rows = []
    for row in element.findall('w:tr', NS):
        cells = []
        for cell in row.findall('w:tc', NS):
            if cell.find('w:tbl', NS) is not None:
                raise ValueError('Nested tables require explicit format review')
            cells.append({'properties': merge(ctx['tcPr'], xml_value(cell.find('w:tcPr', NS))),
                          'paragraphs': [paragraph_record(p, styles, ctx) for p in cell.findall('w:p', NS)]})
        rows.append({'properties': merge(ctx['trPr'], xml_value(row.find('w:trPr', NS))), 'cells': cells})
    grid = element.find('w:tblGrid', NS)
    return {'kind': 'table', 'properties': table_props,
            'grid': tree_record(grid) if grid is not None else None, 'rows': rows}


def relationships(package, part='word/document.xml'):
    relpath = posixpath.join(posixpath.dirname(part), '_rels', posixpath.basename(part) + '.rels')
    if relpath not in package:
        return {}
    result = {}
    for rel in E.fromstring(package[relpath]):
        target = rel.get('Target', '')
        result[rel.get('Id')] = {'type': rel.get('Type'), 'mode': rel.get('TargetMode', 'Internal'),
                                'target': posixpath.normpath(posixpath.join(posixpath.dirname(part), target))}
    return result


def body_image_resources(element, package):
    """Resolve body drawing links to image bytes, not just their relationship IDs."""
    image_ns = {'a': 'http://schemas.openxmlformats.org/drawingml/2006/main', 'r': R}
    rels = relationships(package)
    result = []
    for blip in element.xpath('.//a:blip', namespaces=image_ns):
        if blip.get('{' + R + '}link'):
            raise ValueError('External body images are not approved')
        rid = blip.get('{' + R + '}embed')
        rel = rels.get(rid)
        if (not rel or rel['mode'] != 'Internal' or rel['type'] != R + '/image' or
                rel['target'] not in package):
            raise ValueError('Missing or invalid embedded body image relationship')
        result.append({'relationship_id': rid, 'target': rel['target'],
                       'sha256': hashlib.sha256(package[rel['target']]).hexdigest()})
    return result


def section_record(section, package, styles):
    result = xml_value(section)
    rels = relationships(package)
    extras = []
    for kind in ('headerReference', 'footerReference'):
        result.pop(kind, None)
        for node in section.findall('w:' + kind, NS):
            rel = rels.get(node.get('{' + R + '}id'))
            if not rel or rel['mode'] != 'Internal' or rel['target'] not in package:
                raise ValueError('Missing or external header/footer part')
            target = rel['target']
            root = E.fromstring(package[target])
            content = [element_record(x, styles) for x in root if x.tag in {q('p'), q('tbl')}]
            resources = []
            for linked in relationships(package, target).values():
                resources.append({'type': linked['type'], 'mode': linked['mode'],
                                  'sha256': hashlib.sha256(package[linked['target']]).hexdigest()
                                  if linked['target'] in package else linked['target']})
            extras.append({'kind': kind, 'type': node.get(q('type'), 'default'),
                           'content': content, 'resources': sorted(resources, key=lambda x: str(x))})
    result['headers_footers'] = sorted(extras, key=lambda x: (x['kind'], x['type']))
    return result


def first_difference(expected, actual, path=''):
    if type(expected) is not type(actual):
        return {'property': path, 'expected': expected, 'actual': actual}
    if isinstance(expected, dict):
        if set(expected) != set(actual):
            return {'property': path + '/keys', 'expected': sorted(expected), 'actual': sorted(actual)}
        for key in expected:
            diff = first_difference(expected[key], actual[key], path + '/' + key)
            if diff:
                return diff
    elif isinstance(expected, list):
        if path.endswith('/spans'):
            left_text = ''.join(x['text'] for x in expected)
            right_text = ''.join(x['text'] for x in actual)
            if left_text != right_text:
                return {'property': path + '/text', 'expected': left_text, 'actual': right_text}
            # Align intervals by character offset, not by Word's run boundaries.
            # Adjacent equivalent runs may be split or merged during a save.
            left_i = right_i = left_end = right_end = offset = 0
            while offset < len(left_text):
                if left_end == offset:
                    left_end += len(expected[left_i]['text'])
                if right_end == offset:
                    right_end += len(actual[right_i]['text'])
                end = min(left_end, right_end)
                diff = first_difference(expected[left_i]['format'], actual[right_i]['format'], path + '/format')
                if diff:
                    return {**diff, 'character_start': offset, 'character_end': end,
                            'text_excerpt': left_text[offset:end][:120]}
                offset = end
                if offset == left_end:
                    left_i += 1
                if offset == right_end:
                    right_i += 1
            return None
        if len(expected) != len(actual):
            return {'property': path + '/count', 'expected': len(expected), 'actual': len(actual)}
        for i, (left, right) in enumerate(zip(expected, actual)):
            diff = first_difference(left, right, path + '/' + str(i))
            if diff:
                return diff
    elif expected != actual:
        return {'property': path, 'expected': expected, 'actual': actual}
    return None


def load_master():
    path = Path(__file__).with_name('master_docx.py')
    spec = importlib.util.spec_from_file_location('_saved_format_master', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def required_underline_errors(element, record):
    """Verify explicit target offsets against effective saved character formats."""
    required = element.get('required_underlines')
    if required is None:
        return []
    if record.get('kind') != 'paragraph' or not isinstance(required, list) or not required:
        return [{'code': 'INVALID_REQUIRED_UNDERLINES'}]
    coverage = []
    for span in record['spans']:
        value = span['format'].get('u', {}).get('val', 'none')
        coverage.extend([value not in {'none', '0', 'false', 'off'}] * len(span['text']))
    errors = []
    for target in required:
        if (not isinstance(target, list) or len(target) != 2
                or any(type(offset) is not int for offset in target)
                or not 0 <= target[0] < target[1] <= len(coverage)):
            errors.append({'code': 'INVALID_REQUIRED_UNDERLINE_RANGE', 'target': target})
        elif not all(coverage[target[0]:target[1]]):
            errors.append({'code': 'REQUIRED_TARGET_UNDERLINE_MISSING', 'target': target})
    return errors


def check_format(plan, saved, scope='full', assets=None):
    master = load_master()
    bank = master.RoleBank(assets) if assets is not None else master.RoleBank()
    expected_package = {i.filename: data for i, data in bank.package}
    with ZipFile(saved) as archive:
        actual_package = {i.filename: archive.read(i.filename) for i in archive.infolist()}
    expected_styles, actual_styles = Styles(expected_package), Styles(actual_package)
    root = E.fromstring(actual_package['word/document.xml'])
    body = root.find('w:body', NS)
    blocks = {}
    for sdt in body.findall('w:sdt', NS):
        node = sdt.find('w:sdtPr/w:tag', NS)
        name = node.get(q('val'), '') if node is not None else ''
        if name.startswith('gyogwaseo:'):
            blocks[name[len('gyogwaseo:'):]] = sdt.find('w:sdtContent', NS)
    errors, checked = [], []
    if scope == 'full':
        planned_ids = [x['id'] for x in plan['blocks']]
        if list(blocks) != planned_ids:
            errors.append({'code': 'FORMAT_BLOCK_ORDER_OR_COVERAGE'})
        for node in body:
            if node.tag == q('sectPr'):
                continue
            label = node.find('w:sdtPr/w:tag', NS) if node.tag == q('sdt') else None
            if label is None or not label.get(q('val'), '').startswith('gyogwaseo:'):
                errors.append({'code': 'FORMAT_UNMANAGED_BODY_CONTENT'})
                break
    for block in plan['blocks']:
        if block['id'] not in blocks:
            errors.append({'code': 'FORMAT_BLOCK_MISSING', 'block': block['id']})
            continue
        expected = bank.block(block).find('w:sdtContent', NS)
        actual = blocks[block['id']]
        if len(expected) != len(actual):
            errors.append({'code': 'FORMAT_ELEMENT_COUNT', 'block': block['id'],
                           'expected': len(expected), 'actual': len(actual)})
        for index, (left, right) in enumerate(zip(expected, actual)):
            try:
                actual_record = element_record(right, actual_styles)
                image_diff = first_difference(body_image_resources(left, expected_package),
                                              body_image_resources(right, actual_package))
                if image_diff:
                    errors.append({'code': 'BODY_IMAGE_RESOURCE_MISMATCH', 'block': block['id'],
                                   'element': index, **image_diff})
                diff = first_difference(element_record(left, expected_styles), actual_record)
                if diff:
                    errors.append({'code': 'SAVED_FORMAT_MISMATCH', 'block': block['id'],
                                    'element': index, 'role': block['elements'][index]['role'], **diff})
                for error in required_underline_errors(block['elements'][index], actual_record):
                    errors.append({**error, 'block': block['id'], 'element': index,
                                   'role': block['elements'][index]['role']})
            except ValueError as exc:
                errors.append({'code': 'UNVERIFIED_SAVED_FORMAT', 'block': block['id'],
                               'element': index, 'reason': str(exc)})
        checked.append(block['id'])
    # Global layout affects targeted blocks too; a targeted pass still does not
    # claim that untargeted body content has been checked.
    try:
        expected_sections = [section_record(x, expected_package, expected_styles)
                             for x in bank.root.findall('.//w:sectPr', NS)]
        actual_sections = [section_record(x, actual_package, actual_styles)
                           for x in root.findall('.//w:sectPr', NS)]
        diff = first_difference(expected_sections, actual_sections)
        if diff:
            errors.append({'code': 'SECTION_OR_HEADER_FOOTER_MISMATCH', **diff})
    except ValueError as exc:
        errors.append({'code': 'UNVERIFIED_GLOBAL_FORMAT', 'reason': str(exc)})
    # Theme/font-table/numbering and document settings may affect glyphs or
    # geometry without changing any run. Compare their meaningful XML separately.
    for part in ('word/theme/theme1.xml', 'word/fontTable.xml', 'word/numbering.xml'):
        left, right = expected_package.get(part), actual_package.get(part)
        if left is None and right is None:
            continue
        if left is None or right is None or tree_record(E.fromstring(left)) != tree_record(E.fromstring(right)):
            errors.append({'code': 'RENDER_DEPENDENCY_MISMATCH', 'part': part})
    for part in ('word/settings.xml',):
        left, right = expected_package.get(part), actual_package.get(part)
        if left is None or right is None:
            if left != right:
                errors.append({'code': 'RENDER_DEPENDENCY_MISMATCH', 'part': part})
            continue
        skip = {'zoom', 'view', 'proofState', 'rsids', 'updateFields', 'attachedTemplate',
                'revisionView', 'doNotTrackMoves', 'doNotTrackFormatting'}
        def settings(data):
            return {E.QName(x).localname: tree_record(x) for x in E.fromstring(data)
                    if E.QName(x).localname not in skip}
        if settings(left) != settings(right):
            errors.append({'code': 'RENDER_DEPENDENCY_MISMATCH', 'part': part})
    contract_path = bank.assets / 'layout-contract.json'
    return {'format_validation': 'FAIL' if errors else 'PASS', 'format_scope': scope,
            'format_checked_blocks': checked, 'format_errors': errors,
            'plan_sha256': canonical_hash(plan),
            'contract_sha256': hashlib.sha256(contract_path.read_bytes()).hexdigest(),
            'reference_sha256': hashlib.sha256(bank.reference.read_bytes()).hexdigest(),
            'format_validation_scope': 'Stored OOXML properties and effective character formatting; not visual pagination or content semantics'}
