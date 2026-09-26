"""Read-only, role-specific review inputs. Packets are never FINAL or approval.

The complete manuscript remains authoritative. A partial packet does not reuse,
aggregate, or certify earlier reviews. A fresh blind solver must not have seen
the author key, comparison packet, learning manuscript, or prior answer diff.
"""
import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import re

from book_plan import content_hash, passage_elements, question_elements
from check_book import check as check_book
from check_learning_content import check as check_learning


ROLES = ('learning', 'questions-blind', 'questions-compare')
ROOT = Path(__file__).resolve().parent.parent
COMMON_RULES = ('SKILL.md', 'references/editorial-core.md',
                'references/workflow.md', 'references/layout-rules.md',
                'references/runtime-and-data.md', 'references/handoff-format.md',
                'references/common-errors.md', 'references/current-revision.md',
                'references/manuscript-data.md', 'references/verification.md',
                'references/review-efficiency.md')
LEARNING_RULES = ('references/analysis-content.md', 'references/gloss-rules.md',
                  'references/grammar-labels.md', 'references/preposition-meanings.md',
                  'references/proper-nouns.md')
QUESTION_RULES = ('references/workbook.md', 'references/assessment-content.md')


def canonical_sha256(value):
    """All JSON fields, including layout adjustments; not an input-file hash."""
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True,
                     separators=(',', ':'), allow_nan=False).encode('utf-8')
    return hashlib.sha256(raw).hexdigest()


def _digests(data):
    return {'content_sha256': content_hash(data),
            'canonical_full_json_sha256': canonical_sha256(data),
            'file_sha256': None,
            'file_sha256_status': 'UNAVAILABLE_FOR_IN_MEMORY_INPUT'}


def _index(rows, label, *, sentence=False):
    result = {}
    if not isinstance(rows, list):
        raise ValueError(label + ' must be a list')
    for row in rows:
        if not isinstance(row, dict) or not isinstance(row.get('id'), str):
            raise ValueError(label + ' needs string record IDs')
        key = (row.get('source_id'), row['id']) if sentence else row['id']
        if key in result:
            raise ValueError(label + ' contains duplicate IDs')
        result[key] = row
    return result


def _diff(before, after, path=()):
    """Compare every field without relying on author-provided change notes."""
    if type(before) is not type(after):
        return [{'path': path, 'operation': 'replace', 'before': before, 'after': after}]
    if isinstance(before, dict):
        rows = []
        for key in sorted(set(before) | set(after)):
            if key not in before:
                rows.append({'path': path + (key,), 'operation': 'add', 'after': after[key]})
            elif key not in after:
                rows.append({'path': path + (key,), 'operation': 'remove', 'before': before[key]})
            else:
                rows.extend(_diff(before[key], after[key], path + (key,)))
        return rows
    if isinstance(before, list):
        rows = []
        for i in range(max(len(before), len(after))):
            if i >= len(before):
                rows.append({'path': path + (i,), 'operation': 'add', 'after': after[i]})
            elif i >= len(after):
                rows.append({'path': path + (i,), 'operation': 'remove', 'before': before[i]})
            else:
                rows.extend(_diff(before[i], after[i], path + (i,)))
        return rows
    if before != after:
        return [{'path': path, 'operation': 'replace', 'before': before, 'after': after}]
    return []


