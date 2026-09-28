"""Authored verb/function and omitted-conjunction displays; no grammar guessing."""
from copy import deepcopy
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent / '../scripts'))
from book_plan import structure_hint_element
import check_learning_content as learning
from structure_hints import (display_pairs, display_lines, aligned_display_segments,
                             omitted_conjunction_source_text)
from test_learning_content import aligned_pair, absent_marker_pair, modal_hint_fixture


def verb_hint(english='is produced', korean='생산된다', formula='be p.p.',
              en_markers=None, ko_markers=None):
    return {'category':'function-combination', 'display_mode':'verb-function',
            'display_span':[0, len(english)], 'formula_label':formula,
            'display_pairs':[aligned_pair(english, korean,
                (en_markers or ['is','ed'], ko_markers or ['된다']))]}


def conjunction_hint():
    return {'span':[6,14], 'display_mode':'omitted-conjunction', 'omitted_conjunction':'that',
            'structure_label':'명사절 접속사 that 생략',
            'display_pairs':[aligned_pair('[(that) she knew]', '[그녀가 알았다는 것]',
                                         (['that'], ['가','다는 것']))]}


class VerbFunctionHintTests(unittest.TestCase):
    def test_legacy_tense_voice_display_remains_readable_without_silent_rewriting(self):
        examples = [
            ('is produced','생산된다','be p.p.',['is','ed'],['된다']),
            ('has been recycled','재활용되었다','have been p.p.',['has','been','ed'],['되었다']),
            ('had predicted','예측했다','had p.p.',['had','ed'],['했다']),
            ('is also being produced','또한 생산되고 있다','be being p.p.',
             ['is','being','ed'],['되고 있다']),
            ('may have provided','제공했을지도 모른다','may have p.p.',
             ['may','have','ed'],['했을지도 모른다']),
        ]
        for english,korean,formula,en_markers,ko_markers in examples:
            with self.subTest(english=english):
                hint=verb_hint(english,korean,formula,en_markers,ko_markers); before=deepcopy(hint)
                display_pairs(hint,require_alignment=True)
                expected=english+' → '+korean+' ('+formula+')'
                self.assertEqual(display_lines(hint),[expected])
                runs=structure_hint_element(hint)['runs']
                self.assertEqual(''.join(r['text'] for r in runs),'구조 힌트   '+expected)
                self.assertEqual(runs[-1],{'run':1,'text':' ('+formula+')'})
                self.assertEqual([s for marked,s in aligned_display_segments(hint['display_pairs'][0],'en')
                                  if marked],en_markers)
                self.assertEqual([s for marked,s in aligned_display_segments(hint['display_pairs'][0],'ko')
                                  if marked],ko_markers)
                self.assertEqual(hint,before)

    def test_formula_and_display_range_are_explicit_not_inferred(self):
        base=verb_hint()
        for field in ('formula_label','display_span'):
            hint=deepcopy(base);hint.pop(field)
            with self.subTest(field=field),self.assertRaises(ValueError):display_pairs(hint)
        for formula in ['',None,' be p.p.','be p.p.\n','(be p.p.)','수동태','what to V',
                        'be p.p. + produce','be p.p.; explanation']:
            hint=deepcopy(base);hint['formula_label']=formula
            with self.subTest(formula=formula),self.assertRaises(ValueError):display_pairs(hint)
        hint=deepcopy(base);hint['display_pairs'][0]['ko']+=' (be p.p.)'
        with self.assertRaisesRegex(ValueError,'formula_label'):display_pairs(hint)

    def test_literal_verb_mode_does_not_accept_formula_slots_or_plus_notation(self):
        for english in ['be p.p. + produced','is p.p.','is produced A','is [produced]']:
            hint=verb_hint();hint['display_pairs'][0]['en']=english
            with self.subTest(english=english),self.assertRaises(ValueError):display_pairs(hint)

    def test_current_verb_mode_keeps_required_authored_bilingual_links(self):
        for edit in ('absent','empty'):
            hint=verb_hint();pair=hint['display_pairs'][0]
            if edit=='absent':pair.pop('emphasis_links')
            else:pair.update(emphasis_links=[],emphasis_note='No guessed grammar counterpart.')
            with self.subTest(edit=edit),self.assertRaises(ValueError):display_pairs(hint)

    def test_legacy_tense_displays_are_readable_but_not_current_or_silently_converted(self):
        for english,korean in [('be p.p. + produced','생산된다'),
                               ('had p.p. + predicted','예측했다'),
                               ('be V-ing + be p.p. + produced','생산되고 있다')]:
            hint={'category':'function-combination','display_pairs':[
                aligned_pair(english,korean,([english.split(' + ')[0]],[korean[-2:]]))]}
            before=deepcopy(hint)
            self.assertEqual(display_lines(hint),[english+' → '+korean])
            with self.assertRaisesRegex(ValueError,'verb-function mode'):
                display_pairs(hint,require_alignment=True)
            self.assertEqual(hint,before)
        hint=modal_hint_fixture()['sentences'][0]['hints'][0]
        hint['display_mode']='modal-perfect-verb';hint.pop('formula_label')
        self.assertEqual(display_lines(hint),['may have provided → 제공했을지도 모른다'])
        with self.assertRaisesRegex(ValueError,'not current'):display_pairs(hint,require_alignment=True)

    def test_what_to_v_and_paired_structure_keep_existing_display(self):
        function={'category':'function-combination','display_pairs':[
            aligned_pair('what to V + do','무엇을 해야 할지',(['what to V'],['무엇을 해야 할지']))]}
        paired={'category':'paired-structure','display_spans':[[0,4],[8,11]],
                'display_pairs':[aligned_pair('both … and','둘 다 … 그리고',(['both'],['둘 다']))]}
        for hint in (function,paired):
            display_pairs(hint,require_alignment=True)
            pair=hint['display_pairs'][0]
            self.assertEqual(display_lines(hint),[pair['en']+' → '+pair['ko']])
        function['formula_label']='be p.p.'
        with self.assertRaisesRegex(ValueError,'verb-function'):display_pairs(function)

    def test_verb_source_validation_rejects_object_extension_without_changing_source(self):
        data=modal_hint_fixture();sentence=data['sentences'][0];hint=sentence['hints'][0]
        end=sentence['text'].index(' with')
        hint['display_span'][1]=end
        hint['display_pairs'][0]=aligned_pair(sentence['text'][slice(*hint['display_span'])],
            '제공했을지도 모른다',(['may have','ed'],['했을지도 모른다']))
        before=deepcopy(data)
        with self.assertRaisesRegex(ValueError,'end at a linked lexical verb'):
            learning.check(data,scope='learning')
        self.assertEqual(data,before)


