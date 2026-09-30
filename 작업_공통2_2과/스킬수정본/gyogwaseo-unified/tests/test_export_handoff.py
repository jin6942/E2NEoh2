from copy import deepcopy
from pathlib import Path
import sys
import unittest
import uuid

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'../scripts'))
from export_handoff import render,save,sha
from book_plan import compile_plan
from test_book_plan import fixture,hint_fixture,paired_hint_fixture
from test_learning_content import modal_hint_fixture, noun_phrase_fixture


class HandoffTests(unittest.TestCase):
    def test_noun_phrase_answer_has_no_sv_row_or_replacement_label_in_handoff(self):
        data = noun_phrase_fixture(); data['cover'] = fixture()['cover']
        before = deepcopy(data); output = render(data, 'learning')['learning']
        answer = output.split('----- [문장 2] -----', 1)[1].split('----- [/문장 2] -----', 1)[0]
        self.assertIn('[원문]\n' + data['sentences'][1]['text'], answer)
        self.assertIn('[각주]', answer)
        self.assertIn('[자연 해석]', answer)
        self.assertNotIn('[S/V]', answer)
        self.assertNotIn('noun-phrase-answer', output)
        self.assertNotIn(data['sentences'][1]['sv_review']['reason'], output)
        self.assertEqual(output.count('[S/V]'), 2)
        self.assertIn('[S/V] S: What, V: emerged', output)
        self.assertIn('[S/V] S: I, V: protect', output)
        self.assertEqual(data, before)

    def test_easy_explanation_keeps_all_sentences_in_plan_and_handoff(self):
        for count in [1, 4]:
            with self.subTest(count=count):
                data = fixture()
                lines = [f'서로 구별되는 시험 설명 {i}이다.' for i in range(count)]
                data['units'][0]['analysis']['easy_explanations'][0]['explanatory_sentences'] = lines
                before = deepcopy(data)
                plan = compile_plan(data)
                row = next(e for b in plan['blocks'] for e in b['elements']
                           if e['role'] == 'analysis_easy_explanation')
                self.assertEqual(''.join(r['text'] for r in row['runs']), '↳  ' + ' '.join(lines))
                output = render(data)['learning']
                for line in lines:
                    self.assertEqual(output.count(line), 1)
                self.assertEqual(data, before)

    def test_key_sentence_heading_leads_directly_to_first_question(self):
        data=fixture(); output=render(data)['assessment']
        unit=data['units'][0]
        first_id=unit['workbook']['key_sentence_ids'][0]
        first=next(row for row in data['sentences'] if row['id']==first_id)
        heading='[4. 핵심 문장 2개 다시 해석하기]'
        self.assertIn(heading+'\n1. '+first['text'],output)
        self.assertNotIn('우리말로 다시 해석하세요.',output)

    def test_zero_relations_omit_only_workbook_second_activity_and_its_empty_answer_table(self):
        data=fixture(); previous=render(data)['assessment']; unit=data['units'][0]
        unit['analysis']['relations']=[]
        unit['workbook']['relation_order']=[]
        unit['quantity_exceptions']=[{'field':'relations','actual':0,'expected':3,
            'reason':'시험용 원문 근거 부족','reported_to_user':'시험용 0세트 보고'}]
        next(q for q in data['assessment']['questions'] if q['id']==unit['workbook']['question_id'])['learned_relation_uses']=[]
        before=deepcopy(data); output=render(data)['assessment']
        student_start=previous.index('[2. 유의어·반의어 뜻 쓰기]')
        student_end=previous.index('[3. 실전문제]',student_start)
        answer_start=previous.index('[2. 유의어·반의어 뜻 쓰기]',student_end)
        answer_end=previous.index('[4. 핵심 문장 해석]',answer_start)
        expected=previous[:student_start]+previous[student_end:answer_start]+previous[answer_end:]
        self.assertEqual(output,expected)
        self.assertNotIn('[2. 유의어·반의어 뜻 쓰기]',output)
        self.assertEqual(output.count('우리말 뜻을 쓰세요.'),1)
        self.assertEqual(output.count('| 번호 | 뜻 | 번호 | 뜻 | 번호 | 뜻 |'),1)
        self.assertIn('[1. 오늘의 낱말]',output)
        self.assertIn('[3. 실전문제]',output)
        self.assertIn('[4. 핵심 문장 2개 다시 해석하기]',output)
        plan=compile_plan(data)
        workbook=next(b for b in plan['blocks'] if b['id']=='u1/workbook')
        self.assertNotIn('workbook_relations_heading',[e['role'] for e in workbook['elements']])
        self.assertEqual(data,before)

    def test_one_reported_relation_set_keeps_second_activity_and_answer_table(self):
        data=fixture(); unit=data['units'][0]
        unit['analysis']['relations']=unit['analysis']['relations'][:1]
        terms={t['id']:t for t in unit['analysis']['relations'][0].values()}
        unit['workbook']['relation_order']=[x for x in unit['workbook']['relation_order'] if x in terms]
        unit['quantity_exceptions']=[{'field':'relations','actual':1,'expected':3,
            'reason':'시험용 한 세트만 근거 존재','reported_to_user':'시험용 1세트 보고'}]
        output=render(data)['assessment']
        rows=[terms[x] for x in unit['workbook']['relation_order']]
        activity='[2. 유의어·반의어 뜻 쓰기]\n우리말 뜻을 쓰세요.\n'
        activity+='\n'.join(f'{i}. '+r['text'] for i,r in enumerate(rows,1))+'\n[3. 실전문제]'
        self.assertIn(activity,output)
        cells=[]
        for i,row in enumerate(rows,1):
            cells.extend([str(i),row['meaning_ko']])
        answers=('[2. 유의어·반의어 뜻 쓰기]\n| 번호 | 뜻 | 번호 | 뜻 | 번호 | 뜻 |\n'
                 '| --- | --- | --- | --- | --- | --- |\n| '+' | '.join(cells)+' |\n[4. 핵심 문장 해석]')
        self.assertIn(answers,output)

    def test_modal_perfect_verb_only_matches_in_handoff_and_book_output(self):
        data=modal_hint_fixture()
        data['cover']=fixture()['cover']
        data['sources'][0]['label']='시험용 본문'
        out=render(data,'learning')['learning']; plan=compile_plan(data,'learning')
        row=next(e for b in plan['blocks'] for e in b['elements'] if e['role']=='structure_hint')
        body=''.join(r['text'] for r in row['runs']).removeprefix('구조 힌트   ')
        self.assertEqual(body,'may have provided → 제공했을지도 모른다 (may have p.p.)')
        self.assertIn('[구조 힌트] '+body+'\n',out)
        self.assertEqual(body.count('p.p.'),1)
        self.assertNotIn('A with B',body)
        # The separate glossary still keeps the full verb-construction help.
        self.assertIn('provided A with B',out)

    def test_paired_hint_handoff_matches_docx_mapping_without_label_or_evidence(self):
        d = paired_hint_fixture(); out = render(d, 'learning')['learning']; plan = compile_plan(d, 'learning')
        row = next(e for b in plan['blocks'] for e in b['elements'] if e['role'] == 'structure_hint')
        body = ''.join(r['text'] for r in row['runs']).removeprefix('구조 힌트   ')
        self.assertEqual(body, 'They repair … useful tools → 그들은 고친다 … 유용한 도구')
        self.assertIn('[구조 힌트] '+body+'\n', out)
        self.assertNotIn('검수 전용', out)
        self.assertNotIn('structure_label', out)

    def test_hint_handoff_and_docx_use_the_same_display_pairs(self):
        d=hint_fixture();out=render(d,'learning')['learning'];plan=compile_plan(d,'learning')
        row=next(e for b in plan['blocks'] for e in b['elements'] if e['role']=='structure_hint')
        body=''.join(r['text'] for r in row['runs']).removeprefix('구조 힌트   ')
        self.assertIn('[구조 힌트] '+body,out)
        self.assertNotIn('검수 전용',out)

    def test_handoff_never_falls_back_to_legacy_parenthesized_hint(self):
        d=hint_fixture();d.pop('rule_revision')
        d['sentences'][0]['hints'][0].pop('display_pairs')
        with self.assertRaisesRegex(ValueError,'display_pairs'):
            render(d,'learning')

    def test_qc_exports_keep_all_questions_once_and_no_workbook_duplicate(self):
        d=fixture();out=render(d)
        for q in d['assessment']['questions']:
            self.assertEqual(out['assessment'].count('['+q['id']+']'),1)
        self.assertEqual(out['learning'].count('[자연 해석]'),len(d['sentences']))
        self.assertNotIn('[직역]',out['learning'])
        self.assertNotIn('[S/V]',out['assessment'])

    def test_edited_natural_translation_reaches_both_corresponding_outputs(self):
        d=fixture();d['sentences'][0]['natural_ko']='바뀐 해석이 두 자료에서 같아야 한다.'
        out=render(d)
        self.assertIn(d['sentences'][0]['natural_ko'],out['learning'])
        self.assertIn(d['sentences'][0]['natural_ko'],out['assessment'])

    def test_learning_phase_does_not_require_finished_assessment(self):
        d=fixture();del d['assessment'];del d['question_sources']
        del d['units'][0]['workbook']
        out=render(d,'learning')
        self.assertIn('===== [/지문] =====',out['learning'])

    def test_original_heading_and_source_location_survive_handoff(self):
        d=fixture();out=render(d,'learning')['learning']
        h=d['sources'][0]['subheadings'][0]
        self.assertIn('[원문 소제목] '+h['text'],out)
        self.assertIn(h['location'],out)
        self.assertIn(h['artifact_sha256'],out)
        self.assertIn('[주제] '+d['units'][0]['analysis']['title_or_topic_en'],out)

    def test_display_lesson_is_distinct_from_internal_id(self):
        d=fixture();d['metadata']['lesson']='UNIT03';d['cover']['lesson_number']='03'
        out=render(d,'learning')['learning']
        self.assertIn('[UNIT] UNIT03',out)
        self.assertIn('[학생용 과 표시] 3과',out)

    def test_flow_stage_labels_survive_in_both_docx_plan_and_full_handoff(self):
        d=fixture()
        d['units'][0]['analysis']['flow']=[
            {'sentence_ids':['s1'],'label':'도입','text_ko':'첫 단계의 설명'},
            {'sentence_ids':['s2','s3'],'label':'결론','text_ko':'마지막 단계의 설명'}]
        out=render(d)['learning']
        plan=compile_plan(d)
        rows=[e for b in plan['blocks'] for e in b['elements'] if e['role']=='analysis_flow_item']
        self.assertEqual([e['runs'][0]['text'] for e in rows],['(도입)  ','(결론)  '])
        flow=out.split('[글의 흐름]\n',1)[1].split('[각 문장 쉬운 풀이]',1)[0]
        self.assertTrue(flow.splitlines()[0].startswith('(도입) '))
        self.assertTrue(flow.splitlines()[1].startswith('(결론) '))
        self.assertIn('첫 단계의 설명',flow)
        self.assertIn('마지막 단계의 설명',flow)

    def test_absent_flow_stage_label_keeps_shared_legacy_default(self):
        d=fixture();out=render(d,'learning')['learning'];plan=compile_plan(d,'learning')
        self.assertNotIn('label',d['units'][0]['analysis']['flow'][0])
        row=next(e for b in plan['blocks'] for e in b['elements'] if e['role']=='analysis_flow_item')
        self.assertEqual(row['runs'][0]['text'],'(흐름)  ')
        self.assertIn('[글의 흐름]\n(흐름) ',out)

    def test_stale_update_does_not_overwrite_reviewers_txt(self):
        folder=HERE/('handoff-test-'+uuid.uuid4().hex);folder.mkdir()
        path=folder/'QC_HANDOFF.txt'
        try:
            save(path,'검수자가 고친 내용\n',None)
            with self.assertRaises(ValueError):save(path,'옛 원고\n','0'*64)
            self.assertEqual(path.read_text(encoding='utf-8'),'검수자가 고친 내용\n')
            save(path,'현재 원고\n',sha(path.read_bytes()))
            self.assertEqual(path.read_text(encoding='utf-8'),'현재 원고\n')
        finally:
            for created in folder.iterdir():
                if created.is_file():
                    created.unlink()
            folder.rmdir()


if __name__=='__main__':unittest.main()
