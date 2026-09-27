"""Validate recorded user requests and their CURRENT independent recheck.

This checks provenance, coverage and file bindings. It cannot establish whether
an instruction was understood or an edit is correct; an actual reviewer must
judge every criterion against the final saved artifacts and record evidence.
"""
import hashlib
import json
from pathlib import Path
import re


HASH = re.compile(r'[0-9a-f]{64}')
REQUIRED_BINDINGS = ('package_sha256', 'manuscript_sha256', 'plan_sha256',
                     'contract_sha256', 'docx_sha256', 'pdf_sha256',
                     'learning_final_sha256', 'assessment_final_sha256')


def _unique_json(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('Duplicate JSON key: ' + key)
        result[key] = value
    return result


def validate_user_feedback(value, bindings, producer, base='.', *, required_bindings=None):
    """Validate an explicit user_feedback reference (absence is caller-owned).

    Referenced paths are protected even when their hash or schema is invalid.
    Review records never inherit an earlier PASS or waive the normal S/L/M/N/
    J/K/R reviews. A text field is recorded evidence, not automatic proof of it.
    """
    errors, pending, protected = [], [], set()
    summary = {'status': 'USER_FEEDBACK_INVALID', 'round_id': None,
               'request_count': 0, 'active_request_count': 0,
               'withdrawn_request_count': 0, 'superseded_request_count': 0,
               'checked_request_ids': []}

    def fail(code, detail):
        errors.append({'code': code, 'detail': str(detail)})

    def wait(code, detail):
        pending.append({'code': code, 'detail': str(detail)})

    def result():
        summary['status'] = ('USER_FEEDBACK_INVALID' if errors else
                             'USER_FEEDBACK_PENDING' if pending else
                             'USER_FEEDBACK_PASS')
        return {'errors': errors, 'pending': pending,
                'protected_paths': sorted(protected), 'summary': summary}

    def fields(row, required, optional, name):
        if not isinstance(row, dict):
            fail('USER_FEEDBACK_SCHEMA', name + ': object required')
            return False
        missing = required - set(row)
        extra = set(row) - required - optional
        if missing or extra:
            fail('USER_FEEDBACK_SCHEMA', name + ': missing=' + str(sorted(missing)) +
                 ', unknown=' + str(sorted(extra)))
        return not missing and not extra

    def text(item, name):
        if not isinstance(item, str) or not item.strip():
            fail('USER_FEEDBACK_DETAIL', name + ': nonempty text required')
            return False
        return True

    def texts(items, name):
        if not isinstance(items, list) or not items:
            fail('USER_FEEDBACK_SCHEMA', name + ': nonempty text array required')
            return False
        valid = True
        for index, item in enumerate(items):
            valid = text(item, name + '/' + str(index)) and valid
        return valid

    def version(row, name):
        if type(row.get('schema_version')) is not int or row['schema_version'] != 1:
            fail('USER_FEEDBACK_SCHEMA', name + ': schema_version=1 required')

    def load(ref, name):
        path = None
        if isinstance(ref, dict) and isinstance(ref.get('path'), str) and ref['path'].strip():
            try:
                path = Path(ref['path'])
                path = (path if path.is_absolute() else Path(base) / path).resolve()
                protected.add(str(path))
            except (OSError, ValueError) as exc:
                fail('USER_FEEDBACK_FILE', name + ': ' + str(exc))
                return None
        if not fields(ref, {'path', 'sha256'}, set(), name):
            return None
        if not text(ref.get('path'), name + '/path'):
            return None
        if not isinstance(ref.get('sha256'), str) or not HASH.fullmatch(ref['sha256']):
            fail('USER_FEEDBACK_HASH', name + ': SHA-256 required')
            return None
        try:
            if not path.is_file():
                wait('USER_FEEDBACK_MISSING_FILE', str(path))
                return None
            raw = path.read_bytes()
            actual_hash = hashlib.sha256(raw).hexdigest()
            if actual_hash != ref['sha256']:
                fail('USER_FEEDBACK_HASH', str(path))
                return None
            row = json.loads(raw.decode('utf-8-sig'), object_pairs_hook=_unique_json)
            if not isinstance(row, dict):
                raise ValueError('JSON object required')
            return row, actual_hash
        except (OSError, ValueError, UnicodeError) as exc:
            fail('USER_FEEDBACK_FILE', name + ': ' + str(exc))
            return None

    # Discover/protect both references before rejecting any outer schema issue.
    refs = value if isinstance(value, dict) else {}
    ledger_data = load(refs.get('ledger'), 'user_feedback/ledger')
    if 'review' in refs:
        review_data = load(refs['review'], 'user_feedback/review')
    else:
        review_data = None
        wait('USER_FEEDBACK_REVIEW_PENDING', 'The recorded requests await an independent review')
    fields(value, {'ledger'}, {'review'}, 'user_feedback')
    if not isinstance(bindings, dict) or not isinstance(producer, dict):
        fail('USER_FEEDBACK_CONTEXT', 'Current bindings and producer are required')
        return result()
    for key in ('reviewer_id', 'execution_id'):
        text(producer.get(key), 'producer/' + key)
    if ledger_data is None:
        return result()
    ledger, ledger_hash = ledger_data
    fields(ledger, {'schema_version', 'round_id', 'requests'}, set(), 'ledger')
    version(ledger, 'ledger')
    if text(ledger.get('round_id'), 'ledger/round_id'):
        summary['round_id'] = ledger['round_id']
    requests = ledger.get('requests')
    if not isinstance(requests, list) or not requests:
        fail('USER_FEEDBACK_EMPTY_LEDGER', 'Recorded feedback requires at least one request')
        requests = []
    summary['request_count'] = len(requests)
    indexed, active, replacements = {}, {}, {}
    production_ids = {producer.get('reviewer_id')} if isinstance(producer.get('reviewer_id'), str) else set()
    production_runs = {producer.get('execution_id')} if isinstance(producer.get('execution_id'), str) else set()
    for index, request in enumerate(requests):
        name = 'ledger/requests/' + str(index)
        if not isinstance(request, dict):
            fail('USER_FEEDBACK_SCHEMA', name + ': object required')
            continue
        fields(request, {'id', 'user_text', 'source', 'targets', 'criteria',
                         'disposition', 'implementation'}, {'decision', 'superseded_by'}, name)
        for key in ('id', 'user_text', 'source'):
            text(request.get(key), name + '/' + key)
        texts(request.get('targets'), name + '/targets')
        texts(request.get('criteria'), name + '/criteria')
        request_id = request.get('id')
        valid_id = isinstance(request_id, str) and bool(request_id.strip())
        if valid_id:
            if request_id in indexed:
                fail('USER_FEEDBACK_REQUEST_IDS', 'Duplicate request ID: ' + request_id)
            else:
                indexed[request_id] = request
        disposition = request.get('disposition')
        if not isinstance(disposition, str) or disposition not in {'active', 'withdrawn', 'superseded'}:
            fail('USER_FEEDBACK_DISPOSITION', name)
        elif disposition == 'active':
            summary['active_request_count'] += 1
            if valid_id:
                active[request_id] = request
        else:
            summary[disposition + '_request_count'] += 1
        if disposition != 'active' or 'decision' in request:
            decision = request.get('decision')
            if fields(decision, {'user_text', 'source'}, set(), name + '/decision'):
                for key in ('user_text', 'source'):
                    text(decision.get(key), name + '/decision/' + key)
        if disposition == 'superseded':
            if text(request.get('superseded_by'), name + '/superseded_by') and valid_id:
                replacements[request_id] = request['superseded_by']
        elif 'superseded_by' in request:
            fail('USER_FEEDBACK_SUPERSESSION', name + ': only superseded requests have superseded_by')
        implementation = request.get('implementation')
        if not isinstance(implementation, dict):
            fail('USER_FEEDBACK_SCHEMA', name + '/implementation: object required')
            continue
        fields(implementation, {'status', 'producer_id', 'execution_id', 'detail'}, set(), name + '/implementation')
        for key in ('producer_id', 'execution_id'):
            if text(implementation.get(key), name + '/implementation/' + key) and disposition == 'active':
                (production_ids if key == 'producer_id' else production_runs).add(implementation[key])
        status = implementation.get('status')
        if not isinstance(status, str) or status not in {'pending', 'applied', 'no_change_needed', 'blocked'}:
            fail('USER_FEEDBACK_IMPLEMENTATION', name)
        elif status in {'applied', 'no_change_needed'}:
            text(implementation.get('detail'), name + '/implementation/detail')
        elif disposition == 'active':
            wait('USER_FEEDBACK_IMPLEMENTATION_PENDING', str(request_id) + ': ' + status)
        if 'detail' in implementation and not isinstance(implementation['detail'], str):
            fail('USER_FEEDBACK_DETAIL', name + '/implementation/detail: text required')

    for request_id, target in replacements.items():
        if target not in indexed or target == request_id:
            fail('USER_FEEDBACK_SUPERSESSION', request_id + ': replacement must name another existing request')
        seen, current = set(), request_id
        while current in replacements:
            if current in seen:
                fail('USER_FEEDBACK_SUPERSESSION', request_id + ': replacement cycle')
                break
            seen.add(current)
            current = replacements[current]

    if review_data is None:
        return result()
    review, _ = review_data
    fields(review, {'schema_version', 'round_id', 'ledger_sha256', 'bindings',
                    'reviewer_id', 'execution_id', 'performed_at', 'independent',
                    'status', 'checks'}, set(), 'review')
    version(review, 'review')
    for key in ('round_id', 'reviewer_id', 'execution_id', 'performed_at'):
        text(review.get(key), 'review/' + key)
    if review.get('round_id') != ledger.get('round_id'):
        fail('USER_FEEDBACK_ROUND', 'Review and ledger round_id differ')
    if review.get('ledger_sha256') != ledger_hash:
        fail('USER_FEEDBACK_STALE_LEDGER', 'Review does not bind the current request ledger')
    if (review.get('independent') is not True or
            not isinstance(review.get('reviewer_id'), str) or
            review['reviewer_id'] in production_ids or
            not isinstance(review.get('execution_id'), str) or
            review['execution_id'] in production_runs):
        fail('USER_FEEDBACK_NOT_INDEPENDENT', 'Review must use a different reviewer and execution from every active producer')
    if review.get('status') != 'PASS':
        wait('USER_FEEDBACK_REVIEW_PENDING', 'review/status is not PASS')
    rb = review.get('bindings')
    if not isinstance(rb, dict):
        fail('USER_FEEDBACK_STALE_BINDINGS', 'review/bindings: object required')
    else:
        for key in (REQUIRED_BINDINGS if required_bindings is None else required_bindings):
            current = bindings.get(key)
            if not isinstance(current, str) or not HASH.fullmatch(current) or rb.get(key) != current:
                fail('USER_FEEDBACK_STALE_BINDINGS', key)
        for key, item in rb.items():
            if key not in bindings or not isinstance(item, str) or not HASH.fullmatch(item) or item != bindings[key]:
                fail('USER_FEEDBACK_STALE_BINDINGS', key)
    checks = review.get('checks')
    if not isinstance(checks, list):
        fail('USER_FEEDBACK_COVERAGE', 'review/checks: array required')
        checks = []
    checked = set()
    for index, check in enumerate(checks):
        name = 'review/checks/' + str(index)
        if not isinstance(check, dict):
            fail('USER_FEEDBACK_SCHEMA', name + ': object required')
            continue
        fields(check, {'request_id', 'status', 'results'}, set(), name)
        request_id = check.get('request_id')
        if not isinstance(request_id, str) or request_id not in active or request_id in checked:
            fail('USER_FEEDBACK_COVERAGE', name + ': unknown, inactive or duplicate request ID')
            continue
        checked.add(request_id)
        if check.get('status') != 'PASS':
            wait('USER_FEEDBACK_REVIEW_PENDING', request_id + ': check status is not PASS')
        criteria = active[request_id].get('criteria')
        expected = set(range(len(criteria))) if isinstance(criteria, list) else set()
        results = check.get('results')
        if not isinstance(results, list):
            fail('USER_FEEDBACK_CRITERIA', name + '/results: array required')
            results = []
        covered = set()
        for item_index, item in enumerate(results):
            item_name = name + '/results/' + str(item_index)
            if not isinstance(item, dict):
                fail('USER_FEEDBACK_SCHEMA', item_name + ': object required')
                continue
            fields(item, {'criterion_index', 'status', 'evidence'}, set(), item_name)
            number = item.get('criterion_index')
            if type(number) is not int or number not in expected or number in covered:
                fail('USER_FEEDBACK_CRITERIA', item_name + ': unknown or duplicate criterion index')
            else:
                covered.add(number)
            if item.get('status') != 'PASS':
                wait('USER_FEEDBACK_REVIEW_PENDING', item_name + ': criterion status is not PASS')
            text(item.get('evidence'), item_name + '/evidence')
        if covered != expected:
            fail('USER_FEEDBACK_CRITERIA', request_id + ': every criterion must be checked')
    if checked != set(active):
        fail('USER_FEEDBACK_COVERAGE', 'Every active request must appear exactly once')
    summary['checked_request_ids'] = sorted(checked)
    return result()
