"""Source-backed question passage views. Offsets are Unicode codepoint indices.

Sources: {id, text, sentences:[{id,start,end}]}. The verified text contains the
reading body, including its original paragraph whitespace, not page furniture.
Question: {type, source_id, first_sentence, last_sentence, ...type fields}.
This helper does not determine sentence boundaries, meanings, or unique answers.
Inserted labels are separate metadata, never found/removed by character regex.
"""
import argparse
from functools import lru_cache
import json
from pathlib import Path

PLAIN = {'제목', '주제', '요지', '주장', '목적', '심경·분위기', '내용', '요약'}
LENGTH_PROFILE_ID = 'kr-hs-english-2026-3-6-9-v1'


@lru_cache(maxsize=1)
def length_profile():
    profile = json.loads((Path(__file__).resolve().parent.parent /
                          'assets/exam-length-profile.json').read_text(encoding='utf-8'))
    if profile.get('profile_id') != LENGTH_PROFILE_ID:
        raise ValueError('The official exam length profile identity is inconsistent')
    return profile


def recommended_benchmarks(grade, benchmark_type):
    """Return all measured same-grade, same-type references; no generated verdict."""
    if type(grade) is not int or grade not in (1, 2):
        raise ValueError('Reference grade must be high-school year 1 or 2')
    rows = [r for r in length_profile()['passages']
            if r['grade'] == grade and r['type'] == benchmark_type]
    if not rows:
        raise ValueError('No verified same-grade, same-type length benchmark exists')
    return [r['id'] for r in sorted(rows, key=lambda r: r['id'])]


def compare_length(question, count, expected_grade=None, benchmark_type=None):
    """Record empirical comparison without claiming educational sufficiency.

    The former fixed 100-word rejection is intentionally absent. A short item
    must be explicitly queued for independent review; metadata alone cannot
    turn it into an independently approved item.
    """
    review = question.get('length_review')
    if not isinstance(review, dict) or review.get('profile_id') != LENGTH_PROFILE_ID:
        raise ValueError('A current official-profile length_review is required')
    grade = review.get('grade')
    if expected_grade is not None and grade != expected_grade:
        raise ValueError('Length-review grade differs from the verified textbook course')
    kind = benchmark_type or question.get('type')
    expected = recommended_benchmarks(grade, kind)
    references = review.get('benchmark_ids')
    if not isinstance(references, list) or len(references) != len(expected) or \
            any(not isinstance(x, str) for x in references) or sorted(references) != expected:
        raise ValueError('Length review must cite every same-grade, same-type profile reference')
    if not isinstance(review.get('rationale'), str) or not review['rationale'].strip():
        raise ValueError('Length review requires an actual comparison rationale')
    by_id = {r['id']: r for r in length_profile()['passages']}
    reference_words = [by_id[x]['words'] for x in expected]
    shorter = count < min(reference_words)
    if shorter and review.get('independent_review_required') is not True:
        raise ValueError('Below-reference passage must be explicitly queued for independent length review')
    return {'status': 'NEEDS_INDEPENDENT_REVIEW' if shorter else 'RECORDED',
            'profile_id': LENGTH_PROFILE_ID, 'grade': grade, 'benchmark_type': kind,
            'benchmark_ids': expected, 'reference_words': reference_words,
            'assessment_word_count': count, 'shorter_than_all_references': shorter,
            'independent_review_required': shorter or review.get('independent_review_required') is True,
            'rationale': review['rationale'], 'educational_sufficiency': 'NOT_CHECKED_BY_THIS_TOOL'}


def word_count(text):
    return sum(any(ch.isalnum() for ch in token) for token in text.split())


def span(value, text, allow_empty=False):
    if not isinstance(value, list) or len(value) != 2 or any(type(x) is not int for x in value):
        raise ValueError('Span must have two integer Unicode codepoint offsets')
    a, b = value
    if not (0 <= a <= b <= len(text)) or (a == b and not allow_empty):
        raise ValueError('Span is empty or outside source')
    return a, b


