import hashlib
import json
from pathlib import Path
import sys
import unittest
from datetime import datetime, timezone

root = Path(__file__).resolve().parent
sys.path.insert(0, str(root))
class Result(unittest.TextTestResult):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.passed_ids = []
    def addSuccess(self, test):
        super().addSuccess(test)
        self.passed_ids.append(test.id())

names = ['test_learning_units', 'test_analysis_body', 'test_sv_line',
         'test_answer_links', 'test_question_source', 'test_master_docx', 'test_saved_docx',
         'test_learning_content', 'test_book', 'test_book_plan', 'test_export_handoff', 'test_promotion',
         'test_thumbnail_input', 'test_saved_format', 'test_release',
         'test_confirmed_layout', 'test_build_book', 'test_reading_rule_revision',
         'test_layout_rule_revision', 'test_assessment_rule_revision', 'test_rule_revision_integration',
         'test_special_lesson', 'test_cover_simplify',
         'test_hint_particles', 'test_relative_hints',
         'test_review_preflight', 'test_review_packets', 'test_review_coverage',
         'test_release_text', 'test_review_release_integration',
         'test_user_feedback', 'test_user_feedback_release',
         'test_gloss_identity', 'test_handoff_diagnostics', 'test_preflight_scope',
         'test_render_markers', 'test_quantity_of_passive',
         'test_verb_gloss_revision', 'test_verb_function_hints',
         'test_formula_training_gloss', 'test_formula_training_display',
         'test_syntax_training', 'test_syntax_training_output', 'test_compact_layout',
         'test_split_release', 'test_split_book', 'test_header_standardization']
suite = unittest.TestSuite(unittest.defaultTestLoader.loadTestsFromName(name) for name in names)
result = unittest.TextTestRunner(verbosity=1, resultclass=Result).run(suite)
skill = root.parent
sys.path.insert(0, str(skill / 'scripts'))
from verify_release import package_inventory
inventory = package_inventory(skill)
report = {
    'utc': datetime.now(timezone.utc).isoformat(),
    'scope': 'Common manuscript, approved layout, saved-format mutation, staged build and release-evidence regression suites; not a real textbook semantic or independent review',
    'tests_run': result.testsRun, 'success': result.wasSuccessful(),
    'passed_ids': result.passed_ids,
    'failures': [{'id': t.id(), 'trace': trace} for t, trace in result.failures],
    'errors': [{'id': t.id(), 'trace': trace} for t, trace in result.errors],
    'sha256': inventory['files'],
    'package_sha256': inventory['sha256'],
    'independent_content_review': 'NOT_PERFORMED',
    'claude_environment_run': 'NOT_PERFORMED', 'chatgpt_environment_run': 'NOT_PERFORMED'
}
(root / 'common-test-results.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
raise SystemExit(0 if result.wasSuccessful() else 1)
