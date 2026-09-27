"""Synthetic scope/hash enforcement only: these tests are not review evidence."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import sys
import unittest
import uuid

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'scripts'))
from review_coverage import REQUIRED_BINDINGS, validate_bundle


class ReviewCoverageTests(unittest.TestCase):
    def setUp(self):
        # Normal workspace mkdir preserves the host ACL; tempfile's private
        # Windows directory mode can make its own children inaccessible here.
        self.folder = HERE / ('release-test-' + uuid.uuid4().hex)
        self.folder.mkdir()
        self.addCleanup(self.cleanup)
        self.data = {
            'sources': [{'id': 'src'}],
            'units': [{'id': 'u1', 'source_id': 'src', 'sentence_ids': ['s1', 's2']},
                      {'id': 'u2', 'source_id': 'src', 'sentence_ids': ['s3']}],
            'sentences': [{'id': x} for x in ['s1', 's2', 's3']],
            'assessment': {'questions': [{'id': 'q1', 'answer': 2}, {'id': 'q2', 'answer': 4}]},
        }
        self.bindings = {key: hashlib.sha256(key.encode()).hexdigest()
                         for keys in REQUIRED_BINDINGS.values() for key in keys}
        self.producer = {'reviewer_id': 'SYNTHETIC-producer', 'execution_id': 'SYNTHETIC-production'}
        self.structure = {'status': 'STRUCTURE_PASS', 'independent_length_review_required': ['q2'],
                          'question_views': {qid: {'length_comparison': {'benchmark_ids': ['b1', 'b2']}}
                                             for qid in ['q1', 'q2']}}

    def cleanup(self):
        assert self.folder.resolve().parent == HERE.resolve()
        for path in self.folder.iterdir():
            path.unlink()
        self.folder.rmdir()

    def put(self, name, value):
        path = self.folder / name
        raw = (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
        path.write_bytes(raw)
        return {'path': name, 'sha256': hashlib.sha256(raw).hexdigest()}

    def change(self, ref, mutate):
        path = self.folder / ref['path']
        value = json.loads(path.read_text(encoding='utf-8'))
        mutate(value)
        ref.update(self.put(ref['path'], value))

    def receipt(self, kind, role, identity, scope, **extra):
        return {
            'schema_version': 1, 'type': 'review_shard', 'id': 'SYNTHETIC-' + identity,
            'kind': kind, 'role': role, 'status': 'PASS', 'scope': scope,
            'reviewer_id': 'SYNTHETIC-reviewer-' + identity,
            'execution_id': 'SYNTHETIC-execution-' + identity,
            'performed_at': '2026-09-24T00:00:00Z', 'independent': True,
            'method': 'Synthetic validation fixture, no actual review performed.',
            'summary': 'Synthetic scope enforcement only.',
            'bindings': deepcopy(self.bindings), 'findings': [], **extra,
        }

    def bundle(self, kind='learning', role=None):
        scope = {'kind': 'full', 'source_ids': ['src'], 'unit_ids': ['u1', 'u2']}
        if kind != 'learning':
            scope['question_ids'] = ['q1', 'q2']
        role = role or {'learning': 'L', 'questions': 'M', 'word_layout': 'JK'}[kind]
        bundle = {'schema_version': 1, 'type': 'review_bundle', 'kind': kind, 'role': role,
                  'id': 'SYNTHETIC-bundle-' + role, 'summary': 'Synthetic immutable shard references.',
                  'bindings': deepcopy(self.bindings), 'scope': scope, 'children': []}
        if kind == 'learning':
            for index, sids in enumerate([['s1', 's2'], ['s3']], 1):
                row = self.receipt(kind, role, 'L' + str(index),
                                   {'kind': 'partial', 'source_ids': ['src'],
                                    'unit_ids': ['u' + str(index)], 'sentence_ids': sids})
                bundle['children'].append(self.put('L' + str(index) + '.json', row))
            continuity = self.receipt(kind, role, 'continuity', deepcopy(scope), type='learning_continuity')
            bundle['continuity'] = self.put('continuity.json', continuity)
        elif kind == 'questions':
            for index, answer in enumerate([2, 4], 1):
                qid = 'q' + str(index)
                length = {qid: {'status': 'PASS', 'rationale': 'Synthetic independent length rationale.',
                                 'benchmark_ids': ['b1', 'b2']}} if index == 2 else {}
                row = self.receipt(kind, role, role + str(index), {'kind': 'partial', 'question_ids': [qid]},
                                   answers={qid: answer}, solved_before_answer_key=True, length_reviews=length)
                bundle['children'].append(self.put(role + str(index) + '.json', row))
        else:
            bundle['pdf_pages'] = 4
            for child_role, owned, context, pairs in [
                ('J', [1, 2], [3], [[1, 2], [2, 3]]), ('K', [3, 4], [2], [[3, 4]])
            ]:
                row = self.receipt(kind, child_role, child_role,
                    {'kind': 'partial', 'pages': owned}, renderer='Microsoft Word',
                    pages_reviewed=owned, detail_pages=[owned[0]], context_pages=context,
                    boundaries=[{'pages': pair, 'status': 'PASS', 'summary': 'Synthetic current boundary evidence.'}
                                for pair in pairs])
                bundle['children'].append(self.put(child_role + '.json', row))
        return bundle

    def check(self, bundle, **kwargs):
        return validate_bundle(bundle, self.data, self.bindings, kwargs.pop('page_count', 4),
                               self.producer, self.folder,
                               current_structure=kwargs.pop('current_structure', self.structure), **kwargs)

    def codes(self, bundle, **kwargs):
        report = self.check(bundle, **kwargs)
        self.assertIsNone(report['aggregate'])
        return {row['code'] for row in report['errors'] + report['pending']}

    def test_current_learning_shards_and_continuity_cover_all_units(self):
        report = self.check(self.bundle())
        self.assertEqual(report['errors'] + report['pending'], [])
        self.assertEqual(report['aggregate']['type'], 'review_aggregate')
        self.assertNotIn('reviewer_id', report['aggregate'])
        self.assertEqual(len(report['contributors']), 3)
        self.assertEqual(len(report['protected_paths']), 3)

    def test_current_question_shards_retain_actual_answers_and_contributors(self):
        for role in ['M', 'N']:
            report = self.check(self.bundle('questions', role))
            self.assertEqual(report['errors'] + report['pending'], [])
            self.assertEqual(report['aggregate']['answers'], {'q1': 2, 'q2': 4})
            self.assertTrue(report['aggregate']['solved_before_answer_key'])
            self.assertEqual([c['question_ids'] for c in report['contributors']], [['q1'], ['q2']])

    def test_current_word_partition_checks_every_page_and_connection(self):
        report = self.check(self.bundle('word_layout'))
        self.assertEqual(report['errors'] + report['pending'], [])
        self.assertEqual(report['aggregate']['pages_reviewed'], [1, 2, 3, 4])
        self.assertEqual({c['role'] for c in report['contributors']}, {'J', 'K'})

    def overlapping_word_bundle(self):
        bundle = self.bundle('word_layout')
        self.change(bundle['children'][1], lambda r: r['boundaries'].append(
            {'pages': [2, 3], 'status': 'PASS', 'summary': 'Synthetic independent second observation.'}))
        return bundle

    def test_independent_word_boundary_observations_union_without_rewriting_receipts(self):
        bundle = self.overlapping_word_bundle()
        originals = {ref['path']: (self.folder / ref['path']).read_bytes() for ref in bundle['children']}
        report = self.check(bundle)
        self.assertEqual(report['errors'] + report['pending'], [])
        self.assertEqual(report['aggregate']['boundaries_reviewed'], [[1, 2], [2, 3], [3, 4]])
        self.assertEqual(report['aggregate']['child_ids'], ['SYNTHETIC-J', 'SYNTHETIC-K'])
        for ref, contributor in zip(bundle['children'], report['contributors']):
            self.assertEqual((self.folder / ref['path']).read_bytes(), originals[ref['path']])
            self.assertEqual(contributor['sha256'], ref['sha256'])
            self.assertEqual(contributor['path'], str((self.folder / ref['path']).resolve()))
            self.assertIn([2, 3], contributor['boundaries_reviewed'])

    def test_same_receipt_repeating_a_boundary_is_still_an_error(self):
        bundle = self.overlapping_word_bundle()
        self.change(bundle['children'][0], lambda r: r['boundaries'].append(deepcopy(r['boundaries'][-1])))
        report = self.check(bundle)
        self.assertIsNone(report['aggregate'])
        self.assertIn('REVIEW_COVERAGE_DUPLICATE', {r['code'] for r in report['errors']})

    def test_repeated_boundary_cannot_reuse_actual_reviewer_or_execution(self):
        for identity in ['reviewer_id', 'execution_id']:
            with self.subTest(identity=identity):
                bundle = self.overlapping_word_bundle()
                first = json.loads((self.folder / bundle['children'][0]['path']).read_text(encoding='utf-8'))
                self.change(bundle['children'][1], lambda r: r.update({identity: first[identity]}))
                report = self.check(bundle)
                self.assertIsNone(report['aggregate'])
                codes = {r['code'] for r in report['errors']}
                self.assertIn('WORD_BOUNDARY_NOT_INDEPENDENT', codes)
                self.assertIn('REVIEW_NOT_INDEPENDENT', codes)

    def test_same_role_repeated_boundary_also_requires_distinct_actual_identity(self):
        bundle = self.bundle('word_layout')
        first = json.loads((self.folder / bundle['children'][0]['path']).read_text(encoding='utf-8'))
        second = deepcopy(first)
        second.update(id='SYNTHETIC-J2', execution_id='SYNTHETIC-execution-J2',
                      scope={'kind': 'partial', 'pages': [2]}, pages_reviewed=[2],
                      detail_pages=[2], context_pages=[1, 3])
        self.change(bundle['children'][0], lambda r: r.update(
            scope={'kind': 'partial', 'pages': [1]}, pages_reviewed=[1],
            context_pages=[2], boundaries=[r['boundaries'][0]]))
        bundle['children'].append(self.put('J2.json', second))
        report = self.check(bundle)
        self.assertIsNone(report['aggregate'])
        self.assertIn('WORD_BOUNDARY_NOT_INDEPENDENT', {r['code'] for r in report['errors']})
        self.change(bundle['children'][-1], lambda r: r.update(reviewer_id='SYNTHETIC-reviewer-J2'))
        self.assertEqual(self.check(bundle)['errors'], [])
        self.assertIsNotNone(self.check(bundle)['aggregate'])

    def test_pending_or_disagreeing_boundary_observation_cannot_hide_behind_pass(self):
        for status in ['PENDING', 'FAIL', 'NOT_PERFORMED', None]:
            with self.subTest(status=status):
                bundle = self.overlapping_word_bundle()
                self.change(bundle['children'][1], lambda r: r['boundaries'][-1].update(status=status))
                report = self.check(bundle)
                self.assertEqual(report['errors'], [])
                self.assertIsNone(report['aggregate'])
                self.assertIn('WORD_BOUNDARY_PENDING', {r['code'] for r in report['pending']})

    def test_independent_overlap_does_not_relax_page_access_types_or_current_evidence(self):
        for mutate, code in [
            (lambda r: r.update(context_pages=[]), 'WORD_BOUNDARY_COVERAGE'),
            (lambda r: r['boundaries'][-1].update(pages=[True, 2]), 'WORD_BOUNDARY_COVERAGE'),
            (lambda r: r['boundaries'][-1].update(pages=[3, 2]), 'WORD_BOUNDARY_COVERAGE'),
            (lambda r: r['boundaries'][-1].update(pages=[2, 2]), 'WORD_BOUNDARY_COVERAGE'),
            (lambda r: r['boundaries'][-1].update(summary=''), 'MISSING_REVIEW_DETAIL'),
            (lambda r: r['bindings'].update(pdf_sha256='0' * 64), 'REVIEW_STALE_BINDINGS'),
            (lambda r: r.update(id='SYNTHETIC-J'), 'REVIEW_DUPLICATE_ID'),
            (lambda r: r.update(scope={'kind': 'partial', 'pages': [2, 3, 4]},
                                pages_reviewed=[2, 3, 4], context_pages=[]), 'REVIEW_COVERAGE_DUPLICATE'),
        ]:
            with self.subTest(code=code):
                bundle = self.overlapping_word_bundle()
                self.change(bundle['children'][1], mutate)
                report = self.check(bundle)
                self.assertIsNone(report['aggregate'])
                self.assertIn(code, {r['code'] for r in report['errors']})

    def test_boundary_seen_only_as_context_has_no_actual_owner(self):
        bundle = self.bundle('word_layout')
        self.change(bundle['children'][0], lambda r: (
            r.update(context_pages=[3, 4]),
            r['boundaries'].append({'pages': [3, 4], 'status': 'PASS', 'summary': 'Synthetic context-only observation.'})))
        report = self.check(bundle)
        self.assertIsNone(report['aggregate'])
        self.assertIn('WORD_BOUNDARY_COVERAGE', {r['code'] for r in report['errors']})

    def test_no_findings_source_convenience_never_applies_to_shards(self):
        for kind in ['learning', 'questions', 'word_layout']:
            with self.subTest(kind=kind):
                bundle = self.bundle(kind)
                self.change(bundle['children'][0], lambda r: (r.pop('findings'), r.update(no_findings=True)))
                report = self.check(bundle)
                self.assertIsNone(report['aggregate'])
                self.assertIn('FINDINGS_REQUIRED', {r['code'] for r in report['errors']})

    def test_shared_passage_questions_require_one_owner_even_when_context_is_supplied(self):
        self.data['assessment']['passage_groups'] = [{'id': 'g1', 'question_ids': ['q1', 'q2']}]
        bundle = self.bundle('questions')
        self.change(bundle['children'][0], lambda r: r.update(context={'question_ids': ['q2']}))
        self.assertIn('QUESTION_SHARED_GROUP_SPLIT', self.codes(bundle))
        second = json.loads((self.folder / bundle['children'][1]['path']).read_text(encoding='utf-8'))
        self.change(bundle['children'][0], lambda r: r.update(
            scope={'kind': 'partial', 'question_ids': ['q1', 'q2']}, answers={'q1': 2, 'q2': 4},
            length_reviews=second['length_reviews'], context={}))
        bundle['children'].pop()
        report = self.check(bundle)
        self.assertEqual(report['errors'] + report['pending'], [])

    def test_missing_immutable_child_is_not_completed_coverage(self):
        bundle = self.bundle()
        (self.folder / bundle['children'][0]['path']).unlink()
        self.assertIn('MISSING_REVIEW_CHILD', self.codes(bundle))

    def test_tampering_without_rehash_is_rejected(self):
        bundle = self.bundle()
        path = self.folder / bundle['children'][0]['path']
        path.write_bytes(path.read_bytes() + b' ')
        self.assertIn('REVIEW_CHILD_HASH', self.codes(bundle))

    def test_missing_child_hash_is_rejected(self):
        bundle = self.bundle()
        bundle['children'][0].pop('sha256')
        self.assertIn('REVIEW_BUNDLE_SCHEMA', self.codes(bundle))
        self.assertIn(str((self.folder / 'L1.json').resolve()), self.check(bundle)['protected_paths'])

    def test_rehashed_old_receipt_still_cannot_bind_to_current_version(self):
        bundle = self.bundle()
        self.change(bundle['children'][0], lambda r: r['bindings'].update(learning_content_sha256='0' * 64))
        self.assertIn('REVIEW_STALE_BINDINGS', self.codes(bundle))

    def test_missing_required_stage_hash_rejected_at_bundle_and_child(self):
        for target in ['bundle', 'child']:
            bundle = self.bundle()
            if target == 'bundle':
                bundle['bindings'].pop('package_sha256')
            else:
                self.change(bundle['children'][0], lambda r: r['bindings'].pop('learning_final_sha256'))
            self.assertIn('REVIEW_STALE_BINDINGS', self.codes(bundle))

    def test_context_cannot_fill_missing_owned_learning_unit(self):
        bundle = self.bundle()
        bundle['children'].pop()
        self.change(bundle['children'][0], lambda r: r.update(context={'unit_ids': ['u2'], 'sentence_ids': ['s3']}))
        self.assertIn('REVIEW_COVERAGE_MISSING', self.codes(bundle))

    def test_unit_cannot_be_cut_at_arbitrary_sentence_boundary(self):
        bundle = self.bundle()
        self.change(bundle['children'][0], lambda r: r['scope'].update(sentence_ids=['s1']))
        self.assertIn('LEARNING_UNIT_SPLIT', self.codes(bundle))

    def test_unknown_context_and_duplicate_assigned_ids_are_rejected(self):
        bundle = self.bundle()
        self.change(bundle['children'][0], lambda r: r.update(context={'unit_ids': ['old-unit']}))
        self.assertIn('REVIEW_SCOPE', self.codes(bundle))
        bundle = self.bundle()
        self.change(bundle['children'][0], lambda r: r['scope'].update(unit_ids=['u1', 'u1']))
        self.assertIn('REVIEW_SCOPE', self.codes(bundle))

    def test_overlapping_owners_do_not_count_twice(self):
        bundle = self.bundle()
        row = self.receipt('learning', 'L', 'extra', {'kind': 'partial', 'source_ids': ['src'],
                           'unit_ids': ['u1'], 'sentence_ids': ['s1', 's2']})
        bundle['children'].append(self.put('extra.json', row))
        self.assertIn('REVIEW_COVERAGE_DUPLICATE', self.codes(bundle))

    def test_learning_whole_book_continuity_must_be_current_complete_and_independent(self):
        for mutate, code in [
            (lambda r: r['scope'].update(unit_ids=['u1']), 'LEARNING_CONTINUITY_SCOPE'),
            (lambda r: r['bindings'].update(package_sha256='0' * 64), 'REVIEW_STALE_BINDINGS'),
            (lambda r: r.update(reviewer_id=self.producer['reviewer_id']), 'REVIEW_NOT_INDEPENDENT'),
        ]:
            bundle = self.bundle()
            self.change(bundle['continuity'], mutate)
            self.assertIn(code, self.codes(bundle))

    def test_designated_learning_reviewer_can_perform_continuity_in_same_real_execution(self):
        bundle = self.bundle()
        first = json.loads((self.folder / bundle['children'][0]['path']).read_text(encoding='utf-8'))
        self.change(bundle['continuity'], lambda r: r.update(reviewer_id=first['reviewer_id'], execution_id=first['execution_id']))
        self.assertEqual(self.check(bundle)['errors'], [])

    def test_same_execution_with_different_reviewer_label_is_not_new_reviewer(self):
        bundle = self.bundle('questions')
        self.change(bundle['children'][1], lambda r: r.update(execution_id='SYNTHETIC-execution-M1'))
        codes = self.codes(bundle)
        self.assertIn('REVIEW_EXECUTION_DUPLICATE', codes)
        self.assertIn('REVIEW_EXECUTION_IDENTITY', codes)

    def test_producer_cannot_supply_independent_shard(self):
        for key in ['reviewer_id', 'execution_id']:
            bundle = self.bundle('questions')
            self.change(bundle['children'][0], lambda r: r.update({key: self.producer[key]}))
            self.assertIn('REVIEW_NOT_INDEPENDENT', self.codes(bundle))

    def test_answers_or_missing_blind_order_cannot_pass(self):
        for mutate, code in [
            (lambda r: r.update(answers={'q1': 3}), 'INDEPENDENT_ANSWERS'),
            (lambda r: r.update(answers={'q1': 2, 'q2': 4}), 'INDEPENDENT_ANSWERS'),
            (lambda r: r.update(solved_before_answer_key=False), 'ANSWERS_NOT_BLIND'),
        ]:
            bundle = self.bundle('questions')
            self.change(bundle['children'][0], mutate)
            self.assertIn(code, self.codes(bundle))

    def test_missing_current_length_requirements_cannot_silently_skip_check(self):
        self.assertIn('REVIEW_BUNDLE_CONTEXT', self.codes(self.bundle('questions'), current_structure=None))

    def test_required_length_evidence_and_current_benchmarks_are_preserved(self):
        for mutate, code in [
            (lambda r: r.update(length_reviews={}), 'LENGTH_REVIEW_PENDING'),
            (lambda r: r['length_reviews']['q2'].update(benchmark_ids=['old']), 'LENGTH_REVIEW_BENCHMARK_MISMATCH'),
            (lambda r: r['length_reviews']['q2'].update(rationale=''), 'MISSING_REVIEW_DETAIL'),
        ]:
            bundle = self.bundle('questions')
            self.change(bundle['children'][1], mutate)
            self.assertIn(code, self.codes(bundle))

    def test_open_findings_and_unperformed_review_remain_pending(self):
        bundle = self.bundle()
        self.change(bundle['children'][0], lambda r: r.update(status='NOT_PERFORMED', findings=[
            {'id': 'f1', 'status': 'open', 'description': 'Synthetic unresolved issue',
             'resolution': 'Proposed only', 'recheck': 'Still needs actual review'}]))
        codes = self.codes(bundle)
        self.assertIn('OPEN_FINDING', codes)
        self.assertIn('REVIEW_PENDING', codes)

    def test_role_mismatch_and_recursive_bundle_are_rejected(self):
        for mutate, code in [
            (lambda r: r.update(role='N'), 'REVIEW_ROLE'),
            (lambda r: r.update(type='review_bundle', children=[]), 'REVIEW_BUNDLE_SCHEMA'),
        ]:
            bundle = self.bundle('questions')
            self.change(bundle['children'][0], mutate)
            self.assertIn(code, self.codes(bundle))

    def test_unknown_schema_fields_cannot_introduce_old_pass_inheritance(self):
        bundle = self.bundle()
        bundle['recheck_of'] = {'id': 'old-approval'}
        self.assertIn('REVIEW_BUNDLE_SCHEMA', self.codes(bundle))
        bundle = self.bundle()
        self.change(bundle['children'][0], lambda r: r.update(inherited_pass=True))
        self.assertIn('REVIEW_BUNDLE_SCHEMA', self.codes(bundle))

    def test_missing_word_pages_and_context_only_page_do_not_count(self):
        bundle = self.bundle('word_layout')
        self.change(bundle['children'][1], lambda r: r.update(scope={'kind': 'partial', 'pages': [3]},
                     pages_reviewed=[3], context_pages=[2, 4]))
        self.assertIn('REVIEW_COVERAGE_MISSING', self.codes(bundle))

    def test_every_word_boundary_has_available_context_and_one_owner(self):
        for mutate in [lambda r: r['boundaries'].pop(), lambda r: r.update(context_pages=[])]:
            bundle = self.bundle('word_layout')
            self.change(bundle['children'][0], mutate)
            self.assertIn('WORD_BOUNDARY_COVERAGE', self.codes(bundle))

    def test_word_page_version_count_and_current_pdf_hash_are_required(self):
        bundle = self.bundle('word_layout')
        bundle['pdf_pages'] = 5
        self.assertIn('WORD_VISUAL_COVERAGE', self.codes(bundle))
        bundle = self.bundle('word_layout')
        self.change(bundle['children'][0], lambda r: r['bindings'].update(pdf_sha256='0' * 64))
        self.assertIn('REVIEW_STALE_BINDINGS', self.codes(bundle))
        self.assertIn('WORD_VISUAL_COVERAGE', self.codes(self.bundle('word_layout'), page_count=None))

    def test_word_requires_both_real_roles_and_detailed_review(self):
        for mutate, code in [
            (lambda r: r.update(role='J'), 'REVIEW_ROLE'),
            (lambda r: r.update(reviewer_id='SYNTHETIC-reviewer-J'), 'REVIEW_NOT_INDEPENDENT'),
            (lambda r: r.update(detail_pages=[]), 'REVIEW_SCOPE'),
            (lambda r: r.update(renderer='NOT_PERFORMED'), 'WORD_VISUAL_NOT_PERFORMED'),
        ]:
            bundle = self.bundle('word_layout')
            self.change(bundle['children'][1], mutate)
            self.assertIn(code, self.codes(bundle))

    def test_source_release_and_unknown_schema_cannot_be_bundled(self):
        for kind in ['source', 'release', 'unknown']:
            bundle = self.bundle()
            bundle['kind'] = kind
            self.assertIn('REVIEW_KIND', self.codes(bundle))
        bundle = self.bundle()
        bundle['schema_version'] = 2
        self.assertIn('REVIEW_BUNDLE_SCHEMA', self.codes(bundle))

    def test_duplicate_ids_paths_json_fields_and_missing_identity_fail_closed(self):
        bundle = self.bundle()
        self.change(bundle['children'][1], lambda r: r.update(id='SYNTHETIC-L1'))
        self.assertIn('REVIEW_DUPLICATE_ID', self.codes(bundle))
        bundle = self.bundle()
        bundle['children'].append(bundle['children'][0])
        self.assertIn('REVIEW_CHILD_DUPLICATE', self.codes(bundle))
        bundle = self.bundle()
        self.change(bundle['children'][0], lambda r: r.update(execution_id=''))
        self.assertIn('MISSING_REVIEW_DETAIL', self.codes(bundle))
        bundle = self.bundle()
        raw = b'{"type":"review_shard","type":"review_bundle"}'
        path = self.folder / bundle['children'][0]['path']
        path.write_bytes(raw)
        bundle['children'][0]['sha256'] = hashlib.sha256(raw).hexdigest()
        self.assertIn('REVIEW_CHILD_INVALID', self.codes(bundle))

    def test_bad_external_context_types_fail_without_exception(self):
        bundle = self.bundle()
        for data, bindings, producer in [(None, self.bindings, self.producer),
                                          (self.data, None, self.producer), (self.data, self.bindings, None)]:
            report = validate_bundle(bundle, data, bindings, 4, producer, self.folder)
            self.assertIsNone(report['aggregate'])
            self.assertEqual(report['errors'][0]['code'], 'REVIEW_BUNDLE_CONTEXT')


if __name__ == '__main__':
    unittest.main()