def excerpt(source, question):
    if source.get('id') != question.get('source_id'):
        raise ValueError('Source identity mismatch')
    text = source.get('text')
    records = source.get('sentences')
    if not isinstance(text, str) or not text.strip() or not isinstance(records, list) or not records:
        raise ValueError('Verified source text and sentence boundaries are required')
    previous, seen = 0, set()
    for row in records:
        sid = row.get('id')
        if not isinstance(sid, str) or not sid or sid == '@added' or sid in seen:
            raise ValueError('Missing or duplicate source sentence ID')
        seen.add(sid)
        a, b = span([row.get('start'), row.get('end')], text)
        if a < previous or text[previous:a].strip():
            raise ValueError('Source sentence boundaries overlap, reverse, or omit text')
        if not text[a:b].strip():
            raise ValueError('Empty source sentence')
        previous = b
    if text[previous:].strip():
        raise ValueError('Source sentence boundaries omit the end of the source')
    ids = [r['id'] for r in records]
    try:
        first, last = ids.index(question['first_sentence']), ids.index(question['last_sentence'])
    except (KeyError, ValueError) as exc:
        raise ValueError('Unknown source range sentence') from exc
    if first > last:
        raise ValueError('Reversed source range')
    start, end = records[first]['start'], records[last]['end']
    selected = text[start:end]
    local = [{'id': r['id'], 'start': r['start'] - start, 'end': r['end'] - start}
             for r in records[first:last + 1]]
    return selected, local, [start, end]


