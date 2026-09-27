"""Approved lexical-to-verb training lines preserve authored bilingual emphasis."""
from copy import deepcopy
from pathlib import Path
import sys
import unittest
import uuid
from zipfile import ZipFile

from lxml import etree as E

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / '../scripts'))
from book_plan import structure_hint_element
from master_docx import NS, RoleBank, write
from structure_hints import display_lines, display_pairs
from test_learning_content import aligned_pair


EXAMPLES = [
    ('produced', '생산된', 'is produced', '생산된다', 'be p.p.', ['is', 'ed'], ['된다']),
    ('produced', '생산된', 'is being produced', '생산되고 있다', 'be being p.p.',
     ['is', 'being', 'ed'], ['되고 있다']),
    ('find', '발견하다', 'have found', '발견했다', 'have p.p.', ['have', 'found'], ['했다']),
    ('recycled', '재활용된', 'has been recycled', '재활용되었다', 'have been p.p.',
     ['has', 'been', 'ed'], ['되었다']),
    ('provide', '제공하다', 'may have provided', '제공했을지도 모른다', 'may have p.p.',
     ['may', 'have', 'ed'], ['했을지도 모른다']),
]


def training_hint(example=EXAMPLES[0]):
    form, meaning, english, korean, formula, en_marks, ko_marks = example
    return {'category': 'function-combination', 'display_mode': 'verb-function',
            'display_span': [0, len(english)], 'formula_label': formula,
            'lexical_step': {'gloss_id': 's1-g2', 'form': form, 'meaning_ko': meaning},
            'display_pairs': [aligned_pair(english, korean, (en_marks, ko_marks))]}


def expected_line(example):
    form, meaning, english, korean, formula, *_ = example
    return f'{form}({meaning}) → {english}({korean}) ({formula})'