# Only these well-understood leaf changes may receive a local impact scope.
# New fields, container replacements, additions/removals, and membership changes
# deliberately fall back to a whole stage instead of guessing their meaning.
UNIT_LOCAL = (
    r'hook', r'today_words/\d+/(text|meaning_ko|source_gloss_id)',
    r'analysis/(heading_kind|title_or_topic_en|title_or_topic_ko|intent_ko)',
    r'analysis/flow/\d+/(text_ko|label)',
    r'analysis/easy_explanations/\d+/explanatory_sentences/\d+',
    r'analysis/grammar_points/\d+/(title|explanation|span/\d+|sentence_id)',
    r'analysis/grammar_points/\d+/(id|formula_key|practice/(answer_ko|span/\d+|support_gloss_ids/\d+|formula_support/(en|ko)))',
    r'analysis/grammar_points/\d+/practice/support_overrides/\d+/(gloss_id|form|meaning_ko|review_record|source_span/\d+)',
    r'analysis/grammar_points/\d+/supplemental/(function_gloss_id|reason)',
    r'analysis/formula_routes/\d+/(sentence_id|function_gloss_id|formula_key|route|hint_index|grammar_point_id|review_record|exception_kind|replacement_grammar_point_id|approval_reference|partial_negation_span/\d+)',
    r'analysis/relations/\d+/(head|synonym|antonym)/(text|meaning_ko)',
    r'workbook/(relation_order|key_sentence_ids)/\d+',
    r'workbook/syntax_point_ids/\d+',
)
SENTENCE_LOCAL = (
    r'(key|natural_ko)', r'chunks/\d+/(start|end|ko)',
    r'glosses/\d+/(headword|meaning_ko|referent_ko|star|kind|today_word_id)',
    r'glosses/\d+/(spans/\d+/\d+|combines_with/\d+)',
    r'hints/\d+/(meaning_ko|explanation|structure_label|category|display_mode|omitted_relative|emphasis_policy)',
    r'hints/\d+/(span/\d+|display_span/\d+|display_spans/\d+/\d+|gloss_ids/\d+)',
    r'hints/\d+/display_pairs/\d+/(en|ko|emphasis_note)',
    r'hints/\d+/display_pairs/\d+/emphasis_links/\d+/(en_spans|ko_spans)/\d+/\d+',
    r'clauses/\d+/(kind|start|marker|subject_spans/\d+/\d+|verb_spans/\d+/\d+)',
    r'clauses/\d+/(subject_display_spans/\d+/\d+|subject_display_review)',
    r'clauses/\d+/contraction_readings/\d+/(expanded|span/\d+)',
    r'lexical_coverage/\d+/(gloss_id|exemption|reason|level|first_gloss_id|span/\d+)',
    r'reading_checks/(review_record|(function_gloss_ids|relative_gloss_ids)/\d+)',
    r'reading_checks/(required_breaks|protected_spans)/\d+/(at|kind|reason|gloss_id|span/\d+)',
)
QUESTION_LOCAL = (
    r'(question|type|choice_mode|passage|given|target|summary|answer)',
    r'choices/\d+/(number|text)', r'prompt_underlines/\d+/\d+',
    r'blocks/(A|B|C)', r'permutations/\d+/\d+',
    r'learned_relation_uses/\d+/(term_id|choice_number|surface|reason_ko|choice_span/\d+)',
)
REQUEST_LOCAL = (
    r'(type|first_sentence|last_sentence|replacement|given_sentence|addition_offset|addition)',
    r'(target_span|replacement_span|insertion_slots|sentence_marks)/\d+',
    r'vocabulary_marks/\d+/\d+', r'block_spans/(given|A|B|C)/\d+',
    r'length_review/(profile_id|grade|rationale|independent_review_required|benchmark_ids/\d+)',
)
KEY_LOCAL = (r'answer', r'(evidence|explanation)',
             r'(choices|choices_ko|wrong_reasons)/\d+/(number|text)')


def _local(path, patterns):
    value = '/'.join(str(x) for x in path)
    return any(re.fullmatch(pattern, value) for pattern in patterns)