def build_view(source, question, *, expected_grade=None, benchmark_type=None):
    original, sentences, source_span = excerpt(source, question)
    count = word_count(original)
    kind = question.get('type')
    view = {'original': original, 'source_id': source['id'], 'source_span': source_span,
            'source_sentence_ids': [s['id'] for s in sentences], 'word_count': count,
            'type': kind, 'passage': original, 'annotations': [],
            'source_reconstruction': 'PASS', 'semantic_review': 'NOT_PERFORMED',
            'preserve_paragraphs': False}
    recovered = original
    starts = {r['start'] for r in sentences}
    boundaries = starts | {len(original)}
    if kind in PLAIN:
        pass
    elif kind == '함축 의미':
        a, b = span(question.get('target_span'), original)
        view['target'] = original[a:b]
        view['annotations'] = [{'kind': 'underline', 'span': [a, b]}]
    elif kind in {'빈칸', '어휘'}:
        a, b = span(question.get('replacement_span'), original)
        old = original[a:b]
        replacement = '________________' if kind == '빈칸' else question.get('replacement')
        if not isinstance(replacement, str) or not replacement.strip() or replacement == old:
            raise ValueError('A nonempty, changed question replacement is required')
        if kind == '어휘' and (any(c.isspace() for c in old) or any(c.isspace() for c in replacement)):
            raise ValueError('Vocabulary question changes one word only')
        view['passage'] = original[:a] + replacement + original[b:]
        view['replacement'] = {'start': a, 'end': a + len(replacement),
                               'original': old, 'text': replacement}
        recovered = view['passage'][:a] + old + view['passage'][a + len(replacement):]
        if kind == '어휘':
            marks = question.get('vocabulary_marks')
            if not isinstance(marks, list) or len(marks) != 5:
                raise ValueError('Vocabulary requires five numbered source targets')
            checked = [span(x, original) for x in marks]
            if checked != sorted(checked) or len(set(checked)) != 5:
                raise ValueError('Vocabulary targets must be distinct and in source order')
            if any(checked[i][1] > checked[i + 1][0] for i in range(4)):
                raise ValueError('Vocabulary targets overlap')
            if (a, b) not in checked:
                raise ValueError('Changed vocabulary word is not a numbered target')
            view['answer'] = checked.index((a, b)) + 1
            for n, (x, y) in enumerate(checked, 1):
                offset = len(replacement) - (b - a) if x >= b else 0
                end = a + len(replacement) if (x, y) == (a, b) else y + offset
                view['annotations'].append({'kind': 'numbered_word', 'number': n, 'span': [x + offset, end]})
    elif kind == '삽입':
        given_id = question.get('given_sentence')
        found = [r for r in sentences if r['id'] == given_id]
        if len(found) != 1:
            raise ValueError('Insertion given must be one source sentence in the range')
        a, b = found[0]['start'], found[0]['end']
        slots = question.get('insertion_slots')
        if not isinstance(slots, list) or len(slots) != 5 or any(type(x) is not int for x in slots):
            raise ValueError('Insertion requires five numbered source boundary positions')
        if slots != sorted(set(slots)) or not set(slots) <= boundaries or a not in slots:
            raise ValueError('Insertion slots must be ordered, distinct, and include the source answer')
        # The removed sentence's following boundary aliases the same student gap.
        mapped = [x if x <= a else x - (b - a) for x in slots]
        passage = original[:a] + original[b:]
        gap_keys = [len(passage[:x].rstrip()) for x in mapped]
        if len(set(gap_keys)) != 5:
            raise ValueError('Two insertion slots collapse to the same visible gap')
        view.update(given=original[a:b], passage=passage, answer=slots.index(a) + 1)
        view['annotations'] = [{'kind': 'insertion_slot', 'number': i + 1, 'offset': x}
                               for i, x in enumerate(mapped)]
        recovered = passage[:a] + view['given'] + passage[a:]
    elif kind == '순서':
        ranges = question.get('block_spans')
        if not isinstance(ranges, dict) or set(ranges) != {'given', 'A', 'B', 'C'}:
            raise ValueError('Ordering requires given and A/B/C source spans')
        ordered = sorted((span(value, original), key) for key, value in ranges.items())
        cursor = 0
        for (a, b), key in ordered:
            if a != cursor or a not in boundaries or b not in boundaries or not original[a:b].strip():
                raise ValueError('Ordering blocks must partition source at sentence boundaries exactly')
            cursor = b
        if cursor != len(original) or ordered[0][1] != 'given':
            raise ValueError('Ordering given must be the source beginning and all source must be retained')
        answer_order = [key for _, key in ordered[1:]]
        if answer_order == ['A', 'B', 'C']:
            raise ValueError('Relabel ordering blocks: ABC is absent from the canonical five choices')
        view.update(given=original[slice(*ranges['given'])],
                    blocks={key: original[slice(*ranges[key])] for key in 'ABC'},
                    correct_order=answer_order, passage=None)
        recovered = view['given'] + ''.join(view['blocks'][key] for key in answer_order)
    elif kind == '무관한 문장':
        offset, added = question.get('addition_offset'), question.get('addition')
        if type(offset) is not int or offset not in boundaries:
            raise ValueError('Unrelated sentence must be inserted at a verified source boundary')
        if not isinstance(added, str) or not added.strip():
            raise ValueError('Unrelated sentence is missing')
        marks = question.get('sentence_marks')
        if not isinstance(marks, list) or len(marks) != 5 or len(set(marks)) != 5 or '@added' not in marks:
            raise ValueError('Unrelated question requires five targets including the added sentence')
        positions = {r['id']: r['start'] for r in sentences}
        positions['@added'] = offset
        if any(key not in positions for key in marks):
            raise ValueError('Unknown unrelated sentence target')
        # Added sentence precedes an original sentence at the same boundary.
        ordering = sorted(marks, key=lambda key: (positions[key], key != '@added'))
        if ordering != marks:
            raise ValueError('Numbered targets must follow the displayed sentence order')
        inserted = added.rstrip() + ' '
        passage = original[:offset] + inserted + original[offset:]
        view.update(passage=passage, answer=marks.index('@added') + 1,
                    addition={'start': offset, 'end': offset + len(inserted), 'text': inserted})
        view['annotations'] = [{'kind': 'sentence_number', 'number': i + 1,
                                'offset': positions[key] + (len(inserted) if key != '@added' and positions[key] >= offset else 0)}
                               for i, key in enumerate(marks)]
        recovered = passage[:offset] + passage[offset + len(inserted):]
    else:
        raise ValueError('Unsupported question type, including grammar')
    if recovered != original:
        raise ValueError('Question cannot reconstruct exact original source')
    # The comparison measures the material a student reads. For unrelated-
    # sentence items this includes the inserted distractor, as in the exam
    # profile. word_count continues to describe only the authoritative source.
    assessment_count = count + (word_count(question['addition']) if kind == '무관한 문장' else 0)
    view['length_comparison'] = compare_length(question, assessment_count,
                                              expected_grade, benchmark_type)
    return view


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    if args.input.resolve() == args.output.resolve():
        raise ValueError('Output cannot overwrite source input')
    data = json.loads(args.input.read_text(encoding='utf-8-sig'))
    result = build_view(data['source'], data['question'])
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
