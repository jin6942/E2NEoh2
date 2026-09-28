import importlib.util
import hashlib
import json
import subprocess
import sys
import uuid
from copy import deepcopy
from pathlib import Path
import unittest

MODULE = Path(__file__).parent / '../scripts/sv_line.py'
spec = importlib.util.spec_from_file_location('sv_line', MODULE)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def span(text, fragment):
    start = text.index(fragment)
    return [[start, start + len(fragment)]]


class SVLineTests(unittest.TestCase):
    def noun_phrase_review(self, original):
        return {'kind': 'noun-phrase-answer', 'reviewed': True,
                'reason': 'Answer to the preceding question; called and based are participial modifiers, not finite verbs.',
                'source_text_sha256': hashlib.sha256(original.encode('utf-8')).hexdigest(),
                'context_sentence_id': 'P04S03',
                'context_text_sha256': hashlib.sha256(
                    b'What eventually emerged from these parties?').hexdigest()}

    def test_reviewed_actual_noun_phrase_answer_omits_entire_line(self):
        original = ('A vibrant youth movement called hip-hop culture, based on DJing, '
                    'breakdancing, MCing, and graffiti.')
        review = self.noun_phrase_review(original)
        before = deepcopy(review)
        self.assertEqual(module.render_sv(original, [], review), '')
        self.assertEqual(review, before)

    def test_empty_or_missing_clauses_without_review_remain_errors(self):
        for clauses in [[], None]:
            with self.subTest(clauses=clauses), self.assertRaisesRegex(ValueError, 'clause records'):
                module.render_sv('A vibrant youth movement.', clauses)

    def test_noun_phrase_review_rejects_invalid_records_and_stale_source(self):
        original = 'A vibrant youth movement.'
        base = self.noun_phrase_review(original)
        cases = [('kind', 'fragment'), ('reviewed', False), ('reviewed', 1),
                 ('reason', ''), ('reason', '  '), ('context_sentence_id', ''),
                 ('source_text_sha256', '0' * 64), ('source_text_sha256', None),
                 ('context_text_sha256', 'not-a-hash')]
        for field, value in cases:
            review = dict(base, **{field: value})
            with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                module.render_sv(original, [], review)
        for field in base:
            review = dict(base); review.pop(field)
            with self.subTest(missing=field), self.assertRaises(ValueError):
                module.render_sv(original, [], review)

    def test_noun_phrase_review_requires_explicit_empty_clauses(self):
        original = 'A vibrant youth movement.'
        for clauses in [None, {}, [{'kind': 'main'}]]:
            with self.subTest(clauses=clauses), self.assertRaisesRegex(ValueError, 'explicit clauses'):
                module.render_sv(original, clauses, self.noun_phrase_review(original))

    def test_standalone_cli_forwards_review_and_writes_no_placeholder_line(self):
        original = 'A vibrant youth movement.'
        folder = Path(__file__).resolve().parent / ('sv-cli-' + uuid.uuid4().hex)
        folder.mkdir(); source = folder / 'input.json'; output = folder / 'output.txt'
        try:
            source.write_text(json.dumps({'original': original, 'clauses': [],
                'sv_review': self.noun_phrase_review(original)}), encoding='utf-8')
            result = subprocess.run([sys.executable, '-B', str(MODULE), str(source), str(output)],
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(output.read_bytes(), b'')
        finally:
            for path in [source, output]:
                if path.exists():
                    path.unlink()
            folder.rmdir()

    def subject_clause(self, text, full, displayed, verb='are', kind='main'):
        return {'kind': kind, 'start': 0, 'subject_spans': span(text, full),
                'subject_display_spans': span(text, displayed),
                'subject_display_review': 'Reviewed basic noun phrase; trailing postmodifier omitted only in S display.',
                'verb_spans': span(text, verb)}

    def contracted(self, text, verb, expanded=None, kind='main'):
        apostrophe = '’s' if '’s' in text else "'s"
        clause = {'kind': kind, 'start': 0, 'subject_spans': span(text, 'It'),
                  'verb_spans': span(text, verb)}
        if expanded is not None:
            clause['contraction_readings'] = [{'span': span(text, apostrophe)[0], 'expanded': expanded}]
        return clause

    def test_contracted_is_keeps_original_form(self):
        text = "It's clear."
        self.assertEqual(module.render_sv(text, [self.contracted(text, "'s", 'is')]), "S: It, V: 's")

    def test_contracted_has_is_annotated(self):
        text = "It's changed."
        self.assertEqual(module.render_sv(text, [self.contracted(text, "'s changed", 'has')]),
                         "S: It, V: 's(has) changed")

    def test_curly_apostrophe_preserved_in_has(self):
        text = 'It’s been repaired.'
        self.assertEqual(module.render_sv(text, [self.contracted(text, '’s been repaired', 'has')]),
                         'S: It, V: ’s(has) been repaired')

    def test_same_surface_can_be_passive_is(self):
        text = "It's repaired every year."
        self.assertEqual(module.render_sv(text, [self.contracted(text, "'s repaired", 'is')]),
                         "S: It, V: 's repaired")

    def test_unreviewed_contraction_not_silently_assumed_is(self):
        text = "It's changed."
        with self.assertRaisesRegex(ValueError, 'reviewed is/has'):
            module.render_sv(text, [self.contracted(text, "'s changed")])

    def test_annotation_outside_verb_rejected(self):
        text = "It's changed."
        clause = self.contracted(text, "'s changed", 'has')
        clause['contraction_readings'][0]['span'] = [0, 2]
        with self.assertRaisesRegex(ValueError, 'actual verb contraction'):
            module.render_sv(text, [clause])

    def test_subordinate_has_uses_same_annotation(self):
        text = "It seems that she’s finished."
        clauses = [
            {'kind': 'main', 'start': 0, 'subject_spans': span(text, 'It'), 'verb_spans': span(text, 'seems')},
            {'kind': 'subordinate', 'start': 9, 'marker': 'that', 'subject_spans': span(text, 'she'),
             'verb_spans': span(text, '’s finished'),
             'contraction_readings': [{'span': span(text, '’s')[0], 'expanded': 'has'}]},
        ]
        self.assertEqual(module.render_sv(text, clauses),
                         'S: It, V: seems ／ [that] S′: she, V′: ’s(has) finished')

    def test_imperative_no_invented_you(self):
        text = 'Open the door.'
        self.assertEqual(module.render_sv(text, [
            {'kind': 'imperative', 'start': 0, 'verb_spans': span(text, 'Open')}
        ]), 'V: Open')

    def test_subject_relative_has_v_prime_only(self):
        text = 'The boy who smiled left.'
        result = module.render_sv(text, [
            {'kind': 'main', 'start': 0, 'subject_spans': span(text, 'The boy who smiled'),
             'verb_spans': span(text, 'left')},
            {'kind': 'subject_relative', 'start': 8, 'marker': 'who',
             'verb_spans': span(text, 'smiled')},
        ])
        self.assertEqual(result, 'S: The boy who smiled, V: left ／ [who] V′: smiled')

    def test_object_relative_displays_explicit_subject(self):
        text = 'The book that Mina read disappeared.'
        result = module.render_sv(text, [
            {'kind': 'main', 'start': 0, 'subject_spans': span(text, 'The book that Mina read'),
             'verb_spans': span(text, 'disappeared')},
            {'kind': 'subordinate', 'start': 9, 'marker': 'that',
             'subject_spans': span(text, 'Mina'), 'verb_spans': span(text, 'read')},
        ])
        self.assertIn('[that] S′: Mina, V′: read', result)

    def test_initial_subordinate_keeps_source_order(self):
        text = 'When Mina arrived, Joon smiled.'
        result = module.render_sv(text, [
            {'kind': 'main', 'start': 19, 'subject_spans': span(text, 'Joon'),
             'verb_spans': span(text, 'smiled')},
            {'kind': 'subordinate', 'start': 0, 'marker': 'When',
             'subject_spans': span(text, 'Mina'), 'verb_spans': span(text, 'arrived')},
        ])
        self.assertEqual(result, '[When] S′: Mina, V′: arrived ／ S: Joon, V: smiled')

    def test_all_head_exception_with_omitted_relative(self):
        text = 'All you need is love.'
        result = module.render_sv(text, [
            {'kind': 'main', 'start': 0, 'subject_spans': span(text, 'All'),
             'verb_spans': span(text, 'is')},
            {'kind': 'subordinate', 'start': 4, 'marker': 'that', 'omitted_marker': True,
             'subject_spans': span(text, 'you'), 'verb_spans': span(text, 'need')},
        ])
        self.assertEqual(result, 'S: All, V: is ／ [(that)] S′: you, V′: need')

    def test_reviewed_subject_prefix_retains_full_range_and_omitted_relative(self):
        text = 'There could be many more possible solutions to the problems we currently face.'
        clauses = [self.subject_clause(
            text, 'many more possible solutions to the problems we currently face',
            'many more possible solutions', 'could be'),
            {'kind': 'subordinate', 'start': text.index('we'),
             'marker': 'that', 'omitted_marker': True,
             'subject_spans': span(text, 'we'), 'verb_spans': span(text, 'face')}]
        before = deepcopy(clauses)
        self.assertEqual(module.render_sv(text, clauses),
                         'S: many more possible solutions, V: could be ／ [(that)] S′: we, V′: face')
        self.assertEqual(clauses, before)
        self.assertEqual(module.extract_parts(text, clauses[0]['subject_spans'], 'subject'),
                         'many more possible solutions to the problems we currently face')

    def test_subordinate_subject_prefix_retains_nested_subject_relative(self):
        text = 'I know that the boy who smiled is ready.'
        sub = self.subject_clause(text, 'the boy who smiled', 'the boy', 'is', 'subordinate')
        sub.update(start=text.index('that'), marker='that')
        clauses = [
            {'kind': 'main', 'start': 0, 'subject_spans': span(text, 'I'),
             'verb_spans': span(text, 'know')}, sub,
            {'kind': 'subject_relative', 'start': text.index('who'), 'marker': 'who',
             'verb_spans': span(text, 'smiled')},
        ]
        self.assertEqual(module.render_sv(text, clauses),
                         'S: I, V: know ／ [that] S′: the boy, V′: is ／ [who] V′: smiled')

    def test_no_automatic_truncation_of_protected_subject_structures(self):
        for subject, verb in [('Achieving these goals', 'matters'), ('What she said', 'matters'),
                              ('A number of trees', 'remain'),
                              ('Some of the most unusual ones', 'remain'),
                              ('Existing cells and tissue', 'remain')]:
            text = subject + ' ' + verb + '.'
            clause = {'kind': 'main', 'start': 0, 'subject_spans': span(text, subject),
                      'verb_spans': span(text, verb)}
            with self.subTest(subject=subject):
                self.assertEqual(module.render_sv(text, [clause]), f'S: {subject}, V: {verb}')
                clause.update(subject_display_spans=span(text, subject),
                              subject_display_review='Keep this reviewed subject structure complete.')
                self.assertEqual(module.render_sv(text, [clause]), f'S: {subject}, V: {verb}')

    def test_subject_display_requires_both_fields_and_nonempty_review(self):
        text = 'The tools in the room are ready.'
        base = self.subject_clause(text, 'The tools in the room', 'The tools')
        cases = []
        for key in ['subject_display_spans', 'subject_display_review']:
            clause = deepcopy(base); clause.pop(key); cases.append(clause)
        for review in ['', ' \n ', None, False, 7]:
            clause = deepcopy(base); clause['subject_display_review'] = review; cases.append(clause)
        for clause in cases:
            with self.subTest(clause=clause), self.assertRaisesRegex(ValueError, 'subject_display_review'):
                module.render_sv(text, [clause])

    def test_subject_display_rejects_empty_multiple_and_invalid_spans(self):
        text = 'The tools in the room are ready.'
        base = self.subject_clause(text, 'The tools in the room', 'The tools')
        for spans in [[], None, [[0, 0]], [[0, 3], [4, 9]], [[0, True]],
                      [[0, len(text) + 1]], [[9, 4]]]:
            clause = deepcopy(base); clause['subject_display_spans'] = spans
            with self.subTest(spans=spans), self.assertRaises(ValueError):
                module.render_sv(text, [clause])

    def test_subject_display_cannot_remove_premodifiers_or_exceed_full_subject(self):
        text = 'The new tools in the room are ready.'
        base = self.subject_clause(text, 'The new tools in the room', 'The new tools')
        for selected in ['new tools', 'tools', 'The new tools in the room are']:
            clause = deepcopy(base); clause['subject_display_spans'] = span(text, selected)
            with self.subTest(selected=selected), self.assertRaisesRegex(ValueError, 'prefix inside'):
                module.render_sv(text, [clause])

    def test_subject_display_rejects_partial_words_hyphens_and_apostrophes(self):
        for text, full, shortened in [
            ('The tools nearby work.', 'The tools nearby', 'The tool'),
            ('The eco-friendly tools work.', 'The eco-friendly tools', 'The eco-'),
            ("The child's tools work.", "The child's tools", 'The child'),
            ('The child’s tools work.', 'The child’s tools', 'The child'),
        ]:
            clause = self.subject_clause(text, full, shortened, 'work')
            with self.subTest(text=text), self.assertRaisesRegex(ValueError, 'token boundaries'):
                module.render_sv(text, [clause])

    def test_subject_display_rejects_edge_whitespace_and_midword_source_start(self):
        text = 'The tools in the room are ready.'
        clause = self.subject_clause(text, 'The tools in the room', 'The tools ')
        with self.assertRaisesRegex(ValueError, 'edge whitespace'):
            module.render_sv(text, [clause])
        clause = self.subject_clause(text, 'he tools in the room', 'he tools')
        with self.assertRaisesRegex(ValueError, 'token boundaries'):
            module.render_sv(text, [clause])

    def test_subject_display_cannot_drop_a_disjoint_subject_component(self):
        text = 'The tools and machines are ready.'
        clause = self.subject_clause(text, 'The tools and machines', 'The tools')
        clause['subject_spans'] = span(text, 'The tools') + span(text, 'and machines')
        before = deepcopy(clause)
        with self.assertRaisesRegex(ValueError, 'one complete source span'):
            module.render_sv(text, [clause])
        self.assertEqual(clause, before)

    def test_subject_relative_and_subjectless_imperative_cannot_invent_display_subject(self):
        text = 'The boy who smiled left.'
        clause = {'kind': 'subject_relative', 'start': text.index('who'), 'marker': 'who',
                  'verb_spans': span(text, 'smiled'), 'subject_display_spans': span(text, 'who'),
                  'subject_display_review': 'Invalid attempt to duplicate relative subject.'}
        with self.assertRaisesRegex(ValueError, 'cannot add a displayed subject'):
            module.render_sv(text, [clause])
        text = 'Open the door.'
        clause = {'kind': 'imperative', 'start': 0, 'verb_spans': span(text, 'Open'),
                  'subject_display_spans': span(text, 'the door'),
                  'subject_display_review': 'Invalid attempt to create a subject.'}
        with self.assertRaisesRegex(ValueError, 'one complete source span'):
            module.render_sv(text, [clause])

    def test_relative_subject_duplicate_rejected(self):
        text = 'The boy who smiled left.'
        with self.assertRaisesRegex(ValueError, 'V′ only'):
            module.render_sv(text, [{'kind': 'subject_relative', 'start': 8, 'marker': 'who',
                                   'subject_spans': span(text, 'who'),
                                   'verb_spans': span(text, 'smiled')}])

    def test_bracketed_main_label_rejected(self):
        text = 'Mina smiled.'
        with self.assertRaisesRegex(ValueError, '주절'):
            module.render_sv(text, [{'kind': 'main', 'start': 0, 'marker': '주절',
                                   'subject_spans': span(text, 'Mina'),
                                   'verb_spans': span(text, 'smiled')}])

    def test_nested_coordinated_subordinate_can_keep_prime(self):
        text = 'I know that Mina left and Joon stayed.'
        result = module.render_sv(text, [
            {'kind': 'main', 'start': 0, 'subject_spans': span(text, 'I'),
             'verb_spans': span(text, 'know')},
            {'kind': 'subordinate', 'start': 7, 'marker': 'that',
             'subject_spans': span(text, 'Mina'), 'verb_spans': span(text, 'left')},
            {'kind': 'subordinate', 'start': 21, 'marker': 'and',
             'subject_spans': span(text, 'Joon'), 'verb_spans': span(text, 'stayed')},
        ])
        self.assertIn('[and] S′: Joon, V′: stayed', result)

    def test_reviewed_unit03_parallel_verbs_retain_source_connectors(self):
        text = ('Because the baby stops crying, the tiger mistakenly thinks the gotgam '
                'is a very scary creature and runs away.')
        clauses = [
            {'kind': 'subordinate', 'start': 0, 'marker': 'Because',
             'subject_spans': [[8, 16]], 'verb_spans': [[17, 22]]},
            {'kind': 'main', 'start': 31, 'subject_spans': [[31, 40]],
             'verb_spans': [[52, 58], [95, 98], [99, 103]]},
            {'kind': 'subordinate', 'start': 59, 'marker': 'that', 'omitted_marker': True,
             'subject_spans': [[59, 69]], 'verb_spans': [[70, 72]]},
        ]
        before = deepcopy(clauses)
        self.assertEqual(module.render_sv(text, clauses),
                         '[Because] S′: the baby, V′: stops ／ S: the tiger, V: thinks and runs'
                         ' ／ [(that)] S′: the gotgam, V′: is')
        self.assertEqual(clauses, before)
        text = ('Tigers in Korea faced a decline in population due to hunting during the '
                'Joseon period and nearly went extinct during the Japanese colonial era.')
        clause = self.subject_clause(text, 'Tigers in Korea', 'Tigers', 'faced')
        clause['verb_spans'] = [[16, 21], [86, 89], [97, 101]]
        self.assertEqual(module.render_sv(text, [clause]), 'S: Tigers, V: faced and went')

    def test_reviewed_coordination_preserves_each_original_connector(self):
        for connector in ['and', 'or', 'but']:
            text = f'She reads {connector} writes.'
            clause = {'kind': 'main', 'start': 0, 'subject_spans': span(text, 'She'),
                      'verb_spans': span(text, 'reads') + span(text, connector) + span(text, 'writes')}
            with self.subTest(connector=connector):
                self.assertEqual(module.render_sv(text, [clause]),
                                 f'S: She, V: reads {connector} writes')

    def test_fragmented_auxiliary_verbs_do_not_invent_coordination(self):
        cases = [
            ('More and more waste is also being produced.', 'More and more waste', ['is', 'being produced']),
            ('Will we be able to protect the environment from mountains of plastic?', 'we', ['Will', 'be']),
            ('Octopuses can completely change color.', 'Octopuses', ['can', 'change']),
            ('Will Mina and Joon leave?', 'Mina and Joon', ['Will', 'leave']),
        ]
        for text, subject, verbs in cases:
            clause = {'kind': 'main', 'start': 0, 'subject_spans': span(text, subject),
                      'verb_spans': [span(text, verb)[0] for verb in verbs]}
            with self.subTest(text=text):
                self.assertEqual(module.render_sv(text, [clause]),
                                 f'S: {subject}, V: {" ".join(verbs)}')

    def test_existing_connector_spans_are_not_duplicated(self):
        cases = [
            ('The items are used just once and then discarded.', 'The items', ['are used', 'and', 'discarded']),
            ('Moreover, it only moves the problem to another area and does not really solve it.',
             'it', ['moves', 'and does not', 'solve']),
            ('Some of the most unusual ones have a large, round head and use their eight long arms.',
             'Some of the most unusual ones', ['have', 'and use']),
        ]
        for text, subject, verbs in cases:
            clause = {'kind': 'main', 'start': text.index(subject), 'subject_spans': span(text, subject),
                      'verb_spans': [span(text, verb)[0] for verb in verbs]}
            with self.subTest(text=text):
                self.assertEqual(module.render_sv(text, [clause]),
                                 f'S: {subject}, V: {" ".join(verbs)}')


if __name__ == '__main__':
    unittest.main()
