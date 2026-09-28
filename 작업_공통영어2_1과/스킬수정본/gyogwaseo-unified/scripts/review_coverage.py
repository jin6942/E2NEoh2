"""Validate immutable shards of one CURRENT version, without performing review.

This is deliberately not a change-impact or old-PASS inheritance mechanism.
Each child has its own current hashes, actual execution identity and evidence.
The returned aggregate is coverage metadata, never a fictitious full reviewer.
The caller must still check the book, files, Word render, source/release reviews
and two independent question-review groups against the same current inputs.
"""
import hashlib
import json
from pathlib import Path
import re


REQUIRED_BINDINGS = {
    'learning': ('package_sha256', 'learning_content_sha256', 'learning_final_sha256'),
    'questions': ('package_sha256', 'assessment_content_sha256',
                  'learning_final_sha256', 'assessment_final_sha256'),
    'word_layout': ('package_sha256', 'plan_sha256', 'contract_sha256',
                    'docx_sha256', 'pdf_sha256'),
}
COMMON_RECEIPT = {'schema_version', 'type', 'id', 'kind', 'role', 'status',
                  'reviewer_id', 'execution_id', 'performed_at', 'independent',
                  'method', 'summary', 'scope', 'bindings', 'findings'}
HASH = re.compile(r'[0-9a-f]{64}')


