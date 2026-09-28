"""Build the common analysis reading body from verified source spans.

Input: {sentences: [{source_id, id, text, chunks: [{start, end, ko}],
natural_ko}], units: [{source_id, sentence_ids: [...]}]}.
Offsets are zero-based Unicode code-point offsets with an exclusive end.
This validates structural fidelity, not translation accuracy or FINAL status.
"""
import argparse
import json
from pathlib import Path


def required_text(value, label):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f'{label} must be nonempty text')
    return value


def sentence_blocks(sentence):
    source = required_text(sentence.get('source_id'), 'source_id')
    sid = required_text(sentence.get('id'), 'sentence id')
    original = required_text(sentence.get('text'), 'original text')
    natural = required_text(sentence.get('natural_ko'), 'natural_ko')
    chunks = sentence.get('chunks')
    if not isinstance(chunks, list) or not chunks:
        raise ValueError('At least one verified chunk is required')
    english, korean, offsets = [], [], []
    previous = 0
    for chunk in chunks:
        start, end = chunk.get('start'), chunk.get('end')
        if type(start) is not int or type(end) is not int:
            raise ValueError('Chunk offsets must be integers')
        if not 0 <= previous <= start < end <= len(original):
            raise ValueError('Chunk spans overlap, reverse, or exceed the source')
        if original[previous:start].strip():
            raise ValueError('Chunk spans omit source characters')
        english.append(required_text(original[start:end], 'English chunk'))
        korean.append(required_text(chunk.get('ko'), 'Korean chunk'))
        offsets.append({'start': start, 'end': end})
        previous = end
    if original[previous:].strip():
        raise ValueError('Chunk spans omit the source ending')
    # Source punctuation, superscripts, circled numbers, and quotes are never
    # normalized or stripped. Generated chunk numbers belong to the renderer.
    return {
        'source_id': source,
        'sentence_id': sid,
        'original': original,
        'source_spans': offsets,
        'blocks': [
            {'role': 'analysis_english_chunks', 'chunks': english},
            {'role': 'analysis_korean_chunks', 'chunks': korean},
            {'role': 'analysis_natural_translation', 'text': natural},
        ],
    }


def build_analysis_bodies(data):
    sentences, units = data.get('sentences'), data.get('units')
    if not isinstance(sentences, list) or not sentences:
        raise ValueError('Verified source sentences are required')
    if not isinstance(units, list) or not units:
        raise ValueError('Confirmed common learning units are required')
    records, source_order = {}, []
    for sentence in sentences:
        record = sentence_blocks(sentence)
        key = (record['source_id'], record['sentence_id'])
        if key in records:
            raise ValueError('Duplicate source sentence')
        records[key] = record
        source_order.append(key)
    output, seen, unit_order = [], set(), []
    for index, unit in enumerate(units, 1):
        source = required_text(unit.get('source_id'), 'unit source_id')
        ids = unit.get('sentence_ids')
        if not isinstance(ids, list) or not ids:
            raise ValueError('Empty learning unit')
        body = []
        for sid in ids:
            required_text(sid, 'unit sentence id')
            key = (source, sid)
            if key not in records or key in seen:
                raise ValueError('Unknown or repeated sentence in learning units')
            seen.add(key)
            unit_order.append(key)
            body.append(records[key])
        output.append({'unit_number': index, 'source_id': source,
                       'role': 'analysis_reading_body', 'sentences': body})
    if seen != set(records):
        raise ValueError('Learning units omit source sentences')
    if unit_order != source_order:
        raise ValueError('Learning units change source sentence order')
    return {'status': 'STRUCTURE_VALIDATED',
            'semantic_review': 'NOT_PERFORMED',
            'standalone_model_translation_section': False,
            'units': output}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    if args.input.resolve() == args.output.resolve():
        raise ValueError('Output must not replace source input')
    data = json.loads(args.input.read_text(encoding='utf-8-sig'))
    result = build_analysis_bodies(data)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')


if __name__ == '__main__':
    main()
