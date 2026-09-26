"""Synthetic R diagnostics; no Word rendering or human review is claimed."""
from copy import deepcopy
import contextlib
import io
import json
from pathlib import Path
import shutil
import sys
import unittest
from unittest.mock import patch
import uuid
from zipfile import ZipFile

from lxml import etree

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'scripts'))
import check_release_text as m
import test_release as release_fixture


def chars(text, bottom=20, top=30):
    return [(character, (i * 4, bottom, i * 4 + 4, top)) for i, character in enumerate(text)]


class ReleaseTextTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Keep all generated test artifacts outside the skill package. Ordinary
        # mkdir retains the host's workspace ACLs (TemporaryDirectory may not).
        cls.workspace = HERE.parents[3].resolve()
        cls.root = cls.workspace / ('release-text-tests-' + uuid.uuid4().hex)
        cls.root.mkdir()
        helper = release_fixture.ReleaseTests()
        with patch.object(release_fixture, 'HERE', cls.root):
            helper.prepare_record(release_fixture.fixture())
        cls.folder = helper.folder
        cls.paths = {name: Path(helper.record['artifacts'][name]['path']) for name in
                     ('manuscript', 'plan', 'docx', 'pdf', 'learning_final', 'assessment_final')}
        cls.original = {name: path.read_bytes() for name, path in cls.paths.items()}

    @classmethod
    def tearDownClass(cls):
        target = cls.root.resolve()
        # Verify the exact unique test root before recursive cleanup.
        if target.parent != cls.workspace or not target.name.startswith('release-text-tests-'):
            raise AssertionError('Unexpected test cleanup target')
        shutil.rmtree(target)

    def setUp(self):
        for name, content in self.original.items():
            self.paths[name].write_bytes(content)
        self.plan = json.loads(self.original['plan'].decode('utf-8-sig'))

    def pdf_report(self, text=None, candidates=None, fonts=None):
        fonts = fonts if fonts is not None else ['FixtureFont', 'CambriaMath']
        return {'text': m.plan_text(self.plan) if text is None else text,
                'fonts': fonts, 'pages': [{'page': 1, 'characters': 100, 'fonts': fonts,
                                         'marker_break_candidates': candidates or []}],
                'footer_policy': 'Synthetic extraction only'}

    def result(self, report=None, side_effect=None):
        with patch.object(m, 'inspect_pdf', return_value=deepcopy(report or self.pdf_report()), side_effect=side_effect):
            return m.check_files(**self.paths)

    def footer_docx(self, name, include_footer=True, bare_page=False):
        namespace = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
        literal = '' if bare_page else '<w:r><w:t>Verified Footer </w:t></w:r>'
        paragraph = ('<w:p>' + literal + '<w:r><w:fldChar w:fldCharType="begin"/></w:r>'
                     '<w:r><w:instrText> PAGE \\* MERGEFORMAT </w:instrText></w:r>'
                     '<w:r><w:fldChar w:fldCharType="separate"/></w:r>'
                     '<w:r><w:t>1</w:t></w:r>'
                     '<w:r><w:fldChar w:fldCharType="end"/></w:r></w:p>')
        path = self.root / name
        with ZipFile(path, 'w') as archive:
            archive.writestr('word/document.xml', '<w:document xmlns:w="' + namespace + '">' + paragraph + '</w:document>')
            if include_footer:
                archive.writestr('word/footer1.xml', '<w:ftr xmlns:w="' + namespace + '">' + paragraph + '</w:ftr>')
        return path

    def test_actual_footer_pattern_removes_only_matching_text_near_page_foot(self):
        path = self.footer_docx('with-footer.docx')
        patterns = m.footer_patterns(path)
        body = 'Verified Footer 27'
        footer = 'Verified Footer 9'
        sample = chars(body, bottom=250, top=260) + chars('\n') + chars(footer)
        cleaned = m.remove_known_footers(sample, patterns, 842)
        self.assertEqual(m.compact(cleaned), m.compact(body))
        self.assertIn('VerifiedFooter', patterns[0])

    def test_body_text_and_unknown_bottom_text_are_not_blanket_cropped(self):
        patterns = m.footer_patterns(self.footer_docx('known-footer.docx'))
        for text, bottom in [('Verified Footer 9', 200), ('Actual body text at the bottom', 10),
                             ('정답을 고르시오', 10), ('12345', 10)]:
            with self.subTest(text=text):
                self.assertEqual(m.remove_known_footers(chars(text, bottom, bottom + 10), patterns, 842), text)

    def test_footer_requires_actual_footer_xml_and_specific_literal(self):
        body_only = self.footer_docx('body-only.docx', include_footer=False)
        bare_page = self.footer_docx('bare-page.docx', bare_page=True)
        self.assertEqual(m.footer_patterns(body_only), [])
        self.assertEqual(m.footer_patterns(bare_page), [])
        sample = chars('Verified Footer 9')
        self.assertEqual(m.remove_known_footers(sample, [], 842), 'Verified Footer 9')

    def test_missing_footer_coordinates_do_not_authorize_exclusion(self):
        patterns = m.footer_patterns(self.footer_docx('uncertain-footer.docx'))
        sample = [(letter, None) for letter in 'Verified Footer 9']
        self.assertEqual(m.remove_known_footers(sample, patterns, 842), 'Verified Footer 9')

    def test_marker_breaks_use_vertical_geometry_and_provide_review_coordinates(self):
        sample = [('★', (10, 100, 17, 108)), (' ', None), ('w', (20, 75, 25, 83))]
        rows = m.marker_breaks(sample)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]['marker'], '★')
        self.assertEqual(rows[0]['next_character'], 'w')
        self.assertEqual(rows[0]['character_index'], 0)
        self.assertEqual(list(rows[0]['marker_box']), [10, 100, 17, 108])
        self.assertEqual(list(rows[0]['next_box']), [20, 75, 25, 83])

    def test_same_line_markers_and_small_baseline_variation_are_not_breaks(self):
        for marker in '★①②③④⑤':
            sample = [(marker, (10, 100, 17, 108)), (' ', None), ('w', (800, 98, 806, 106))]
            self.assertEqual(m.marker_breaks(sample), [])
        self.assertEqual(m.marker_breaks([('★', None), ('w', (1, 10, 5, 18))]), [])

    def test_standalone_answer_marker_does_not_require_next_paragraph_binding(self):
        path=self.root/'marker-context.docx'
        xml=('<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
             '<w:body><w:p><w:r><w:t>1. ③</w:t></w:r></w:p>'
             '<w:p><w:r><w:t>미니 모의고사</w:t></w:r></w:p>'
             '<w:p><w:r><w:t>★\u00a0useful / ①\u00a0benefit</w:t></w:r></w:p></w:body></w:document>')
        with ZipFile(path,'w') as archive:archive.writestr('word/document.xml',xml)
        prefixes=m.marker_following_prefixes(path)
        self.assertEqual(prefixes['③'],set())
        sample=chars('③',100,108)+chars('미니',75,83)
        self.assertEqual(m.marker_breaks(sample,prefixes),[])
        sample=chars('①',100,108)+chars('benefit',75,83)
        self.assertEqual(len(m.marker_breaks(sample,prefixes)),1)

    def test_exact_canonical_checks_and_equal_pdf_are_never_visual_certification(self):
        before = {name: path.read_bytes() for name, path in self.paths.items()}
        result = self.result()
        self.assertEqual(result['status'], 'NOT_CERTIFIED')
        self.assertEqual(result['machine_status'], 'PASS', result['errors'])
        self.assertTrue(result['pdf']['normalized_text_equal'])
        self.assertEqual(result['independent_review'], 'NOT_PERFORMED')
        self.assertEqual(result['visual_review'], 'NOT_PERFORMED')
        self.assertNotIn('text', result['pdf'])
        self.assertEqual(before, {name: path.read_bytes() for name, path in self.paths.items()})
        self.assertTrue({name + '_sha256' for name in self.paths} <= set(result['bindings']))
        self.assertEqual(len(result['bindings']['package_sha256']), 64)

    def test_pdf_whitespace_normalization_does_not_weaken_exact_final_comparison(self):
        expected = m.plan_text(self.plan)
        observed = ' \n\u00a0'.join(expected)
        learning = self.original['learning_final'].decode('utf-8-sig')
        self.paths['learning_final'].write_bytes((learning + ' ').encode('utf-8'))
        result = self.result(self.pdf_report(observed))
        self.assertTrue(result['pdf']['normalized_text_equal'])
        self.assertEqual(result['machine_status'], 'FAIL')
        self.assertIn({'code': 'FINAL_MISMATCH', 'detail': 'learning'}, result['errors'])

    def test_saved_docx_mutation_remains_an_error_even_if_pdf_text_matches(self):
        path = self.paths['docx']
        with ZipFile(path) as archive:
            parts = [(entry, archive.read(entry.filename)) for entry in archive.infolist()]
        with ZipFile(path, 'w') as archive:
            for entry, content in parts:
                if entry.filename == 'word/document.xml':
                    tree = etree.fromstring(content)
                    node = tree.find('.//{*}sdtContent/{*}p/{*}r/{*}t')
                    self.assertIsNotNone(node)
                    node.text = 'Changed saved DOCX content'
                    content = etree.tostring(tree, encoding='utf-8', xml_declaration=True)
                archive.writestr(entry, content)
        result = self.result()
        self.assertTrue(result['pdf']['normalized_text_equal'])
        self.assertEqual(result['machine_status'], 'FAIL')
        self.assertTrue(any(row['code'] == 'SAVED_DOCX' for row in result['errors']))

    def test_plan_mismatch_remains_an_error(self):
        changed = deepcopy(self.plan)
        changed['unexpected_metadata'] = 'Changed canonical plan'
        self.paths['plan'].write_text(json.dumps(changed, ensure_ascii=False), encoding='utf-8')
        result = self.result()
        self.assertEqual(result['machine_status'], 'FAIL')
        self.assertTrue(any(row['code'] == 'PLAN_MISMATCH' for row in result['errors']))

    def test_pdf_differences_are_bounded_warnings_requiring_actual_review(self):
        result = self.result(self.pdf_report('Extracted glyph difference ' + 'x' * 1000))
        self.assertEqual(result['machine_status'], 'PASS', result['errors'])
        self.assertEqual(result['status'], 'NOT_CERTIFIED')
        warning = next(row for row in result['warnings'] if row['code'] == 'PDF_TEXT_DIFFERENCE')
        self.assertTrue(warning['id'].startswith('R-'))
        self.assertLessEqual(len(warning['detail']['expected']), 100)
        self.assertLessEqual(len(warning['detail']['observed']), 100)
        self.assertEqual(result['visual_review'], 'NOT_PERFORMED')

    def test_punctuation_glyph_changes_are_not_normalized_away(self):
        expected = m.plan_text(self.plan)
        result = self.result(self.pdf_report(expected + '\ufffe'))
        self.assertFalse(result['pdf']['normalized_text_equal'])
        self.assertTrue(any(row['code'] == 'PDF_TEXT_DIFFERENCE' for row in result['warnings']))
        self.assertEqual(result['machine_status'], 'PASS')

    def test_marker_candidates_keep_page_and_font_inventory_has_no_whitelist_failure(self):
        candidate = {'marker': '①', 'character_index': 12, 'next_character': 'W',
                     'marker_box': [10, 100, 17, 108], 'next_box': [20, 75, 25, 83]}
        result = self.result(self.pdf_report(candidates=[candidate], fonts=['CambriaMath', 'ABCDEE+Symbol']))
        self.assertEqual(result['machine_status'], 'PASS')
        self.assertIn('ABCDEE+Symbol', result['pdf']['fonts'])
        warning = next(row for row in result['warnings'] if row['code'] == 'PDF_MARKER_BREAK')
        self.assertEqual(warning['detail']['page'], 1)
        self.assertEqual(warning['detail']['marker_break_candidates'][0], candidate)

    def test_optional_pdf_dependency_failure_is_a_noncertifying_warning(self):
        result = self.result(side_effect=ImportError('Synthetic unavailable PDF dependency'))
        self.assertEqual(result['status'], 'NOT_CERTIFIED')
        self.assertEqual(result['machine_status'], 'PASS')
        self.assertTrue(any(row['code'] == 'PDF_EXTRACTION_UNVERIFIED' for row in result['warnings']))
        self.assertEqual(result['visual_review'], 'NOT_PERFORMED')

    def test_invalid_manuscript_structure_returns_fail_not_an_uncaught_exception(self):
        data = json.loads(self.original['manuscript'].decode('utf-8-sig'))
        data['schema_version'] = 999
        self.paths['manuscript'].write_text(json.dumps(data, ensure_ascii=False), encoding='utf-8')
        result = self.result()
        self.assertEqual(result['status'], 'NOT_CERTIFIED')
        self.assertEqual(result['machine_status'], 'FAIL')
        self.assertTrue(result['errors'])

    def test_normal_answer_prompt_is_only_a_review_candidate_not_a_hard_failure(self):
        # Canonical machinery is exercised by the other mutation tests. This
        # focused case controls a normal prompt to test the candidate boundary.
        plan = {'blocks': [{'id': 'normal-question', 'elements': [
            {'kind': 'paragraph', 'role': 'mock_question_prompt', 'runs': [{'text': '정답을 고르시오. 예시를 읽으시오.'}]}]}]}
        self.paths['plan'].write_text(json.dumps(plan, ensure_ascii=False), encoding='utf-8')
        with patch.object(m, 'compile_plan', return_value=deepcopy(plan)), \
                patch.object(m, 'check_saved', return_value={'status': 'SAVED_CONTENT_MATCH', 'errors': [], 'format_errors': []}), \
                patch.object(m, 'inspect_pdf', return_value=self.pdf_report(m.plan_text(plan))):
            result = m.check_files(**self.paths)
        self.assertEqual(result['machine_status'], 'PASS', result['errors'])
        self.assertTrue(any(row['code'] == 'STUDENT_ANSWER_TEXT_CANDIDATE' for row in result['warnings']))
        self.assertTrue(any(row['code'] == 'PLACEHOLDER_CANDIDATE' for row in result['warnings']))

    def test_cli_writes_only_a_new_report_and_refuses_inputs_and_existing_files(self):
        output = self.root / 'release-text-report.json'
        arguments = [str(self.paths[name]) for name in
                     ('manuscript', 'plan', 'docx', 'pdf', 'learning_final', 'assessment_final')]
        with patch.object(sys, 'argv', ['check_release_text.py', *arguments, str(output)]), \
                patch.object(m, 'inspect_pdf', return_value=self.pdf_report()), \
                contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(m.main(), 0)
        self.assertEqual(json.loads(output.read_text(encoding='utf-8'))['status'], 'NOT_CERTIFIED')
        original_report = output.read_bytes()
        for denied in [output, *self.paths.values()]:
            before = denied.read_bytes()
            with patch.object(sys, 'argv', ['check_release_text.py', *arguments, str(denied)]), self.assertRaises(ValueError):
                m.main()
            self.assertEqual(denied.read_bytes(), before)
        self.assertEqual(output.read_bytes(), original_report)


if __name__ == '__main__':
    unittest.main()
