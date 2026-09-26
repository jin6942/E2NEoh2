"""Approved formula training: source links, printed p.p. notes and narrow hints."""
from copy import deepcopy
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent / '../scripts'))
import check_learning_content as m
from structure_hints import display_lines
from test_learning_content import aligned_pair
from test_reading_rule_revision import sentence
from test_verb_gloss_revision import combined_sentence


def training_sentence(original, phrase, participle, lemma, formula, formula_ko,
                      lexical_ko, result_ko, passive=False, frame=None, connector=None):
    s = sentence(original)
    start = original.index(phrase)
    end = start + len(phrase)
    va = original.index(participle, start)
    vb = va + len(participle)
    old = {g['id'] for g in s['glosses'] if start <= g['spans'][0][0] < end}
    f = {'id': 'formula', 'kind': 'function', 'spans': [[start, va - 1]],
         'headword': formula, 'meaning_ko': formula_ko, 'star': False,
         'combines_with': ['word']}
    meaning = lexical_ko if passive else f'{lexical_ko} ({participle}는 {lemma}의 p.p.형)'
    lexical = {'id': 'word', 'kind': 'lexical', 'spans': [[va, vb]],
               'headword': participle if passive else lemma, 'meaning_ko': meaning,
               'star': False, 'verb_form': {
                   'usage': 'passive-participle' if passive else 'perfect-participle',
                   'source_span': [va, vb], 'lemma': lemma, 'function_gloss_id': 'formula'}}
    hint_end = end
    if frame:
        ca = original.index(connector, vb)
        cb = ca + len(connector)
        lexical['headword'] = frame
        lexical['spans'].append([ca, cb])
        lexical['verb_construction'] = {
            'kind': 'to-complement' if connector == 'to' else 'verb-frame',
            'verb_span': [va, vb], 'lemma': lemma, 'link_spans': [[ca, cb]],
            'review_record': 'Synthetic authored complement/frame decision.'}
        old.update(g['id'] for g in s['glosses'] if g['spans'] == [[ca, cb]])
        hint_end = cb
    s['glosses'] = [g for g in s['glosses'] if g['id'] not in old] + [f, lexical]
    s['glosses'].sort(key=lambda g: g['spans'][0][0])
    for row in s['lexical_coverage']:
        if row.get('gloss_id') in old:
            row['gloss_id'] = 'formula' if row['span'][1] <= va else 'word'
    s['reading_checks'] = {'review_record': 'Synthetic authored form decision.',
        'required_breaks': [], 'protected_spans': [], 'function_gloss_ids': ['formula']}
    # Whole irregular inflections can be selected; no automatic morphology
    # claim is made by this source-binding fixture.
    s['hints'] = [{'span': [start, hint_end], 'category': 'function-combination',
        'display_mode': 'verb-function', 'display_span': [start, end],
        'formula_label': formula, 'meaning_ko': result_ko,
        'explanation': 'Synthetic source/form alignment only.',
        'gloss_ids': ['formula', 'word'],
        'lexical_step': {'gloss_id': 'word', 'form': participle if passive else lemma,
                         'meaning_ko': lexical_ko},
        'display_pairs': [aligned_pair(phrase, result_ko, ([phrase], [result_ko]))]}]
    return s


def five_examples():
    return [
        training_sentence('Plastic is produced.', 'is produced', 'produced', 'produce',
                          'be p.p.', '~되다', '생산된', '생산된다', passive=True),
        training_sentence('Plastic is being produced.', 'is being produced', 'produced', 'produce',
                          'be being p.p.', '~되고 있다', '생산된', '생산되고 있다', passive=True),
        training_sentence('Researchers have found evidence.', 'have found', 'found', 'find',
                          'have p.p.', '~했다', '발견하다', '발견했다'),
        training_sentence('Plastic has been recycled.', 'has been recycled', 'recycled', 'recycle',
                          'have been p.p.', '~되었다', '재활용된', '재활용되었다', passive=True),
        training_sentence('They may have provided us with food.', 'may have provided', 'provided', 'provide',
                          'may have p.p.', '~했을지도 모른다', '제공하다', '제공했을지도 모른다',
                          frame='provide A with B', connector='with')]


