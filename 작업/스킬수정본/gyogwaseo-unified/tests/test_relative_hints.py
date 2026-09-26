"""Declared relative-marker coverage only; no automatic grammar classification."""
from copy import deepcopy
from pathlib import Path
import sys
import unittest

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'../scripts'))
import check_learning_content as m
from test_learning_content import fixture, aligned_pair, absent_marker_pair
from structure_hints import display_pairs, omitted_relative_source_text


def relative_fixture(subject_relative=False):
    original=('They have abilities that help them survive.' if subject_relative else
              'These are areas where changes happen.')
    data=fixture([original,'We save valuable materials.','I protect local resources.'])
    for sentence in data['sentences']:
        sentence['reading_checks']['relative_gloss_ids']=[]
    s=data['sentences'][0]
    marker='that' if subject_relative else 'where'
    marker_start=original.index(marker)
    gloss=next(g for g in s['glosses'] if g['headword']==marker)
    s['reading_checks']['relative_gloss_ids']=[gloss['id']]
    if subject_relative:
        s['clauses'].append({'kind':'subject_relative','start':marker_start,'marker':marker,
            'subject_spans':[],'verb_spans':[[original.index('help'),original.index('help')+4]]})
        english='abilities [that help them survive]'; korean='[그들이 살아남도록 돕는] 능력들'
        head_start=original.index('abilities')
    else:
        s['clauses'].append({'kind':'subordinate','start':marker_start,'marker':marker,
            'subject_spans':[[original.index('changes'),original.index('changes')+7]],
            'verb_spans':[[original.index('happen'),original.index('happen')+6]]})
        english='areas [where changes happen]'; korean='[변화가 일어나는] 분야들'
        head_start=original.index('areas')
    s['hints']=[{'span':[head_start,len(original)-1], 'meaning_ko':'검토된 관계사 연결',
        'explanation':'시험용 명시적 관계사 선언이며 기계의 문법 추론이 아님',
        'structure_label':'관계사 연결','display_pairs':[aligned_pair(english,korean,
            ([marker],['는']))]}]
    return data


def omitted_relative_fixture(marker='that'):
    original = 'They repair tools we use.'
    data = fixture([original, 'We save valuable materials.', 'I protect local resources.'])
    sentence = data['sentences'][0]
    sentence['hints'] = [{
        'span': [original.index('tools'), len(original) - 1],
        'meaning_ko': '우리가 쓰는 도구', 'explanation': '검토된 목적격 관계사 생략 위치',
        'display_mode': 'omitted-relative', 'omitted_relative': marker,
        'structure_label': f'목적격 관계대명사 {marker} 생략',
        'display_pairs': [aligned_pair(f'tools [({marker}) we use]', '[우리가 쓰는] 도구',
                                      ([marker], ['는']))],
    }]
    return data


