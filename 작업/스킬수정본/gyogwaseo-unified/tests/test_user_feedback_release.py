"""Synthetic user-feedback integration; no actual user/Word review is claimed."""
from copy import deepcopy
import json
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch

import test_release


class UserFeedbackReleaseTests(unittest.TestCase):
    def setUp(self):
        self.fixture = test_release.ReleaseTests(methodName='runTest')
        self.fixture.setUp()
        self.record = self.fixture.record
        self.ledger = {'schema_version': 1, 'round_id': 'synthetic-round-2', 'requests': [{
            'id': 'UR-001', 'user_text': 'Synthetic request: keep the existing answer space.',
            'source': 'Synthetic test only, not a user instruction.',
            'targets': ['synthetic-workbook'], 'criteria': ['The answer space is preserved.'],
            'disposition': 'active', 'implementation': {'status': 'no_change_needed',
                'producer_id': 'synthetic-editor', 'execution_id': 'synthetic-edit-run',
                'detail': 'Synthetic already-satisfied fixture, never actual evidence.'}}]}
        self.review = {'schema_version': 1, 'round_id': 'synthetic-round-2',
            'ledger_sha256': '', 'bindings': {
                **{name+'_sha256':ref['sha256'] for name,ref in self.record['artifacts'].items()},
                'package_sha256': self.record['package']['sha256']},
            'reviewer_id': 'synthetic-feedback-reviewer', 'execution_id': 'synthetic-feedback-run',
            'performed_at': '2026-09-25T00:00:00Z', 'independent': True, 'status': 'PASS',
            'checks': [{'request_id':'UR-001','status':'PASS','results':[
                {'criterion_index':0,'status':'PASS','evidence':'Synthetic current page observation.'}]}]}

    def save(self, name, obj):
        return self.fixture.ref(self.fixture.put(name, obj))

    def link(self):
        ledger = self.save('사용자수정요청.json', self.ledger)
        self.review['ledger_sha256'] = ledger['sha256']
        self.record['user_feedback'] = {'ledger':ledger,
            'review':self.save('user-feedback-review.json', self.review)}

    def gate(self):
        with patch.object(test_release.m, 'pdf_pages', return_value=1):
            return test_release.m.verify(self.record, self.fixture.folder)

    def blocked(self, code):
        report = self.gate()
        self.assertNotEqual(report['status'], 'READY_FOR_RELEASE')
        self.assertIn(code,{r['code'] for r in report['errors']+report['pending']})
        return report

    def test_valid_feedback_adds_gate_without_replacing_existing_reviews(self):
        self.link()
        report = self.gate()
        self.assertEqual(report['status'],'READY_FOR_RELEASE',report['errors']+report['pending'])
        self.assertEqual(report['user_feedback']['status'],'USER_FEEDBACK_PASS')
        self.assertEqual(report['user_feedback']['checked_request_ids'],['UR-001'])

    def test_old_ready_cannot_ignore_new_ledger_even_without_book_change(self):
        self.save('사용자수정요청.json', self.ledger)
        report = self.blocked('USER_FEEDBACK_LINK_MISSING')
        self.assertIn(str((self.fixture.folder/'사용자수정요청.json').resolve()),report['protected_paths'])

    def test_new_criterion_invalidates_prior_review_after_pointer_refresh(self):
        self.link()
        self.ledger['requests'][0]['criteria'].append('Synthetic later instruction.')
        self.record['user_feedback']['ledger'] = self.save('사용자수정요청.json',self.ledger)
        self.blocked('USER_FEEDBACK_STALE_LEDGER')

    def test_archive_snapshot_cannot_replace_current_ledger(self):
        self.link()
        self.record['user_feedback']['ledger'] = self.save('archived-old-ledger.json',self.ledger)
        self.blocked('USER_FEEDBACK_CURRENT_LEDGER')

    def test_review_not_yet_created_is_pending(self):
        self.record['user_feedback']={'ledger':self.save('사용자수정요청.json',self.ledger)}
        report=self.gate()
        self.assertEqual(report['status'],'REVIEW_PENDING',report['errors'])
        self.assertEqual(report['user_feedback']['status'],'USER_FEEDBACK_PENDING')

    def test_feedback_pass_does_not_waive_two_blind_reviewers(self):
        self.link()
        self.record['reviews'].pop(3)
        self.blocked('MISSING_REVIEW')

    def test_implicit_current_ledger_cannot_be_overwritten_by_report(self):
        ledger_path=self.fixture.put('사용자수정요청.json',self.ledger)
        original=ledger_path.read_bytes()
        record_path=self.fixture.put('release-record.json',self.record)
        result=subprocess.run([sys.executable,'-B',str(Path(test_release.m.__file__)),
            str(record_path),str(ledger_path)],capture_output=True)
        self.assertNotEqual(result.returncode,0)
        self.assertEqual(ledger_path.read_bytes(),original)

    def test_unparseable_record_still_cannot_overwrite_implicit_ledger(self):
        ledger_path=self.fixture.put('사용자수정요청.json',self.ledger)
        original=ledger_path.read_bytes()
        record_path=self.fixture.folder/'broken-record.json'
        record_path.write_text('{broken JSON',encoding='utf-8')
        result=subprocess.run([sys.executable,'-B',str(Path(test_release.m.__file__)),
            str(record_path),str(ledger_path)],capture_output=True)
        self.assertNotEqual(result.returncode,0)
        self.assertEqual(ledger_path.read_bytes(),original)


if __name__ == '__main__':
    unittest.main()
