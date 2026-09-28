"""Source-bound headings, lesson identity and suspicious sentence-boundary review.

This checks supplied records and hashes, not the contents of an external textbook.
It never invents headings or inserts whitespace into the authoritative source.
"""
import hashlib
import re


def normalize_course(course):
    """Canonicalize known course aliases for checks, without changing display text."""
    compact = ''.join(course.split()) if isinstance(course, str) else ''
    return {'영어II': '영어2', '영어Ⅱ': '영어2'}.get(compact, compact)


def course_policy(course):
    """Use one course identity for reference grade and full mock-set counts.

    The existing five-question default remains for other courses; their grade
    must still be supplied and verified explicitly by the caller.
    """
    normalized = normalize_course(course)
    known = {'공통영어1': (1, 5), '공통영어2': (1, 5), '영어2': (2, 7)}
    grade, count = known.get(normalized, (None, 5))
    return {'course': normalized, 'reference_grade': grade,
            'mock_questions_per_round': count}


def _text(value, label):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f'{label}: nonempty text required')
    return value


def _display_line(value, label):
    value = _text(value, label)
    if len(value.splitlines()) != 1 or any(c in value for c in '\r\n'):
        raise ValueError(f'{label}: one line required')
    return ' '.join(value.split())


def display_publisher_author(metadata):
    """Normalize the confirmed publisher alias, preserving other identities."""
    value = _display_line(metadata.get('publisher_author'), 'metadata/publisher_author')
    if ''.join(value.split()) in {'능률(민병천)', 'NE능률(민병천)'}:
        return 'NE능률(민병천)'
    return value


def display_book_name(metadata):
    """Derive the printed name from identity fields, never a legacy filename."""
    course = _display_line(metadata.get('course'), 'metadata/course')
    return normalize_course(course) + ' ' + display_publisher_author(metadata)


def display_source_label(source):
    """Unify only equivalent main-text labels; keep distinct source names."""
    value = _display_line(source.get('label'), 'source/label')
    return '본문' if value in {'교과서 본문', '본문'} else value


LESSON_KINDS = {
    'lesson': ('UNIT', '{number}과'),
    'special': ('SL', 'Special Lesson {number}'),
}


def _identity(value, label):
    """Return (kind, number); bare numbers can confirm either lesson kind."""
    if type(value) is int and value >= 0:
        return None, value
    if isinstance(value, str):
        match = re.fullmatch(r'\s*(?:SPECIAL\s*LESSON|SL)\s*(\d+)\s*', value, re.I)
        if match:
            return 'special', int(match.group(1))
        match = re.fullmatch(r'\s*(?:(?:UNIT|LESSON)\s*|제\s*)?(\d+)\s*과?\s*', value, re.I)
        if match:
            kind = None if re.fullmatch(r'\s*\d+\s*', value) else 'lesson'
            return kind, int(match.group(1))
    raise ValueError(f'{label}: a verified numeric lesson identity is required')


def _number(value, label):
    return _identity(value, label)[1]


def lesson_identity(metadata, cover=None):
    """Return display/internal forms without rewriting legacy metadata.lesson."""
    kind, number = _identity(metadata.get('lesson'), 'metadata/lesson')
    kind = kind or 'lesson'
    for field in ('lesson_id', 'lesson_number'):
        if field in metadata:
            other_kind, other = _identity(metadata[field], 'metadata/' + field)
            if other != number or (other_kind is not None and other_kind != kind):
                raise ValueError(f'Lesson identity conflict: metadata/{field}')
    if cover is not None:
        if 'lesson_number' in cover:
            other_kind, other = _identity(cover['lesson_number'], 'cover/lesson_number')
            if other != number or (other_kind is not None and other_kind != kind):
                raise ValueError('Lesson identity conflict: metadata.lesson and cover.lesson_number')
        if 'lesson_label' in cover:
            label = cover['lesson_label']
            normalized = ' '.join(label.split()).upper() if isinstance(label, str) else ''
            label_kind = {'LESSON': 'lesson', 'UNIT': 'lesson', 'SPECIAL LESSON': 'special'}.get(normalized)
            if label_kind is not None and label_kind != kind:
                raise ValueError('Lesson identity conflict: metadata.lesson and cover.lesson_label')
    prefix, display = LESSON_KINDS[kind]
    return {'number': number, 'kind': kind, 'internal_id': f'{prefix}{number:02d}',
            'display': display.format(number=number)}


def display_lesson(metadata, cover=None):
    return lesson_identity(metadata, cover)['display']


def transcription_sha256(source):
    return hashlib.sha256(source['text'].encode('utf-8')).hexdigest()


