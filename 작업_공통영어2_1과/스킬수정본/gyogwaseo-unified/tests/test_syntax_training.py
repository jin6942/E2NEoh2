"""Source-bound syntax practice and complete formula routes, not meaning QA."""
from copy import deepcopy
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent / '../scripts'))
import syntax_training as m
import check_learning_content as learning
from test_learning_content import fixture
from test_formula_training_gloss import training_sentence


def selected(text, value):
    start = text.index(value)
    return [start, start + len(value)]


def point(sentence, pid, formula, practice, supports, answer='시험용 정답'):
    return {'id': pid, 'sentence_id': sentence['id'],
            'span': [0, len(sentence['text'])], 'title': '시험용 구문',
            'explanation': '명시된 공식과 낱말 결합의 시험용 설명', 'formula_key': formula,
            'practice': {'span': selected(sentence['text'], practice),
                         'formula_support': {'en': formula, 'ko': '시험용 공식 뜻'},
                         'support_gloss_ids': supports, 'answer_ko': answer}}


def route(sentence_id, function_id, formula, *, hint=None, analysis=None):
    result = {'sentence_id': sentence_id, 'function_gloss_id': function_id,
              'formula_key': formula, 'route': 'hint' if hint is not None else 'analysis',
              'review_record': 'Synthetic declared selection, not a linguistic review.'}
    result['hint_index' if hint is not None else 'grammar_point_id'] = hint if hint is not None else analysis
    return result


def full_fixture():
    original = 'Plastic is produced.'
    data = fixture([original, 'We save valuable materials.', 'I protect local resources.'])
    training = training_sentence(original, 'is produced', 'produced', 'produce',
                                 'be p.p.', '~되다', '생산된', '생산된다', passive=True)
    data['sentences'][0].update(training)
    data['sentences'][0]['hints'] = []
    data['sentences'][0]['clauses'][0]['verb_spans'] = [selected(original, 'is produced')]
    data['metadata']['syntax_training_version'] = 1
    unit = data['units'][0]
    unit['today_words'] = []
    s1, s2, s3 = data['sentences']
    points = [point(s1, 'p1', '명사 주어', 'Plastic', ['g0']),
              point(s2, 'p2', '일반동사 현재형', 'save valuable materials', ['g2-1']),
              point(s3, 'p3', '일반동사 목적어', 'protect local resources', ['g3-1'])]
    supplemental = point(s1, 'p4', 'be p.p.', 'is produced', ['word'], '생산된다')
    supplemental['practice']['formula_support']['ko'] = '~되다'
    supplemental['supplemental'] = {'function_gloss_id': 'formula',
                                    'reason': 'No selected function hint or base point for this formula.'}
    points.append(supplemental)
    unit['analysis']['grammar_points'] = points
    unit['analysis']['formula_routes'] = [route('s1', 'formula', 'be p.p.', analysis='p4')]
    unit['workbook']['syntax_point_ids'] = [p['id'] for p in points]
    return data


def exception_fixture():
    """Declared partial negative with an approved positive replacement.

    This fixture tests links and source boundaries, not whether an approval or
    semantic review actually occurred in a production project.
    """
    data = full_fixture()
    s1, s2, s3 = data['sentences']
    s1.update(text='It is not controlled solely by its brain.', hints=[], glosses=[
        {'id': 'negative', 'kind': 'function', 'headword': 'be not p.p.', 'meaning_ko': '~되지 않다',
         'spans': [[3, 20]], 'combines_with': ['controlled']},
        {'id': 'controlled', 'headword': 'controlled', 'meaning_ko': '통제된', 'spans': [[10, 20]]}])
    s2.update(text='They are located here.', hints=[
        {'category': 'function-combination', 'gloss_ids': ['positive', 'located']}], glosses=[
        {'id': 'positive', 'kind': 'function', 'headword': 'be p.p.', 'meaning_ko': '~되다',
         'spans': [[5, 16]], 'combines_with': ['located']},
        {'id': 'located', 'headword': 'located', 'meaning_ko': '위치한', 'spans': [[9, 16]]},
        {'id': 'they', 'headword': 'They', 'meaning_ko': '그것들은', 'spans': [[0, 4]]}])
    points = [point(s1, 'p1', 'not … solely', 'is not controlled solely by its brain',
                    ['controlled'], '오로지 그것의 뇌에 의해서만 통제되는 것은 아니다'),
              point(s2, 'p2', '명사 주어', 'They', ['they']),
              point(s3, 'p3', '일반동사 목적어', 'protect local resources', ['g3-1']),
              point(s2, 'p4', 'be p.p.', 'are located', ['located'], '위치한다')]
    points[-1]['supplemental'] = {'function_gloss_id': 'positive',
                                 'reason': 'Approved positive replacement for a partial-negative sentence.'}
    unit = data['units'][0]
    unit['analysis']['grammar_points'] = points
    unit['analysis']['formula_routes'] = [
        {'sentence_id': 's1', 'function_gloss_id': 'negative', 'formula_key': 'be not p.p.',
         'route': 'approved-exception', 'exception_kind': 'partial-negation',
         'grammar_point_id': 'p1', 'replacement_grammar_point_id': 'p4',
         'partial_negation_span': selected(s1['text'], 'is not controlled solely'),
         'approval_reference': 'synthetic-test-approval',
         'review_record': 'Synthetic source-bound partial-negation declaration.'},
        route('s2', 'positive', 'be p.p.', hint=0)]
    unit['workbook']['syntax_point_ids'] = [p['id'] for p in points]
    return data