def idiom_sentence(original='Students are provided with books.', headword='be provided with',
                   phrase='are provided with', verb='provided'):
    s = sentence(original)
    start = original.index(phrase)
    end = start + len(phrase)
    va = original.index(verb, start)
    old = {g['id'] for g in s['glosses'] if start <= g['spans'][0][0] < end}
    g = {'id': 'idiom', 'kind': 'lexical', 'spans': [[start, end]],
         'headword': headword, 'meaning_ko': '~을 제공받다', 'star': False,
         'verb_phrase': {'usage': 'idiom', 'dictionary_headword': headword,
             'review_record': 'Synthetic reviewed idiom.', 'reason': 'Whole construction meaning.',
             'formula_label': 'be p.p.', 'source_spans': [[start, end]],
             'verb_span': [va, va + len(verb)]}}
    s['glosses'] = [r for r in s['glosses'] if r['id'] not in old] + [g]
    s['glosses'].sort(key=lambda r: r['spans'][0][0])
    for row in s['lexical_coverage']:
        if row.get('gloss_id') in old:
            row['gloss_id'] = 'idiom'
    s['reading_checks'] = {'review_record': 'Synthetic idiom declaration.',
        'required_breaks': [], 'protected_spans': [], 'function_gloss_ids': []}
    return s


def with_outer_function(s, source_prefix, headword):
    """Declare a separately reviewed outer function using its earlier words."""
    start = s['text'].index(source_prefix)
    end = start + len(source_prefix)
    old = {g['id'] for g in s['glosses'] if start <= g['spans'][0][0] < end}
    s['glosses'] = [g for g in s['glosses'] if g['id'] not in old]
    s['glosses'].append({'id': 'outer', 'kind': 'function', 'spans': [[start, end]],
                        'headword': headword, 'meaning_ko': '시험용 외부 기능',
                        'star': False, 'combines_with': ['word']})
    s['glosses'].sort(key=lambda g: g['spans'][0][0])
    for row in s['lexical_coverage']:
        if row.get('gloss_id') in old:
            row['gloss_id'] = 'outer'
    s['reading_checks']['function_gloss_ids'] = [g['id'] for g in s['glosses'] if g.get('kind') == 'function']
    return s


