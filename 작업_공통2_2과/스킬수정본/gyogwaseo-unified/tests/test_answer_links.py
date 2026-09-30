import copy
import importlib.util
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
script = Path(__file__).parent / '../scripts/check_answer_links.py'
spec = importlib.util.spec_from_file_location('check_answer_links', script)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def fixture():
    key = {'id': 'Q01', 'set_id': 'mock1', 'number': 1}
    choices = [{'number': n, 'text': f'Choice {n}'} for n in range(1, 6)]
    q = dict(key, type='주제', question='What is the topic?', passage='A source excerpt.',
             choice_mode='text', choices=choices, answer=3)
    exp = dict(key, choices=copy.deepcopy(choices), answer=3,
               choices_ko=[{'number': n, 'text': f'선지 {n} 해석'} for n in range(1, 6)],
               wrong_reasons=[{'number': n, 'text': '원문과 맞지 않는 개별 근거'} for n in [1, 2, 4, 5]],
               evidence='해당 원문 문장', explanation='정답이 되는 이유')
    return {'scope': {'kind': 'partial', 'instruction': '미니 모의고사 한 문항의 대응 시험'},
            'plan': [key], 'questions': [q], 'quick_key': [dict(key, answer=3)],
            'explanations': [exp]}


class AnswerLinksTests(unittest.TestCase):
    def codes(self, data):
        return {e['code'] for e in m.check(data)['errors']}

    def test_complete_correspondence_has_limited_claim(self):
        r = m.check(fixture())
        self.assertEqual(r['status'], 'PASS')
        self.assertEqual(r['docx_presence'], 'NOT_CHECKED_BY_THIS_TOOL')
        self.assertEqual(r['semantic_review'], 'NOT_PERFORMED')

    def test_empty_plan_and_questions_never_pass(self):
        self.assertTrue({'EMPTY_PLAN', 'EMPTY_QUESTIONS'} <= self.codes({}))

    def test_quick_answer_error_is_actually_detected(self):
        d = fixture()
        d['quick_key'][0]['answer'] = 2
        self.assertIn('QUICK_ANSWER_MISMATCH', self.codes(d))

    def test_missing_student_question_not_silently_skipped(self):
        d = fixture()
        d['questions'] = []
        self.assertIn('ID_COVERAGE', self.codes(d))

    def test_short_korean_choice_list_not_zip_truncated(self):
        d = fixture()
        d['explanations'][0]['choices_ko'].pop()
        self.assertIn('CHOICE_COVERAGE', self.codes(d))

    def test_duplicate_choice_number_is_not_equal_count_pass(self):
        d = fixture()
        d['explanations'][0]['choices_ko'][4]['number'] = 4
        self.assertIn('CHOICE_DUPLICATE', self.codes(d))

    def test_symbol_insertion_still_requires_given(self):
        d = fixture()
        q = d['questions'][0]
        q.update(type='삽입', choice_mode='in_passage')
        q['choices'] = [{'number': n, 'text': chr(0x2460 + n - 1)} for n in range(1, 6)]
        d['explanations'][0].update(choices=copy.deepcopy(q['choices']), choices_ko=[])
        self.assertIn('GIVEN_REQUIRED', self.codes(d))
        q['given'] = 'The sentence to insert.'
        self.assertEqual(m.check(d)['status'], 'PASS')

    def test_same_display_number_in_different_round_is_valid(self):
        d = fixture()
        for field in ('plan', 'questions', 'quick_key', 'explanations'):
            row = copy.deepcopy(d[field][0])
            row.update(id='Q02', set_id='mock2')
            if field == 'questions':
                row['question'] = 'Which topic best describes the passage?'
            d[field].append(row)
        self.assertEqual(m.check(d)['status'], 'PASS')
        d['quick_key'][1]['set_id'] = 'mock1'
        self.assertIn('DISPLAY_MISMATCH', self.codes(d))

    def test_prohibited_grammar_question_and_duplicate_id(self):
        d = fixture()
        d['questions'][0]['type'] = '어법'
        d['questions'].append(copy.deepcopy(d['questions'][0]))
        self.assertTrue({'QUESTION_TYPE', 'DUPLICATE_ID'} <= self.codes(d))

    def test_wrong_reason_missing_and_student_choice_changed(self):
        d = fixture()
        d['explanations'][0]['wrong_reasons'].pop()
        d['questions'][0]['choices'][0]['text'] = 'Changed choice'
        self.assertTrue({'CHOICE_COVERAGE', 'EXPLANATION_CHOICES_MISMATCH'} <= self.codes(d))

    def test_full_scope_does_not_accept_partial_count(self):
        d = fixture()
        d['scope'] = {'kind': 'full', 'course': '공통영어2', 'unit_ids': ['U1']}
        self.assertTrue({'SET_COUNTS', 'WORKBOOK_UNIT_COVERAGE'} <= self.codes(d))

    def test_other_verified_course_keeps_default_and_empty_name_rejected(self):
        d = fixture()
        d['scope'] = {'kind': 'full', 'course': '영어I', 'unit_ids': ['U1']}
        self.assertNotIn('COURSE_REQUIRED', self.codes(d))
        d['scope']['course'] = ''
        self.assertIn('COURSE_REQUIRED', self.codes(d))

    def test_ordering_missing_block_and_repeated_permutation(self):
        d = fixture()
        q = d['questions'][0]
        q.update(type='순서', choice_mode='order', given='Given passage.',
                 blocks={'A': 'First.', 'B': 'Second.'}, permutations=[['A', 'B', 'C']] * 5)
        d['explanations'][0]['choices_ko'] = []
        self.assertTrue({'BLOCKS_REQUIRED', 'ORDER_CHOICES'} <= self.codes(d))


if __name__ == '__main__':
    unittest.main()