class SyntaxTrainingTests(unittest.TestCase):
    def check(self, data, scope='full'):
        before = deepcopy(data)
        version = m.training_version(data)
        result = m.check_unit(data['units'][0], data['sentences'], version, scope)
        self.assertEqual(data, before)
        return result

    def test_full_checker_keeps_three_base_points_and_accepts_one_linked_supplement(self):
        data = full_fixture(); before = deepcopy(data)
        result = learning.check(data)
        self.assertEqual(result['status'], 'STRUCTURE_PASS')
        report = result['syntax_training']['units'][0]
        self.assertEqual(report['base_grammar_point_count'], 3)
        self.assertEqual(report['supplemental_count'], 1)
        self.assertEqual(report['practice_count'], 4)
        self.assertEqual(data, before)

    def test_legacy_without_version_preserves_old_content_and_reports_unchecked_training(self):
        data = fixture(); before = deepcopy(data)
        self.assertIsNone(m.training_version(data))
        self.assertEqual(learning.check(data)['syntax_training']['status'], 'UNDECLARED_LEGACY_INPUT')
        self.assertEqual(data, before)

    def test_partial_contract_and_wrong_version_are_rejected(self):
        for mutate in [lambda d: d['metadata'].pop('syntax_training_version'),
                       lambda d: d['metadata'].update(syntax_training_version=True),
                       lambda d: d['metadata'].update(syntax_training_version=2)]:
            data = full_fixture(); mutate(data)
            with self.subTest(mutate=mutate), self.assertRaisesRegex(ValueError, 'syntax_training_version'):
                m.training_version(data)
        for field in ['formula_routes', 'syntax_point_ids', 'practice', 'supplemental']:
            data = fixture()
            if field == 'formula_routes': data['units'][0]['analysis'][field] = []
            elif field == 'syntax_point_ids': data['units'][0]['workbook'][field] = []
            else: data['units'][0]['analysis']['grammar_points'][0][field] = {}
            with self.subTest(field=field), self.assertRaisesRegex(ValueError, 'partial contract'):
                m.training_version(data)

    def test_canonical_keys_do_not_merge_tense_modal_negative_or_passive(self):
        self.assertEqual(m.canonical_formula_key('  BE   pp  '), 'be p.p.')
        self.assertEqual(m.canonical_formula_key('have p.p'), 'have p.p.')
        forms = ['have p.p.', 'had p.p.', 'have not p.p.', 'have been p.p.', 'may have p.p.']
        self.assertEqual(len({m.canonical_formula_key(x) for x in forms}), len(forms))
        self.assertEqual(m.authored_formula_kind('be not p.p.'), 'passive')
        self.assertEqual(m.authored_formula_kind('have been p.p.'), 'passive')
        self.assertEqual(m.authored_formula_kind('may have p.p.'), 'active-perfect')
        self.assertIsNone(m.authored_formula_kind('have been V-ing'))
        self.assertIsNone(m.authored_formula_kind('The plastic is produced.'))

    def test_base_point_count_cannot_be_hidden_by_unlinked_supplement(self):
        data = full_fixture()
        data['units'][0]['analysis']['grammar_points'][-1].pop('supplemental')
        with self.assertRaisesRegex(ValueError, 'exceeds the confirmed default'):
            learning.check(data)
        data = full_fixture()
        data['units'][0]['analysis']['grammar_points'][0]['supplemental'] = {
            'function_gloss_id': 'formula', 'reason': 'False supplemental marker'}
        with self.assertRaisesRegex(ValueError, 'own actual function'):
            self.check(data)

    def test_every_point_needs_id_practice_formula_and_answer(self):
        changes = [lambda p: p.pop('id'), lambda p: p.update(id='p2'),
                   lambda p: p.pop('practice'), lambda p: p['practice'].pop('formula_support'),
                   lambda p: p['practice']['formula_support'].update(en='another formula'),
                   lambda p: p['practice']['formula_support'].update(ko=' '),
                   lambda p: p['practice'].update(answer_ko='')]
        for mutate in changes:
            data = full_fixture(); mutate(data['units'][0]['analysis']['grammar_points'][0])
            with self.subTest(mutate=mutate), self.assertRaises(ValueError):
                self.check(data)

    def test_practice_span_must_preserve_words_and_stay_inside_analysis_evidence(self):
        for value in [[8, 18], [0, 500], [8, 8], [False, 7]]:
            data = full_fixture()
            data['units'][0]['analysis']['grammar_points'][-1]['practice']['span'] = value
            with self.subTest(value=value), self.assertRaises(ValueError): self.check(data)
        data = full_fixture()
        data['units'][0]['analysis']['grammar_points'][-1]['span'] = selected('Plastic is produced.', 'produced')
        with self.assertRaisesRegex(ValueError, 'inside the grammar evidence'): self.check(data)

    def test_support_must_be_unique_actual_lexical_from_practice_sentence(self):
        for ids in [[], ['word', 'word'], ['g2-1'], ['formula'], ['missing'], ['g0']]:
            data = full_fixture()
            data['units'][0]['analysis']['grammar_points'][-1]['practice']['support_gloss_ids'] = ids
            with self.subTest(ids=ids), self.assertRaises(ValueError): self.check(data)

    def test_formula_support_is_not_repeated_as_lexical_support(self):
        data = full_fixture()
        p = data['units'][0]['analysis']['grammar_points'][0]
        p['formula_key'] = p['practice']['formula_support']['en'] = 'Plastic'
        with self.assertRaisesRegex(ValueError, 'must not repeat'): self.check(data)

    def test_workbook_must_cover_every_base_and_supplement_in_order(self):
        for ids in [[], ['p1', 'p2', 'p3'], ['p1', 'p2', 'p3', 'p3'], ['p4', 'p1', 'p2', 'p3']]:
            data = full_fixture(); data['units'][0]['workbook']['syntax_point_ids'] = ids
            with self.subTest(ids=ids), self.assertRaisesRegex(ValueError, 'exactly once'): self.check(data)

    def test_learning_scope_checks_routes_and_practice_but_does_not_require_workbook(self):
        data = full_fixture(); data['units'][0]['workbook'].pop('syntax_point_ids')
        self.assertEqual(learning.check(data, 'learning')['syntax_training']['units'][0]['workbook_links'],
                         'NOT_CHECKED_LEARNING_SCOPE')
        data['units'][0]['analysis']['formula_routes'] = []
        with self.assertRaisesRegex(ValueError, 'exactly one route'):
            learning.check(data, 'learning')

    def test_missing_duplicate_unknown_and_mismatched_formula_routes_fail(self):
        changes = [lambda a: a.pop('formula_routes'), lambda a: a.update(formula_routes=[]),
                   lambda a: a['formula_routes'].append(deepcopy(a['formula_routes'][0])),
                   lambda a: a['formula_routes'][0].update(sentence_id='s3'),
                   lambda a: a['formula_routes'][0].update(formula_key='have p.p.'),
                   lambda a: a['formula_routes'][0].update(review_record=' ')]
        for mutate in changes:
            data = full_fixture(); mutate(data['units'][0]['analysis'])
            with self.subTest(mutate=mutate), self.assertRaises(ValueError): self.check(data)

    def test_hint_route_requires_actual_same_sentence_function_combination(self):
        data = full_fixture()
        data['sentences'][0]['hints'] = [{'category': 'function-combination', 'gloss_ids': ['formula', 'word']}]
        unit = data['units'][0]
        unit['analysis']['grammar_points'].pop()
        unit['workbook']['syntax_point_ids'].pop()
        unit['analysis']['formula_routes'] = [route('s1', 'formula', 'be p.p.', hint=0)]
        self.assertEqual(self.check(data)['supplemental_count'], 0)
        for mutate in [lambda d: d['sentences'][0]['hints'][0].update(category='paired-structure'),
                       lambda d: d['sentences'][0]['hints'][0].update(gloss_ids=['word']),
                       lambda d: d['units'][0]['analysis']['formula_routes'][0].update(hint_index=True)]:
            changed = deepcopy(data); mutate(changed)
            with self.subTest(mutate=mutate), self.assertRaisesRegex(ValueError, 'same sentence'):
                self.check(changed)

    def test_existing_function_hint_is_not_rerouted_to_redundant_analysis(self):
        data = full_fixture()
        data['sentences'][0]['hints'] = [{'category': 'function-combination', 'gloss_ids': ['formula', 'word']}]
        with self.assertRaisesRegex(ValueError, 'routed as hint'): self.check(data)

    def test_other_sentence_can_share_one_analysis_representative_of_same_formula(self):
        data = full_fixture(); repeated = deepcopy(data['sentences'][0]); repeated['id'] = 's2'
        data['sentences'][1] = repeated
        p = data['units'][0]['analysis']['grammar_points'][1]
        p['span'] = [0, len(repeated['text'])]
        p['practice']['span'] = selected(repeated['text'], 'Plastic')
        p['practice']['support_gloss_ids'] = ['g0']
        data['units'][0]['analysis']['formula_routes'].append(route('s2', 'formula', 'be p.p.', analysis='p4'))
        result = self.check(data)
        self.assertEqual(result['formula_occurrence_count'], 2)
        self.assertEqual(result['supplemental_count'], 1)

    def test_supplement_cannot_duplicate_base_formula_or_name_another_sentences_function(self):
        data = full_fixture()
        point0 = data['units'][0]['analysis']['grammar_points'][0]
        point0['formula_key'] = point0['practice']['formula_support']['en'] = 'be p.p.'
        with self.assertRaisesRegex(ValueError, 'do not repeat'): self.check(data)
        data = full_fixture()
        data['units'][0]['analysis']['grammar_points'][-1]['supplemental']['function_gloss_id'] = 'missing'
        with self.assertRaisesRegex(ValueError, 'own actual function'): self.check(data)

    def test_analysis_route_requires_representative_source_formula_and_lexical_support(self):
        data = full_fixture()
        p = data['units'][0]['analysis']['grammar_points'][-1]
        p.pop('supplemental')
        p['practice']['span'] = selected('Plastic is produced.', 'produced')
        with self.assertRaisesRegex(ValueError, 'same actual formula'): self.check(data)

    def test_unreviewed_english_is_not_regex_parsed_into_formula_routes(self):
        data = full_fixture()
        data['sentences'][0]['glosses'] = [g for g in data['sentences'][0]['glosses'] if g['id'] != 'formula']
        unit = data['units'][0]
        unit['analysis']['grammar_points'].pop(); unit['workbook']['syntax_point_ids'].pop()
        unit['analysis']['formula_routes'] = []
        self.assertEqual(self.check(data)['formula_occurrence_count'], 0)

    def test_support_override_only_uses_reviewed_construction_lemma_and_keeps_gloss(self):
        data = full_fixture()
        actual = 'They may have provided us with food.'
        frame = training_sentence(actual, 'may have provided', 'provided', 'provide',
                                  'may have p.p.', '~했을지도 모른다', '제공하다', '제공했을지도 모른다',
                                  frame='provide A with B', connector='with')
        frame['hints'] = []
        data['sentences'][0].update(frame)
        base = data['units'][0]['analysis']['grammar_points'][0]
        base['span'] = [0, len(actual)]
        base['practice']['span'] = selected(actual, 'They')
        supplement = data['units'][0]['analysis']['grammar_points'][-1]
        supplement['span'] = [0, len(actual)]
        supplement['formula_key'] = 'may have p.p.'
        supplement['practice']['span'] = selected(actual, 'may have provided')
        supplement['practice']['formula_support']['en'] = 'may have p.p.'
        data['units'][0]['analysis']['formula_routes'][0]['formula_key'] = 'may have p.p.'
        gloss = next(g for g in data['sentences'][0]['glosses'] if g['id'] == 'word')
        p = data['units'][0]['analysis']['grammar_points'][-1]['practice']
        p['support_overrides'] = [{'gloss_id': 'word', 'form': 'provide', 'meaning_ko': '제공하다',
                                  'review_record': 'Synthetic short lexical support decision.'}]
        before = deepcopy(gloss); self.check(data); self.assertEqual(gloss, before)
        for mutate in [lambda d: next(g for g in d['sentences'][0]['glosses'] if g['id'] == 'word').pop('verb_construction'),
                       lambda d: d['units'][0]['analysis']['grammar_points'][-1]['practice']['support_overrides'][0].update(form='produce'),
                       lambda d: d['units'][0]['analysis']['grammar_points'][-1]['practice']['support_overrides'][0].update(review_record=''),
                       lambda d: d['units'][0]['analysis']['grammar_points'][-1]['practice']['support_overrides'].append(deepcopy(p['support_overrides'][0]))]:
            changed = deepcopy(data); mutate(changed)
            with self.subTest(mutate=mutate), self.assertRaises(ValueError): self.check(changed)

    def test_source_projection_preserves_actual_word_inside_combined_gloss(self):
        data = full_fixture()
        s = data['sentences'][1]
        s['text'] = 'He is a contributor to the damage.'
        a, b = selected(s['text'], 'contributor to')
        s['glosses'] = [{'id': 'combined', 'headword': 'contributor to', 'meaning_ko': '~의 원인 제공자',
                        'spans': [[a, b]]}]
        p = data['units'][0]['analysis']['grammar_points'][1]
        p['span'] = [0, len(s['text'])]
        p['practice']['span'] = selected(s['text'], 'He is a contributor')
        p['practice']['support_gloss_ids'] = ['combined']
        override = {'gloss_id': 'combined', 'source_span': selected(s['text'], 'contributor'),
                    'form': 'contributor', 'meaning_ko': '원인 제공자', 'review_record': 'Only this source noun is practiced.'}
        p['practice']['support_overrides'] = [override]
        before = deepcopy(s['glosses']); self.check(data); self.assertEqual(s['glosses'], before)
        for changes in [{'form': 'contribute'}, {'source_span': [a, b]},
                        {'source_span': [a, a + 10]}, {'source_span': [0, 2]},
                        {'meaning_ko': ''}, {'review_record': ''}, {'gloss_id': 'unknown'}]:
            changed = deepcopy(data)
            changed['units'][0]['analysis']['grammar_points'][1]['practice']['support_overrides'][0].update(changes)
            with self.subTest(changes=changes), self.assertRaises(ValueError): self.check(changed)

    def test_ancillary_function_support_is_allowed_with_a_lexical_support(self):
        data = full_fixture()
        sentence = data['sentences'][1]
        sentence.update(text='We can save valuable materials.', glosses=[
            {'id': 'can', 'kind': 'function', 'headword': 'can V', 'meaning_ko': '~할 수 있다',
             'spans': [[3, 6]]},
            {'id': 'save', 'headword': 'save', 'meaning_ko': '절약하다', 'spans': [[7, 11]]}])
        practice_point = data['units'][0]['analysis']['grammar_points'][1]
        practice_point.update(point(sentence, 'p2', '(that) S′ V′', 'We can save', ['can', 'save']))
        self.check(data)
        practice_point['practice']['support_gloss_ids'] = ['can']
        with self.assertRaisesRegex(ValueError, 'at least one lexical'): self.check(data)
        practice_point['practice']['support_gloss_ids'] = ['can', 'save']
        practice_point['formula_key'] = practice_point['practice']['formula_support']['en'] = 'can V'
        with self.assertRaisesRegex(ValueError, 'must not repeat'): self.check(data)

    def test_ancillary_function_support_cannot_be_overridden_as_a_lexical_word(self):
        data = full_fixture()
        practice = data['units'][0]['analysis']['grammar_points'][-1]['practice']
        practice['support_gloss_ids'].append('formula')
        practice['support_overrides'] = [{'gloss_id': 'formula', 'source_span': [8, 10],
            'form': 'is', 'meaning_ko': '이다', 'review_record': 'Invalid function-to-word projection.'}]
        with self.assertRaisesRegex(ValueError, 'actual lexical support'): self.check(data)

    def test_approved_partial_negative_routes_to_distinct_positive_replacement(self):
        result = self.check(exception_fixture())
        self.assertEqual(result['base_grammar_point_count'], 3)
        self.assertEqual(result['supplemental_count'], 1)
        self.assertEqual(result['formula_occurrence_count'], 2)
        self.assertEqual(result['practice_count'], 4)

    def test_partial_negative_exception_requires_explicit_approval_and_supported_kind(self):
        for change in [{'approval_reference': ''}, {'approval_reference': None},
                       {'exception_kind': 'hard-sentence'}, {'review_record': ''}]:
            data = exception_fixture()
            data['units'][0]['analysis']['formula_routes'][0].update(change)
            with self.subTest(change=change), self.assertRaises(ValueError): self.check(data)
        data = exception_fixture()
        data['units'][0]['analysis']['formula_routes'][0].pop('approval_reference')
        with self.assertRaisesRegex(ValueError, 'approval_reference'): self.check(data)

    def test_exception_requires_own_point_and_another_sentence_in_same_unit(self):
        for change in [{'grammar_point_id': 'p2'}, {'grammar_point_id': 'missing'},
                       {'replacement_grammar_point_id': 'p1'}, {'replacement_grammar_point_id': 'other-unit-point'}]:
            data = exception_fixture()
            data['units'][0]['analysis']['formula_routes'][0].update(change)
            with self.subTest(change=change), self.assertRaisesRegex(ValueError, 'different-sentence replacement'):
                self.check(data)

    def test_partial_negative_evidence_must_cover_function_and_fit_practice(self):
        for value in [[10, 20], [0, 30], [3, 22], [3, 500], [3, 3], None]:
            data = exception_fixture()
            data['units'][0]['analysis']['formula_routes'][0]['partial_negation_span'] = value
            with self.subTest(value=value), self.assertRaises(ValueError): self.check(data)

    def test_positive_or_active_perfect_cannot_use_partial_negative_exception(self):
        for formula in ['be p.p.', 'have not p.p.']:
            data = exception_fixture()
            data['sentences'][0]['glosses'][0]['headword'] = formula
            data['units'][0]['analysis']['formula_routes'][0]['formula_key'] = formula
            with self.subTest(formula=formula), self.assertRaisesRegex(ValueError, 'negative passive'):
                self.check(data)
        data = exception_fixture()
        data['sentences'][0]['hints'] = [{'category': 'function-combination',
                                        'gloss_ids': ['negative', 'controlled']}]
        with self.assertRaisesRegex(ValueError, 'unselected negative passive'): self.check(data)

    def test_replacement_rejects_negative_modal_and_perfect_formulas(self):
        for formula in ['be not p.p.', 'can be p.p.', 'have p.p.', 'have been p.p.']:
            data = exception_fixture()
            data['sentences'][1]['glosses'][0]['headword'] = formula
            unit = data['units'][0]
            replacement = unit['analysis']['grammar_points'][-1]
            replacement['formula_key'] = replacement['practice']['formula_support']['en'] = formula
            unit['analysis']['formula_routes'][1]['formula_key'] = formula
            with self.subTest(formula=formula), self.assertRaisesRegex(ValueError, 'positive simple passive'):
                self.check(data)

    def test_exception_cannot_disguise_an_unused_or_duplicate_supplement(self):
        data = exception_fixture()
        data['units'][0]['analysis']['formula_routes'][0].update(
            route='analysis', grammar_point_id='p1')
        with self.assertRaisesRegex(ValueError, 'unknown or inapplicable'): self.check(data)
        data = exception_fixture()
        other = data['units'][0]['analysis']['grammar_points'][1]
        other['formula_key'] = other['practice']['formula_support']['en'] = 'be p.p.'
        with self.assertRaisesRegex(ValueError, 'do not repeat'): self.check(data)

    def test_route_types_reject_foreign_or_unknown_fields(self):
        for route_index, extra in [(0, {'hint_index': 0}), (0, {'unknown': True}),
                                   (1, {'grammar_point_id': 'p4'}),
                                   (1, {'approval_reference': 'not-applicable'})]:
            data = exception_fixture()
            data['units'][0]['analysis']['formula_routes'][route_index].update(extra)
            with self.subTest(extra=extra), self.assertRaisesRegex(ValueError, 'unknown or inapplicable'):
                self.check(data)


if __name__ == '__main__':
    unittest.main()
