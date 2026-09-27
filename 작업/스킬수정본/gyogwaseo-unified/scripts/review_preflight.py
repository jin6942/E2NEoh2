"""Read-only, compact manuscript diagnostics; always NOT_CERTIFIED.

Runs the existing complete-book structural check by default. Explicit learning
scope checks only the learning manuscript, without workbook or assessment gates.
Additional warnings identify review candidates, never semantic approvals.
Full S/L/M/N/J/K/R review, saved-artifact checks and release gates still apply.
"""
import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import re

from check_book import check as check_book
from check_learning_content import check as check_learning
from check_answer_links import SYMBOL_TYPES
from question_source import build_view, excerpt
from structure_hints import display_pairs


WORDS = re.compile(r"[A-Za-z]+(?:[’'-][A-Za-z]+)*|\d+(?:[.,]\d+)*")
MARKERS = re.compile(r'\(\s*([AB])\s*\)')
SNIPPET_LIMIT = 180
SHAPE_ERRORS = (ValueError, TypeError, KeyError, AttributeError, IndexError)


def _rows(value):
    return [row for row in value if isinstance(row, dict)] if isinstance(value, list) else []


def _object(value):
    return value if isinstance(value, dict) else {}


def _snippet(value):
    value = re.sub(r'\s+', ' ', str(value)).strip()
    return value if len(value) <= SNIPPET_LIMIT else value[:SNIPPET_LIMIT - 1] + '…'


def _identity(row, index):
    return _snippet(row.get('id', f'@index:{index}'))


def _sentence_count(value):
    """Conservative punctuation candidates, not a Korean grammar judgment.

    Decimal points, ellipses, initials and common English abbreviations are not
    treated as sentence endings. Unpunctuated trailing text counts as one part.
    Reviewers still decide whether quoted text is a separate explanation.
    """
    if not isinstance(value, str) or not value.strip():
        return 0
    protected = list(value)
    for pattern in (r'(?<=\d)\.(?=\d)', r'\.{2,}',
                    r'\b(?:[A-Za-z]\.){2,}',
                    r'\b(?:Mr|Mrs|Ms|Dr|Prof|Sr|Jr|vs|etc)\.',
                    r'\b[A-Z]\.(?=\s+[A-Z][a-z])'):
        for match in re.finditer(pattern, value, re.IGNORECASE if 'Mr|' in pattern else 0):
            for index in range(match.start(), match.end()):
                if protected[index] == '.':
                    protected[index] = '·'
    # Require whitespace/end after final punctuation (and any closing quotes).
    parts = re.split(r'''[.!?。！？]+["'”’»\)\]]*(?:\s+|$)''', ''.join(protected))
    return sum(bool(re.search(r'[A-Za-z0-9가-힣]', part)) for part in parts)


def _compact_book(data, diagnostics, *, scope='full'):
    checker = 'check_learning_content' if scope == 'learning' else 'check_book'
    prefix = 'CHECK_LEARNING' if scope == 'learning' else 'CHECK_BOOK'
    try:
        if scope == 'learning':
            learning = check_learning(data, scope='learning')
            result = {'status': learning['status'], 'learning': learning}
        else:
            result = check_book(data)
    except SHAPE_ERRORS as exc:
        error = {'code': prefix + '_EXCEPTION', 'location': checker,
                 'message': _snippet(exc), 'exception_type': type(exc).__name__}
        diagnostics.append(dict(error, severity='ERROR'))
        return {'status': 'FAIL', 'errors': [error]}
    compact = {'status': result.get('status', 'FAIL'), 'errors': []}
    for name in ('learning', 'assessment'):
        child = _object(result.get(name))
        if not child:
            continue
        compact[name] = {key: child[key] for key in
                         ('status', 'source_count', 'unit_count', 'sentence_count',
                          'gloss_count', 'checked_question_count') if key in child}
        grouping = _object(child.get('grouping'))
        if grouping:
            compact[name]['grouping_status'] = grouping.get('status')
        for issue in _rows(child.get('errors')) + _rows(child.get('source_issues')):
            error = {'code': _snippet(issue.get('code', prefix + '_ISSUE')),
                     'location': _snippet(issue.get('location', name)),
                     'message': _snippet(issue.get('message', issue.get('reason', 'Existing check requires review.')))}
            for key in ('source_id', 'sentence_id', 'unit_id', 'question_id'):
                if key in issue:
                    error[key] = _snippet(issue[key])
            compact['errors'].append(error)
            diagnostics.append(dict(error, severity='ERROR', origin=checker))
    if compact['status'] != 'STRUCTURE_PASS' and not compact['errors']:
        label = 'learning-content' if scope == 'learning' else 'complete-book'
        error = {'code': prefix + '_INCOMPLETE', 'location': checker,
                 'message': 'Existing ' + label + ' check: ' + _snippet(compact['status'])}
        compact['errors'].append(error)
        diagnostics.append(dict(error, severity='ERROR', origin=checker))
    if 'checked_question_count' in result:
        compact['checked_question_count'] = result['checked_question_count']
    return compact


