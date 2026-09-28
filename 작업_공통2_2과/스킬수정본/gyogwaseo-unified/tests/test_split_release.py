"""Synthetic six-DOCX release gates; receipts here are never real review evidence."""
from copy import deepcopy
import json
from pathlib import Path
import unittest
from unittest.mock import patch

import test_release
import test_review_release_integration
from split_book import export, VOLUME_KINDS
from split_release_support import check_split_evidence
import verify_split_release


class SplitReleaseTests(unittest.TestCase):
    def setUp(self):
        self.fixture = test_release.ReleaseTests(methodName='runTest')
        self.fixture.setUp()
        self.record = self.fixture.record
        self.record['delivery_mode'] = 'integrated_plus_five_docx'
        self.manifest = export(self.record['artifacts']['docx']['path'],
                               self.record['artifacts']['plan']['path'],
                               self.fixture.folder / 'six-deliverables',
                               '혼공독해교재_공통영어2_능률(민)_1과')
        self.record['artifacts']['split_manifest'] = self.save('split-manifest.json', self.manifest)
        self.record['reports']['split_word_renders'] = []
        for volume in self.manifest['volumes']:
            kind = volume['kind']
            pdf = self.fixture.folder / (kind + '.pdf')
            pdf.write_bytes(test_release.blank_pdf())
            receipt = {'status': 'PASS', 'renderer': 'Microsoft Word',
                       'version': 'SYNTHETIC-NO-WORD-EXECUTED',
                       'execution_id': 'SYNTHETIC-render-' + kind,
                       'source_unchanged': True, 'source_sha256': volume['sha256'],
                       'pdf_sha256': self.fixture.ref(pdf)['sha256'], 'pages': 1}
            self.record['reports']['split_word_renders'].append({
                'kind': kind, 'pdf': self.fixture.ref(pdf),
                'receipt': self.save(kind + '-word.json', receipt)})
        files = {key: (Path(ref['path']), Path(ref['path']).read_bytes(), ref['sha256'])
                 for key, ref in self.record['artifacts'].items()}
        with patch.object(test_release.m, 'pdf_pages', return_value=1):
            split = check_split_evidence(self.manifest, self.record['reports'], files, self.fixture.folder)
        self.assertEqual(split['errors'] + split['pending'], [])
        self.bindings = {name + '_sha256': ref['sha256'] for name, ref in self.record['artifacts'].items()}
        self.bindings.update(package_sha256=self.record['package']['sha256'],
                             **test_release.m.content_digests(self.fixture.data), **split['bindings'])
        for index, ref in enumerate(self.record['reviews']):
            def update(row, index=index):
                row['bindings'] = deepcopy(self.bindings)
                if index in (2, 3):
                    row['role'] = 'M' if index == 2 else 'N'
            self.fixture.change(ref, update)
        template = self.read(self.record['reviews'][4])
        self.word_bundle = {'schema_version': 1, 'type': 'review_bundle',
                            'kind': 'word_layout', 'role': 'JK', 'id': 'SYNTHETIC-six-volume-JK',
                            'summary': 'Synthetic full plus five visual coverage, not actual review.',
                            'scope': template['scope'], 'bindings': deepcopy(self.bindings),
                            'word_pages': 6, 'children': []}
        for role, pages in [('J', [1, 2, 3]), ('K', [4, 5, 6])]:
            row = deepcopy(template)
            row.update(schema_version=1, type='review_shard', role=role,
                       id='SYNTHETIC-' + role, reviewer_id='SYNTHETIC-reviewer-' + role,
                       execution_id='SYNTHETIC-execution-' + role,
                       scope={'kind': 'partial', 'pages': pages}, pages_reviewed=pages,
                       detail_pages=pages, context_pages=[], boundaries=[])
            self.word_bundle['children'].append(self.save('six-review-' + role + '.json', row))
        self.record['reviews'][4] = self.save('six-JK-bundle.json', self.word_bundle)

    def tearDown(self):
        self.fixture.tearDown()

    def read(self, ref):
        return json.loads(Path(ref['path']).read_text(encoding='utf-8'))

    def save(self, name, row):
        return self.fixture.ref(self.fixture.put(name, row))

    def gate(self):
        with patch.object(test_release.m, 'pdf_pages', return_value=1):
            return verify_split_release.verify(self.record, self.fixture.folder)

    def assert_blocks(self, code):
        result = self.gate()
        self.assertNotEqual(result['status'], 'READY_FOR_RELEASE', result)
        self.assertIn(code, {r['code'] for r in result['errors'] + result['pending']}, result)

    def change_child(self, index, mutate):
        self.fixture.change(self.word_bundle['children'][index], mutate)
        self.record['reviews'][4] = self.save('six-JK-bundle.json', self.word_bundle)

    def test_complete_current_six_saved_files_connect_without_pdf_delivery(self):
        result = self.gate()
        self.assertEqual(result['status'], 'READY_FOR_RELEASE', result)
        self.assertEqual([x['kind'] for x in result['docx_files']], ['integrated', *VOLUME_KINDS])
        self.assertTrue(all(x['path'].endswith('.docx') for x in result['docx_files']))
        self.assertEqual(len(result['delivery_files']), 1)
        self.assertTrue(result['delivery_files'][0]['path'].endswith('.zip'))
        self.assertEqual(len(result['word_page_map']), 6)
        self.assertEqual(result['word_pages'], 6)

    def test_explicit_mode_is_required_and_legacy_entry_cannot_accept_it(self):
        self.record.pop('delivery_mode')
        self.assert_blocks('DELIVERY_MODE')
        self.record['delivery_mode'] = 'integrated_plus_five_docx'
        with patch.object(test_release.m, 'pdf_pages', return_value=1):
            result = test_release.m.verify(self.record, self.fixture.folder)
        self.assertNotEqual(result['status'], 'READY_FOR_RELEASE')
        self.assertIn('DELIVERY_MODE', {x['code'] for x in result['errors']})

    def test_changed_saved_volume_does_not_inherit_integrated_pass(self):
        path = Path(self.manifest['volumes'][0]['path'])
        path.write_bytes(path.read_bytes() + b'changed')
        self.assert_blocks('SPLIT_CONTENT_MISMATCH')

    def test_missing_split_word_evidence_is_pending(self):
        self.record['reports'].pop('split_word_renders')
        self.assert_blocks('SPLIT_WORD_RENDERS_MISSING')

    def test_integrated_word_receipt_cannot_stand_for_a_split_volume(self):
        self.record['reports']['split_word_renders'][0]['receipt'] = self.record['reports']['word_render']
        self.assert_blocks('SPLIT_WORD_RENDER_MISMATCH')

    def test_unperformed_word_render_blocks_even_if_docx_structural_check_passes(self):
        self.fixture.change(self.record['reports']['split_word_renders'][0]['receipt'],
                            lambda r: r.update(status='NOT_PERFORMED'))
        self.assert_blocks('SPLIT_WORD_NOT_PERFORMED')

    def test_stale_internal_split_pdf_blocks(self):
        path = Path(self.record['reports']['split_word_renders'][0]['pdf']['path'])
        path.write_bytes(path.read_bytes() + b'changed')
        self.assert_blocks('SPLIT_EVIDENCE_STALE')

    def test_sixth_file_visual_coverage_cannot_be_omitted(self):
        self.change_child(1, lambda r: r.update(scope={'kind': 'partial', 'pages': [4, 5]},
                                               pages_reviewed=[4, 5], detail_pages=[4, 5]))
        self.assert_blocks('REVIEW_COVERAGE_MISSING')

    def test_word_two_roles_require_actual_distinct_identities(self):
        self.change_child(1, lambda r: r.update(reviewer_id='SYNTHETIC-reviewer-J'))
        self.assert_blocks('REVIEW_NOT_INDEPENDENT')

    def test_old_release_review_without_split_bindings_blocks(self):
        self.fixture.change(self.record['reviews'][5], lambda r: r['bindings'].pop('volume_set_sha256'))
        self.assert_blocks('REVIEW_STALE_BINDINGS')

    def test_blind_question_requirement_is_unchanged(self):
        self.fixture.change(self.record['reviews'][2], lambda r: r.update(solved_before_answer_key=False))
        self.assert_blocks('ANSWERS_NOT_BLIND')

    def test_unlinked_user_request_ledger_still_blocks(self):
        self.fixture.put('사용자수정요청.json', {'schema_version': 1})
        self.assert_blocks('USER_FEEDBACK_LINK_MISSING')

    def test_malformed_manifest_input_reference_returns_structured_failure(self):
        self.fixture.change(self.record['artifacts']['split_manifest'], lambda m: m.update(source_docx=[]))
        self.assert_blocks('SPLIT_INPUT_MISMATCH')

    def test_current_integrated_diagnostic_remains_valid_supplement(self):
        helper = test_review_release_integration.ReviewReleaseIntegrationTests
        report = helper.release_text(self)
        helper.resolve_release_text(self, report)
        result = self.gate()
        self.assertEqual(result['status'], 'READY_FOR_RELEASE', result)
        self.assertEqual(len(result['docx_files']), 6)

    def test_stale_integrated_diagnostic_still_blocks(self):
        helper = test_review_release_integration.ReviewReleaseIntegrationTests
        report = helper.release_text(self)
        helper.resolve_release_text(self, report)
        self.fixture.change(self.record['reports']['release_text'], lambda r: r['pdf'].update(fonts=['FORGED']))
        self.assert_blocks('RELEASE_TEXT_REPORT_MISMATCH')

    def test_changed_delivery_zip_cannot_inherit_six_docx_pass(self):
        path = Path(self.manifest['delivery_zip']['path'])
        path.write_bytes(path.read_bytes() + b'changed')
        self.assert_blocks('SPLIT_CONTENT_MISMATCH')

    def test_old_r_without_delivery_zip_binding_blocks(self):
        self.fixture.change(self.record['reviews'][5], lambda r: r['bindings'].pop('delivery_zip_sha256'))
        self.assert_blocks('REVIEW_STALE_BINDINGS')


if __name__ == '__main__':
    unittest.main()
