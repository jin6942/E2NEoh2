"""Synthetic release-record tests; no actual language/independent/Word review.

The deliberately synthetic receipts exercise binding/coverage enforcement only.
They must never be reused as production verification evidence.
"""
from copy import deepcopy
import json
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch
import uuid
from zipfile import ZipFile

HERE = Path(__file__).resolve().parent
SKILL = HERE.parent
sys.path.insert(0, str(SKILL / 'scripts'))
from test_book_plan import fixture
from book_plan import compile_plan
from check_book import check as check_book
from check_saved_docx import check as check_saved
from master_docx import write
from export_handoff import render
import verify_release as m


def blank_pdf():
    objects = [b'<< /Type /Catalog /Pages 2 0 R >>',
               b'<< /Type /Pages /Kids [3 0 R] /Count 1 >>',
               b'<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Resources << >> /Contents 4 0 R >>',
               b'<< /Length 0 >>\nstream\n\nendstream']
    result = b'%PDF-1.4\n'
    offsets = [0]
    for index, obj in enumerate(objects, 1):
        offsets.append(len(result))
        result += f'{index} 0 obj\n'.encode() + obj + b'\nendobj\n'
    xref = len(result)
    result += b'xref\n0 5\n0000000000 65535 f \n'
    result += b''.join(f'{offset:010d} 00000 n \n'.encode() for offset in offsets[1:])
    return result + f'trailer\n<< /Size 5 /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n'.encode()


