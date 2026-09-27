"""Further Reading 워크북 실전문제(Q01~Q02)와 미니 모의고사 1회(Q03~Q09) 원고.

지문·정답 위치는 원문에서 계산하고 question_source.build_view로 복원을 검증한다.
조립 코드는 영어2 능률(오) 2과 작업의 assessment_data.py와 같은 방식이다.

회차 편성 원칙: 한 회차 안에서 빈칸·어휘·순서·삽입·무관 문항의 정답 근거가 다른 문항 지문에
원형으로 드러나지 않도록 원문 구간을 나눈다(능률 2과 4단계 M·N 지적에서 얻은 기준).
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / '작업' / '스킬수정본' / 'gyogwaseo-unified' / 'scripts'))
from question_source import build_view, recommended_benchmarks, LENGTH_PROFILE_ID  # noqa: E402

CIRCLED = '①②③④⑤'
ORDER = [['A', 'C', 'B'], ['B', 'A', 'C'], ['B', 'C', 'A'], ['C', 'A', 'B'], ['C', 'B', 'A']]
BENCH_SHORT_NOTE = '동일 유형 공식 표본보다 짧아 독립 검수에서 분량·정보 전개를 확인해야 함. '

Q = []  # 작성 순서 = 출력 순서


def q(**kw):
    Q.append(kw)


# ================================================================ 워크북 실전문제
q(id='Q01', set_id='workbook', number=1, unit_id='u1', type='주제', first='s01', last='s12',
  question='다음 글의 주제로 가장 적절한 것은?',
  choices=['the essential role of shopping in making people happy',
           'why familiar possessions bring more joy than novel ones',
           'critical reasons why the happiness from things does not last long',
           'minor differences between buying cars and buying clothes',
           'the obvious benefits of comparing ourselves with others'],
  answer=3,
  uses=[('u1-r2s', 1, 'essential', 'essential(필수적인)의 뜻을 알아야 쇼핑이 행복에 필수라는 말이 본문 결론과 반대임을 판단할 수 있음'),
        ('u1-r3a', 2, 'familiar', 'novel의 반대인 familiar(익숙한) 물건이 더 큰 기쁨을 준다는 말이 본문에 없음을 판단해야 함'),
        ('u1-r3h', 2, 'novel', 'novel(새로운)의 뜻을 알아야 선지를 해석할 수 있음'),
        ('u1-r2h', 3, 'critical', 'critical(결정적인)의 뜻을 알아야 세 가지 결정적인 이유라는 주제를 판단할 수 있음'),
        ('u1-r2a', 4, 'minor', 'critical의 반대인 minor(사소한) 차이는 본문 내용이 아님을 판단해야 함'),
        ('u1-r1s', 5, 'obvious', 'clear와 같은 뜻의 obvious(명백한) 이점이 본문과 반대임을 판단해야 함')],
  evidence='The trouble with things is that the happiness they provide fades quickly. There are three critical reasons for this.',
  explanation='물건에 돈을 쓰지 말라는 연구 결론을 소개한 뒤, 물건이 주는 행복은 빨리 사라진다고 하고 그 세 가지 결정적인 이유(새 물건에 익숙해짐, 계속 높아지는 기준, 남과의 비교)를 설명한다. 따라서 ③이 주제다.',
  choices_ko=['사람들을 행복하게 하는 데 있어 쇼핑의 필수적인 역할',
              '익숙한 소유물이 새로운 것보다 더 큰 기쁨을 주는 이유',
              '물건에서 얻는 행복이 오래가지 않는 결정적인 이유들',
              '차를 사는 것과 옷을 사는 것의 사소한 차이',
              '자신을 다른 사람과 비교하는 것의 명백한 이점'],
  wrong={1: '물건에 돈을 쓰지 말라는 결론이므로 쇼핑이 행복에 필수적이라는 것은 반대 내용이다.',
         2: '새 물건도 곧 익숙해져 평범해진다고 했을 뿐, 익숙한 물건이 더 큰 기쁨을 준다는 내용은 없다.',
         4: '차는 남과 비교하는 예로 나올 뿐이고 옷과 비교하는 내용은 없다.',
         5: '남과의 비교는 행복을 빨리 사라지게 하는 이유로 제시되었으므로 이점이 아니다.'})

q(id='Q02', set_id='workbook', number=2, unit_id='u2', type='요지', first='s10', last='s20',
  question='다음 글의 요지로 가장 적절한 것은?',
  choices=['Physical items are the best way to show who we really are.',
           'Buying a better car than our friends’ brings us enduring joy.',
           'Material goods and experiences give us the same kind of happiness.',
           'Our experiences remain separate from our sense of self.',
           'Experiences give more lasting happiness because they become part of who we are.'],
  answer=5,
  uses=[('u2-r2s', 1, 'Physical', 'material과 같은 뜻의 physical(물질의) 물건이 우리를 보여 준다는 말이 본문과 어긋남을 판단해야 함'),
        ('u2-r1s', 2, 'enduring', 'lasting과 같은 뜻의 enduring(오래가는) 기쁨이 본문의 비교 예와 반대임을 판단해야 함'),
        ('u2-r2h', 3, 'Material', 'material(물질적인)의 뜻을 알아야 물질적 재화와 경험을 같다고 한 선지를 판단할 수 있음'),
        ('u2-r3h', 4, 'separate', 'separate(분리된)의 뜻을 알아야 경험이 우리와 분리된다는 선지가 본문과 반대임을 판단할 수 있음'),
        ('u2-r1h', 5, 'lasting', 'lasting(오래가는)의 뜻을 알아야 경험이 더 오래가는 행복을 준다는 요지를 판단할 수 있음')],
  evidence='Gilovich and other researchers have found that experiences deliver longer lasting happiness than things. That’s because experiences become a part of our identity.',
  explanation='새 물건에 익숙해지면 더 좋은 것을 찾고 남과 비교하게 되지만, 경험은 물건보다 더 오래 지속되는 행복을 주며 그 이유는 경험이 우리 정체성의 일부가 되기 때문이라고 한다. 따라서 ⑤가 요지다.',
  choices_ko=['물질적인 물건은 우리가 진짜 누구인지 보여 주는 가장 좋은 방법이다.',
              '친구의 차보다 더 좋은 차를 사는 것은 우리에게 오래가는 기쁨을 준다.',
              '물질적인 재화와 경험은 우리에게 같은 종류의 행복을 준다.',
              '우리의 경험은 우리 자신이라는 감각과 분리된 채로 남는다.',
              '경험은 우리를 이루는 일부가 되기 때문에 더 오래가는 행복을 준다.'],
  wrong={1: '물건이 정체성과 연결되어 있다고 생각해도 물건은 여전히 우리와 분리되어 있다고 했다.',
         2: '친구가 더 좋은 차를 사면 기쁨이 끝나고, 더 좋은 것을 가진 사람은 언제나 있다고 했으므로 반대다.',
         3: '경험은 물질적 재화보다 우리 자신의 더 큰 부분이며 더 오래가는 행복을 준다고 했으므로 반대다.',
         4: '경험은 정말로 우리의 일부라고 했으므로 반대다.'})


# ================================================================ 미니 모의고사 1회
# 공유 장문(Q08·Q09)이 전체 지문 s01~s20이므로, 같은 회의 일반 5문항은 원문을 보면 답이 드러나는
# 빈칸·순서·삽입·무관 유형을 쓰지 않고 내용·함축·요약·요지·주장으로 편성한다.
# 어휘 문항 표적은 일반 5문항 지문(모두 s01~s15 안)에 나오지 않는 s16~s19에만 둔다.
q(id='Q03', set_id='mock1', number=1, type='내용', first='s01', last='s12',
  question='다음 글의 내용과 일치하지 않는 것은?',
  choices=['Thomas Gilovich’s study was carried out over a long period.',
           'People are usually right to think the joy of buying lasts long.',
           'New things soon stop feeling fresh and thrilling.',
           'Once people are used to what they bought, they look for something better.',
           'Owning things leads people to measure themselves against others.'],
  answer=2,
  evidence='We assume that the happiness we get from buying something will last as long as the thing itself. But it’s wrong.',
  explanation='우리는 무언가를 사서 얻는 행복이 물건만큼 오래갈 것이라고 생각하지만 그것은 틀렸다고 했다. 따라서 그 생각이 대개 옳다고 한 ②는 글의 내용과 일치하지 않는다.',
  choices_ko=['토머스 길로비치의 연구는 오랜 기간에 걸쳐 수행되었다.',
              '사람들이 물건을 사는 기쁨이 오래간다고 생각하는 것은 대개 옳다.',
              '새 물건은 곧 새롭고 신나게 느껴지지 않게 된다.',
              '사람들은 산 물건에 익숙해지면 더 좋은 것을 찾는다.',
              '물건을 소유하는 것은 사람들이 자신을 남과 견주어 보게 만든다.'],
  wrong={1: '“A long-term study conducted by Thomas Gilovich”와 일치한다.',
         3: '“What once seemed novel and exciting quickly becomes the norm.”과 일치한다.',
         4: '“As soon as we get used to a new possession, we look for an even better one.”과 일치한다.',
         5: '“possessions stimulate humans to compare themselves with others”와 일치한다.'})

q(id='Q04', set_id='mock1', number=2, type='함축 의미', first='s01', last='s14',
  target='raising the bar',
  question='밑줄 친 raising the bar가 다음 글에서 의미하는 바로 가장 적절한 것은?',
  choices=['making the prices of new products higher',
           'trying to own fewer things than before',
           'spending more time with friends and family',
           'expecting something better from each new purchase',
           'setting strict rules for saving money'],
  answer=4,
  evidence='Second, we keep raising the bar. New purchases lead to new expectations. As soon as we get used to a new possession, we look for an even better one.',
  explanation='둘째 이유로 새 구매가 새 기대로 이어지고, 새 소유물에 익숙해지자마자 훨씬 더 좋은 것을 찾는다고 했다. 따라서 raising the bar는 새로 살 때마다 더 좋은 것을 기대하게 된다는 뜻이다.',
  choices_ko=['새 제품들의 가격을 더 높게 만드는 것',
              '예전보다 더 적은 물건을 소유하려고 하는 것',
              '친구와 가족과 더 많은 시간을 보내는 것',
              '새로 살 때마다 더 좋은 것을 기대하는 것',
              '돈을 모으기 위한 엄격한 규칙을 정하는 것'],
  wrong={1: '높아지는 기준(bar)은 가격이 아니라 우리가 기대하는 수준이다.',
         2: '물건을 덜 가지려 한다는 내용은 없다.',
         3: '친구·가족과 시간을 보내는 이야기는 나오지 않는다.',
         5: '돈을 모으는 규칙은 나오지 않는다.'})

q(id='Q05', set_id='mock1', number=3, type='요약', first='s02', last='s15',
  summary='The happiness we get from things tends to be (A) ________, while experiences give us more lasting happiness because they become part of our (B) ________.',
  question='다음 글의 내용을 한 문장으로 요약하고자 한다. 빈칸 (A), (B)에 들어갈 말로 가장 적절한 것은?',
  choices=['short-lived …… identity',
           'long-lasting …… identity',
           'short-lived …… wealth',
           'exciting …… possessions',
           'permanent …… memories'],
  answer=1,
  evidence='The trouble with things is that the happiness they provide fades quickly. / That’s because experiences become a part of our identity.',
  explanation='물건이 주는 행복은 새 물건에 익숙해지고, 기준이 높아지고, 남과 비교하게 되어 빨리 사라진다. 반면 경험은 우리 정체성의 일부가 되기 때문에 더 오래가는 행복을 준다. 따라서 (A)에는 short-lived, (B)에는 identity가 알맞다.',
  choices_ko=['오래가지 않는 …… 정체성', '오래 지속되는 …… 정체성', '오래가지 않는 …… 부', '신나는 …… 소유물', '영구적인 …… 기억'],
  wrong={2: '물건이 주는 행복은 빨리 사라진다고 했으므로 (A)의 long-lasting은 반대다.',
         3: '경험은 부(wealth)가 아니라 정체성의 일부가 된다고 했다.',
         4: '새 물건은 곧 평범해진다고 했고, 경험이 소유물의 일부가 된다는 내용도 없다.',
         5: '물건이 주는 행복이 영구적이라는 것은 반대 내용이다.'})

q(id='Q06', set_id='mock1', number=4, type='요지', first='s04', last='s15',
  question='다음 글의 요지로 가장 적절한 것은?',
  choices=['Comparing our possessions with others’ helps us feel satisfied.',
           'New purchases always create deeper happiness than old ones.',
           'Unlike things, experiences bring happiness that lasts because they shape who we are.',
           'We should buy better products to keep our expectations high.',
           'Researchers still cannot explain why experiences make us happy.'],
  answer=3,
  evidence='The trouble with things is that the happiness they provide fades quickly. / Gilovich and other researchers have found that experiences deliver longer lasting happiness than things. That’s because experiences become a part of our identity.',
  explanation='물건이 주는 행복은 세 가지 이유로 빨리 사라지지만, 경험은 우리 정체성의 일부가 되기 때문에 더 오래가는 행복을 준다는 내용이다. 따라서 ③이 요지다.',
  choices_ko=['우리의 소유물을 다른 사람들의 것과 비교하는 것은 우리가 만족감을 느끼도록 돕는다.',
              '새로 산 물건은 항상 오래된 것보다 더 깊은 행복을 만든다.',
              '물건과 달리 경험은 우리를 이루는 부분이 되기 때문에 오래가는 행복을 준다.',
              '우리는 기대를 높게 유지하기 위해 더 좋은 제품을 사야 한다.',
              '연구자들은 경험이 왜 우리를 행복하게 하는지 아직 설명하지 못한다.'],
  wrong={1: '남과의 비교는 물건의 행복이 사라지는 이유로 제시되었다.',
         2: '새 구매는 새 기대로 이어질 뿐이고, 익숙해지면 더 좋은 것을 찾게 된다고 했다.',
         4: '기대가 계속 높아지는 것은 행복이 사라지는 이유로 제시되었다.',
         5: '경험이 오래가는 행복을 주는 이유(정체성의 일부가 됨)를 설명했다.'})

q(id='Q07', set_id='mock1', number=5, type='주장', first='s01', last='s15',
  question='다음 글에서 필자가 주장하는 바로 가장 적절한 것은?',
  choices=['We should buy new things often to keep ourselves excited.',
           'We must stop comparing our cars with our friends’ cars.',
           'We should set higher standards for the products we buy.',
           'We need to save money instead of spending it on anything.',
           'We should spend our money on experiences rather than on things.'],
  answer=5,
  evidence='A long-term study … reached a powerful and clear conclusion: Don’t spend your money on things. / Gilovich and other researchers have found that experiences deliver longer lasting happiness than things.',
  explanation='연구의 결론으로 물건에 돈을 쓰지 말라고 하고, 물건의 행복은 빨리 사라지지만 경험은 더 오래가는 행복을 준다고 했다. 따라서 물건보다 경험에 돈을 쓰라는 ⑤가 필자의 주장이다.',
  choices_ko=['우리는 계속 신나기 위해 새 물건을 자주 사야 한다.',
              '우리는 우리의 차를 친구들의 차와 비교하는 것을 멈춰야 한다.',
              '우리는 사는 제품에 대해 더 높은 기준을 정해야 한다.',
              '우리는 무엇에든 돈을 쓰는 대신 돈을 모아야 한다.',
              '우리는 물건보다 경험에 돈을 써야 한다.'],
  wrong={1: '새 물건은 곧 평범해져 즐거움이 오래가지 않는다고 했으므로 반대다.',
         2: '차 비교는 물건의 행복이 사라지는 셋째 이유의 예일 뿐 필자의 주장이 아니다.',
         3: '기준을 계속 높이는 것은 행복이 사라지는 이유로 제시되었다.',
         4: '돈을 쓰지 말라는 대상은 물건이며, 경험은 더 오래가는 행복을 준다고 했다.'})

q(id='Q08', set_id='mock1', number=6, type='제목', first='s01', last='s20', group='G1',
  question='윗글의 제목으로 가장 적절한 것은?',
  choices=['How to Choose the Best Car for Your Family',
           'Spend on Experiences, Not on Things',
           'Why We Should Always Upgrade Our Possessions',
           'Comparing Yourself with Others: The Key to Joy',
           'The Science of Saving Money for the Future'],
  answer=2,
  evidence='Don’t spend your money on things. / Gilovich and other researchers have found that experiences deliver longer lasting happiness than things. / We are the sum total of our experiences.',
  explanation='길로비치의 연구를 바탕으로 물건이 주는 행복은 빨리 사라지고, 경험은 우리의 일부가 되어 더 오래가는 행복을 준다고 한다. 따라서 ‘물건이 아니라 경험에 돈을 써라’라는 ②가 제목으로 가장 적절하다.',
  choices_ko=['가족을 위한 최고의 차를 고르는 방법', '물건이 아니라 경험에 돈을 써라',
              '우리가 항상 소유물을 업그레이드해야 하는 이유', '자신을 남과 비교하기: 기쁨의 열쇠',
              '미래를 위해 돈을 모으는 과학'],
  wrong={1: '차는 남과 비교하는 예로 나올 뿐이다.',
         3: '계속 더 좋은 것을 찾는 것은 물건의 행복이 사라지는 이유로 제시되었다.',
         4: '남과의 비교는 행복을 사라지게 하는 이유로 제시되었다.',
         5: '돈을 모으는 방법은 나오지 않는다.'})

q(id='Q09', set_id='mock1', number=7, type='어휘', first='s01', last='s20', group='G1',
  marks=[('bigger', 's16'), ('like', 's17'), ('connected', 's18'), ('separate', 's18'), ('part', 's19')],
  replace=('separate', 'inseparable'),
  question='윗글의 밑줄 친 부분 중, 문맥상 낱말의 쓰임이 적절하지 않은 것은?',
  answer=4,
  evidence='You can even think that part of your identity is connected to those things, but nonetheless they remain separate from you. On the other hand, your experiences really are part of you.',
  explanation='물건이 정체성과 연결되어 있다고 생각할 수 있지만 그럼에도(nonetheless) 여전히 우리와 분리되어 있고, 반면에 경험은 정말로 우리의 일부라고 대조한다. 따라서 ④의 inseparable(분리할 수 없는)은 문맥에 맞지 않고 separate(분리된)가 되어야 한다.',
  wrong={1: '경험이 물질적 재화보다 우리 자신의 더 큰(bigger) 부분이라는 뜻으로 적절하다.',
         2: '물건을 정말 좋아할(like) 수는 있다고 인정하는 흐름에 맞다.',
         3: '정체성의 일부가 그 물건들과 연결되어(connected) 있다고 생각할 수 있다는 뜻으로 적절하다.',
         5: '경험은 정말로 우리의 일부(part)라는 뜻으로 적절하다.'})


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
        probe = dict(req, length_review={'profile_id': LENGTH_PROFILE_ID, 'grade': 2,
                                         'benchmark_ids': recommended_benchmarks(2, bench_type),
                                         'rationale': 'probe', 'independent_review_required': True})
        view = build_view(src, probe, expected_grade=2, benchmark_type=bench_type)
        lc = view['length_comparison']
        refs = lc['reference_words']
        short = lc['shorter_than_all_references']
        rationale = (f"{'공유 장문 41~42' if grouped else kind} 고2 표본 {refs}단어와 비교해 현재 {lc['assessment_word_count']}단어. "
                     + (BENCH_SHORT_NOTE if short else '표본 범위 이상으로 너무 짧지 않음. ')
                     + '연속 원문 범위 안에서 정답과 네 오답의 근거가 자족적임.')
        req['length_review'] = {'profile_id': LENGTH_PROFILE_ID, 'grade': 2,
                                'benchmark_ids': recommended_benchmarks(2, bench_type), 'rationale': rationale}
        if short:
            req['length_review']['independent_review_required'] = True
        view = build_view(src, req, expected_grade=2, benchmark_type=bench_type)
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
                  'instruction': ('2026-09-27 사용자 선택 “워크북+모의 1회 (추천)”: 253단어 Further Reading에 맞춰 공통 단위당 워크북 실전문제 1개(2문항) + '
                                  '미니 모의고사 1회 7문항(일반 5 + 공유 장문 제목·어휘 2).')},
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
