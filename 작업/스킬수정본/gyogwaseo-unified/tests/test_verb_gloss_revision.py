"""Source-bound approved verb glosses; no automatic grammatical classification."""
from copy import deepcopy
from pathlib import Path
import sys,unittest
sys.path.insert(0,str(Path(__file__).resolve().parent/'../scripts'))
import check_learning_content as m
from test_reading_rule_revision import sentence
from test_learning_content import aligned_pair


def combined_sentence(original='It was changed.', expression='was changed', verb='changed', formula='was p.p.'):
    s=sentence(original);start=original.index(expression);end=start+len(expression)
    verb_start=original.index(verb,start)
    members=[g for g in s['glosses'] if start <= g['spans'][0][0] < end]
    ids={g['id'] for g in members}
    new={'id':'combined','kind':'lexical','spans':[[start,end]],'headword':expression,
         'meaning_ko':'바뀌었다','star':False,'verb_phrase':{'formula_label':formula,
         'source_spans':[[start,end]],'verb_span':[verb_start,end]}}
    s['glosses']=[g for g in s['glosses'] if g['id'] not in ids]+[new]
    s['glosses'].sort(key=lambda g:g['spans'][0][0])
    for row in s['lexical_coverage']:
        if row.get('gloss_id') in ids:row['gloss_id']='combined'
    s['reading_checks']={'review_record':'Synthetic reviewer declaration only.',
        'required_breaks':[],'protected_spans':[],'function_gloss_ids':[]}
    s['hints']=[{'span':[start,end],'category':'function-combination','display_mode':'verb-function',
        'display_span':[start,end],'formula_label':formula,'meaning_ko':'바뀌었다',
        'explanation':'Synthetic test only.','gloss_ids':['combined'],
        'display_pairs':[aligned_pair(expression,'바뀌었다',(['was','ed'],['뀌었다']))]}]
    return s


