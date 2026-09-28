"""Synthetic bundle integration with the complete release gate, never real reviews."""
from copy import deepcopy
import json
from pathlib import Path
import unittest
from unittest.mock import patch
from zipfile import ZipFile

import test_release
import check_release_text


class ReviewReleaseIntegrationTests(unittest.TestCase):
    def setUp(self):
        # Module-qualified composition avoids collecting/inheriting the legacy
        # suite again while retaining its real manuscript, DOCX and full gate.
        self.fixture = test_release.ReleaseTests(methodName='runTest')
        self.fixture.setUp()
        self.record = self.fixture.record
        self.data = self.fixture.data
        self.pages = 1

    def read(self, ref):
        return json.loads(Path(ref['path']).read_text(encoding='utf-8'))

    def save(self, name, value):
        return self.fixture.ref(self.fixture.put(name, value))

    def run_gate(self):
        with patch.object(test_release.m, 'pdf_pages', return_value=self.pages):
            return test_release.m.verify(self.record, self.fixture.folder)

    def assert_failure(self, code):
        result = self.run_gate()
        self.assertNotEqual(result['status'], 'READY_FOR_RELEASE')
        self.assertIn(code, {row['code'] for row in result['errors'] + result['pending']},
                      result['errors'] + result['pending'])
        return result

    def base_bundle(self, kind, role, template):
        return {'schema_version': 1, 'type': 'review_bundle', 'kind': kind, 'role': role,
                'id': 'SYNTHETIC-bundle-' + role, 'summary': 'Synthetic bundle gate integration.',
                'scope': deepcopy(template['scope']), 'bindings': deepcopy(template['bindings']), 'children': []}

    def child(self, template, role, suffix, scope):
        row = deepcopy(template)
        row.update(schema_version=1, type='review_shard', role=role, scope=scope,
                   id='SYNTHETIC-child-' + suffix, reviewer_id='SYNTHETIC-reviewer-' + suffix,
                   execution_id='SYNTHETIC-execution-' + suffix)
        return row

    def questions(self, index, role):
        template = self.read(self.record['reviews'][index])
        bundle = self.base_bundle('questions', role, template)
        set_ids = list(dict.fromkeys(q['set_id'] for q in self.data['assessment']['questions']))
        for set_id in set_ids:
            qids = [q['id'] for q in self.data['assessment']['questions'] if q['set_id'] == set_id]
            suffix = role + '-' + set_id
            row = self.child(template, role, suffix, {'kind': 'partial', 'question_ids': qids})
            row['answers'] = {qid: template['answers'][qid] for qid in qids}
            row['length_reviews'] = {qid: item for qid, item in template['length_reviews'].items() if qid in qids}
            bundle['children'].append(self.save('child-' + suffix + '.json', row))
        self.record['reviews'][index] = self.save('bundle-' + role + '.json', bundle)

    def question_pair(self):
        self.questions(2, 'M')
        self.questions(3, 'N')

    def change_child(self, index, child_index, mutate):
        ref = self.record['reviews'][index]
        bundle = self.read(ref)
        self.fixture.change(bundle['children'][child_index], mutate)
        self.fixture.change(ref, lambda current: current.update(children=bundle['children']))

    def learning(self):
        template = self.read(self.record['reviews'][1])
        bundle = self.base_bundle('learning', 'L', template)
        for unit in self.data['units']:
            suffix = 'L-' + unit['id']
            row = self.child(template, 'L', suffix, {'kind': 'partial', 'source_ids': [unit['source_id']],
                'unit_ids': [unit['id']], 'sentence_ids': unit['sentence_ids']})
            bundle['children'].append(self.save('child-' + suffix + '.json', row))
        continuity = self.child(template, 'L', 'L-continuity', deepcopy(template['scope']))
        continuity['type'] = 'learning_continuity'
        bundle['continuity'] = self.save('continuity.json', continuity)
        self.record['reviews'][1] = self.save('bundle-L.json', bundle)

    def word(self):
        self.pages = 4
        self.fixture.change(self.record['reports']['word_render'], lambda r: r.update(pages=4))
        template = self.read(self.record['reviews'][4])
        bundle = self.base_bundle('word_layout', 'JK', template)
        bundle['pdf_pages'] = 4
        for role, owned, context, pairs in [('J', [1, 2], [3], [[1, 2], [2, 3]]),
                                             ('K', [3, 4], [2], [[3, 4]])]:
            row = self.child(template, role, role, {'kind': 'partial', 'pages': owned})
            row.update(pages_reviewed=owned, detail_pages=[owned[0]], context_pages=context,
                       boundaries=[{'pages': pair, 'status': 'PASS',
                                    'summary': 'Synthetic boundary receipt.'} for pair in pairs])
            bundle['children'].append(self.save('child-' + role + '.json', row))
        self.record['reviews'][4] = self.save('bundle-JK.json', bundle)

    def release_text(self):
        # Only PDF extraction is synthetic. Canonical manuscript, plan, DOCX
        # and FINAL comparisons run normally in both preparation and release.
        def synthetic_pdf(*_):
            return {'text': '', 'fonts': ['SYNTHETIC-font'],
                    'pages': [{'page': 1, 'characters': 0, 'fonts': ['SYNTHETIC-font'],
                               'marker_break_candidates': []}],
                    'footer_policy': 'Synthetic test extraction; not actual visual evidence'}
        patcher = patch.object(check_release_text, 'inspect_pdf', side_effect=synthetic_pdf)
        patcher.start()
        self.addCleanup(patcher.stop)
        names = ('manuscript', 'plan', 'docx', 'pdf', 'learning_final', 'assessment_final')
        report = check_release_text.check_files(**{name: self.record['artifacts'][name]['path'] for name in names})
        self.assertEqual(report['errors'], [])
        self.assertEqual(report['status'], 'NOT_CERTIFIED')
        self.assertTrue(report['warnings'])
        self.record['reports']['release_text'] = self.save('release-text.json', report)
        return report

    def resolve_release_text(self, report):
        dispositions = {row['id']: {'status': 'resolved',
            'resolution': 'Synthetic unit-test disposition, not a real review claim.',
            'recheck': 'Synthetic evidence exercises the gate schema only.'} for row in report['warnings']}
        self.fixture.change(self.record['reviews'][5], lambda r: r.update(release_text_dispositions=dispositions))

    def test_current_question_bundles_pass_with_all_existing_full_gates(self):
        self.question_pair()
        result = self.run_gate()
        self.assertEqual(result['status'], 'READY_FOR_RELEASE', result['errors'] + result['pending'])
        self.assertEqual(len(result['review_contributors']), 8)
        self.assertEqual(result['scope'], 'full')
        self.assertIn('structure', ' '.join(result['checked_artifacts']))

    def test_real_reviewer_or_execution_reused_across_m_n_is_rejected(self):
        self.question_pair()
        m_child = self.read(self.read(self.record['reviews'][2])['children'][0])
        n_original = self.read(self.read(self.record['reviews'][3])['children'][0])
        for key in ['reviewer_id', 'execution_id']:
            self.change_child(3, 0, lambda r: r.update({key: m_child[key]}))
            self.assert_failure('QUESTION_REVIEWERS_NOT_DISTINCT')
            self.change_child(3, 0, lambda r: r.update({key: n_original[key]}))

    def test_same_actual_child_cannot_be_counted_in_multiple_bundles(self):
        self.question_pair()
        duplicate = self.read(self.record['reviews'][2])
        duplicate['id'] = 'SYNTHETIC-other-M-bundle'
        self.record['reviews'].append(self.save('other-M-bundle.json', duplicate))
        self.assert_failure('REVIEW_DUPLICATE_ID')

    def test_mixed_legacy_question_review_requires_explicit_role(self):
        self.questions(2, 'M')
        self.assert_failure('QUESTION_REVIEW_ROLES')
        self.fixture.change(self.record['reviews'][3], lambda r: r.update(role='N'))
        result = self.run_gate()
        self.assertEqual(result['status'], 'READY_FOR_RELEASE', result['errors'] + result['pending'])

    def test_mixed_legacy_cannot_reuse_bundle_actual_reviewer(self):
        self.questions(2, 'M')
        first = self.read(self.read(self.record['reviews'][2])['children'][0])
        self.fixture.change(self.record['reviews'][3], lambda r: r.update(role='N', reviewer_id=first['reviewer_id']))
        self.assert_failure('QUESTION_REVIEWERS_NOT_DISTINCT')

    def test_bundle_scope_and_current_child_bindings_are_enforced_by_full_gate(self):
        self.question_pair()
        reference = self.record['reviews'][2]
        original = self.read(reference)
        self.fixture.change(reference, lambda r: r['scope'].update(question_ids=[]))
        self.assert_failure('REVIEW_SCOPE')
        self.fixture.change(reference, lambda r: r.update(original))
        self.change_child(2, 0, lambda r: r['bindings'].pop('assessment_final_sha256'))
        self.assert_failure('REVIEW_STALE_BINDINGS')

    def test_missing_or_tampered_child_cannot_be_hidden_by_bundle_full_scope(self):
        self.question_pair()
        bundle = self.read(self.record['reviews'][2])
        path = Path(bundle['children'][0]['path'])
        raw = path.read_bytes()
        path.write_bytes(raw + b' ')
        self.assert_failure('REVIEW_CHILD_HASH')
        path.unlink()
        self.assert_failure('MISSING_REVIEW_CHILD')

    def test_valid_learning_and_word_bundles_preserve_all_full_gates(self):
        self.question_pair()
        self.learning()
        self.word()
        result = self.run_gate()
        self.assertEqual(result['status'], 'READY_FOR_RELEASE', result['errors'] + result['pending'])
        self.assertEqual(result['pdf_pages'], 4)
        kinds = {row['kind'] for row in result['review_contributors']}
        self.assertTrue({'questions', 'learning', 'learning_continuity', 'word_layout'} <= kinds)
        self.fixture.change(self.record['reviews'][0], lambda r: r.update(status='NOT_PERFORMED'))
        self.assert_failure('REVIEW_PENDING')
        self.fixture.change(self.record['reviews'][0], lambda r: r.update(status='PASS'))
        self.fixture.change(self.record['reviews'][5], lambda r: r.update(status='NOT_PERFORMED'))
        self.assert_failure('REVIEW_PENDING')

    def test_source_declaration_and_independent_boundary_overlap_pass_full_gate(self):
        self.question_pair()
        self.word()
        self.fixture.change(self.record['reviews'][0], lambda r: (r.pop('findings'), r.update(no_findings=True)))
        self.change_child(4, 1, lambda r: r['boundaries'].append(
            {'pages': [2, 3], 'status': 'PASS', 'summary': 'Synthetic independent repeated observation.'}))
        bundle = self.read(self.record['reviews'][4])
        refs = [self.record['reviews'][0], self.record['reviews'][4], *bundle['children']]
        before = {ref['path']: Path(ref['path']).read_bytes() for ref in refs}
        result = self.run_gate()
        self.assertEqual(result['status'], 'READY_FOR_RELEASE', result['errors'] + result['pending'])
        contributors = {r['id']: r for r in result['review_contributors'] if r['kind'] == 'word_layout'}
        for ref in bundle['children']:
            child = self.read(ref)
            self.assertEqual(contributors[child['id']]['sha256'], ref['sha256'])
            self.assertEqual(contributors[child['id']]['path'], str(Path(ref['path']).resolve()))
            self.assertIn([2, 3], contributors[child['id']]['boundaries_reviewed'])
        for path, raw in before.items():
            self.assertEqual(Path(path).read_bytes(), raw)
        self.change_child(4, 1, lambda r: r['boundaries'][-1].update(status='PENDING'))
        pending = self.run_gate()
        self.assertEqual(pending['status'], 'REVIEW_PENDING', pending['errors'])
        self.assertIn('WORD_BOUNDARY_PENDING', {r['code'] for r in pending['pending']})

    def test_duplicate_observation_inside_receipt_stays_fail_through_full_gate(self):
        self.question_pair()
        self.word()
        self.change_child(4, 0, lambda r: r['boundaries'].append(deepcopy(r['boundaries'][-1])))
        result = self.assert_failure('REVIEW_COVERAGE_DUPLICATE')
        self.assertEqual(result['status'], 'FAIL')
        self.assertIn('REVIEW_COVERAGE_DUPLICATE', {r['code'] for r in result['errors']})

    def test_bundles_cannot_skip_current_final_content_gate(self):
        self.question_pair()
        final = self.record['artifacts']['learning_final']
        path = Path(final['path'])
        path.write_bytes(path.read_bytes() + b'\nSynthetic divergence')
        final.update(self.fixture.ref(path))
        self.assert_failure('FINAL_CONTENT_MISMATCH')

    def test_bundles_cannot_skip_current_saved_docx_gate(self):
        self.question_pair()
        docx = self.record['artifacts']['docx']
        path = Path(docx['path'])
        with ZipFile(path) as archive:
            parts = {name: archive.read(name) for name in archive.namelist()}
        self.assertIn(b'Shared Layout Test', parts['word/document.xml'])
        parts['word/document.xml'] = parts['word/document.xml'].replace(
            b'Shared Layout Test', b'Synthetic Incorrect Cover', 1)
        with ZipFile(path, 'w') as archive:
            for name, raw in parts.items():
                archive.writestr(name, raw)
        docx.update(self.fixture.ref(path))
        self.assert_failure('CURRENT_SAVED_FAIL')

    def test_invalid_child_identity_does_not_enter_global_identity_sets(self):
        self.question_pair()
        self.change_child(2, 0, lambda r: r.update(id=[]))
        self.assert_failure('MISSING_REVIEW_DETAIL')

    def test_invalid_child_hash_still_protects_its_file_from_report_output(self):
        self.question_pair()
        ref = self.record['reviews'][2]
        bundle = self.read(ref)
        protected_path = str(Path(bundle['children'][0]['path']).resolve())
        bundle['children'][0].pop('sha256')
        self.fixture.change(ref, lambda r: r.update(bundle))
        result = self.assert_failure('REVIEW_BUNDLE_SCHEMA')
        self.assertIn(protected_path, result['protected_paths'])

    def test_corrupt_docx_returns_current_saved_failure_without_crashing(self):
        self.question_pair()
        ref = self.record['artifacts']['docx']
        path = Path(ref['path'])
        path.write_bytes(b'Synthetic broken ZIP container')
        ref.update(self.fixture.ref(path))
        self.assert_failure('CURRENT_SAVED_FAIL')

    def test_optional_release_text_is_recomputed_and_unresolved_warnings_remain_pending(self):
        self.question_pair()
        self.release_text()
        with patch.object(check_release_text, 'check_files', wraps=check_release_text.check_files) as fresh:
            result = self.assert_failure('RELEASE_TEXT_REVIEW_PENDING')
            self.assertEqual(fresh.call_count, 1)
        self.assertEqual(result['status'], 'REVIEW_PENDING', result['errors'])

    def test_optional_release_text_with_actual_disposition_fields_can_pass_full_gate(self):
        self.question_pair()
        report = self.release_text()
        self.resolve_release_text(report)
        result = self.run_gate()
        self.assertEqual(result['status'], 'READY_FOR_RELEASE', result['errors'] + result['pending'])
        self.assertEqual(self.read(self.record['reports']['release_text'])['independent_review'], 'NOT_PERFORMED')

    def test_optional_release_text_content_tampering_fails_even_with_updated_file_hash(self):
        self.question_pair()
        report = self.release_text()
        self.resolve_release_text(report)
        self.fixture.change(self.record['reports']['release_text'], lambda r: r['pdf'].update(fonts=['FORGED-font']))
        self.assert_failure('RELEASE_TEXT_REPORT_MISMATCH')

    def test_word_current_pdf_count_pages_and_boundaries_remain_mandatory(self):
        self.question_pair()
        self.word()
        ref = self.record['reviews'][4]
        original = self.read(ref)
        self.fixture.change(ref, lambda r: r.pop('pdf_pages'))
        self.assert_failure('WORD_VISUAL_COVERAGE')
        self.fixture.change(ref, lambda r: r.update(original))
        self.change_child(4, 1, lambda r: r.update(scope={'kind': 'partial', 'pages': [3]},
                         pages_reviewed=[3], context_pages=[2, 4]))
        self.assert_failure('REVIEW_COVERAGE_MISSING')

    def test_standalone_shard_cannot_satisfy_review_minimum(self):
        self.questions(2, 'M')
        bundle = self.read(self.record['reviews'][2])
        self.record['reviews'][2] = bundle['children'][0]
        self.assert_failure('REVIEW_BUNDLE_REQUIRED')

    def test_shared_passage_question_split_is_rejected_through_full_gate(self):
        self.question_pair()
        ref = self.record['reviews'][2]
        bundle = self.read(ref)
        group = self.data['assessment']['passage_groups'][0]
        moved_qid = group['question_ids'][0]
        owner_index = next(index for index, child in enumerate(bundle['children'])
                           if moved_qid in self.read(child)['scope']['question_ids'])
        owner = self.read(bundle['children'][owner_index])
        destination = self.read(bundle['children'][0])
        self.assertNotEqual(owner_index, 0)
        destination['scope']['question_ids'].append(moved_qid)
        destination['answers'][moved_qid] = owner['answers'].pop(moved_qid)
        owner['scope']['question_ids'].remove(moved_qid)
        if moved_qid in owner['length_reviews']:
            destination['length_reviews'][moved_qid] = owner['length_reviews'].pop(moved_qid)
        self.fixture.change(bundle['children'][0], lambda r: r.update(destination))
        self.fixture.change(bundle['children'][owner_index], lambda r: r.update(owner))
        self.fixture.change(ref, lambda r: r.update(bundle))
        self.assert_failure('QUESTION_SHARED_GROUP_SPLIT')


if __name__ == '__main__':
    unittest.main()
