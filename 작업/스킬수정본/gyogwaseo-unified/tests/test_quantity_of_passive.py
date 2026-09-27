"""Authored quantity/of protection and passive hint contracts, not grammar inference."""
from copy import deepcopy
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent / '../scripts'))
import check_learning_content as m
from structure_hints import display_lines
from test_reading_rule_revision import sentence, cuts, dummy_sentence


def quantity_sentence(phrase='metric tons of'):
    s = sentence('They produce ' + phrase + ' plastic.')
    start = s['text'].index(phrase)
    end = start + len(phrase)
    members = [g for g in s['glosses'] if start <= g['spans'][0][0] < end]
    combined = {'id': 'quantity', 'spans': [[start, end]], 'headword': phrase,
                'meaning_ko': '(미터법) 톤의' if phrase == 'metric tons of' else '어떤 종류의',
                'star': False}
    insert_at = s['glosses'].index(members[0])
    s['glosses'][insert_at:insert_at + len(members)] = [combined]
    for row in s['lexical_coverage']:
        if start <= row['span'][0] < end:
            row['gloss_id'] = 'quantity'
    s['reading_checks'] = {'review_record': 'Synthetic reviewer-declared quantity/kind expression.',
        'required_breaks': [], 'function_gloss_ids': [],
        'protected_spans': [{'span': [start, end], 'kind': 'quantity-kind-of',
                             'gloss_id': 'quantity', 'reason': 'Synthetic reviewed same-order expression.'}]}
    return s


def passive_sentence(past=False):
    s = sentence('They ' + ('were' if past else 'are') + ' produced.')
    function, lexical = s['glosses'][1:3]
    selected = [function['spans'][0][0], lexical['spans'][0][1]]
    english, korean = s['text'][slice(*selected)], '생산되었다' if past else '생산된다'
    function.update(kind='function', headword='be p.p.', meaning_ko='~되다',
                    combines_with=[lexical['id']])
    lexical.update(kind='lexical', headword='produced', meaning_ko='생산된',
                   verb_form={'usage':'passive-participle',
                              'source_span':lexical['spans'][0], 'lemma':'produce',
                              'function_gloss_id':function['id']})
    s['hints'] = [{'category': 'function-combination',
        'span': selected, 'display_mode':'verb-function', 'display_span':selected,
        'formula_label':'be p.p.', 'gloss_ids': [function['id'], lexical['id']], 'meaning_ko': korean,
        'lexical_step': {'gloss_id':lexical['id'], 'form':'produced', 'meaning_ko':'생산된'},
        'explanation': 'Synthetic passive candidate after higher-priority grammar review.',
        'display_pairs': [{'en': english, 'ko': korean,
                           'emphasis_links': [{'en_spans': [[0, english.index(' ')], [len(english)-2,len(english)]],
                                               'ko_spans': [[2, len(korean)]]}]}]}]
    s['reading_checks'] = {'review_record': 'Synthetic review found no higher-priority connection.',
        'required_breaks': [], 'protected_spans': [], 'function_gloss_ids': [function['id']]}
    return s


