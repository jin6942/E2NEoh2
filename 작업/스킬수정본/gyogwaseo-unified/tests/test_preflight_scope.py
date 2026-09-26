"""Learning preflight cannot certify a complete book or replace release checks."""
from copy import deepcopy
import contextlib
import io
import json
from pathlib import Path
import sys
import unittest
import uuid

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'scripts'))
import review_preflight as m
import verify_release as release
from check_book import check as check_book
from test_learning_content import fixture as learning_fixture
from test_book import fixture as full_fixture


def draft():
    data = learning_fixture()
    for unit in data['units']:
        unit.pop('workbook', None)
    return data


class PreflightScopeTests(unittest.TestCase):
    def test_learning_draft_without_workbook_or_assessment_keeps_learning_diagnostics(self):
        data = draft()
        data['units'][0]['analysis']['easy_explanations'][0]['explanatory_sentences'] = [
            '첫 설명이다. 둘째 설명이다.', '셋째 설명이다.']
        before = deepcopy(data)
        result = m.check(data, scope='learning')
        self.assertEqual(data, before)
        self.assertEqual(result['status'], 'NOT_CERTIFIED')
        self.assertEqual(result['scope'], 'learning')
        self.assertEqual(result['check_book']['scope'], 'learning')
        self.assertEqual(result['check_book']['status'], 'STRUCTURE_PASS')
        self.assertEqual(result['check_book']['learning']['sentence_count'], 3)
        self.assertNotIn('assessment', result['check_book'])
        self.assertEqual(result['diagnostic_counts']['ERROR'], 0)
        self.assertIn('EASY_EXPLANATION_SENTENCE_COUNT', {row['code'] for row in result['diagnostics']})
        self.assertEqual(result['semantic_review'], 'NOT_PERFORMED')
        self.assertEqual(result['saved_artifact_checks'], 'NOT_PERFORMED')

    def test_learning_scope_still_rejects_invalid_learning_and_preserves_source_pending(self):
        data = draft()
        data['units'][0]['analysis']['easy_explanations'][0]['explanatory_sentences'] = []
        result = m.check(data, scope='learning')
        self.assertEqual(result['check_book']['status'], 'FAIL')
        self.assertEqual(result['diagnostics'][0]['code'], 'CHECK_LEARNING_EXCEPTION')
        self.assertIn('nonempty', result['diagnostics'][0]['message'])
        data = draft()
        source = data['sources'][0]
        source['text'] = ''.join(row['text'] for row in data['sentences'])
        offset = 0
        for bounds, sentence in zip(source['sentences'], data['sentences']):
            bounds.update(start=offset, end=offset + len(sentence['text']))
            offset = bounds['end']
        result = m.check(data, scope='learning')
        self.assertEqual(result['check_book']['status'], 'NEEDS_SOURCE_REVIEW')
        self.assertGreater(result['diagnostic_counts']['ERROR'], 0)
        self.assertTrue(all(row.get('origin') == 'check_learning_content'
                            for row in result['diagnostics'] if row['severity'] == 'ERROR'))

    def test_full_remains_the_default_and_requires_workbook_and_assessment(self):
        complete = full_fixture()
        self.assertEqual(m.check(complete), m.check(complete, scope='full'))
        self.assertEqual(m.check(complete)['check_book']['status'], 'STRUCTURE_PASS')
        for data in [draft(), learning_fixture()]:
            result = m.check(data)
            self.assertEqual(result['check_book']['status'], 'FAIL')
            self.assertEqual(result['diagnostics'][0]['code'], 'CHECK_BOOK_EXCEPTION')
            self.assertNotIn('scope', result)  # Existing full report schema.

    def test_learning_does_not_diagnose_unfinished_assessment(self):
        data = full_fixture()
        data['assessment']['quick_key'][0]['answer'] = 5
        data['assessment']['questions'][1].update(type='요약', summary='(B) only')
        self.assertGreater(m.check(data)['diagnostic_counts']['ERROR'], 0)
        result = m.check(data, scope='learning')
        self.assertEqual(result['check_book']['status'], 'STRUCTURE_PASS')
        self.assertEqual(result['diagnostics'], [])

    def test_scope_must_be_explicit_and_known(self):
        for scope in ['partial', '', None, 'LEARNING']:
            with self.subTest(scope=scope), self.assertRaisesRegex(ValueError, 'scope'):
                m.check(draft(), scope=scope)

    def make_folder(self):
        # Keep scratch outside the distributed skill and preserve workspace ACLs.
        root = HERE.parents[2] / 'blockers-fix'
        root.mkdir(exist_ok=True)
        folder = root / ('preflight-scope-' + uuid.uuid4().hex)
        folder.mkdir()
        self.addCleanup(folder.rmdir)
        return folder

    def put(self, folder, name, value):
        path = folder / name
        path.write_text(json.dumps(value, ensure_ascii=False), encoding='utf-8')
        self.addCleanup(path.unlink, missing_ok=True)
        return path

    def test_cli_scope_and_error_reports_preserve_input_and_default_full(self):
        folder = self.make_folder()
        source = self.put(folder, 'draft.json', draft())
        before = source.read_bytes()
        for args, name, expected in [(['--scope', 'learning'], 'learning.json', 0),
                                     ([], 'full.json', 1)]:
            target = folder / name
            self.addCleanup(target.unlink, missing_ok=True)
            with contextlib.redirect_stdout(io.StringIO()):
                code = m.main([str(source), str(target), *args])
            self.assertEqual(code, expected)
            report = json.loads(target.read_text(encoding='utf-8'))
            self.assertEqual(report['status'], 'NOT_CERTIFIED')
            self.assertEqual(report['input_sha256'], release.digest(before))
            self.assertEqual(report.get('scope'), 'learning' if args else None)
        self.assertEqual(source.read_bytes(), before)
        invalid_scope = folder / 'invalid-scope.json'
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            m.main([str(source), str(invalid_scope), '--scope', 'partial'])
        self.assertFalse(invalid_scope.exists())
        source.write_bytes(b'{invalid')
        target = folder / 'invalid-input.json'
        self.addCleanup(target.unlink, missing_ok=True)
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(m.main([str(source), str(target), '--scope', 'learning']), 1)
        report = json.loads(target.read_text(encoding='utf-8'))
        self.assertEqual(report['scope'], 'learning')
        self.assertEqual(report['check_book']['scope'], 'learning')
        self.assertEqual(report['diagnostics'][0]['code'], 'INPUT_JSON')

    def test_release_rechecks_full_structure_and_rejects_learning_report_substitution(self):
        # Focus on the real structure-report consumption path. Other release
        # artifacts/reviews are deliberately absent; no release pass is claimed.
        folder = self.make_folder()
        data = full_fixture()
        manuscript = self.put(folder, 'manuscript.json', data)
        def ref(path):
            return {'path': str(path), 'sha256': release.digest(path.read_bytes())}
        raw_hash = ref(manuscript)['sha256']
        full = check_book(data)
        full['input_sha256'] = raw_hash
        record = {'schema_version': 1, 'scope': 'full',
                  'producer': {'reviewer_id': 'synthetic', 'execution_id': 'synthetic'},
                  'artifacts': {'manuscript': ref(manuscript)}, 'reports': {}}
        full_path = self.put(folder, 'full-check.json', full)
        record['reports']['structure'] = ref(full_path)
        result = release.verify(record, folder)
        codes = {row['code'] for row in result['errors']}
        self.assertNotIn('CURRENT_STRUCTURE_FAIL', codes)
        self.assertNotIn('REPORT_CONTENT_MISMATCH', codes)
        learning = m.check(data, scope='learning')
        learning['input_sha256'] = raw_hash
        learning_path = self.put(folder, 'learning-preflight.json', learning)
        record['reports']['structure'] = ref(learning_path)
        result = release.verify(record, folder)
        self.assertNotEqual(result['status'], 'READY_FOR_RELEASE')
        self.assertTrue(any(row['code'] == 'REPORT_CONTENT_MISMATCH'
                            and row['detail'].startswith('structure:') for row in result['errors']))


if __name__ == '__main__':
    unittest.main()