def _learning_diagnostics(data, emit):
    formula_count = 0
    for index, unit in enumerate(_rows(data.get('units'))):
        uid = _identity(unit, index)
        for n, easy in enumerate(_rows(_object(unit.get('analysis')).get('easy_explanations'))):
            lines = easy.get('explanatory_sentences')
            if not isinstance(lines, list) or any(not isinstance(line, str) for line in lines):
                continue  # Existing check owns malformed fields and empty explanations.
            counts = [_sentence_count(line) for line in lines]
            multiple = [i + 1 for i, count in enumerate(counts) if count > 1]
            if multiple:
                emit('WARNING', 'EASY_EXPLANATION_SENTENCE_COUNT',
                     f'units/{uid}/analysis/easy_explanations/{n}',
                     'An explanation array item may contain multiple sentences; review sentence separation and one idea per sentence. Total sentence count is unrestricted.',
                     unit_id=uid, sentence_id=_snippet(easy.get('sentence_id', '')),
                     sentence_count_candidate=sum(counts), multiple_sentence_elements=multiple,
                     snippet=_snippet(' '.join(lines)))
    for index, sentence in enumerate(_rows(data.get('sentences'))):
        original = sentence.get('text')
        if not isinstance(original, str):
            continue
        count = len(WORDS.findall(original))
        sid = _identity(sentence, index)
        for n, hint in enumerate(_rows(sentence.get('hints'))):
            try:
                pairs = display_pairs(hint)
            except SHAPE_ERRORS:
                continue  # Do not invent a display from an invalid/internal span.
            if hint.get('category') == 'function-combination' and hint.get('display_mode') != 'modal-perfect-verb':
                formula_count += 1
                continue
            displayed = ' / '.join(pair['en'] for pair in pairs)
            shown = len(WORDS.findall(displayed))
            if count >= 15 and shown * 5 >= count * 4:
                emit('WARNING', 'HINT_DISPLAY_LENGTH', f'sentences/{sid}/hints/{n}',
                     'Review actual English display for one grammar focus; retain justified S′/V′ and be-complement exceptions.',
                     source_id=_snippet(sentence.get('source_id', '')), sentence_id=sid,
                     hint_index=n, original_word_count=count, displayed_word_count=shown,
                     displayed_ratio=round(shown / count, 4), snippet=_snippet(displayed))
    return formula_count


def _overlap(q, qid, passage, passage_location, emit):
    if not isinstance(q.get('type'), str) or q['type'] in SYMBOL_TYPES | {'순서'} or q.get('choice_mode') != 'text' or not isinstance(passage, str):
        return
    source_tokens = list(WORDS.finditer(passage))
    windows = defaultdict(list)
    for i in range(len(source_tokens) - 4):
        windows[tuple(token.group().casefold() for token in source_tokens[i:i + 5])].append(i)
    for choice in _rows(q.get('choices')):
        value = choice.get('text')
        if not isinstance(value, str):
            continue
        tokens = list(WORDS.finditer(value))
        examples, match_count = [], 0
        for i in range(len(tokens) - 4):
            found = windows.get(tuple(token.group().casefold() for token in tokens[i:i + 5]), [])
            match_count += len(found)
            for j in found[:max(0, 3 - len(examples))]:
                a, b = source_tokens[j].start(), source_tokens[j + 4].end()
                examples.append({'choice_span': [tokens[i].start(), tokens[i + 4].end()],
                                 'passage_span': [a, b], 'phrase': _snippet(passage[a:b]),
                                 'context': _snippet(passage[max(0, a - 35):b + 35])})
        if match_count:
            emit('WARNING', 'CHOICE_PASSAGE_OVERLAP', f'assessment/questions/{qid}/choices/{choice.get("number")}',
                 'Review matching wording in context; proper names, necessary terms and justified repetition may remain.',
                 question_id=qid, choice_number=choice.get('number'), passage_location=passage_location,
                 five_word_match_count=match_count, examples=examples)


