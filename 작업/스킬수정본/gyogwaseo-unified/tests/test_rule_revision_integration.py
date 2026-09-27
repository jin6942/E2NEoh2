from copy import deepcopy
from pathlib import Path
import sys
import unittest

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'../scripts'))
from book_plan import compile_plan, passage_elements, prompt_runs, content_hash
from test_book_plan import fixture
from revision_fixtures import length_review
from export_handoff import render


def text(element):
    return ''.join(run['text'] for run in element.get('runs',[]))


class RuleRevisionIntegrationTests(unittest.TestCase):
    def test_old_unreviewed_manuscript_cannot_generate_a_new_book(self):
        data=fixture();data.pop('rule_revision')
        with self.assertRaisesRegex(ValueError,'rule_revision'):
            compile_plan(data)

    def test_paragraph_join_keeps_source_offsets_and_underlines(self):
        view={'passage':'Alpha.\n\nBeta target.', 'annotations':[{'kind':'numbered_word','number':1,'span':[13,19]}]}
        before=deepcopy(view)
        element=passage_elements(view,'mock_question_passage')[0]
        self.assertNotIn('\n',text(element))
        a,b=element['required_underlines'][0]
        self.assertEqual(text(element)[a:b],'target')
        self.assertEqual(view,before)

    def test_long_passage_keeps_paragraphs_and_numbered_words(self):
        view={'passage':'Alpha.\n\nBeta target.', 'annotations':[{'kind':'numbered_word','number':1,'span':[13,19]}],
              'preserve_paragraphs':True}
        paragraphs=passage_elements(view,'mock_question_passage')
        self.assertEqual(len(paragraphs),2)
        self.assertEqual(text(paragraphs[0]),'Alpha.')
        a,b=paragraphs[1]['required_underlines'][0]
        self.assertEqual(text(paragraphs[1])[a:b],'target')

    def test_shared_passage_printed_once_with_two_prompts(self):
        data=fixture();before=deepcopy(data);plan=compile_plan(data)
        self.assertEqual(data,before)
        for bid in ['mock1','mock2','mock3']:
            rows=next(b['elements'] for b in plan['blocks'] if b['id']==bid)
            self.assertEqual(sum(e['role']=='mock_question_passage' for e in rows),4)
            shared=next(e for e in rows if e.get('anchor','').startswith('passage_group/'))
            self.assertFalse(shared['page_break_before'])
            self.assertEqual(shared['role'], 'mock_question_prompt_spaced')
            self.assertIn('[4~5]',text(shared))
            self.assertEqual(sum(e.get('anchor','').startswith('question/') for e in rows),5)
            marks=[e['required_underlines'] for e in rows if 'required_underlines' in e]
            self.assertEqual(sum(len(m) for m in marks),5)

    def test_meaning_target_is_underlined_in_prompt_and_passage(self):
        data=fixture();q=next(q for q in data['assessment']['questions'] if q['id']=='mock1-2')
        q.update(type='함축 의미',target='They',question='밑줄 친 They가 의미하는 바로 가장 적절한 것은?',prompt_underlines=[[5,9]])
        req=next(r for r in data['question_sources'] if r['id']==q['id'])
        req.update(type='함축 의미',target_span=[0,4],length_review=length_review('함축 의미'))
        plan=compile_plan(data)
        rows=next(b['elements'] for b in plan['blocks'] if b['id']=='mock1')
        at=next(i for i,e in enumerate(rows) if e.get('anchor')=='question/mock1-2')
        for element in rows[at:at+2]:
            a,b=element['required_underlines'][0]
            self.assertEqual(text(element)[a:b],'They')

    def test_cover_and_word_answer_grid_preserve_all_content(self):
        data=fixture();data['metadata']['course']='영어II';data['assessment']['scope']={'kind':'custom','instruction':'Synthetic count fixture','reference_grade':2}
        for req in data['question_sources']:
            kind='long41_42' if any(q['id']==req['id'] and q.get('passage_group_id') for q in data['assessment']['questions']) else req['type']
            req['length_review']=length_review(kind,2)
        plan=compile_plan(data);cover=plan['blocks'][0]['elements']
        self.assertIn('영어2',[text(e) for e in cover])
        self.assertIn('혼공교재 독해편',[text(e) for e in cover])
        self.assertFalse(any(e['role']=='cover_student_name' for e in cover))
        box=next(e for e in cover if e['role']=='cover_topic_box')
        self.assertEqual(box['entries'],['Shared Layout Test Synthetic Data Only',data['cover']['topic_ko']])
        answers=next(b['elements'] for b in plan['blocks'] if b['id']=='u1/answers')
        grids=[e for e in answers if e['role']=='workbook_answer_grid']
        self.assertEqual([len(g['entries']) for g in grids],[1,9])
        self.assertEqual(text(grids[0]['entries'][0]),'1. 고치다')

    def test_word_observed_question_page_break_drops_extra_top_spacing(self):
        data=fixture();data['layout_adjustments']=[{'kind':'question_page_break','block_id':'mock1',
            'before_anchor':'question/mock1-3','content_sha256':content_hash(data),'renderer':'Microsoft Word',
            'observed_page':7,'reason':'Synthetic observation record for adapter test only.'}]
        plan=compile_plan(data)
        q=next(e for b in plan['blocks'] for e in b['elements'] if e.get('anchor')=='question/mock1-3')
        self.assertTrue(q['page_break_before']);self.assertEqual(q['role'],'mock_question_prompt')
        data['layout_adjustments'][0]['before_anchor']='question/mock1-4'
        with self.assertRaisesRegex(ValueError,'shared-passage group'):
            compile_plan(data)

    def test_explicit_word_observed_shared_passage_page_break_still_overrides_default_flow(self):
        data=fixture();data['layout_adjustments']=[{'kind':'question_page_break','block_id':'mock1',
            'before_anchor':'passage_group/mock1-long','content_sha256':content_hash(data),'renderer':'Microsoft Word',
            'observed_page':7,'reason':'Synthetic reviewed page override; not an automatic shared-passage break.'}]
        plan=compile_plan(data)
        shared=next(e for b in plan['blocks'] for e in b['elements']
                    if e.get('anchor')=='passage_group/mock1-long')
        self.assertTrue(shared['page_break_before'])
        self.assertEqual(shared['role'],'mock_question_prompt')

    def test_handoff_contains_one_complete_shared_passage_and_child_links(self):
        output=render(fixture())['assessment']
        self.assertEqual(output.count('[PASSAGE_GROUP mock1-long]'),1)
        self.assertEqual(output.count('PASSAGE_GROUP:\nmock1-long'),2)
        self.assertIn('| 번호 | 뜻 | 번호 | 뜻 | 번호 | 뜻 |',output)

    def test_mock_subtitle_keeps_both_title_parts_and_accepts_optional_second(self):
        data=fixture()
        for expected in ['Shared Layout Test Synthetic Data Only · 5문항','Shared Layout Test · 5문항']:
            plan=compile_plan(data)
            subtitles=[text(e) for b in plan['blocks'] for e in b['elements'] if e['role']=='mock_subtitle']
            self.assertEqual(subtitles,[expected]*3)
            data['cover'].pop('topic_second',None)

    def test_gloss_star_stays_attached_to_following_word(self):
        plan=compile_plan(fixture())
        glosses=[text(e) for b in plan['blocks'] for e in b['elements'] if e['role']=='gloss']
        self.assertTrue(any('★\u00a0' in value for value in glosses))
        self.assertFalse(any('★ ' in value for value in glosses))

    def test_explanation_and_key_answer_chains_end_at_requested_boundaries(self):
        plan=compile_plan(fixture())
        rows=next(b['elements'] for b in plan['blocks'] if b['id']=='u1/answers')
        explanation=next(e for e in rows if e['role']=='question_explanation')
        self.assertIs(explanation['chain'],False)
        translations=[e for e in rows if e['role'] in {'choice_translation','correct_choice_translation'}]
        self.assertEqual([e['chain'] for e in translations],[True,True,True,True,False])
        keys=[e for e in rows if e['role']=='workbook_key_answer']
        self.assertEqual([e['chain'] for e in keys],[True,False])

    def test_continuation_can_precede_key_activity_heading(self):
        data=fixture()
        data['layout_adjustments']=[{'block_id':'u1/workbook','before_anchor':'key/heading',
            'content_sha256':content_hash(data),'renderer':'Microsoft Word','observed_page':8,
            'reason':'Synthetic anchor regression, not a real page approval.'}]
        rows=next(b['elements'] for b in compile_plan(data)['blocks'] if b['id']=='u1/workbook')
        index=next(i for i,e in enumerate(rows) if e.get('anchor')=='key/heading')
        self.assertEqual(rows[index-1]['role'],'workbook_continuation')

    def test_normal_and_shared_handoff_passages_use_plain_spaces(self):
        data=fixture()
        vocab=deepcopy(next(q for q in data['assessment']['questions'] if q['id']=='mock1-5'))
        vocab.update(id='mock1-2',number=2);vocab.pop('passage_group_id')
        vocab['question']=vocab['question'].replace('mock1-5','mock1-2')
        vocab['passage']=vocab['passage'].replace('Changed','Altered')
        for name in ['questions','explanations','quick_key']:
            rows=data['assessment'][name]
            owner=deepcopy(next(q for q in rows if q['id']=='mock1-5'))
            owner.update(id='mock1-2',number=2)
            rows[rows.index(next(q for q in rows if q['id']=='mock1-2'))]=vocab if name=='questions' else owner
        request=deepcopy(next(q for q in data['question_sources'] if q['id']=='mock1-5'))
        request.update(id='mock1-2',replacement='Altered',length_review=length_review('어휘'))
        data['question_sources']=[request if q['id']=='mock1-2' else q for q in data['question_sources']]
        before=deepcopy(data)
        plan=compile_plan(data)
        self.assertTrue(any('①\u00a0' in text(e) for b in plan['blocks'] for e in b['elements']))
        output=render(data)['assessment']
        self.assertNotIn('\u00a0',output)
        self.assertIn('① ',output)
        self.assertEqual(data,before)


if __name__=='__main__':unittest.main()
