from copy import deepcopy
from pathlib import Path
import sys
import unittest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / '../scripts'))
import check_book as m
from test_learning_content import fixture as learning_fixture


def fixture():
    texts = ['They repair ' + ' '.join(['useful'] * 36) + ' tools.',
             'We save ' + ' '.join(['valuable'] * 36) + ' materials.',
             'I protect ' + ' '.join(['local'] * 36) + ' resources.']
    data = learning_fixture(texts)
    assessment = {'scope': {'kind': 'full', 'course': '공통영어1', 'unit_ids': ['u1']},
                  'plan': [], 'questions': [], 'quick_key': [], 'explanations': []}
    source_requests = []
    sets = [('workbook', 1)] + [(f'mock{x}', 5) for x in range(1, 4)]
    for set_id, count in sets:
        for number in range(1, count + 1):
            qid = 'q1' if set_id == 'workbook' else f'{set_id}-{number}'
            identity = {'id': qid, 'set_id': set_id, 'number': number}
            answer = (len(assessment['questions']) % 5) + 1
            planned = dict(identity)
            if set_id == 'workbook':
                planned['unit_id'] = 'u1'
            assessment['plan'].append(planned)
            choices = [{'number': x, 'text': f'Option {x} for {qid}'} for x in range(1, 6)]
            assessment['questions'].append(dict(identity, type='주제', choice_mode='text',
                question=f'{qid} 시험용 발문', passage=data['sources'][0]['text'], choices=choices, answer=answer))
            assessment['quick_key'].append(dict(identity, answer=answer))
            assessment['explanations'].append(dict(identity, choices=deepcopy(choices), answer=answer,
                evidence='시험용 근거', explanation='시험용 설명',
                choices_ko=[{'number': x, 'text': f'{x} 시험용 해석'} for x in range(1, 6)],
                wrong_reasons=[{'number': x, 'text': f'{x} 시험용 배제 근거'} for x in range(1,6) if x != answer]))
            source_requests.append(dict(id=qid, type='주제', source_id='src', first_sentence='s1', last_sentence='s3'))
    data.update(assessment=assessment, question_sources=source_requests)
    from revision_fixtures import upgrade_assessment_fixture
    return upgrade_assessment_fixture(data)


class BookTests(unittest.TestCase):
    def test_full_structural_bridge(self):
        result = m.check(fixture())
        self.assertEqual(result['status'], 'STRUCTURE_PASS')
        self.assertEqual(result['checked_question_count'], 16)
        self.assertEqual(result['independent_reviews'], 'NOT_PERFORMED')

    def test_changed_printed_passage_rejected(self):
        d = fixture()
        d['assessment']['questions'][0]['passage'] += ' Invented sentence.'
        with self.assertRaisesRegex(ValueError, 'source reconstruction'):
            m.check(d)

    def test_full_book_cannot_bypass_pending_source_boundary_review(self):
        d=fixture();source=d['sources'][0];parts=[s['text'] for s in d['sentences']]
        source['text']=''.join(parts);offset=0
        for bound,part in zip(source['sentences'],parts):
            bound['start']=offset;bound['end']=offset+len(part);offset+=len(part)
        for q in d['assessment']['questions']:q['passage']=source['text']
        result=m.check(d)
        self.assertEqual(result['status'],'NEEDS_SOURCE_REVIEW')
        self.assertTrue(any(x['code']=='JOINED_SENTENCE_BOUNDARY' for x in result['learning']['source_issues']))

    def test_missing_question_source_rejected(self):
        d = fixture()
        d['question_sources'].pop()
        with self.assertRaisesRegex(ValueError, 'Every question'):
            m.check(d)

    def test_wrong_workbook_unit_rejected(self):
        d = fixture()
        d['assessment']['plan'][0]['unit_id'] = 'u2'
        self.assertEqual(m.check(d)['status'], 'FAIL')

    def test_course_mismatch_rejected(self):
        d = fixture()
        d['metadata']['course'] = '다른 확인 과목'
        with self.assertRaisesRegex(ValueError, 'course differs'):
            m.check(d)

    def test_partial_is_not_full_book(self):
        d = fixture()
        d['assessment']['scope'] = {'kind': 'partial', 'instruction': '일부 작업'}
        with self.assertRaisesRegex(ValueError, 'Partial'):
            m.check(d)

    def test_shortness_requires_independent_review_and_is_not_marked_sufficient(self):
        d = fixture()
        d['question_sources'][0]['length_review'].pop('independent_review_required')
        with self.assertRaisesRegex(ValueError, 'independent length review'):
            m.check(d)

    def test_quick_key_error_still_detected_through_bridge(self):
        d = fixture()
        d['assessment']['quick_key'][-1]['answer'] = 5
        result = m.check(d)
        self.assertEqual(result['status'], 'FAIL')
        self.assertTrue(any(e['code'] == 'QUICK_ANSWER_MISMATCH' for e in result['assessment']['errors']))

    def test_full_book_answer_concentration_is_checked(self):
        d = fixture()
        for section in ['questions', 'quick_key', 'explanations']:
            for row in d['assessment'][section]:
                row['answer'] = 3
                if section == 'explanations':
                    row['wrong_reasons'] = [{'number': x, 'text': '시험용 배제 근거'} for x in [1,2,4,5]]
        result=m.check(d)
        self.assertEqual(result['status'],'FAIL')
        self.assertTrue(any(e['code']=='ANSWER_DISTRIBUTION' for e in result['assessment']['errors']))


if __name__ == '__main__':
    unittest.main()
