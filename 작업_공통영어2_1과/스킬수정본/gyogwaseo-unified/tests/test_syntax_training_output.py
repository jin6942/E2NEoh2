"""Check the actual student/answer split and stored DOCX for syntax practice."""
from copy import deepcopy
from pathlib import Path
import sys
import unittest
import uuid
from zipfile import ZipFile

from lxml import etree as E

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / '../scripts'))
from book_plan import compile_plan, grammar_number
from export_handoff import render
from master_docx import NS, RoleBank, write
from check_saved_docx import check as check_saved
from test_book_plan import fixture as book_fixture


def fixture():
    data = book_fixture()
    data['metadata']['syntax_training_version'] = 1
    unit = data['units'][0]
    unit['analysis']['formula_routes'] = []
    for i, point in enumerate(unit['analysis']['grammar_points'], 1):
        sentence = data['sentences'][i-1]
        gloss = sentence['glosses'][1]
        point.update(id=f'gp{i}', formula_key=f'formula {i}',
                     span=[0, len(sentence['text'])],
                     practice={'span': gloss['spans'][0],
                               'formula_support': {'en': f'Formula {i}', 'ko': f'공식 뜻 {i}'},
                               'support_gloss_ids': [gloss['id']],
                               'answer_ko': f'정답에만 실리는 결합 해석 {i}'})
    unit['workbook']['syntax_point_ids'] = ['gp1', 'gp2', 'gp3']
    return data


def visible(block):
    return '\n'.join(''.join(run['text'] for run in row.get('runs', []))
                     for row in block['elements'])


def expected_practices(data):
    sentences = {row['id']: row for row in data['sentences']}
    for n, point in enumerate(data['units'][0]['analysis']['grammar_points'], 1):
        practice = point['practice']
        sentence = sentences[point['sentence_id']]
        expression = sentence['text'][slice(*practice['span'])]
        glosses = {row['id']: row for row in sentence['glosses']}
        support = f'Formula {n} — 공식 뜻 {n}' + ''.join(
            ' / ' + glosses[gid]['headword'] + ' — ' + glosses[gid]['meaning_ko']
            for gid in practice['support_gloss_ids'])
        yield n, point['id'], expression + ' → ______________________________', support


