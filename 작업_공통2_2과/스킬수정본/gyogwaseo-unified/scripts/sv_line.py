"""Render reviewed clause records with the common S/V punctuation.

This helper does not parse English or infer clause boundaries. Input is one
verified original sentence and its reviewed clauses. Each clause has kind,
start (Unicode code-point offset), marker, subject_spans and verb_spans.
Spans are [start, end] with exclusive end. An omitted marker is metadata only.
subject_spans retains the complete reviewed subject. Optional
subject_display_spans plus subject_display_review selects one source-prefix
span for the printed basic noun phrase; this helper never infers that phrase.
For each 's/’s in verb_spans, contraction_readings contains
{span: [start,end], expanded: "is"|"has"}, reviewed in context.
Only has is appended to the source form for display; the source is unchanged.
An optional reviewed noun-phrase-answer record permits an explicitly empty
clause list and returns an empty string: consumers omit the whole S/V row.
The verbless-fragment kind (2026-09-28 user decision, 공통영어2 YBM(박) 2과:
“S/V 줄 빼기 + 스킬 사본 보완”) uses the same record and context contract for a
reviewed sentence with no finite verb that is not an answer (e.g. Lucky!).
This standalone helper checks the review record and original-text hash only;
the manuscript checker binds its context to the preceding source sentence.
"""
import argparse
import hashlib
import json
import re
from pathlib import Path


def extract_parts(original, spans, label):
    if not isinstance(spans, list):
        raise ValueError(f'{label} spans must be a list')
    parts, previous = [], -1
    for span in spans:
        if not isinstance(span, list) or len(span) != 2:
            raise ValueError(f'Invalid {label} span')
        start, end = span
        if type(start) is not int or type(end) is not int:
            raise ValueError('Span offsets must be integers')
        if not 0 <= start < end <= len(original) or start < previous:
            raise ValueError('Source spans overlap, reverse, or exceed the sentence')
        part = original[start:end]
        if not part.strip():
            raise ValueError('Empty source span')
        parts.append(part)
        previous = end
    return ' '.join(parts)


def render_subject(original, clause):
    """Render an explicitly reviewed prefix without changing subject evidence.

    Only source bounds and token boundaries are checked here. Whether the
    remainder is a postmodifier, rather than a necessary part of a clause,
    gerund, quantity/partitive expression or coordination, requires review.
    Existing records without the optional display fields remain unchanged.
    """
    full_spans = clause.get('subject_spans', [])
    full = extract_parts(original, full_spans, 'subject')
    has_display = 'subject_display_spans' in clause
    has_review = 'subject_display_review' in clause
    if not has_display and not has_review:
        return full
    if not has_display or not has_review:
        raise ValueError('Subject display needs both spans and subject_display_review')
    if clause.get('kind') == 'subject_relative':
        raise ValueError('Subject relative clause cannot add a displayed subject')
    review = clause['subject_display_review']
    if not isinstance(review, str) or not review.strip():
        raise ValueError('Subject display needs a nonempty subject_display_review')
    spans = clause['subject_display_spans']
    displayed = extract_parts(original, spans, 'subject display')
    if len(full_spans) != 1 or len(spans) != 1:
        raise ValueError('Subject display requires one complete source span and one display span')
    full_start, full_end = full_spans[0]
    start, end = spans[0]
    if start != full_start or end > full_end:
        raise ValueError('Subject display must be a prefix inside the complete subject')
    if displayed != displayed.strip():
        raise ValueError('Subject display must not include edge whitespace')
    # A token includes internal apostrophes/hyphens: do not print eco-, child
    # from child's, or part of a word. No English grammar is inferred here.
    def inside_token(position):
        return (0 < position < len(original)
                and re.fullmatch(r"[\w'’\-]", original[position - 1]) is not None
                and re.fullmatch(r"[\w'’\-]", original[position]) is not None)
    if inside_token(start) or inside_token(end):
        raise ValueError('Subject display must end and start at source token boundaries')
    return displayed