class VerbGlossRevisionTests(unittest.TestCase):
    def test_declared_third_person_lexical_headword_uses_lemma(self):
        for actual, lemma in [('helps', 'help'), ('studies', 'study'), ('watches', 'watch'),
                              ('goes', 'go'), ('does', 'do'), ('has', 'have')]:
            with self.subTest(actual=actual):
                g={'kind':'lexical','spans':[[3,3+len(actual)]],'headword':lemma,
                   'verb_form':{'usage':'third-person-singular','source_span':[3,3+len(actual)],
                                'lemma':lemma,'review_record':'Reviewed finite lexical verb, not a noun or auxiliary.'}}
                original='It '+actual+'.';before=deepcopy(g)
                m.verb_form_review(g,original)
                self.assertEqual(g,before)
                g['headword']=actual
                with self.assertRaisesRegex(ValueError,'use the lemma'):
                    m.verb_form_review(g,original)

    def test_third_person_rule_preserves_a_reviewed_verb_frame(self):
        original='It provides us with food.';a=original.index('provides');w=original.index('with')
        g={'kind':'lexical','spans':[[a,a+8],[w,w+4]],'headword':'provide A with B',
           'verb_form':{'usage':'third-person-singular','source_span':[a,a+8],'lemma':'provide',
                        'review_record':'Reviewed third-person lexical verb.'},
           'verb_construction':{'kind':'verb-frame','verb_span':[a,a+8],'lemma':'provide',
                                'link_spans':[[w,w+4]],'review_record':'Source-bound recipient/content frame.'}}
        before=deepcopy(g)
        m.verb_form_review(g,original);m.verb_construction_review(g,original)
        self.assertEqual(g,before)

    def test_third_person_rule_requires_review_and_source_form_relation(self):
        g={'kind':'lexical','spans':[[0,7]],'headword':'study','verb_form':{
            'usage':'third-person-singular','source_span':[0,7],'lemma':'study'}}
        with self.assertRaisesRegex(ValueError,'review record'):
            m.verb_form_review(g,'studies')
        g['verb_form']['review_record']='Reviewed finite verb.'
        for actual,lemma in [('studies','stud'),('news','new'),('is','be'),('does','did')]:
            if actual == 'news':
                # The suffix alone cannot establish a part of speech: unreviewed nouns are untouched.
                noun={'headword':actual};before=deepcopy(noun)
                m.verb_form_review(noun,actual);self.assertEqual(noun,before)
                continue
            g['spans']=[[0,len(actual)]];g['verb_form'].update(source_span=[0,len(actual)],lemma=lemma)
            g['headword']=lemma
            with self.assertRaisesRegex(ValueError,'third-person-singular source'):
                m.verb_form_review(g,actual)

    def test_third_person_rule_does_not_rewrite_plurals_or_function_formulas(self):
        for head in ['creatures','species','has p.p.','does not V']:
            g={'headword':head};before=deepcopy(g)
            m.verb_form_review(g,head);self.assertEqual(g,before)
        g={'kind':'function','spans':[[0,3]],'headword':'have','verb_form':{
            'usage':'third-person-singular','source_span':[0,3],'lemma':'have',
            'review_record':'An auxiliary is not a lexical verb.'}}
        with self.assertRaisesRegex(ValueError,'lexical gloss'):
            m.verb_form_review(g,'has')

    def test_legacy_combined_passive_is_readable_and_preserves_input(self):
        s=combined_sentence();before=deepcopy(s)
        result=m.glossary(s,{},require_reading_checks=False)
        self.assertEqual(result['combined']['headword'],'was changed')
        self.assertEqual(s,before)

    def test_combined_passive_cannot_normalize_actual_auxiliary(self):
        s=combined_sentence();s['glosses'][-1]['headword']='be changed'
        with self.assertRaisesRegex(ValueError,'actual source verb phrase'):
            m.glossary(s,{},require_reading_checks=False)

    def test_combined_phrase_rejects_duplicate_function_or_word(self):
        s=combined_sentence();s['glosses'].insert(1,{'id':'extra','spans':[[3,6]],
            'headword':'was p.p.','meaning_ko':'~되었다','kind':'function',
            'combines_with':['combined'],'star':False})
        s['reading_checks']['function_gloss_ids']=['extra']
        with self.assertRaisesRegex(ValueError,'must not duplicate'):
            m.glossary(s,{},require_reading_checks=False)

    def test_hint_cannot_extend_after_reviewed_verb(self):
        s=combined_sentence('It was changed yesterday.');h=s['hints'][0]
        h['span'][1]=h['display_span'][1]=len(s['text'])-1
        h['display_pairs'][0]['en']='was changed yesterday'
        with self.assertRaisesRegex(ValueError,'end before objects'):
            m.glossary(s,{},require_reading_checks=False)

    def test_hint_formula_must_match_expression_record(self):
        s=combined_sentence();s['hints'][0]['formula_label']='have p.p.'
        with self.assertRaisesRegex(ValueError,'display/formula'):
            m.glossary(s,{},require_reading_checks=False)

    def test_combined_formula_rejects_pp_substring_without_hint(self):
        s=combined_sentence();s['hints']=[]
        s['glosses'][-1]['verb_phrase']['formula_label']='happy'
        with self.assertRaisesRegex(ValueError,'passive or perfect formula'):
            m.glossary(s,{},require_reading_checks=False)

    def test_perfect_progressive_is_combined_but_plain_progressive_is_not(self):
        original='He has been working.'
        g={'kind':'lexical','spans':[[3,19]],'headword':'has been working',
           'verb_phrase':{'formula_label':'have been V-ing','source_spans':[[3,19]],'verb_span':[12,19]}}
        m.verb_phrase_review(g,original)
        g['verb_phrase']['formula_label']='be V-ing'
        with self.assertRaisesRegex(ValueError,'passive or perfect formula'):
            m.verb_phrase_review(g,original)

    def test_combined_verb_range_cannot_be_punctuation(self):
        s=combined_sentence();g=s['glosses'][-1]
        g['spans']=[[3,15]];g['headword']='was changed.'
        g['verb_phrase']['source_spans']=[[3,15]];g['verb_phrase']['verb_span']=[14,15]
        s['hints']=[]
        with self.assertRaisesRegex(ValueError,'lexical words'):
            m.glossary(s,{},require_reading_checks=False)

    def test_combined_headword_cannot_append_invented_words(self):
        for suffix in (' imaginary invention',' A invented B'):
            s=combined_sentence();s['glosses'][-1]['headword']+=suffix
            with self.assertRaisesRegex(ValueError,'frame'):
                m.glossary(s,{},require_reading_checks=False)

    def test_combined_expression_preserves_source_bound_ab_frame(self):
        original='They have provided us with food.';a=original.index('have');v=original.index('provided');b=v+8
        w=original.index('with')
        g={'kind':'lexical','spans':[[a,b],[w,w+4]],'headword':'have provided A with B',
           'verb_phrase':{'formula_label':'have p.p.','source_spans':[[a,b]],'verb_span':[v,b]}}
        m.verb_phrase_review(g,original)
        g['headword']='have provided A for B'
        with self.assertRaisesRegex(ValueError,'source-bound'):
            m.verb_phrase_review(g,original)

    def test_standalone_participle_keeps_actual_form(self):
        original='The event held yesterday ended.';a=original.index('held')
        g={'kind':'lexical','spans':[[a,a+4]],'headword':'held','verb_form':{
            'usage':'past-participle','source_span':[a,a+4],'lemma':'hold'}}
        m.verb_form_review(g,original)
        g['headword']='hold'
        with self.assertRaisesRegex(ValueError,'must preserve'):
            m.verb_form_review(g,original)

    def test_same_ed_spelling_uses_reviewed_role(self):
        for role,head in [('regular-past','change'),('past-participle','changed')]:
            g={'kind':'lexical','spans':[[3,10]],'headword':head,'verb_form':{
                'usage':role,'source_span':[3,10],'lemma':'change'}}
            m.verb_form_review(g,'It changed.')
            g['headword']='changed' if head=='change' else 'change'
            with self.assertRaisesRegex(ValueError,'must preserve'):
                m.verb_form_review(g,'It changed.')

    def test_unreviewed_legacy_form_does_not_claim_grammar_inference(self):
        m.verb_form_review({'headword':'change'},'changed')

    def test_reviewed_participle_inside_see_a_pp_keeps_the_verb_construction(self):
        s=sentence('They saw him trained.')
        target=next(g for g in s['glosses'] if g['headword']=='trained')
        target.update(kind='lexical',meaning_ko='훈련받은',verb_form={
            'usage':'past-participle','source_span':target['spans'][0],'lemma':'train'})
        construction=next(g for g in s['glosses'] if g['headword']=='saw')
        construction.update(kind='function',headword='see A p.p.',meaning_ko='A가 ~된 것을 보다',
                            combines_with=[target['id']])
        s['reading_checks']={'review_record':'Synthetic construction-review record.',
            'required_breaks':[],'protected_spans':[],'function_gloss_ids':[construction['id']]}
        result=m.glossary(s,{},require_reading_checks=True)
        self.assertEqual(result[target['id']]['headword'],'trained')
        self.assertEqual(result[construction['id']]['headword'],'see A p.p.')

    def test_form_span_cannot_point_to_another_gloss_or_partial_word(self):
        for selected in ([0,2],[4,10]):
            g={'kind':'lexical','spans':[[3,10]],'headword':'changed','verb_form':{
                'usage':'past-participle','source_span':selected,'lemma':'change'}}
            with self.assertRaises(ValueError):m.verb_form_review(g,'It changed.')

    def test_to_hagiro_is_not_a_standalone_function(self):
        s=sentence('We decided to leave.');g=next(g for g in s['glosses'] if g['headword']=='to')
        target=next(g for g in s['glosses'] if g['headword']=='leave');target['kind']='lexical'
        g.update(kind='function',headword='to V',meaning_ko='~하기로',combines_with=[target['id']])
        with self.assertRaisesRegex(ValueError,'Do not split to V'):
            m.glossary(s,{},require_reading_checks=True)

    def test_to_hagiro_cannot_omit_kind_to_bypass_current_rule(self):
        s=sentence('We decided to leave.');g=next(g for g in s['glosses'] if g['headword']=='to')
        g.update(headword='to V',meaning_ko='~하기로')
        with self.assertRaisesRegex(ValueError,'Do not split to V'):
            m.glossary(s,{},require_reading_checks=True)

    def test_omitted_conjunction_matches_source_without_mutating_it(self):
        original='I think laws had to be changed.';a=original.index('laws');b=original.index('.')
        h={'span':[a,b],'display_mode':'omitted-conjunction','omitted_conjunction':'that',
            'structure_label':'명사절 접속사 that 생략','display_pairs':[
                aligned_pair('[(that) laws had to be changed]','[법이 바뀌어야 한다고]',(['that'],['이','다고']))]}
        before=deepcopy(h)
        self.assertEqual(m.omitted_conjunction_display_range(h,original),(a,b))
        self.assertEqual(h,before)

    def test_omitted_conjunction_does_not_authorize_source_rewriting(self):
        original='I think laws had to be changed.';a=original.index('laws');b=original.index('.')
        h={'span':[a,b],'display_mode':'omitted-conjunction','omitted_conjunction':'that',
            'structure_label':'명사절 접속사 that 생략','display_pairs':[
                aligned_pair('[(that) laws have to be changed]','[법이 바뀌어야 한다고]',(['that'],['이','다고']))]}
        with self.assertRaisesRegex(ValueError,'exact original excerpt'):
            m.omitted_conjunction_display_range(h,original)


if __name__=='__main__':unittest.main()
