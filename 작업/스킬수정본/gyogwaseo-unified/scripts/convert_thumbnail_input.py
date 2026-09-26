"""Convert a checked common manuscript to the unchanged Claude thumbnail input.

Only exports title, source-ordered chunks and glosses. Does not render, select a
preview, change thumbnail copy, or certify semantic/layout review.
"""
import argparse
import json
from pathlib import Path
import re

from check_learning_content import check


def legacy_title(metadata):
    course = metadata['course'].strip()
    publisher = metadata['publisher_author'].strip()
    lesson = metadata['lesson'].strip()
    numbered = re.fullmatch(r'(?:(?:UNIT|LESSON)\s*|제\s*)?(\d+)\s*과?', lesson, re.I)
    if numbered:
        lesson = f'{int(numbered[1])}과'
    title = f'{course} {publisher} {lesson}'
    # Reject labels that the original parse_meta would silently misidentify.
    match = re.match(r'^(\S+)\s+(.+?)\s+(\S*\d+\s*과)\b', title.split('·')[0].strip())
    if not match or match.groups() != (course, publisher, lesson):
        raise ValueError('Metadata cannot be represented by the original thumbnail title parser; '
                         'check course, publisher_author and lesson labels before export')
    return title


def convert(data):
    result = check(data)
    if result['status'] != 'STRUCTURE_PASS':
        raise ValueError('Resolve source grouping before thumbnail input conversion')
    title = legacy_title(data['metadata'])
    indexed = {(s['source_id'], s['id']): s for s in data['sentences']}
    sections = []
    for source in data['sources']:
        rows = []
        for boundary in source['sentences']:
            sentence = indexed[(source['id'], boundary['id'])]
            glosses = []
            for gloss in sentence['glosses']:
                meaning = gloss['meaning_ko']
                if gloss.get('referent_ko'):
                    meaning += ' (' + gloss['referent_ko'] + ')'
                glosses.append([gloss['headword'], meaning, gloss['star']])
            rows.append({'chunks': [sentence['text'][c['start']:c['end']]
                                    for c in sentence['chunks']], 'gloss': glosses})
        sections.append({'sentences': rows})
    if not sections or not any(row['chunks'] for s in sections for row in s['sentences']):
        raise ValueError('No thumbnail sentence chunks; refusing empty output')
    return {'title': title, 'sections': sections}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('manuscript', type=Path)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    if args.output.exists():
        parser.error('Output already exists; preserve it and choose a new working path')
    try:
        data = json.loads(args.manuscript.read_text(encoding='utf-8-sig'))
        converted = convert(data)
    except (ValueError, KeyError, TypeError, OSError) as exc:
        parser.error(str(exc))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open('x', encoding='utf-8', newline='\n') as stream:
        json.dump(converted, stream, ensure_ascii=False, indent=2)
        stream.write('\n')
    rows = [r for s in converted['sections'] for r in s['sentences']]
    print(json.dumps({'output': str(args.output), 'sentences': len(rows),
                      'glosses': sum(len(r['gloss']) for r in rows),
                      'thumbnail_rendered': False}, ensure_ascii=False))


if __name__ == '__main__':
    main()
