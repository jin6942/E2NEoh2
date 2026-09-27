from copy import deepcopy
import json
from pathlib import Path
import sys
import unittest
import uuid
from zipfile import ZipFile
from lxml import etree as E

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'../scripts'))
from book_plan import compile_plan,passage_runs,p,content_hash,structure_hint_element
from master_docx import RoleBank,write,NS
from check_saved_docx import check
from test_book import fixture as book_fixture
from test_learning_content import absent_marker_pair


def fixture():
    data=book_fixture()
    data['sources'][0]['label']='시험용 본문'
    data['cover']={'lesson_label':'LESSON','lesson_number':'00','topic_first':'Shared Layout Test',
                   'topic_second':'Synthetic Data Only','topic_ko':'자동 연결 시험 · 학습용 자료 아님'}
    data['set_labels']={f'mock{x}':f'미니 모의고사 {x}회' for x in range(1,4)}
    return data


def hint_fixture():
    data=fixture()
    data['sentences'][0]['hints']=[{'span':[12,24], 'meaning_ko':'검수 전용 뜻',
        'explanation':'검수 전용 문법 설명',
        'structure_label':'형용사 수식',
        'display_pairs':[absent_marker_pair('[useful] tools','[유용한] 도구',
            '합성 형용사 수식 시험: 한국어 관형형 어미에 대응되는 독립 영어 문법 표면형이 없다.')]}]
    return data


def paired_hint_fixture():
    # Synthetic selection plumbing only; this does not claim a semantic pairing.
    data = fixture()
    tail = data['sentences'][0]['text'].rindex('useful tools')
    data['sentences'][0]['hints'] = [{'category': 'paired-structure', 'span': [0, tail+12],
        'meaning_ko': '검수 전용 뜻', 'explanation': '검수 전용 구조 근거',
        'display_spans': [[0, 11], [tail, tail+12]],
        'display_pairs': [absent_marker_pair('They repair … useful tools','그들은 고친다 … 유용한 도구',
            '문법 관계를 주장하지 않는 합성 범위 시험으로 대응되는 문법 표면형이 없다.')]}]
    return data


