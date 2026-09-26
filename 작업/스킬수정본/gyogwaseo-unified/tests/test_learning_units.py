import importlib.util
import json
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('learning_units', HERE / '../scripts/learning_units.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def paragraph(pid, count, heading='h1', source='s1'):
    return {'id': pid, 'source_id': source, 'subheading_id': heading,
            'sentence_ids': [f'{pid}-{i+1}' for i in range(count)]}


class GroupingTests(unittest.TestCase):
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
