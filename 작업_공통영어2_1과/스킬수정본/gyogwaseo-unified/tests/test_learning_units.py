import importlib.util
import json
import copy
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('learning_units', HERE / '../scripts/learning_units.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def paragraph(pid, count, heading='h1', source='s1'):
    return {'id': pid, 'source_id': source, 'subheading_id': heading,
            'sentence_ids': [f'{pid}-{i+1}' for i in range(count)]}


def approved_merge(rows):
    return {'kind': 'approved-merge', 'source_id': rows[0]['source_id'],
            'subheading_id': rows[0]['subheading_id'],
            'paragraph_ids': [row['id'] for row in rows],
            'sentence_ids': [sid for row in rows for sid in row['sentence_ids']],
            'paragraph_sentence_counts': {row['id']: len(row['sentence_ids']) for row in rows},
            'approved_by': 'user', 'approval_id': 'user-approval-test-2026-09-28',
            'instruction': '사용자가 이 두 원문 단락의 병합을 명시적으로 승인함.'}


def ybm_paragraphs():
    counts = [7, 8, 3, 5, 5, 4, 5, 7, 4, 8, 8, 4, 2]
    headings = [None, None, None, 'H01', 'H01', 'H01', 'H01',
                'H02', 'H02', 'H03', 'H03', 'H04', 'H04']
    return [{'id': f'P{i:02d}', 'source_id': 'UNIT01-본문',
             'subheading_id': heading,
             'sentence_ids': [f'P{i:02d}S{j:02d}' for j in range(1, count + 1)]}
            for i, (count, heading) in enumerate(zip(counts, headings), 1)]


class GroupingTests(unittest.TestCase):
    def test_actual_shaped_eight_plus_eight_requires_explicit_approval(self):
        rows = ybm_paragraphs()
        intro = {'source_id': 'UNIT01-본문', 'paragraph_ids': ['P01', 'P02', 'P03'],
                 'instruction': '사용자 승인: 소제목 없는 도입부 묶어.'}
        default = module.group_units(rows, [intro])
        self.assertEqual(default['status'], 'READY')
        self.assertEqual([len(u['sentence_ids']) for u in default['units']], [18, 19, 11, 8, 8, 6])
        original = copy.deepcopy(rows)
        decision = approved_merge(rows[9:11])
        result = module.group_units(rows, [intro, decision])
        self.assertEqual(result['status'], 'READY')
        self.assertEqual([len(u['sentence_ids']) for u in result['units']], [18, 19, 11, 16, 6])
        self.assertEqual(result['units'][3]['paragraph_ids'], ['P10', 'P11'])
        self.assertEqual(result['units'][3]['reason'], 'explicit-user-approved-merge')
        self.assertEqual(result['units'][3]['approval_id'], decision['approval_id'])
        self.assertEqual(result['units'][:3], default['units'][:3])
        self.assertEqual(result['units'][4], default['units'][5])
        self.assertEqual([sid for unit in result['units'] for sid in unit['sentence_ids']],
                         [sid for row in rows for sid in row['sentence_ids']])
        self.assertEqual(rows, original)

    def test_approved_merge_does_not_change_other_eight_plus_eight(self):
        rows = [paragraph('p1', 8), paragraph('p2', 8),
                paragraph('p3', 8, 'h2'), paragraph('p4', 8, 'h2')]
        result = module.group_units(rows, [approved_merge(rows[:2])])
        self.assertEqual([u['paragraph_ids'] for u in result['units']], [['p1', 'p2'], ['p3'], ['p4']])

    def test_approved_merge_requires_user_approval_record(self):
        rows = [paragraph('p1', 8), paragraph('p2', 8)]
        for key, bad_values in {'approved_by': [None, 'assistant', 'machine', True],
                                'approval_id': [None, '', ' '],
                                'instruction': [None, '', ' ']}.items():
            for value in bad_values:
                with self.subTest(key=key, value=value):
                    decision = approved_merge(rows)
                    decision[key] = value
                    with self.assertRaises(ValueError):
                        module.group_units(rows, [decision])

    def test_approved_merge_binds_exact_sentence_ids_and_counts(self):
        rows = [paragraph('p1', 8), paragraph('p2', 8)]
        decision = approved_merge(rows)
        for key, value in [('sentence_ids', decision['sentence_ids'][:-1]),
                           ('sentence_ids', list(reversed(decision['sentence_ids']))),
                           ('sentence_ids', ['changed'] + decision['sentence_ids'][1:]),
                           ('paragraph_sentence_counts', {'p1': 7, 'p2': 9}),
                           ('paragraph_sentence_counts', {'p1': 8}),
                           ('paragraph_sentence_counts', {'p1': 8, 'p2': 8, 'p3': 8}),
                           ('paragraph_sentence_counts', {'p1': 8.0, 'p2': 8}),
                           ('paragraph_sentence_counts', [8, 8])]:
            with self.subTest(key=key, value=value):
                changed = copy.deepcopy(decision)
                changed[key] = value
                with self.assertRaises(ValueError):
                    module.group_units(rows, [changed])
        changed_rows = copy.deepcopy(rows)
        changed_rows[0]['sentence_ids'][0] = 'new-source-id'
        with self.assertRaises(ValueError):
            module.group_units(changed_rows, [decision])
        changed_rows = copy.deepcopy(rows)
        changed_rows[0]['sentence_ids'].append('extra-source-id')
        with self.assertRaises(ValueError):
            module.group_units(changed_rows, [decision])

    def test_approved_merge_cannot_cross_sources_or_headings_or_be_unheaded(self):
        for rows in [[paragraph('p1', 8), paragraph('p2', 8, 'h2')],
                     [paragraph('p1', 8), paragraph('p2', 8, source='s2')],
                     [paragraph('p1', 8, None), paragraph('p2', 8, None)]]:
            with self.subTest(rows=rows):
                with self.assertRaises(ValueError):
                    module.group_units(rows, [approved_merge(rows)])
        rows = [paragraph('p1', 8), paragraph('p2', 8)]
        for key, value in [('source_id', 'other'), ('subheading_id', 'invented-heading')]:
            decision = approved_merge(rows)
            decision[key] = value
            with self.assertRaises(ValueError):
                module.group_units(rows, [decision])

    def test_approved_merge_cannot_skip_reverse_or_repeat_paragraphs(self):
        rows = [paragraph('p1', 8), paragraph('p2', 8), paragraph('p3', 8)]
        for selected in [[rows[0], rows[2]], [rows[1], rows[0]], [rows[0], rows[0]], [rows[0]]]:
            with self.subTest(selected=selected):
                with self.assertRaises(ValueError):
                    module.group_units(rows, [approved_merge(selected)])

    def test_approved_merge_rejects_overlapping_decisions(self):
        rows = [paragraph('p1', 8), paragraph('p2', 8), paragraph('p3', 8)]
        with self.assertRaises(ValueError):
            module.group_units(rows, [approved_merge(rows[:2]), approved_merge(rows[1:])])

    def test_approved_merge_cannot_partially_consume_short_heading_group(self):
        for rows in [[paragraph('p1', 4), paragraph('p2', 8), paragraph('p3', 8)],
                     [paragraph('p1', 8), paragraph('p2', 8), paragraph('p3', 4)]]:
            for selected in [rows[:2], rows[1:]]:
                with self.subTest(rows=rows, selected=selected):
                    with self.assertRaises(ValueError):
                        module.group_units(rows, [approved_merge(selected)])

    def test_unknown_or_malformed_resolution_rejected(self):
        rows = [paragraph('p1', 8), paragraph('p2', 8)]
        decision = approved_merge(rows)
        decision['kind'] = 'auto-merge'
        for resolutions in [[decision], decision, [None], 'approved-merge']:
            with self.subTest(resolutions=resolutions):
                with self.assertRaises(ValueError):
                    module.group_units(rows, resolutions)

    def test_cli_supports_canonical_and_legacy_resolution_keys(self):
        rows = [paragraph('p1', 8), paragraph('p2', 8)]
        for key in ['grouping_resolutions', 'resolutions']:
            with self.subTest(key=key):
                data = json.dumps({'paragraphs': rows, key: [approved_merge(rows)]})
                with patch.object(sys, 'argv', ['learning_units.py', 'input.json', 'output.json']), \
                        patch.object(Path, 'read_text', return_value=data), \
                        patch.object(Path, 'write_text') as write:
                    self.assertEqual(module.main(), 0)
                    result = json.loads(write.call_args.args[0])
                    self.assertEqual(result['units'][0]['paragraph_ids'], ['p1', 'p2'])

    def test_cli_rejects_conflicting_resolution_keys(self):
        rows = [paragraph('p1', 8), paragraph('p2', 8)]
        data = json.dumps({'paragraphs': rows, 'resolutions': [],
                           'grouping_resolutions': [approved_merge(rows)]})
        with patch.object(sys, 'argv', ['learning_units.py', 'input.json', 'output.json']), \
                patch.object(Path, 'read_text', return_value=data), \
                patch.object(Path, 'write_text') as write:
            with self.assertRaisesRegex(ValueError, 'Conflicting grouping_resolutions'):
                module.main()
            write.assert_not_called()

    def test_explicit_review_can_combine_short_and_adjacent_long(self):
        rows = [paragraph('p1', 4, None), paragraph('p2', 8, None)]
        decision = {'source_id': 's1', 'paragraph_ids': ['p1', 'p2'], 'instruction': '원문 검토 후 두 단락을 묶도록 사용자 결정'}
        result = module.group_units(rows, [decision])
        self.assertEqual(result['status'], 'READY')
        self.assertEqual(result['units'][0]['paragraph_ids'], ['p1', 'p2'])

    def test_review_cannot_skip_or_reverse_paragraphs(self):
        rows = [paragraph('p1', 4, None), paragraph('p2', 4, None), paragraph('p3', 4, None)]
        for ids in [['p1', 'p3'], ['p2', 'p1']]:
            with self.assertRaises(ValueError):
                module.group_units(rows, [{'source_id': 's1', 'paragraph_ids': ids, 'instruction': '시험'}])

    def test_review_cannot_replace_heading_rule(self):
        with self.assertRaises(ValueError):
            module.group_units([paragraph('p1', 4)], [{'source_id': 's1', 'paragraph_ids': ['p1'], 'instruction': '시험'}])

    def test_review_requires_actual_instruction(self):
        with self.assertRaises(ValueError):
            module.group_units([paragraph('p1', 4, None)], [{'source_id': 's1', 'paragraph_ids': ['p1']}])

    def test_review_cannot_cross_independent_sources(self):
        with self.assertRaises(ValueError):
            module.group_units([paragraph('p1', 4, None), paragraph('p2', 4, None, 's2')],
                               [{'source_id': 's1', 'paragraph_ids': ['p1', 'p2'], 'instruction': '시험'}])

    def test_six_merges_entire_heading_including_long_paragraph(self):
        rows = [paragraph('p1', 6), paragraph('p2', 8)]
        result = module.group_units(rows)
        self.assertEqual(result['status'], 'READY')
        self.assertEqual(len(result['units']), 1)
        self.assertEqual(result['units'][0]['sentence_ids'], rows[0]['sentence_ids'] + rows[1]['sentence_ids'])

    def test_seven_preserves_paragraph_units(self):
        result = module.group_units([paragraph('p1', 7), paragraph('p2', 8)])
        self.assertEqual([u['paragraph_ids'] for u in result['units']], [['p1'], ['p2']])

    def test_short_last_paragraph_still_merges_whole_heading(self):
        result = module.group_units([paragraph('p1', 8), paragraph('p2', 4)])
        self.assertEqual([u['paragraph_ids'] for u in result['units']], [['p1', 'p2']])

    def test_headings_and_sources_do_not_cross(self):
        result = module.group_units([paragraph('p1', 4), paragraph('p2', 8),
            paragraph('p3', 4, 'h2'), paragraph('p4', 8, 'h2'),
            paragraph('p5', 4, 'h1', 's2')])
        self.assertEqual([u['paragraph_ids'] for u in result['units']], [['p1', 'p2'], ['p3', 'p4'], ['p5']])

    def test_unheaded_short_does_not_emit_final_map(self):
        result = module.group_units([paragraph('p1', 7, None), paragraph('p2', 6, None)])
        self.assertEqual(result['status'], 'NEEDS_SOURCE_REVIEW')
        self.assertEqual(result['units'], [])
        self.assertEqual(result['unresolved'][0]['paragraph_id'], 'p2')

    def test_unheaded_long_allowed(self):
        result = module.group_units([paragraph('p1', 7, None)])
        self.assertEqual(result['status'], 'READY')

    def test_short_heading_preserved_without_fabrication(self):
        result = module.group_units([paragraph('p1', 2)])
        self.assertEqual(result['units'][0]['sentence_ids'], ['p1-1', 'p1-2'])

    def test_duplicate_sentence_rejected(self):
        rows = [paragraph('p1', 7), paragraph('p2', 7)]
        rows[1]['sentence_ids'][0] = rows[0]['sentence_ids'][0]
        with self.assertRaises(ValueError):
            module.group_units(rows)

    def test_noncontiguous_heading_rejected(self):
        with self.assertRaises(ValueError):
            module.group_units([paragraph('p1', 4), paragraph('p2', 4, 'h2'), paragraph('p3', 8)])

    def test_empty_blocks_rejected(self):
        with self.assertRaises(ValueError):
            module.group_units([paragraph('p1', 0)])
        with self.assertRaises(ValueError):
            module.group_units([])


if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(GroupingTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    (HERE / 'learning-unit-test-results.json').write_text(json.dumps({
        'tests_run': result.testsRun, 'failures': len(result.failures),
        'errors': len(result.errors), 'successful': result.wasSuccessful(),
        'scope': 'Source grouping only; no linguistic or DOCX layout verification'
    }, ensure_ascii=False, indent=2), encoding='utf-8')
    raise SystemExit(0 if result.wasSuccessful() else 1)
