"""워크북 실전문제(Q01)와 미니 모의고사 1회(Q02~Q06) 원고 — 공통영어2 YBM(박준언) 2과 Further Reading.

지문·정답 위치는 원문에서 계산하고 question_source.build_view로 복원을 검증한다.
조립 코드는 같은 과 본책의 작업_공통2_2과/assessment_data.py와 같다(고1 grade 1 분량 비교).

회차 편성 원칙: 공유 장문(Q05·Q06)이 전체 지문 s01~s09이므로, 같은 회의 일반 3문항은 원문을 보면
답이 드러나는 빈칸·순서·삽입·무관 유형을 쓰지 않고 내용·함축·요지로 편성한다.
어휘 문항에서 바꾼 표적(s08 severe)은 일반 3문항 지문(모두 s01~s07 안)에 나오지 않게 한다.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / '작업_공통2_2과' / '스킬수정본' / 'gyogwaseo-unified' / 'scripts'))
from question_source import build_view, recommended_benchmarks, LENGTH_PROFILE_ID  # noqa: E402

GRADE = 1
CIRCLED = '①②③④⑤'
ORDER = [['A', 'C', 'B'], ['B', 'A', 'C'], ['B', 'C', 'A'], ['C', 'A', 'B'], ['C', 'B', 'A']]
BENCH_SHORT_NOTE = '동일 유형 공식 표본보다 짧아 독립 검수에서 분량·정보 전개를 확인해야 함. '
INSTRUCTION = ('2026-09-29 사용자 선택 “워크북 1 + 모의 1회 5문항 (추천)”: 약 175단어 Further Reading 1단위에 맞춰 '
               '워크북 실전문제 1문항 + 미니 모의고사 1회 5문항(일반 3 + 공유 장문 제목·어휘 2). '
               '공유 장문은 전체 원문이지만 고1 장문 표본보다 짧아 독립 검수에서 분량을 확인한다.')

Q = []  # 작성 순서 = 출력 순서


def q(**kw):
    Q.append(kw)


# ================================================================ 워크북 실전문제
q(id='Q01', set_id='workbook', number=1, unit_id='u1', type='내용', first='s01', last='s09',
  question='다음 글의 내용과 일치하지 않는 것은?',
  choices=['Hunger stones usually stay invisible under the water of rivers.',
           'The stones become noticeable when water levels drop in dry times.',
           'The stones are important because they carry records of past droughts.',
           'Experts expect the coming drought to cease within a short time.',
           'Without significant action, most people in the world could suffer from drought by 2050.'],
  answer=4,
  uses=[('u1-r1a', 1, 'invisible', 'visible의 반의어 invisible(보이지 않는)의 뜻을 알아야 돌이 보통 물속에 잠겨 있다는 본문 내용과 비교할 수 있음'),
        ('u1-r1s', 2, 'noticeable', 'visible과 같은 뜻의 noticeable(눈에 띄는)을 알아야 수위가 내려가면 돌이 보이게 된다는 본문 내용과 연결할 수 있음'),
        ('u1-r2s', 3, 'important', 'significant와 같은 뜻의 important(중요한)를 알아야 “The stones are significant because …”와 같은 내용임을 판단할 수 있음'),
        ('u1-r3a', 4, 'cease', 'persist의 반의어 cease(그치다)의 뜻을 알아야 가뭄이 수십 년 지속될 수 있다는 본문과 반대임을 판단할 수 있음'),
        ('u1-r2h', 5, 'significant', 'significant(중요한, 의미 있는)의 뜻을 알아야 상당한 조치가 없으면 피해가 생긴다는 선지를 해석할 수 있음')],
  evidence='experts warn that the situation we face is not just a simple, occasional drought but a severe drought that could persist for decades.',
  explanation='전문가들은 우리가 마주한 상황이 단순하고 이따금 있는 가뭄이 아니라 수십 년 동안 지속될 수 있는 심각한 가뭄이라고 경고한다. 따라서 다가올 가뭄이 짧은 기간 안에 그칠 것으로 예상한다는 ④는 글의 내용과 일치하지 않는다.',
  choices_ko=['기아석은 보통 강물 속에서 보이지 않는 채로 있다.',
              '그 돌들은 건조한 시기에 수위가 내려가면 눈에 띄게 된다.',
              '그 돌들은 과거 가뭄의 기록을 담고 있기 때문에 중요하다.',
              '전문가들은 다가올 가뭄이 짧은 기간 안에 그칠 것으로 예상한다.',
              '상당한 조치가 없으면 2050년까지 세계 대부분의 사람들이 가뭄으로 고통받을 수 있다.'],
  wrong={1: '“The hunger stones … typically remain underwater.”와 일치한다.',
         2: '“when droughts occur and water levels retreat, these stones become visible”과 일치한다.',
         3: '“The stones are significant because they bear records of the past severe droughts.”와 일치한다.',
         5: '2050년까지 세계 인구의 75퍼센트가 가뭄의 영향으로 고통받을 수 있다고 했고, 상당한 조치가 취해지지 않는다면(unless significant action is taken)이라는 조건과도 일치한다.'})


# ================================================================ 미니 모의고사 1회
q(id='Q02', set_id='mock1', number=1, type='내용', first='s01', last='s06',
  question='다음 글의 내용과 일치하는 것은?',
  choices=['The hunger stone in the Czech town was found in the spring of 2022.',
           'The drought in Europe in 2022 was the worst one in 50 years.',
           'Droughts can bring smaller harvests and a lack of food.',
           'Hunger stones can be found only along the Elbe River.',
           'The poor are the least affected by droughts.'],
  answer=3,
  evidence='Droughts cause reduced harvests, food shortages, and hunger, especially for the poor.',
  explanation='가뭄은 수확량 감소, 식량 부족, 굶주림을 일으킨다고 했다. 따라서 가뭄이 더 적은 수확과 식량 부족을 가져올 수 있다는 ③이 글의 내용과 일치한다.',
  choices_ko=['체코 마을의 기아석은 2022년 봄에 발견되었다.',
              '2022년 유럽의 가뭄은 50년 만의 최악의 가뭄이었다.',
              '가뭄은 더 적은 수확과 식량 부족을 가져올 수 있다.',
              '기아석은 엘베강을 따라서만 발견될 수 있다.',
              '가난한 사람들이 가뭄의 영향을 가장 적게 받는다.'],
  wrong={1: '“In the summer of 2022”라고 했으므로 봄이 아니라 여름이다.',
         2: '“the worst drought in 500 years”라고 했으므로 50년이 아니라 500년 만의 최악이다.',
         4: '“found in rivers across central Europe”라고 했으므로 엘베강에서만 발견되는 것이 아니다.',
         5: '“especially for the poor”라고 했으므로 가난한 사람들이 특히 큰 영향을 받는다.'})

q(id='Q03', set_id='mock1', number=2, type='함축 의미', first='s01', last='s07',
  target='If you see me, then cry.',
  question='밑줄 친 “If you see me, then cry.”가 다음 글에서 의미하는 바로 가장 적절한 것은?',
  choices=['The stone was placed in the river to remember people who died in floods.',
           'When this stone can be seen, a drought is bringing hunger and hard times.',
           'People should feel sad because the old stone has been damaged by water.',
           'Anyone who finds the stone should return it to the river at once.',
           'The stone marks the place where people used to say goodbye to each other.'],
  answer=2,
  evidence='However, when droughts occur and water levels retreat, these stones become visible.',
  explanation='기아석은 보통 물속에 있다가 가뭄이 들어 수위가 내려가야 보이게 되고, 가뭄은 수확 감소·식량 부족·굶주림을 일으키며, 돌의 글은 이런 고난을 경고한다고 믿어진다. 따라서 “나를 보면 울어라”는 이 돌이 보인다면 가뭄으로 굶주림과 힘든 시기가 오고 있다는 뜻이다.',
  choices_ko=['그 돌은 홍수로 죽은 사람들을 기억하기 위해 강에 놓였다.',
              '이 돌이 보일 때는 가뭄이 굶주림과 힘든 시기를 가져오고 있다.',
              '오래된 돌이 물에 의해 손상되었기 때문에 사람들은 슬퍼해야 한다.',
              '그 돌을 발견하는 사람은 누구든 즉시 그것을 강에 돌려놓아야 한다.',
              '그 돌은 사람들이 서로 작별 인사를 하던 장소를 표시한다.'],
  wrong={1: '홍수가 아니라 가뭄과 관련된 돌이며, 죽은 사람들을 기억한다는 내용은 없다.',
         3: '돌이 물에 의해 손상되었다는 내용은 없고, 울어야 하는 이유는 가뭄이 가져올 고난이다.',
         4: '돌을 강에 돌려놓으라는 내용은 없다.',
         5: '작별 인사를 하던 장소라는 내용은 없다.'})

# 요지는 s03~s07(69단어)이 고1 표본의 절반 수준이라, 발견 이야기(s01~s02)까지 포함한 s01~s07(116단어)로 둔다.
q(id='Q04', set_id='mock1', number=3, type='요지', first='s01', last='s07',
  question='다음 글의 요지로 가장 적절한 것은?',
  choices=['Hunger stones were used to mark the best fishing spots in rivers.',
           'People carved words on stones to celebrate good harvests.',
           'Droughts in central Europe have always been short and mild.',
           'Rivers in central Europe rarely change their water levels.',
           'Hunger stones remind people of past hardships and warn them to prepare.'],
  answer=5,
  evidence='The stones are significant because they bear records of the past severe droughts.',
  explanation='기아석은 과거의 심각한 가뭄 기록을 담고 있어 중요하며, 돌의 글은 가뭄이 가져오는 고난을 경고하고 사람들에게 대비하라고 촉구한다고 믿어진다. 따라서 ⑤가 요지다.',
  choices_ko=['기아석은 강에서 가장 좋은 낚시 장소를 표시하는 데 쓰였다.',
              '사람들은 좋은 수확을 축하하기 위해 돌에 글을 새겼다.',
              '중부 유럽의 가뭄은 언제나 짧고 가벼웠다.',
              '중부 유럽의 강들은 수위가 거의 변하지 않는다.',
              '기아석은 사람들에게 과거의 고난을 떠올리게 하고 대비하라고 경고한다.'],
  wrong={1: '낚시 장소를 표시했다는 내용은 없고, 가뭄 때 드러나 과거 가뭄을 기록한 돌이다.',
         2: '돌의 글은 좋은 수확이 아니라 가뭄으로 인한 고난을 경고한다.',
         3: '돌에는 과거의 심각한(severe) 가뭄 기록이 남아 있다고 했으므로 반대다.',
         4: '가뭄이 들면 수위가 내려가(water levels retreat) 돌이 보인다고 했으므로 반대다. 2022년 가뭄 때 엘베강에서 돌이 발견된 것도 수위가 변한 예다.'})

# 공유 장문(Q05 제목·Q06 어휘): 전체 원문 s01~s09
q(id='Q05', set_id='mock1', number=4, type='제목', first='s01', last='s09', group='G1',
  question='윗글의 제목으로 가장 적절한 것은?',
  choices=['Hunger Stones: Old Warnings for a Drier Future',
           'How to Find Stones Hidden Under Rivers',
           'Why Europe’s Rivers Are Getting Deeper',
           'The Czech Town That Became Famous for Crying',
           'Farming Methods That Prevent Food Shortages'],
  answer=1,
  evidence='The words on the hunger stones are believed to warn of these hardships and to urge people to be prepared.',
  explanation='가뭄 때 드러나는 기아석은 과거 가뭄의 기록이자 고난에 대비하라는 경고이고, 전문가와 유엔은 기후 변화로 심각한 가뭄이 오래 지속될 수 있다고 경고한다. 따라서 옛 경고가 더 건조해질 미래에도 의미가 있다는 ①이 제목으로 가장 적절하다.',
  choices_ko=['기아석: 더 건조한 미래를 위한 옛 경고',
              '강 아래 숨겨진 돌을 찾는 방법',
              '유럽의 강들이 더 깊어지고 있는 이유',
              '울음으로 유명해진 체코 마을',
              '식량 부족을 막는 농사 방법'],
  wrong={2: '돌을 찾는 방법은 다루지 않는다.',
         3: '가뭄 때 수위가 내려간다(water levels retreat)고 했으므로 강이 깊어진다는 것은 반대다.',
         4: '체코 마을은 기아석이 발견된 장소로만 나오며, 마을이 유명해진 이야기가 아니다.',
         5: '식량 부족은 가뭄의 결과로 언급될 뿐, 그것을 막는 농사 방법은 나오지 않는다.'})

q(id='Q06', set_id='mock1', number=5, type='어휘', first='s01', last='s09', group='G1',
  marks=[('visible', 's04'), ('significant', 's05'), ('warn', 's07'), ('severe', 's08'), ('address', 's09')],
  replace=('severe', 'mild'),
  question='윗글의 밑줄 친 부분 중, 문맥상 낱말의 쓰임이 적절하지 않은 것은?',
  answer=4,
  evidence='experts warn that the situation we face is not just a simple, occasional drought but a severe drought that could persist for decades.',
  explanation='not just A but B 구조로 단순하고 이따금 있는 가뭄(A)보다 더 나쁜 상황(B)을 말하고, 그 가뭄은 수십 년 동안 지속될 수 있다고 한다. 따라서 ④의 mild(가벼운)는 문맥에 맞지 않고 severe(심각한)가 되어야 한다.',
  wrong={1: '가뭄으로 수위가 내려가면 물속에 있던 돌이 보이게(visible) 된다는 흐름에 맞다.',
         2: '과거 가뭄의 기록을 담고 있어 중요하다(significant)는 뜻으로 적절하다.',
         3: '돌의 글이 가뭄이 가져오는 고난을 경고한다(warn)는 뜻으로 적절하다.',
         5: '기후 변화에 대처하기(address) 위해 상당한 조치가 취해져야 한다는 뜻으로 적절하다.'})


def _bounds(source):
    return {s['id']: s for s in source['sentences']}


def attach(data):
    src = data['sources'][0]
    B = _bounds(src)
    text = src['text']
    questions, quick, exps, plan, requests, groups = [], [], [], [], [], {}
    for row in Q:
        a, z = B[row['first']]['start'], B[row['last']]['end']
        original = text[a:z]
        kind = row['type']
        req = {'id': row['id'], 'type': kind, 'source_id': 'src',
               'first_sentence': row['first'], 'last_sentence': row['last']}
        rel = lambda sid: B[sid]['start'] - a  # noqa: E731
        if kind == '빈칸':
            s = original.index(row['blank'])
            req['replacement_span'] = [s, s + len(row['blank'])]
        elif kind == '함축 의미':
            s = original.index(row['target'])
            req['target_span'] = [s, s + len(row['target'])]
        elif kind == '어휘':
            marks = []
            for word, sid in row['marks']:
                base = rel(sid)
                m = re.compile(r'(?<![A-Za-z])' + re.escape(word) + r'(?![A-Za-z])').search(original, base)
                marks.append([m.start(), m.end()])
            req['vocabulary_marks'] = marks
            old, new = row['replace']
            idx = [w for w, _ in row['marks']].index(old)
            req['replacement_span'] = marks[idx]
            req['replacement'] = new
        elif kind == '삽입':
            req['given_sentence'] = row['given']
            req['insertion_slots'] = [rel(s) for s in row['slots']]
        elif kind == '순서':
            req['block_spans'] = _order_spans(row, B, a, len(original))
        elif kind == '무관한 문장':
            req['addition_offset'] = rel(row['add_before'])
            req['addition'] = row['addition']
            req['sentence_marks'] = row['marks']
        grouped = 'group' in row
        bench_type = 'long41_42' if grouped else kind
        probe = dict(req, length_review={'profile_id': LENGTH_PROFILE_ID, 'grade': GRADE,
                                         'benchmark_ids': recommended_benchmarks(GRADE, bench_type),
                                         'rationale': 'probe', 'independent_review_required': True})
        view = build_view(src, probe, expected_grade=GRADE, benchmark_type=bench_type)
        lc = view['length_comparison']
        refs = lc['reference_words']
        short = lc['shorter_than_all_references']
        rationale = (f"{'공유 장문 41~42' if grouped else kind} 고1 표본 {refs}단어와 비교해 현재 {lc['assessment_word_count']}단어. "
                     + (BENCH_SHORT_NOTE if short else '표본 범위 이상으로 너무 짧지 않음. ')
                     + '연속 원문 범위 안에서 정답과 네 오답의 근거가 자족적임.')
        req['length_review'] = {'profile_id': LENGTH_PROFILE_ID, 'grade': GRADE,
                                'benchmark_ids': recommended_benchmarks(GRADE, bench_type), 'rationale': rationale}
        if short:
            req['length_review']['independent_review_required'] = True
        view = build_view(src, req, expected_grade=GRADE, benchmark_type=bench_type)
        requests.append(req)
        identity = {'id': row['id'], 'set_id': row['set_id'], 'number': row['number']}
        p = dict(identity)
        if row['set_id'] == 'workbook':
            p['unit_id'] = row['unit_id']
        plan.append(p)
        qrow = dict(identity, type=kind, question=row['question'], answer=row['answer'])
        if kind in {'삽입', '무관한 문장', '어휘'}:
            qrow['choice_mode'] = 'in_passage'
            choices = [{'number': n, 'text': CIRCLED[n - 1]} for n in range(1, 6)]
        elif kind == '순서':
            qrow['choice_mode'] = 'order'
            qrow['permutations'] = ORDER
            choices = [{'number': n + 1, 'text': ' → '.join(p_)} for n, p_ in enumerate(ORDER)]
        else:
            qrow['choice_mode'] = 'text'
            choices = [{'number': n + 1, 'text': t} for n, t in enumerate(row['choices'])]
        qrow['choices'] = choices
        for field in ['passage', 'given', 'blocks', 'target']:
            if field in view and view[field] is not None:
                qrow[field] = view[field]
        if kind == '순서':
            qrow.pop('passage', None)
        if kind == '요약':
            qrow['summary'] = row['summary']
        if kind == '함축 의미':
            s = row['question'].index(row['target'])
            qrow['prompt_underlines'] = [[s, s + len(row['target'])]]
        if 'answer' in view:
            assert view['answer'] == row['answer'], (row['id'], view['answer'], row['answer'])
        if kind == '순서':
            assert ORDER[row['answer'] - 1] == view['correct_order'], (row['id'], view['correct_order'])
        if grouped:
            gid = 'long-' + row['set_id']
            qrow['passage_group_id'] = gid
            groups.setdefault(gid, {'id': gid, 'kind': 'long_reading', 'set_id': row['set_id'], 'question_ids': []})
            groups[gid]['question_ids'].append(row['id'])
            if kind == '어휘':
                groups[gid]['passage_question_id'] = row['id']
        if row['set_id'] == 'workbook':
            uses = []
            for term, num, surface, reason in row['uses']:
                ctext = row['choices'][num - 1]
                s = ctext.index(surface)
                uses.append({'term_id': term, 'choice_number': num, 'choice_span': [s, s + len(surface)],
                             'surface': surface, 'reason_ko': reason})
            qrow['learned_relation_uses'] = uses
        questions.append(qrow)
        quick.append(dict(identity, answer=row['answer']))
        exp = dict(identity, choices=[dict(c) for c in choices], answer=row['answer'],
                   evidence=row['evidence'], explanation=row['explanation'],
                   wrong_reasons=[{'number': n, 'text': t} for n, t in sorted(row['wrong'].items())])
        if qrow['choice_mode'] == 'text':
            exp['choices_ko'] = [{'number': n + 1, 'text': t} for n, t in enumerate(row['choices_ko'])]
        else:
            exp['choices_ko'] = []
        exps.append(exp)
    data['assessment'] = {
        'scope': {'kind': 'custom', 'course': data['metadata']['course'], 'unit_ids': [u['id'] for u in data['units']],
                  'instruction': INSTRUCTION},
        'plan': plan, 'questions': questions, 'quick_key': quick, 'explanations': exps,
        'passage_groups': list(groups.values()),
    }
    data['question_sources'] = requests
    return data


def _order_spans(row, B, a, total):
    g0, g1, blocks = row['blocks']
    starts = {k: B[v[0]]['start'] - a for k, v in blocks.items()}
    ordered = sorted(starts.items(), key=lambda kv: kv[1])
    spans = {'given': [0, ordered[0][1]]}
    for i, (k, s) in enumerate(ordered):
        e = ordered[i + 1][1] if i + 1 < len(ordered) else total
        spans[k] = [s, e]
    return spans