class SyntaxTrainingOutputTests(unittest.TestCase):
    def test_student_supports_and_separate_answers_preserve_other_activities(self):
        data = fixture()
        before = deepcopy(data)
        plan = compile_plan(data)
        blocks = {b['id']: b for b in plan['blocks']}
        student = visible(blocks['u1/workbook'])
        answers = visible(blocks['u1/answers'])
        for n in (1, 2, 3):
            self.assertIn(f'Formula {n} — 공식 뜻 {n}', student)
            self.assertNotIn(f'정답에만 실리는 결합 해석 {n}', student)
            self.assertEqual(answers.count(f'정답에만 실리는 결합 해석 {n}'), 1)
        self.assertLess(student.index('3. 실전문제'), student.index('4. 구문 결합해서 해석하기'))
        self.assertLess(student.index('4. 구문 결합해서 해석하기'), student.index('5. 핵심 문장'))
        self.assertIn('5. 핵심 문장 해석', answers)
        rows = blocks['u1/workbook']['elements']
        continuation = next(row for row in rows if row['role'] == 'workbook_continuation')
        self.assertTrue(continuation['page_break_before'])
        for n, point_id, question, support in expected_practices(data):
            index = next(i for i, row in enumerate(rows)
                         if row.get('anchor') == 'syntax/' + point_id)
            question_row, help_row = rows[index:index+2]
            self.assertEqual(question_row['role'], 'workbook_key_sentence')
            self.assertEqual(visible({'elements': [question_row]}), f'{n}.   {question}')
            self.assertEqual(help_row['role'], 'choice_translation')
            self.assertEqual(visible({'elements': [help_row]}), '도움말  ' + support)
            self.assertTrue(question_row['chain'])
            self.assertFalse(help_row['chain'])
        self.assertEqual(rows[index+2], {'role': 'workbook_question_gap', 'chain': False})
        self.assertEqual(rows[index+3]['anchor'], 'key/heading')
        self.assertEqual(data, before)

    def test_final_text_exercises_and_answers_match_docx_inputs(self):
        data = fixture()
        output = render(data)['assessment']
        student, remainder = output.split('[워크북 정답]', 1)
        for n in (1, 2, 3):
            self.assertIn(f'Formula {n} — 공식 뜻 {n}', student)
            self.assertNotIn(f'정답에만 실리는 결합 해석 {n}', student)
            self.assertEqual(remainder.count(f'정답에만 실리는 결합 해석 {n}'), 1)
        lines = student.splitlines()
        first_question = next(expected_practices(data))[2]
        syntax_heading = lines.index('[4. 구문 결합해서 해석하기]')
        self.assertEqual(lines[syntax_heading+1], '1. ' + first_question)
        for n, _, question, support in expected_practices(data):
            index = lines.index(f'{n}. {question}')
            self.assertEqual(lines[index+1], '도움말: ' + support)
        self.assertIn('[5. 핵심 문장 2개 다시 해석하기]', student)
        key_heading = lines.index('[5. 핵심 문장 2개 다시 해석하기]')
        self.assertEqual(lines[key_heading-1], '')
        self.assertTrue(lines[key_heading-2].startswith('도움말: '))
        first_key_id = data['units'][0]['workbook']['key_sentence_ids'][0]
        first_key = next(s for s in data['sentences'] if s['id'] == first_key_id)
        self.assertEqual(lines[key_heading+1], '1. ' + first_key['text'])
        self.assertNotIn('도움말을 결합하여 우리말로 해석하세요.', student)
        self.assertNotIn('우리말로 다시 해석하세요.', student)
        self.assertIn('[5. 핵심 문장 해석]', remainder)

    def test_whole_key_activity_stays_together_without_another_forced_page(self):
        plan = compile_plan(fixture())
        block = next(b for b in plan['blocks'] if b['id'] == 'u1/workbook')
        at = next(i for i, row in enumerate(block['elements'])
                  if row.get('anchor') == 'key/heading')
        activity = {'id': 'key-activity-test', 'elements': block['elements'][at:]}
        paragraphs = RoleBank().block(activity).findall('w:sdtContent/w:p', NS)
        self.assertEqual(len(paragraphs), 7)  # Heading and two complete activities.
        for paragraph in paragraphs[:-1]:
            keep = paragraph.find('w:pPr/w:keepNext', NS)
            self.assertIsNotNone(keep)
            self.assertNotIn(keep.get('{'+NS['w']+'}val'), {'0', 'false', 'off'})
        last_keep = paragraphs[-1].find('w:pPr/w:keepNext', NS)
        self.assertIsNotNone(last_keep)
        self.assertEqual(last_keep.get('{'+NS['w']+'}val'), '0')
        for paragraph in paragraphs:
            page_break = paragraph.find('w:pPr/w:pageBreakBefore', NS)
            if page_break is not None:
                self.assertIn(page_break.get('{'+NS['w']+'}val'), {'0', 'false', 'off'})

    def test_saved_docx_checks_new_elements_and_detects_lost_practice(self):
        data = fixture()
        plan = compile_plan(data)
        folder = HERE / ('syntax-output-' + uuid.uuid4().hex)
        folder.mkdir()
        target = folder / 'book.docx'
        try:
            write(plan, target)
            self.assertEqual(check_saved(plan, target)['status'], 'SAVED_CONTENT_MATCH')
            with ZipFile(target) as saved:
                document = E.fromstring(saved.read('word/document.xml'))
            paragraphs = document.findall('.//w:p', NS)
            texts = [''.join(p.xpath('.//w:t/text()', namespaces=NS)) for p in paragraphs]
            syntax_heading = texts.index('4. 구문 결합해서 해석하기')
            first_question = next(expected_practices(data))[2]
            self.assertEqual(texts[syntax_heading+1], '1.   ' + first_question)
            for n, _, question, support in expected_practices(data):
                index = texts.index(f'{n}.   {question}')
                self.assertEqual(texts[index+1], '도움말  ' + support)
                for offset, expected_keep in ((0, '1'), (1, '0')):
                    keep = paragraphs[index+offset].find('w:pPr/w:keepNext', NS)
                    self.assertIsNotNone(keep)
                    self.assertEqual(keep.get('{'+NS['w']+'}val'), expected_keep)
            self.assertEqual(texts[index+2], '')
            self.assertEqual(texts[index+3], '5. 핵심 문장 2개 다시 해석하기')
            first_key_id = data['units'][0]['workbook']['key_sentence_ids'][0]
            first_key = next(s for s in data['sentences'] if s['id'] == first_key_id)
            self.assertEqual(texts[index+4], '1.   ' + first_key['text'])
            self.assertNotIn('도움말을 결합하여 우리말로 해석하세요.', texts)
            self.assertNotIn('우리말로 다시 해석하세요.', texts)
            changed = deepcopy(plan)
            block = next(b for b in changed['blocks'] if b['id'] == 'u1/workbook')
            row = next(e for e in block['elements'] if e.get('anchor') == 'syntax/gp2')
            row['runs'][1]['text'] = 'WRONG PRACTICE EXPRESSION'
            self.assertNotEqual(check_saved(changed, target)['status'], 'SAVED_CONTENT_MATCH')
        finally:
            for path in folder.iterdir():
                if path.is_file():
                    path.unlink()
            folder.rmdir()

    def test_analysis_numbering_does_not_stop_at_five(self):
        self.assertEqual(grammar_number(5), '⑥')
        self.assertEqual(grammar_number(19), '⑳')
        self.assertEqual(grammar_number(20), '21.')


if __name__ == '__main__':
    unittest.main()
