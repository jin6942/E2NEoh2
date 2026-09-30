"""Further Reading 워크북 실전문제(Q01)와 미니 모의고사 1회(Q02~Q04) 원고: 공통영어2 YBM(박준언) 1과 Further Reading.

조립 코드는 1과 본문 assessment_data.py와 같다(고1 공식 표본 grade=1).
사용자 선택(2026-09-29 “워크북 1 + 모의 1회 3문항”): 장문 없이 앞·뒤 반 지문을 쓴다.
회차 편성: 1회 1번 순서는 앞 반 s01~s04(주어진 글 s01)만, 2번 함축·3번 요약은 뒤 반 s05~s09.
4단계 M·N 지적 반영: 2번 함축 표적을 this trap에서 s09 it doesn’t always mean that it is true로 교체(1번 순서 지문 s04가 this trap의 뜻을 알려 주던 문제),
3번 요약은 요약문에서 and divide society를 빼고 수능형 고른 분포 선택지로(2026-09-29 사용자 선택), 2·3번 같은 지문 반복은 유지(사용자 선택).
순서 문항의 문장 배열이 같은 회 다른 지문에 원래 순서로 드러나지 않게 하고, 함축·요약은 내용 판단 유형이라 같은 지문을 써도 답이 새지 않는다.
단문(82·90단어)은 사용자 기준(100단어 안팎 허용)에 따른다.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / '작업_공통영어2_1과' / '스킬수정본' / 'gyogwaseo-unified' / 'scripts'))
from question_source import build_view, recommended_benchmarks, LENGTH_PROFILE_ID  # noqa: E402

CIRCLED = '①②③④⑤'
ORDER = [['A', 'C', 'B'], ['B', 'A', 'C'], ['B', 'C', 'A'], ['C', 'A', 'B'], ['C', 'B', 'A']]
BENCH_SHORT_NOTE = '동일 유형 공식 표본보다 짧아 독립 검수에서 분량·정보 전개를 확인해야 함(사용자 기준: 단문 100단어 안팎 허용). '

Q = []  # 작성 순서 = 출력 순서


def q(**kw):
    Q.append(kw)


# ================================================================ 워크북 실전문제
q(id='Q01', set_id='workbook', number=1, unit_id='u1', type='요지', first='s01', last='s09',
  question='다음 글의 요지로 가장 적절한 것은?',
  choices=['An echo chamber originally refers to an enclosed space where sound returns as an echo.',
           'To avoid an echo chamber, we should look for various views and stay open to new ideas.',
           'Governments should restrict the spread of opinions on social media.',
           'Social media has expanded the ways in which people can access the news.',
           'People should be encouraged to share their opinions freely on social media.'],
  answer=2,
  # 2026-09-30 검수 반영 A6: 오답 ①④⑤가 모두 본문과 정반대 진술이라 지문 없이 ②가 골라지던 문제로 ①④⑤ 교체(②③ 유지).
  uses=[('u1-r3s', 2, 'various', 'various가 diverse(다양한)와 같은 뜻임을 알아야 필자의 요지를 판단할 수 있음'),
        ('u1-r1s', 3, 'restrict', 'restrict(제한하다)의 뜻을 알아야 정부가 의견 확산을 막아야 한다는 말이 본문에 없음을 판단할 수 있음'),
        ('u1-r1a', 4, 'expanded', 'expand(넓히다)의 뜻을 알아야 뉴스 접근 방법이 넓어졌다는 말이 본문에 없고 요지도 아님을 판단할 수 있음'),
        ('u1-r2s', 5, 'encouraged', 'encourage(장려하다)의 뜻을 알아야 의견을 자유롭게 나누도록 장려하라는 말이 본문에 없음을 판단할 수 있음')],
  evidence='To avoid falling into this trap, you must actively seek diverse sources of information and engage with people who have different views. / Always remember to check the information you receive, and keep an open mind when discussing new ideas.',
  explanation='글은 자신이 동의하는 의견만 듣는 에코 챔버가 현실 이해를 왜곡하고 사회적 분열을 조장할 수 있다고 설명한 뒤, 이를 피하려면 다양한 정보 출처와 다른 견해를 적극적으로 접하고 열린 마음을 유지하라고 한다. 따라서 ②가 요지다.',
  choices_ko=['에코 챔버는 원래 소리가 메아리로 되돌아오는 밀폐된 공간을 가리킨다.',
              '에코 챔버를 피하려면 다양한 견해를 찾고 새로운 생각에 열려 있어야 한다.',
              '정부는 소셜 미디어에서 의견이 퍼지는 것을 제한해야 한다.',
              '소셜 미디어는 사람들이 뉴스를 접하는 방법을 넓혔다.',
              '사람들이 소셜 미디어에서 자유롭게 의견을 나누도록 장려해야 한다.'],
  wrong={1: '본문에 나온 사실이지만 용어의 뜻풀이일 뿐, 글이 말하려는 중심 내용이 아니다.',
         3: '정부가 의견의 확산을 제한해야 한다는 내용은 본문에 없다.',
         4: '본문은 사람들이 인터넷과 소셜 미디어로 뉴스를 접한다고 했을 뿐, 뉴스 접근 방법이 넓어졌다는 내용은 없고 요지도 아니다.',
         5: '의견을 자유롭게 나누도록 장려하라는 내용은 본문에 없다. 글은 다양한 견해를 찾으라고 했다.'})


# ================================================================ 미니 모의고사 1회
q(id='Q02', set_id='mock1', number=1, type='순서', first='s01', last='s04',
  blocks=('s01', 's01', {'B': ('s02', 's02'), 'C': ('s03', 's03'), 'A': ('s04', 's04')}),
  question='주어진 글 다음에 이어질 글의 순서로 가장 적절한 것은?',
  answer=3,
  evidence='(B) However, … can lead you to be trapped in an “echo chamber.” / (C) An echo chamber refers to an enclosed space … / (A) The term “echo chamber” is also used to describe …',
  explanation='주어진 글은 요즘 사람들이 자신의 취향이나 신념에 맞는 정보만 골라 받아들인다고 말한다. (B) However로 이어 비슷한 관점만 접하면 ‘에코 챔버’에 갇힐 수 있다며 이 용어를 처음 꺼낸다. (C) 에코 챔버가 원래 소리가 새지 않고 메아리로 돌아오는 밀폐된 공간이라고 뜻을 풀이한다. (A) 이 용어가 also(또한) 이미 동의하는 의견만 듣는 상황에도 쓰인다고 뜻을 넓힌다. 따라서 (B)-(C)-(A)이다.',
  wrong={1: '(A)의 also(또한)는 에코 챔버의 원래 뜻을 먼저 말한 (C) 뒤라야 쓸 수 있고, 용어를 처음 꺼내는 (B)보다 앞설 수도 없다.',
         2: '(A)의 also는 에코 챔버의 원래 뜻을 설명하는 (C)보다 앞에 올 수 없다.',
         4: '(C)가 주어진 글 바로 뒤에서 에코 챔버를 설명하면, 아직 그 용어가 나오지 않았는데 뜻부터 풀이하게 되고 (B)의 However도 흐름이 어색해진다.',
         5: '(C)의 뜻풀이가 용어를 꺼내는 (B)보다 먼저 나오고, (A)의 also가 받아야 할 (C)와 (A) 사이에 (B)가 끼어 연결이 끊긴다.'})

q(id='Q03', set_id='mock1', number=2, type='함축 의미', first='s05', last='s09',
  # 2026-09-30 검수 반영 A5: 이전 밑줄 it doesn’t always mean that it is true는 그 문장만 읽어도 답이 골라져,
  # 문맥이 있어야 풀리는 s07 falling into this trap으로 옮김(지문·정답 번호 ① 유지).
  target='falling into this trap',
  question='밑줄 친 falling into this trap이 다음 글에서 의미하는 바로 가장 적절한 것은?',
  choices=['being surrounded only by views similar to your own',
           'believing every piece of information you find online',
           'arguing with people whose opinions differ from yours',
           'losing interest in social issues that affect everyone',
           'spreading false news without checking the facts'],
  answer=1,
  evidence='Worse still, an echo chamber may foster social division, making collaboration on common issues challenging. / To avoid falling into this trap, you must actively seek diverse sources of information and engage with people who have different views.',
  explanation='밑줄 친 ‘이 함정에 빠지는 것’은 바로 앞 문장에서 사회적 분열까지 일으킨다고 한 에코 챔버에 갇히는 것을 가리킨다. 이를 피하려면 다양한 정보 출처를 찾고 다른 견해를 가진 사람들과 교류하라고 했으므로, 함정은 그 반대 상태, 곧 자신과 비슷한 견해에만 둘러싸이는 것이다. 따라서 ①이 알맞다.',
  choices_ko=['자신과 비슷한 견해에만 둘러싸이는 것',
              '온라인에서 찾은 모든 정보를 믿는 것',
              '자신과 의견이 다른 사람들과 다투는 것',
              '모두에게 영향을 미치는 사회 문제에 관심을 잃는 것',
              '사실을 확인하지 않고 거짓 뉴스를 퍼뜨리는 것'],
  wrong={2: '받은 정보를 확인하라는 말은 있지만, 글이 말하는 함정은 온라인 정보를 다 믿는 것이 아니라 에코 챔버에 갇히는 것이다.',
         3: '다른 견해를 가진 사람들과 교류하라고 했을 뿐, 그들과 다투는 것을 함정이라고 하지 않았다.',
         4: '에코 챔버가 공통 문제에 대한 협력을 어렵게 만든다고 했을 뿐, 사회 문제에 관심을 잃는 것이 함정은 아니다.',
         5: '거짓 뉴스를 퍼뜨리는 내용은 본문에 없다.'})

q(id='Q04', set_id='mock1', number=3, type='요약', first='s05', last='s09',
  summary='An echo chamber can (A) ________ our understanding of reality, so we need to (B) ________ diverse information and different views.',
  question='다음 글의 내용을 한 문장으로 요약하고자 한다. 빈칸 (A), (B)에 들어갈 말로 가장 적절한 것은?',
  choices=['improve …… seek out',
           'twist …… avoid',
           'sharpen …… limit',
           'twist …… seek out',
           'sharpen …… avoid'],
  answer=4,
  evidence='This can distort your understanding of reality … / … you must actively seek diverse sources of information and engage with people who have different views.',
  explanation='에코 챔버는 현실에 대한 이해를 왜곡할(distort) 수 있으므로, 다양한 정보와 다른 견해를 적극적으로 찾아야(seek) 한다. 따라서 (A) twist(왜곡하다), (B) seek out(찾아 나서다)인 ④가 알맞다.',
  choices_ko=['향상시키다 …… 찾아 나서다', '왜곡하다 …… 피하다', '날카롭게 하다 …… 제한하다',
              '왜곡하다 …… 찾아 나서다', '날카롭게 하다 …… 피하다'],
  wrong={1: '(B)는 맞지만, 에코 챔버는 현실에 대한 이해를 향상시키는 것이 아니라 왜곡할 수 있다고 했다.',
         2: '(A)는 맞지만, 다양한 정보와 다른 견해를 피하는 것이 아니라 적극적으로 찾으라고 했다.',
         3: '에코 챔버는 현실에 대한 이해를 날카롭게 하는 것이 아니라 왜곡할 수 있다고 했고, 다양한 정보는 제한하는 것이 아니라 찾아야 한다고 했다.',
         5: '에코 챔버는 이해를 날카롭게 하지 않고 왜곡할 수 있다고 했으며, 다양한 정보와 다른 견해는 피하지 말고 찾아야 한다고 했다.'})


# ================================================================ 조립
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
        probe = dict(req, length_review={'profile_id': LENGTH_PROFILE_ID, 'grade': 1,
                                         'benchmark_ids': recommended_benchmarks(1, bench_type),
                                         'rationale': 'probe', 'independent_review_required': True})
        view = build_view(src, probe, expected_grade=1, benchmark_type=bench_type)
        lc = view['length_comparison']
        refs = lc['reference_words']
        short = lc['shorter_than_all_references']
        rationale = (f"{'공유 장문 41~42' if grouped else kind} 고1 표본 {refs}단어와 비교해 현재 {lc['assessment_word_count']}단어. "
                     + (BENCH_SHORT_NOTE if short else '표본 범위 이상으로 너무 짧지 않음. ')
                     + '연속 원문 범위 안에서 정답과 네 오답의 근거가 자족적임.')
        req['length_review'] = {'profile_id': LENGTH_PROFILE_ID, 'grade': 1,
                                'benchmark_ids': recommended_benchmarks(1, bench_type), 'rationale': rationale}
        if short:
            req['length_review']['independent_review_required'] = True
        view = build_view(src, req, expected_grade=1, benchmark_type=bench_type)
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
                  'instruction': ('2026-09-29 사용자 선택 “워크북 1 + 모의 1회 3문항”: 172단어 Further Reading에 맞춰 공통 단위 워크북 실전문제 1문항 + '
                                  '미니 모의고사 1회 3문항(공유 장문 없음, 앞·뒤 반 지문). 단문 100단어 안팎 허용(2026-09-28 사용자 기준), '
                                  '문제 오류·지문 밖 정답 단서는 불가. 4단계 뒤 사용자 결정: 1회 2번 함축·3번 요약은 같은 지문(s05~s09)을 각각 싣는 것을 유지, '
                                  '3번 요약 선택지는 모든 오답을 반쪽 정답으로 두지 않고 낱말별 빈도를 2·2·1로 고르게 한 수능형 분포(빈도 단서 방지).')},
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
