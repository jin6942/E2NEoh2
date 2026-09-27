"""Mechanical diagnostics do not substitute for educational or final review."""
from copy import deepcopy
import contextlib
import io
import json
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch
import uuid

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'scripts'))
import review_preflight as m
from test_book import fixture
from test_learning_content import fixture as learning_fixture
from test_question_source import fixture as source_fixture
from revision_fixtures import length_review


def diagnostics(data, code):
    return [row for row in m.check(data)['diagnostics'] if row['code'] == code]


def hint(original, shown):
    return {'span': [0, len(original)], 'meaning_ko': '합성 검수 근거',
            'explanation': '합성 검수 근거', 'structure_label': '시험용 구조',
            'display_pairs': [{'en': shown, 'ko': '[시험용] 설명'}]}


class ReviewPreflightTests(unittest.TestCase):
    def test_normal_book_is_compact_read_only_and_never_certified(self):
        data = fixture()
        before = deepcopy(data)
        result = m.check(data)
        self.assertEqual(result, m.check(data))
        self.assertEqual(data, before)
        self.assertEqual(result['status'], 'NOT_CERTIFIED')
        self.assertEqual(result['check_book']['status'], 'STRUCTURE_PASS')
        self.assertEqual(result['diagnostic_counts']['ERROR'], 0)
        self.assertNotIn(data['sources'][0]['text'], json.dumps(result, ensure_ascii=False))
        self.assertNotIn('question_views', result['check_book'])
        self.assertEqual(result['independent_reviews'], 'NOT_PERFORMED')

    def test_existing_answer_error_remains_fail_closed(self):
        data = fixture()
        data['assessment']['quick_key'][0]['answer'] = 5
        result = m.check(data)
        self.assertEqual(result['check_book']['status'], 'FAIL')
        self.assertTrue(any(row['code'] == 'QUICK_ANSWER_MISMATCH' for row in result['diagnostics']))

    def test_existing_source_failure_is_not_a_warning_pass(self):
        data = fixture()
        data['assessment']['questions'][0]['passage'] += ' Changed.'
        result = m.check(data)
        self.assertEqual(result['check_book']['status'], 'FAIL')
        self.assertEqual(result['diagnostics'][0]['code'], 'CHECK_BOOK_EXCEPTION')

    def test_pending_source_review_is_preserved(self):
        data = fixture()
        source = data['sources'][0]
        offset = 0
        source['text'] = ''.join(row['text'] for row in data['sentences'])
        for bounds, sentence in zip(source['sentences'], data['sentences']):
            bounds.update(start=offset, end=offset + len(sentence['text']))
            offset = bounds['end']
        result = m.check(data)
        self.assertEqual(result['check_book']['status'], 'NEEDS_SOURCE_REVIEW')
        self.assertTrue(result['diagnostic_counts']['ERROR'])

    def test_summary_requires_exactly_one_a_then_one_b_only_in_summary(self):
        for summary, expected in [('The (A) part supports (B).', False),
                                  ('The (B) part supports (A).', True),
                                  ('The (A) part supports (B) and (B).', True),
                                  ('The (A) part.', True)]:
            with self.subTest(summary=summary):
                data = fixture()
                q = data['assessment']['questions'][1]
                q.update(type='요약', summary=summary)
                data['question_sources'][1]['type'] = '요약'
                data['question_sources'][1]['length_review'] = length_review('요약')
                data['assessment']['explanations'][1]['evidence'] = '(B) source evidence appears before (A).'
                result = m.check(data)
                self.assertEqual(result['check_book']['status'], 'STRUCTURE_PASS')
                rows = [r for r in result['diagnostics'] if r['code'] == 'SUMMARY_AB_MARKERS']
                self.assertEqual(bool(rows), expected)
                if rows:
                    self.assertEqual(rows[0]['severity'], 'ERROR')
                    self.assertEqual(rows[0]['question_id'], q['id'])

    def test_rendered_four_sentences_inside_three_elements_warn_without_edit(self):
        data = fixture()
        row = data['units'][0]['analysis']['easy_explanations'][0]
        row['explanatory_sentences'] = ['처음 설명이다. 다음 설명이다.', '세 번째다.', '네 번째다.']
        before = deepcopy(data)
        result = m.check(data)
        self.assertEqual(data, before)
        self.assertEqual(result['check_book']['status'], 'STRUCTURE_PASS')
        warning = next(r for r in result['diagnostics'] if r['code'] == 'EASY_EXPLANATION_SENTENCE_COUNT')
        self.assertEqual(warning['sentence_count_candidate'], 4)
        self.assertEqual(warning['multiple_sentence_elements'], [1])
        self.assertEqual(warning['severity'], 'WARNING')

    def test_multiple_sentences_per_element_warn_even_when_total_is_three(self):
        data = fixture()
        data['units'][0]['analysis']['easy_explanations'][0]['explanatory_sentences'] = ['하나다. 둘이다.', '셋이다.']
        self.assertEqual(diagnostics(data, 'EASY_EXPLANATION_SENTENCE_COUNT')[0]['sentence_count_candidate'], 3)

    def test_decimals_abbreviations_and_ellipsis_do_not_add_sentences(self):
        data = fixture()
        data['units'][0]['analysis']['easy_explanations'][0]['explanatory_sentences'] = [
            'Dr. Kim은 U.S. 자료에서 3.5를 보았다.', 'e.g. 예시...를 차근차근 설명한다.']
        self.assertFalse(diagnostics(data, 'EASY_EXPLANATION_SENTENCE_COUNT'))

    def test_explanation_sentence_count_has_no_two_to_three_limit(self):
        for count in [1, 4, 8]:
            with self.subTest(count=count):
                data = fixture()
                data['units'][0]['analysis']['easy_explanations'][0]['explanatory_sentences'] = [
                    f'이는 {index}번째 설명이다.' for index in range(count)]
                before = deepcopy(data)
                result = m.check(data)
                self.assertEqual(result['check_book']['status'], 'STRUCTURE_PASS')
                self.assertFalse(any(r['code'] == 'EASY_EXPLANATION_SENTENCE_COUNT'
                                     for r in result['diagnostics']))
                self.assertEqual(data, before)

    def test_hint_warns_on_actual_display_and_not_internal_span(self):
        data = fixture()
        sentence = data['sentences'][0]
        sentence['hints'] = [hint(sentence['text'], '[They] repair …')]
        self.assertFalse(diagnostics(data, 'HINT_DISPLAY_LENGTH'))
        sentence['hints'][0]['display_pairs'][0]['en'] = '[' + sentence['text'] + ']'
        rows = diagnostics(data, 'HINT_DISPLAY_LENGTH')
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]['displayed_ratio'], 1)
        self.assertEqual(rows[0]['severity'], 'WARNING')

    def test_hint_threshold_is_inclusive_but_short_original_is_exempt(self):
        for original_count, shown_count, expected in [(15, 12, True), (15, 11, False), (14, 14, False)]:
            with self.subTest(original_count=original_count, shown_count=shown_count):
                original = ' '.join(['word'] * original_count)
                data = learning_fixture([original, 'We save valuable materials.', 'I protect local resources.'])
                data['sentences'][0]['hints'] = [hint(original, '[' + ' '.join(['word'] * shown_count) + '] …')]
                self.assertEqual(bool(diagnostics(data, 'HINT_DISPLAY_LENGTH')), expected)

    def test_function_formula_does_not_use_source_ratio(self):
        data = fixture()
        sentence = data['sentences'][0]
        sentence['hints'] = [{'category': 'function-combination', 'display_pairs': [
            {'en': 'to V + ' + ' '.join(['word'] * 60), 'ko': '시험용 뜻'}]}]
        result = m.check(data)
        self.assertEqual(result['formula_hints_excluded_from_ratio'], 1)
        self.assertFalse(any(r['code'] == 'HINT_DISPLAY_LENGTH' for r in result['diagnostics']))

    def test_every_choice_gets_overlap_warning_with_context_and_offsets(self):
        data = fixture()
        q = data['assessment']['questions'][1]
        phrase = ' '.join(q['passage'].split()[:5])
        for choice in q['choices']:
            choice['text'] = phrase + f' alternative {choice["number"]}'
        rows = [r for r in diagnostics(data, 'CHOICE_PASSAGE_OVERLAP') if r['question_id'] == q['id']]
        self.assertEqual([r['choice_number'] for r in rows], [1, 2, 3, 4, 5])
        for row in rows:
            example = row['examples'][0]
            self.assertEqual(example['phrase'], q['passage'][slice(*example['passage_span'])])
            self.assertTrue(example['context'])
            self.assertEqual(row['severity'], 'WARNING')

    def test_four_word_match_and_interrupted_sequence_do_not_warn(self):
        data = fixture()
        q = data['assessment']['questions'][1]
        words = q['passage'].split()[:5]
        q['choices'][0]['text'] = ' '.join(words[:4])
        q['choices'][1]['text'] = ' '.join(words[:2] + ['DIFFERENT'] + words[2:])
        self.assertFalse([r for r in diagnostics(data, 'CHOICE_PASSAGE_OVERLAP') if r['question_id'] == q['id']])

    def test_symbolic_types_and_order_choices_are_not_word_overlap_targets(self):
        for kind in ['삽입', '어휘', '무관한 문장', '순서']:
            data = fixture()
            q = data['assessment']['questions'][1]
            q['type'] = kind
            q['choices'][0]['text'] = q['passage']
            self.assertFalse([r for r in diagnostics(data, 'CHOICE_PASSAGE_OVERLAP') if r['question_id'] == q['id']])

    def test_shared_passage_uses_the_displayed_owner_not_hidden_normal_text(self):
        data = fixture()
        q = data['assessment']['questions'][4]
        owner = data['assessment']['questions'][5]
        self.assertEqual(q['passage_group_id'], owner['passage_group_id'])
        q['choices'][0]['text'] = ' '.join(q['passage'].split()[:5])
        self.assertNotEqual(q['passage'].split()[0], owner['passage'].split()[0])
        self.assertFalse([r for r in diagnostics(data, 'CHOICE_PASSAGE_OVERLAP') if r['question_id'] == q['id']])

    def test_set_distribution_is_information_and_never_each_number_once(self):
        data = fixture()
        q = data['assessment']['questions'][2]
        new_answer = 2
        q['answer'] = new_answer
        data['assessment']['quick_key'][2]['answer'] = new_answer
        exp = data['assessment']['explanations'][2]
        exp['answer'] = new_answer
        exp['wrong_reasons'] = [{'number': n, 'text': '시험용 배제 근거'} for n in range(1, 6) if n != new_answer]
        result = m.check(data)
        self.assertEqual(result['check_book']['status'], 'STRUCTURE_PASS')
        row = next(r for r in result['diagnostics'] if r['code'] == 'SET_ANSWER_DISTRIBUTION' and r['set_id'] == 'mock1')
        self.assertEqual(row['severity'], 'INFO')
        self.assertEqual(row['counts']['2'], 2)
        self.assertEqual(row['counts']['3'], 0)
        self.assertEqual(result['diagnostic_counts']['ERROR'], 0)

    def test_irrelevant_gap_warning_allows_unmarked_leading_and_trailing_sentences(self):
        for marks, expected in [(['s1', '@added', 's2', 's3', 's4'], False),
                                (['s1', '@added', 's3', 's4', 's5'], True)]:
            source, request = source_fixture()
            request.update(id='gap-question', type='무관한 문장', addition='An inserted unrelated sentence.',
                           addition_offset=source['sentences'][2]['start'], sentence_marks=marks,
                           length_review=length_review('무관한 문장'))
            view = m.build_view(source, request)
            q = {'id': request['id'], 'type': request['type'], 'set_id': 'mock1', 'choice_mode': 'in_passage',
                 'passage': view['passage'], 'answer': view['answer']}
            data = {'sources': [source], 'question_sources': [request], 'assessment': {'questions': [q]}}
            rows = diagnostics(data, 'IRRELEVANT_TARGETS_NONADJACENT')
            self.assertEqual(bool(rows), expected)
            if rows:
                self.assertEqual(rows[0]['severity'], 'WARNING')
                self.assertEqual(rows[0]['intervening_sentence_ids'], ['s2'])

    def test_invalid_record_shapes_are_noncertified_failures(self):
        for data in [None, [], {}, {'assessment': {'questions': [{'type': [], 'id': [], 'answer': True}]}}]:
            with self.subTest(data=data):
                result = m.check(data)
                self.assertEqual(result['status'], 'NOT_CERTIFIED')
                self.assertEqual(result['check_book']['status'], 'FAIL')

    def test_cli_preserves_input_and_refuses_overwrite(self):
        # Ordinary mkdir preserves workspace ACLs on Windows; Python's 0700
        # TemporaryDirectory can make its children unreadable in this sandbox.
        folder = HERE.parents[3] / ('review-preflight-' + uuid.uuid4().hex)
        folder.mkdir()
        input_path, output_path = folder / 'input.json', folder / 'report.json'
        final_path, docx_path = folder / 'learning_FINAL.txt', folder / 'book.docx'
        invalid_report = folder / 'invalid-report.json'
        try:
            input_path.write_text(json.dumps(fixture(), ensure_ascii=False), encoding='utf-8')
            before = input_path.read_bytes()
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(m.main([str(input_path), str(output_path)]), 0)
            result = json.loads(output_path.read_text(encoding='utf-8'))
            self.assertEqual(result['status'], 'NOT_CERTIFIED')
            self.assertEqual(input_path.read_bytes(), before)
            final_path.write_bytes('기존 FINAL 원문\n'.encode('utf-8'))
            docx_path.write_bytes(b'PK\x03\x04Existing DOCX bytes\x00\xff')
            for protected in [input_path, output_path, final_path, docx_path]:
                preserved = protected.read_bytes()
                with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
                    m.main([str(input_path), str(protected)])
                self.assertEqual(protected.read_bytes(), preserved)
            self.assertEqual(input_path.read_bytes(), before)
            input_path.write_text('{invalid', encoding='utf-8')
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(m.main([str(input_path), str(invalid_report)]), 1)
            self.assertEqual(json.loads(invalid_report.read_text(encoding='utf-8'))['diagnostics'][0]['code'], 'INPUT_JSON')
        finally:
            # Only exact test files and this unique empty directory.
            for path in [input_path, output_path, final_path, docx_path, invalid_report]:
                path.unlink(missing_ok=True)
            folder.rmdir()

    def test_cli_exclusive_create_preserves_a_file_created_during_check(self):
        folder = HERE.parents[3] / ('review-preflight-' + uuid.uuid4().hex)
        folder.mkdir()
        input_path, output_path = folder / 'input.json', folder / 'raced_FINAL.txt'
        sentinel = b'Existing final created after precheck\x00\xff'
        original_check = m.check

        def concurrent_creation(data):
            output_path.write_bytes(sentinel)
            return original_check(data)

        try:
            input_path.write_text(json.dumps(fixture(), ensure_ascii=False), encoding='utf-8')
            before = input_path.read_bytes()
            with patch.object(m, 'check', side_effect=concurrent_creation), self.assertRaises(FileExistsError):
                m.main([str(input_path), str(output_path)])
            self.assertEqual(output_path.read_bytes(), sentinel)
            self.assertEqual(input_path.read_bytes(), before)
        finally:
            input_path.unlink(missing_ok=True)
            output_path.unlink(missing_ok=True)
            folder.rmdir()

    def test_help_documents_noncertifying_read_only_contract(self):
        run = subprocess.run([sys.executable, '-B', str(HERE.parent / 'scripts/review_preflight.py'), '--help'],
                             capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(run.returncode, 0)
        self.assertIn('NOT_CERTIFIED', run.stdout)
        self.assertIn('read-only', run.stdout)


if __name__ == '__main__':
    unittest.main()
