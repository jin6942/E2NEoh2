import importlib.util
from pathlib import Path
import uuid
import unittest
from zipfile import ZipFile

script = Path(__file__).parent / '../scripts/master_docx.py'
spec = importlib.util.spec_from_file_location('master_docx', script)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def block(key, text, role='analysis_prose'):
    return {'id': key, 'elements': [{'role': role, 'runs': [{'run': 0, 'text': text}]}]}


class MasterTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(__file__).parent / ('master-test-' + uuid.uuid4().hex)
        self.tmp.mkdir()
        self.target = self.tmp / 'test.docx'
        self.bank = m.RoleBank()

    def tearDown(self):
        # Retain isolated work evidence; this Windows sandbox blocks recursive
        # tempfile cleanup and can stall Python's fallback permission handler.
        pass

    def create(self):
        return m.write({'blocks': [block('a', '첫 영역'), block('b', '보존 영역')]}, self.target)

    def test_review_line_keeps_gold_format_with_new_analysis_reference(self):
        data = self.bank.contract['additional_paragraph_roles']['interpretation_review_line']
        p = self.bank.paragraph('interpretation_review_line', data['runs'], chain=False)
        text = ''.join(p.xpath('.//w:t/text()', namespaces=m.NS))
        self.assertIn('지문 분석지의 해석', text)
        self.assertNotIn('모범 해석', text)
        self.assertEqual(p.xpath('./w:r/w:rPr/w:sz/@w:val', namespaces=m.NS), ['15'] * 3)
        self.assertEqual(p.find('w:pPr/w:spacing', m.NS).get(m.tag('line')), '195')

    def root(self):
        with ZipFile(self.target) as z:
            return m.E.fromstring(z.read('word/document.xml'))

    def test_untargeted_block_and_all_other_parts_preserved(self):
        first = self.create()
        before = m.block_index(self.root().find('w:body', m.NS))
        kept = m.E.tostring(before['b'])
        r = m.write({'blocks': [block('a', '수정 영역')]}, self.target, 'patch', first['sha256'])
        after = m.block_index(self.root().find('w:body', m.NS))
        self.assertEqual(m.E.tostring(after['b']), kept)
        self.assertEqual(r['untargeted_block_count'], 1)
        with ZipFile(self.target) as z:
            for info, data in self.bank.package:
                if info.filename != 'word/document.xml':
                    self.assertEqual(z.read(info.filename), data)

    def test_insert_workbook_before_next_unit_preserves_existing(self):
        first = self.create()
        new = block('workbook', '추가 워크북')
        new['insert_before'] = 'b'
        m.write({'blocks': [new]}, self.target, 'patch', first['sha256'])
        self.assertEqual(list(m.block_index(self.root().find('w:body', m.NS))), ['a', 'workbook', 'b'])

    def test_stale_hash_refuses_save(self):
        self.create()
        before = self.target.read_bytes()
        with self.assertRaisesRegex(ValueError, 'version'):
            m.write({'blocks': [block('a', '잘못된 덮어쓰기')]}, self.target, 'patch', '0' * 64)
        self.assertEqual(self.target.read_bytes(), before)

    def test_create_refuses_existing(self):
        self.create()
        with self.assertRaisesRegex(ValueError, 'existing'):
            self.create()

    def test_unknown_patch_requires_verified_anchor(self):
        first = self.create()
        with self.assertRaisesRegex(ValueError, 'anchor'):
            m.write({'blocks': [block('missing', '새 내용')]}, self.target, 'patch', first['sha256'])

    def test_master_cannot_be_overwritten(self):
        with self.assertRaisesRegex(ValueError, 'MASTER'):
            m.write({'blocks': [block('a', '내용')]}, self.bank.reference)

    def test_explicit_sizes_and_circled_source_text(self):
        for role, size in [('sv', '15'), ('gloss', '17'), ('workbook_question_choice', '20')]:
            p = self.bank.paragraph(role, [{'run': 0, 'text': '“① A²”\n다음 줄\t끝'}])
            self.assertEqual(p.find('.//w:sz', m.NS).get(m.tag('val')), size)
            self.assertEqual(''.join(p.xpath('.//w:t/text()', namespaces=m.NS)), '“① A²”다음 줄끝')
            self.assertEqual(len(p.findall('.//w:br', m.NS)), 1)
            self.assertEqual(len(p.findall('.//w:tab', m.NS)), 1)

    def test_box_and_odd_word_table_preserve_structure(self):
        box = self.bank.paragraph('given_box', [{'run': 0, 'text': 'A given sentence.'}])
        borders = box.findall('w:pPr/w:pBdr/*', m.NS)
        self.assertEqual(len(borders), 4)
        self.assertTrue(all(b.get(m.tag('sz')) == '6' and b.get(m.tag('space')) == '5' for b in borders))
        table = self.bank.table('workbook_word_table', ['alpha', 'beta', 'gamma'])
        self.assertEqual(len(table.findall('w:tr', m.NS)), 2)
        self.assertEqual([len(r.findall('w:tc', m.NS)) for r in table.findall('w:tr', m.NS)], [4, 4])
        text = ''.join(table.xpath('.//w:t/text()', namespaces=m.NS))
        self.assertIn('3. gamma', text)
        self.assertNotIn('4.', text)

    def test_guide_line_breaks_and_approved_edits_survive(self):
        first_index = str(self.bank.contract['roles']['guide_item_one']['locator']['zero_based_index'])
        last_index = str(self.bank.contract['roles']['guide_item_three']['locator']['zero_based_index'])
        records = self.bank.contract['guide_runs'][first_index]
        p = self.bank.paragraph('guide_item_one', records)
        self.assertGreater(len(p.findall('.//w:br', m.NS)), 0)
        text = ''.join(r['text'] for r in self.bank.contract['guide_runs'][last_index])
        self.assertNotIn('[주절]입니다', text)
        self.assertIn('S·V로 바로', text)

    def test_invalid_role_cannot_write_arbitrary_style(self):
        with self.assertRaisesRegex(ValueError, 'Unknown paragraph'):
            self.bank.paragraph('custom_font', [{'run': 0, 'text': '가나다'}])


if __name__ == '__main__':
    unittest.main()