class BookPlanTests(unittest.TestCase):
    def test_evidence_heading_is_separate_and_preserves_all_evidence_text(self):
        data = fixture(); before = deepcopy(data); plan = compile_plan(data)
        headings, evidence = [], []
        for block in plan['blocks']:
            for index, row in enumerate(block['elements']):
                if row['role'] == 'question_evidence':
                    heading = block['elements'][index-1]
                    headings.append(heading)
                    evidence.append(''.join(run['text'] for run in row['runs']))
                    self.assertEqual(heading['role'], 'choice_translation_heading')
                    self.assertEqual(''.join(run['text'] for run in heading['runs']), '정답 근거')
        self.assertEqual(len(headings), len(data['assessment']['explanations']))
        self.assertCountEqual(evidence, [row['evidence'] for row in data['assessment']['explanations']])
        self.assertEqual(data, before)

    def test_saved_evidence_heading_matches_peer_headings_and_shared_passage_can_flow(self):
        plan = compile_plan(fixture())
        folder = HERE/('book-plan-test-'+uuid.uuid4().hex); folder.mkdir()
        dest = folder/'evidence-pagination.docx'; write(plan, dest)
        self.assertEqual(check(plan, dest)['status'], 'SAVED_CONTENT_MATCH')
        with ZipFile(dest) as z:
            doc = E.fromstring(z.read('word/document.xml'))
        paragraphs = doc.findall('.//w:p', NS)
        value = lambda p: ''.join(p.xpath('.//w:t/text()', namespaces=NS))
        props = lambda node: [(n.tag, sorted(n.attrib.items())) for n in node.iter()]
        headings = {title: next(p for p in paragraphs if value(p) == title)
                    for title in ['정답 근거', '선지 해석', '오답 정리']}
        for heading in headings.values():
            self.assertEqual(heading.find('w:r/w:rPr/w:sz', NS).get('{'+NS['w']+'}val'), '17')
            for path in ['w:pPr', 'w:r/w:rPr']:
                self.assertEqual(props(heading.find(path, NS)), props(headings['선지 해석'].find(path, NS)))
        shared = [(i, p) for i, p in enumerate(paragraphs) if value(p).startswith('[4~5]')]
        self.assertEqual(len(shared), 3)
        for i, header in shared:
            self.assertEqual(header.find('w:pPr/w:pageBreakBefore', NS).get('{'+NS['w']+'}val'), '0')
            self.assertEqual(header.find('w:pPr/w:spacing', NS).get('{'+NS['w']+'}before'), '494')
            self.assertEqual(header.find('w:pPr/w:keepNext', NS).get('{'+NS['w']+'}val'), '1')
            self.assertEqual(paragraphs[i-1].find('w:pPr/w:keepNext', NS).get('{'+NS['w']+'}val'), '0')
            self.assertEqual(paragraphs[i+1].find('w:pPr/w:keepNext', NS).get('{'+NS['w']+'}val'), '0')

    def test_paired_selected_parts_are_bilingual_without_a_label_or_manual_linebreak(self):
        hint = {'category': 'paired-structure', 'display_spans': [[25, 37], [53, 74]],
            'meaning_ko': '검수 전용 뜻', 'explanation': '검수 전용 문법 설명',
            'display_pairs': [{'en': 'both to hide … and to secretly crawl …',
                               'ko': '숨기 위해서도 … 몰래 기어가기 위해서도 …'}]}
        element = structure_hint_element(hint)
        value = ''.join(run['text'] for run in element['runs'])
        self.assertEqual(value, '구조 힌트   both to hide … and to secretly crawl … → '
                               '숨기 위해서도 … 몰래 기어가기 위해서도 …')
        paragraph = RoleBank().paragraph('structure_hint', element['runs'])
        self.assertEqual(len(paragraph.findall('.//w:br', NS)), 0)
        self.assertNotIn('검수 전용', value)

    def test_paired_bilingual_mapping_survives_actual_saved_docx(self):
        plan = compile_plan(paired_hint_fixture(), 'learning')
        folder = HERE/('book-plan-test-'+uuid.uuid4().hex); folder.mkdir()
        dest = folder/'paired-hint.docx'; write(plan, dest)
        self.assertEqual(check(plan, dest)['status'], 'SAVED_CONTENT_MATCH')
        with ZipFile(dest) as z:
            doc = E.fromstring(z.read('word/document.xml'))
        paragraphs = doc.xpath('//w:p[contains(string(.), "구조 힌트")]', namespaces=NS)
        self.assertEqual(len(paragraphs), 1)
        self.assertEqual(''.join(paragraphs[0].xpath('.//w:t/text()', namespaces=NS)),
            '구조 힌트   They repair … useful tools → 그들은 고친다 … 유용한 도구')
        self.assertEqual(len(paragraphs[0].findall('.//w:br', NS)), 0)

    def test_structure_hint_prints_only_bilingual_pairs_with_one_label(self):
        plan=compile_plan(hint_fixture())
        rows=[e for b in plan['blocks'] for e in b['elements'] if e['role']=='structure_hint']
        self.assertEqual(len(rows),1)
        content=''.join(run['text'] for run in rows[0]['runs'])
        self.assertEqual(content,'구조 힌트   [useful] tools → [유용한] 도구 (형용사 수식)')
        self.assertNotIn('검수 전용',json.dumps(plan,ensure_ascii=False))

    def test_hint_without_overt_grammar_pair_keeps_both_brackets_plain(self):
        hint=hint_fixture()['sentences'][0]['hints'][0]
        element=structure_hint_element(hint)
        paragraph=RoleBank().paragraph('structure_hint',element['runs'])
        bold=paragraph.xpath('.//w:r[w:rPr/w:b[not(@w:val="0")]]/w:t/text()',namespaces=NS)
        normal=paragraph.xpath('.//w:r[not(w:rPr/w:b) or w:rPr/w:b[@w:val="0"]]/w:t/text()',namespaces=NS)
        self.assertEqual(bold,['구조 힌트   '])
        self.assertIn('[useful] tools',normal)
        self.assertIn('[유용한] 도구',normal)
        self.assertIn(' (형용사 수식)',normal)
        self.assertEqual(paragraph.xpath('.//w:u[not(@w:val="none")]',namespaces=NS),[])
        self.assertEqual(len(paragraph.findall('.//w:br',NS)),0)

    def test_multiple_general_pairs_remain_one_line_with_one_final_label(self):
        hint={'structure_label':'수식어와 주어 연결','display_pairs':[
            {'en':'tools [we repair]','ko':'[우리가 고치는] 도구'},
            {'en':'[tools we repair] are useful','ko':'[우리가 고치는 도구는] 유용하다'}]}
        element=structure_hint_element(hint)
        value=''.join(run['text'] for run in element['runs'])
        self.assertEqual(value,'구조 힌트   tools [we repair] → [우리가 고치는] 도구 / '
            '[tools we repair] are useful → [우리가 고치는 도구는] 유용하다 (수식어와 주어 연결)')
        self.assertNotIn('\n',value)
        paragraph=RoleBank().paragraph('structure_hint',element['runs'])
        self.assertEqual(len(paragraph.findall('.//w:br',NS)),0)

    def test_hint_lines_and_emphasis_survive_saved_docx_checks(self):
        plan=compile_plan(hint_fixture())
        folder=HERE/('book-plan-test-'+uuid.uuid4().hex);folder.mkdir()
        dest=folder/'hint.docx';write(plan,dest)
        result=check(plan,dest)
        self.assertEqual(result['status'],'SAVED_CONTENT_MATCH')

    def test_function_combination_formula_and_lexical_form_are_one_line(self):
        hint={'category':'function-combination','meaning_ko':'출력하지 않는 뜻',
            'explanation':'출력하지 않는 설명','display_pairs':[
                {'en':'can be p.p. + dug up','ko':'파내어질 수 있다'}]}
        element=structure_hint_element(hint)
        content=''.join(run['text'] for run in element['runs'])
        self.assertEqual(content,'구조 힌트   can be p.p. + dug up → 파내어질 수 있다')
        self.assertEqual(content.count('구조 힌트'),1)

    def test_multistage_function_hints_cannot_return_via_old_mixed_format(self):
        hint={'category':'function-combination','display_pairs':[
            {'en':'are located','ko':'위치해 있다'},
            {'en':'are located [in its arms]','ko':'[팔에] 위치해 있다'}]}
        with self.assertRaisesRegex(ValueError,'exactly one compact pair'):
            structure_hint_element(hint)

    def test_modal_perfect_hint_is_grouped_before_book_output(self):
        hint={'category':'function-combination','display_mode':'modal-perfect-verb',
            'display_span':[17,34],'display_pairs':[
            {'en':'may have provided','ko':'제공했을지도 모른다'}]}
        element=structure_hint_element(hint)
        self.assertEqual(''.join(run['text'] for run in element['runs']),
            '구조 힌트   may have provided → 제공했을지도 모른다')
        hint['display_pairs'][0]['en']='may + have p.p. + provided A with B'
        with self.assertRaisesRegex(ValueError,'Modal-perfect'):
            structure_hint_element(hint)

    def test_custom_two_rounds_cover_steps_match_actual_counts(self):
        d=fixture()
        d['assessment']['scope']={'kind':'custom','instruction':'사용자 지정 시험: 2회 편성'}
        removed={q['id'] for q in d['assessment']['plan'] if q['set_id']=='mock3'}
        for key in ['plan','questions','quick_key','explanations']:
            d['assessment'][key]=[q for q in d['assessment'][key] if q['id'] not in removed]
        d['question_sources']=[q for q in d['question_sources'] if q['id'] not in removed]
        d['assessment']['passage_groups']=[g for g in d['assessment']['passage_groups'] if g['set_id']!='mock3']
        cover=compile_plan(d)['blocks'][0]['elements']
        content=' '.join(r['text'] for e in cover for r in e.get('runs',[]))
        self.assertIn('5문항×2회',content)
        self.assertIn('2회로 학습 마무리하기',content)
        self.assertNotIn('세 회로',content)

    def test_learning_stage_can_precede_question_authoring(self):
        d=fixture();del d['assessment'];del d['question_sources']
        plan=compile_plan(d,'learning')
        self.assertEqual([b['id'] for b in plan['blocks']],['cover','u1/reading','u1/analysis'])
        self.assertNotIn('실전문제 0문항',json.dumps(plan,ensure_ascii=False))
    def test_all_sections_in_confirmed_order(self):
        plan=compile_plan(fixture())
        self.assertEqual([b['id'] for b in plan['blocks']],['cover','u1/reading','u1/analysis','u1/workbook',
            'mock1','mock2','mock3','answers/quick','u1/answers','answers/mock1','answers/mock2','answers/mock3'])
        self.assertEqual(plan['semantic_review'],'NOT_PERFORMED')

    def test_review_line_and_no_standalone_model(self):
        plan=compile_plan(fixture())
        roles=[e['role'] for b in plan['blocks'] for e in b['elements']]
        self.assertEqual(roles.count('interpretation_review_line'),1)
        self.assertEqual(roles.count('analysis_natural_translation'),3)
        self.assertNotIn('model_translation_header',roles)

    def test_title_is_one_paragraph_with_existing_korean_format(self):
        plan=compile_plan(fixture())
        rows=plan['blocks'][1]['elements']
        self.assertEqual(sum(x['role']=='unit_topic_english' for x in rows),1)
        self.assertFalse(any(x['role']=='unit_topic_korean' for x in rows))
        title=next(x for x in rows if x['role']=='unit_topic_english')
        self.assertEqual(title['runs'][1]['format_role'],'unit_topic_korean')

    def test_workbook_has_no_gloss_or_sv(self):
        plan=compile_plan(fixture())
        roles={e['role'] for e in plan['blocks'][3]['elements']}
        self.assertFalse(roles & {'gloss','sv','structure_hint'})

    def test_saved_full_book_matches_plan(self):
        plan=compile_plan(fixture())
        folder=HERE/('book-plan-test-'+uuid.uuid4().hex)
        folder.mkdir()
        dest=folder/'test.docx'
        write(plan,dest)
        self.assertEqual(check(plan,dest)['status'],'SAVED_CONTENT_MATCH')

    def test_source_circled_numbers_preserved_with_added_marks(self):
        view={'passage':'Original ① token. Next.', 'annotations':[{'kind':'insertion_slot','number':2,'offset':18}]}
        runs=passage_runs(view)
        self.assertEqual(''.join(r['text'] for r in runs),'Original ① token. ②\u00a0Next.')

    def test_insertion_slot_spacing_at_edges_and_whitespace(self):
        for value,offset,expected in [('Next.',0,'①\u00a0Next.'),('A.  Next.',3,'A. ①\u00a0Next.'),
                                      ('A.\r\n\tNext.',5,'A. ①\u00a0Next.'),('A.Next.',2,'A. ①\u00a0Next.')]:
            with self.subTest(value=value):
                view={'passage':value,'annotations':[{'kind':'insertion_slot','number':1,'offset':offset}]}
                self.assertEqual(''.join(x['text'] for x in passage_runs(view)),expected)
                self.assertEqual(view['passage'],value)

    def test_sentence_and_word_numbers_use_nbsp_without_moving_underlines(self):
        view={'passage':'Alpha beta.', 'annotations':[{'kind':'sentence_number','number':1,'offset':0},
              {'kind':'numbered_word','number':2,'span':[6,10]}]}
        runs=passage_runs(view)
        self.assertEqual(''.join(x['text'] for x in runs),'①\u00a0Alpha ②\u00a0beta.')
        self.assertEqual([x['text'] for x in runs if x.get('format_role')=='question_underlined_reference'],['beta'])

    def test_underline_uses_actual_master_run(self):
        view={'passage':'This is a target.', 'annotations':[{'kind':'underline','span':[10,16]}]}
        el=RoleBank().paragraph('mock_question_passage',passage_runs(view))
        underlined=el.xpath('.//w:r[w:rPr/w:u]/w:t/text()',namespaces=NS)
        self.assertEqual(underlined,['target'])

    def test_arbitrary_inline_format_not_allowed(self):
        with self.assertRaisesRegex(ValueError,'Unapproved'):
            RoleBank().paragraph('sv',[{'run':0,'text':'X','format_role':'cover_lesson_number'}])

    def test_missing_cover_never_copies_old_master_lesson(self):
        d=fixture();del d['cover']['lesson_number']
        with self.assertRaisesRegex(ValueError,'lesson_number'):
            compile_plan(d)

    def test_workbook_retranslation_starts_on_new_page_with_all_actual_key_activities(self):
        data=fixture(); before=deepcopy(data); plan=compile_plan(data)
        els=next(b['elements'] for b in plan['blocks'] if b['id']=='u1/workbook')
        at=next(i for i,e in enumerate(els) if e.get('anchor')=='key/heading')
        header=els[at-1]
        self.assertEqual(header['role'],'workbook_continuation')
        self.assertEqual(''.join(r['text'] for r in header['runs']),'문단 1 워크북 (계속)')
        self.assertTrue(header['page_break_before'])
        self.assertTrue(header['chain'])
        self.assertFalse(els[at].get('page_break_before',False))
        self.assertNotIn('workbook_question_gap',[e['role'] for e in els])
        keys=data['units'][0]['workbook']['key_sentence_ids']
        self.assertEqual(''.join(r['text'] for r in els[at]['runs']),f'4. 핵심 문장 {len(keys)}개 다시 해석하기')
        self.assertEqual([e['role'] for e in els[at+1:]],
                         ['workbook_key_sentence','workbook_key_answer_label','workbook_key_answer_space']*len(keys))
        sentences={s['id']:s for s in data['sentences']}
        activity_rows=els[at+1::3]
        self.assertEqual([e['anchor'] for e in activity_rows],['key/'+sid for sid in keys])
        self.assertEqual([''.join(r['text'] for r in e['runs']) for e in activity_rows],
                         [f'{i}.   '+sentences[sid]['text'] for i,sid in enumerate(keys,1)])
        self.assertEqual([e['role'] for e in els if e.get('page_break_before')],
                         ['workbook_header','workbook_continuation'])
        self.assertEqual(data,before)

    def test_prior_key_continuations_are_validated_but_superseded_by_whole_activity_page(self):
        baseline=compile_plan(fixture())
        for anchors in [['key/s2'],['key/heading'],['key/heading','key/s2']]:
            with self.subTest(anchors=anchors):
                d=fixture()
                d['layout_adjustments']=[{'block_id':'u1/workbook','before_anchor':anchor,
                    'content_sha256':content_hash(d),'renderer':'Microsoft Word','observed_page':6,
                    'reason':'시험용 이전 관찰 기록'} for anchor in anchors]
                before=deepcopy(d); plan=compile_plan(d)
                self.assertEqual(plan,baseline)
                self.assertEqual(d,before)
                els=next(b['elements'] for b in plan['blocks'] if b['id']=='u1/workbook')
                self.assertEqual(sum(e['role']=='workbook_continuation' for e in els),1)
                second=next(i for i,e in enumerate(els) if e.get('anchor')=='key/s2')
                self.assertEqual(els[second-1]['role'],'workbook_key_answer_space')

    def test_superseded_key_continuation_still_rejects_invalid_or_repeated_anchor(self):
        for anchors in [['key/missing'],['key/heading','key/heading']]:
            with self.subTest(anchors=anchors):
                d=fixture()
                d['layout_adjustments']=[{'block_id':'u1/workbook','before_anchor':anchor,
                    'content_sha256':content_hash(d),'renderer':'Microsoft Word','observed_page':6,
                    'reason':'시험용 잘못된 관찰'} for anchor in anchors]
                with self.assertRaisesRegex(ValueError,'existing noninitial content anchor|repeated continuation'):
                    compile_plan(d)

    def test_non_key_workbook_continuation_remains_in_its_reviewed_position(self):
        d=fixture(); qid=d['units'][0]['workbook']['question_id']
        d['layout_adjustments']=[{'block_id':'u1/workbook','before_anchor':'question/'+qid,
            'content_sha256':content_hash(d),'renderer':'Microsoft Word','observed_page':6,'reason':'문제 앞 관찰 기록'}]
        plan=compile_plan(d)
        els=next(b['elements'] for b in plan['blocks'] if b['id']=='u1/workbook')
        at=next(i for i,e in enumerate(els) if e.get('anchor')=='question/'+qid)
        self.assertEqual(els[at-1]['role'],'workbook_continuation')
        self.assertFalse(els[at-1].get('page_break_before',False))
        self.assertEqual(sum(e['role']=='workbook_continuation' for e in els),2)

    def test_continuation_is_bound_to_reviewed_content(self):
        d=fixture()
        d['layout_adjustments']=[{'block_id':'u1/workbook','before_anchor':'key/s2',
            'content_sha256':content_hash(d),'renderer':'Microsoft Word','observed_page':6,'reason':'시험용 관찰 기록'}]
        plan=compile_plan(d)
        els=next(b['elements'] for b in plan['blocks'] if b['id']=='u1/workbook')
        at=next(i for i,e in enumerate(els) if e.get('anchor')=='key/s2')
        self.assertEqual(els[at-1]['role'],'workbook_key_answer_space')
        d['cover']['topic_ko']='바뀐 원고'
        with self.assertRaisesRegex(ValueError,'different manuscript'):
            compile_plan(d)

    def test_wrong_reason_block_does_not_break_after_each_reason(self):
        plan=compile_plan(fixture())
        els=next(b['elements'] for b in plan['blocks'] if b['id']=='answers/mock1')
        flags=[x['chain'] for x in els if x['role']=='wrong_reason']
        self.assertEqual(flags,[True,True,True,False]*5)


if __name__=='__main__':
    unittest.main()
