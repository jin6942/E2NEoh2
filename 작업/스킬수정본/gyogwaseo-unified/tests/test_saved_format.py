"""Negative tests for final saved formatting, separate from content validity."""
from copy import deepcopy
import hashlib
import importlib.util
import json
from pathlib import Path
import unittest
import uuid
from zipfile import ZipFile

from lxml import etree as E

ROOT = Path(__file__).resolve().parent
SCRIPTS = ROOT.parent / 'scripts'


def module(name, file):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / file)
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


checker = module('saved_format_test_check', 'check_saved_docx.py')
master = module('saved_format_test_master', 'master_docx.py')
NS, q = master.NS, master.tag


class SavedFormatTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.directory = ROOT / ('saved-format-test-' + uuid.uuid4().hex)
        cls.directory.mkdir()
        cls.plan = json.loads((ROOT / 'template-audit/layout-specimen.json').read_text(encoding='utf-8'))
        cls.source = cls.directory / 'baseline.docx'
        master.write(cls.plan, cls.source)

    def mutated(self, change, part='word/document.xml'):
        with ZipFile(self.source) as archive:
            parts = {x.filename: archive.read(x.filename) for x in archive.infolist()}
        root = E.fromstring(parts[part])
        change(root)
        parts[part] = E.tostring(root, xml_declaration=True, encoding='UTF-8', standalone=True)
        target = self.directory / (uuid.uuid4().hex + '.docx')
        with ZipFile(target, 'w') as archive:
            for name, data in parts.items():
                archive.writestr(name, data)
        return target

    def check(self, target, plan=None):
        return checker.check(plan or self.plan, target)

    def fails_format(self, target, code='SAVED_FORMAT_MISMATCH'):
        result = self.check(target)
        self.assertEqual(result['status'], 'FAIL')
        self.assertEqual(result['content_validation'], 'PASS')
        self.assertEqual(result['format_validation'], 'FAIL')
        self.assertIn(code, {x['code'] for x in result['errors']})
        self.assertEqual(result['layout_geometry_review'], 'NOT_PERFORMED')
        return result

    def first_run(self, root):
        return root.find('.//w:sdtContent//w:r[w:t]', NS)

    def test_normal_current_plan_passes_and_hashes_bind_inputs(self):
        result = self.check(self.source)
        self.assertEqual(result['status'], 'SAVED_CONTENT_MATCH')
        self.assertEqual(result['format_validation'], 'PASS')
        self.assertEqual(result['content_validation'], 'PASS')
        expected = json.dumps(self.plan, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')
        self.assertEqual(result['plan_sha256'], hashlib.sha256(expected).hexdigest())
        assets = SCRIPTS.parent / 'assets'
        self.assertEqual(result['contract_sha256'], hashlib.sha256((assets / 'layout-contract.json').read_bytes()).hexdigest())
        self.assertEqual(result['saved_sha256'], hashlib.sha256(self.source.read_bytes()).hexdigest())

    def test_font_size_mutation_fails(self):
        def change(root):
            master.set_property(self.first_run(root).find('w:rPr', NS), 'sz', {'val': 36})
        self.fails_format(self.mutated(change))

    def test_color_mutation_fails(self):
        def change(root):
            master.set_property(self.first_run(root).find('w:rPr', NS), 'color', {'val': 'FF0000'})
        self.fails_format(self.mutated(change))

    def test_font_family_mutation_fails(self):
        def change(root):
            master.set_property(self.first_run(root).find('w:rPr', NS), 'rFonts',
                                {'ascii': 'Comic Sans MS', 'eastAsia': '궁서'})
        self.fails_format(self.mutated(change))

    def test_paragraph_spacing_mutation_fails(self):
        def change(root):
            pp = root.find('.//w:sdtContent/w:p/w:pPr', NS)
            master.set_property(pp, 'spacing', {'before': 600, 'after': 600, 'line': 720, 'lineRule': 'auto'})
        self.fails_format(self.mutated(change))

    def test_margin_mutation_fails(self):
        self.fails_format(self.mutated(lambda root: root.find('.//w:sectPr/w:pgMar', NS).set(q('top'), '1440')),
                          'SECTION_OR_HEADER_FOOTER_MISMATCH')

    def test_footer_distance_mutation_fails(self):
        self.fails_format(self.mutated(lambda root: root.find('.//w:sectPr/w:pgMar', NS).set(q('footer'), '720')),
                          'SECTION_OR_HEADER_FOOTER_MISMATCH')

    def test_extra_section_fails(self):
        def change(root):
            pp = root.find('.//w:sdtContent/w:p/w:pPr', NS)
            pp.append(deepcopy(root.find('.//w:sectPr', NS)))
        self.fails_format(self.mutated(change))

    def test_table_width_mutation_fails(self):
        self.fails_format(self.mutated(lambda root: root.find('.//w:tbl/w:tblPr/w:tblW', NS).set(q('w'), '5000')))

    def test_table_cell_margin_mutation_fails(self):
        def change(root):
            pr = root.find('.//w:tbl/w:tr/w:tc/w:tcPr', NS)
            mar = master.set_property(pr, 'tcMar', {})
            master.set_property(mar, 'top', {'w': 480, 'type': 'dxa'})
        self.fails_format(self.mutated(change))

    def test_table_grid_width_mutation_fails(self):
        self.fails_format(self.mutated(lambda root: root.find('.//w:tbl/w:tblGrid/w:gridCol', NS).set(q('w'), '5000')))

    def test_cell_color_mutation_fails(self):
        def change(root):
            master.set_property(root.find('.//w:tbl/w:tr/w:tc/w:tcPr', NS), 'shd', {'fill': 'FF0000'})
        self.fails_format(self.mutated(change))

    def test_footer_font_and_text_checked(self):
        with ZipFile(self.source) as archive:
            part = next(name for name in archive.namelist() if name.startswith('word/footer') and name.endswith('.xml'))
        def change(root):
            r = root.find('.//w:r[w:t]', NS)
            pr = r.find('w:rPr', NS)
            if pr is None:
                pr = E.Element(q('rPr'))
                r.insert(0, pr)
            master.set_property(pr, 'sz', {'val': 40})
        self.fails_format(self.mutated(change, part), 'SECTION_OR_HEADER_FOOTER_MISMATCH')

    def test_wrong_existing_role_is_detected_against_approved_plan(self):
        altered = deepcopy(self.plan)
        element = next(e for b in altered['blocks'] for e in b['elements'] if e['role'] == 'sv')
        element['role'] = 'gloss'
        target = self.directory / (uuid.uuid4().hex + '.docx')
        master.write(altered, target)
        self.fails_format(target)

    def test_wrong_existing_run_is_detected_against_approved_plan(self):
        altered = deepcopy(self.plan)
        element = next(e for b in altered['blocks'] for e in b['elements'] if e['role'] == 'analysis_easy_explanation')
        element['runs'][1]['run'] = 0
        target = self.directory / (uuid.uuid4().hex + '.docx')
        master.write(altered, target)
        self.fails_format(target)

    def test_run_split_is_format_equivalent(self):
        def change(root):
            r = self.first_run(root)
            t = r.find('w:t', NS)
            other = deepcopy(r)
            half = len(t.text) // 2
            other.find('w:t', NS).text = t.text[half:]
            t.text = t.text[:half]
            r.addnext(other)
        self.assertEqual(self.check(self.mutated(change))['status'], 'SAVED_CONTENT_MATCH')

    def test_run_merge_is_format_equivalent(self):
        plan = {'blocks': [{'id': 'merged-example', 'elements': [
            {'role': 'analysis_prose', 'runs': [{'run': 0, 'text': '같은 서식 '},
                                               {'run': 0, 'text': '두 구간'}]}]}]}
        source = self.directory / (uuid.uuid4().hex + '.docx')
        master.write(plan, source)
        with ZipFile(source) as archive:
            parts = {x.filename: archive.read(x.filename) for x in archive.infolist()}
        root = E.fromstring(parts['word/document.xml'])
        p = root.find('.//w:sdtContent/w:p', NS)
        runs = p.findall('w:r', NS)
        runs[0].find('w:t', NS).text += runs[1].find('w:t', NS).text
        p.remove(runs[1])
        parts['word/document.xml'] = E.tostring(root, encoding='UTF-8', xml_declaration=True)
        target = self.directory / (uuid.uuid4().hex + '.docx')
        with ZipFile(target, 'w') as archive:
            for name, data in parts.items():
                archive.writestr(name, data)
        self.assertEqual(self.check(target, plan)['status'], 'SAVED_CONTENT_MATCH')

    def test_paragraph_mark_size_change_fails(self):
        def change(root):
            pp = root.find('.//w:sdtContent/w:p/w:pPr', NS)
            rp = master.set_property(pp, 'rPr', {})
            master.set_property(rp, 'sz', {'val': 50})
        self.fails_format(self.mutated(change))

    def test_section_column_count_mutation_fails(self):
        def change(root):
            master.set_property(root.find('.//w:sectPr', NS), 'cols', {'num': 2})
        self.fails_format(self.mutated(change), 'SECTION_OR_HEADER_FOOTER_MISMATCH')

    def test_default_style_font_mutation_fails(self):
        def change(root):
            rp = root.find('w:docDefaults/w:rPrDefault/w:rPr', NS)
            master.set_property(rp, 'rFonts', {'eastAsia': '궁서'})
        result = self.check(self.mutated(change, 'word/styles.xml'))
        self.assertEqual(result['format_validation'], 'FAIL')
        self.assertEqual(result['content_validation'], 'PASS')

    def style_case(self, color):
        with ZipFile(self.source) as archive:
            parts = {x.filename: archive.read(x.filename) for x in archive.infolist()}
        doc, styles = (E.fromstring(parts[name]) for name in ('word/document.xml', 'word/styles.xml'))
        block_index = next(i for i, b in enumerate(self.plan['blocks']) if b['id'] == 'unit1/analysis')
        index = next(i for i, e in enumerate(self.plan['blocks'][block_index]['elements']) if e['role'] == 'analysis_prose')
        p = doc.find('w:body', NS).findall('w:sdt', NS)[block_index].find('w:sdtContent', NS)[index]
        old = p.find('w:pPr/w:pStyle', NS)
        default = next(x.get(q('styleId')) for x in styles.findall('w:style', NS)
                       if x.get(q('type')) == 'paragraph' and x.get(q('default')) == '1')
        style = E.SubElement(styles, q('style'), {q('type'): 'paragraph', q('styleId'): 'AuditInherited'})
        E.SubElement(style, q('basedOn'), {q('val'): old.get(q('val')) if old is not None else default})
        rp = E.SubElement(style, q('rPr'))
        master.set_property(rp, 'color', {'val': color})
        master.set_property(p.find('w:pPr', NS), 'pStyle', {'val': 'AuditInherited'})
        for run in p.findall('w:r', NS):
            pr = run.find('w:rPr', NS)
            direct = pr.find('w:color', NS) if pr is not None else None
            if direct is not None:
                pr.remove(direct)
        parts['word/document.xml'] = E.tostring(doc, xml_declaration=True, encoding='UTF-8')
        parts['word/styles.xml'] = E.tostring(styles, xml_declaration=True, encoding='UTF-8')
        target = self.directory / (uuid.uuid4().hex + '.docx')
        with ZipFile(target, 'w') as archive:
            for name, value in parts.items():
                archive.writestr(name, value)
        return target

    def test_equivalent_inherited_style_is_accepted(self):
        self.assertEqual(self.check(self.style_case('000000'))['status'], 'SAVED_CONTENT_MATCH')

    def test_inherited_style_color_mutation_fails(self):
        self.fails_format(self.style_case('FF0000'))

    def test_targeted_scope_keeps_explicit_scope(self):
        plan = {'blocks': [self.plan['blocks'][2]]}
        result = checker.check(plan, self.source, 'targeted')
        self.assertEqual(result['format_validation'], 'PASS')
        self.assertEqual(result['format_scope'], 'targeted')
        self.assertEqual(result['scope'], 'targeted')

    def test_alternate_assets_directory_is_supported(self):
        result = checker.check(self.plan, self.source, assets=SCRIPTS.parent / 'assets')
        self.assertEqual(result['format_validation'], 'PASS')


if __name__ == '__main__':
    unittest.main()