class RelativeHintTests(unittest.TestCase):
    def test_omitted_relative_matches_exact_source_without_mutating_source_or_sv(self):
        data = omitted_relative_fixture(); before = deepcopy(data)
        self.assertEqual(m.check(data, scope='learning')['status'], 'STRUCTURE_PASS')
        self.assertEqual(data, before)
        hint = data['sentences'][0]['hints'][0]
        self.assertEqual(omitted_relative_source_text(hint), 'tools we use')
        self.assertEqual(m.omitted_relative_display_range(hint, data['sentences'][0]['text']),
                         (12, len(data['sentences'][0]['text']) - 1))

    def test_omitted_relative_choices_are_explicit_not_grammar_inference(self):
        # Shape validation accepts the declared spellings. Which is valid
        # for the actual antecedent remains an independent language-review task.
        for marker in ['that', 'which', 'who', 'whom', 'when', 'where', 'why']:
            hint = omitted_relative_fixture(marker)['sentences'][0]['hints'][0]
            self.assertEqual(omitted_relative_source_text(hint), 'tools we use')
        for marker in ['because', 'That', '', None, [], 'which is']:
            hint = omitted_relative_fixture()['sentences'][0]['hints'][0]
            hint['omitted_relative'] = marker
            with self.subTest(marker=marker), self.assertRaises(ValueError):
                display_pairs(hint, require_alignment=True)

    def test_current_omitted_relative_cannot_use_old_empty_link_exception(self):
        hint = omitted_relative_fixture()['sentences'][0]['hints'][0]
        hint.pop('display_mode'); hint.pop('omitted_relative')
        hint['display_pairs'] = [absent_marker_pair('tools [we use]', '[우리가 쓰는] 도구',
                                                  '생략된 관계사가 원문에 없음')]
        with self.assertRaisesRegex(ValueError, 'omitted-relative mode'):
            display_pairs(hint, require_alignment=True)
        # Older unannotated data remains readable, without certifying current rules.
        self.assertEqual(display_pairs(hint), hint['display_pairs'])

    def test_omitted_relative_rejects_unlicensed_or_misplaced_supplements(self):
        baseline = omitted_relative_fixture()['sentences'][0]['hints'][0]
        edits = [
            {'display_mode': 'split-phrasal-verb'}, {'display_mode': None},
            {'structure_label': '접속사 that 생략'}, {'structure_label': '관계대명사'},
            {'category': 'paired-structure'}, {'category': 'function-combination'},
        ]
        for update in edits:
            with self.subTest(update=update), self.assertRaises(ValueError):
                display_pairs({**deepcopy(baseline), **update}, require_alignment=True)
        for english in ['tools (that) [we use]', 'tools [we (that) use]',
                        'tools [(that) (that) we use]', 'tools [(that) (which) we use]',
                        'tools [( that ) we use]', 'tools [(that)]']:
            hint = deepcopy(baseline)
            hint['display_pairs'] = [aligned_pair(english, '[우리가 쓰는] 도구', (['that'], ['는']))]
            with self.subTest(english=english), self.assertRaises(ValueError):
                display_pairs(hint, require_alignment=True)
        hint = deepcopy(baseline); hint.pop('display_mode'); hint.pop('omitted_relative')
        hint['structure_label'] = '원문 연결'
        with self.assertRaisesRegex(ValueError, 'parenthetical relative'):
            display_pairs(hint)

    def test_omitted_relative_cannot_omit_or_expand_its_english_marker_link(self):
        baseline = omitted_relative_fixture()['sentences'][0]['hints'][0]
        for selected in ['we', 'that) we']:
            hint = deepcopy(baseline)
            hint['display_pairs'] = [aligned_pair('tools [(that) we use]', '[우리가 쓰는] 도구',
                                                   ([selected], ['는']))]
            with self.subTest(selected=selected), self.assertRaises(ValueError):
                display_pairs(hint, require_alignment=True)
        hint = deepcopy(baseline)
        hint['display_pairs'][0].update(emphasis_links=[], emphasis_note='원문에는 관계사가 생략됨')
        with self.assertRaisesRegex(ValueError, 'supplied marker'):
            display_pairs(hint, require_alignment=True)
        hint = deepcopy(baseline); hint['display_pairs'] *= 2
        with self.assertRaisesRegex(ValueError, 'exactly one'):
            display_pairs(hint, require_alignment=True)

    def test_omitted_relative_rejects_vague_or_unrelated_korean_links(self):
        baseline = omitted_relative_fixture()['sentences'][0]['hints'][0]
        for selected in ['우리가 쓰는', '도구']:
            hint = deepcopy(baseline)
            hint['display_pairs'] = [aligned_pair('tools [(that) we use]', '[우리가 쓰는] 도구',
                                                   (['that'], [selected]))]
            with self.subTest(selected=selected), self.assertRaisesRegex(ValueError, 'grammatical range'):
                display_pairs(hint, require_alignment=True)
        # Stem/ending-fused syllables are valid minimal surface displays.
        for korean, ending in [('[우리가 쓴] 도구', '쓴'), ('[우리가 쓸] 도구', '쓸'),
                               ('[문어가 잃었던] 팔', '던'), ('[이미 된] 일', '된')]:
            hint = deepcopy(baseline)
            hint['display_pairs'] = [aligned_pair('tools [(that) we use]', korean,
                                                   (['that'], [ending]))]
            display_pairs(hint, require_alignment=True)

    def test_relative_adverb_korean_correspondence_has_no_pronoun_ending_whitelist(self):
        hint = omitted_relative_fixture('when')['sentences'][0]['hints'][0]
        hint['structure_label'] = '관계부사 when 생략'
        hint['display_pairs'] = [aligned_pair('the time [(when) we met]', '[우리가 만났던 때]',
                                              (['when'], ['때']))]
        display_pairs(hint, require_alignment=True)

    def test_omitted_relative_does_not_license_changed_or_inserted_source_words(self):
        for english in ['tools [(that) we used]', 'tools [(that) we can use]',
                        'tool [(that) we use]', 'tools [(that) I use]',
                        'tools [(that) that we use]']:
            data = omitted_relative_fixture(); before = deepcopy(data)
            hint = data['sentences'][0]['hints'][0]
            hint['display_pairs'] = [aligned_pair(english, '[우리가 쓰는] 도구', (['that'], ['는']))]
            with self.subTest(english=english), self.assertRaisesRegex(ValueError, 'exact original excerpt'):
                m.check(data, scope='learning')
            for field in ['sources', 'paragraphs', 'units']:
                self.assertEqual(data[field], before[field])
            for field in ['text', 'chunks', 'clauses']:
                self.assertEqual(data['sentences'][0][field], before['sentences'][0][field])

    def test_declared_where_requires_a_general_hint(self):
        data=relative_fixture();data['sentences'][0].pop('hints')
        with self.assertRaisesRegex(ValueError,'Relative marker.*general structure hint display'):
            m.check(data,scope='learning')

    def test_valid_relative_display_preserves_data_and_reports_declared_scope(self):
        data=relative_fixture();before=deepcopy(data)
        result=m.check(data,scope='learning')
        self.assertEqual(result['status'],'STRUCTURE_PASS')
        report=result['relative_hint_declarations']
        self.assertEqual(report['status'],'DECLARED_LOCATIONS_CHECKED')
        self.assertEqual(report['declared_sentence_count'],3)
        self.assertEqual(report['undeclared_sentences'],[])
        self.assertIn('NOT_GRAMMAR_INFERENCE',report['scope'])
        self.assertEqual(data,before)

    def test_large_internal_span_does_not_cover_an_omitted_or_rewritten_display_marker(self):
        for english,korean in [('These [are areas]','이것들은 [분야들이다]'),
                               ('areas [changes happen]','[변화가 일어나는] 분야들'),
                               ('areas [where changes occur]','[변화가 일어나는] 분야들')]:
            data=relative_fixture();s=data['sentences'][0];hint=s['hints'][0]
            hint['span']=[0,len(s['text'])]
            hint['display_pairs']=[aligned_pair(english,korean,(['where'],['는']))
                if 'where' in english else absent_marker_pair(english,korean,
                    '변조 시험: 관계사가 빠져 대응되는 영어 표면형이 없다.')]
            with self.subTest(english=english),self.assertRaisesRegex(ValueError,'Relative marker'):
                m.check(data,scope='learning')

    def test_indirect_question_where_is_not_classified_by_spelling(self):
        original='They wonder where the items go.'
        data=fixture([original,'We save valuable materials.','I protect local resources.'])
        for s in data['sentences']:
            s['reading_checks']['relative_gloss_ids']=[]
        s=data['sentences'][0]
        s['clauses'].append({'kind':'subordinate','start':original.index('where'),'marker':'where',
            'subject_spans':[[original.index('the items'),original.index('the items')+9]],
            'verb_spans':[[original.index('go'),original.index('go')+2]]})
        # Prose labels are not a machine grammar classifier, either.
        next(g for g in s['glosses'] if g['headword']=='where')['meaning_ko']='관계부사와 구별할 간접의문 표현'
        self.assertEqual(m.check(data,scope='learning')['status'],'STRUCTURE_PASS')
        self.assertNotIn('hints',s)

    def test_reviewed_subject_relative_cannot_be_hidden_by_an_empty_gloss_list(self):
        data=relative_fixture(subject_relative=True)
        data['sentences'][0]['reading_checks']['relative_gloss_ids']=[]
        self.assertEqual(m.check(data,scope='learning')['status'],'STRUCTURE_PASS')
        data['sentences'][0].pop('hints')
        with self.assertRaisesRegex(ValueError,'Relative marker'):
            m.check(data,scope='learning')

    def test_relative_gloss_ids_reject_bad_types_duplicates_and_unknown_ids(self):
        for value in [None,{},'',True,[1],[''],[' g1-3 '],['g1-3','g1-3'],['missing']]:
            data=relative_fixture();data['sentences'][0]['reading_checks']['relative_gloss_ids']=value
            with self.subTest(value=value),self.assertRaisesRegex(ValueError,'relative_gloss_ids'):
                m.check(data,scope='learning')

    def test_undeclared_legacy_relatives_remain_compatible_without_claiming_new_check(self):
        data=relative_fixture(subject_relative=True)
        data['sentences'][0].pop('hints')
        for s in data['sentences']:
            s['reading_checks'].pop('relative_gloss_ids')
        before=deepcopy(data);result=m.check(data,scope='learning')
        self.assertEqual(result['status'],'STRUCTURE_PASS')
        self.assertEqual(result['relative_hint_declarations']['status'],'UNDECLARED_LEGACY_INPUT')
        self.assertEqual(result['relative_hint_declarations']['undeclared_sentences'],['src/s1','src/s2','src/s3'])
        self.assertEqual(data,before)
        data['sentences'][1]['reading_checks']['relative_gloss_ids']=[]
        self.assertEqual(m.check(data,scope='learning')['relative_hint_declarations']['status'],'PARTIALLY_DECLARED')

    def test_paired_or_function_category_cannot_replace_a_general_relative_hint(self):
        data=relative_fixture();s=data['sentences'][0];hint=s['hints'][0]
        start=s['text'].index('where');end=start+len('where')
        hint.pop('structure_label');hint.update(category='paired-structure',display_spans=[[start,end]])
        hint['display_pairs']=[aligned_pair('where','그곳',(['where'],['그곳']))]
        with self.assertRaisesRegex(ValueError,'Relative marker'):
            m.check(data,scope='learning')
        # The coverage helper also explicitly excludes function-combination
        # records; display-shape validity is enforced separately by glossary().
        hint['category']='function-combination'
        glosses={g['id']:g for g in s['glosses']}
        with self.assertRaisesRegex(ValueError,'Relative marker'):
            m.relative_hint_coverage(s,glosses)

    def test_subject_relative_source_start_is_not_guessed_from_another_occurrence(self):
        data=relative_fixture(subject_relative=True)
        data['sentences'][0]['clauses'][-1]['start']+=1
        with self.assertRaisesRegex(ValueError,'subject_relative marker.*exact source start'):
            m.check(data,scope='learning')


if __name__=='__main__':
    unittest.main()
