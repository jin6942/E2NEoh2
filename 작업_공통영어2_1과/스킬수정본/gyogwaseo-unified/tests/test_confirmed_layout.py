"""Independent expected values from user decisions A01-A20 and restored R01-R03.

Do not derive expectations from layout-contract.json: these tests must fail when
both a generated document and its implementation contract drift together.
"""
from copy import deepcopy
from pathlib import Path
import sys
import unittest
from lxml import etree as E

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / '../scripts'))
from book_plan import compile_plan
from master_docx import RoleBank, NS
from test_book_plan import fixture
from test_learning_content import fixture as learning_fixture

W = '{' + NS['w'] + '}'


def content(element):
    return ''.join(run['text'] for run in element.get('runs', []))


class ConfirmedLayoutTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bank = RoleBank()
        cls.data = fixture()
        cls.data['metadata']['lesson'] = 'UNIT03'
        cls.data['cover']['lesson_number'] = '03'
        cls.data['units'][0]['hook'] = '원문 사실에 근거한 시험용 질문'
        cls.plan = compile_plan(cls.data)
        cls.blocks = {b['id']: b['elements'] for b in cls.plan['blocks']}
        styles = E.fromstring(dict((i.filename, raw) for i, raw in cls.bank.package)['word/styles.xml'])
        cls.styles = {s.get(W+'styleId'): s for s in styles.findall('w:style',NS)}
        cls.defaults = styles.find('w:docDefaults/w:rPrDefault/w:rPr',NS)
        cls.default_style = next((s.get(W+'styleId') for s in cls.styles.values()
                                  if s.get(W+'type')=='paragraph' and s.get(W+'default')=='1'), 'Normal')

    def effective_run(self, role, index):
        paragraph = self.bank.paragraph(role, [{'run': index, 'text': 'probe'}])
        out = {}
        def overlay(node):
            if node is not None:
                for child in node:
                    out.setdefault(E.QName(child).localname, {}).update(
                        {E.QName(k).localname:v for k,v in child.attrib.items()} or {'val':'1'})
        overlay(self.defaults)
        ps = paragraph.find('w:pPr/w:pStyle',NS)
        sid = ps.get(W+'val') if ps is not None else self.default_style
        chain=[];seen=set()
        while sid and sid not in seen and sid in self.styles:
            seen.add(sid);style=self.styles[sid];chain.insert(0,style)
            based=style.find('w:basedOn',NS);sid=based.get(W+'val') if based is not None else None
        for style in chain:overlay(style.find('w:rPr',NS))
        overlay(paragraph.find('w:r/w:rPr',NS))
        return out

    def run_value(self, role, index, name, default=None):
        return self.effective_run(role,index).get(name,{}).get('val',default)

    def assert_run(self, role, index, *, size=None, color=None, bold=None, font=None):
        props=self.effective_run(role,index)
        if size is not None:self.assertEqual(float(props['sz']['val'])/2,size,(role,index,'size'))
        if color is not None:self.assertEqual(props.get('color',{}).get('val','000000'),color,(role,index,'color'))
        if bold is not None:
            self.assertEqual(props.get('b',{}).get('val','0') not in ('0','false','off'),bold,(role,index,'bold'))
        if font is not None:self.assertEqual(props['rFonts']['ascii'],font,(role,index,'font'))

    def spacing(self, role):
        # The empty gap paragraph must be rendered with runs omitted.
        para=self.bank.paragraph(role,None if role=='analysis_sentence_gap' else [{'run':0,'text':'probe'}])
        node=para.find('w:pPr/w:spacing',NS)
        return {E.QName(k).localname:v for k,v in node.attrib.items()}

    def test_a01_r01_gloss_sv_and_star_exact_values(self):
        self.assert_run('sv',0,size=7.5)
        self.assert_run('sv',1,size=7.5)
        self.assert_run('gloss',0,size=8.5,color='333333',bold=False)
        self.assert_run('gloss',1,size=8.5,color='203864',bold=True)

    def test_a02_easy_explanation_does_not_color_or_bold_the_body(self):
        self.assert_run('analysis_easy_explanation',0,size=10,color='1F4E79',bold=True)
        self.assert_run('analysis_easy_explanation',1,size=10,color='000000',bold=False)

    def test_revised_analysis_starts_explanation_on_a_new_blue_header_page(self):
        els=self.blocks['u1/analysis'];roles=[e['role'] for e in els]
        self.assertEqual(roles[0],'analysis_header')
        self.assertEqual(roles.count('analysis_natural_translation'),3)
        headings = [i for i,e in enumerate(els) if e['role']=='analysis_header']
        self.assertEqual(len(headings), 2)
        self.assertTrue(els[headings[1]]['page_break_before'])
        self.assertEqual(roles[headings[1]+1], 'analysis_section_heading')
        self.assertGreater(headings[1], max(i for i,role in enumerate(roles) if role=='analysis_natural_translation'))
        self.assertTrue(roles.index('analysis_natural_translation')<roles.index('analysis_section_heading'))
        self.assertFalse(any('모범 해석' in content(e) or '끊어읽기 해석' in content(e)
                             for e in els if e['role'].endswith('header')))

    def test_a04_explanation_spacing_uses_confirmed_gpt_values(self):
        for role,after in [('analysis_prose','100'),('analysis_flow_item','100'),
                           ('analysis_easy_explanation','120'),('analysis_grammar_item','120')]:
            self.assertEqual(self.spacing(role)['after'],after,role)

    def test_a05_student_question_choices_have_blue_numbers_only(self):
        for role in ['workbook_question_choice','mock_question_choice']:
            self.assert_run(role,0,size=10,color='2E5496',bold=True)
            self.assert_run(role,1,size=10,color='000000',bold=False,font='Times New Roman')

    def test_a06_workbook_key_english_is_plain_black(self):
        self.assert_run('workbook_key_sentence',1,size=10,color='000000',bold=False,font='Times New Roman')

    def test_a07_analysis_key_is_plain_with_separate_orange_marker(self):
        self.assert_run('analysis_key_english_chunks',2,size=10,color='000000',bold=False,font='Times New Roman')
        els=[e for e in self.blocks['u1/analysis'] if e['role']=='analysis_key_english_chunks']
        self.assertEqual(len(els),2)
        for element in els:
            self.assertTrue(content(element).endswith('★\ufeff핵\ufeff심'))
            marker=element['runs'][-1]
            self.assert_run(element['role'],marker['run'],size=10,color='C55A11',bold=True)
        for element in self.blocks['u1/analysis']:
            if element['role']=='analysis_english_chunks':self.assertNotIn('★핵심',content(element).replace('\ufeff',''))

    def test_a08_authored_heading_placement_and_kind_metadata(self):
        title='Resource Care (자원 관리)'
        for bid,role in [('u1/reading','unit_topic_english'),('u1/workbook','workbook_subtitle')]:
            heading=next(e for e in self.blocks[bid] if e['role']==role)
            self.assertEqual(content(heading),title)
            self.assertEqual(heading['heading_kind'],'주제')
            self.assertNotIn('[주제]',content(heading))
        self.assertNotIn(title,'\n'.join(content(e) for e in self.blocks['u1/analysis']))
        changed=deepcopy(self.data);changed['units'][0]['analysis']['heading_kind']='제목'
        plan=compile_plan(changed)
        headings=[e for b in plan['blocks'] for e in b['elements'] if e['role'] in ('unit_topic_english','workbook_subtitle')]
        self.assertEqual([e['heading_kind'] for e in headings],['제목','제목'])
        self.assertEqual([content(e) for e in headings],[title,title])

    def test_a08_original_heading_is_separate_and_at_its_sentence(self):
        rows=self.blocks['u1/reading'];matches=[i for i,e in enumerate(rows) if e['role']=='source_subheading']
        self.assertEqual(len(matches),1)
        i=matches[0]
        self.assertEqual(content(rows[i]),'Synthetic Source Heading')
        self.assertEqual(rows[i]['source_heading_id'],'h1')
        self.assertEqual(rows[i+1]['role'],'interpretation_key_english')
        for bid in ['u1/analysis','u1/workbook']:
            self.assertFalse(any(e['role']=='source_subheading' for e in self.blocks[bid]))

    def test_a08_one_original_heading_is_not_repeated_for_later_long_paragraph(self):
        # Both paragraphs exceed six sentences, so they remain separate units
        # under a single original heading occurrence before s1.
        data=learning_fixture(['They repair useful tools.']*14)
        data['sources'][0]['label']='Synthetic source'
        data['cover']={'lesson_label':'LESSON','lesson_number':'00',
                       'topic_first':'Synthetic','topic_second':'fixture','topic_ko':'합성 시험'}
        base=deepcopy(data['units'][0]);data['paragraphs']=[];data['units']=[]
        for i in range(2):
            ids=[f's{j}' for j in range(i*7+1,i*7+8)]
            paragraph_id=f'p{i+1}'
            data['paragraphs'].append({'id':paragraph_id,'source_id':'src',
                                       'subheading_id':'h1','sentence_ids':ids})
            unit=deepcopy(base)
            unit.update(id=f'u{i+1}',paragraph_ids=[paragraph_id],sentence_ids=ids)
            unit['analysis']['flow']=[{'sentence_ids':ids,'text_ko':'시험용 흐름'}]
            for field in ['easy_explanations','grammar_points']:
                for row,sid in zip(unit['analysis'][field],ids):row['sentence_id']=sid
            unit.pop('workbook')
            if i:unit['today_words']=[]
            data['units'].append(unit)
        for sentence in data['sentences']:
            sentence['key']=sentence['id'] in {'s1','s2','s8','s9'}
        plan=compile_plan(data,'learning')
        occurrences=[(block['id'],element['source_heading_id'])
                     for block in plan['blocks'] for element in block['elements']
                     if element['role']=='source_subheading']
        self.assertEqual(occurrences,[('u1/reading','h1')])

    def test_a09_analysis_heading_wording_is_fixed_korean(self):
        roles=['analysis_section_heading','analysis_flow_heading','analysis_easy_explanation_heading',
               'analysis_grammar_heading','analysis_relations_heading']
        texts=[content(e) for e in self.blocks['u1/analysis'] if e['role'] in roles]
        self.assertEqual(texts,['▶ 글의 의도','▶ 글의 흐름','▶ 각 문장 쉬운 풀이','▶ 구문으로 해석하기','▶ 필수 유의어 / 반의어'])

    def test_a10_bracketed_source_sentence_references_are_not_question_numbers(self):
        els=self.blocks['u1/analysis']
        self.assertIn('[1~3번 문장]',content(next(e for e in els if e['role']=='analysis_flow_item')))
        self.assertTrue(content(next(e for e in els if e['role']=='analysis_easy_sentence')).startswith('[1번 문장]'))
        self.assertIn('[1번 문장]:',content(next(e for e in els if e['role']=='analysis_grammar_item')))

    def test_a11_answer_english_and_korean_styles_are_separate(self):
        for role in ['choice_translation','correct_choice_translation']:
            self.assert_run(role,1,size=8.5,color='000000',bold=False)
            self.assert_run(role,2,size=8.5,color='666666',bold=False)
            self.assert_run(role,0,size=8.5,bold=True)

    def test_a12_natural_translation_label_is_present_on_every_sentence(self):
        rows=[e for e in self.blocks['u1/analysis'] if e['role']=='analysis_natural_translation']
        self.assertEqual(len(rows),3)
        self.assertTrue(all(content(e).startswith('↳ 자연 해석  ') for e in rows))

    def test_a13_flow_stage_reference_and_body_have_distinct_emphasis(self):
        self.assert_run('analysis_flow_item',0,size=10,bold=True)
        self.assert_run('analysis_flow_item',1,size=9,color='1F3864',bold=True)
        self.assert_run('analysis_flow_item',2,size=10,color='000000',bold=False)

    def test_a14_grammar_item_uses_circled_item_source_reference_quote_explanation(self):
        rows=[e for e in self.blocks['u1/analysis'] if e['role']=='analysis_grammar_item']
        self.assertEqual([content(e)[0] for e in rows],list('①②③'))
        self.assertIn('[1번 문장]:',content(rows[0]))
        self.assertIn(' — 시험용 설명',content(rows[0]))
        self.assert_run('analysis_grammar_item',0,bold=True)
        self.assert_run('analysis_grammar_item',1,color='1F3864',bold=True)
        self.assert_run('analysis_grammar_item',3,font='Times New Roman',bold=False)
        self.assert_run('analysis_grammar_item',4,bold=False)

    def test_a15_relation_symbols_and_typographic_roles(self):
        rows=[e for e in self.blocks['u1/analysis'] if e['role']=='analysis_relations_item']
        self.assertTrue(all(' ≈ ' in content(e) and ' ↔ ' in content(e) for e in rows))
        self.assert_run('analysis_relations_item',0,size=10,bold=True,font='Times New Roman')
        self.assert_run('analysis_relations_item',2,color='1F4E79',bold=True)
        self.assert_run('analysis_relations_item',3,size=9.5,bold=False,font='Times New Roman')
        self.assert_run('analysis_relations_item',4,size=9,color='333333',bold=False)

    def test_a16_question_source_lines_removed_without_mutating_source_links(self):
        d=deepcopy(self.data);before=deepcopy(d['question_sources']);plan=compile_plan(d)
        self.assertEqual(d['question_sources'],before)
        roles=[e['role'] for b in plan['blocks'] for e in b['elements']]
        self.assertNotIn('workbook_question_source',roles)
        self.assertNotIn('mock_question_source',roles)
        self.assertEqual(len(before),16)

    def test_a17_student_section_headings_use_three_gwa_not_internal_unit(self):
        targets={'interpretation_header','analysis_header','workbook_header','mock_round_header','answers_header'}
        headings=[content(e) for b in self.plan['blocks'] for e in b['elements'] if e['role'] in targets]
        self.assertTrue(all('3과' in title for title in headings),headings)
        self.assertTrue(all('UNIT03' not in title for title in headings),headings)
        self.assertEqual(self.data['metadata']['lesson'],'UNIT03')
        self.assertEqual(self.data['cover']['lesson_number'], '03')
        self.assertTrue(content(next(e for e in self.blocks['cover']
                                     if e['role']=='cover_publisher_large')).endswith('3과'))
        self.assertFalse(any(e['role']=='cover_lesson_number' for e in self.blocks['cover']))

    def test_a18_cover_summarizes_equal_rounds_from_actual_counts(self):
        detail=content(next(e for e in self.blocks['cover'] if e['role']=='cover_assessment_counts'))
        self.assertEqual(detail,'워크북 실전문제 1문항  +  미니 모의고사 5문항×3회')
        d=deepcopy(self.data);a=d['assessment'];a['scope']={'kind':'custom','instruction':'Synthetic fixture: five/five/four rounds'}
        for field in ['plan','questions','quick_key','explanations']:
            a[field]=[row for row in a[field] if row['id']!='mock3-3']
            for row in a[field]:
                if row['set_id']=='mock3' and row['number']>3:
                    row['number']-=1
        d['question_sources']=[row for row in d['question_sources'] if row['id']!='mock3-3']
        plan=compile_plan(d)
        detail=content(next(e for e in plan['blocks'][0]['elements'] if e['role']=='cover_assessment_counts'))
        self.assertEqual(detail,'워크북 실전문제 1문항  +  미니 모의고사 1회 5문항  +  미니 모의고사 2회 5문항  +  미니 모의고사 3회 4문항')

    def test_a19_superseded_hook_is_not_printed_even_when_present_in_manuscript(self):
        self.assertNotIn('unit_hook', [e['role'] for b in self.plan['blocks'] for e in b['elements']])
        self.assertNotIn(self.data['units'][0]['hook'], '\n'.join(
            content(e) for b in self.plan['blocks'] for e in b['elements']))

    def test_a20_sentence_gap_does_not_double_add_gpt_after_spacing(self):
        for role in ['analysis_english_chunks','analysis_key_english_chunks','analysis_korean_chunks','analysis_natural_translation']:
            s=self.spacing(role)
            self.assertEqual((s['before'],s['after'],s['line'],s['lineRule']),('30','40','253','exact'),role)
        gap=self.spacing('analysis_sentence_gap')
        self.assertEqual((gap.get('before','0'),gap.get('after','0'),gap['line'],gap['lineRule']),('0','0','170','exact'))
        rows=self.blocks['u1/analysis']
        for i,e in enumerate(rows):
            if e['role']=='analysis_natural_translation':self.assertEqual(rows[i+1]['role'],'analysis_sentence_gap')

    def test_r02_workbook_answer_order_matches_student_activities(self):
        headings=[content(e) for e in self.blocks['u1/answers']
                  if e['role'] in ['workbook_answer_activity_heading','workbook_key_answers_heading']]
        self.assertEqual(headings,['1. 오늘의 낱말','2. 유의어·반의어 뜻 쓰기','3. 실전문제','4. 핵심 문장 해석'])

    def test_r03_review_line_retains_exact_approved_wording(self):
        row=next(e for e in self.blocks['u1/reading'] if e['role']=='interpretation_review_line')
        self.assertEqual(content(row),'틀린 문장은 다음에 다시!  지문 분석지의 해석과 달랐던 문장 번호를 여기 적어 두고, 다음엔 그것만 다시 풀어요 → ________________')


if __name__ == '__main__':
    unittest.main()
