"""Approved marker typography and narrow PDF normalization regressions."""
from copy import deepcopy
from pathlib import Path
import sys
import unittest
import uuid
from zipfile import ZipFile
from lxml import etree as E

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / '../scripts'))
from book_plan import compile_plan
from master_docx import RoleBank, NS, tag, write
from check_saved_docx import check as check_saved, paragraph_text
from check_release_text import compact, marker_breaks
from test_book_plan import fixture


class RenderMarkerTests(unittest.TestCase):
    def test_circled_choice_digits_use_one_font_without_changing_other_glyphs(self):
        bank = RoleBank(); legacy = RoleBank(); legacy.circled = None
        for role in ('mock_question_passage', 'workbook_question_passage',
                     'quick_answers_row', 'mock_question_choice', 'choice_translation',
                     'analysis_grammar_item', 'question_explanation'):
            with self.subTest(role=role):
                text = 'English ①\u00a0one ②③④⑤ / ⑥⑯⑳ ★핵심 한국어'
                runs = [{'run': 0, 'text': text}]
                actual = bank.paragraph(role, runs)
                original = legacy.paragraph(role, runs)
                self.assertEqual(paragraph_text(actual), text)
                self.assertEqual(E.tostring(actual.find('w:pPr', NS)),
                                 E.tostring(original.find('w:pPr', NS)))
                original_rpr = original.find('w:r/w:rPr', NS)
                for run in actual.findall('w:r', NS):
                    rtext = ''.join(run.xpath('.//w:t/text()', namespaces=NS))
                    properties = deepcopy(run.find('w:rPr', NS))
                    expected = deepcopy(original_rpr)
                    if rtext and rtext[0] in '①②③④⑤':
                        fonts = properties.find('w:rFonts', NS)
                        self.assertEqual(fonts.attrib, {**{tag(slot): '맑은 고딕'
                            for slot in ('ascii','hAnsi','eastAsia','cs')}, tag('hint'): 'eastAsia'})
                        properties.remove(fonts)
                        old_fonts = expected.find('w:rFonts', NS)
                        if old_fonts is not None: expected.remove(old_fonts)
                    self.assertEqual(E.tostring(properties), E.tostring(expected))

    def test_circled_run_split_preserves_underlining_and_control_characters(self):
        bank = RoleBank(); legacy = RoleBank(); legacy.circled = None
        text = '\t①\u00a0word\n② more\t③④⑤\n'
        runs = [{'run': 0, 'text': text, 'underline': True}]
        actual = bank.paragraph('mock_question_prompt', runs)
        original = legacy.paragraph('mock_question_prompt', runs)
        self.assertEqual(paragraph_text(actual), text)
        for name in ('br', 'tab'):
            self.assertEqual(len(actual.findall('.//w:'+name, NS)),
                             len(original.findall('.//w:'+name, NS)))
        self.assertTrue(all(r.find('w:rPr/w:u', NS).get(tag('val')) == 'single'
                            for r in actual.findall('w:r', NS)))

    def test_circled_font_does_not_override_compact_size_or_emphasis(self):
        bank = RoleBank(); legacy = RoleBank(); legacy.circled = None
        roles = [role for role, spec in bank.contract['derived_roles'].items()
                 if spec.get('compact_font') and spec['base_role'] != 'analysis_sentence_gap']
        self.assertTrue(roles)
        for role in roles:
            with self.subTest(role=role):
                actual = bank.paragraph(role, [{'run': 0, 'text': '①'}])
                original = legacy.paragraph(role, [{'run': 0, 'text': '①'}])
                for name in ('sz', 'szCs', 'b', 'color', 'u'):
                    a = actual.find('w:r/w:rPr/w:'+name, NS)
                    b = original.find('w:r/w:rPr/w:'+name, NS)
                    self.assertEqual(None if a is None else E.tostring(a),
                                     None if b is None else E.tostring(b))

    def test_saved_checker_rejects_circled_font_substitution(self):
        plan = {'blocks': [{'id': 'circle', 'elements': [{'role': 'quick_answers_row',
                'runs': [{'run': 0, 'text': '1. ① 2. ②'}], 'chain': False}]}]}
        directory = HERE / ('saved-docx-test-' + uuid.uuid4().hex)
        directory.mkdir()
        source = directory/'source.docx'; target = directory/'changed.docx'
        write(plan, source)
        self.assertEqual(check_saved(plan, source)['status'], 'SAVED_CONTENT_MATCH')
        with ZipFile(source) as z: parts = [(i,z.read(i.filename)) for i in z.infolist()]
        root = E.fromstring(dict((i.filename,b) for i,b in parts)['word/document.xml'])
        runs = root.findall('.//w:sdtContent/w:p/w:r', NS)
        circled = next(r for r in runs if ''.join(r.xpath('.//w:t/text()', namespaces=NS)) == '①')
        circled.find('w:rPr/w:rFonts', NS).set(tag('eastAsia'), 'Cambria Math')
        with ZipFile(target,'w') as z:
            for info,data in parts:
                z.writestr(info, E.tostring(root,xml_declaration=True,encoding='UTF-8',standalone=True)
                           if info.filename == 'word/document.xml' else data)
        result = check_saved(plan, target)
        self.assertNotEqual(result['format_validation'], 'PASS')
        self.assertTrue(result['errors'])

    def test_reading_and_analysis_markers_keep_visible_text_and_master_properties(self):
        data = fixture(); before = deepcopy(data)
        bank = RoleBank(); plan = compile_plan(data)
        seen = set()
        for block in plan['blocks']:
            for element in block['elements']:
                role = element['role']
                if role not in {'interpretation_key_english', 'analysis_key_english_chunks'}:
                    continue
                seen.add(role)
                marker = element['runs'][-1]
                prefix = '\u00a0' * 3 if role == 'analysis_key_english_chunks' else '   '
                self.assertEqual(marker['text'], prefix + '★\ufeff핵\ufeff심')
                self.assertEqual(marker['text'].replace('\ufeff', '').replace('\u00a0', ' '), '   ★핵심')
                paragraph = bank.paragraph(role, [marker])
                template = bank.paragraph(role, [{**marker, 'text': '   ★핵심'}])
                from lxml import etree as E
                self.assertEqual(E.tostring(paragraph.find('w:pPr', NS)),
                                 E.tostring(template.find('w:pPr', NS)))
                self.assertEqual(E.tostring(paragraph.find('w:r/w:rPr', NS)),
                                 E.tostring(template.find('w:r/w:rPr', NS)))
        self.assertEqual(seen, {'interpretation_key_english', 'analysis_key_english_chunks'})
        self.assertEqual(data, before)

    def test_analysis_marker_keeps_final_word_without_changing_source(self):
        data = fixture(); before = deepcopy(data); plan = compile_plan(data)
        original = {s['text'] for s in data['sentences'] if s['key']}
        bank = RoleBank()
        for block in plan['blocks']:
            for element in block['elements']:
                if element['role'] != 'analysis_key_english_chunks':
                    continue
                runs = element['runs']
                self.assertTrue(any(text.endswith(runs[-2]['text']) for text in original))
                self.assertFalse(runs[-2]['text'][-1].isspace())
                saved = bank.paragraph(element['role'], runs)
                self.assertTrue(paragraph_text(saved).endswith(
                    runs[-2]['text'] + '\u00a0\u00a0\u00a0★\ufeff핵\ufeff심'))
        self.assertEqual(data, before)

    def test_pdf_normalization_ignores_only_joiners_of_exact_approved_marker(self):
        self.assertEqual(compact('line   ★\ufeff핵\ufeff심'), compact('line ★핵심'))
        self.assertNotEqual(compact('word\ufeffword'), compact('wordword'))
        self.assertNotEqual(compact('★\ufeff다른표식'), compact('★다른표식'))
        self.assertNotEqual(compact('★\ufeff핵\ufeff심'), compact('★심핵'))

    def test_marker_break_diagnostic_still_detects_wrapped_key_after_joiners(self):
        same = (0, 10, 5, 20); other = (0, 30, 5, 40)
        prefixes = {c: set() for c in '★①②③④⑤'}
        prefixes['★'] = {'핵심'}
        for text in ['★핵심', '★\ufeff핵\ufeff심']:
            chars = [(c, same if c in '★\ufeff' else other) for c in text]
            result = marker_breaks(chars, prefixes)
            self.assertEqual(len(result), 1, text)
            self.assertEqual(result[0]['next_character'], '핵')
            self.assertEqual(marker_breaks([(c, same) for c in text], prefixes), [])


if __name__ == '__main__':
    unittest.main()
