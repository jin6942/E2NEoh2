"""User-confirmed page separation, cover, answer grid and underline guards."""
from copy import deepcopy
import json
import shutil
from pathlib import Path
import sys
import uuid
import unittest
from zipfile import ZipFile
from lxml import etree as E

ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parent/'scripts'))
from master_docx import RoleBank, write
from check_saved_docx import check, expected_element
from saved_format import Styles, paragraph_record
W='{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
NS={'w':W[1:-1]}

class RevisionLayoutTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bank=RoleBank()
        cls.styles=Styles({info.filename:data for info,data in cls.bank.package})
        cls.directory=ROOT/('saved-format-test-'+uuid.uuid4().hex)
        cls.directory.mkdir()

    def role_run(self,role,index=0):
        p=self.bank.paragraph(role,[{'run':index,'text':'검사'}])
        return paragraph_record(p,self.styles)['spans'][0]['format']

    def test_cover_lesson_matches_number_color_at_twenty_points(self):
        label=self.role_run('cover_lesson_label');number=self.role_run('cover_lesson_number')
        self.assertEqual(label['sz']['val'],'40')
        self.assertEqual(label['szCs']['val'],'40')
        self.assertEqual(label['color'],number['color'])
        self.assertEqual(label['color']['val'],'203864')
        p=self.bank.paragraph('cover_lesson_label',[{'run':0,'text':'LESSON'}])
        spacing=p.find('w:pPr/w:spacing',NS)
        self.assertEqual((spacing.get(W+'line'),spacing.get(W+'lineRule')),('520','atLeast'))

    def test_cover_has_two_paragraphs_and_rejects_legacy_three(self):
        table=self.bank.table('cover_topic_box',['English title','한국어 제목'])
        self.assertEqual(len(table.findall('.//w:p',NS)),2)
        self.assertEqual(self.role_run('cover_topic_first')['sz']['val'],'44')
        self.assertEqual(self.role_run('cover_topic_korean')['sz']['val'],'21')
        with self.assertRaises(ValueError):self.bank.table('cover_topic_box',['a','b','c'])
        with self.assertRaises(ValueError):self.bank.paragraph('cover_student_name',[{'run':0,'text':'이름'}])

    def test_answer_grid_row_major_and_empty_last_cell(self):
        entries=[{'runs':[{'run':0,'text':f'{i}.'},{'run':1,'text':f' 뜻{i}'}]} for i in range(1,6)]
        table=self.bank.table('workbook_answer_grid',entries)
        self.assertEqual([c.get(W+'w') for c in table.findall('w:tblGrid/w:gridCol',NS)],['3489','3489','3488'])
        rows=table.findall('w:tr',NS);self.assertEqual(len(rows),2)
        self.assertTrue(all(r.find('w:trPr/w:cantSplit',NS) is not None for r in rows))
        texts=[''.join(p.xpath('.//w:t/text()',namespaces=NS)) for p in table.findall('.//w:p',NS)]
        self.assertEqual(texts,['1. 뜻1','2. 뜻2','3. 뜻3','4. 뜻4','5. 뜻5',''])
        for p in table.findall('.//w:p',NS)[:-1]:
            actual=paragraph_record(p,self.styles)['spans']
            original=self.bank.paragraph('workbook_word_answer',entries[int(actual[0]['text'].split('.')[0])-1]['runs'],chain=False)
            self.assertEqual(actual,paragraph_record(original,self.styles)['spans'])
        self.assertEqual(expected_element({'kind':'table','role':'workbook_answer_grid','entries':entries})['rows'][-1][-1],[''])

    def test_spacing_uses_paragraph_before_not_an_empty_line(self):
        p=self.bank.paragraph('mock_question_prompt_spaced',[{'run':0,'text':'2. 질문'}])
        self.assertEqual(p.find('w:pPr/w:spacing',NS).get(W+'before'),'494')
        self.assertIsNone(p.find('.//w:br',NS))
        self.assertEqual(self.role_run('mock_question_prompt_spaced'),self.role_run('mock_question_prompt'))

    def test_summary_spacing_changes_only_before_and_after(self):
        runs=[{'run':0,'text':'[요약문] A sample summary.'}]
        base=self.bank.paragraph('mock_summary',runs)
        spaced=self.bank.paragraph('mock_summary_spaced',runs)
        spacing=spaced.find('w:pPr/w:spacing',NS)
        self.assertEqual((spacing.get(W+'before'),spacing.get(W+'after')),('200','200'))
        self.assertEqual(self.role_run('mock_summary_spaced')['sz']['val'],'20')
        self.assertEqual(self.role_run('mock_summary_spaced'),self.role_run('mock_summary'))
        self.assertIsNone(spaced.find('.//w:br',NS))
        # Normalize only the approved two attributes: all other paragraph/run
        # properties, including line spacing and keep settings, must match.
        base_spacing=base.find('w:pPr/w:spacing',NS)
        for name in ('before','after'):
            prior=base_spacing.get(W+name)
            if prior is None:spacing.attrib.pop(W+name,None)
            else:spacing.set(W+name,prior)
        self.assertEqual(E.tostring(spaced),E.tostring(base))

    def test_saved_summary_rejects_lost_space_above_or_below(self):
        plan={'blocks':[{'id':'summary-test','elements':[
            {'role':'mock_summary_spaced','runs':[{'run':0,'text':'[요약문] A sample summary.'}]}]}]}
        for name in ('before','after'):
            with self.subTest(lost_spacing=name):
                path=self.directory/(uuid.uuid4().hex+'.docx')
                write(plan,path)
                self.assertFalse(check(plan,path)['errors'])
                with ZipFile(path) as z:parts=[(info,z.read(info.filename)) for info in z.infolist()]
                doc=E.fromstring(dict((info.filename,data) for info,data in parts)['word/document.xml'])
                doc.find('.//w:sdtContent/w:p/w:pPr/w:spacing',NS).set(W+name,'0')
                with ZipFile(path,'w') as z:
                    for info,data in parts:z.writestr(info,E.tostring(doc) if info.filename=='word/document.xml' else data)
                errors=check(plan,path)['errors']
                self.assertTrue(any(e['code']=='SAVED_FORMAT_MISMATCH' for e in errors))

    def test_archived_specimen_structure_and_current_role_rendering(self):
        plan=json.loads((ROOT/'template-audit/layout-specimen.json').read_text(encoding='utf-8'))
        blocks={b['id']:b['elements'] for b in plan['blocks']}
        analysis=blocks['unit1/analysis'];intent=next(i for i,e in enumerate(analysis) if e['role']=='analysis_section_heading')
        self.assertEqual(analysis[intent-1]['role'],'analysis_header')
        self.assertTrue(analysis[intent-1]['page_break_before'])
        self.assertTrue(any(e['role']=='workbook_answer_grid' for e in blocks['answers']))
        self.assertFalse(any(e['role']=='cover_student_name' for e in blocks['cover']))
        # Keep the archived specimen immutable. Isolate the newly approved
        # circled font policy from its two known old workbook 8.5pt sizes.
        legacy_assets=self.directory/'legacy-circled-font-assets'
        legacy_assets.mkdir()
        for asset in self.bank.assets.iterdir():
            if asset.is_file():shutil.copy2(asset,legacy_assets/asset.name)
        contract=deepcopy(self.bank.contract)
        contract.pop('circled_number_typography')
        (legacy_assets/'layout-contract.json').write_text(json.dumps(contract,ensure_ascii=False),encoding='utf8')
        errors=check(plan,ROOT/'template-audit/layout-specimen.docx',assets=legacy_assets)['errors']
        self.assertEqual([(e['code'],e['role'],e.get('expected'),e.get('actual')) for e in errors],
                         [('SAVED_FORMAT_MISMATCH','workbook_word_table','20','17'),
                          ('SAVED_FORMAT_MISMATCH','workbook_relations_table','20','17')])
        current_errors=check(plan,ROOT/'template-audit/layout-specimen.docx')['errors']
        font_errors=[e for e in current_errors if '/rFonts/' in e.get('property','')]
        self.assertTrue(font_errors)
        for error in font_errors:
            self.assertEqual(error['code'],'SAVED_FORMAT_MISMATCH')
            self.assertTrue(error.get('text_excerpt'))
            self.assertLessEqual(set(error['text_excerpt']),set('①②③④⑤'))
        self.assertEqual([e for e in current_errors if e not in font_errors],errors)
        current=self.directory/'current-specimen.docx'
        write(plan,current)
        self.assertFalse(check(plan,current)['errors'])

    def test_required_prompt_underline_is_independent_of_expected_style(self):
        # A buggy plan that forgot the underline in both source and DOCX still fails.
        element={'role':'mock_question_prompt','runs':[{'run':0,'text':'1. 밑줄 친 target의 의미는?'}],
                 'required_underlines':[[9,15]]}
        path=self.directory/(uuid.uuid4().hex+'.docx');plan={'blocks':[{'id':'test','elements':[element]}]}
        write(plan,path)
        report=check(plan,path)
        self.assertTrue(any(e['code']=='REQUIRED_TARGET_UNDERLINE_MISSING' for e in report['errors']))

    def test_prompt_inline_underline_preserves_base_character_style(self):
        p=self.bank.paragraph('mock_question_prompt',[{'run':0,'text':'target','underline':True}])
        actual=paragraph_record(p,self.styles)['spans'][0]['format'];base=self.role_run('mock_question_prompt')
        self.assertEqual(actual['u']['val'],'single')
        actual.pop('u');base.pop('u',None);self.assertEqual(actual,base)
        with self.assertRaises(ValueError):self.bank.paragraph('sv',[{'run':0,'text':'not allowed','underline':True}])

    def test_each_of_five_word_targets_must_be_underlined(self):
        runs=[];spans=[];offset=0
        for i,word in enumerate(['one','two','three','four','five'],1):
            label=f'{i}. ';runs.append({'run':0,'text':label});offset+=len(label)
            runs.append({'run':1,'text':word,'format_role':'question_underlined_reference'})
            spans.append([offset,offset+len(word)]);offset+=len(word)
        element={'role':'mock_question_passage','runs':runs,'required_underlines':spans}
        path=self.directory/(uuid.uuid4().hex+'.docx');plan={'blocks':[{'id':'test','elements':[element]}]}
        write(plan,path);self.assertFalse(check(plan,path)['errors'])
        with ZipFile(path) as z:parts=[(info,z.read(info.filename)) for info in z.infolist()]
        doc=E.fromstring(dict((info.filename,data) for info,data in parts)['word/document.xml'])
        underline=doc.findall('.//w:sdtContent/w:p/w:r/w:rPr/w:u',NS)[2]
        underline.set(W+'val','none')
        with ZipFile(path,'w') as z:
            for info,data in parts:z.writestr(info,E.tostring(doc) if info.filename=='word/document.xml' else data)
        errors=check(plan,path)['errors']
        self.assertTrue(any(e['code']=='REQUIRED_TARGET_UNDERLINE_MISSING' and e['target']==spans[2] for e in errors))

if __name__=='__main__':unittest.main()