class QuantityOfPassiveTests(unittest.TestCase):
    def accepted(self, s, required=True):
        before = deepcopy(s)
        result = m.glossary(s, {}, require_reading_checks=required)
        self.assertEqual(s, before, 'Validation must not rewrite source or annotations')
        return result

    def test_quantity_and_kind_are_one_gloss_without_forcing_the_following_noun(self):
        for phrase in ('metric tons of', 'some kind of'):
            with self.subTest(phrase=phrase):
                s = quantity_sentence(phrase)
                protected = s['reading_checks']['protected_spans'][0]['span']
                cuts(s, [protected[0], s['text'].index('plastic')])
                result = self.accepted(s)
                self.assertEqual(result['quantity']['headword'], phrase)
                self.assertTrue(any(g['headword'] == 'plastic' for g in result.values()))

    def test_quantity_protection_rejects_of_and_other_internal_chunk_boundaries(self):
        for part in ('tons', 'of'):
            with self.subTest(part=part):
                s = quantity_sentence(); cuts(s, [s['text'].index(part)])
                with self.assertRaisesRegex(ValueError, 'protected span'):
                    self.accepted(s)

    def test_quantity_gloss_must_exist_and_own_one_exact_contiguous_span(self):
        s = quantity_sentence()
        s['reading_checks']['protected_spans'][0]['gloss_id'] = 'missing'
        with self.assertRaisesRegex(ValueError, 'combined gloss'):
            self.accepted(s)
        for spans in ([[13, 24]], [[13, 19], [20, 27]], [[13, 27], [28, 35]]):
            with self.subTest(spans=spans):
                s = quantity_sentence()
                s['glosses'][2]['spans'] = spans
                with self.assertRaisesRegex(ValueError, 'single protected source span'):
                    m.reading_rules(s, {g['id']: g for g in s['glosses']}, required=True)

    def test_quantity_headword_matches_source_with_only_space_and_case_normalization(self):
        s = quantity_sentence(); s['glosses'][2]['headword'] = ' METRIC  TONS\tof '
        self.accepted(s)
        for head in ('metric tons', 'tons of', 'a kind of', 'metric tons of plastic'):
            with self.subTest(head=head):
                s = quantity_sentence(); s['glosses'][2]['headword'] = head
                with self.assertRaisesRegex(ValueError, 'headword must match'):
                    self.accepted(s)

    def test_quantity_declaration_needs_a_phrase_ending_in_of(self):
        for phrase in ('metric tons', 'of'):
            with self.subTest(phrase=phrase):
                s = quantity_sentence(phrase)
                with self.assertRaisesRegex(ValueError, 'ending in of'):
                    self.accepted(s)

    def test_quantity_cannot_keep_standalone_of_or_other_component_glosses(self):
        for word in ('of', 'metric', 'tons'):
            with self.subTest(word=word):
                s = quantity_sentence(); at = s['text'].index(word)
                s['glosses'].insert(3, {'id': 'duplicate', 'spans': [[at, at + len(word)]],
                    'headword': word, 'meaning_ko': '중복 시험 뜻', 'star': False})
                with self.assertRaisesRegex(ValueError, 'duplicate its component'):
                    self.accepted(s)

    def test_old_of_boundary_is_not_silently_waived_by_the_new_declaration(self):
        s = quantity_sentence()
        s['reading_checks']['required_breaks'] = [{'at': s['text'].index('of'),
            'kind': 'postnominal-preposition', 'reason': 'Synthetic conflicting old classification.'}]
        with self.assertRaisesRegex(ValueError, 'Missing declared postmodifier'):
            self.accepted(s)

    def test_general_of_and_passive_agent_by_keep_their_required_boundaries(self):
        for original, word, kind in [('a career of more than thirty years', 'of', 'postnominal-preposition'),
                                      ('It is produced by workers.', 'by', 'passive-agent-by')]:
            with self.subTest(word=word):
                s = sentence(original); at = original.index(word)
                s['reading_checks'] = {'required_breaks': [{'at': at, 'kind': kind, 'reason': 'Synthetic reviewed relation.'}]}
                with self.assertRaisesRegex(ValueError, 'Missing declared'):
                    self.accepted(s, required=False)
                cuts(s, [at]); self.accepted(s, required=False)

    def test_fixed_expression_and_dummy_it_keep_existing_contracts(self):
        s = sentence('They look for books.')
        s['reading_checks'] = {'protected_spans': [{'span': [5, 13], 'kind': 'fixed-expression',
                                                 'reason': 'Synthetic existing fixed-expression declaration.'}]}
        self.accepted(s, required=False)
        self.accepted(dummy_sentence(), required=False)

    def test_passive_uses_formula_and_actual_participle_with_learning_step(self):
        for past in (False, True):
            with self.subTest(past=past):
                s = passive_sentence(past); self.accepted(s)
                self.assertEqual(display_lines(s['hints'][0]),
                    ['produced(생산된) → ' + ('were' if past else 'are') + ' produced(' +
                     ('생산되었다' if past else '생산된다') + ') (be p.p.)'])
                self.assertEqual(s['glosses'][1]['headword'], 'be p.p.')
                self.assertEqual(s['glosses'][2]['headword'], 'produced')

    def test_passive_combination_does_not_displace_higher_priority_hint(self):
        s = passive_sentence()
        higher = {'span': [0, 4], 'meaning_ko': '시험용 뜻', 'explanation': '시험용 기존 우선 구조'}
        lower = deepcopy(s['hints'][0])
        s['hints'] = [higher, lower]; self.accepted(s, required=False)
        s['hints'] = [lower, higher]
        with self.assertRaisesRegex(ValueError, 'higher-priority'):
            self.accepted(s, required=False)


if __name__ == '__main__':
    unittest.main()
