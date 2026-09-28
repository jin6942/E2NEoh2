"""Deterministic paragraph/subheading grouping after source segmentation is verified.

Input: {"paragraphs": [{"id": str, "source_id": str,
"subheading_id": str|null, "sentence_ids": [str, ...]}]}
IDs for subheadings identify occurrences, not merely identical heading text.
The helper does not infer sentence boundaries or resolve unheaded short passages.
An approved-merge resolution can override paragraph grouping only for its exact,
user-approved source, heading, ordered paragraphs, and ordered sentence IDs.
"""
import argparse
import json
from pathlib import Path


def group_units(paragraphs, resolutions=None):
    if not paragraphs:
        raise ValueError('No source paragraphs supplied')
    ids, sentences, closed_headings = set(), set(), set()
    previous = None
    headings = {}
    for paragraph in paragraphs:
        pid = paragraph['id']
        source = paragraph['source_id']
        heading = paragraph.get('subheading_id')
        sids = paragraph['sentence_ids']
        if not isinstance(pid, str) or not pid or pid in ids:
            raise ValueError('Missing or duplicate paragraph ID')
        if not isinstance(source, str) or not source:
            raise ValueError('Missing source ID')
        if heading is not None and (not isinstance(heading, str) or not heading):
            raise ValueError('Subheading ID must be nonempty or null')
        if not isinstance(sids, list) or not sids:
            raise ValueError('Headings and empty blocks are not source paragraphs')
        ids.add(pid)
        for sid in sids:
            if not isinstance(sid, str) or not sid or (source, sid) in sentences:
                raise ValueError('Missing or duplicate sentence ID within source')
            sentences.add((source, sid))
        key = (source, heading)
        if key != previous:
            if previous is not None:
                closed_headings.add(previous)
            if heading is not None and key in closed_headings:
                raise ValueError('Noncontiguous subheading ID: verify source segmentation')
            previous = key
        if heading is not None:
            headings.setdefault(key, []).append(paragraph)

    merged = {key for key, rows in headings.items()
              if any(len(row['sentence_ids']) <= 6 for row in rows)}
    # Legacy source-review decisions apply only to unheaded paragraphs. A
    # headed merge requires separately recorded, exact user-approved scope.
    reviewed, consumed = {}, set()
    positions = {row['id']: i for i, row in enumerate(paragraphs)}
    if resolutions is not None and not isinstance(resolutions, list):
        raise ValueError('Grouping resolutions must be a list')
    for decision in resolutions or []:
        if not isinstance(decision, dict):
            raise ValueError('A grouping resolution must be an object')
        pids = decision.get('paragraph_ids')
        evidence = decision.get('instruction')
        if not isinstance(pids, list) or not pids or any(not isinstance(x, str) for x in pids):
            raise ValueError('A source-review decision needs paragraph IDs')
        if not isinstance(evidence, str) or not evidence.strip():
            raise ValueError('Record the actual source-review instruction')
        if len(set(pids)) != len(pids) or any(x not in positions or x in consumed for x in pids):
            raise ValueError('Unknown, duplicate, or overlapping reviewed paragraphs')
        indexes = [positions[x] for x in pids]
        if indexes != list(range(indexes[0], indexes[0] + len(indexes))):
            raise ValueError('Reviewed paragraphs must be contiguous and in source order')
        rows = [paragraphs[i] for i in indexes]
        kind = decision.get('kind')
        if kind == 'approved-merge':
            heading = decision.get('subheading_id')
            if len(pids) < 2:
                raise ValueError('An approved merge requires at least two full paragraphs')
            if not isinstance(heading, str) or not heading.strip() or any(
                    row['source_id'] != decision.get('source_id') or
                    row.get('subheading_id') != heading for row in rows):
                raise ValueError('An approved merge must stay within one source and real subheading')
            if decision.get('approved_by') != 'user':
                raise ValueError('An approved merge requires actual user approval')
            approval_id = decision.get('approval_id')
            if not isinstance(approval_id, str) or not approval_id.strip():
                raise ValueError('An approved merge requires a user approval record ID')
            counts = decision.get('paragraph_sentence_counts')
            expected_counts = {row['id']: len(row['sentence_ids']) for row in rows}
            if not isinstance(counts, dict) or counts != expected_counts or any(
                    type(value) is not int for value in counts.values()):
                raise ValueError('Approved paragraph sentence counts must exactly match the source')
            expected_sids = [sid for row in rows for sid in row['sentence_ids']]
            if decision.get('sentence_ids') != expected_sids:
                raise ValueError('Approved sentence IDs must match complete paragraphs in source order')
            key = (decision['source_id'], heading)
            if key in merged and pids != [row['id'] for row in headings[key]]:
                raise ValueError('An approved merge cannot partially consume an automatic short-heading group')
            metadata = {'reason': 'explicit-user-approved-merge',
                        'approved_by': 'user', 'approval_id': approval_id,
                        'instruction': evidence,
                        'paragraph_sentence_counts': dict(counts)}
        elif kind is None:
            if any(row['source_id'] != decision.get('source_id') or row.get('subheading_id') is not None for row in rows):
                raise ValueError('Source review cannot cross sources or replace headed grouping')
            if not any(len(row['sentence_ids']) <= 6 for row in rows):
                raise ValueError('Source-review exception requires an unheaded short paragraph')
            metadata = {'reason': 'explicit-unheaded-source-review', 'instruction': evidence}
        else:
            raise ValueError('Unknown grouping resolution kind')
        reviewed[pids[0]] = (rows, metadata)
        consumed.update(pids)

    units, unresolved, visited = [], [], set()
    for paragraph in paragraphs:
        source, heading = paragraph['source_id'], paragraph.get('subheading_id')
        key = (source, heading)
        if paragraph['id'] in consumed:
            if paragraph['id'] in reviewed:
                rows, metadata = reviewed[paragraph['id']]
                units.append({'source_id': source, 'subheading_id': heading,
                              'paragraph_ids': [row['id'] for row in rows],
                              'sentence_ids': [sid for row in rows for sid in row['sentence_ids']],
                              **metadata})
            continue
        if heading is None and len(paragraph['sentence_ids']) <= 6:
            unresolved.append({'code': 'UNHEADED_SHORT_REQUIRES_SOURCE_REVIEW',
                               'source_id': source, 'paragraph_id': paragraph['id'],
                               'sentence_ids': list(paragraph['sentence_ids'])})
            continue
        if key in merged:
            if key in visited:
                continue
            visited.add(key)
            rows, reason = headings[key], 'short-paragraph-groups-entire-subheading'
        else:
            rows, reason = [paragraph], 'original-paragraph'
        units.append({'source_id': source, 'subheading_id': heading,
                      'paragraph_ids': [row['id'] for row in rows],
                      'sentence_ids': [sid for row in rows for sid in row['sentence_ids']],
                      'reason': reason})
    # No partly finalized map is emitted when a user decision remains necessary.
    if unresolved:
        return {'status': 'NEEDS_SOURCE_REVIEW', 'unresolved': unresolved,
                'candidate_units': units, 'units': []}
    return {'status': 'READY', 'units': units, 'unresolved': []}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    data = json.loads(args.input.read_text(encoding='utf-8-sig'))
    if ('grouping_resolutions' in data and 'resolutions' in data and
            data['grouping_resolutions'] != data['resolutions']):
        raise ValueError('Conflicting grouping_resolutions and legacy resolutions')
    resolutions = data.get('grouping_resolutions', data.get('resolutions'))
    result = group_units(data['paragraphs'], resolutions)
    if args.input.resolve() == args.output.resolve():
        raise ValueError('Output must not replace source input')
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    return 0 if result['status'] == 'READY' else 2


if __name__ == '__main__':
    raise SystemExit(main())
