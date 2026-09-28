"""Read-only release gate for a complete, reviewed textbook.

Rechecks current manuscript/plan/DOCX and hash-bound review evidence. A release
record is not proof that a person/agent truly performed independent reasoning;
execution identities and evidence must come from the actual review sessions.
See references/release-record.md. Never upgrades structural PASS to FINAL.
"""
import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import re
from zipfile import BadZipFile

from book_plan import compile_plan
from check_book import check as check_book
from check_saved_docx import check as check_saved
from export_handoff import render as render_handoff
from review_coverage import _unique_json

SCHEMA = 1
RUNTIME_TEST = re.compile(r'(?:master|saved-docx|saved-format|book-plan|build-book|handoff|release)-test-[0-9a-f]{32}')
ARTIFACTS = ('manuscript', 'plan', 'contract', 'docx', 'pdf', 'learning_final', 'assessment_final')
REVIEW_KINDS = ('source', 'learning', 'questions', 'word_layout', 'release')


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def canonical_hash(value):
    return digest(json.dumps(value, ensure_ascii=False, sort_keys=True,
                             separators=(',', ':')).encode('utf-8'))


def runtime_file(relative):
    """Only known generated files; never exclude authored rules/tests by suffix."""
    parts = relative.parts
    if '__pycache__' in parts or '.pytest_cache' in parts:
        return True
    if relative.as_posix() == 'tests/common-test-results.json':
        return True
    if len(parts) > 2 and parts[0] == 'tests':
        return bool(RUNTIME_TEST.fullmatch(parts[1]) or
                    (parts[1] == 'thumbnail-input-test' and re.fullmatch('[0-9a-f]{32}', parts[2])))
    return False


def package_inventory(root):
    """Fingerprint every distributed file, including policies, tests and deps."""
    root = Path(root).resolve()
    files = {}
    for path in sorted(root.rglob('*')):
        relative = path.relative_to(root)
        if runtime_file(relative):
            continue
        if path.is_symlink():
            raise ValueError('Package symlink is not an unambiguous release input: ' + str(relative))
        if path.is_file():
            files[relative.as_posix()] = digest(path.read_bytes())
    for name in ('SKILL.md', 'requirements.txt', 'requirements-visual.txt',
                 'references/workflow.md', 'references/release-record.md',
                 'scripts/verify_release.py', 'tests/run_tests.py',
                 'assets/layout-contract.json', 'assets/latest-approved-reference.docx'):
        if name not in files:
            raise ValueError('Required package file is absent: ' + name)
    return {'files': files, 'sha256': canonical_hash(files)}


def content_digests(data):
    """Stage receipts survive unrelated later layout/assessment additions."""
    source = {k: data.get(k) for k in ('metadata', 'sources', 'paragraphs', 'grouping_resolutions')}
    learning = dict(source, sentences=data.get('sentences'),
                    units=[{k: v for k, v in u.items() if k != 'workbook'} for u in data.get('units', [])])
    assessment = dict(learning, units=data.get('units'), assessment=data.get('assessment'),
                      question_sources=data.get('question_sources'))
    return {'source_content_sha256': canonical_hash(source),
            'learning_content_sha256': canonical_hash(learning),
            'assessment_content_sha256': canonical_hash(assessment)}


def assessment_configuration(data):
    """Describe an already checked manuscript; this is not a release condition.

    Assessment full/custom describes the requested question arrangement, while
    release scope full still requires all of that request and its review evidence.
    Counts come from actual questions, never course defaults or review receipts.
    """
    assessment = data['assessment']
    kind = assessment['scope']['kind']
    counts = {}
    for question in assessment['questions']:
        set_id = question['set_id']
        counts[set_id] = counts.get(set_id, 0) + 1
    rounds = [{'set_id': set_id, 'label': data.get('set_labels', {}).get(set_id, set_id),
               'question_count': count} for set_id, count in counts.items() if set_id != 'workbook']
    return {'kind': kind, 'label': {'full': '표준 편성', 'custom': '맞춤 편성'}[kind],
            'workbook_question_count': counts.get('workbook', 0),
            'mock_round_count': len(rounds), 'mock_rounds': rounds,
            'instruction': assessment['scope']['instruction'] if kind == 'custom' else None}