class FormulaTrainingGlossTests(unittest.TestCase):
    def check(self, s):
        before = deepcopy(s)
        result = m.glossary(s, {}, require_reading_checks=True)
        self.assertEqual(s, before)
        return result

    def test_five_approved_examples_are_source_bound_and_print_lexical_step(self):
        expected = [
            'produced(생산된) → is produced(생산된다) (be p.p.)',
            'produced(생산된) → is being produced(생산되고 있다) (be being p.p.)',
            'find(발견하다) → have found(발견했다) (have p.p.)',
            'recycled(재활용된) → has been recycled(재활용되었다) (have been p.p.)',
            'provide(제공하다) → may have provided(제공했을지도 모른다) (may have p.p.)']
        for s, line in zip(five_examples(), expected):
            with self.subTest(line=line):
                self.check(s)
                self.assertEqual(display_lines(s['hints'][0]), [line])

    def test_perfect_note_must_be_visible_not_metadata_only(self):
        s = five_examples()[2]
        g = next(g for g in s['glosses'] if g['id'] == 'word')
        g['meaning_ko'] = '발견하다'
        g['verb_form']['note'] = '(found는 find의 p.p.형)'
        with self.assertRaisesRegex(ValueError, 'must print'):
            self.check(s)

    def test_perfect_note_must_identify_actual_form_and_correct_lemma(self):
        for note in ('(find는 find의 p.p.형)', '(found는 found의 p.p.형)'):
            s = five_examples()[2]
            next(g for g in s['glosses'] if g['id'] == 'word')['meaning_ko'] = '발견하다 ' + note
            with self.assertRaisesRegex(ValueError, 'must print'):
                self.check(s)

    def test_visible_pp_note_accepts_natural_korean_topic_particle(self):
        s = training_sentence('They have written letters.', 'have written', 'written', 'write',
                              'have p.p.', '~했다', '쓰다', '썼다')
        g = next(g for g in s['glosses'] if g['id'] == 'word')
        g['meaning_ko'] = '쓰다 (written은 write의 p.p.형)'
        self.check(s)

    def test_passive_keeps_pp_and_active_perfect_uses_lemma(self):
        for index, bad in ((0, 'produce'), (2, 'found'), (3, 'recycle')):
            s = five_examples()[index]
            next(g for g in s['glosses'] if g['id'] == 'word')['headword'] = bad
            with self.assertRaisesRegex(ValueError, 'must preserve'):
                self.check(s)

    def test_passive_headword_cannot_append_unreviewed_phrase(self):
        s = five_examples()[0]
        next(g for g in s['glosses'] if g['id'] == 'word')['headword'] = 'produced invented phrase'
        with self.assertRaisesRegex(ValueError, 'only its actual source'):
            self.check(s)

    def test_perfect_passive_cannot_be_marked_active_perfect(self):
        s = five_examples()[3]
        g = next(g for g in s['glosses'] if g['id'] == 'word')
        g['verb_form']['usage'] = 'perfect-participle'
        g['headword'] = 'recycle'
        g['meaning_ko'] = '재활용하다 (recycled는 recycle의 p.p.형)'
        with self.assertRaisesRegex(ValueError, 'passive takes precedence'):
            self.check(s)

    def test_declared_participle_cannot_link_two_split_function_formulas(self):
        s = five_examples()[3]
        f = deepcopy(next(g for g in s['glosses'] if g['id'] == 'formula'))
        f['id'] = 'other-formula'
        s['glosses'].insert(1, f)
        s['reading_checks']['function_gloss_ids'] = ['other-formula', 'formula']
        with self.assertRaisesRegex(ValueError, 'exactly one composite'):
            self.check(s)

    def test_missing_or_unrelated_function_link_fails(self):
        s = five_examples()[0]
        next(g for g in s['glosses'] if g['id'] == 'word')['verb_form']['function_gloss_id'] = 'absent'
        with self.assertRaisesRegex(ValueError, 'exactly one composite'):
            self.check(s)

    def test_outer_obligation_and_passive_support_omitted_that_hint(self):
        s = training_sentence('They said laws had to be changed.', 'be changed', 'changed', 'change',
                              'be p.p.', '~되다', '바뀐', '바뀌다', passive=True)
        with_outer_function(s, 'had to', 'had to V')
        a = s['text'].index('laws')
        b = s['text'].index('.')
        s['hints'] = [{'span': [a, b], 'display_mode': 'omitted-conjunction',
                      'omitted_conjunction': 'that', 'structure_label': '명사절 접속사 that 생략',
                      'meaning_ko': '법이 바뀌어야 한다고', 'explanation': 'Synthetic omitted that.',
                      'display_pairs': [aligned_pair('[(that) laws had to be changed]',
                          '[법이 바뀌어야 한다고]', (['that'], ['이', '다고']))]}]
        self.check(s)
        next(g for g in s['glosses'] if g['id'] == 'outer')['headword'] = 'have to V'
        self.check(s)

    def test_outer_to_v_and_simple_passive_modal_are_preserved(self):
        examples = [('They hope to be invited.', 'to', 'to V', 'invited', 'invite', '초대된'),
                    ('The plan would be adopted.', 'would', 'would V', 'adopted', 'adopt', '채택된')]
        for original, prefix, formula, pp, lemma, meaning in examples:
            s = training_sentence(original, 'be ' + pp, pp, lemma,
                                  'be p.p.', '~되다', meaning, meaning, passive=True)
            with_outer_function(s, prefix, formula)
            s['hints'] = []
            self.check(s)

    def test_outer_function_requires_earlier_disjoint_source_correspondence(self):
        for bad in ('overlap', 'wrong-frame'):
            s = training_sentence('They hope to be invited.', 'be invited', 'invited', 'invite',
                                  'be p.p.', '~되다', '초대된', '초대되다', passive=True)
            with_outer_function(s, 'to', 'to V')
            s['hints'] = []
            outer = next(g for g in s['glosses'] if g['id'] == 'outer')
            if bad == 'overlap':
                outer['spans'][0][1] = s['text'].index('be') + 2
            else:
                outer['headword'] = 'had to V'
            with self.assertRaisesRegex(ValueError, 'exactly one composite'):
                self.check(s)

    def test_outer_modal_cannot_split_active_or_passive_modal_perfect(self):
        for passive in (False, True):
            phrase = 'have been found' if passive else 'have found'
            formula = 'have been p.p.' if passive else 'have p.p.'
            s = training_sentence('Evidence may ' + phrase + ' clues.', phrase, 'found', 'find',
                                  formula, '~되었다' if passive else '~했다',
                                  '발견된' if passive else '발견하다', '발견했다', passive=passive)
            with_outer_function(s, 'may', 'may V')
            s['hints'] = []
            with self.assertRaisesRegex(ValueError, 'exactly one composite'):
                self.check(s)

    def test_supported_modal_negation_and_ought_formulas_remain_valid(self):
        for auxiliary in ('may not have', 'cannot have', 'ought to have'):
            s = training_sentence('They ' + auxiliary + ' found evidence.', auxiliary + ' found',
                'found', 'find', auxiliary + ' p.p.', '~했을지도 모른다', '발견하다', '발견했을지도 모른다')
            self.check(s)
        s = five_examples()[2]
        next(g for g in s['glosses'] if g['id'] == 'formula')['headword'] = 'happy have p.p.'
        with self.assertRaisesRegex(ValueError, 'passive takes precedence'):
            self.check(s)

    def test_function_cannot_cover_following_object(self):
        s = five_examples()[2]
        next(g for g in s['glosses'] if g['id'] == 'formula')['spans'][0][1] = len(s['text']) - 1
        with self.assertRaisesRegex(ValueError, 'stop before objects'):
            self.check(s)

    def test_no_hint_required_when_formula_is_lower_priority(self):
        for s in five_examples():
            s['hints'] = []
            self.check(s)

    def test_selected_new_formula_hint_requires_lexical_step(self):
        s = five_examples()[0]
        del s['hints'][0]['lexical_step']
        with self.assertRaisesRegex(ValueError, 'needs its lexical_step'):
            self.check(s)

    def test_lexical_step_cannot_use_wrong_form_or_gloss(self):
        for field, value in (('form', 'produced'), ('gloss_id', 'g0')):
            s = five_examples()[2]
            s['hints'][0]['lexical_step'][field] = value
            with self.assertRaisesRegex(ValueError, 'lexical_step'):
                self.check(s)

    def test_lexical_step_simple_meaning_matches_printed_gloss(self):
        s = five_examples()[2]
        g = next(g for g in s['glosses'] if g['id'] == 'word')
        g['meaning_ko'] = '발견하다, 알아내다 (흔한 뜻: 찾다) (found는 find의 p.p.형)'
        self.check(s)
        s['hints'][0]['lexical_step']['meaning_ko'] = '찾다'
        with self.assertRaisesRegex(ValueError, 'meaning must match'):
            self.check(s)
        s['hints'][0]['lexical_step']['meaning_ko'] = '파괴하다'
        with self.assertRaisesRegex(ValueError, 'meaning must match'):
            self.check(s)

    def test_frame_allows_local_short_meaning_without_displaying_object(self):
        s = five_examples()[4]
        g = next(g for g in s['glosses'] if g['id'] == 'word')
        g['meaning_ko'] = 'A에게 B를 제공하다 (provided는 provide의 p.p.형)'
        self.check(s)
        self.assertNotIn('with', display_lines(s['hints'][0])[0])

    def test_frame_rejects_invented_connector_or_hidden_frame_declaration(self):
        for mode in ('replace', 'remove'):
            s = five_examples()[4]
            g = next(g for g in s['glosses'] if g['id'] == 'word')
            if mode == 'replace':
                g['headword'] = 'provide A for B'
            else:
                del g['verb_construction']
            with self.assertRaisesRegex(ValueError, 'source-bound'):
                self.check(s)

    def test_frame_source_spans_cannot_absorb_object(self):
        s = five_examples()[4]
        g = next(g for g in s['glosses'] if g['id'] == 'word')
        g['spans'] = [[g['spans'][0][0], g['spans'][1][1]]]
        with self.assertRaisesRegex(ValueError, 'not objects'):
            self.check(s)

    def test_current_blanket_combined_phrase_rejected_but_legacy_readable(self):
        s = combined_sentence()
        m.glossary(s, {}, require_reading_checks=False)
        with self.assertRaisesRegex(ValueError, 'separates formula'):
            self.check(s)

    def test_explicit_dictionary_idioms_keep_one_gloss(self):
        for original, head, phrase, verb in [
            ('Students are provided with books.', 'be provided with', 'are provided with', 'provided'),
            ('They were satisfied with results.', 'be satisfied with', 'were satisfied with', 'satisfied'),
            ('He was born yesterday.', 'be born', 'was born', 'born'),
            ('It is called a gift.', 'be called A', 'is called', 'called')]:
            self.check(idiom_sentence(original, head, phrase, verb))

    def test_idiom_requires_review_and_source_dictionary_correspondence(self):
        for field, value in (('review_record', ''), ('dictionary_headword', 'be supplied with')):
            s = idiom_sentence()
            next(g for g in s['glosses'] if g['id'] == 'idiom')['verb_phrase'][field] = value
            with self.assertRaises(ValueError):
                self.check(s)

    def test_perfect_progressive_unchanged_outside_new_pp_scope(self):
        original = 'He has been working.'
        g = {'kind': 'lexical', 'spans': [[3, 19]], 'headword': 'has been working',
             'verb_phrase': {'formula_label': 'have been V-ing', 'source_spans': [[3, 19]],
                             'verb_span': [12, 19]}}
        m.verb_phrase_review(g, original, required=True)

    def test_struggle_to_v_frame_combines_only_complement_formula(self):
        s = training_sentence('She had struggled to enter.', 'had struggled', 'struggled', 'struggle',
            'had p.p.', '~했다', '애쓰다', '애썼다', frame='struggle to V', connector='to')
        g = next(g for g in s['glosses'] if g['id'] == 'word')
        g['meaning_ko'] = '~하려고 애쓰다 (struggled는 struggle의 p.p.형)'
        self.check(s)
        self.assertEqual(display_lines(s['hints'][0]), ['struggle(애쓰다) → had struggled(애썼다) (had p.p.)'])

    def test_to_function_uncommon_complement_meanings_rejected_purpose_allowed(self):
        for meaning in ('~하기로', '~하려고', '~하는 데', '~하는데', '~하기 위해'):
            s = sentence('She used money to buy books.')
            g = next(g for g in s['glosses'] if g['headword'] == 'to')
            target = next(g for g in s['glosses'] if g['headword'] == 'buy')
            target['kind'] = 'lexical'
            g.update(kind='function', headword='to V', meaning_ko=meaning, combines_with=[target['id']])
            s['reading_checks'] = {'review_record': 'Synthetic purpose decision.', 'required_breaks': [],
                                  'protected_spans': [], 'function_gloss_ids': [g['id']]}
            if meaning == '~하기 위해':
                self.check(s)
            else:
                with self.assertRaisesRegex(ValueError, 'Do not split to V'):
                    self.check(s)

    def test_independent_participle_focus_requires_whole_bilingual_word(self):
        s = sentence('The meeting held yesterday ended.')
        g = next(g for g in s['glosses'] if g['headword'] == 'held')
        g.update(kind='lexical', meaning_ko='개최된', verb_form={
            'usage': 'past-participle', 'source_span': g['spans'][0], 'lemma': 'hold'})
        a, b = g['spans'][0]
        s['reading_checks'] = {'review_record': 'Synthetic independent participle.', 'required_breaks': [],
                              'protected_spans': [], 'function_gloss_ids': []}
        s['hints'] = [{'span': [a, b], 'meaning_ko': '개최된', 'explanation': 'Synthetic independent pp.',
            'participle_focus_gloss_id': g['id'], 'structure_label': '과거분사 후치수식',
            'display_pairs': [aligned_pair('[held]', '[개최된]', (['held'], ['개최된']))]}]
        self.check(s)
        g['meaning_ko'] = '(행사가) 열린, 개최된 (흔한 뜻: 손에 쥔)'
        self.check(s)
        s['hints'][0]['display_pairs'] = [aligned_pair('[held]', '[개최된]', (['held'], ['된']))]
        with self.assertRaisesRegex(ValueError, 'entire contextual Korean meaning'):
            self.check(s)


