import importlib.util
import json
from pathlib import Path
import unittest
import uuid
from zipfile import ZipFile
from lxml import etree as E

ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('saved_docx', ROOT / '../scripts/check_saved_docx.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
master_spec = importlib.util.spec_from_file_location('saved_test_master', ROOT / '../scripts/master_docx.py')
master = importlib.util.module_from_spec(master_spec)
master_spec.loader.exec_module(master)


class SavedDocxTests(unittest.TestCase):
    def setUp(self):
        self.plan = json.loads((ROOT / 'template-audit/layout-specimen.json').read_text(encoding='utf-8'))
        self.directory = ROOT / ('saved-docx-test-' + uuid.uuid4().hex)
        self.directory.mkdir()
        self.source = self.directory / 'current-contract-specimen.docx'
        master.write(self.plan, self.source)

    def altered(self, mutate):
        with ZipFile(self.source) as z:
            parts = [(entry, z.read(entry.filename)) for entry in z.infolist()]
        body = E.fromstring(dict((i.filename, b) for i, b in parts)['word/document.xml'])
        mutate(body)
        target = self.directory / 'changed.docx'
        with ZipFile(target, 'w') as z:
            for entry, data in parts:
                z.writestr(entry, E.tostring(body, xml_declaration=True, encoding='UTF-8', standalone=True)
                           if entry.filename == 'word/document.xml' else data)
        return target

    def codes(self, path, plan=None, scope='full'):
        return {e['code'] for e in m.check(plan or self.plan, path, scope)['errors']}

    def test_saved_specimen(self):
        self.assertEqual(self.codes(self.source), set())
        self.assertEqual(m.check(self.plan, self.source)['format_validation'], 'PASS')

    def test_saved_text_tampering(self):
        target = self.altered(lambda root: setattr(root.find('.//w:sdtContent/w:p/w:r/w:t', m.NS), 'text', 'Changed'))
        self.assertIn('SAVED_CONTENT_MISMATCH', self.codes(target))

    def test_missing_saved_paragraph(self):
        def mutate(root):
            content = root.find('.//w:sdtContent', m.NS)
            content.remove(content.find('w:p', m.NS))
        self.assertIn('ELEMENT_COUNT', self.codes(self.altered(mutate)))

    def test_saved_table_tampering(self):
        def mutate(root):
            root.find('.//w:sdtContent/w:tbl//w:t', m.NS).text = 'Wrong title'
        self.assertIn('SAVED_CONTENT_MISMATCH', self.codes(self.altered(mutate)))

    def test_unmanaged_text_not_silently_ignored(self):
        def mutate(root):
            body = root.find('w:body', m.NS)
            p = E.Element(m.q('p'))
            E.SubElement(E.SubElement(p, m.q('r')), m.q('t')).text = 'Old model translation'
            body.insert(0, p)
        self.assertIn('UNMANAGED_BODY_CONTENT', self.codes(self.altered(mutate)))

    def test_duplicate_saved_tag(self):
        def mutate(root):
            tags = root.findall('.//w:sdtPr/w:tag', m.NS)
            tags[1].set(m.q('val'), tags[0].get(m.q('val')))
        with self.assertRaisesRegex(ValueError, 'duplicate'):
            m.check(self.plan, self.altered(mutate))

    def test_block_order(self):
        def mutate(root):
            body = root.find('w:body', m.NS)
            first = body[0]
            body.remove(first)
            body.insert(1, first)
        self.assertIn('BLOCK_ORDER_OR_COVERAGE', self.codes(self.altered(mutate)))

    def test_targeted_mode_does_not_claim_whole_doc(self):
        plan = {'blocks': [self.plan['blocks'][3]]}
        result = m.check(plan, self.source, 'targeted')
        self.assertEqual(result['errors'], [])
        self.assertEqual(result['scope'], 'targeted')
        self.assertIn('BLOCK_ORDER_OR_COVERAGE', self.codes(self.source, plan))

    def test_manual_linebreak_loss(self):
        def mutate(root):
            br = root.find('.//w:sdtContent//w:br', m.NS)
            br.getparent().remove(br)
        self.assertIn('SAVED_CONTENT_MISMATCH', self.codes(self.altered(mutate)))

    def test_tracked_deletion_requires_review(self):
        def mutate(root):
            p = root.find('.//w:sdtContent/w:p', m.NS)
            E.SubElement(p, m.q('del'))
        with self.assertRaisesRegex(ValueError, 'Tracked changes'):
            m.check(self.plan, self.altered(mutate))


if __name__ == '__main__':
    unittest.main()
