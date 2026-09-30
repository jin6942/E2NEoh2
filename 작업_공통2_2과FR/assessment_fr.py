"""워크북 실전문제(Q01)와 미니 모의고사 1회(Q02~Q06) 원고 — 공통영어2 YBM(박준언) 2과 Further Reading.

지문·정답 위치는 원문에서 계산하고 question_source.build_view로 복원을 검증한다.
조립 코드는 같은 과 본책의 작업_공통2_2과/assessment_data.py와 같다(고1 grade 1 분량 비교).

회차 편성 원칙: 공유 장문(Q05·Q06)이 전체 지문 s01~s09이므로, 같은 회의 일반 3문항은 원문을 보면
답이 드러나는 빈칸·순서·삽입·무관 유형을 쓰지 않고 내용·함축·요약으로 편성한다.
어휘 문항의 밑줄 5개(바꾼 표적 s08 persist 포함)는 일반 3문항 지문(모두 s01~s07 안)에 나오지 않는 s08~s09에만 둔다.
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

MOCK_LENGTH_NOTE = (' 원문 전체가 175단어라, 회차 안 지문 범위를 서로 다르게 하고 어휘 문항 밑줄이 다른 지문에 드러나지 않도록 '
                    '짧게 발췌함. 4단계 M·N 독립 검수에서 근거가 지문 안에서 해결되어 수용 가능함을 확인.')

LONG_LENGTH_NOTE = (' 공유 장문은 원문 전체(175단어)를 그대로 쓰며 더 늘릴 원문이 없음. '
                    '4단계 M·N 독립 검수에서 문항 성립과 근거 자족을 확인.')

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
           'Without action on climate change, most people in the world could suffer from drought by 2050.'],
  answer=4,
  uses=[('u1-r1a', 1, 'invisible', 'visible의 반의어 invisible(보이지 않는)의 뜻을 알아야 돌이 보통 물속에 잠겨 있다는 본문 내용과 비교할 수 있음'),
        ('u1-r1s', 2, 'noticeable', 'visible과 같은 뜻의 noticeable(눈에 띄는)을 알아야 수위가 내려가면 돌이 보이게 된다는 본문 내용과 연결할 수 있음'),
        ('u1-r2s', 3, 'important', 'significant와 같은 뜻의 important(중요한)를 알아야 “The stones are significant because …”와 같은 내용임을 판단할 수 있음'),
        ('u1-r3a', 4, 'cease', 'persist의 반의어 cease(그치다)의 뜻을 알아야 가뭄이 수십 년 지속될 수 있다는 본문과 반대임을 판단할 수 있음')],
  evidence='experts warn that the situation we face is not just a simple, occasional drought but a severe drought that could persist for decades.',
  explanation='전문가들은 우리가 마주한 상황이 단순하고 이따금 있는 가뭄이 아니라 수십 년 동안 지속될 수 있는 심각한 가뭄이라고 경고한다. 따라서 다가올 가뭄이 짧은 기간 안에 그칠 것으로 예상한다는 ④는 글의 내용과 일치하지 않는다.',
  choices_ko=['기아석은 보통 강물 속에서 보이지 않는 채로 있다.',
              '그 돌들은 건조한 시기에 수위가 내려가면 눈에 띄게 된다.',
              '그 돌들은 과거 가뭄의 기록을 담고 있기 때문에 중요하다.',
              '전문가들은 다가올 가뭄이 짧은 기간 안에 그칠 것으로 예상한다.',
              '기후 변화에 대한 조치가 없으면 2050년까지 세계 대부분의 사람들이 가뭄으로 고통받을 수 있다.'],
  wrong={1: '“The hunger stones … typically remain underwater.”와 일치한다.',
         2: '“when droughts occur and water levels retreat, these stones become visible”과 일치한다.',
         3: '“The stones are significant because they bear records of the past severe droughts.”와 일치한다.',
         5: '2050년까지 세계 인구의 75퍼센트(4명 중 3명, 즉 대부분)가 가뭄의 영향으로 고통받을 수 있다고 했고, 기후 변화에 대처하는 상당한 조치가 취해지지 않는다면(unless significant action is taken to address climate change)이라는 조건과도 일치한다.'})


# ================================================================ 미니 모의고사 1회
# 4단계 M·N 블라인드 의견 반영(2026-09-29): ① 일반 3문항 지문을 s01~s05 / s01~s06 / s01~s07로 서로 다르게 두고,
# ② 어휘 문항 밑줄 5개를 일반 3문항 지문 밖(s08~s09)에만 두며, ③ 요지(장문 제목과 답이 겹침)를 요약으로 바꾼다.
q(id='Q02', set_id='mock1', number=1, type='내용', first='s01', last='s05',
  question='다음 글의 내용과 일치하는 것은?',
  choices=['The hunger stone in the Czech town was discovered by scientists studying the river.',
           'The sentence on the stone told people to be happy when they saw it.',
           'Hunger stones in central European rivers can usually be seen above the water.',
           'Hunger stones are important because they record the floods of the past.',
           'Hunger stones appear when the water in rivers goes down during droughts.'],
  answer=5,
  evidence='However, when droughts occur and water levels retreat, these stones become visible.',
  explanation='기아석은 보통 물속에 있다가 가뭄이 들어 수위가 낮아지면 보이게 된다고 했다. 따라서 가뭄 때 강물이 줄어들면 기아석이 드러난다는 ⑤가 글의 내용과 일치한다.',
  choices_ko=['체코 마을의 기아석은 강을 연구하던 과학자들이 발견했다.',
              '돌에 새겨진 문장은 사람들에게 그것을 보면 기뻐하라고 했다.',
              '중부 유럽 강의 기아석은 보통 물 위로 보인다.',
              '기아석은 과거의 홍수를 기록하고 있어서 중요하다.',
              '기아석은 가뭄 동안 강물이 줄어들 때 모습을 드러낸다.'],
  wrong={1: '돌이 체코 마을에서 발견되었다는 내용만 있고, 누가 발견했는지는 나오지 않는다.',
         2: '돌의 문장은 “If you see me, then cry.”(나를 보면 울어라)이므로 기뻐하라는 것이 아니다.',
         3: '“typically remain underwater”라고 했으므로 보통은 물속에 잠겨 있다.',
         4: '기아석은 과거의 심각한 가뭄(droughts) 기록을 담고 있다고 했으며 홍수가 아니다.'})

# 함축 의미는 s07(경고한다는 설명)이 밑줄의 뜻을 바로 풀어 주므로 s01~s06으로 둔다(M·N 의견).
q(id='Q03', set_id='mock1', number=2, type='함축 의미', first='s01', last='s06',
  target='If you see me, then cry.',
  question='밑줄 친 “If you see me, then cry.”가 다음 글에서 의미하는 바로 가장 적절한 것은?',
  choices=['Seeing the stone means that heavy rain and floods are coming soon.',
           'People should be sad because the old stone has been damaged by the river.',
           'Those who find the stone should cry with joy at their lucky discovery.',
           'When this stone can be seen, a drought is bringing hunger and hard times.',
           'The stone warns people not to swim in the river when the water is low.'],
  answer=4,
  evidence='However, when droughts occur and water levels retreat, these stones become visible. / Droughts cause reduced harvests, food shortages, and hunger, especially for the poor.',
  explanation='기아석은 보통 물속에 있다가 가뭄이 들어 수위가 내려가야 보이게 되고, 가뭄은 수확 감소·식량 부족·굶주림을 일으킨다. 따라서 “나를 보면 울어라”는 이 돌이 보인다면 가뭄으로 굶주림과 힘든 시기가 오고 있다는 뜻이다.',
  choices_ko=['그 돌을 보는 것은 곧 폭우와 홍수가 온다는 뜻이다.',
              '오래된 돌이 강물에 손상되었기 때문에 사람들은 슬퍼해야 한다.',
              '그 돌을 발견한 사람들은 운 좋은 발견에 기뻐서 울어야 한다.',
              '이 돌이 보일 때는 가뭄이 굶주림과 힘든 시기를 가져오고 있다.',
              '그 돌은 물이 얕을 때 강에서 수영하지 말라고 경고한다.'],
  wrong={1: '돌은 비가 많을 때가 아니라 가뭄으로 수위가 내려갈 때 보이므로 반대다.',
         2: '돌이 손상되었다는 내용은 없고, 울어야 하는 이유는 가뭄이 가져올 굶주림이다.',
         3: '가뭄이 굶주림을 일으킨다는 흐름이므로 기뻐서 우는 것이 아니라 슬퍼서 우는 것이다.',
         5: '물이 얕아진다는 점은 맞지만, 수영의 위험에 대한 내용은 없고 가뭄으로 인한 굶주림을 말한다.'})

q(id='Q04', set_id='mock1', number=3, type='요약', first='s01', last='s07',
  # J-W 권고: (A)·(B)와 빈칸 사이는 줄바꿈 없는 공백(U+00A0)
  summary='Hunger stones, which can be (A)\u00a0________ only when droughts lower the water in rivers, are believed to (B)\u00a0________ people of the hardships that droughts bring.',
  question='다음 글의 내용을 한 문장으로 요약하고자 한다. 빈칸 (A), (B)에 들어갈 말로 가장 적절한 것은?',
  choices=['hidden …… remind',
           'seen …… remind',
           'seen …… relieve',
           'buried …… assure',
           'hidden …… relieve'],
  answer=2,
  evidence='However, when droughts occur and water levels retreat, these stones become visible. / The words on the hunger stones are believed to warn of these hardships and to urge people to be prepared.',
  explanation='기아석은 가뭄이 들어 수위가 내려갈 때 보이게 되고(visible), 돌의 글은 가뭄이 가져오는 고난을 경고하는(warn of) 것으로 여겨진다. 따라서 (A) seen(보이는), (B) remind(A에게 B를 일깨우다)인 ②가 알맞다.',
  choices_ko=['숨겨진 …… 일깨우다', '보이는 …… 일깨우다', '보이는 …… 덜어 주다', '묻힌 …… 확신시키다', '숨겨진 …… 덜어 주다'],
  wrong={1: '(B) remind는 맞지만, 기아석은 가뭄 때 숨겨지는 것이 아니라 드러나므로(become visible) (A) hidden은 반대다.',
         3: '(A) seen은 맞지만, 돌의 글은 사람들의 고난을 덜어 주는(relieve A of B) 것이 아니라 고난을 경고한다.',
         4: '기아석은 가뭄 때 물 밖으로 드러나므로(become visible) (A) buried(묻힌)는 반대다. (B) assure A of B(A에게 B를 확신시키다·보장하다)도 돌의 글이 고난을 경고하고 대비를 촉구한다는 내용과 맞지 않는다.',
         5: '기아석은 가뭄 때 드러나며(hidden은 반대), 돌의 글은 고난을 덜어 주는 것이 아니라 경고한다.'})

# 공유 장문(Q05 제목·Q06 어휘): 전체 원문 s01~s09
q(id='Q05', set_id='mock1', number=4, type='제목', first='s01', last='s09', group='G1',
  question='윗글의 제목으로 가장 적절한 것은?',
  choices=['Hunger Stones: Old Warnings for a Drier Future',
           'The Hunger Stone: A Rare Find in a Czech Town',
           'How Droughts Helped Europe Grow More Food',
           'Climate Change: Why Rivers Rise Every Summer',
           'Ancient Stones That Predicted Floods in Europe'],
  answer=1,
  evidence='The words on the hunger stones are believed to warn of these hardships and to urge people to be prepared. / The United Nations has predicted that by 2050, 75 percent of the global population could suffer from the effects of drought unless significant action is taken to address climate change.',
  explanation='가뭄 때 드러나는 기아석은 과거 가뭄의 기록이자 고난에 대비하라는 경고이고, 전문가와 유엔은 기후 변화로 심각한 가뭄이 오래 지속될 수 있다고 경고한다. 따라서 옛 경고가 더 건조해질 미래에도 의미가 있다는 ①이 제목으로 가장 적절하다.',
  choices_ko=['기아석: 더 건조한 미래에 대한 옛 경고',
              '기아석: 체코 마을에서의 드문 발견',
              '가뭄이 유럽의 식량 증산을 도운 방법',
              '기후 변화: 강물이 매년 여름 불어나는 이유',
              '유럽의 홍수를 예고한 옛 돌들'],
  wrong={2: '체코 마을에서의 발견은 글을 시작하는 사례일 뿐이고, 글은 기아석의 의미와 앞으로의 가뭄 경고까지 다룬다.',
         3: '가뭄은 수확 감소와 식량 부족을 일으킨다고 했으므로 반대다.',
         4: '가뭄 때 수위가 내려간다(water levels retreat)고 했으므로 강물이 불어난다는 것은 반대다.',
         5: '기아석은 홍수가 아니라 가뭄 때 드러나 가뭄의 고난을 경고한다.'})

q(id='Q06', set_id='mock1', number=5, type='어휘', first='s01', last='s09', group='G1',
  marks=[('continuation', 's08'), ('occasional', 's08'), ('persist', 's08'), ('global', 's09'), ('address', 's09')],
  replace=('persist', 'cease'),
  question='윗글의 밑줄 친 부분 중, 문맥상 낱말의 쓰임이 적절하지 않은 것은?',
  answer=3,
  evidence='experts warn that the situation we face is not just a simple, occasional drought but a severe drought that could cease for decades.',
  explanation='(원문 낱말: persist) not just A but B 구조로 단순하고 이따금 있는 가뭄(A)이 아니라 더 심각한 상황(B)을 말한다. 기후 변화가 계속되는 것을 고려하면 그 심각한 가뭄은 수십 년 동안 지속될(persist) 수 있어야 문맥에 맞다. 따라서 ③의 cease(그치다)는 적절하지 않다.',
  wrong={1: '기후 변화의 계속(continuation)을 고려한다는 뜻으로, 가뭄이 오래갈 것이라는 경고의 근거가 된다.',
         2: '단순하고 이따금 있는(occasional) 가뭄이 아니라는 뜻으로, 뒤의 오래 지속되는 심각한 가뭄과 대조된다.',
         4: '2050년까지 세계(global) 인구의 75퍼센트가 영향을 받을 수 있다는 뜻으로 적절하다.',
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
                     + '연속 원문 범위 안에서 정답과 네 오답의 근거가 자족적임.'
                     + (MOCK_LENGTH_NOTE if row['set_id'] != 'workbook' and not grouped else '')
                     + (LONG_LENGTH_NOTE if grouped else ''))
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