def _linked_questions(data, unit_ids):
    """Return every verified overlapping or explicitly linked question.

    An unverifiable dependency broadens to every current question. The passage
    range alone is insufficient for workbook items whose studied words come
    from a different unit, so both relationships are included.
    """
    units = _index(data['units'], 'units')
    questions = _index(data.get('assessment', {}).get('questions', []), 'questions')
    if not unit_ids:
        return set()
    try:
        sources = _index(data['sources'], 'sources')
        requests = _index(data['question_sources'], 'question_sources')
        plans = _index(data['assessment']['plan'], 'plan')
        if set(requests) != set(questions) or set(plans) != set(questions):
            return set(questions)
        unit_sentences = {(units[uid]['source_id'], sid)
                          for uid in unit_ids for sid in units[uid]['sentence_ids']}
        linked = {units[uid]['workbook']['question_id'] for uid in unit_ids}
        for qid in questions:
            req = requests[qid]
            src = req['source_id']
            ids = [s['id'] for s in sources[src]['sentences']]
            first, last = ids.index(req['first_sentence']), ids.index(req['last_sentence'])
            if first > last:
                return set(questions)
            if plans[qid].get('unit_id') in unit_ids or any(
                    (src, sid) in unit_sentences for sid in ids[first:last + 1]):
                linked.add(qid)
        if not linked <= set(questions):
            return set(questions)
        return linked
    except (KeyError, TypeError, ValueError):
        return set(questions)


def _expand_groups(data, selected):
    expanded = set(selected)
    groups = data.get('assessment', {}).get('passage_groups', [])
    while True:
        previous = set(expanded)
        for group in groups:
            if expanded.intersection(group['question_ids']):
                expanded.update(group['question_ids'])
        if expanded == previous:
            return expanded


def _impact(data, baseline, changes):
    all_units = {u['id'] for u in data['units']}
    all_questions = {q['id'] for q in data.get('assessment', {}).get('questions', [])}
    units, questions, reasons = set(), set(), []
    full_learning = full_questions = False
    for change in changes:
        path = change['path']
        try:
            if path[0] in {'units', 'sentences'}:
                collection = path[0]
                before = baseline[collection][path[1]]
                after = data[collection][path[1]]
                same = (before['id'], before.get('source_id')) == (after['id'], after.get('source_id'))
                patterns = UNIT_LOCAL if collection == 'units' else SENTENCE_LOCAL
                if not same or change['operation'] != 'replace' or not _local(path[2:], patterns):
                    full_learning = full_questions = True
                    reasons.append('Learning membership or unclassified field changed')
                elif collection == 'units':
                    units.add(after['id'])
                else:
                    found = {u['id'] for u in data['units'] if u['source_id'] == after['source_id']
                             and after['id'] in u['sentence_ids']}
                    if not found:
                        full_learning = full_questions = True
                    units.update(found)
            elif path[0] == 'question_sources' or (path[0] == 'assessment' and len(path) > 2
                    and path[1] in {'questions', 'quick_key', 'explanations'}):
                offset = 1 if path[0] == 'question_sources' else 2
                section = 'question_sources' if offset == 1 else path[1]
                old_rows = baseline[section] if offset == 1 else baseline['assessment'][section]
                new_rows = data[section] if offset == 1 else data['assessment'][section]
                old, new = old_rows[path[offset]], new_rows[path[offset]]
                patterns = REQUEST_LOCAL if offset == 1 else QUESTION_LOCAL if section == 'questions' else KEY_LOCAL
                if old['id'] != new['id'] or change['operation'] != 'replace' or not _local(path[offset + 1:], patterns):
                    full_questions = True
                    reasons.append('Question membership or unclassified field changed')
                else:
                    questions.add(new['id'])
            elif path[0] == 'assessment':
                full_questions = True
                reasons.append('Assessment plan, shared group, scope, or unclassified field changed')
            else:
                full_learning = full_questions = True
                reasons.append('Source, metadata, rule, or unclassified global field changed')
        except (KeyError, IndexError, TypeError):
            full_learning = full_questions = True
            reasons.append('Dependency could not be proven')
    if full_learning:
        units = all_units
    questions.update(_linked_questions(data, units))
    if full_questions:
        questions = all_questions
    return units, _expand_groups(data, questions), {
        'full_learning_fallback': full_learning, 'full_questions_fallback': full_questions,
        'reasons': sorted(set(reasons)), 'method': 'COMPLETE_RECURSIVE_JSON_COMPARISON'}