class OmittedConjunctionHintTests(unittest.TestCase):
    def test_that_supports_subject_particle_and_actual_noun_clause_meaning(self):
        hint=conjunction_hint();before=deepcopy(hint)
        display_pairs(hint,require_alignment=True)
        self.assertEqual(omitted_conjunction_source_text(hint),'she knew')
        self.assertEqual(learning.omitted_conjunction_display_range(hint,'Think she knew.'),(6,14))
        self.assertEqual(hint,before)
        pair=hint['display_pairs'][0]
        self.assertEqual([s for marked,s in aligned_display_segments(pair,'en') if marked],['that'])
        self.assertEqual([s for marked,s in aligned_display_segments(pair,'ko') if marked],['가','다는 것'])

    def test_editorial_parentheses_stay_plain_in_word_and_txt(self):
        hint=conjunction_hint();runs=structure_hint_element(hint)['runs']
        self.assertEqual([r['text'] for r in runs if r.get('underline')],['that'])
        self.assertEqual([r['text'] for r in runs if r.get('format_role')=='structure_hint_ko' and r['run']==1],
                         ['가','다는 것'])
        for run in runs:
            if '(' in run['text'] or ')' in run['text']:
                self.assertFalse(run.get('underline',False))
        self.assertEqual(display_lines(hint),[
            '[(that) she knew] → [그녀가 알았다는 것] (명사절 접속사 that 생략)'])

    def test_conjunction_mode_cannot_be_confused_with_relative_or_other_supplements(self):
        base=conjunction_hint()
        for update in [{'omitted_conjunction':'because'}, {'omitted_conjunction':'which'},
                       {'omitted_conjunction':None}, {'omitted_relative':'that'},
                       {'display_mode':'omitted-relative'}, {'structure_label':'관계대명사 that 생략'},
                       {'structure_label':'명사절 접속사 that'}, {'category':'function-combination'}]:
            with self.subTest(update=update),self.assertRaises(ValueError):
                display_pairs({**deepcopy(base),**update},require_alignment=True)

    def test_that_marker_cannot_be_misplaced_duplicated_or_have_blank_link(self):
        for english in ['(that) [she knew]','[she (that) knew]',
                        '[(that) (that) she knew]','[( that ) she knew]']:
            hint=conjunction_hint()
            hint['display_pairs'][0]=aligned_pair(english,'[그녀가 알았다는 것]',(['that'],['가','다는 것']))
            with self.subTest(english=english),self.assertRaises(ValueError):display_pairs(hint)
        hint=conjunction_hint()
        hint['display_pairs'][0].update(emphasis_links=[],emphasis_note='that is omitted in source.')
        with self.assertRaisesRegex(ValueError,'supplied marker'):display_pairs(hint)

    def test_marker_only_links_inside_korean_bracket_without_blanket_emphasis(self):
        for english_marker,korean_markers in [('she',['가']),('that',['그녀가 알았다는 것'])]:
            hint=conjunction_hint()
            hint['display_pairs'][0]=aligned_pair('[(that) she knew]','[그녀가 알았다는 것]',
                                                 ([english_marker],korean_markers))
            with self.subTest(marker=english_marker),self.assertRaises(ValueError):display_pairs(hint)

    def test_legacy_empty_omitted_that_link_is_readable_but_not_current(self):
        hint={'structure_label':'명사절 접속사 that 생략','display_pairs':[
            absent_marker_pair('[she knew]','[그녀가 알았다는 것]','Previously recorded omitted marker.') ]}
        before=deepcopy(hint)
        self.assertEqual(display_pairs(hint),hint['display_pairs'])
        with self.assertRaisesRegex(ValueError,'omitted-conjunction mode'):
            display_pairs(hint,require_alignment=True)
        self.assertEqual(hint,before)


if __name__=='__main__':
    unittest.main()