def pdf_pages(path):
    try:
        import pypdfium2
    except ImportError as exc:
        raise RuntimeError('PDF page verification needs requirements-visual.txt') from exc
    document = pypdfium2.PdfDocument(str(path))
    try:
        return len(document)
    finally:
        document.close()


def verify(record, base='.', *, delivery_mode=None):
    base = Path(base).resolve()
    split_mode = delivery_mode == 'integrated_plus_five_docx'
    if delivery_mode not in (None, 'integrated_plus_five_docx'):
        raise ValueError('Unsupported delivery mode')
    artifact_names = ARTIFACTS + ('split_manifest',) if split_mode else ARTIFACTS
    errors, pending, checked, observed = [], [], [], {}
    protected = set()

    def fail(code, detail):
        errors.append({'code': code, 'detail': str(detail)})

    def wait(code, detail):
        pending.append({'code': code, 'detail': str(detail)})

    def path_for(value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError('Nonempty file path required')
        path = Path(value)
        return (path if path.is_absolute() else base / path).resolve()

    def artifact(value, name):
        if not isinstance(value, dict) or not value.get('path'):
            wait('MISSING_ARTIFACT', name)
            return None
        try:
            path = path_for(value['path'])
            protected.add(str(path))
            if not path.is_file():
                wait('MISSING_ARTIFACT', name + ': ' + str(path))
                return None
            raw = path.read_bytes()
            actual = digest(raw)
            observed[name] = actual
            if value.get('sha256') != actual:
                fail('STALE_ARTIFACT', name)
                return None
            checked.append(name)
            return path, raw, actual
        except (OSError, ValueError) as exc:
            fail('UNREADABLE_ARTIFACT', name + ': ' + str(exc))
            return None

    def load_json(item, name):
        if item is None:
            return None
        try:
            result = json.loads(item[1].decode('utf-8-sig'), object_pairs_hook=_unique_json)
            if not isinstance(result, dict) or not result:
                raise ValueError('Nonempty JSON object required')
            return result
        except (ValueError, UnicodeError) as exc:
            fail('INVALID_JSON', name + ': ' + str(exc))
            return None

    def required_text(value, name):
        if not isinstance(value, str) or not value.strip():
            fail('MISSING_REVIEW_DETAIL', name)
            return False
        return True

    if record.get('schema_version') != SCHEMA:
        fail('RELEASE_SCHEMA', 'Expected release schema_version=1')
    if split_mode and record.get('delivery_mode') != 'integrated_plus_five_docx':
        fail('DELIVERY_MODE', 'The record must explicitly declare delivery_mode=integrated_plus_five_docx')
    if not split_mode and record.get('delivery_mode') == 'integrated_plus_five_docx':
        fail('DELIVERY_MODE', 'Use verify_split_release.py for the integrated-plus-five DOCX record')
    if record.get('scope') != 'full':
        fail('PARTIAL_SCOPE_NOT_RELEASE', 'Only the complete requested textbook can receive release-ready status')
    producer = record.get('producer', {})
    for key in ('reviewer_id', 'execution_id'):
        required_text(producer.get(key), 'producer/' + key)
    package = record.get('package', {})
    package_root, inventory = None, None
    try:
        package_root = path_for(package.get('root'))
        inventory = package_inventory(package_root)
        protected.update(str((package_root / p).resolve()) for p in inventory['files'])
        if package.get('files') != inventory['files'] or package.get('sha256') != inventory['sha256']:
            fail('PACKAGE_CHANGED', 'Package inventory/fingerprint differs; includes policies, tests and requirements')
        # compile_plan and its source helpers use their installed default assets.
        # Equal scripts alone cannot justify checking a different claimed MASTER
        # or policy set. A relocated copy is allowed only when ALL static files
        # match the actual running package, including assets/rules/tests/deps.
        running_root = Path(__file__).resolve().parent.parent
        running_inventory = inventory if running_root == package_root else package_inventory(running_root)
        if running_inventory != inventory:
            fail('RUNNING_PACKAGE_MISMATCH', 'Running package assets/rules/code differ from the recorded package')
    except (OSError, TypeError, ValueError) as exc:
        fail('PACKAGE_INVALID', exc)

    supplied = record.get('artifacts', {})
    files = {name: artifact(supplied.get(name), name) for name in artifact_names}
    present_paths = [x[0] for x in files.values() if x]
    if len(present_paths) != len(set(present_paths)):
        fail('ARTIFACT_ALIAS', 'Different artifact roles must not reuse one file')
    data = load_json(files['manuscript'], 'manuscript')
    plan = load_json(files['plan'], 'plan')
    if package_root and files['contract'] and files['contract'][0] != package_root / 'assets/layout-contract.json':
        fail('DETACHED_CONTRACT', 'Contract must be the verified package assets/layout-contract.json')
    bindings = {name + '_sha256': entry[2] for name, entry in files.items() if entry}
    if inventory:
        bindings['package_sha256'] = inventory['sha256']

    sources = record.get('sources', [])
    source_files = {}
    if not isinstance(sources, list):
        fail('SOURCES_FORMAT', 'sources must be an array'); sources = []
    for row in sources:
        sid = row.get('id') if isinstance(row, dict) else None
        if not isinstance(sid, str) or not sid or sid in source_files:
            fail('SOURCE_IDS', 'Source IDs must be nonempty and unique'); continue
        source_files[sid] = artifact(row, 'source/' + sid)
    scope = None
    configuration = None
    current_structure = current_saved = None
    if data:
        bindings.update(content_digests(data))
        source_ids = [s['id'] for s in data.get('sources', [])]
        unit_ids = [u['id'] for u in data.get('units', [])]
        question_ids = [q['id'] for q in data.get('assessment', {}).get('questions', [])]
        scope = {'kind': 'full', 'source_ids': source_ids, 'unit_ids': unit_ids, 'question_ids': question_ids}
        if set(source_files) != set(source_ids):
            fail('SOURCE_COVERAGE', 'Actual source files must cover every manuscript source exactly')
        for source in data.get('sources', []):
            item = source_files.get(source['id'])
            if item and source.get('provenance', {}).get('sha256') != item[2]:
                fail('SOURCE_PROVENANCE', source['id'])
        try:
            current_structure = check_book(data)
            if current_structure.get('status') != 'STRUCTURE_PASS':
                fail('CURRENT_STRUCTURE_FAIL', current_structure.get('status'))
            else:
                configuration = assessment_configuration(data)
                syntax = (current_structure.get('learning') or {}).get('syntax_training') or {}
                if (type(syntax.get('version')) is not int or syntax.get('version') != 1 or
                        syntax.get('status') != 'DECLARED_LINKS_CHECKED'):
                    wait('SYNTAX_TRAINING_REVIEW_REQUIRED',
                         'Current release requires syntax_training_version=1 and checked analysis/practice links. '
                         'Legacy structural compatibility is not current-rule completion; semantic review remains required.')
            canonical_final = render_handoff(data)
            for name, section in [('learning_final', 'learning'), ('assessment_final', 'assessment')]:
                if files[name] and files[name][1].decode('utf-8-sig') != canonical_final[section]:
                    fail('FINAL_CONTENT_MISMATCH', name + ': does not match the current canonical manuscript')
            if plan:
                expected = compile_plan(data, 'full')
                actual = deepcopy(plan)
                declared_input = actual.pop('input_sha256', None)
                if declared_input is not None and declared_input != files['manuscript'][2]:
                    fail('PLAN_INPUT_MISMATCH', 'Plan was compiled from another manuscript')
                if actual != expected:
                    fail('PLAN_NOT_CANONICAL', 'Current plan differs from current manuscript compiled by this package')
        except (ValueError, TypeError, KeyError, AttributeError) as exc:
            fail('CURRENT_STRUCTURE_FAIL', exc)
    if plan and files['docx'] and package_root and files['contract']:
        try:
            current_saved = check_saved(plan, files['docx'][0], 'full', assets=package_root / 'assets')
            if current_saved.get('status') != 'SAVED_CONTENT_MATCH' or current_saved.get('format_validation') != 'PASS':
                fail('CURRENT_SAVED_FAIL', 'Current saved content/format check failed')
        except (OSError, ValueError, TypeError, KeyError, AttributeError, BadZipFile) as exc:
            fail('CURRENT_SAVED_FAIL', exc)

    reports = record.get('reports', {})
    for name, fresh in [('structure', current_structure), ('saved_docx', current_saved)]:
        evidence = artifact(reports.get(name), 'report/' + name)
        report = load_json(evidence, 'report/' + name)
        if fresh is None:
            fail('CURRENT_CHECK_NOT_PERFORMED', name + ': current inputs could not be checked')
            continue
        if report is None:
            continue
        if name == 'structure':
            if files['manuscript'] and report.get('input_sha256') != files['manuscript'][2]:
                fail('REPORT_INPUT_MISMATCH', name)
            compare_keys = list(fresh)
        else:
            compare_keys = ['status', 'scope', 'saved_sha256', 'checked_blocks', 'errors', 'content_validation',
                            'format_validation', 'format_scope', 'format_errors',
                            'plan_sha256', 'contract_sha256', 'reference_sha256',
                            'layout_geometry_review', 'semantic_review', 'question_answer_validity']
        if any(key not in fresh or report.get(key) != fresh[key] for key in compare_keys):
            fail('REPORT_CONTENT_MISMATCH', name + ': existing report does not match a fresh check')

    page_count = None
    split_context = None
    if split_mode:
        from split_release_support import check_split_evidence
        manifest = load_json(files.get('split_manifest'), 'split_manifest')
        split_context = check_split_evidence(manifest, reports, files, base)
        errors.extend(split_context['errors']); pending.extend(split_context['pending'])
        protected.update(split_context['protected_paths'])
        bindings.update(split_context['bindings'])
        page_count = split_context['pages']
    integrated_page_count = None
    if files['pdf']:
        try:
            integrated_page_count = pdf_pages(files['pdf'][0])
            if not split_mode:
                page_count = integrated_page_count
            if integrated_page_count < 1:
                fail('PDF_EMPTY', 'PDF has no pages')
        except RuntimeError as exc:
            wait('PDF_CHECK_UNAVAILABLE', exc)
        except Exception as exc:
            fail('PDF_INVALID', exc)
    render = load_json(artifact(reports.get('word_render'), 'report/word_render'), 'report/word_render')
    if render is not None:
        if render.get('status') != 'PASS' or render.get('renderer') != 'Microsoft Word':
            wait('WORD_NOT_PERFORMED', 'Final pagination requires an actually completed Microsoft Word render')
        elif not (render.get('source_unchanged') is True and
                  render.get('source_sha256') == bindings.get('docx_sha256') and
                  render.get('pdf_sha256') == bindings.get('pdf_sha256') and
                  type(render.get('pages')) is int and render.get('pages') > 0 and
                  (integrated_page_count is None or render.get('pages') == integrated_page_count)):
            fail('WORD_RENDER_MISMATCH', 'Word receipt must bind the current DOCX/PDF and actual PDF page count')
        required_text(render.get('version'), 'Word renderer/version')
        required_text(render.get('execution_id'), 'Word renderer/execution_id')

    required_bindings = {
        'source': ['package_sha256', 'source_content_sha256'],
        'learning': ['package_sha256', 'learning_content_sha256', 'learning_final_sha256'],
        'questions': ['package_sha256', 'assessment_content_sha256', 'learning_final_sha256', 'assessment_final_sha256'],
        'word_layout': ['package_sha256', 'plan_sha256', 'contract_sha256', 'docx_sha256', 'pdf_sha256'],
        'release': ['package_sha256'] + [name + '_sha256' for name in artifact_names],
    }
    if split_mode:
        split_keys = ['split_manifest_sha256', 'volume_set_sha256', 'pdf_set_sha256',
                      'word_renders_sha256', 'word_page_map_sha256']
        required_bindings['word_layout'] = ['package_sha256', 'plan_sha256', 'contract_sha256'] + split_keys
        required_bindings['release'] += split_keys + ['delivery_zip_sha256']
    # Optional compact R evidence supplements all existing gates. It never
    # substitutes for a real release reviewer or Word visual review.
    release_text_warnings = []
    if 'release_text' in reports:
        diagnostic = load_json(artifact(reports.get('release_text'), 'report/release_text'), 'report/release_text')
        if diagnostic is not None:
            try:
                from check_release_text import check_files
                names = ('manuscript','plan','docx','pdf','learning_final','assessment_final')
                if not all(files.get(name) for name in names):
                    raise ValueError('Current diagnostic inputs unavailable')
                fresh = check_files(**{name: files[name][0] for name in names})
                if diagnostic != fresh:
                    fail('RELEASE_TEXT_REPORT_MISMATCH', 'Diagnostic differs from current files/checker')
                if fresh['errors']:
                    fail('RELEASE_TEXT_MACHINE_FAILURE', fresh['errors'])
                release_text_warnings = [row['id'] for row in fresh['warnings']]
            except Exception as exc:
                fail('RELEASE_TEXT_CHECK_UNAVAILABLE', exc)
    reviews = record.get('reviews', [])
    if not isinstance(reviews, list):
        fail('REVIEW_FORMAT', 'reviews must be an array'); reviews = []
    kinds = {kind: [] for kind in REVIEW_KINDS}
    review_ids = set()
    contributors, question_groups = [], []
    bundle_mode = False
    for ref in reviews:
        evidence = artifact(ref, 'review/' + str(ref.get('path', '?')) if isinstance(ref, dict) else 'review')
        review = load_json(evidence, 'review')
        if review is None:
            continue
        kind = review.get('kind')
        if kind not in kinds:
            fail('REVIEW_KIND', kind); continue
        if review.get('type') == 'review_bundle':
            from review_coverage import validate_bundle
            bundle_mode = True
            identity = review.get('id')
            if not required_text(identity, 'review/id') or identity in review_ids:
                fail('REVIEW_DUPLICATE_ID', identity)
            if isinstance(identity, str):review_ids.add(identity)
            try:
                result = validate_bundle(review, data or {}, bindings, page_count, producer, base,
                                         current_structure=current_structure,
                                         word_context=split_context if split_mode and kind == 'word_layout' else None)
            except (ValueError,TypeError,KeyError,AttributeError) as exc:
                fail('REVIEW_BUNDLE_INVALID', exc)
                continue
            errors.extend(result['errors']);pending.extend(result['pending'])
            protected.update(result['protected_paths'])
            if result['aggregate'] is not None:
                for child in result['contributors']:
                    if child['id'] in review_ids:
                        fail('REVIEW_DUPLICATE_ID', child['id'])
                    review_ids.add(child['id'])
                contributors.extend(result['contributors'])
                kinds[kind].append(result['aggregate'])
                if kind == 'questions':
                    question_groups.append({'role':review.get('role'),
                        'reviewers':{x['reviewer_id'] for x in result['contributors']},
                        'executions':{x['execution_id'] for x in result['contributors']}})
            continue
        if review.get('type') in {'review_shard','review_aggregate','learning_continuity'}:
            fail('REVIEW_BUNDLE_REQUIRED', 'Partial/derived evidence must be validated through its bundle')
            continue
        if split_mode and kind == 'word_layout':
            fail('SPLIT_WORD_BUNDLE_REQUIRED', 'All six DOCX files require a current J/K coverage bundle')
        kinds[kind].append(review)
        identity = review.get('id')
        if not required_text(identity, 'review/id') or identity in review_ids:
            fail('REVIEW_DUPLICATE_ID', identity)
        review_ids.add(identity)
        for key in ('reviewer_id', 'execution_id', 'performed_at', 'method', 'summary'):
            required_text(review.get(key), str(identity) + '/' + key)
        if review.get('status') != 'PASS':
            wait('REVIEW_PENDING', str(identity) + ': ' + str(review.get('status')))
        expected_scope = scope
        if scope and kind in {'source', 'learning'}:
            expected_scope = {key: value for key, value in scope.items()
                              if key != 'question_ids' and (kind != 'source' or key != 'unit_ids')}
        if review.get('scope') != expected_scope:
            fail('REVIEW_SCOPE', str(identity) + ': full source/unit/question coverage must match the current request')
        rb = review.get('bindings', {})
        if any(key not in bindings or rb.get(key) != bindings[key] for key in required_bindings[kind]):
            fail('REVIEW_STALE_BINDINGS', identity)
        if kind in {'learning', 'questions', 'release'}:
            if (review.get('reviewer_id') == producer.get('reviewer_id') or
                    review.get('execution_id') == producer.get('execution_id')):
                fail('REVIEW_NOT_INDEPENDENT', identity)
            if review.get('independent') is not True:
                fail('REVIEW_NOT_INDEPENDENT', identity)
        findings = review.get('findings')
        if 'no_findings' in review:
            if kind != 'source' or review['no_findings'] is not True:
                fail('NO_FINDINGS_DECLARATION', str(identity) + ': only source may declare no_findings:true')
            if review['no_findings'] is True and isinstance(findings, list) and findings:
                fail('FINDINGS_CONFLICT', str(identity) + ': no_findings:true conflicts with recorded findings')
        # Only an explicit source-review declaration can replace an omitted
        # array. A present null/malformed array still fails, and the original
        # receipt bytes are never filled in or rewritten by this validator.
        if 'findings' not in review and kind == 'source' and review.get('no_findings') is True:
            findings = []
        if not isinstance(findings, list):
            fail('FINDINGS_REQUIRED', identity)
        else:
            finding_ids = set()
            for finding in findings:
                if not isinstance(finding, dict):
                    fail('FINDING_FORMAT', identity); continue
                fid = finding.get('id')
                if isinstance(fid, str):
                    if fid in finding_ids:
                        fail('FINDING_FORMAT', str(identity) + ': duplicate finding ID')
                    finding_ids.add(fid)
                if finding.get('status') != 'resolved':
                    wait('OPEN_FINDING', str(identity) + '/' + str(finding.get('id')))
                for key in ('id', 'description', 'resolution', 'recheck'):
                    required_text(finding.get(key), str(identity) + '/finding/' + key)
        if kind == 'questions' and data:
            question_groups.append({'role':review.get('role'),
                'reviewers':{review.get('reviewer_id')}, 'executions':{review.get('execution_id')}})
            answers = {q['id']: q['answer'] for q in data.get('assessment', {}).get('questions', [])}
            if review.get('answers') != answers:
                fail('INDEPENDENT_ANSWERS', str(identity) + ': reviewed answers do not match all current questions')
            if review.get('solved_before_answer_key') is not True:
                fail('ANSWERS_NOT_BLIND', identity)
            needed = set((current_structure or {}).get('independent_length_review_required', []))
            length_reviews = review.get('length_reviews', {})
            if not isinstance(length_reviews, dict):
                fail('LENGTH_REVIEW_FORMAT', identity)
            else:
                if set(length_reviews) - set(answers):
                    fail('LENGTH_REVIEW_UNKNOWN_QUESTION', identity)
                for qid in sorted(needed):
                    row = length_reviews.get(qid)
                    if not isinstance(row, dict) or row.get('status') != 'PASS':
                        wait('LENGTH_REVIEW_PENDING', str(identity) + '/' + qid)
                        continue
                    required_text(row.get('rationale'), str(identity) + '/' + qid + '/length rationale')
                    current_ids = current_structure['question_views'][qid]['length_comparison']['benchmark_ids']
                    if row.get('benchmark_ids') != current_ids:
                        fail('LENGTH_REVIEW_BENCHMARK_MISMATCH', str(identity) + '/' + qid)
        if kind == 'word_layout':
            if page_count is not None and (review.get('pages_reviewed') != list(range(1, page_count + 1)) or
                    not isinstance(review.get('detail_pages'), list) or not review['detail_pages'] or
                    any(type(x) is not int or not 1 <= x <= page_count for x in review['detail_pages'])):
                fail('WORD_VISUAL_COVERAGE', identity)
            if review.get('renderer') != 'Microsoft Word':
                wait('WORD_VISUAL_NOT_PERFORMED', identity)
        if kind == 'release' and release_text_warnings:
            dispositions = review.get('release_text_dispositions', {})
            if not isinstance(dispositions,dict):
                fail('RELEASE_TEXT_DISPOSITIONS', identity);dispositions = {}
            for warning_id in release_text_warnings:
                row = dispositions.get(warning_id)
                if not isinstance(row,dict) or row.get('status') != 'resolved':
                    wait('RELEASE_TEXT_REVIEW_PENDING', str(identity)+'/'+warning_id)
                else:
                    for key in ('resolution','recheck'):
                        required_text(row.get(key), str(identity)+'/'+warning_id+'/'+key)
    for kind, minimum in [('source', 1), ('learning', 1), ('questions', 2), ('word_layout', 1), ('release', 1)]:
        if len(kinds[kind]) < minimum:
            wait('MISSING_REVIEW', f'{kind}: need {minimum}, found {len(kinds[kind])}')
    if (bundle_mode or split_mode) and {group['role'] for group in question_groups} != {'M','N'}:
        fail('QUESTION_REVIEW_ROLES', 'Bundle mode requires explicit independent full-coverage M and N groups')
    for index, group in enumerate(question_groups):
        for other in question_groups[index+1:]:
            if group['reviewers'] & other['reviewers'] or group['executions'] & other['executions']:
                fail('QUESTION_REVIEWERS_NOT_DISTINCT', 'Two actual independent reviewer and execution identities are required')
    # A user's post-delivery requests are separate from the textbook text and
    # may invalidate completion before any artifact bytes have changed.
    feedback_summary = {'status': 'NOT_RECORDED'}
    current_feedback = base / '사용자수정요청.json'
    if current_feedback.is_file():
        protected.add(str(current_feedback))
        if 'user_feedback' not in record:
            wait('USER_FEEDBACK_LINK_MISSING', 'Current 사용자수정요청.json must be linked before re-release')
            feedback_summary = {'status': 'REVIEW_PENDING'}
        else:
            try:
                if path_for(record['user_feedback']['ledger']['path']) != current_feedback:
                    fail('USER_FEEDBACK_CURRENT_LEDGER', 'Use the current ledger, not an archived request snapshot')
            except (TypeError, KeyError, ValueError):
                fail('USER_FEEDBACK_CURRENT_LEDGER', 'Current request ledger reference is invalid')
    if 'user_feedback' in record:
        from user_feedback import validate_user_feedback
        try:
            feedback_result = validate_user_feedback(record['user_feedback'], bindings, producer, base,
                required_bindings=required_bindings['release'] if split_mode else None)
            errors.extend(feedback_result['errors'])
            pending.extend(feedback_result['pending'])
            protected.update(feedback_result['protected_paths'])
            feedback_summary = feedback_result['summary']
        except (OSError, ValueError, TypeError, KeyError, AttributeError) as exc:
            fail('USER_FEEDBACK_INVALID', exc)
            feedback_summary = {'status': 'FAIL'}
    return {
        'status': 'FAIL' if errors else 'REVIEW_PENDING' if pending else 'READY_FOR_RELEASE',
        'scope': 'full', 'errors': errors, 'pending': pending, 'checked_artifacts': checked,
        'observed_sha256': observed, 'package_sha256': inventory['sha256'] if inventory else None,
        'bindings': bindings, 'review_scope': scope,
        ('word_pages' if split_mode else 'pdf_pages'): page_count,
        **({'delivery_mode': 'integrated_plus_five_docx', 'delivery_files': split_context['delivery_files'],
            'docx_files': split_context['docx_files'],
            'word_page_map': split_context['page_map']} if split_mode and split_context else {}),
        'assessment_configuration': configuration,
        'review_contributors': contributors,
        'user_feedback': feedback_summary,
        'protected_paths': sorted(protected),
        'limits': ['Hash/coverage checks do not prove review truth, human/agent independence, translation accuracy or unique answers.',
                   'READY_FOR_RELEASE validates supplied execution evidence and current files; it does not create a FINAL or perform a review.',
                   'Unrecorded user messages cannot be detected; NOT_RECORDED never means user visual approval.'],
    }


def main(*, delivery_mode=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('record', type=Path, nargs='?', help='release-record JSON')
    parser.add_argument('report', type=Path, nargs='?', help='verification JSON output; never an input file')
    parser.add_argument('--fingerprint', type=Path, help='print full static-package file map/fingerprint without verifying a textbook')
    args = parser.parse_args()
    if args.fingerprint:
        if args.record or args.report:
            parser.error('--fingerprint cannot be combined with record/report')
        print(json.dumps(package_inventory(args.fingerprint), ensure_ascii=False, indent=2))
        return 0
    if not args.record or not args.report:
        parser.error('record and report are required')
    if args.report.suffix.lower() != '.json':
        raise ValueError('Verification report must have a .json extension')
    if args.record.resolve() == args.report.resolve():
        raise ValueError('Verification report must not overwrite the release record')
    # Protect the current request ledger even if the release record cannot be
    # parsed and verify() never gets a chance to discover referenced inputs.
    if args.report.resolve() == args.record.resolve().parent / '사용자수정요청.json':
        raise ValueError('Verification report must not overwrite the current user request ledger')
    raw = args.record.read_bytes()
    output_forbidden = False
    try:
        record = json.loads(raw.decode('utf-8-sig'), object_pairs_hook=_unique_json)
        if not isinstance(record, dict):
            raise ValueError('Release record must be a JSON object')
        # Protect referenced inputs even if a malformed record fails early.
        def referenced_paths(value):
            if isinstance(value, dict):
                for key, child in value.items():
                    if key == 'path' and isinstance(child, str):
                        candidate = Path(child)
                        yield (candidate if candidate.is_absolute() else args.record.resolve().parent / candidate).resolve()
                    yield from referenced_paths(child)
            elif isinstance(value, list):
                for child in value:
                    yield from referenced_paths(child)
        if args.report.resolve() in set(referenced_paths(record)):
            output_forbidden = True
            raise ValueError('Verification report must not overwrite a referenced input')
        package_path = record.get('package', {}).get('root')
        if isinstance(package_path, str) and package_path:
            package_path = Path(package_path)
            package_path = (package_path if package_path.is_absolute() else args.record.resolve().parent / package_path).resolve()
            if args.report.resolve().is_relative_to(package_path):
                output_forbidden = True
                raise ValueError('Verification report must stay outside the installed package')
        result = verify(record, args.record.resolve().parent, delivery_mode=delivery_mode)
    except (OSError, ValueError, TypeError, KeyError, AttributeError) as exc:
        result = {'status': 'FAIL', 'errors': [{'code': 'INVALID_RELEASE_RECORD', 'detail': str(exc)}], 'pending': []}
    if output_forbidden:
        raise ValueError('Verification report must not overwrite an input or a package file')
    if str(args.report.resolve()) in result.get('protected_paths', []):
        raise ValueError('Verification report must not overwrite any package, source, evidence, or output input')
    result['record_sha256'] = digest(raw)
    args.report.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({key: result.get(key) for key in ('status', 'scope', 'errors', 'pending')}, ensure_ascii=False))
    return 0 if result['status'] == 'READY_FOR_RELEASE' else 2 if result['status'] == 'REVIEW_PENDING' else 1


if __name__ == '__main__':
    raise SystemExit(main())