def _select(requested, known, name):
    if requested is None:
        return set()
    if isinstance(requested, (str, bytes)):
        raise ValueError(name + ' must be an iterable of IDs, not a string')
    values = set(requested)
    unknown = values - set(known)
    if unknown:
        raise ValueError('Unknown ' + name + ': ' + ', '.join(sorted(unknown)))
    return values


def _student_blocks(elements):
    # Whitelist only displayed text and actual underline spans, never raw view
    # fields such as original, answer, correct_order, replacement, or offsets.
    return [{'text': ''.join(run['text'] for run in element['runs']),
             'underlines': deepcopy(element.get('required_underlines', []))}
            for element in elements]


def _student_data(data, result, selected):
    questions = _index(data['assessment']['questions'], 'questions')
    rows = []
    for plan in data['assessment']['plan']:
        qid = plan['id']
        if qid not in selected:
            continue
        q = questions[qid]
        row = {'id': qid, 'set_id': q['set_id'], 'number': q['number']}
        if q.get('passage_group_id'):
            row['passage_group_id'] = q['passage_group_id']
        row['student_blocks'] = _student_blocks(question_elements(
            q, result['question_views'][qid], '',
            scope='workbook' if q['set_id'] == 'workbook' else 'mock',
            include_passage=not bool(q.get('passage_group_id'))))
        rows.append(row)
    groups = []
    for group in data['assessment'].get('passage_groups', []):
        if selected.intersection(group['question_ids']):
            groups.append({'id': group['id'], 'question_ids': list(group['question_ids']),
                           'student_blocks': _student_blocks(passage_elements(
                               result['passage_group_views'][group['id']], 'mock_question_passage'))})
    return {'questions': rows, 'passage_groups': groups}


def _sentence_refs(units):
    return [{'source_id': u['source_id'], 'sentence_id': sid} for u in units for sid in u['sentence_ids']]


def _learning_data(data, selected):
    units = data['units']
    chosen = [u for u in units if u['id'] in selected]
    neighbors = set()
    for index, unit in enumerate(units):
        if unit['id'] in selected:
            for adjacent in (index - 1, index + 1):
                if 0 <= adjacent < len(units) and units[adjacent]['source_id'] == unit['source_id']:
                    neighbors.add(units[adjacent]['id'])
    neighbors -= selected
    context_units = [u for u in units if u['id'] in neighbors]
    def sentences(rows):
        keys = {(u['source_id'], sid) for u in rows for sid in u['sentence_ids']}
        return [s for s in data['sentences'] if (s['source_id'], s['id']) in keys]
    sources = {u['source_id'] for u in chosen}
    payload = {'metadata': data['metadata'], 'units': chosen, 'sentences': sentences(chosen)}
    context = {'sources': [s for s in data['sources'] if s['id'] in sources],
               'paragraphs': [p for p in data.get('paragraphs', []) if p['source_id'] in sources],
               'grouping_resolutions': [r for r in data.get('grouping_resolutions', [])
                                         if r.get('source_id') in sources],
               'units': context_units, 'sentences': sentences(context_units)}
    return deepcopy(payload), deepcopy(context), {
        'source_ids': [s['id'] for s in context['sources']],
        'unit_ids': [u['id'] for u in context_units], 'sentence_refs': _sentence_refs(context_units)}


def _change_inventory(changes, data, baseline, selected, role):
    rows = []
    for change in changes:
        path = change['path']
        row = {'path': '/' + '/'.join(str(x).replace('~', '~0').replace('/', '~1') for x in path),
               'operation': change['operation']}
        include_values = role == 'learning' and path and path[0] in {'units', 'sentences'}
        if role == 'questions-compare' and len(path) > 2 and path[0] == 'assessment' \
                and path[1] in {'questions', 'quick_key', 'explanations'}:
            for manuscript in (data, baseline):
                try:
                    include_values |= manuscript['assessment'][path[1]][path[2]]['id'] in selected
                except (KeyError, IndexError, TypeError):
                    pass
        for side in ('before', 'after'):
            if side in change:
                row[side + '_canonical_sha256'] = canonical_sha256(change[side])
                if include_values:
                    row[side] = deepcopy(change[side])
        rows.append(row)
    return rows