class SourceBoundBookConstructionTests(unittest.TestCase):
    def test_negative_passive_and_perfect_keep_voice_and_negation(self):
        for formula, original, phrase, word, lemma, passive, meaning, result in [
            ('be not p.p.', 'It is not controlled.', 'is not controlled', 'controlled', 'control', True, '통제된', '통제되지 않는다'),
            ('have not p.p.', 'They have not found it.', 'have not found', 'found', 'find', False, '발견하다', '발견하지 않았다')]:
            s = training_sentence(original, phrase, word, lemma, formula, '~하지 않다', meaning, result, passive=passive)
            m.glossary(s, {}, require_reading_checks=True)
            self.assertIn(phrase, display_lines(s['hints'][0])[0])
            g = next(g for g in s['glosses'] if g['id'] == 'word')
            g['verb_form']['usage'] = 'perfect-participle' if passive else 'passive-participle'
            with self.assertRaisesRegex(ValueError, 'must match its composite formula'):
                m.participle_function_review({g['id']: g for g in s['glosses']}, original)

    def phrasal(self):
        return {'kind': 'lexical', 'spans': [[12, 15], [16, 18]],
                'headword': 'dug up', 'meaning_ko': '파내어진',
                'verb_form': {'usage': 'passive-participle', 'source_span': [12, 15],
                              'lemma': 'dig', 'function_gloss_id': 'passive',
                              'particle_spans': [[16, 18]],
                              'review_record': 'The particle up belongs to dig up, not a separate object.'}}

    def frame(self):
        return {'kind': 'lexical', 'spans': [[10, 15]], 'headword': 'give A B',
                'meaning_ko': 'A에게 B를 주다 (given은 give의 p.p.형)',
                'verb_form': {'usage': 'perfect-participle', 'source_span': [10, 15],
                              'lemma': 'give', 'function_gloss_id': 'perfect'},
                'verb_construction': {'kind': 'verb-frame', 'verb_span': [10, 15],
                                      'lemma': 'give', 'link_spans': [],
                                      'review_record': 'Give has two objects here without a preposition.'}}

    def test_passive_phrasal_word_preserves_its_source_particle(self):
        m.verb_form_review(self.phrasal(), 'Soil can be dug up safely.')

    def test_passive_particle_rejects_invented_word_or_inflated_span(self):
        for change in ('headword', 'span', 'review'):
            g = self.phrasal()
            if change == 'headword': g['headword'] = 'dug out'
            if change == 'span': g['verb_form']['particle_spans'] = [[16, 25]]
            if change == 'review': g['verb_form']['review_record'] = ''
            with self.subTest(change=change), self.assertRaises(ValueError):
                m.verb_form_review(g, 'Soil can be dug up safely.')

    def test_passive_particle_cannot_absorb_object_or_duplicate(self):
        for change in ('spans', 'duplicate'):
            g = self.phrasal()
            if change == 'spans': g['spans'] = [[12, 18]]
            if change == 'duplicate': g['verb_form']['particle_spans'] *= 2
            with self.subTest(change=change), self.assertRaises(ValueError):
                m.verb_form_review(g, 'Soil can be dug up safely.')

    def test_double_object_frame_has_no_invented_link_word(self):
        g = self.frame()
        m.verb_form_review(g, 'Study has given us hope.')
        m.verb_construction_review(g, 'Study has given us hope.')

    def test_empty_links_do_not_allow_unbound_preposition_or_to_complement(self):
        for change in ('preposition', 'to-complement', 'object'):
            g = self.frame()
            if change == 'preposition': g['headword'] = 'give A to B'
            if change == 'to-complement': g['verb_construction']['kind'] = 'to-complement'
            if change == 'object': g['spans'] = [[10, 18]]
            with self.subTest(change=change), self.assertRaises(ValueError):
                m.verb_construction_review(g, 'Study has given us hope.')


if __name__ == '__main__':
    unittest.main()