def _unique_json(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('Duplicate JSON key: ' + key)
        result[key] = value
    return result


def validate_bundle(bundle, data, bindings, page_count, producer, base='.', *,
                    current_structure=None, word_context=None):
    """Return errors/pending, actual contributors and a derived aggregate.

    ``current_structure`` is the caller's fresh check_book report and is required
    for questions; missing length-review requirements never default to empty.
    Paths are relative to ``base`` (the release-record directory), including the
    learning continuity receipt. No receipt is rewritten or recursively expanded.
    Unknown fields are rejected so unimplemented inheritance cannot be implied.
    """
    errors, pending, contributors, protected = [], [], [], set()
    aggregate = None
    split_word = word_context is not None
    required_bindings = dict(REQUIRED_BINDINGS)
    if split_word:
        required_bindings['word_layout'] = ('package_sha256', 'plan_sha256', 'contract_sha256',
            'split_manifest_sha256', 'volume_set_sha256', 'pdf_set_sha256',
            'word_renders_sha256', 'word_page_map_sha256')

    def fail(code, detail):
        errors.append({'code': code, 'detail': str(detail)})

    def wait(code, detail):
        pending.append({'code': code, 'detail': str(detail)})

    def result():
        return {'errors': errors, 'pending': pending, 'aggregate': aggregate,
                'contributors': contributors, 'protected_paths': sorted(protected)}

    def fields(value, required, optional, name):
        if not isinstance(value, dict):
            fail('REVIEW_BUNDLE_SCHEMA', name + ': object required')
            return False
        missing, extra = required - set(value), set(value) - required - optional
        if missing or extra:
            fail('REVIEW_BUNDLE_SCHEMA', name + ': missing=' + str(sorted(missing)) +
                 ', unknown=' + str(sorted(extra)))
        return not missing and not extra

    def text(value, name):
        if not isinstance(value, str) or not value.strip():
            fail('MISSING_REVIEW_DETAIL', name)
            return False
        return True

    def ids(value, allowed, name, nonempty=False, integer=False):
        if not isinstance(value, list):
            fail('REVIEW_SCOPE', name + ': array required')
            return []
        valid = []
        for item in value:
            typed = type(item) is int if integer else isinstance(item, str) and bool(item.strip())
            if not typed or item not in allowed:
                fail('REVIEW_SCOPE', name + ': unknown or invalid ID ' + repr(item))
            elif item in valid:
                fail('REVIEW_SCOPE', name + ': duplicate ID ' + repr(item))
            else:
                valid.append(item)
        if nonempty and not value:
            fail('REVIEW_SCOPE', name + ': nonempty assigned scope required')
        return valid

    def binding_check(row, kind, name):
        rb = row.get('bindings')
        if not isinstance(rb, dict):
            fail('REVIEW_STALE_BINDINGS', name)
            return
        for key in required_bindings[kind]:
            current = bindings.get(key)
            if not isinstance(current, str) or not HASH.fullmatch(current) or rb.get(key) != current:
                fail('REVIEW_STALE_BINDINGS', name + '/' + key)
        # Extra supplied hashes are assertions, not a place to hide old versions.
        for key, value in rb.items():
            if key not in bindings or not isinstance(value, str) or not HASH.fullmatch(value) or value != bindings[key]:
                fail('REVIEW_STALE_BINDINGS', name + '/' + key)

    def load(ref, name):
        # A failed hash/schema must not make a referenced file eligible as the
        # caller's report output. Protect the path before validating the ref.
        path = None
        if isinstance(ref, dict) and isinstance(ref.get('path'), str) and ref['path'].strip():
            try:
                path = Path(ref['path'])
                path = (path if path.is_absolute() else Path(base) / path).resolve()
                protected.add(str(path))
            except (OSError, ValueError) as exc:
                fail('REVIEW_CHILD_INVALID', name + ': ' + str(exc))
                return None
        if not fields(ref, {'path', 'sha256'}, set(), name):
            return None
        if not text(ref.get('path'), name + '/path'):
            return None
        if not isinstance(ref.get('sha256'), str) or not HASH.fullmatch(ref['sha256']):
            fail('REVIEW_CHILD_HASH', name + ': a SHA-256 is required')
            return None
        try:
            if not path.is_file():
                wait('MISSING_REVIEW_CHILD', str(path))
                return None
            raw = path.read_bytes()
            if hashlib.sha256(raw).hexdigest() != ref['sha256']:
                fail('REVIEW_CHILD_HASH', str(path))
                return None
            value = json.loads(raw.decode('utf-8-sig'), object_pairs_hook=_unique_json)
            if not isinstance(value, dict):
                raise ValueError('Receipt must be a JSON object')
            return value, str(path)
        except (OSError, ValueError, UnicodeError) as exc:
            fail('REVIEW_CHILD_INVALID', name + ': ' + str(exc))
            return None

    def receipt(row, kind, role, receipt_type, name, extra):
        fields(row, COMMON_RECEIPT | extra, {'context'}, name)
        if type(row.get('schema_version')) is not int or row['schema_version'] != 1 or row.get('type') != receipt_type:
            fail('REVIEW_BUNDLE_SCHEMA', name + ': unsupported child schema/type')
        if row.get('kind') != kind or not isinstance(row.get('role'), str) or row['role'] not in role:
            fail('REVIEW_ROLE', name)
        for key in ('id', 'reviewer_id', 'execution_id', 'performed_at', 'method', 'summary'):
            text(row.get(key), name + '/' + key)
        if row.get('status') != 'PASS':
            wait('REVIEW_PENDING', name + ': ' + str(row.get('status')))
        if (row.get('independent') is not True or
                row.get('reviewer_id') == producer.get('reviewer_id') or
                row.get('execution_id') == producer.get('execution_id')):
            fail('REVIEW_NOT_INDEPENDENT', name)
        binding_check(row, kind, name)
        findings = row.get('findings')
        if not isinstance(findings, list):
            fail('FINDINGS_REQUIRED', name)
        else:
            finding_ids = set()
            for finding in findings:
                if not fields(finding, {'id', 'status', 'description', 'resolution', 'recheck'}, set(), name + '/finding'):
                    continue
                for key in ('id', 'description', 'resolution', 'recheck'):
                    text(finding.get(key), name + '/finding/' + key)
                fid = finding.get('id')
                if isinstance(fid, str):
                    if fid in finding_ids:
                        fail('FINDING_FORMAT', name + ': duplicate finding ID')
                    finding_ids.add(fid)
                if finding.get('status') != 'resolved':
                    wait('OPEN_FINDING', name + '/' + str(fid))

    if not isinstance(bundle, dict):
        fail('REVIEW_BUNDLE_SCHEMA', 'Bundle must be an object')
        return result()
    if not isinstance(data, dict) or not isinstance(bindings, dict) or not isinstance(producer, dict):
        fail('REVIEW_BUNDLE_CONTEXT', 'Current manuscript, bindings and producer are required')
        return result()
    kind = bundle.get('kind')
    if not isinstance(kind, str) or kind not in REQUIRED_BINDINGS:
        fail('REVIEW_KIND', str(kind) + ': source and release cannot be bundled')
        return result()
    page_key = 'word_pages' if split_word else 'pdf_pages'
    extra = {'continuity'} if kind == 'learning' else {page_key} if kind == 'word_layout' else set()
    fields(bundle, {'schema_version', 'type', 'id', 'kind', 'role', 'summary',
                    'bindings', 'scope', 'children'} | extra, set(), 'bundle')
    if type(bundle.get('schema_version')) is not int or bundle['schema_version'] != 1 or bundle.get('type') != 'review_bundle':
        fail('REVIEW_BUNDLE_SCHEMA', 'Expected schema_version=1, type=review_bundle')
    for key in ('id', 'summary'):
        text(bundle.get(key), 'bundle/' + key)
    roles = {'learning': {'L'}, 'questions': {'M', 'N'}, 'word_layout': {'JK'}}
    if not isinstance(bundle.get('role'), str) or bundle['role'] not in roles[kind]:
        fail('REVIEW_ROLE', 'bundle/' + str(bundle.get('role')))
        return result()
    binding_check(bundle, kind, 'bundle')
    for key in ('reviewer_id', 'execution_id'):
        text(producer.get(key), 'producer/' + key)
    try:
        source_order = [row['id'] for row in data['sources']]
        unit_order = [row['id'] for row in data['units']]
        sentence_order = [row['id'] for row in data['sentences']]
        question_order = [row['id'] for row in data.get('assessment', {}).get('questions', [])]
        for name, order in [('sources', source_order), ('units', unit_order),
                            ('sentences', sentence_order), ('questions', question_order)]:
            if any(not isinstance(x, str) or not x.strip() for x in order) or len(order) != len(set(order)):
                raise ValueError('Invalid current ' + name + ' IDs')
        units = {row['id']: row for row in data['units']}
        answers = {row['id']: row['answer'] for row in data.get('assessment', {}).get('questions', [])}
    except (KeyError, TypeError, ValueError) as exc:
        fail('REVIEW_BUNDLE_CONTEXT', exc)
        return result()
    source_set, unit_set, sentence_set, question_set = map(set, (source_order, unit_order, sentence_order, question_order))
    expected_scope = {'kind': 'full', 'source_ids': source_order, 'unit_ids': unit_order}
    if kind != 'learning':
        expected_scope['question_ids'] = question_order
    if bundle.get('scope') != expected_scope:
        fail('REVIEW_SCOPE', 'Bundle full coverage must match the current request')
    needed, views, shared_groups = set(), {}, []
    if kind == 'questions':
        groups = data.get('assessment', {}).get('passage_groups', [])
        if not isinstance(groups, list):
            fail('REVIEW_BUNDLE_CONTEXT', 'Current shared passage groups must be an array')
            groups = []
        for group in groups:
            if not isinstance(group, dict):
                fail('REVIEW_BUNDLE_CONTEXT', 'Current shared passage group must be an object')
                continue
            members = ids(group.get('question_ids'), question_set, 'shared passage group/' + str(group.get('id')), nonempty=True)
            shared_groups.append(set(members))
        if (not isinstance(current_structure, dict) or current_structure.get('status') != 'STRUCTURE_PASS' or
                not isinstance(current_structure.get('independent_length_review_required'), list) or
                not isinstance(current_structure.get('question_views'), dict)):
            fail('REVIEW_BUNDLE_CONTEXT', 'Fresh full structure/length review requirements are required')
        else:
            needed = set(ids(current_structure['independent_length_review_required'], question_set, 'length requirements'))
            views = current_structure['question_views']
            if set(views) != question_set:
                fail('REVIEW_BUNDLE_CONTEXT', 'Fresh question views must cover current questions')
    pages = set(range(1, page_count + 1)) if type(page_count) is int and page_count > 0 else set()
    if kind == 'word_layout' and (not pages or type(bundle.get(page_key)) is not int or bundle[page_key] != page_count):
        fail('WORD_VISUAL_COVERAGE', 'Current actual Word/PDF page count is required')

    children = bundle.get('children')
    if not isinstance(children, list) or not children:
        fail('REVIEW_BUNDLE_SCHEMA', 'Nonempty child references required')
        return result()
    review_ids = {bundle.get('id')} if isinstance(bundle.get('id'), str) else set()
    paths, executions, execution_reviewers = set(), set(), {}
    assigned, covered_sources, boundaries, detail_pages, actual_roles = set(), set(), set(), set(), set()
    boundary_observers = {}
    union_answers, union_lengths = {}, {}

    def identity(row, path, ref, name, continuity=False):
        rid, execution, reviewer = row.get('id'), row.get('execution_id'), row.get('reviewer_id')
        if isinstance(rid, str):
            if rid in review_ids:
                fail('REVIEW_DUPLICATE_ID', rid)
            review_ids.add(rid)
        if path in paths:
            fail('REVIEW_CHILD_DUPLICATE', path)
        paths.add(path)
        if isinstance(execution, str):
            if execution in executions and not continuity:
                fail('REVIEW_EXECUTION_DUPLICATE', name)
            if execution in execution_reviewers and execution_reviewers[execution] != reviewer:
                fail('REVIEW_EXECUTION_IDENTITY', name + ': one execution cannot acquire another reviewer label')
            executions.add(execution)
            execution_reviewers[execution] = reviewer
        item = {key: row.get(key) for key in ('id', 'kind', 'role', 'reviewer_id', 'execution_id')}
        item.update(path=path, sha256=ref['sha256'], unit_ids=[], question_ids=[], pages_reviewed=[])
        contributors.append(item)
        return item

    def own(values, name):
        for value in values:
            if value in assigned:
                fail('REVIEW_COVERAGE_DUPLICATE', name + '/' + str(value))
            assigned.add(value)

    for index, ref in enumerate(children):
        name = 'child/' + str(index)
        loaded = load(ref, name)
        if loaded is None:
            continue
        row, path = loaded
        extras = {'answers', 'solved_before_answer_key', 'length_reviews'} if kind == 'questions' else \
            {'renderer', 'pages_reviewed', 'detail_pages', 'context_pages', 'boundaries'} if kind == 'word_layout' else set()
        child_roles = {'J', 'K'} if kind == 'word_layout' else {bundle.get('role')}
        receipt(row, kind, child_roles, 'review_shard', name, extras)
        contributor = identity(row, path, ref, name)
        role = row.get('role')
        if isinstance(role, str):
            actual_roles.add(role)
        child_scope = row.get('scope', {})
        scope_fields = {'source_ids', 'unit_ids', 'sentence_ids'} if kind == 'learning' else \
            {'question_ids'} if kind == 'questions' else {'pages'}
        fields(child_scope, {'kind'} | scope_fields, set(), name + '/scope')
        if not isinstance(child_scope, dict):
            child_scope = {}
        if child_scope.get('kind') != 'partial':
            fail('REVIEW_SCOPE', name + ': actual shard scope must be partial')
        context = row.get('context', {})
        if kind != 'word_layout':
            fields(context, set(), scope_fields, name + '/context')
            if isinstance(context, dict):
                allowed = {'source_ids': source_set, 'unit_ids': unit_set, 'sentence_ids': sentence_set,
                           'question_ids': question_set}
                for key, values in context.items():
                    if key in allowed:
                        ids(values, allowed[key], name + '/context/' + key)
        elif 'context' in row:
            fail('REVIEW_BUNDLE_SCHEMA', name + ': use context_pages for Word context')
        if kind == 'learning':
            owned = ids(child_scope.get('unit_ids'), unit_set, name + '/units', nonempty=True)
            sids = ids(child_scope.get('sentence_ids'), sentence_set, name + '/sentences', nonempty=True)
            sources = ids(child_scope.get('source_ids'), source_set, name + '/sources', nonempty=True)
            try:
                expected_sentences = [sid for uid in owned for sid in units[uid]['sentence_ids']]
                expected_sources = {units[uid]['source_id'] for uid in owned}
                if set(sids) != set(expected_sentences) or len(sids) != len(expected_sentences) or set(sources) != expected_sources:
                    fail('LEARNING_UNIT_SPLIT', name + ': each assigned unit needs every sentence and its source')
            except (KeyError, TypeError) as exc:
                fail('REVIEW_BUNDLE_CONTEXT', exc)
            own(owned, name)
            covered_sources.update(sources)
            contributor['unit_ids'] = owned
        elif kind == 'questions':
            owned = ids(child_scope.get('question_ids'), question_set, name + '/questions', nonempty=True)
            for group in shared_groups:
                if group & set(owned) and not group <= set(owned):
                    fail('QUESTION_SHARED_GROUP_SPLIT', name + ': connected shared-passage questions need one actual owner')
            own(owned, name)
            contributor['question_ids'] = owned
            if row.get('answers') != {qid: answers[qid] for qid in owned}:
                fail('INDEPENDENT_ANSWERS', name + ': answer evidence must match exactly the assigned current questions')
            if row.get('solved_before_answer_key') is not True:
                fail('ANSWERS_NOT_BLIND', name)
            if isinstance(row.get('answers'), dict):
                union_answers.update(row['answers'])
            length_reviews = row.get('length_reviews')
            if not isinstance(length_reviews, dict):
                fail('LENGTH_REVIEW_FORMAT', name)
            else:
                if set(length_reviews) - set(owned):
                    fail('LENGTH_REVIEW_UNKNOWN_QUESTION', name)
                for qid in (needed & set(owned)) | set(length_reviews):
                    detail = length_reviews.get(qid)
                    if not isinstance(detail, dict) or detail.get('status') != 'PASS':
                        wait('LENGTH_REVIEW_PENDING', name + '/' + qid)
                        continue
                    fields(detail, {'status', 'rationale', 'benchmark_ids'}, set(), name + '/length/' + qid)
                    text(detail.get('rationale'), name + '/' + qid + '/length rationale')
                    view = views.get(qid)
                    comparison = view.get('length_comparison') if isinstance(view, dict) else None
                    expected = comparison.get('benchmark_ids') if isinstance(comparison, dict) else None
                    if not isinstance(expected, list) or detail.get('benchmark_ids') != expected:
                        fail('LENGTH_REVIEW_BENCHMARK_MISMATCH', name + '/' + qid)
                union_lengths.update(length_reviews)
        else:
            owned = ids(child_scope.get('pages'), pages, name + '/pages', nonempty=True, integer=True)
            own(owned, name)
            contributor['pages_reviewed'] = owned
            if row.get('pages_reviewed') != child_scope.get('pages'):
                fail('WORD_VISUAL_COVERAGE', name + ': assigned pages and actual reviewed pages differ')
            context_pages = ids(row.get('context_pages'), pages, name + '/context_pages', integer=True)
            if set(owned) & set(context_pages):
                fail('REVIEW_SCOPE', name + ': context pages must be context-only')
            details = ids(row.get('detail_pages'), set(owned) | set(context_pages), name + '/detail_pages', nonempty=True, integer=True)
            detail_pages.update(details)
            if row.get('renderer') != 'Microsoft Word':
                wait('WORD_VISUAL_NOT_PERFORMED', name)
            checks = row.get('boundaries')
            receipt_boundaries = set()
            contributor['boundaries_reviewed'] = []
            if not isinstance(checks, list):
                fail('WORD_BOUNDARY_COVERAGE', name + ': boundary evidence array required')
                checks = []
            for check in checks:
                if not fields(check, {'pages', 'status', 'summary'}, set(), name + '/boundary'):
                    continue
                pair = check.get('pages')
                if (not isinstance(pair, list) or len(pair) != 2 or any(type(p) is not int for p in pair) or
                        pair[1] != pair[0] + 1 or not set(pair) <= (set(owned) | set(context_pages)) or
                        not set(pair) & set(owned)):
                    fail('WORD_BOUNDARY_COVERAGE', name + ': boundary must be adjacent current pages available to its actual owner')
                    continue
                key = tuple(pair)
                if key in receipt_boundaries:
                    fail('REVIEW_COVERAGE_DUPLICATE', name + '/boundary/' + str(pair))
                else:
                    observers = boundary_observers.setdefault(key, [])
                    if any(row.get('reviewer_id') == reviewer or row.get('execution_id') == execution
                           for reviewer, execution in observers):
                        fail('WORD_BOUNDARY_NOT_INDEPENDENT', name + '/boundary/' + str(pair) +
                             ': repeated observations require distinct actual reviewer and execution identities')
                    observers.append((row.get('reviewer_id'), row.get('execution_id')))
                    contributor['boundaries_reviewed'].append(list(pair))
                receipt_boundaries.add(key)
                boundaries.add(key)
                text(check.get('summary'), name + '/boundary/summary')
                if check.get('status') != 'PASS':
                    wait('WORD_BOUNDARY_PENDING', name + '/' + str(pair))

    expected_assigned = unit_set if kind == 'learning' else question_set if kind == 'questions' else pages
    if assigned != expected_assigned:
        fail('REVIEW_COVERAGE_MISSING', kind + ': uncovered assigned scope ' + str(sorted(expected_assigned - assigned)))
    if kind == 'learning':
        if covered_sources != source_set:
            fail('REVIEW_COVERAGE_MISSING', 'learning: every source must be covered')
        loaded = load(bundle.get('continuity'), 'continuity')
        if loaded:
            row, path = loaded
            receipt(row, kind, {'L'}, 'learning_continuity', 'continuity', set())
            contributor = identity(row, path, bundle['continuity'], 'continuity', continuity=True)
            contributor['kind'] = 'learning_continuity'
            contributor['unit_ids'] = unit_order
            if row.get('scope') != expected_scope:
                fail('LEARNING_CONTINUITY_SCOPE', 'Continuity evidence must check terminology, references and connections across every unit')
            if 'context' in row:
                fail('REVIEW_BUNDLE_SCHEMA', 'Continuity uses the full current source/unit scope')
    if kind == 'word_layout':
        if actual_roles != {'J', 'K'}:
            fail('REVIEW_ROLE', 'Word partition requires actual J and K child roles')
        for left in contributors:
            for right in contributors:
                if left['role'] != right['role'] and (left['reviewer_id'] == right['reviewer_id'] or
                                                       left['execution_id'] == right['execution_id']):
                    fail('REVIEW_NOT_INDEPENDENT', 'J and K must retain distinct actual reviewer/execution identities')
                    break
        expected_boundaries = ({tuple(pair) for pair in word_context.get('boundaries', [])} if split_word else
                               {(p, p + 1) for p in sorted(pages) if p + 1 in pages})
        if boundaries != expected_boundaries:
            fail('WORD_BOUNDARY_COVERAGE', 'Every current PDF page connection needs at least one valid actual observation')
    if not errors and not pending:
        aggregate = {'type': 'review_aggregate', 'id': bundle['id'], 'kind': kind,
                     'role': bundle['role'], 'status': 'PASS', 'scope': expected_scope,
                     'bindings': dict(bundle['bindings']), 'child_ids': [x['id'] for x in contributors]}
        if kind == 'questions':
            aggregate.update(answers=union_answers, solved_before_answer_key=True, length_reviews=union_lengths)
        elif kind == 'word_layout':
            aggregate.update(pages_reviewed=sorted(pages), detail_pages=sorted(detail_pages),
                             boundaries_reviewed=[list(pair) for pair in sorted(boundaries)],
                             renderer='Microsoft Word', **{page_key: page_count})
    return result()