def check_source_structure(source, paragraphs):
    """Return review issues for missing headings or unreviewed joined boundaries.

    Malformed records are errors; incomplete legacy metadata needs source review.
    location is the actual textbook page/region; before_sentence_id anchors the
    heading in body order because sources.text intentionally contains body only.
    """
    source_id = source['id']
    artifact_sha = source['provenance']['sha256']
    source_paragraphs = [p for p in paragraphs if p['source_id'] == source_id]
    sentence_ids = [row['id'] for row in source['sentences']]
    headings = source.get('subheadings', [])
    if not isinstance(headings, list):
        raise ValueError('Source subheadings must be a list of actual occurrences')
    indexed = {}
    for row in headings:
        if not isinstance(row, dict):
            raise ValueError('Source subheading must be an object')
        hid = _text(row.get('id'), 'Source subheading occurrence ID')
        if hid in indexed:
            raise ValueError('Duplicate source subheading occurrence ID')
        _text(row.get('text'), 'Original subheading text')
        _text(row.get('location'), 'Original subheading source location')
        if row.get('artifact_sha256') != artifact_sha:
            raise ValueError('Source subheading artifact hash differs from source provenance')
        if row.get('before_sentence_id') not in sentence_ids:
            raise ValueError('Source subheading anchor is not a source sentence')
        indexed[hid] = row
    used = list(dict.fromkeys(p['subheading_id'] for p in source_paragraphs if p.get('subheading_id') is not None))
    issues = []
    for hid in used:
        if hid not in indexed:
            issues.append({'code': 'MISSING_SOURCE_SUBHEADING', 'source_id': source_id,
                           'subheading_id': hid, 'instruction': 'Read the original heading and record its text, location and source hash; do not derive it from the analysis title.'})
            continue
        first = next(p for p in source_paragraphs if p.get('subheading_id') == hid)
        if indexed[hid]['before_sentence_id'] != first['sentence_ids'][0]:
            raise ValueError('Source subheading must anchor the first sentence under that occurrence')
    if set(indexed) - set(used):
        raise ValueError('Recorded source subheading has no corresponding original paragraph')

    bounds = source['sentences']
    original = source['text']
    suspicious = {}
    for left, right in zip(bounds, bounds[1:]):
        # Offsets/order/coverage are already checked by question_source.excerpt.
        a, b = left['end'], right['start']
        bridge = original[a:b]
        if bridge or not a or b >= len(original):
            continue
        if original[a-1].isspace() or original[b].isspace():
            continue
        left_text = original[left['start']:a]
        right_text = original[b:right['end']]
        if (re.search(r'[.!?][\"\'”’\)\]]*$', left_text)
                and re.match(r'[\"\'“‘\(\[]*[A-Za-z]', right_text)):
            key = (left['id'], right['id'])
            suspicious[key] = {'code': 'JOINED_SENTENCE_BOUNDARY', 'source_id': source_id,
                               'left_sentence_id': key[0], 'right_sentence_id': key[1],
                               'offset': b, 'context': original[max(0, b-35):b+35],
                               'instruction': 'Compare this boundary with the original; do not automatically insert a space.'}
    exceptions = source.get('boundary_reviews', [])
    if not isinstance(exceptions, list):
        raise ValueError('Boundary reviews must be a list')
    reviewed = set()
    for row in exceptions:
        if not isinstance(row, dict):
            raise ValueError('Boundary review must be an object')
        key = (row.get('left_sentence_id'), row.get('right_sentence_id'))
        if key not in suspicious or key in reviewed:
            raise ValueError('Boundary review is duplicate or does not match a suspicious boundary')
        if row.get('resolution') not in {'source-confirmed-no-space', 'abbreviation-boundary'}:
            raise ValueError('Boundary review needs an explicit source-confirmed resolution')
        _text(row.get('reason'), 'Boundary review reason')
        _text(row.get('verification_record'), 'Actual boundary source-review record')
        if row.get('artifact_sha256') != artifact_sha:
            raise ValueError('Boundary review artifact hash differs from source provenance')
        if row.get('transcription_sha256') != transcription_sha256(source):
            raise ValueError('Boundary review is stale for this source transcription')
        reviewed.add(key)
    issues += [issue for key, issue in suspicious.items() if key not in reviewed]
    return {'issues': issues, 'subheading_count': len(indexed),
            'reviewed_boundary_count': len(reviewed),
            'review_evidence': 'REVIEWER_SUPPLIED_EXTERNAL_SOURCE_BYTES_NOT_CHECKED'}


def unit_subheadings(data, unit):
    """Actual headings for this unit, in occurrence order, after source checking."""
    source = next(s for s in data['sources'] if s['id'] == unit['source_id'])
    lookup = {row['id']: row for row in source.get('subheadings', [])}
    selected = set(unit['paragraph_ids'])
    ids = list(dict.fromkeys(p['subheading_id'] for p in data['paragraphs']
                            if p['source_id'] == source['id'] and p['id'] in selected
                            and p.get('subheading_id') is not None))
    if any(hid not in lookup for hid in ids):
        raise ValueError('Original subheading text requires source review before output')
    return [lookup[hid] for hid in ids]