def make_packet(data, role, *, unit_ids=None, question_ids=None, baseline=None, changed_only=False):
    """Return a detached packet; never change the manuscript or review records.

    Selectors add explicit assignments. In changed-only mode they cannot remove
    any machine-detected impact. An equal baseline yields an empty assignment,
    still NOT_FINAL/NOT_CERTIFIED. Current structure must pass the existing gate.
    """
    if role not in ROLES:
        raise ValueError('Unknown review role: ' + str(role))
    if changed_only and baseline is None:
        raise ValueError('changed_only requires an actual baseline manuscript')
    if role == 'learning' and question_ids is not None:
        raise ValueError('Learning packets select complete units, not question IDs')
    current = deepcopy(data)
    previous = deepcopy(baseline)
    units = _index(current['units'], 'units')
    questions = _index(current.get('assessment', {}).get('questions', []), 'questions')
    chosen_units = _select(unit_ids, units, 'unit IDs')
    chosen_questions = _select(question_ids, questions, 'question IDs')
    result = check_learning(current, scope='learning') if role == 'learning' else check_book(current)
    if result['status'] != 'STRUCTURE_PASS':
        raise ValueError('Current manuscript must pass existing structure checks before packet export')
    changes = _diff(previous, current) if previous is not None else []
    impact = None
    if previous is not None:
        impacted_units, impacted_questions, impact = _impact(current, previous, changes)
        if changed_only:
            chosen_units.update(impacted_units)
            chosen_questions.update(impacted_questions)
    if not changed_only and unit_ids is None and question_ids is None:
        if role == 'learning':
            chosen_units = set(units)
        else:
            chosen_questions = set(questions)
    if role != 'learning':
        chosen_questions.update(_linked_questions(current, chosen_units))
        chosen_questions = _expand_groups(current, chosen_questions)
    ordered_units = [uid for uid in units if uid in chosen_units]
    ordered_questions = [p['id'] for p in current.get('assessment', {}).get('plan', [])
                         if p['id'] in chosen_questions]
    rule_paths = COMMON_RULES + (LEARNING_RULES if role == 'learning' else QUESTION_RULES)
    packet = {
        'schema_version': 1, 'purpose': 'REVIEW_INPUT_PACKET_NOT_FINAL',
        'status': 'NOT_FINAL', 'certification': 'NOT_CERTIFIED', 'role': role,
        'input_digest': _digests(current),
        'current_rules': [{'path': path, 'sha256': hashlib.sha256((ROOT / path).read_bytes()).hexdigest()}
                          for path in rule_paths],
        'review_contract': {
            'independent_review': 'NOT_PERFORMED', 'approval_reuse': 'NOT_IMPLEMENTED',
            'complete_final_required': True, 'existing_release_gate_unchanged': True,
            'required_independent_question_solvers': 2,
            'context_is_not_assigned_or_reviewed': True,
            'unresolved_items': 'CONSULT_CURRENT_HANDOFF_SEPARATELY; NOT_CLEARED_BY_PACKET'},
    }
    if role == 'learning':
        selected_data, context, context_scope = _learning_data(current, chosen_units)
        packet['scope'] = {'assigned': {'unit_ids': ordered_units,
                            'sentence_refs': _sentence_refs([units[x] for x in ordered_units])},
                           'context_only': context_scope,
                           'whole_stage_assigned': set(ordered_units) == set(units),
                           'cross_unit_consistency_review': 'NOT_PERFORMED'}
        packet['selected_data'], packet['context'] = selected_data, context
    else:
        packet['scope'] = {'assigned': {'question_ids': ordered_questions},
                           'context_only': {'question_ids': []},
                           'whole_stage_assigned': chosen_questions == set(questions)}
        packet['selected_data'] = _student_data(current, result, chosen_questions)
        if role == 'questions-blind':
            packet['review_contract']['unresolved_items'] = (
                'COORDINATOR_MUST_SUPPLY_BLIND_SAFE_ITEMS; NOT_CLEARED_BY_PACKET')
            packet['review_contract']['blind_use'] = (
                'Fresh independent solver only. Store own answers and reasoning before opening '
                'comparison, source, learning material, or author feedback. Removing answers '
                'does not restore blindness for a solver who already saw them.')
        else:
            packet['review_contract']['comparison_use'] = 'OPEN_ONLY_AFTER_INDEPENDENT_ANSWERS_ARE_SAVED'
            packet['comparison'] = {
                name: deepcopy([r for r in current['assessment'].get(name, []) if r['id'] in chosen_questions])
                for name in ('questions', 'quick_key', 'explanations')}
            packet['comparison']['source_excerpts'] = [
                {'question_id': qid, 'original': result['question_views'][qid]['original'],
                 'source_id': result['question_views'][qid]['source_id'],
                 'source_sentence_ids': result['question_views'][qid]['source_sentence_ids']}
                for qid in ordered_questions]
            source_requests = _index(current['question_sources'], 'question_sources')
            packet['comparison']['length_reviews'] = [
                {'question_id': qid, 'length_review': deepcopy(source_requests[qid]['length_review']),
                 'length_comparison': deepcopy(result['question_views'][qid]['length_comparison'])}
                for qid in ordered_questions]
    # Even paths/reasons may reveal a changed answer or transformation to a blind
    # solver. The baseline and all impact information therefore stay out entirely.
    if role != 'questions-blind' and previous is not None:
        packet['baseline_digest'] = _digests(previous)
        packet['change_scope'] = dict(impact, changed_only=bool(changed_only),
                                     affected_unit_ids=[u for u in units if u in impacted_units],
                                     affected_question_ids=[q for q in questions if q in impacted_questions])
        packet['changes'] = _change_inventory(changes, current, previous, chosen_questions, role)
    return packet


