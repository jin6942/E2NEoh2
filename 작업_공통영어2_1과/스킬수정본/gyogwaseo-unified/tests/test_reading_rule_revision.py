"""Reading-rule contract tests; examples are synthetic, not reviewed book content."""
from copy import deepcopy
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent / '../scripts'))
import check_learning_content as m
from test_learning_content import fixture


def sentence(original):
    glosses, coverage = [], []
    for i, match in enumerate(m.WORDS.finditer(original)):
        gid = f'g{i}'
        gloss = {'id': gid, 'spans': [[match.start(), match.end()]],
                 'headword': match.group(), 'meaning_ko': '시험용 뜻', 'star': False}
        if match.group().lower() in m.PRONOUNS:
            gloss['referent_ko'] = '시험용 실제 지시 대상'
        glosses.append(gloss)
        coverage.append({'span': [match.start(), match.end()], 'gloss_id': gid})
    return {'text': original, 'glosses': glosses, 'lexical_coverage': coverage,
            'chunks': [{'start': 0, 'end': len(original), 'ko': '시험용 대응 해석'}]}


def cuts(s, positions):
    limits = [0] + sorted(positions) + [len(s['text'])]
    s['chunks'] = [{'start': a, 'end': b - (len(s['text'][a:b]) - len(s['text'][a:b].rstrip())),
                    'ko': '시험용 대응 해석'} for a, b in zip(limits, limits[1:])]


def had_sentence():
    s = sentence('They had predicted rain.')
    s['glosses'][1].update(kind='function', headword='had p.p.', meaning_ko='~했다', combines_with=['g2'])
    s['glosses'][2].update(kind='lexical', meaning_ko='예측하다')
    return s


def participle_sentence():
    s = sentence('The letter written in French arrived.')
    lexical = s['glosses'][2]
    lexical.update(kind='lexical', meaning_ko='쓰다 (write의 변화형)')
    function = {'id': 'pp', 'spans': deepcopy(lexical['spans']), 'headword': 'p.p.',
                'meaning_ko': '~된', 'star': False, 'kind': 'function', 'combines_with': ['g2']}
    s['glosses'].insert(2, function)
    return s


def dummy_sentence(verb='seems'):
    original = f'It {verb} that the people in the room are ready.'
    s = sentence(original)
    end = original.index('that') + len('that')
    meanings = {'seems': 'S′(이/가) V′하는 것 같다', 'appears': 'S′(이/가) V′하는 것으로 보인다',
                'is likely': 'S′(이/가) V′할 가능성이 높다'}
    combined = {'id': 'it-that', 'spans': [[0, end]], 'headword': f'It {verb} that S′ V′',
                'meaning_ko': meanings[verb], 'star': False}
    prefix_words = sum(row['span'][1] <= end for row in s['lexical_coverage'])
    s['glosses'][:prefix_words] = [combined]
    for row in s['lexical_coverage'][:prefix_words]:
        row['gloss_id'] = 'it-that'
    s['reading_checks'] = {'protected_spans': [{'span': [0, end], 'kind': 'dummy-it-prefix',
        'reason': '검토자가 확인한 가주어 구문 시작', 'gloss_id': 'it-that'}],
        'required_breaks': [{'at': original.index('in the'), 'kind': 'postnominal-preposition',
        'reason': 'people을 후치수식하는 전치사구'}]}
    cuts(s, [original.index('in the'), original.index('are ready')])
    return s