def _irrelevant(data, q, qid, emit):
    if q.get('type') != '무관한 문장':
        return
    requests = [row for row in _rows(data.get('question_sources')) if row.get('id') == q.get('id')]
    if len(requests) != 1:
        return
    request = requests[0]
    sources = [row for row in _rows(data.get('sources')) if row.get('id') == request.get('source_id')]
    if len(sources) != 1:
        return
    try:
        view = build_view(sources[0], request)
        if view.get('passage') != q.get('passage'):
            return  # Warning must describe the actual student text.
        original, sentences, unused_span = excerpt(sources[0], request)
        ordered = [(row['start'], 1, row['id']) for row in sentences]
        ordered.append((request['addition_offset'], 0, '@added'))
        ids = [row[2] for row in sorted(ordered)]
        marks = request['sentence_marks']
        positions = [ids.index(mark) for mark in marks]
        gaps = [ids[left + 1:right] for left, right in zip(positions, positions[1:]) if right > left + 1]
    except SHAPE_ERRORS:
        return
    if gaps:
        emit('WARNING', 'IRRELEVANT_TARGETS_NONADJACENT', f'question_sources/{qid}/sentence_marks',
             'Unnumbered sentences occur between targets; adjacency is a review candidate, not a new mandatory rule.',
             question_id=qid, source_id=_snippet(request.get('source_id', '')),
             target_sentence_ids=[_snippet(value) for value in marks],
             intervening_sentence_ids=[_snippet(value) for gap in gaps for value in gap],
             snippet=_snippet(view['passage']))