def render_verb(original, spans, readings):
    extract_parts(original, spans, 'verb')
    if not isinstance(readings, list):
        raise ValueError('contraction_readings must be a list')
    contractions = {}
    for start, end in spans:
        for match in re.finditer(r"['’]s\b", original[start:end]):
            contractions[(start + match.start(), start + match.end())] = None
    for record in readings:
        if not isinstance(record, dict):
            raise ValueError('Invalid contraction reading')
        position = record.get('span')
        if (not isinstance(position, list) or len(position) != 2
                or any(type(n) is not int for n in position)):
            raise ValueError('Contraction reading needs a source span')
        key = tuple(position)
        if key not in contractions:
            raise ValueError('Contraction reading is not an actual verb contraction')
        if contractions[key] is not None:
            raise ValueError('Duplicate contraction reading')
        if record.get('expanded') not in {'is', 'has'}:
            raise ValueError('Review the contraction as is or has')
        contractions[key] = record['expanded']
    if any(value is None for value in contractions.values()):
        raise ValueError('Every verb contraction needs a reviewed is/has reading')
    parts = []
    for start, end in spans:
        part = original[start:end]
        for (a, b), value in sorted(contractions.items(), reverse=True):
            if start <= a < b <= end and value == 'has':
                at = b - start
                part = part[:at] + '(has)' + part[at:]
        parts.append(part)
    return ' '.join(parts)


SV_REVIEW_KINDS = ('noun-phrase-answer', 'verbless-fragment')


def validate_sv_review(original, clauses, review):
    """Validate explicit omission evidence without inferring English grammar."""
    if not isinstance(review, dict) or review.get('kind') not in SV_REVIEW_KINDS:
        raise ValueError('Unsupported sv_review kind; expected noun-phrase-answer or verbless-fragment')
    if review.get('reviewed') is not True:
        raise ValueError('sv_review requires reviewed: true')
    for field in ['reason', 'context_sentence_id']:
        if not isinstance(review.get(field), str) or not review[field].strip():
            raise ValueError(f'sv_review requires a nonempty {field}')
    for field in ['source_text_sha256', 'context_text_sha256']:
        value = review.get(field)
        if not isinstance(value, str) or re.fullmatch('[0-9a-f]{64}', value) is None:
            raise ValueError(f'sv_review requires a lowercase SHA-256 at {field}')
    if review['source_text_sha256'] != hashlib.sha256(original.encode('utf-8')).hexdigest():
        raise ValueError('sv_review source_text_sha256 differs from the original sentence')
    if not isinstance(clauses, list) or clauses != []:
        raise ValueError('Reviewed verbless sentence requires explicit clauses: []')


def render_sv(original, clauses, sv_review=None):
    if not isinstance(original, str) or not original.strip():
        raise ValueError('Original sentence is required')
    if sv_review is not None:
        validate_sv_review(original, clauses, sv_review)
        return ''
    if not isinstance(clauses, list) or not clauses:
        raise ValueError('Reviewed clause records are required')
    ordered = []
    for index, clause in enumerate(clauses):
        kind = clause.get('kind')
        if kind not in {'main', 'subordinate', 'subject_relative', 'imperative'}:
            raise ValueError('Unknown reviewed clause kind')
        start = clause.get('start')
        if type(start) is not int or not 0 <= start < len(original):
            raise ValueError('Clause start must be a source position')
        marker = clause.get('marker', '')
        if not isinstance(marker, str) or any(x in marker for x in '[]／'):
            raise ValueError('Marker is text without display brackets or clause separators')
        if marker == '주절':
            raise ValueError('A main clause without a marker has no [주절] label')
        omitted = clause.get('omitted_marker', False)
        if type(omitted) is not bool:
            raise ValueError('omitted_marker must be boolean')
        if omitted and (not marker or kind != 'subordinate'):
            raise ValueError('An omitted connector must belong to a subordinate clause')
        if marker and not omitted and marker not in original:
            raise ValueError('Visible marker is absent from source')
        subject = render_subject(original, clause)
        verb = render_verb(original, clause.get('verb_spans', []),
                           clause.get('contraction_readings', []))
        if not verb:
            raise ValueError('Every displayed clause needs a reviewed verb')
        if kind == 'subject_relative':
            if not marker or subject:
                raise ValueError('Subject relative clause has a marker and V′ only')
        elif kind != 'imperative' and not subject:
            raise ValueError('A clause with an explicit subject must display it')
        prime = '′' if kind in {'subordinate', 'subject_relative'} else ''
        prefix = f'[{"(" + marker + ")" if omitted else marker}] ' if marker else ''
        fields = ([f'S{prime}: {subject}'] if subject else []) + [f'V{prime}: {verb}']
        ordered.append((start, index, prefix + ', '.join(fields)))
    # Positions, not repeated-word text searches, determine nested clause order.
    return ' ／ '.join(item[2] for item in sorted(ordered))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    if args.input.resolve() == args.output.resolve():
        raise ValueError('Output must not replace source input')
    data = json.loads(args.input.read_text(encoding='utf-8-sig'))
    text = render_sv(data['original'], data.get('clauses'), data.get('sv_review'))
    args.output.write_text(text + '\n' if text else '', encoding='utf-8')


if __name__ == '__main__':
    main()
