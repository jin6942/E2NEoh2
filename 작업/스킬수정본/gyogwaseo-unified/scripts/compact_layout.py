"""Apply explicitly approved, Word-observed compact paragraph role profiles.

This module does not estimate pagination or invent smaller formatting. The
contract owns the approved derived roles; a manuscript decision selects one
profile for one unit's analysis commentary or workbook answer block.
"""
import hashlib
import json
import re


PROFILES = frozenset({'spacing', 'spacing_and_type'})
SHA256 = re.compile(r'[0-9a-fA-F]{64}\Z')


def content_hash(data):
    """Match book_plan.content_hash without importing the plan compiler."""
    value = {key: value for key, value in data.items() if key != 'layout_adjustments'}
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'))
    return hashlib.sha256(payload.encode('utf-8')).hexdigest()


def _nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def _approved_role_map(contract, profile):
    profiles = contract.get('compact_profiles', {})
    if profile not in PROFILES or not isinstance(profiles, dict) or profile not in profiles:
        raise ValueError('Compact adjustment requires an approved compact profile')
    definition = profiles[profile]
    role_map = definition.get('role_map') if isinstance(definition, dict) else None
    if not isinstance(role_map, dict) or not role_map:
        raise ValueError('Compact profile requires a nonempty role_map')
    derived = contract.get('derived_roles', {})
    base_roles = set(contract.get('roles', {})) | set(contract.get('additional_paragraph_roles', {}))
    for source, target in role_map.items():
        if not _nonempty(source) or not _nonempty(target) or source == target:
            raise ValueError('Compact role_map must select distinct named derived roles')
        target_definition = derived.get(target) if isinstance(derived, dict) else None
        if (source not in base_roles or not isinstance(target_definition, dict)
                or target_definition.get('base_role') != source):
            raise ValueError('Compact role_map must preserve each approved base role')
    return role_map


def apply_compact_adjustments(data, blocks, contract, current_content_hash=None):
    """Mutate only eligible paragraph ``role`` values, after validating all requests.

    Other layout adjustment kinds belong to their existing handlers. With no
    compact request this is a no-op, including for legacy contracts. Analysis
    starts after the final analysis_header so its earlier chunk translations
    stay untouched. Tables and all content, ordering and chaining are retained.
    The compiler may supply its canonical current_content_hash; the local
    equivalent is a fallback for independent callers. An invalid request raises
    ValueError before any compact mutation is applied.
    """
    adjustments = data.get('layout_adjustments', [])
    if not isinstance(adjustments, list):
        raise ValueError('layout_adjustments must be a list')
    requests = [row for row in adjustments
                if isinstance(row, dict) and row.get('kind') == 'compact_block']
    if not requests:
        return

    allowed = {unit['id'] + '/' + section
               for unit in data.get('units', []) for section in ('analysis', 'answers')}
    lookup = {}
    for block in blocks:
        lookup.setdefault(block['id'], []).append(block)
    revision = content_hash(data) if current_content_hash is None else current_content_hash
    if not isinstance(revision, str) or not SHA256.fullmatch(revision):
        raise ValueError('Compact adjustment requires a canonical manuscript SHA256')
    seen, changes = set(), []
    for request in requests:
        bid = request.get('block_id')
        if not isinstance(bid, str) or bid not in allowed:
            raise ValueError('Compact adjustment is limited to a known unit analysis or answers block')
        if len(lookup.get(bid, [])) != 1:
            raise ValueError('Compact adjustment requires one known block')
        if bid in seen:
            raise ValueError('Repeated compact adjustment for the same block')
        seen.add(bid)
        if request.get('content_sha256') != revision:
            raise ValueError('Compact decision belongs to a different manuscript revision')
        if (request.get('renderer') != 'Microsoft Word'
                or type(request.get('observed_page')) is not int
                or request['observed_page'] <= 0):
            raise ValueError('Compact adjustment needs an actual positive Word page observation')
        evidence = request.get('evidence_pdf_sha256')
        if not isinstance(evidence, str) or not SHA256.fullmatch(evidence):
            raise ValueError('Compact adjustment requires a PDF SHA256 observation')
        if not _nonempty(request.get('reason')) or not _nonempty(request.get('approval_reference')):
            raise ValueError('Compact adjustment requires a reason and explicit approval reference')
        profile = request.get('profile')
        if not isinstance(profile, str):
            raise ValueError('Compact adjustment requires an approved compact profile')
        role_map = _approved_role_map(contract, profile)
        elements = lookup[bid][0]['elements']
        start = 0
        if bid.endswith('/analysis'):
            headers = [index for index, element in enumerate(elements)
                       if element.get('role') == 'analysis_header'
                       and element.get('kind', 'paragraph') == 'paragraph']
            if not headers:
                raise ValueError('Compact analysis requires its commentary header boundary')
            start = headers[-1] + 1
        planned = [(element, role_map[element['role']]) for element in elements[start:]
                   if element.get('kind', 'paragraph') == 'paragraph'
                   and element.get('role') in role_map]
        if not planned:
            raise ValueError('Compact profile has no eligible paragraph role in the requested block')
        changes.extend(planned)

    for element, role in changes:
        element['role'] = role