class FormulaTrainingDisplayTests(unittest.TestCase):
    def test_all_five_approved_lines_are_identical_in_text_and_docx_plan(self):
        for example in EXAMPLES:
            hint = training_hint(example)
            before = deepcopy(hint)
            with self.subTest(english=example[2]):
                display_pairs(hint, require_alignment=True)
                expected = expected_line(example)
                self.assertEqual(display_lines(hint), [expected])
                row = structure_hint_element(hint)
                self.assertEqual(''.join(run['text'] for run in row['runs']), '구조 힌트   ' + expected)
                self.assertNotIn('\n', expected)
                self.assertEqual(hint, before)

    def test_only_reviewed_actual_verb_and_korean_ending_receive_emphasis(self):
        bank = RoleBank()
        for example in EXAMPLES:
            row = structure_hint_element(training_hint(example))
            paragraph = bank.paragraph(row['role'], row['runs'])
            with self.subTest(english=example[2]):
                en_marks, ko_marks = example[5:]
                self.assertEqual([run['text'] for run in row['runs'] if run.get('underline')], en_marks)
                self.assertEqual([run['text'] for run in row['runs']
                                  if run.get('format_role') == 'structure_hint_ko' and run['run'] == 1], ko_marks)
                marked = paragraph.xpath('.//w:r[w:rPr/w:u[not(@w:val="none")]]/w:t/text()', namespaces=NS)
                self.assertEqual(marked, en_marks + ko_marks)
                for run in paragraph.findall('w:r', NS):
                    text = ''.join(run.xpath('.//w:t/text()', namespaces=NS))
                    if any(char in text for char in '()→'):
                        self.assertEqual(run.xpath('./w:rPr/w:b[not(@w:val="0")]', namespaces=NS), [])
                        self.assertEqual(run.xpath('./w:rPr/w:u[not(@w:val="none")]', namespaces=NS), [])
                self.assertEqual(paragraph.findall('.//w:br', NS), [])

    def test_lexical_korean_intro_keeps_plain_existing_black_korean_role(self):
        row = structure_hint_element(training_hint())
        self.assertEqual(row['runs'][1], {'run': 1, 'text': 'produced('})
        self.assertEqual(row['runs'][2], {'run': 0, 'text': '생산된', 'format_role': 'structure_hint_ko'})
        bank = RoleBank()
        paragraph = bank.paragraph(row['role'], row['runs'])
        intro = paragraph.xpath('./w:r[w:t="생산된"]', namespaces=NS)[0]
        normal_ko = bank.paragraph('structure_hint_ko', [{'run': 0, 'text': '생산된'}]).find('w:r', NS)
        self.assertEqual(E.tostring(intro.find('w:rPr', NS)), E.tostring(normal_ko.find('w:rPr', NS)))

    def test_five_lines_survive_actual_docx_save_without_manual_breaks(self):
        rows = [structure_hint_element(training_hint(example)) for example in EXAMPLES]
        plan = {'blocks': [{'id': 'synthetic/formula-training', 'elements': rows}]}
        folder = HERE / ('formula-training-' + uuid.uuid4().hex)
        folder.mkdir()
        dest = folder / 'examples.docx'
        try:
            write(plan, dest)
            with ZipFile(dest) as package:
                document = E.fromstring(package.read('word/document.xml'))
            paragraphs = document.xpath('//w:p[contains(string(.), "구조 힌트")]', namespaces=NS)
            self.assertEqual([''.join(p.xpath('.//w:t/text()', namespaces=NS)) for p in paragraphs],
                             ['구조 힌트   ' + expected_line(example) for example in EXAMPLES])
            self.assertFalse(any(p.findall('.//w:br', NS) for p in paragraphs))
        finally:
            if dest.exists():
                dest.unlink()
            if not any(folder.iterdir()):
                folder.rmdir()

    def test_lexical_step_cannot_be_attached_to_other_hint_modes(self):
        for changes in [{'display_mode': 'modal-perfect-verb'}, {'display_mode': 'omitted-relative'},
                        {'category': 'paired-structure'}, {'category': 'general'}, {'display_mode': None}]:
            hint = {**training_hint(), **changes}
            with self.subTest(changes=changes), self.assertRaisesRegex(ValueError, 'lexical_step'):
                display_pairs(hint)

    def test_malformed_or_expanded_lexical_steps_are_rejected(self):
        valid = training_hint()['lexical_step']
        candidates = [None, [], {}, {'form': 'find', 'meaning_ko': '발견하다'},
                      {**valid, 'explanation': 'extra'}, {**valid, 'gloss_id': ''},
                      {**valid, 'gloss_id': 's1 g2'}, {**valid, 'gloss_id': 's1\ng2'}]
        for form in ['be p.p.', 'is produced', 'provide A with B', 'find\n', '[find]',
                     'find(발견하다)', 'A', 'x' * 81]:
            candidates.append({**valid, 'form': form})
        for meaning in ['생산된\n', '생산된 (수동태)', '[생산된]', '생산된 → 생산된다',
                        '생산된.', 'A에게 제공하다', '생산된 ' * 30]:
            candidates.append({**valid, 'meaning_ko': meaning})
        for step in candidates:
            hint = training_hint()
            hint['lexical_step'] = step
            with self.subTest(step=step), self.assertRaisesRegex(ValueError, 'lexical_step'):
                display_pairs(hint)

    def test_new_step_never_replaces_source_pair_or_grammatical_links(self):
        hint = training_hint(EXAMPLES[2])
        self.assertEqual(display_pairs(hint)[0]['en'], 'have found')
        self.assertNotEqual(display_pairs(hint)[0]['en'], hint['lexical_step']['form'])
        hint['display_pairs'][0].pop('emphasis_links')
        with self.assertRaisesRegex(ValueError, 'emphasis_links'):
            display_pairs(hint)

    def test_legacy_helper_display_is_not_silently_rewritten(self):
        hint = training_hint()
        hint.pop('lexical_step')
        self.assertEqual(display_lines(hint), ['is produced → 생산된다 (be p.p.)'])
        self.assertEqual(''.join(r['text'] for r in structure_hint_element(hint)['runs']),
                         '구조 힌트   is produced → 생산된다 (be p.p.)')


if __name__ == '__main__':
    unittest.main()