class ReadingRuleRevisionTests(unittest.TestCase):
    def check(self, s):
        before = deepcopy(s)
        result = m.glossary(s, {})
        self.assertEqual(s, before, 'Validation must not rewrite user annotations')
        return result

    def test_separate_past_perfect_and_lexical_glosses(self):
        result = self.check(had_sentence())
        self.assertEqual(result['g1']['headword'], 'had p.p.')
        self.assertEqual(result['g1']['meaning_ko'], '~했다')
        self.assertEqual(result['g2']['headword'], 'predicted')

    def test_past_perfect_forbidden_extended_meanings(self):
        for meaning in ['~했었다', '그때보다 앞서 ~했다', '그때보다 먼저 ~했다', '~했다 (과거완료)']:
            with self.subTest(meaning=meaning):
                s = had_sentence(); s['glosses'][1]['meaning_ko'] = meaning
                with self.assertRaisesRegex(ValueError, 'exactly ~했다'):
                    self.check(s)

    def test_explicit_function_lexical_pair_may_share_participle_span(self):
        self.assertEqual(len(self.check(participle_sentence())), 7)

    def test_untyped_duplicate_is_still_rejected(self):
        s = participle_sentence(); s['glosses'][2].pop('kind'); s['glosses'][2].pop('combines_with')
        with self.assertRaisesRegex(ValueError, 'explicitly linked'):
            self.check(s)

    def test_equal_span_pair_needs_link_to_that_lexical_gloss(self):
        s = participle_sentence(); s['glosses'][2]['combines_with'] = ['g3']
        s['glosses'][4]['kind'] = 'lexical'
        with self.assertRaisesRegex(ValueError, 'explicitly linked'):
            self.check(s)

    def test_three_identical_spans_are_not_a_blanket_exception(self):
        s = participle_sentence(); extra = deepcopy(s['glosses'][2]); extra['id'] = 'extra-function'
        s['glosses'].insert(3, extra)
        with self.assertRaisesRegex(ValueError, 'Duplicate gloss'):
            self.check(s)

    def test_same_position_function_must_come_first(self):
        s = participle_sentence(); s['glosses'][2:4] = s['glosses'][2:4][::-1]
        with self.assertRaisesRegex(ValueError, 'must precede'):
            self.check(s)

    def test_function_needs_existing_lexical_link(self):
        for target in ['missing', 'g0', 'g1']:
            s = had_sentence(); s['glosses'][1]['combines_with'] = [target]
            with self.subTest(target=target), self.assertRaisesRegex(ValueError, 'lexical gloss'):
                self.check(s)

    def test_lexical_gloss_cannot_claim_function_link(self):
        s = had_sentence(); s['glosses'][2]['combines_with'] = ['g1']
        with self.assertRaisesRegex(ValueError, 'Only function'):
            self.check(s)

    def test_participle_coverage_must_link_to_lexical_not_function(self):
        s = participle_sentence(); s['lexical_coverage'][2]['gloss_id'] = 'pp'
        with self.assertRaisesRegex(ValueError, 'lexical coverage must point'):
            self.check(s)

    def test_nested_function_and_word_coverage_stays_distinct(self):
        s = had_sentence(); s['glosses'][1]['spans'] = [[5, 18]]
        self.check(s)
        s['lexical_coverage'][2]['gloss_id'] = 'g1'
        with self.assertRaisesRegex(ValueError, 'lexical coverage must point'):
            self.check(s)

    def test_all_function_families_can_be_independent(self):
        # Validate representation, not the grammatical classification of a sentence.
        examples = [('to preserve', 'to V', '~하기 위해', 'preserve', '보존하다'),
                    ('is reading', 'be V-ing', '~하고 있다', 'reading', '읽다'),
                    ('was predicted', 'was p.p.', '~되었다', 'predicted', '예측하다'),
                    ('can swim', 'can V', '~할 수 있다', 'swim', '수영하다'),
                    ('could not solve', 'could not V', '~할 수 없었다', 'solve', '풀다')]
        for original, formula, meaning, word, lexical_meaning in examples:
            with self.subTest(formula=formula):
                s = sentence(original); at = original.index(word)
                function = {'id': 'function', 'kind': 'function', 'spans': [[0, at - 1]],
                            'headword': formula, 'meaning_ko': meaning, 'star': False, 'combines_with': ['word']}
                lexical = {'id': 'word', 'kind': 'lexical', 'spans': [[at, len(original)]],
                           'headword': word, 'meaning_ko': lexical_meaning, 'star': False}
                s['glosses'] = [function, lexical]
                for row in s['lexical_coverage']:
                    row['gloss_id'] = 'function' if row['span'][0] < at else 'word'
                self.check(s)

    def test_nested_functions_stay_separate_and_share_one_lexical_target(self):
        s = sentence('to be invited')
        s['glosses'][0].update(kind='function', headword='to V', meaning_ko='~하기를', combines_with=['g2'])
        s['glosses'][1].update(kind='function', headword='be p.p.', meaning_ko='~받다', combines_with=['g2'])
        s['glosses'][2].update(kind='lexical', meaning_ko='초대하다')
        self.check(s)

    def test_ing_function_and_lexical_meaning_share_one_word_without_merging(self):
        s = sentence('Reading helps.')
        s['glosses'][0].update(kind='lexical', meaning_ko='읽다')
        s['glosses'].insert(0, {'id': 'ing', 'kind': 'function', 'spans': [[0, 7]],
            'headword': 'V-ing', 'meaning_ko': '~하는 것', 'star': False, 'combines_with': ['g0']})
        self.check(s)

    def test_postmodifier_boundaries_are_required(self):
        for original, phrase, kind in [('a book full of pictures', 'full', 'postpositive-adjective'),
                                       ('the people in the room', 'in', 'postnominal-preposition')]:
            with self.subTest(kind=kind):
                s = sentence(original); at = original.index(phrase)
                s['reading_checks'] = {'required_breaks': [{'at': at, 'kind': kind, 'reason': '명사 후치수식 확인'}]}
                with self.assertRaisesRegex(ValueError, 'Missing declared'):
                    self.check(s)
                cuts(s, [at]); self.check(s)

    def test_passive_agent_by_boundary_cannot_be_merged(self):
        s = sentence('It is not controlled solely by its brain.')
        at = s['text'].index('by')
        s['reading_checks'] = {'required_breaks': [{'at': at, 'kind': 'passive-agent-by',
            'reason': '수동태에서 통제 주체를 나타내는 by 구'}]}
        with self.assertRaisesRegex(ValueError, 'Missing declared passive-agent'):
            self.check(s)
        cuts(s, [at]); self.check(s)

    def test_passive_agent_boundary_requires_actual_by_word(self):
        for original, at in [('It is made with clay.', 11), ('A nearby tree stands.', 6)]:
            with self.subTest(original=original):
                s = sentence(original); cuts(s, [at])
                s['reading_checks'] = {'required_breaks': [{'at': at, 'kind': 'passive-agent-by',
                    'reason': '위치 오지정 시험'}]}
                with self.assertRaisesRegex(ValueError, 'must start source by'):
                    m.reading_rules(s, {})

    def test_other_by_uses_are_not_inferred_as_passive_agents(self):
        for original in ['They learn by doing.', 'She stands by the door.']:
            with self.subTest(original=original):
                s = sentence(original)
                s['reading_checks'] = {'required_breaks': []}
                self.check(s)

    def test_adjective_complement_is_not_another_postmodifier_boundary(self):
        s = sentence('a book full of pictures'); start = s['text'].index('full'); at = s['text'].index('of')
        s['reading_checks'] = {'required_breaks': [{'at': start, 'kind': 'postpositive-adjective', 'reason': 'book 수식'}],
            'protected_spans': [{'span': [start, len(s['text'])], 'kind': 'adjective-complement', 'reason': 'full의 보충어'}]}
        cuts(s, [start]); self.check(s)
        cuts(s, [start, at])
        with self.assertRaisesRegex(ValueError, 'protected span'):
            self.check(s)

    def test_fixed_expression_is_not_split(self):
        s = sentence('They look for books.'); a = s['text'].index('look'); b = s['text'].index('for') + 3
        s['reading_checks'] = {'protected_spans': [{'span': [a, b], 'kind': 'fixed-expression', 'reason': 'look for 숙어'}]}
        self.check(s); cuts(s, [s['text'].index('for')])
        with self.assertRaisesRegex(ValueError, 'protected span'):
            self.check(s)

    def test_dummy_it_template_unified_with_internal_postmodifier_break(self):
        for verb in ['seems', 'appears', 'is likely']:
            with self.subTest(verb=verb):
                self.check(dummy_sentence(verb))

    def test_dummy_it_prefix_cannot_break_before_that(self):
        s = dummy_sentence(); cuts(s, [s['text'].index('that'), s['text'].index('in the')])
        with self.assertRaisesRegex(ValueError, 'protected span'):
            self.check(s)

    def test_dummy_it_gloss_cannot_be_only_it(self):
        s = dummy_sentence(); s['glosses'][0]['headword'] = 'It'
        with self.assertRaisesRegex(ValueError, 'full It .* that'):
            self.check(s)

    def test_dummy_it_declared_source_prefix_must_reach_that(self):
        s = dummy_sentence('is likely'); s['reading_checks']['protected_spans'][0]['span'] = [0, 2]
        with self.assertRaisesRegex(ValueError, 'source It through that'):
            self.check(s)

    def test_separate_that_gloss_cannot_duplicate_template(self):
        s = dummy_sentence(); a = s['text'].index('that')
        s['glosses'].insert(1, {'id': 'extra-that', 'spans': [[a, a + 4]], 'headword': 'that S′ V′',
                               'meaning_ko': 'S′가 V′라고', 'star': False})
        with self.assertRaisesRegex(ValueError, 'Separate It/that'):
            self.check(s)

    def test_combination_hint_connects_source_glosses(self):
        s = had_sentence(); s['hints'] = [{'span': [5, 18], 'category': 'function-combination',
            'gloss_ids': ['g1', 'g2'], 'meaning_ko': '예측했다', 'explanation': 'had + p.p.의 기능과 predict의 뜻을 결합한 동사구'}]
        self.check(s)
        s['hints'][0]['span'] = [5, 8]
        with self.assertRaisesRegex(ValueError, 'cover its linked'):
            self.check(s)

    def test_combination_hint_is_lower_priority(self):
        s = had_sentence(); higher = {'span': [0, 4], 'meaning_ko': '시험용 뜻', 'explanation': '시험용 우선 구조'}
        lower = {'span': [5, 18], 'category': 'function-combination', 'gloss_ids': ['g1', 'g2'],
                 'meaning_ko': '예측했다', 'explanation': '기능과 낱말을 연결한 동사구'}
        s['hints'] = [higher, lower]; self.check(s)
        s['hints'] = [lower, higher]
        with self.assertRaisesRegex(ValueError, 'higher-priority'):
            self.check(s)

    def test_paired_structure_precedes_function_combination_without_new_priority_rules(self):
        s = sentence('They had predicted both rain and snow.')
        s['glosses'][1].update(kind='function', headword='had p.p.', meaning_ko='~했다', combines_with=['g2'])
        s['glosses'][2].update(kind='lexical', meaning_ko='예측하다')
        parts = ['both rain', 'and snow']
        ranges = [[s['text'].index(p), s['text'].index(p)+len(p)] for p in parts]
        paired = {'category': 'paired-structure', 'span': [ranges[0][0], ranges[-1][1]],
            'meaning_ko': '비와 눈 둘 다', 'explanation': '시험용 상관구문 근거',
            'display_spans': ranges, 'display_pairs': [{'en': ' … '.join(parts), 'ko': '비도 … 눈도'}]}
        function = {'category': 'function-combination', 'span': [5, 18], 'gloss_ids': ['g1', 'g2'],
            'meaning_ko': '예측했다', 'explanation': '시험용 기능 결합 근거',
            'display_pairs': [{'en': 'had p.p + predicted', 'ko': '예측했다'}]}
        s['hints'] = [paired, function]; self.check(s)
        s['hints'] = [function, paired]
        with self.assertRaisesRegex(ValueError, 'higher-priority'):
            self.check(s)

    def test_combination_hint_does_not_increase_two_hint_limit(self):
        s = had_sentence(); s['hints'] = [{'span': [0, 4], 'meaning_ko': '뜻', 'explanation': '설명'}] * 3
        with self.assertRaisesRegex(ValueError, 'At most two'):
            self.check(s)

    def test_legacy_data_stays_readable_without_semantic_pass_claim(self):
        data = fixture(); data.pop('rule_revision', None)
        for row in data['sentences']:
            row.pop('reading_checks', None)
        before = deepcopy(data); result = m.check(data)
        self.assertEqual(data, before)
        self.assertEqual(result['status'], 'STRUCTURE_PASS')
        self.assertEqual(result['semantic_review'], 'NOT_PERFORMED')
        self.assertEqual(result['reading_rule_declarations'], 'SUPPLIED_CONSTRAINTS_ONLY_NOT_GRAMMAR_INFERENCE')
        self.assertEqual(result['reading_revision_audit'], 'NOT_REQUESTED_LEGACY_INPUT')

    def test_new_revision_cannot_silently_omit_reading_declarations(self):
        data = fixture(); data['rule_revision'] = m.READING_RULE_REVISION
        for row in data['sentences']:
            row.pop('reading_checks', None)
        with self.assertRaisesRegex(ValueError, 'reading_checks'):
            m.check(data)
        for row in data['sentences']:
            row['reading_checks'] = {'review_record': 'Synthetic no-target-structure review',
                'required_breaks': [], 'protected_spans': [], 'function_gloss_ids': []}
        result = m.check(data)
        self.assertEqual(result['reading_revision_audit'], 'DECLARATIONS_REQUIRED')
        self.assertEqual(result['semantic_review'], 'NOT_PERFORMED')

    def test_new_revision_requires_explicit_empty_lists_and_review_record(self):
        s = had_sentence(); s['reading_checks'] = {'review_record': 'Synthetic reviewed example',
            'required_breaks': [], 'protected_spans': [], 'function_gloss_ids': ['g1']}
        m.glossary(s, {}, require_reading_checks=True)
        for field in list(s['reading_checks']):
            with self.subTest(field=field):
                broken = deepcopy(s); del broken['reading_checks'][field]
                with self.assertRaises(ValueError):
                    m.glossary(broken, {}, require_reading_checks=True)

    def test_reviewed_function_list_cannot_omit_declared_function(self):
        s = had_sentence(); s['reading_checks'] = {'function_gloss_ids': []}
        with self.assertRaisesRegex(ValueError, 'match all declared function'):
            self.check(s)


if __name__ == '__main__':
    unittest.main()