class ReleaseTests(unittest.TestCase):
    def setUp(self):
        self.prepare_record(fixture())

    def prepare_record(self, data, *, current_syntax=True):
        # Upgrade only this synthetic receipt fixture. Production compatibility
        # must never manufacture exercises, review records or release approval.
        if current_syntax and 'syntax_training_version' not in data['metadata']:
            data = deepcopy(data)
            data['metadata']['syntax_training_version'] = 1
            sentences = {s['id']: s for s in data['sentences']}
            for unit in data['units']:
                unit['analysis']['formula_routes'] = []
                for i, point in enumerate(unit['analysis']['grammar_points'], 1):
                    sentence = sentences[point['sentence_id']]
                    gloss = sentence['glosses'][1]
                    point.update(id=f'{unit["id"]}-gp{i}', formula_key=f'formula {i}',
                                 span=[0, len(sentence['text'])],
                                 practice={'span': gloss['spans'][0],
                                           'formula_support': {'en': f'Formula {i}', 'ko': f'공식 뜻 {i}'},
                                           'support_gloss_ids': [gloss['id']],
                                           'answer_ko': f'시험 전용 결합 해석 {i}'})
                unit['workbook']['syntax_point_ids'] = [p['id'] for p in unit['analysis']['grammar_points']]
        # Like the existing suites, use a writable workspace subfolder; some
        # Windows hosts have an inaccessible system temporary-directory ACL.
        self.folder = HERE / ('release-test-' + uuid.uuid4().hex)
        self.folder.mkdir()
        self.data = data
        source = self.folder / 'synthetic-source.txt'
        source.write_text(self.data['sources'][0]['text'], encoding='utf-8')
        self.data['sources'][0]['provenance'].update(filename=source.name,
                                                     sha256=m.digest(source.read_bytes()))
        for heading in self.data['sources'][0].get('subheadings', []):
            heading['artifact_sha256'] = m.digest(source.read_bytes())
        manuscript = self.put('manuscript.json', self.data)
        plan = compile_plan(self.data)
        plan['input_sha256'] = m.digest(manuscript.read_bytes())
        plan_path = self.put('plan.json', plan)
        docx = self.folder / 'synthetic.docx'
        write(plan, docx)
        pdf = self.folder / 'synthetic.pdf'
        pdf.write_bytes(blank_pdf())
        handoff = render(self.data)
        learning = self.folder / 'learning_FINAL.txt'
        learning.write_bytes(handoff['learning'].encode('utf-8'))
        assessment = self.folder / 'assessment_FINAL.txt'
        assessment.write_bytes(handoff['assessment'].encode('utf-8'))
        files = {'manuscript': manuscript, 'plan': plan_path,
                 'contract': SKILL / 'assets/layout-contract.json', 'docx': docx, 'pdf': pdf,
                 'learning_final': learning, 'assessment_final': assessment}
        inventory = m.package_inventory(SKILL)
        self.record = {
            'schema_version': 1, 'scope': 'full',
            'producer': {'reviewer_id': 'SYNTHETIC-producer', 'execution_id': 'SYNTHETIC-production'},
            'package': {'root': str(SKILL), **inventory},
            'sources': [{'id': 'src', **self.ref(source)}],
            'artifacts': {name: self.ref(path) for name, path in files.items()},
            'reports': {}, 'reviews': [],
        }
        structure = check_book(self.data)
        structure['input_sha256'] = self.ref(manuscript)['sha256']
        self.record['reports']['structure'] = self.ref(self.put('structure.json', structure))
        saved = check_saved(plan, docx, 'full', assets=SKILL / 'assets')
        self.record['reports']['saved_docx'] = self.ref(self.put('saved.json', saved))
        self.record['reports']['word_render'] = self.ref(self.put('word.json', {
            'status': 'PASS', 'renderer': 'Microsoft Word', 'version': 'SYNTHETIC-test-only',
            'execution_id': 'SYNTHETIC-render-no-Word-was-executed', 'source_unchanged': True,
            'source_sha256': self.ref(docx)['sha256'], 'pdf_sha256': self.ref(pdf)['sha256'], 'pages': 1,
        }))
        bindings = {name + '_sha256': ref['sha256'] for name, ref in self.record['artifacts'].items()}
        bindings.update(package_sha256=inventory['sha256'], **m.content_digests(self.data))
        scope = {'kind': 'full', 'source_ids': ['src'], 'unit_ids': ['u1'],
                 'question_ids': [q['id'] for q in self.data['assessment']['questions']]}
        for i, kind in enumerate(['source', 'learning', 'questions', 'questions', 'word_layout', 'release']):
            receipt = {
                'id': f'SYNTHETIC-{kind}-{i}', 'kind': kind, 'status': 'PASS',
                'reviewer_id': f'SYNTHETIC-agent-{i}', 'execution_id': f'SYNTHETIC-session-{i}',
                'performed_at': '2026-01-01T00:00:00Z', 'independent': True,
                'method': 'Synthetic unit-test evidence only; no real independent review.',
                'summary': 'Fixture for release binding validation, never production evidence.',
                'scope': deepcopy(scope), 'bindings': bindings, 'findings': [],
            }
            if kind in {'source', 'learning'}:
                receipt['scope'].pop('question_ids')
                if kind == 'source':
                    receipt['scope'].pop('unit_ids')
            if kind == 'questions':
                receipt['solved_before_answer_key'] = True
                receipt['answers'] = {q['id']: q['answer'] for q in self.data['assessment']['questions']}
                receipt['length_reviews'] = {qid: {'status':'PASS',
                    'rationale':'Synthetic gate fixture only; no real length approval.',
                    'benchmark_ids':structure['question_views'][qid]['length_comparison']['benchmark_ids']}
                    for qid in structure['independent_length_review_required']}
            if kind == 'word_layout':
                receipt.update(renderer='Microsoft Word', pages_reviewed=[1], detail_pages=[1])
            self.record['reviews'].append(self.ref(self.put(f'review-{i}.json', receipt)))

    def put(self, name, value):
        path = self.folder / name
        path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        return path

    def ref(self, path):
        return {'path': str(path), 'sha256': m.digest(path.read_bytes())}

    def change(self, ref, mutate):
        path = Path(ref['path'])
        value = json.loads(path.read_text(encoding='utf-8'))
        mutate(value)
        path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')
        ref['sha256'] = m.digest(path.read_bytes())

    def result(self):
        # Core tests need only requirements.txt. Actual PDFium parsing is tested
        # separately when the optional visual dependency is installed.
        with patch.object(m, 'pdf_pages', return_value=1):
            return m.verify(self.record, self.folder)

    def codes(self):
        result = self.result()
        return {x['code'] for x in result['errors'] + result['pending']}

    def test_complete_current_synthetic_receipts_connect(self):
        result = self.result()
        self.assertEqual(result['status'], 'READY_FOR_RELEASE',
                         {'errors': result['errors'], 'pending': result['pending']})
        self.assertIn('do not prove review truth', result['limits'][0])
        self.assertEqual(result['scope'], 'full')
        self.assertEqual(result['assessment_configuration'], {
            'kind': 'full', 'label': '표준 편성', 'workbook_question_count': 1,
            'mock_round_count': 3, 'mock_rounds': [
                {'set_id': f'mock{i}', 'label': f'미니 모의고사 {i}회', 'question_count': 5}
                for i in range(1, 4)], 'instruction': None})

    def test_legacy_structural_compatibility_cannot_claim_current_syntax_release(self):
        self.tearDown()
        self.prepare_record(fixture(), current_syntax=False)
        structural = check_book(self.data)
        self.assertEqual(structural['status'], 'STRUCTURE_PASS')
        self.assertEqual(structural['learning']['syntax_training']['status'], 'UNDECLARED_LEGACY_INPUT')
        self.assertEqual(structural['learning']['syntax_training']['semantic_review'], 'NOT_PERFORMED')
        result = self.result()
        self.assertEqual(result['status'], 'REVIEW_PENDING', result)
        self.assertEqual(result['errors'], [])
        self.assertEqual({row['code'] for row in result['pending']}, {'SYNTAX_TRAINING_REVIEW_REQUIRED'})

    def test_custom_full_request_reports_actual_counts_and_exact_request_without_relaxing_reviews(self):
        data=fixture()
        instruction='시험용 사용자 요청: 워크북 1문항과 모의고사 1회 5문항·2회 4문항으로 완성.'
        assessment=data['assessment']
        assessment['scope']={'kind':'custom','instruction':instruction}
        removed={q['id'] for q in assessment['questions'] if q['set_id']=='mock3'} | {'mock2-3'}
        for key in ['plan','questions','quick_key','explanations']:
            assessment[key]=[row for row in assessment[key] if row['id'] not in removed]
            for row in assessment[key]:
                if row['set_id']=='mock2' and row['number']>3:
                    row['number']-=1
        assessment['passage_groups']=[g for g in assessment['passage_groups'] if g['set_id']!='mock3']
        data['question_sources']=[row for row in data['question_sources'] if row['id'] not in removed]
        self.prepare_record(data)
        result=self.result()
        self.assertEqual(result['status'],'READY_FOR_RELEASE',result['errors'])
        self.assertEqual(result['scope'],'full')
        self.assertEqual(result['review_scope']['kind'],'full')
        self.assertEqual(result['assessment_configuration'],{
            'kind':'custom','label':'맞춤 편성','workbook_question_count':1,'mock_round_count':2,
            'mock_rounds':[{'set_id':'mock1','label':'미니 모의고사 1회','question_count':5},
                           {'set_id':'mock2','label':'미니 모의고사 2회','question_count':4}],
            'instruction':instruction})
        self.record['reviews'].pop(3)
        pending=self.result()
        self.assertEqual(pending['status'],'REVIEW_PENDING')
        self.assertIn('MISSING_REVIEW',{row['code'] for row in pending['pending']})
        self.assertEqual(pending['assessment_configuration'],result['assessment_configuration'])

    def test_partial_assessment_manuscript_cannot_be_full_release_or_reported_as_standard(self):
        self.change(self.record['artifacts']['manuscript'],
                    lambda data: data['assessment'].update(scope={'kind':'partial','instruction':'시험용 부분 원고'}))
        result=self.result()
        self.assertEqual(result['status'],'FAIL')
        self.assertIn('CURRENT_STRUCTURE_FAIL',{row['code'] for row in result['errors']})
        self.assertIsNone(result['assessment_configuration'])

    def test_missing_second_independent_review_remains_pending(self):
        self.record['reviews'].pop(3)
        self.assertIn('MISSING_REVIEW', self.codes())
        self.assertEqual(self.result()['status'], 'REVIEW_PENDING')

    def test_short_passage_review_cannot_be_replaced_by_general_answers(self):
        self.change(self.record['reviews'][2], lambda value: value.pop('length_reviews'))
        self.assertIn('LENGTH_REVIEW_PENDING', self.codes())
        self.assertEqual(self.result()['status'],'REVIEW_PENDING')

    def test_short_passage_review_must_identify_actual_benchmarks(self):
        self.change(self.record['reviews'][3], lambda value: value['length_reviews']['q1'].update(benchmark_ids=[]))
        self.assertIn('LENGTH_REVIEW_BENCHMARK_MISMATCH',self.codes())

    def test_short_passage_review_needs_written_comparison_reason(self):
        self.change(self.record['reviews'][2], lambda value: value['length_reviews']['q1'].update(rationale=''))
        self.assertIn('MISSING_REVIEW_DETAIL',self.codes())

    def test_two_names_for_same_execution_are_not_independent(self):
        self.change(self.record['reviews'][3], lambda value: value.update(execution_id='SYNTHETIC-session-2'))
        self.assertIn('QUESTION_REVIEWERS_NOT_DISTINCT', self.codes())

    def test_producer_cannot_review_own_final(self):
        self.change(self.record['reviews'][1], lambda value: value.update(reviewer_id='SYNTHETIC-producer'))
        self.assertIn('REVIEW_NOT_INDEPENDENT', self.codes())

    def test_partial_scope_cannot_be_full_release(self):
        self.record['scope'] = 'learning'
        self.assertIn('PARTIAL_SCOPE_NOT_RELEASE', self.codes())

    def test_old_docx_hash_rejected(self):
        self.record['artifacts']['docx']['sha256'] = '0' * 64
        self.assertIn('STALE_ARTIFACT', self.codes())

    def test_rehashed_changed_docx_cannot_reuse_old_reports(self):
        ref = self.record['artifacts']['docx']
        path = Path(ref['path'])
        with ZipFile(path) as archive:
            parts = [(info, archive.read(info.filename)) for info in archive.infolist()]
        with ZipFile(path, 'w') as archive:
            for info, raw in parts:
                if info.filename == 'word/document.xml':
                    raw = raw.replace('혼공교재 독해편'.encode('utf-8'), b'CHANGED', 1)
                archive.writestr(info, raw)
        ref['sha256'] = m.digest(path.read_bytes())
        self.assertIn('CURRENT_SAVED_FAIL', self.codes())
        self.assertIn('REVIEW_STALE_BINDINGS', self.codes())

    def test_contract_change_or_old_contract_record_rejected(self):
        self.record['artifacts']['contract']['sha256'] = '0' * 64
        self.assertIn('STALE_ARTIFACT', self.codes())

    def test_policy_and_test_files_are_part_of_package_fingerprint(self):
        self.assertIn('references/workflow.md', self.record['package']['files'])
        self.assertIn('tests/test_release.py', self.record['package']['files'])
        self.assertIn('requirements-visual.txt', self.record['package']['files'])
        self.record['package']['files']['references/workflow.md'] = '0' * 64
        self.assertIn('PACKAGE_CHANGED', self.codes())

    def test_claimed_package_must_match_running_assets_and_rules(self):
        other_root = self.folder / 'other-package'
        self.record['package']['root'] = str(other_root)
        claimed = deepcopy(self.record['package'])
        claimed['files']['assets/layout-contract.json'] = '1' * 64
        claimed['sha256'] = m.canonical_hash(claimed['files'])
        self.record['package'].update(claimed)
        actual_inventory = m.package_inventory(SKILL)
        def choose_inventory(path):
            return {'files': claimed['files'], 'sha256': claimed['sha256']} if Path(path) == other_root else actual_inventory
        with patch.object(m, 'package_inventory', side_effect=choose_inventory):
            result = self.result()
        self.assertIn('RUNNING_PACKAGE_MISMATCH', {row['code'] for row in result['errors']})

    def test_rehashed_targeted_report_cannot_replace_full_check(self):
        self.change(self.record['reports']['saved_docx'], lambda value: value.update(scope='targeted'))
        self.assertIn('REPORT_CONTENT_MISMATCH', self.codes())

    def test_matching_report_file_hash_is_not_enough(self):
        self.change(self.record['reports']['structure'], lambda value: value.update(input_sha256='0' * 64))
        self.assertIn('REPORT_INPUT_MISMATCH', self.codes())

    def test_structural_report_cannot_claim_unperformed_semantic_review(self):
        self.change(self.record['reports']['saved_docx'], lambda value: value.update(semantic_review='PASS'))
        self.assertIn('REPORT_CONTENT_MISMATCH', self.codes())

    def test_plan_rewrite_rejected_even_when_rehashed(self):
        self.change(self.record['artifacts']['plan'],
                    lambda value: next(e for e in value['blocks'][0]['elements']
                                       if e['role'] == 'cover_series_title')['runs'][0].update(text='DIFFERENT LABEL'))
        self.assertIn('PLAN_NOT_CANONICAL', self.codes())

    def test_empty_plan_and_report_cannot_skip_current_checks(self):
        self.change(self.record['artifacts']['plan'], lambda value: value.clear())
        self.change(self.record['reports']['saved_docx'], lambda value: value.clear())
        plan_hash = self.record['artifacts']['plan']['sha256']
        for ref in self.record['reviews']:
            self.change(ref, lambda value: value['bindings'].update(plan_sha256=plan_hash))
        result = self.result()
        self.assertEqual(result['status'], 'FAIL')
        self.assertIn('CURRENT_CHECK_NOT_PERFORMED', {row['code'] for row in result['errors']})

    def test_empty_manuscript_cannot_skip_current_checks(self):
        self.change(self.record['artifacts']['manuscript'], lambda value: value.clear())
        result = self.result()
        self.assertEqual(result['status'], 'FAIL')
        self.assertIn('CURRENT_CHECK_NOT_PERFORMED', {row['code'] for row in result['errors']})

    def test_unperformed_word_is_pending(self):
        self.change(self.record['reports']['word_render'], lambda value: value.update(status='NOT_PERFORMED'))
        self.assertIn('WORD_NOT_PERFORMED', self.codes())
        self.assertEqual(self.result()['status'], 'REVIEW_PENDING')

    def test_pdf_page_count_and_word_receipt_are_bound(self):
        self.change(self.record['reports']['word_render'], lambda value: value.update(pages=2))
        self.assertIn('WORD_RENDER_MISMATCH', self.codes())

    def test_unavailable_pdf_reader_remains_pending(self):
        with patch.object(m, 'pdf_pages', side_effect=RuntimeError('Visual dependency unavailable')):
            result = m.verify(self.record, self.folder)
        self.assertEqual(result['status'], 'REVIEW_PENDING')
        self.assertIn('PDF_CHECK_UNAVAILABLE', {row['code'] for row in result['pending']})

    def test_actual_pdf_page_reader_when_installed(self):
        try:
            import pypdfium2  # noqa: F401
        except ImportError:
            self.skipTest('Optional requirements-visual.txt is not installed')
        self.assertEqual(m.pdf_pages(Path(self.record['artifacts']['pdf']['path'])), 1)

    def test_partial_visual_review_cannot_pass(self):
        self.change(self.record['reviews'][4], lambda value: value.update(pages_reviewed=[]))
        self.assertIn('WORD_VISUAL_COVERAGE', self.codes())

    def test_old_final_content_rejected_after_file_hash_update(self):
        ref = self.record['artifacts']['learning_final']
        Path(ref['path']).write_text('Another final manuscript.', encoding='utf-8')
        ref['sha256'] = m.digest(Path(ref['path']).read_bytes())
        self.assertIn('FINAL_CONTENT_MISMATCH', self.codes())

    def test_incomplete_independent_answers_rejected(self):
        self.change(self.record['reviews'][2], lambda value: value.update(answers={}))
        self.assertIn('INDEPENDENT_ANSWERS', self.codes())

    def test_changed_source_file_rejected_despite_new_record_hash(self):
        ref = self.record['sources'][0]
        Path(ref['path']).write_text('Changed authority.', encoding='utf-8')
        ref['sha256'] = m.digest(Path(ref['path']).read_bytes())
        self.assertIn('SOURCE_PROVENANCE', self.codes())

    def test_open_finding_cannot_release(self):
        finding = {'id': 'x', 'description': 'Synthetic issue', 'status': 'open',
                   'resolution': 'Not resolved', 'recheck': 'Not rechecked'}
        self.change(self.record['reviews'][1], lambda value: value.update(findings=[finding]))
        self.assertIn('OPEN_FINDING', self.codes())

    def test_source_explicit_no_findings_can_replace_only_an_omitted_array(self):
        ref = self.record['reviews'][0]
        self.change(ref, lambda r: (r.pop('findings'), r.update(no_findings=True)))
        original = Path(ref['path']).read_bytes()
        result = self.result()
        self.assertEqual(result['status'], 'READY_FOR_RELEASE', result['errors'] + result['pending'])
        self.assertEqual(Path(ref['path']).read_bytes(), original)
        self.assertNotIn('findings', json.loads(original))
        self.change(ref, lambda r: r.update(findings=[]))
        self.assertEqual(self.result()['status'], 'READY_FOR_RELEASE')

    def test_source_missing_findings_without_true_declaration_fails(self):
        ref = self.record['reviews'][0]
        self.change(ref, lambda r: r.pop('findings'))
        result = self.result()
        self.assertEqual(result['status'], 'FAIL')
        self.assertIn('FINDINGS_REQUIRED', {r['code'] for r in result['errors']})
        for declaration in [False, 1, 'true', None, [], {}]:
            with self.subTest(declaration=declaration):
                self.change(ref, lambda r: r.update(no_findings=declaration))
                result = self.result()
                self.assertEqual(result['status'], 'FAIL')
                self.assertIn('FINDINGS_REQUIRED', {r['code'] for r in result['errors']})
                self.assertIn('NO_FINDINGS_DECLARATION', {r['code'] for r in result['errors']})

    def test_source_no_findings_does_not_hide_present_malformed_array(self):
        ref = self.record['reviews'][0]
        for findings in [None, {}, '', False, ['malformed']]:
            with self.subTest(findings=findings):
                self.change(ref, lambda r: r.update(no_findings=True, findings=findings))
                result = self.result()
                self.assertEqual(result['status'], 'FAIL')
                self.assertTrue({'FINDINGS_REQUIRED', 'FINDING_FORMAT'} & {r['code'] for r in result['errors']})

    def test_source_no_findings_conflicts_even_with_resolved_findings(self):
        ref = self.record['reviews'][0]
        finding = {'id': 'SYNTHETIC-f1', 'description': 'Synthetic finding',
                   'resolution': 'Synthetic resolution', 'recheck': 'Synthetic recheck'}
        for status in ['resolved', 'open']:
            with self.subTest(status=status):
                self.change(ref, lambda r: r.update(no_findings=True, findings=[dict(finding, status=status)]))
                result = self.result()
                self.assertEqual(result['status'], 'FAIL')
                self.assertIn('FINDINGS_CONFLICT', {r['code'] for r in result['errors']})
                if status == 'open':
                    self.assertIn('OPEN_FINDING', {r['code'] for r in result['pending']})

    def test_source_findings_keep_validation_and_unique_ids(self):
        ref = self.record['reviews'][0]
        finding = {'id': 'SYNTHETIC-f1', 'status': 'resolved', 'description': 'Synthetic finding',
                   'resolution': 'Synthetic resolution', 'recheck': 'Synthetic recheck'}
        self.change(ref, lambda r: r.update(findings=[finding]))
        self.assertEqual(self.result()['status'], 'READY_FOR_RELEASE')
        self.change(ref, lambda r: r.update(findings=[finding, finding]))
        result = self.result()
        self.assertEqual(result['status'], 'FAIL')
        self.assertIn('FINDING_FORMAT', {r['code'] for r in result['errors']})
        self.change(ref, lambda r: r.update(findings=[dict(finding, recheck='')]))
        self.assertEqual(self.result()['status'], 'FAIL')

    def test_duplicate_json_keys_cannot_hide_source_findings_or_status(self):
        ref = self.record['reviews'][0]
        path = Path(ref['path'])
        original = json.loads(path.read_text(encoding='utf-8'))
        original.update(no_findings=True)
        hidden = {'id': 'SYNTHETIC-hidden', 'status': 'open', 'description': 'Synthetic open issue',
                  'resolution': 'Unresolved', 'recheck': 'Not rechecked'}
        for duplicate in [
            '"findings":' + json.dumps([hidden]) + ',',
            '"status":"PENDING",',
            '"no_findings":false,',
        ]:
            with self.subTest(duplicate=duplicate):
                raw = ('{' + duplicate + json.dumps(original)[1:]).encode('utf-8')
                path.write_bytes(raw)
                ref['sha256'] = m.digest(raw)
                result = self.result()
                self.assertEqual(result['status'], 'FAIL')
                self.assertIn('INVALID_JSON', {r['code'] for r in result['errors']})
                self.assertEqual(path.read_bytes(), raw)

    def test_no_findings_never_replaces_other_full_review_arrays(self):
        for ref in self.record['reviews'][1:]:
            with self.subTest(review=ref['path']):
                original = json.loads(Path(ref['path']).read_text(encoding='utf-8'))
                self.change(ref, lambda r: (r.pop('findings'), r.update(no_findings=True)))
                result = self.result()
                self.assertEqual(result['status'], 'FAIL')
                self.assertIn('FINDINGS_REQUIRED', {r['code'] for r in result['errors']})
                self.assertIn('NO_FINDINGS_DECLARATION', {r['code'] for r in result['errors']})
                self.change(ref, lambda r: (r.clear(), r.update(original)))

    def test_source_no_findings_keeps_status_scope_identity_and_hash_gates(self):
        ref = self.record['reviews'][0]
        self.change(ref, lambda r: (r.pop('findings'), r.update(no_findings=True)))
        original = json.loads(Path(ref['path']).read_text(encoding='utf-8'))
        for mutate, status, code in [
            (lambda r: r.update(status='PENDING'), 'REVIEW_PENDING', 'REVIEW_PENDING'),
            (lambda r: r['scope'].update(source_ids=[]), 'FAIL', 'REVIEW_SCOPE'),
            (lambda r: r.update(reviewer_id=''), 'FAIL', 'MISSING_REVIEW_DETAIL'),
            (lambda r: r['bindings'].update(source_content_sha256='0' * 64), 'FAIL', 'REVIEW_STALE_BINDINGS'),
        ]:
            with self.subTest(code=code):
                self.change(ref, mutate)
                result = self.result()
                self.assertEqual(result['status'], status)
                self.assertIn(code, {r['code'] for r in result['errors'] + result['pending']})
                self.change(ref, lambda r: (r.clear(), r.update(original)))

    def test_cli_does_not_overwrite_referenced_json(self):
        record_path = self.put('release.json', self.record)
        manuscript = Path(self.record['artifacts']['manuscript']['path'])
        before = manuscript.read_bytes()
        result = subprocess.run([sys.executable, str(SKILL / 'scripts/verify_release.py'),
                                 str(record_path), str(manuscript)], capture_output=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(manuscript.read_bytes(), before)


if __name__ == '__main__':
    unittest.main()