def check(data, *, scope='full'):
    """Return deterministic compact diagnostics without mutating the manuscript."""
    if scope not in {'full', 'learning'}:
        raise ValueError('Unknown preflight scope')
    diagnostics = []
    existing = _compact_book(data, diagnostics, scope=scope)
    if scope == 'learning':
        # Keep the established envelope for callers, but never present its
        # child status as a complete-book check or release certificate.
        existing['scope'] = 'learning'
    data = _object(data)

    def emit(severity, code, location, message, **details):
        diagnostics.append(dict(severity=severity, code=code, location=location,
                                message=message, **details))

    formula_count = _learning_diagnostics(data, emit)
    assessment = _object(data.get('assessment')) if scope == 'full' else {}
    questions = _rows(assessment.get('questions'))
    # Shared long-reading items display their group's owner passage, including
    # the owner's vocabulary alteration, not a hidden normal-source projection.
    qmap = {row['id']: row for row in questions if isinstance(row.get('id'), str)}
    owners = {row['id']: row.get('passage_question_id') for row in _rows(assessment.get('passage_groups'))
              if isinstance(row.get('id'), str) and isinstance(row.get('passage_question_id'), str)}
    sets = {}
    for index, q in enumerate(questions):
        qid = _identity(q, index)
        set_id = _snippet(q.get('set_id', '@missing'))
        stats = sets.setdefault(set_id, {'question_count': 0, 'counts': {str(n): 0 for n in range(1, 6)}, 'invalid_answer_count': 0})
        stats['question_count'] += 1
        answer = q.get('answer')
        if type(answer) is int and 1 <= answer <= 5:
            stats['counts'][str(answer)] += 1
        else:
            stats['invalid_answer_count'] += 1
        if q.get('type') == '요약':
            summary = q.get('summary')
            markers = MARKERS.findall(summary) if isinstance(summary, str) else []
            if markers != ['A', 'B']:
                emit('ERROR', 'SUMMARY_AB_MARKERS', f'assessment/questions/{qid}/summary',
                     'The displayed summary requires exactly one (A), then exactly one (B).',
                     question_id=qid, markers=markers, snippet=_snippet(summary))
        group_id = q.get('passage_group_id')
        owner_id = owners.get(group_id) if isinstance(group_id, str) else None
        owner = qmap.get(owner_id, q)
        _overlap(q, qid, owner.get('passage'), f'assessment/questions/{_identity(owner, index)}/passage', emit)
        _irrelevant(data, q, qid, emit)
    for set_id, stats in sets.items():
        emit('INFO', 'SET_ANSWER_DISTRIBUTION', f'assessment/sets/{set_id}',
             'Distribution only; no once-per-number requirement is imposed.', set_id=set_id, **stats)
    counts = Counter(row['severity'] for row in diagnostics)
    result = {'status': 'NOT_CERTIFIED', 'check_book': existing,
            'diagnostic_counts': {level: counts[level] for level in ('ERROR', 'WARNING', 'INFO')},
            'diagnostics': diagnostics,
            'thresholds': {'hint_min_original_words': 15, 'hint_display_ratio': 0.8, 'choice_contiguous_words': 5},
            'formula_hints_excluded_from_ratio': formula_count,
            'semantic_review': 'NOT_PERFORMED', 'independent_reviews': 'NOT_PERFORMED',
            'saved_artifact_checks': 'NOT_PERFORMED', 'visual_review': 'NOT_PERFORMED',
            'limitations': [
                'Sentence counts are punctuation candidates; quoted speech and ambiguous boundaries require L review.',
                'Overlap compares case-folded English/number tokens in each displayed passage; it cannot judge answer leakage or justified repetition.',
                'Summary markers are structural only; choice/translation/explanation A/B meanings require L and M/N review.',
                'Grammar omissions, preposition grouping, meaning and correct-answer uniqueness require existing L/M/N review.',
                'No warning is an automatic edit, approval, or replacement for full final-artifact and release checks.']}
    if scope == 'learning':
        result['scope'] = 'learning'
        result['limitations'].append(
            'Learning scope excludes workbook and assessment checks; this report is not complete-book structure or release evidence.')
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path, help='Existing manuscript JSON (read-only)')
    parser.add_argument('output', type=Path, help='New compact diagnostic JSON; cannot replace any existing file')
    parser.add_argument('--scope', choices=['full', 'learning'], default='full',
                        help='full: complete book (default); learning: learning draft only, never release evidence')
    args = parser.parse_args(argv)
    if args.input.resolve() == args.output.resolve() or args.output.exists() or args.output.is_symlink():
        parser.error('Use a new report path; output cannot replace the manuscript or any existing file')
    raw = args.input.read_bytes()
    try:
        data = json.loads(raw.decode('utf-8-sig'))
        result = check(data) if args.scope == 'full' else check(data, scope=args.scope)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        result = {'status': 'NOT_CERTIFIED', 'check_book': {'status': 'FAIL'},
                  'diagnostic_counts': {'ERROR': 1, 'WARNING': 0, 'INFO': 0},
                  'diagnostics': [{'severity': 'ERROR', 'code': 'INPUT_JSON',
                                   'location': 'input', 'message': _snippet(exc)}]}
        if args.scope == 'learning':
            result['scope'] = 'learning'
            result['check_book']['scope'] = 'learning'
    result['input_sha256'] = hashlib.sha256(raw).hexdigest()
    report = (json.dumps(result, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
    # Exclusive creation also protects a file created after the initial check.
    with args.output.open('xb') as stream:
        stream.write(report)
    print(json.dumps({'status': result['status'], 'check_book_status': result['check_book']['status'],
                      'diagnostic_counts': result['diagnostic_counts'], 'output': str(args.output)}, ensure_ascii=False))
    return 0 if result['check_book']['status'] == 'STRUCTURE_PASS' and not result['diagnostic_counts']['ERROR'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
