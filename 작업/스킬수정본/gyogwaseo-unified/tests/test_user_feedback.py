"""Synthetic gate tests; none of these records proves a real user review."""
from copy import deepcopy
import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
import uuid

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'scripts'))
from user_feedback import REQUIRED_BINDINGS, validate_user_feedback


class UserFeedbackTests(unittest.TestCase):
    def setUp(self):
        if os.name == 'nt':
            # The Windows sandbox cannot reopen tempfile's private 0700 ACL.
            # Normal mkdir inherits the host ACL; stay outside the package so
            # live test fixtures never contaminate the package fingerprint.
            self.folder = Path(tempfile.gettempdir()) / ('gyogwaseo-feedback-' + uuid.uuid4().hex)
            self.folder.mkdir()
            self.addCleanup(self.cleanup_windows)
        else:
            self.temporary = tempfile.TemporaryDirectory(prefix='gyogwaseo-feedback-')
            self.addCleanup(self.temporary.cleanup)
            self.folder = Path(self.temporary.name)
        self.bindings = {key: hashlib.sha256(key.encode()).hexdigest()
                         for key in REQUIRED_BINDINGS}
        self.producer = {'reviewer_id': 'synthetic-producer',
                         'execution_id': 'synthetic-production-run'}
        self.ledger = {
            'schema_version': 1, 'round_id': 'synthetic-round-2', 'requests': [{
                'id': 'U1', 'user_text': 'Synthetic request: keep the font and add spacing.',
                'source': 'Synthetic test message, not a real user instruction.',
                'targets': ['synthetic-question-1'],
                'criteria': ['Keep the existing font.', 'Add the requested spacing.'],
                'disposition': 'active',
                'implementation': {'status': 'applied', 'producer_id': 'synthetic-editor',
                                   'execution_id': 'synthetic-edit-run',
                                   'detail': 'Synthetic implementation evidence only.'},
            }],
        }
        self.review = {
            'schema_version': 1, 'round_id': 'synthetic-round-2', 'ledger_sha256': '',
            'bindings': deepcopy(self.bindings), 'reviewer_id': 'synthetic-reviewer',
            'execution_id': 'synthetic-recheck-run', 'performed_at': '2026-09-25T00:00:00Z',
            'independent': True, 'status': 'PASS', 'checks': [{
                'request_id': 'U1', 'status': 'PASS', 'results': [
                    {'criterion_index': 0, 'status': 'PASS',
                     'evidence': 'Synthetic page 1 font comparison.'},
                    {'criterion_index': 1, 'status': 'PASS',
                     'evidence': 'Synthetic page 1 spacing comparison.'},
                ],
            }],
        }

    def cleanup_windows(self):
        assert self.folder.resolve().parent == Path(tempfile.gettempdir()).resolve()
        assert self.folder.name.startswith('gyogwaseo-feedback-')
        for name in ('ledger.json', 'review.json'):
            (self.folder / name).unlink(missing_ok=True)
        self.folder.rmdir()

    def put(self, name, value):
        raw = (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
        (self.folder / name).write_bytes(raw)
        return {'path': name, 'sha256': hashlib.sha256(raw).hexdigest()}

    def refs(self):
        ledger = self.put('ledger.json', self.ledger)
        self.review['ledger_sha256'] = ledger['sha256']
        return {'ledger': ledger, 'review': self.put('review.json', self.review)}

    def check(self, refs=None):
        return validate_user_feedback(self.refs() if refs is None else refs,
                                      self.bindings, self.producer, self.folder)

    def codes(self, refs=None):
        report = self.check(refs)
        self.assertNotEqual(report['summary']['status'], 'USER_FEEDBACK_PASS')
        return {row['code'] for row in report['errors'] + report['pending']}

    def test_current_independent_review_covers_each_request_criterion(self):
        report = self.check()
        self.assertEqual(report['errors'] + report['pending'], [])
        self.assertEqual(report['summary']['status'], 'USER_FEEDBACK_PASS')
        self.assertEqual(report['summary']['checked_request_ids'], ['U1'])
        self.assertEqual(report['protected_paths'], sorted(str((self.folder / name).resolve())
                                                         for name in ['ledger.json', 'review.json']))

    def test_explicit_missing_or_malformed_references_never_pass(self):
        for value in [None, {}, [], {'ledger': None, 'review': None}]:
            with self.subTest(value=value):
                report = validate_user_feedback(value, self.bindings, self.producer, self.folder)
                self.assertTrue(report['errors'])
                self.assertEqual(report['summary']['status'], 'USER_FEEDBACK_INVALID')

    def test_saved_bytes_hash_checked_and_bad_reference_paths_still_protected(self):
        refs = self.refs()
        refs['ledger']['sha256'] = '0' * 64
        report = self.check(refs)
        self.assertIn('USER_FEEDBACK_HASH', {item['code'] for item in report['errors']})
        self.assertEqual(len(report['protected_paths']), 2)
        refs['review']['unexpected'] = True
        report = self.check(refs)
        self.assertEqual(len(report['protected_paths']), 2)
        self.assertIn('USER_FEEDBACK_SCHEMA', {item['code'] for item in report['errors']})

    def test_duplicate_json_keys_rejected_even_with_matching_file_hash(self):
        refs = self.refs()
        raw = b'{"schema_version":1,"schema_version":1}'
        (self.folder / 'ledger.json').write_bytes(raw)
        refs['ledger']['sha256'] = hashlib.sha256(raw).hexdigest()
        self.assertIn('USER_FEEDBACK_FILE', self.codes(refs))

    def test_missing_referenced_review_remains_pending(self):
        refs = self.refs()
        (self.folder / 'review.json').unlink()
        report = self.check(refs)
        self.assertFalse(report['errors'])
        self.assertEqual(report['summary']['status'], 'USER_FEEDBACK_PENDING')
        self.assertEqual(len(report['protected_paths']), 2)

    def test_new_valid_ledger_without_review_key_waits_but_bad_ledger_is_invalid(self):
        self.ledger['requests'][0]['implementation']['status'] = 'pending'
        refs = {'ledger': self.put('ledger.json', self.ledger)}
        report = self.check(refs)
        self.assertFalse(report['errors'])
        self.assertEqual(report['summary']['status'], 'USER_FEEDBACK_PENDING')
        self.assertEqual(report['summary']['active_request_count'], 1)
        self.assertEqual(len(report['protected_paths']), 1)
        self.assertIn('USER_FEEDBACK_IMPLEMENTATION_PENDING',
                      {row['code'] for row in report['pending']})
        self.ledger['requests'][0]['criteria'] = []
        refs['ledger'] = self.put('ledger.json', self.ledger)
        report = self.check(refs)
        self.assertTrue(report['errors'])
        self.assertEqual(report['summary']['status'], 'USER_FEEDBACK_INVALID')

    def test_later_user_request_invalidates_old_review_even_after_ref_hash_update(self):
        refs = self.refs()
        self.ledger['requests'][0]['criteria'].append('Keep answer evidence visible.')
        refs['ledger'] = self.put('ledger.json', self.ledger)
        codes = self.codes(refs)
        self.assertIn('USER_FEEDBACK_STALE_LEDGER', codes)
        self.assertIn('USER_FEEDBACK_CRITERIA', codes)

    def test_all_current_artifact_bindings_are_required(self):
        for key in REQUIRED_BINDINGS:
            with self.subTest(key=key):
                original = self.review['bindings'].pop(key)
                self.assertIn('USER_FEEDBACK_STALE_BINDINGS', self.codes())
                self.review['bindings'][key] = original
        self.review['bindings']['docx_sha256'] = '0' * 64
        self.assertIn('USER_FEEDBACK_STALE_BINDINGS', self.codes())
        self.review['bindings']['invented_sha256'] = '0' * 64
        self.assertIn('USER_FEEDBACK_STALE_BINDINGS', self.codes())

    def test_self_review_rejected_for_book_producer_and_every_editor(self):
        for key, forbidden in [('reviewer_id', self.producer['reviewer_id']),
                               ('execution_id', self.producer['execution_id']),
                               ('reviewer_id', 'synthetic-editor'),
                               ('execution_id', 'synthetic-edit-run')]:
            with self.subTest(key=key, forbidden=forbidden):
                previous = self.review[key]
                self.review[key] = forbidden
                self.assertIn('USER_FEEDBACK_NOT_INDEPENDENT', self.codes())
                self.review[key] = previous
        self.review['independent'] = False
        self.assertIn('USER_FEEDBACK_NOT_INDEPENDENT', self.codes())

    def test_pending_and_blocked_implementation_cannot_be_cleared_by_pass(self):
        for status in ['pending', 'blocked']:
            with self.subTest(status=status):
                self.ledger['requests'][0]['implementation']['status'] = status
                report = self.check()
                self.assertEqual(report['summary']['status'], 'USER_FEEDBACK_PENDING')
                self.assertIn('USER_FEEDBACK_IMPLEMENTATION_PENDING',
                              {row['code'] for row in report['pending']})

    def test_missing_duplicate_and_unknown_request_checks_rejected(self):
        original = deepcopy(self.review['checks'])
        for checks in [[], original + original,
                       [dict(original[0], request_id='U999')]]:
            with self.subTest(checks=checks):
                self.review['checks'] = checks
                self.assertIn('USER_FEEDBACK_COVERAGE', self.codes())
        self.review['checks'] = original
        self.ledger['requests'].append(deepcopy(self.ledger['requests'][0]))
        self.assertIn('USER_FEEDBACK_REQUEST_IDS', self.codes())

    def test_every_subcriterion_has_pass_and_real_evidence_field(self):
        results = self.review['checks'][0]['results']
        original = deepcopy(results)
        for changed in [original[:1], original + [original[0]],
                        [dict(original[0], criterion_index=True), original[1]],
                        [dict(original[0], criterion_index=99), original[1]]]:
            with self.subTest(changed=changed):
                self.review['checks'][0]['results'] = changed
                self.assertIn('USER_FEEDBACK_CRITERIA', self.codes())
        self.review['checks'][0]['results'] = deepcopy(original)
        self.review['checks'][0]['results'][0]['evidence'] = ' '
        self.assertIn('USER_FEEDBACK_DETAIL', self.codes())
        self.review['checks'][0]['results'][0]['evidence'] = 'Synthetic unresolved location.'
        self.review['checks'][0]['results'][0]['status'] = 'FAIL'
        self.assertIn('USER_FEEDBACK_REVIEW_PENDING', self.codes())

    def test_no_change_needed_requires_reason_and_recheck(self):
        implementation = self.ledger['requests'][0]['implementation']
        implementation['status'] = 'no_change_needed'
        self.assertEqual(self.check()['summary']['status'], 'USER_FEEDBACK_PASS')
        implementation['detail'] = ''
        self.assertIn('USER_FEEDBACK_DETAIL', self.codes())

    def test_withdrawal_requires_actual_user_decision_and_independent_empty_check(self):
        request = self.ledger['requests'][0]
        request['disposition'] = 'withdrawn'
        self.review['checks'] = []
        self.assertIn('USER_FEEDBACK_SCHEMA', self.codes())
        request['decision'] = {'user_text': 'Synthetic: withdraw this request.',
                               'source': 'Synthetic later user message.'}
        report = self.check()
        self.assertEqual(report['summary']['status'], 'USER_FEEDBACK_PASS')
        self.assertEqual(report['summary']['withdrawn_request_count'], 1)
        self.review['independent'] = False
        self.assertIn('USER_FEEDBACK_NOT_INDEPENDENT', self.codes())

    def test_supersession_preserves_old_request_and_requires_existing_noncyclic_target(self):
        replacement = deepcopy(self.ledger['requests'][0])
        replacement['id'] = 'U2'
        self.ledger['requests'].append(replacement)
        old = self.ledger['requests'][0]
        old['disposition'] = 'superseded'
        old['decision'] = {'user_text': 'Synthetic: replace U1 with U2.',
                           'source': 'Synthetic later user message.'}
        old['superseded_by'] = 'U2'
        self.review['checks'][0]['request_id'] = 'U2'
        self.assertEqual(self.check()['summary']['status'], 'USER_FEEDBACK_PASS')
        for invalid in ['U1', 'missing']:
            old['superseded_by'] = invalid
            self.assertIn('USER_FEEDBACK_SUPERSESSION', self.codes())
        old['superseded_by'] = 'U2'
        replacement['disposition'] = 'superseded'
        replacement['decision'] = deepcopy(old['decision'])
        replacement['superseded_by'] = 'U1'
        self.review['checks'] = []
        self.assertIn('USER_FEEDBACK_SUPERSESSION', self.codes())

    def test_empty_ledger_cannot_claim_user_review_complete(self):
        self.ledger['requests'] = []
        self.review['checks'] = []
        self.assertIn('USER_FEEDBACK_EMPTY_LEDGER', self.codes())

    def test_malformed_nested_fields_return_errors_without_throwing(self):
        for location, key, value in [(self.ledger, 'schema_version', True),
                                     (self.ledger['requests'][0], 'id', []),
                                     (self.ledger['requests'][0], 'disposition', {}),
                                     (self.ledger['requests'][0], 'criteria', None),
                                     (self.review, 'reviewer_id', []),
                                     (self.review, 'bindings', [])]:
            with self.subTest(key=key):
                previous = location[key]
                location[key] = value
                self.assertTrue(self.check()['errors'])
                location[key] = previous


if __name__ == '__main__':
    unittest.main()
