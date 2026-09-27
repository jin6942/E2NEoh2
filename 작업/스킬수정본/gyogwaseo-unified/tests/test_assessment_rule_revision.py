"""Regression checks for source length, source freedom, and shared mock sets."""
from copy import deepcopy
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'scripts'))
import check_answer_links as links
import check_book
import question_source as source_module
from source_contract import course_policy, normalize_course


def length_review(kind, grade=1):
    return {'profile_id': source_module.LENGTH_PROFILE_ID, 'grade': grade,
            'benchmark_ids': source_module.recommended_benchmarks(grade, kind),
            'rationale': 'Synthetic regression fixture; this is not an educational sufficiency review.',
            'independent_review_required': True}


def source_fixture(words=150):
    texts = [' '.join(f'word{n}_{i}' for i in range(words // 5)) + '.' for n in range(5)]
    offset = 0
    bounds = []
    for n, text in enumerate(texts):
        bounds.append({'id': f's{n}', 'start': offset, 'end': offset + len(text)})
        offset += len(text) + 2
    source = {'id': 'src', 'text': '\n\n'.join(texts), 'sentences': bounds}
    q = {'type': '제목', 'source_id': 'src', 'first_sentence': 's0', 'last_sentence': 's4',
         'length_review': length_review('제목')}
    return source, q


def assessment_fixture(shared=True):
    rows = []
    for number, kind in [(4, '제목'), (5, '어휘')]:
        row = {'id': f'q{number}', 'set_id': 'mock1', 'number': number,
               'type': kind, 'question': f'{number} synthetic prompt', 'passage': 'Synthetic shared body.',
               'answer': 2, 'choice_mode': 'text' if kind == '제목' else 'in_passage',
               'choices': [{'number': n, 'text': f'choice {n}' if kind == '제목' else chr(0x2460+n-1)}
                           for n in range(1, 6)]}
        if shared:
            row['passage_group_id'] = 'g1'
        rows.append(row)
    result = {'scope': {'kind': 'partial', 'instruction': 'A synthetic last-two-question regression set.'},
              'questions': rows, 'plan': [], 'quick_key': [], 'explanations': []}
    for row in rows:
        identity = {k: row[k] for k in ['id', 'set_id', 'number']}
        result['plan'].append(identity)
        result['quick_key'].append(dict(identity, answer=2))
        result['explanations'].append(dict(identity, answer=2, choices=deepcopy(row['choices']),
            choices_ko=[{'number': n, 'text': f'{n} 시험용 뜻'} for n in range(1, 6)] if row['choice_mode'] == 'text' else [],
            evidence='Synthetic source evidence.', explanation='Synthetic explanation.',
            wrong_reasons=[{'number': n, 'text': 'Synthetic elimination reason.'} for n in [1, 3, 4, 5]]))
    if shared:
        result['passage_groups'] = [{'id': 'g1', 'kind': 'long_reading', 'set_id': 'mock1',
                                     'question_ids': ['q4', 'q5'], 'passage_question_id': 'q5'}]
    return result


class AssessmentRuleRevisionTests(unittest.TestCase):
    def codes(self, data):
        return {x['code'] for x in links.check(data)['errors']}

    def test_official_profile_has_same_grade_type_three_exam_references(self):
        for grade in (1, 2):
            for kind in links.TYPES | {'long41_42'}:
                refs = source_module.recommended_benchmarks(grade, kind)
                self.assertEqual(len(refs), 3)
                self.assertEqual(len(set(refs)), 3)
        self.assertEqual(source_module.length_profile()['status'],
                         'EMPIRICAL_COMPARISON_PROFILE_NOT_OFFICIAL_MINIMUM')

    def test_under_100_is_compared_and_never_auto_approved(self):
        source, q = source_fixture(95)
        view = source_module.build_view(source, q)
        self.assertEqual(view['word_count'], 95)
        self.assertEqual(view['length_comparison']['status'], 'NEEDS_INDEPENDENT_REVIEW')
        self.assertEqual(view['length_comparison']['educational_sufficiency'], 'NOT_CHECKED_BY_THIS_TOOL')
        self.assertEqual(view['passage'], source['text'])
        self.assertFalse(view['preserve_paragraphs'])

    def test_short_source_cannot_silently_drop_independent_review_flag(self):
        source, q = source_fixture(95)
        del q['length_review']['independent_review_required']
        with self.assertRaisesRegex(ValueError, 'queued for independent'):
            source_module.build_view(source, q)

    def test_no_fixed_upper_limit_or_silent_rewrite(self):
        source, q = source_fixture(500)
        view = source_module.build_view(source, q)
        self.assertEqual(view['passage'], source['text'])
        self.assertEqual(view['length_comparison']['status'], 'RECORDED')

    def test_missing_stale_cherry_picked_or_wrong_grade_review_fails(self):
        source, q = source_fixture()
        for replacement in [None, {'profile_id': 'obsolete'}]:
            wrong = deepcopy(q)
            wrong['length_review'] = replacement
            with self.assertRaisesRegex(ValueError, 'length_review'):
                source_module.build_view(source, wrong)
        q['length_review']['benchmark_ids'].pop()
        with self.assertRaisesRegex(ValueError, 'every same-grade'):
            source_module.build_view(source, q)
        q['length_review'] = length_review('제목', 2)
        with self.assertRaisesRegex(ValueError, 'grade differs'):
            source_module.build_view(source, q, expected_grade=1)

    def test_shared_length_uses_long_reference_not_short_title_reference(self):
        source, q = source_fixture()
        with self.assertRaisesRegex(ValueError, 'every same-grade'):
            source_module.build_view(source, q, benchmark_type='long41_42')
        q['length_review'] = length_review('long41_42')
        view = source_module.build_view(source, q, benchmark_type='long41_42')
        self.assertEqual(view['length_comparison']['reference_words'], [212, 212, 216])

    def test_ordering_abc_requires_relabeling(self):
        source, q = source_fixture()
        starts = [s['start'] for s in source['sentences']]
        q.update(type='순서', length_review=length_review('순서'),
                 block_spans={'given': [0, starts[1]], 'A': [starts[1], starts[2]],
                              'B': [starts[2], starts[3]], 'C': [starts[3], len(source['text'])]})
        with self.assertRaisesRegex(ValueError, 'Relabel ordering blocks'):
            source_module.build_view(source, q)

    def test_canonical_order_choice_list_is_enforced(self):
        d = assessment_fixture(False)
        q = d['questions'][0]
        q.update(type='순서', choice_mode='order', given='given', blocks={k:k for k in 'ABC'},
                 permutations=deepcopy(links.ORDER_PERMUTATIONS))
        q['choices'] = [{'number': i+1, 'text': ' → '.join(p)} for i,p in enumerate(q['permutations'])]
        d['explanations'][0].update(choices=deepcopy(q['choices']), choices_ko=[])
        self.assertEqual(links.check(d)['status'], 'PASS')
        q['permutations'][0] = ['A', 'B', 'C']
        self.assertIn('ORDER_CANONICAL_CHOICES', self.codes(d))

    def test_content_prompt_cannot_name_specific_fact(self):
        d = assessment_fixture(False)
        d['questions'][0].update(type='내용', question='바이러스가 치료에 사용되는 방식은?')
        self.assertIn('CONTENT_PROMPT', self.codes(d))
        d['questions'][0]['question'] = '다음 글의 내용과 일치하지 않는 것은?'
        self.assertNotIn('CONTENT_PROMPT', self.codes(d))

    def test_underlined_meaning_needs_exact_prompt_target_span(self):
        d = assessment_fixture(False)
        q = d['questions'][0]
        q.update(type='함축 의미', target='target phrase', question='밑줄 친 target phrase의 의미는?')
        self.assertIn('PROMPT_TARGET_UNDERLINE', self.codes(d))
        start = q['question'].index(q['target'])
        q['prompt_underlines'] = [[start, start+len(q['target'])]]
        self.assertEqual(links.check(d)['status'], 'PASS')
        q['prompt_underlines'][0][0] += 1
        self.assertIn('PROMPT_TARGET_UNDERLINE', self.codes(d))

    def test_shared_pair_default_links_position_and_modes(self):
        d = assessment_fixture()
        self.assertEqual(links.check(d)['status'], 'PASS')
        wrong = deepcopy(d)
        wrong['passage_groups'][0]['passage_question_id'] = 'q4'
        self.assertIn('PASSAGE_GROUP_DEFAULT', self.codes(wrong))
        wrong = deepcopy(d)
        wrong['questions'][0]['passage_group_id'] = 'absent'
        self.assertIn('PASSAGE_GROUP_LINK', self.codes(wrong))
        wrong = deepcopy(d)
        wrong['passage_groups'][0]['question_ids'].reverse()
        self.assertIn('PASSAGE_GROUP_POSITION', self.codes(wrong))

    def test_missing_full_mock_shared_sets_cannot_pass(self):
        d = assessment_fixture(False)
        d['scope'] = {'kind': 'full', 'course': '공통영어1', 'unit_ids': ['u1']}
        self.assertIn('LONG_READING_COVERAGE', self.codes(d))

    def test_unmapped_course_is_not_silently_treated_as_grade_one(self):
        self.assertEqual(check_book.reference_grade('공통영어2', {}), 1)
        self.assertEqual(check_book.reference_grade('영어2', {}), 2)
        with self.assertRaisesRegex(ValueError, 'explicitly verified'):
            check_book.reference_grade('영어I', {})

    def test_course_aliases_share_grade_and_full_mock_counts(self):
        cases = [(c, 2, 7) for c in ['영어II', '영어Ⅱ', '영어2', ' 영어 II ',
                 '영 어 Ⅱ', '영어\t2', '영어\u3000Ⅱ']]
        cases += [(c, 1, 5) for c in ['공통영어1', '공통 영어 1', '공통영어2', '공통 영어\t2']]
        for course, grade, count in cases:
            with self.subTest(course=course):
                self.assertEqual(check_book.reference_grade(course, {}), grade)
                self.assertEqual(course_policy(course)['mock_questions_per_round'], count)
                plan = [{'id': 'wb', 'set_id': 'workbook', 'number': 1, 'unit_id': 'u1'}]
                plan += [{'id': f'{set_id}-{n}', 'set_id': set_id, 'number': n}
                         for set_id in ['mock1', 'mock2', 'mock3'] for n in range(1, count+1)]
                # Isolate the actual production-count check. The absent content
                # records must fail their own checks, but never SET_COUNTS.
                d = {'scope': {'kind': 'full', 'course': course, 'unit_ids': ['u1']},
                     'plan': plan, 'questions': [], 'quick_key': [], 'explanations': []}
                self.assertNotIn('SET_COUNTS', self.codes(d))
                d['plan'].pop()
                self.assertIn('SET_COUNTS', self.codes(d))
                with self.assertRaisesRegex(ValueError, 'conflicts'):
                    check_book.reference_grade(course, {'reference_grade': 3-grade})
        self.assertEqual(normalize_course('영어Ⅱ'), normalize_course('영어 II'))
        self.assertNotEqual(normalize_course('공통영어1'), normalize_course('공통영어2'))

    def test_full_book_accepts_equivalent_course_spacing_without_display_mutation(self):
        from test_book import fixture
        data = fixture()
        data['metadata']['course'] = '공통 영어 1'
        self.assertEqual(check_book.check(data)['status'], 'STRUCTURE_PASS')
        self.assertEqual(data['metadata']['course'], '공통 영어 1')
        self.assertEqual(data['assessment']['scope']['course'], '공통영어1')

    def test_reported_zero_relations_allow_ordinary_workbook_question(self):
        from test_book import fixture
        data = fixture()
        unit = data['units'][0]
        unit['analysis']['relations'] = []
        unit['workbook']['relation_order'] = []
        unit['quantity_exceptions'] = [{'field': 'relations', 'expected': 3, 'actual': 0,
            'reason': 'Synthetic source-shortage record.', 'reported_to_user': 'Synthetic report reference.'}]
        q = data['assessment']['questions'][0]
        del q['learned_relation_uses']
        self.assertEqual(check_book.check(data)['status'], 'STRUCTURE_PASS')
        q['learned_relation_uses'] = []
        self.assertEqual(check_book.check(data)['status'], 'STRUCTURE_PASS')
        # The exception cannot manufacture an absent relation ID, and it cannot
        # bypass the pre-existing requirement to report actual source shortage.
        q['learned_relation_uses'] = [{'term_id': 'invented'}]
        with self.assertRaisesRegex(ValueError, 'assigned common unit'):
            check_book.check(data)
        q['learned_relation_uses'] = []
        del unit['quantity_exceptions']
        with self.assertRaisesRegex(ValueError, 'record actual source shortage'):
            check_book.check(data)

    def test_present_relations_cannot_skip_actual_workbook_connection(self):
        unit = {'analysis': {'relations': [{'head': {'id': 'h'}, 'synonym': {'id': 's'},
                                            'antonym': {'id': 'a'}}]}}
        for q in [{'choices': []}, {'choices': [], 'learned_relation_uses': []}]:
            with self.assertRaisesRegex(ValueError, 'requires actual learned_relation_uses'):
                check_book.check_learned_relation_uses(q, unit)

    def test_workbook_learning_link_checks_actual_choice_span(self):
        unit = {'analysis': {'relations': [{'head': {'id': 'h'}, 'synonym': {'id': 's'},
                                            'antonym': {'id': 'a'}}]}}
        q = {'choices': [{'number': 1, 'text': 'Students repair tools.'}],
             'learned_relation_uses': [{'term_id':'h','choice_number':1,'choice_span':[9,15],
                                       'surface':'repair','reason_ko':'시험용 의미 대응 기록'}]}
        check_book.check_learned_relation_uses(q, unit)
        q['learned_relation_uses'][0]['term_id'] = 'another-unit-word'
        with self.assertRaisesRegex(ValueError, 'assigned common unit'):
            check_book.check_learned_relation_uses(q, unit)
        q['learned_relation_uses'][0]['term_id'] = 'h'
        q['learned_relation_uses'][0]['choice_span'][0] = 8
        with self.assertRaisesRegex(ValueError, 'actual choice span'):
            check_book.check_learned_relation_uses(q, unit)

    def test_five_vocabulary_targets_are_annotated_and_offsets_preserved(self):
        source, q = source_fixture()
        q.update(type='어휘', length_review=length_review('어휘'), replacement_span=[0,7],
                 replacement='replacement', vocabulary_marks=[[i*8, i*8+7] for i in range(5)])
        view = source_module.build_view(source, q)
        self.assertEqual(len(view['annotations']), 5)
        self.assertTrue(all(a['kind'] == 'numbered_word' for a in view['annotations']))
        self.assertEqual(view['source_reconstruction'], 'PASS')

    def test_shared_book_view_is_one_owner_view_with_exact_common_source(self):
        from test_book import fixture
        data = fixture()
        result = check_book.check(data)
        self.assertEqual(len(result['passage_group_views']), 3)
        group = data['assessment']['passage_groups'][0]
        view = result['passage_group_views'][group['id']]
        self.assertEqual(view['question_ids'], group['question_ids'])
        self.assertTrue(view['preserve_paragraphs'])
        self.assertEqual(len(view['annotations']), 5)
        self.assertEqual(view['original'], result['question_views'][group['question_ids'][0]]['original'])
        # A coherent title-only excerpt still cannot silently replace the
        # exact shared long-passage extent.
        qid = group['question_ids'][0]
        request = next(r for r in data['question_sources'] if r['id'] == qid)
        source = next(r for r in data['sources'] if r['id'] == request['source_id'])
        request['first_sentence'] = source['sentences'][1]['id']
        question = next(q for q in data['assessment']['questions'] if q['id'] == qid)
        question['passage'] = source_module.build_view(source, request, benchmark_type='long41_42')['passage']
        with self.assertRaisesRegex(ValueError, 'exact same source extent'):
            check_book.check(data)

    def test_workbook_source_can_leave_unit_but_learning_link_cannot(self):
        from test_book import fixture
        data = fixture()
        q = next(q for q in data['assessment']['questions'] if q['set_id'] == 'workbook')
        request = next(r for r in data['question_sources'] if r['id'] == q['id'])
        other_source = deepcopy(data['sources'][0])
        other_source['id'] = 'second-independent-source-in-this-lesson'
        data['sources'].append(other_source)
        request['source_id'] = other_source['id']
        # Isolate the assessment/learning bridge from the separate source-
        # ingestion coverage checker in this deliberately synthetic unit test.
        with patch.object(check_book, 'check_learning', return_value={'status': 'STRUCTURE_PASS'}):
            self.assertEqual(check_book.check(data)['status'], 'STRUCTURE_PASS')
            q['learned_relation_uses'][0]['term_id'] = 'other-unit-term'
            with self.assertRaisesRegex(ValueError, 'assigned common unit'):
                check_book.check(data)


if __name__ == '__main__':
    unittest.main()
