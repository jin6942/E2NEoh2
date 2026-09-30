"""Review-only diagnostics and displayed-text regressions; no real-book writes."""
from contextlib import redirect_stderr
from copy import deepcopy
from io import StringIO
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / '../scripts'))
from book_plan import compile_plan
from check_book import check
from export_handoff import main, render
from question_source import build_view
from review_packets import make_packet
from test_book_plan import fixture
from test_review_packets import order_book


class HandoffDiagnosticsTests(unittest.TestCase):
    def test_compare_has_only_assigned_length_evidence_including_shared_members(self):
        data = fixture()
        before = deepcopy(data)
        result = check(data)
        packet = make_packet(data, 'questions-compare', question_ids=['mock1-4'])
        rows = packet['comparison']['length_reviews']
        self.assertEqual([r['question_id'] for r in rows], ['mock1-4', 'mock1-5'])
        requests = {r['id']: r for r in data['question_sources']}
        for row in rows:
            qid = row['question_id']
            self.assertEqual(row['length_review'], requests[qid]['length_review'])
            self.assertEqual(row['length_comparison'], result['question_views'][qid]['length_comparison'])
            self.assertTrue(row['length_comparison']['independent_review_required'])
            self.assertEqual(row['length_comparison']['educational_sufficiency'], 'NOT_CHECKED_BY_THIS_TOOL')
        self.assertEqual(packet['review_contract']['comparison_use'],
                         'OPEN_ONLY_AFTER_INDEPENDENT_ANSWERS_ARE_SAVED')
        self.assertEqual(packet['review_contract']['independent_review'], 'NOT_PERFORMED')
        rows[0]['length_review']['benchmark_ids'].clear()
        rows[1]['length_comparison']['rationale'] = 'Changed detached comparison'
        self.assertEqual(data, before)

    def test_author_length_evidence_stays_out_of_blind_and_default_final(self):
        data = fixture()
        for request in data['question_sources']:
            request['length_review']['rationale'] = 'PRIVATE_LENGTH_REASON_SENTINEL'
        before = deepcopy(data)
        blind = make_packet(data, 'questions-blind')
        final = render(data)
        qc = render(data, qc_diagnostics=True)
        for output in (json.dumps(blind), final['learning'], final['assessment'],
                       json.dumps(compile_plan(data))):
            self.assertNotIn('PRIVATE_LENGTH_REASON_SENTINEL', output)
        self.assertNotIn('length_comparison', json.dumps(blind))
        self.assertNotIn('length_review', json.dumps(blind))
        self.assertNotIn('LENGTH_REVIEW:', final['assessment'])
        self.assertNotIn('LENGTH_COMPARISON:', final['assessment'])
        self.assertEqual(qc['learning'], final['learning'])
        self.assertEqual(qc['assessment'].count('LENGTH_REVIEW:\n'), len(data['question_sources']))
        self.assertEqual(qc['assessment'].count('LENGTH_COMPARISON:\n'), len(data['question_sources']))
        result = check(data)
        for request in data['question_sources']:
            block = qc['assessment'].split('[' + request['id'] + ']\n', 1)[1].split('[/' + request['id'] + ']', 1)[0]
            authored = json.loads(block.split('LENGTH_REVIEW:\n', 1)[1].splitlines()[0])
            computed = json.loads(block.split('LENGTH_COMPARISON:\n', 1)[1].splitlines()[0])
            self.assertEqual(authored, request['length_review'])
            self.assertEqual(computed, result['question_views'][request['id']]['length_comparison'])
        self.assertEqual(data, before)

    def test_changed_length_rationale_is_available_after_independent_solving_only(self):
        baseline = fixture()
        current = deepcopy(baseline)
        qid = 'mock2-1'
        request = next(r for r in current['question_sources'] if r['id'] == qid)
        request['length_review']['rationale'] = 'CHANGED_PRIVATE_LENGTH_REASON'
        blind = make_packet(current, 'questions-blind', baseline=baseline, changed_only=True)
        compare = make_packet(current, 'questions-compare', baseline=baseline, changed_only=True)
        self.assertEqual(blind['scope']['assigned']['question_ids'], [qid])
        self.assertNotIn('CHANGED_PRIVATE_LENGTH_REASON', json.dumps(blind))
        self.assertNotIn('change_scope', blind)
        self.assertEqual(compare['comparison']['length_reviews'][0]['length_review']['rationale'],
                         'CHANGED_PRIVATE_LENGTH_REASON')

    def test_annotation_words_use_transformed_passage_and_preserve_raw_spans(self):
        data = fixture()
        before = deepcopy(data)
        result = check(data)
        output = render(data)['assessment']
        changed_found = False
        for gid, view in result['passage_group_views'].items():
            block = output.split('[PASSAGE_GROUP ' + gid + ']\n', 1)[1].split('[/PASSAGE_GROUP', 1)[0]
            self.assertIn('Transformed passage before generated labels', block)
            self.assertIn('not offsets in the displayed PASSAGE', block)
            rows = json.loads(block.split('ANNOTATIONS:\n', 1)[1].splitlines()[0])
            self.assertEqual(len(rows), len(view['annotations']))
            printed = block.split('PASSAGE:\n', 1)[1].split('\nANNOTATIONS_BASIS:', 1)[0]
            for row, raw in zip(rows, view['annotations']):
                self.assertEqual({k: v for k, v in row.items() if k != 'text'}, raw)
                self.assertEqual(row['text'], view['passage'][slice(*raw['span'])])
                self.assertIn(row['text'], printed)
                changed_found |= row['text'] == 'Changed'
            self.assertNotEqual(printed[slice(*rows[0]['span'])], rows[0]['text'])
        self.assertTrue(changed_found)
        self.assertEqual(data, before)

    def test_order_block_source_newline_is_flattened_like_student_output(self):
        data = order_book()
        source = data['sources'][0]
        gap = source['sentences'][2]['end']
        self.assertEqual(source['text'][gap], ' ')
        source['text'] = source['text'][:gap] + '\n' + source['text'][gap + 1:]
        questions = {q['id']: q for q in data['assessment']['questions']}
        for request in data['question_sources']:
            q = questions[request['id']]
            view = build_view(source, request, expected_grade=1,
                              benchmark_type='long41_42' if q.get('passage_group_id') else q['type'])
            for field in ('passage', 'given', 'blocks', 'target'):
                if field in view:
                    q[field] = view[field]
        before = deepcopy(data)
        self.assertTrue(questions['mock1-1']['blocks']['B'].endswith('\n'))
        output = render(data)['assessment']
        question = output.split('[mock1-1]\n', 1)[1].split('[/mock1-1]', 1)[0]
        printed_blocks = question.split('BLOCKS:\n', 1)[1].split('\nCHOICES:', 1)[0]
        student = make_packet(data, 'questions-blind', question_ids=['mock1-1'])
        student_blocks = [b['text'] for b in student['selected_data']['questions'][0]['student_blocks']
                          if b['text'].startswith(('(A) ', '(B) ', '(C) '))]
        self.assertEqual(printed_blocks, '\n'.join(student_blocks))
        self.assertEqual(len(printed_blocks.splitlines()), 3)
        self.assertEqual(data, before)

    def test_qc_diagnostics_cannot_be_used_for_learning_or_named_final_or_packets(self):
        with self.assertRaisesRegex(ValueError, 'assessment handoff'):
            render(fixture(), 'learning', qc_diagnostics=True)
        for options in (['--learning', 'learning_QC.txt'],
                        ['--assessment', 'Book_FINAL.txt'],
                        ['--review-packet', 'blind.json', '--review-role', 'questions-blind']):
            with self.subTest(options=options), patch.object(sys, 'argv',
                    ['export_handoff.py', 'book.json', '--qc-diagnostics', *options]), \
                    redirect_stderr(StringIO()), patch.object(Path, 'read_text') as read_input:
                with self.assertRaises(SystemExit) as error:
                    main()
                self.assertEqual(error.exception.code, 2)
                read_input.assert_not_called()

    def test_qc_diagnostics_does_not_bypass_input_overwrite_guard(self):
        with patch.object(sys, 'argv', ['export_handoff.py', 'book.json',
                          '--qc-diagnostics', '--assessment', 'book.json']), \
                patch.object(Path, 'read_text') as read_input:
            with self.assertRaisesRegex(ValueError, 'paths must be different'):
                main()
            read_input.assert_not_called()


if __name__ == '__main__':
    unittest.main()