def save_packet(path, packet):
    """Exclusive create only; existing FINAL, handoff, or packet is untouched."""
    path = Path(path)
    raw = (json.dumps(packet, ensure_ascii=False, indent=2, allow_nan=False) + '\n').encode('utf-8')
    with path.open('xb') as handle:
        handle.write(raw)
    if path.read_bytes() != raw:
        raise ValueError('Saved review packet differs from generated packet')
    return hashlib.sha256(raw).hexdigest()


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    parser.add_argument('output', type=Path)
    parser.add_argument('--role', required=True, choices=ROLES)
    parser.add_argument('--unit-id', action='append', dest='unit_ids')
    parser.add_argument('--question-id', action='append', dest='question_ids')
    parser.add_argument('--baseline', type=Path)
    parser.add_argument('--changed-only', action='store_true')
    args = parser.parse_args(argv)
    if args.output.exists() or args.output.resolve() in {
            args.input.resolve(), args.baseline.resolve() if args.baseline else args.input.resolve()}:
        raise ValueError('Review packet requires a new output path; no existing file may be overwritten')
    raw = args.input.read_bytes()
    baseline_raw = args.baseline.read_bytes() if args.baseline else None
    packet = make_packet(json.loads(raw.decode('utf-8-sig')), args.role,
                         unit_ids=args.unit_ids, question_ids=args.question_ids,
                         baseline=json.loads(baseline_raw.decode('utf-8-sig')) if baseline_raw is not None else None,
                         changed_only=args.changed_only)
    packet['input_digest'].update(file_sha256=hashlib.sha256(raw).hexdigest(), file_sha256_status='EXACT_INPUT_BYTES')
    if baseline_raw is not None and args.role != 'questions-blind':
        packet['baseline_digest'].update(file_sha256=hashlib.sha256(baseline_raw).hexdigest(),
                                         file_sha256_status='EXACT_INPUT_BYTES')
    digest = save_packet(args.output, packet)
    print(json.dumps({'status': 'REVIEW_PACKET_EXPORTED_NOT_FINAL', 'certification': 'NOT_CERTIFIED',
                      'role': args.role, 'output_sha256': digest}, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
