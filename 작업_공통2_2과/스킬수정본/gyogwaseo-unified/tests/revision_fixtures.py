"""Synthetic records for regression only; these do not approve real content."""
from copy import deepcopy
import re
from question_source import LENGTH_PROFILE_ID, recommended_benchmarks, build_view


def length_review(kind, grade=1):
    return {'profile_id': LENGTH_PROFILE_ID, 'grade': grade,
            'benchmark_ids': recommended_benchmarks(grade, kind),
            'rationale': 'Synthetic mechanical fixture; no educational sufficiency claim.',
            'independent_review_required': True}


def upgrade_assessment_fixture(data):
    a = data['assessment']
    a['scope']['course'] = data['metadata']['course']
    a['passage_groups'] = []
    qmap = {q['id']: q for q in a['questions']}
    requests = {r['id']: r for r in data['question_sources']}
    explanations = {q['id']: q for q in a['explanations']}
    for q in a['questions']:
        requests[q['id']]['length_review'] = length_review(q['type'])
    for u in data['units']:
        q = qmap[u['workbook']['question_id']]
        term = u['analysis']['relations'][0]['head']
        q['choices'][0]['text'] += ' ' + term['text']
        text = q['choices'][0]['text']
        start = text.index(term['text'])
        q['learned_relation_uses'] = [{'term_id': term['id'], 'choice_number': 1,
            'choice_span': [start, start+len(term['text'])], 'surface': term['text'],
            'reason_ko': '합성 연결 검사 전용. 실제 의미 평가로 주장하지 않음.'}]
        explanations[q['id']]['choices'] = deepcopy(q['choices'])
    for sid in dict.fromkeys(q['set_id'] for q in a['questions'] if q['set_id'] != 'workbook'):
        rows = sorted([q for q in a['questions'] if q['set_id'] == sid], key=lambda q: q['number'])
        title, vocabulary = rows[-2:]
        gid = sid + '-long'
        title['type'] = '제목'
        title['question'] = title['id'] + ' 다음 글의 제목으로 가장 적절한 것은?'
        vocabulary.update(type='어휘', choice_mode='in_passage',
            question=vocabulary['id'] + ' 다음 글의 ①~⑤ 중 문맥상 낱말의 쓰임이 적절하지 않은 것은?',
            choices=[{'number': n, 'text': chr(0x2460+n-1)} for n in range(1, 6)])
        original = title['passage']
        marks = [[m.start(), m.end()] for m in list(re.finditer(r'[A-Za-z]+', original))[:5]]
        vr = requests[vocabulary['id']]
        vr.update(type='어휘', replacement_span=marks[vocabulary['answer']-1], replacement='Changed', vocabulary_marks=marks)
        for q in [title, vocabulary]:
            q['passage_group_id'] = gid
            req = requests[q['id']]
            req.update(type=q['type'], length_review=length_review('long41_42'))
        source = next(s for s in data['sources'] if s['id']==vr['source_id'])
        view = build_view(source, vr, expected_grade=1, benchmark_type='long41_42')
        vocabulary['passage'] = view['passage']
        explanations[vocabulary['id']].update(choices=deepcopy(vocabulary['choices']), choices_ko=[])
        a['passage_groups'].append({'id': gid, 'kind': 'long_reading', 'set_id': sid,
            'question_ids': [title['id'], vocabulary['id']], 'passage_question_id': vocabulary['id']})
    return data
