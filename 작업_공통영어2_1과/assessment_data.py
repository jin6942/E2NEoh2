"""워크북 실전문제(Q01~Q04)와 미니 모의고사 3회(Q05~Q19) 원고: 공통영어2 YBM(박준언) 1과.

지문·정답 위치는 원문에서 계산하고 question_source.build_view로 복원을 검증한다.
조립 코드는 영어2 YBM(박준언) 2과 작업의 assessment_data.py와 같으며, 공통영어2이므로
고1 동유형 공식 표본(grade=1)과 회당 5문항(일반 3 + 공유 장문 2)을 적용한다.

회차 편성 원칙: 한 회차 안에서 빈칸·어휘·순서·삽입·무관 문항의 정답 근거가 다른 문항 지문에
원형으로 드러나지 않도록 원문 구간을 나눈다.
  1회: 요지 s11~s19 / 순서 s01~s10 / 삽입 s31~s43 / 장문(제목·어휘) s20~s30
  2회: 내용 s01~s10 / 빈칸 s22~s30 / 무관 s11~s19 / 장문(제목·어휘) s31~s47
  3회: 요약 s11~s19 / 함축 s22~s30 / 순서 s31~s43 / 장문(제목·어휘) s01~s14 (어휘 교체는 s01~s10 구간)
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / '스킬수정본' / 'gyogwaseo-unified' / 'scripts'))
from question_source import build_view, recommended_benchmarks, LENGTH_PROFILE_ID  # noqa: E402

CIRCLED = '①②③④⑤'
ORDER = [['A', 'C', 'B'], ['B', 'A', 'C'], ['B', 'C', 'A'], ['C', 'A', 'B'], ['C', 'B', 'A']]
BENCH_SHORT_NOTE = '동일 유형 공식 표본보다 짧아 독립 검수에서 분량·정보 전개를 확인해야 함. '

Q = []  # 작성 순서 = 출력 순서


def q(**kw):
    Q.append(kw)


# ================================================================ 워크북 실전문제
q(id='Q01', set_id='workbook', number=1, unit_id='u1', type='주제', first='s01', last='s10',
  question='다음 글의 주제로 가장 적절한 것은?',
  choices=['praising people who intentionally check the news before sharing it',
           'how even someone who condemns fake news can unintentionally spread it',
           'why unknown content creators prefer to write true stories',
           'the harm that well-known athletes suffer from online rumors',
           'the reasons reporters intentionally hide news about natural disasters'],
  answer=2,
  uses=[('u1-r2a', 1, 'praising', 'praise(칭찬하다)는 criticize의 반대로, 글이 누군가를 칭찬하는 내용이 아님을 판단해야 함'),
        ('u1-r3a', 1, 'intentionally', 'intentionally(일부러)의 뜻을 알아야 지나가 뉴스를 일부러 확인했다는 말이 본문과 어긋남을 판단할 수 있음'),
        ('u1-r2s', 2, 'condemns', 'condemn(비난하다)이 criticize와 같은 뜻임을 알아야 가짜 뉴스를 비판하던 지나를 가리킨다는 것을 판단할 수 있음'),
        ('u1-r3s', 2, 'unintentionally', 'unintentionally(의도하지 않게)가 accidentally와 같은 뜻임을 알아야 주제를 판단할 수 있음'),
        ('u1-r1a', 3, 'unknown', 'unknown(알려지지 않은) 제작자가 참된 이야기를 좋아한다는 말은 본문에 없음을 판단해야 함'),
        ('u1-r1s', 4, 'well-known', 'well-known(유명한)이 famous와 같은 뜻임을 알아도 운동선수 사건은 한 예일 뿐 주제가 아님을 판단해야 함')],
  evidence='At that time, Gina criticized those who had made and spread fake news because it had hurt the athlete and confused people. This time, however, Gina herself had accidentally contributed to the spread of fake news.',
  explanation='지나는 흔들바위가 떨어졌다는 가짜 뉴스를 믿고 친구들에게 공유했다가 가짜라는 사실을 알고 당황한다. 예전에 운동선수 사망 가짜 뉴스를 만들고 퍼뜨린 사람들을 비판했던 지나가 이번에는 자신도 모르게 가짜 뉴스를 퍼뜨린 것이다. 따라서 가짜 뉴스를 비난하는 사람조차 의도하지 않게 그것을 퍼뜨릴 수 있다는 ②가 주제다.',
  choices_ko=['공유하기 전에 일부러 뉴스를 확인하는 사람들을 칭찬하는 것',
              '가짜 뉴스를 비난하는 사람조차 어떻게 의도하지 않게 그것을 퍼뜨릴 수 있는지',
              '알려지지 않은 콘텐츠 제작자들이 진짜 이야기를 쓰는 것을 선호하는 이유',
              '유명한 운동선수들이 온라인 소문으로 겪는 피해',
              '기자들이 자연재해에 관한 뉴스를 일부러 숨기는 이유'],
  wrong={1: '지나는 뉴스를 확인하지 않고 곧바로 공유했으며, 글은 누군가를 칭찬하는 내용이 아니다.',
         3: '콘텐츠 제작자들은 관심과 돈을 위해 자극적인 거짓 이야기를 만들었다고 했으므로 반대 내용이다.',
         4: '운동선수 사망 가짜 뉴스는 지나가 떠올린 한 예일 뿐 글 전체의 중심이 아니다.',
         5: '기자는 오히려 흔들바위 기사가 가짜라고 알렸으며, 뉴스를 숨긴다는 내용은 없다.'})

q(id='Q02', set_id='workbook', number=2, unit_id='u2', type='내용', first='s11', last='s19',
  question='다음 글의 내용과 일치하지 않는 것은?',
  choices=['Spreading fake news by accident, as Gina did, is not rare.',
           'Fake news is an intentional effort to control people with incorrect information.',
           'Some groups make fake news to get attention, money, or political benefits.',
           'During emergencies, it is usual for false stories to be widely shared.',
           'After the earthquake, the government confirmed that the tsunami messages were accurate.'],
  answer=5,
  uses=[('u2-r3a', 1, 'rare', 'rare(드문)의 뜻을 알아야 not unusual(드물지 않다)과 같은 말임을 판단할 수 있음'),
        ('u2-r1s', 2, 'intentional', 'intentional이 deliberate(의도적인)와 같은 뜻임을 판단해야 함'),
        ('u2-r2s', 2, 'incorrect', 'incorrect가 inaccurate(부정확한)와 같은 뜻임을 판단해야 함'),
        ('u2-r3s', 4, 'usual', 'usual(흔한)이 common과 같은 뜻임을 알아야 일치 여부를 판단할 수 있음'),
        ('u2-r2a', 5, 'accurate', 'accurate(정확한)의 뜻을 알아야 정부가 정보가 가짜라고 발표했다는 본문과 어긋남을 판단할 수 있음')],
  evidence='Many displaced people were so anxious about aftershocks that the government had to announce that the information was fake.',
  explanation='정부는 또 다른 지진과 쓰나미가 온다는 정보가 가짜라고 발표해야 했다. 따라서 정부가 쓰나미 메시지가 정확하다고 확인했다는 ⑤는 본문과 일치하지 않는다.',
  choices_ko=['지나처럼 뜻하지 않게 가짜 뉴스를 퍼뜨리는 것은 드물지 않다.',
              '가짜 뉴스는 틀린 정보로 사람들을 통제하려는 의도적인 노력이다.',
              '어떤 집단들은 관심, 돈, 또는 정치적 이득을 얻으려고 가짜 뉴스를 만든다.',
              '비상사태 동안에는 거짓 이야기가 널리 공유되는 것이 흔한 일이다.',
              '지진 후에 정부는 쓰나미 메시지가 정확하다고 확인했다.'],
  wrong={1: '“becoming an accidental distributor of fake news like Gina is not unusual”과 일치한다(not unusual = not rare).',
         2: '“Fake news is a deliberate attempt to manipulate people by spreading inaccurate information.”과 일치한다.',
         3: '“with the intention of attracting people’s attention, making profits, or gaining political benefits”와 일치한다.',
         4: '“It is very common for fake news to spread during states of emergency.”와 일치한다(very common = usual, fake news = false stories, spread = be widely shared).'})

q(id='Q03', set_id='workbook', number=3, unit_id='u3', type='제목', first='s20', last='s30',
  question='다음 글의 제목으로 가장 적절한 것은?',
  choices=['Why Fake News Travels Considerably Faster Than the Truth',
           'True Stories Spread Only Slightly Slower Than Fake News',
           'How People Learn to Disregard Stimulating Information',
           'Accepting Unfavorable News: A Habit of Most Voters',
           'The Positive Effects of Election Season on the Media'],
  answer=1,
  uses=[('u3-r1s', 1, 'Considerably', 'considerably가 significantly(훨씬, 상당히)와 같은 뜻임을 알아야 가짜 뉴스가 훨씬 빨리 퍼진다는 내용과 맞는지 판단할 수 있음'),
        ('u3-r1a', 2, 'Slightly', 'slightly(약간)의 뜻을 알아야 6배나 빠르다는 본문과 어긋남을 판단할 수 있음'),
        ('u3-r2s', 3, 'Disregard', 'disregard가 ignore(무시하다)와 같은 뜻임을 알아야 자극적인 정보를 공유하고 싶어 한다는 본문과 반대임을 판단할 수 있음'),
        ('u3-r2a', 4, 'Accepting', 'accept(받아들이다)의 뜻을 알아야 믿음을 뒷받침하지 않는 뉴스는 무시한다는 본문과 어긋남을 판단할 수 있음'),
        ('u3-r3s', 4, 'Unfavorable', 'unfavorable이 negative와 같은 뜻임을 판단해야 함'),
        ('u3-r3a', 5, 'Positive', 'positive(긍정적인)의 뜻을 알아야 선거철 예시가 확증 편향의 예일 뿐 좋은 영향을 말하지 않음을 판단할 수 있음')],
  evidence='Fake news on social media spreads significantly farther and faster than true stories. / One explanation for this phenomenon is that people like new and provocative things. / Also, fake news goes viral because people … tend to think simply and effortlessly. / … people easily fall into the trap of “confirmation bias.”',
  explanation='글은 가짜 뉴스가 진짜 이야기보다 훨씬 더 멀리, 빨리 퍼진다는 사실을 제시한 뒤, 그 이유로 사람들이 새롭고 자극적인 것을 좋아하고, 단순하게 생각하며, 확증 편향에 빠진다는 점을 설명한다. 따라서 ①이 제목으로 가장 적절하다.',
  choices_ko=['왜 가짜 뉴스는 진실보다 상당히 더 빨리 퍼지는가',
              '진짜 이야기는 가짜 뉴스보다 약간만 더 느리게 퍼진다',
              '사람들이 자극적인 정보를 무시하는 법을 배우는 방법',
              '불리한 뉴스를 받아들이기: 대부분 유권자의 습관',
              '선거철이 언론에 미치는 긍정적인 영향'],
  wrong={2: '가짜 뉴스가 평균 6배 더 빠르게 퍼진다고 했으므로 ‘약간’은 본문과 어긋난다.',
         3: '사람들은 놀라운 정보를 다른 사람들과 공유하고 싶어 한다고 했으므로 반대 내용이다.',
         4: '사람들은 자신의 믿음을 뒷받침하지 않는 뉴스는 무시한다고 했으므로 반대 내용이다.',
         5: '선거철은 확증 편향의 예로 나올 뿐, 선거가 언론에 주는 좋은 영향은 다루지 않는다.'})

q(id='Q04', set_id='workbook', number=4, unit_id='u4', type='주장', first='s37', last='s47',
  question='다음 글에서 필자가 주장하는 바로 가장 적절한 것은?',
  choices=['Read only reliable news sources that agree with your beliefs.',
           'Judge news impartially by checking whether its source is trustworthy and its evidence is sound.',
           'Judge a news story subjectively, since your first feelings about it are usually right.',
           'Ignore all invalid news, because false information can be completely removed online.',
           'Let social media companies remove every piece of unreliable information for you.'],
  answer=2,
  uses=[('u4-r1h', 1, 'reliable', 'reliable(믿을 만한)의 뜻을 알아도 믿음과 같은 뉴스만 읽으라는 말은 반대 의견 기사도 찾으라는 본문과 어긋남을 판단해야 함'),
        ('u4-r3s', 2, 'impartially', 'impartially가 objectively(객관적으로)와 같은 뜻임을 알아야 필자의 주장을 판단할 수 있음'),
        ('u4-r1s', 2, 'trustworthy', 'trustworthy가 reliable과 같은 뜻임을 판단해야 함'),
        ('u4-r2s', 2, 'sound', 'sound가 여기서 valid(타당한)와 같은 뜻임을 판단해야 함'),
        ('u4-r3a', 3, 'subjectively', 'subjectively(주관적으로)가 objectively의 반대임을 알아야 본문과 어긋남을 판단할 수 있음'),
        ('u4-r2a', 4, 'invalid', 'invalid(타당하지 않은)의 뜻과 함께, 거짓 정보를 모두 없애는 것은 불가능할 수 있다는 본문과 어긋남을 판단해야 함'),
        ('u4-r1a', 5, 'unreliable', 'unreliable(믿을 수 없는)의 뜻을 알아도 판단을 남에게 맡기라는 말은 스스로 비판적으로 보라는 본문과 어긋남을 판단해야 함')],
  evidence='Finally, check the credibility of the source. / You also need to check whether the news story is from a reliable media source and the evidence is valid. / However, if you have the ability to view information critically and objectively, you will be able to reduce the damage that fake news can cause.',
  explanation='필자는 읽은 것에 의문을 갖고 평가하며, 자신의 편견을 점검하고, 출처의 신뢰성과 증거의 타당성을 확인하라고 한다. 또 정보를 비판적이고 객관적으로 보는 능력이 있으면 가짜 뉴스의 피해를 줄일 수 있다고 한다. 따라서 출처가 믿을 만하고 증거가 타당한지 확인하며 뉴스를 공정하게 판단하라는 ②가 주장이다.',
  choices_ko=['자신의 믿음과 일치하는 믿을 만한 뉴스 출처만 읽어라.',
              '출처가 신뢰할 수 있고 증거가 타당한지 확인하여 뉴스를 공정하게 판단하라.',
              '뉴스에 대한 첫 느낌이 대개 옳으므로 뉴스 기사를 주관적으로 판단하라.',
              '거짓 정보는 온라인에서 완전히 없앨 수 있으므로 타당하지 않은 뉴스는 모두 무시하라.',
              '소셜 미디어 회사가 당신을 위해 믿을 수 없는 정보를 모두 없애게 하라.'],
  wrong={1: '자신의 의견에 반대되는 기사도 찾아 읽으라고 했으므로 믿음과 같은 뉴스만 읽으라는 것은 반대 내용이다.',
         3: '자신의 믿음이 판단에 영향을 줄 수 있는지 살피고 객관적으로 보라고 했으므로 반대 내용이다.',
         4: '디지털 시대에 모든 거짓 정보를 피하거나 없애는 것은 불가능할지도 모른다고 했으므로 틀리다.',
         5: '필자는 독자 스스로 정보를 비판적으로 판단하라고 하며, 판단을 남에게 맡기라는 내용은 없다.'})


# ================================================================ 미니 모의고사 1회
q(id='Q05', set_id='mock1', number=1, type='요지', first='s11', last='s19',
  question='다음 글의 요지로 가장 적절한 것은?',
  choices=['Most fake news is created by ordinary people who share stories by mistake.',
           'Governments are the main cause of false information during natural disasters.',
           'Fake news, made on purpose to mislead people, can cause serious harm, especially in emergencies.',
           'Earthquakes cause far more confusion than any kind of false information.',
           'Social media helps people get accurate safety information quickly in emergencies.'],
  answer=3,
  evidence='Fake news is a deliberate attempt to manipulate people by spreading inaccurate information. / It can confuse people, disturb society, and even seriously harm the public as well as all individuals involved. / It is very common for fake news to spread during states of emergency.',
  explanation='가짜 뉴스는 사람들을 조종하려는 의도적인 시도로, 사람들을 혼란스럽게 하고 사회에 심각한 해를 끼칠 수 있으며, 특히 비상사태 때 흔히 퍼진다. 암본 지진 사례는 이를 보여 준다. 따라서 ③이 요지다.',
  choices_ko=['대부분의 가짜 뉴스는 실수로 이야기를 공유하는 평범한 사람들이 만든다.',
              '정부가 자연재해 동안 거짓 정보의 주된 원인이다.',
              '사람들을 속이려고 일부러 만든 가짜 뉴스는 특히 비상사태에 심각한 해를 끼칠 수 있다.',
              '지진은 어떤 거짓 정보보다 훨씬 더 큰 혼란을 일으킨다.',
              '소셜 미디어는 비상사태에 사람들이 정확한 안전 정보를 빨리 얻도록 돕는다.'],
  wrong={1: '가짜 뉴스는 특정 집단이 의도를 가지고 만든다고 했다. 지나처럼 실수로 퍼뜨리는 사람이 있다는 것과 만드는 사람은 구별된다.',
         2: '정부는 오히려 정보가 가짜라고 발표해 바로잡았다.',
         4: '지진과 가짜 뉴스의 혼란을 비교하는 내용은 없으며, 주민들이 대피소에 남은 것은 가짜 뉴스 때문이었다.',
         5: '소셜 미디어에서 퍼진 가짜 뉴스 때문에 주민들이 집에 돌아가지 못했으므로 반대 내용이다.'})

q(id='Q06', set_id='mock1', number=2, type='순서', first='s01', last='s10',
  blocks=('s01', 's02', {'A': ('s05', 's07'), 'B': ('s08', 's10'), 'C': ('s03', 's04')}),
  question='주어진 글 다음에 이어질 글의 순서로 가장 적절한 것은?',
  answer=4,
  evidence='(C) “Today’s Internet stories of the Heundeulbawi being damaged were fake.”로 공유한 소식이 가짜임이 밝혀짐 / (A) “It reminded her of another incident of fake news …”의 It과 another가 (C)의 사건을 받음 / (B) “They produced …”의 They가 (A)의 content creators를 가리키고, “This time, however, …”으로 마무리됨.',
  explanation='주어진 글은 지나가 흔들바위가 떨어졌다는 헤드라인을 보고 친구들에게 공유한 장면이다. (C) 기자가 그 기사가 가짜라고 밝히고 지나는 당황한다. (A) 이 일이 떠올리게 한 또 다른 가짜 뉴스(운동선수 사망 뉴스)와 그것을 만든 콘텐츠 제작자들이 나온다. (B) 그들(They)이 돈을 벌려고 자극적인 거짓 이야기를 만들었고, 지나는 그때 그들을 비판했지만 이번에는 자신이 가짜 뉴스를 퍼뜨렸다. 따라서 (C)-(A)-(B)이다.',
  wrong={1: '(A)의 another incident of fake news는 앞에서 흔들바위 뉴스가 가짜라고 밝혀진 뒤에야 쓸 수 있어 주어진 글 바로 뒤에 올 수 없다.',
         2: '(B)의 They가 가리킬 대상(content creators)이 앞에 없고, (B)의 This time, however는 이미 흔들바위 뉴스가 가짜로 밝혀진 뒤라야 이어질 수 있다.',
         3: '(B)를 주어진 글 바로 뒤에 두면 They가 가리킬 대상이 없다.',
         5: '(C) 뒤에 (B)가 오면 They가 가리킬 콘텐츠 제작자와 운동선수 사건이 아직 나오지 않았다.'})

q(id='Q07', set_id='mock1', number=3, type='삽입', first='s31', last='s43', given='s38',
  slots=['s33', 's35', 's36', 's38', 's41'],
  question='글의 흐름으로 보아, 주어진 문장이 들어가기에 가장 적절한 곳은?',
  answer=4,
  evidence='You should question, analyze, and evaluate what you read. ( ④ ) Consider if your own beliefs could affect your judgment. Ask yourself if you are only reading articles that suit your opinion …',
  explanation='주어진 문장은 가짜 뉴스를 피하는 세 번째 방법으로 자신의 편견을 점검하라는 내용이다. ④ 뒤의 문장들은 자신의 믿음이 판단에 영향을 줄 수 있는지 생각하고 자기 의견에 맞는 기사만 읽는지 스스로 물어보라며 편견 점검을 구체적으로 설명한다. 또 Second 다음, Finally 앞이라는 순서에도 맞으므로 ④가 알맞다.',
  wrong={1: 'First 방법(헤드라인 너머 읽기)과 그 이유를 설명하는 They can be so stimulating … 사이이므로 Third가 들어갈 수 없다.',
         2: 'Second보다 앞이라 First–Third–Second의 순서가 된다.',
         3: 'Second, don’t read the news at face value.와 그것을 설명하는 Exercise critical thinking skills … 사이를 끊는다.',
         5: '편견을 점검하는 구체적 방법(자기 믿음·의견 살피기)이 Third보다 먼저 나와 버리고, 바로 뒤가 Finally라 흐름이 어색하다.'})

q(id='Q08', set_id='mock1', number=4, type='제목', first='s20', last='s30', group='G1',
  question='윗글의 제목으로 가장 적절한 것은?',
  choices=['How Social Media Helps Us Check the Facts',
           'Election News: Always Fair and Balanced',
           'Scientific Methods for Measuring the Speed of News',
           'Critical Thinking: The Main Reason Fake News Spreads',
           'What Makes Fake News Spread So Fast?'],
  answer=5,
  evidence='Fake news on social media spreads significantly farther and faster than true stories. / One explanation for this phenomenon … / Also, fake news goes viral because … / Moreover, people are inclined to believe information that fits their prejudices …',
  explanation='가짜 뉴스가 진짜 이야기보다 훨씬 빨리 퍼진다는 사실을 제시하고, 그 이유 세 가지(새롭고 자극적인 것을 좋아함, 단순하게 생각함, 확증 편향)를 설명한다. 따라서 ⑤가 제목으로 가장 적절하다.',
  choices_ko=['소셜 미디어는 우리가 사실을 확인하도록 어떻게 돕는가',
              '선거 뉴스: 언제나 공정하고 균형 잡힌',
              '뉴스의 속도를 측정하는 과학적 방법',
              '비판적 사고: 가짜 뉴스가 퍼지는 주된 이유',
              '무엇이 가짜 뉴스를 그렇게 빨리 퍼지게 하는가?'],
  wrong={1: '소셜 미디어의 가짜 뉴스가 더 빨리 퍼진다고 했을 뿐, 사실 확인을 돕는다는 내용은 없다.',
         2: '선거철에 사람들은 지지 후보에게 유리한 뉴스를 맹목적으로 믿는다고 했으므로 반대 내용이다.',
         3: 'MIT 연구 결과는 가짜 뉴스가 빠르다는 근거로 쓰였을 뿐, 측정 방법은 다루지 않는다.',
         4: '사람들이 비판적으로 검토하지 않고 믿기 때문에 퍼진다고 했으므로 비판적 사고가 원인이라는 것은 반대다.'})

q(id='Q09', set_id='mock1', number=5, type='어휘', first='s20', last='s30', group='G1',
  marks=[('provocative', 's22'), ('share', 's23'), ('simply', 's25'), ('ignore', 's29'), ('negative', 's30')],
  replace=('ignore', 'trust'),
  question='윗글의 밑줄 친 부분 중, 문맥상 낱말의 쓰임이 적절하지 않은 것은?',
  answer=4,
  evidence='In this process, people easily fall into the trap of “confirmation bias.” That is, they selectively accept news in a way that only confirms their beliefs and … news that doesn’t support them.',
  explanation='확증 편향은 자신의 믿음을 확인해 주는 뉴스만 골라 받아들이는 것이다. 따라서 믿음을 뒷받침하지 않는 뉴스는 무시한다(ignore)가 되어야 하며, ④의 trust(믿다)는 문맥에 맞지 않는다.',
  wrong={1: '사람들이 새롭고 자극적인(provocative) 것을 좋아한다는 설명으로 적절하다.',
         2: '놀라운 정보를 다른 사람들과 공유하고(share) 싶어 한다는 흐름에 맞다.',
         3: '일상생활에서 단순하고(simply) 쉽게 생각하는 경향이 있다는 뜻으로 적절하다.',
         5: '다른 후보에 대해 부정적인(negative) 내용을 보도하는 뉴스를 믿는다는 선거철 예시로 적절하다.'})


# ================================================================ 미니 모의고사 2회
q(id='Q10', set_id='mock2', number=1, type='내용', first='s01', last='s10',
  question='다음 글의 내용과 일치하는 것은?',
  choices=['Gina first saw the news about the Heundeulbawi on TV.',
           'Gina checked whether the story was true before sharing it.',
           'A reporter said that the Heundeulbawi had been damaged.',
           'The fake news about the athlete was made to attract people’s attention.',
           'Gina supported the people who spread the news about the athlete.'],
  answer=4,
  evidence='It had been made by content creators who sought people’s attention. They produced provocative false stories to make money by raising the number of views of their posts.',
  explanation='운동선수 사망 가짜 뉴스는 사람들의 관심을 끌려던 콘텐츠 제작자들이 만든 것이었다. 따라서 ④가 본문과 일치한다.',
  choices_ko=['지나는 흔들바위에 관한 뉴스를 TV에서 처음 보았다.',
              '지나는 이야기를 공유하기 전에 그것이 사실인지 확인했다.',
              '한 기자는 흔들바위가 손상되었다고 말했다.',
              '운동선수에 관한 가짜 뉴스는 사람들의 관심을 끌려고 만들어졌다.',
              '지나는 운동선수에 관한 뉴스를 퍼뜨린 사람들을 지지했다.'],
  wrong={1: '지나는 소셜 미디어를 스크롤하다가 헤드라인을 처음 보았다.',
         2: '지나는 헤드라인을 보고 곧바로(immediately) 친구들에게 공유했다.',
         3: '기자는 흔들바위가 손상되었다는 인터넷 기사가 가짜라고 말했다.',
         5: '지나는 그 가짜 뉴스를 만들고 퍼뜨린 사람들을 비판했다.'})

q(id='Q11', set_id='mock2', number=2, type='빈칸', first='s22', last='s30',
  blank='fits their prejudices or experiences',
  question='다음 빈칸에 들어갈 말로 가장 적절한 것은?',
  choices=['matches what they already believe',
           'comes from experts they have never trusted',
           'challenges their usual way of thinking',
           'has been checked by many other people',
           'is shared by those who disagree with them'],
  answer=1,
  evidence='In this process, people easily fall into the trap of “confirmation bias.” That is, they selectively accept news in a way that only confirms their beliefs and ignore news that doesn’t support them.',
  explanation='빈칸 뒤에서 이 과정이 확증 편향이며, 사람들은 자신의 믿음을 확인해 주는 뉴스만 받아들이고 그렇지 않은 뉴스는 무시한다고 설명한다. 따라서 사람들이 사실이 아니어도 이미 믿는 것과 맞는 정보를 믿는다는 ①이 알맞다.',
  choices_ko=['그들이 이미 믿는 것과 일치하다', '그들이 한 번도 믿지 않았던 전문가에게서 나오다',
              '그들의 평소 사고방식에 이의를 제기하다', '많은 다른 사람들에 의해 확인되었다',
              '그들과 의견이 다른 사람들에 의해 공유되다'],
  wrong={2: '전문가나 신뢰 여부는 본문의 근거와 관계없다.',
         3: '사람들은 자신의 믿음을 확인해 주는 뉴스만 받아들인다고 했으므로 반대 내용이다.',
         4: '사람들은 증거 없이 믿는 경향이 있다고 했으며, 여러 사람이 확인했다는 조건은 나오지 않는다.',
         5: '사람들은 자기 믿음을 뒷받침하지 않는 뉴스는 무시한다고 했으므로 맞지 않는다.'})

q(id='Q12', set_id='mock2', number=3, type='무관한 문장', first='s11', last='s19',
  addition='Indonesia is famous for its beautiful islands, which attract many tourists every year.',
  add_before='s17', marks=['s15', 's16', '@added', 's17', 's18'],
  question='다음 글에서 전체 흐름과 관계 없는 문장은?',
  answer=3,
  evidence='For example, after an earthquake measuring 6.5 struck Ambon, Indonesia, in September 2019, thousands of residents did not return to their homes … This was because of fake news stories on social media …',
  explanation='글은 가짜 뉴스가 사회에 끼치는 해와, 비상사태에 가짜 뉴스가 퍼진 암본 지진 사례를 다룬다. ③은 인도네시아의 아름다운 섬과 관광객 이야기로, 주민들이 집에 돌아가지 않은 일과 그 이유(This was because of fake news …)를 잇는 흐름을 끊는다.',
  wrong={1: '비상사태 동안 가짜 뉴스가 퍼지는 것이 흔하다는 이 부분의 주제문이다.',
         2: '암본 지진 뒤 주민들이 집에 돌아가지 않았다는 사례를 제시한다.',
         4: '주민들이 돌아가지 않은 이유가 소셜 미디어의 가짜 뉴스였다고 설명한다.',
         5: '가짜 메시지의 실제 예를 보여 준다.'})

q(id='Q13', set_id='mock2', number=4, type='제목', first='s31', last='s47', group='G2',
  question='윗글의 제목으로 가장 적절한 것은?',
  choices=['Headlines Tell You Everything You Need to Know',
           'Read Smart: How Not to Be Fooled by Fake News',
           'Why Biased News Is Better Than No News',
           'The Digital Age Has Finally Ended Fake News',
           'How to Write News That Gets More Clicks'],
  answer=2,
  evidence='With so much information on the Internet, how can you make sure that fake news does not mislead you? First, … Second, … Third, … Finally, … / … if you have the ability to view information critically and objectively, you will be able to reduce the damage that fake news can cause.',
  explanation='가짜 뉴스에 속지 않는 네 가지 방법(헤드라인 너머 읽기, 곧이곧대로 읽지 않기, 편견 점검, 출처 신뢰성 확인)을 제시하고, 비판적·객관적 태도로 피해를 줄일 수 있다고 강조한다. 따라서 ②가 제목으로 가장 적절하다.',
  choices_ko=['헤드라인이 당신이 알아야 할 모든 것을 알려 준다',
              '똑똑하게 읽기: 가짜 뉴스에 속지 않는 방법',
              '왜 편향된 뉴스가 뉴스가 없는 것보다 나은가',
              '디지털 시대가 마침내 가짜 뉴스를 끝냈다',
              '더 많은 클릭을 얻는 뉴스를 쓰는 방법'],
  wrong={1: '헤드라인만 읽지 말고 본문을 주의 깊게 읽으라고 했으므로 반대 내용이다.',
         3: '편견을 점검하고 반대 의견의 기사도 찾으라고 했을 뿐, 편향된 뉴스가 낫다는 내용은 없다.',
         4: '디지털 시대에 모든 거짓 정보를 없애는 것은 불가능할지도 모른다고 했으므로 반대 내용이다.',
         5: '클릭을 노린 자극적인 헤드라인을 조심하라는 글이지, 클릭을 얻는 뉴스 작성법을 다루지 않는다.'})

q(id='Q14', set_id='mock2', number=5, type='어휘', first='s31', last='s47', group='G2',
  marks=[('beyond', 's32'), ('accidentally', 's33'), ('critical', 's36'), ('oppose', 's40'), ('reduce', 's45')],
  replace=('oppose', 'support'),
  question='윗글의 밑줄 친 부분 중, 문맥상 낱말의 쓰임이 적절하지 않은 것은?',
  answer=4,
  evidence='Third, examine your biases. … Ask yourself if you are only reading articles that suit your opinion, and look for articles that … your opinion as well.',
  explanation='편견을 점검하려면 자기 의견에 맞는 기사만 읽고 있는지 돌아보고, 자기 의견에 반대되는(oppose) 기사도 찾아 읽어야 한다. ④의 support(지지하다)는 자기 의견에 맞는 기사만 읽는 태도를 되풀이하게 되므로 문맥에 맞지 않는다.',
  wrong={1: '자극적인 헤드라인에서 멈추지 말고 그 너머(beyond)까지 읽으라는 뜻으로 적절하다.',
         2: '헤드라인이 너무 자극적이어서 무심코(accidentally) 클릭할 수 있다는 흐름에 맞다.',
         3: '뉴스를 판단하려면 비판적(critical) 사고 기술을 발휘하라는 뜻으로 적절하다.',
         5: '비판적·객관적으로 볼 수 있으면 가짜 뉴스의 피해를 줄일(reduce) 수 있다는 결론에 맞다.'})


# ================================================================ 미니 모의고사 3회
q(id='Q15', set_id='mock3', number=1, type='요약', first='s11', last='s19',
  summary='Fake news, which is (A) ________ created to manipulate people, can cause serious harm, especially when people are (B) ________ during emergencies.',
  question='다음 글의 내용을 한 문장으로 요약하고자 한다. 빈칸 (A), (B)에 들어갈 말로 가장 적절한 것은?',
  choices=['accidentally …… calm',
           'intentionally …… fearful',
           'intentionally …… careless',
           'rarely …… fearful',
           'accidentally …… informed'],
  answer=2,
  evidence='Fake news is a deliberate attempt to manipulate people by spreading inaccurate information. / Many displaced people were so anxious about aftershocks that the government had to announce that the information was fake.',
  explanation='가짜 뉴스는 사람들을 조종하려는 의도적인(deliberate) 시도이며, 암본 지진 때 이재민들이 여진을 몹시 불안해한(anxious) 상황에서 퍼져 큰 피해를 주었다. 따라서 (A) intentionally(의도적으로), (B) fearful(두려워하는)인 ②가 알맞다.',
  choices_ko=['우연히 …… 침착한', '의도적으로 …… 두려워하는', '의도적으로 …… 부주의한',
              '드물게 …… 두려워하는', '우연히 …… 정보를 잘 아는'],
  wrong={1: '가짜 뉴스는 의도적으로 만들어지며, 이재민들은 침착한 것이 아니라 불안해했다.',
         3: '(A)는 맞지만, 이재민들은 부주의한 것이 아니라 여진을 불안해했다.',
         4: '(B)는 맞지만, 가짜 뉴스가 드물게 만들어진다는 내용은 없고 의도적으로 만들어진다고 했다.',
         5: '가짜 뉴스는 우연히가 아니라 의도적으로 만들어지며, 이재민들은 정보를 잘 아는 상태가 아니었다.'})

q(id='Q16', set_id='mock3', number=2, type='함축 의미', first='s22', last='s30',
  target='fall into the trap',
  question='밑줄 친 fall into the trap이 다음 글에서 의미하는 바로 가장 적절한 것은?',
  choices=['deliberately set up traps to fool other people',
           'lose all interest in reading the news',
           'get caught while spreading false stories online',
           'fail to find any information about the candidates',
           'are easily led into a way of thinking that misleads them'],
  answer=5,
  evidence='Moreover, people are inclined to believe information that fits their prejudices or experiences even when not true. … That is, they selectively accept news in a way that only confirms their beliefs and ignore news that doesn’t support them.',
  explanation='사람들은 사실이 아니어도 자신의 편견이나 경험에 맞는 정보를 믿는 경향이 있고, 자신의 믿음을 확인해 주는 뉴스만 골라 받아들인다. 이렇게 자기도 모르게 잘못된 판단으로 이끄는 사고방식에 빠진다는 뜻이므로 ⑤가 알맞다.',
  choices_ko=['다른 사람들을 속이려고 일부러 함정을 설치하다', '뉴스를 읽는 데 모든 흥미를 잃다',
              '온라인에서 거짓 이야기를 퍼뜨리다가 들키다', '후보들에 관한 어떤 정보도 찾지 못하다',
              '자신을 잘못 이끄는 사고방식에 쉽게 빠져들다'],
  wrong={1: '함정은 다른 사람을 속이려고 만든 것이 아니라 스스로 빠지는 사고방식을 비유한 말이다.',
         2: '사람들은 오히려 자신의 믿음에 맞는 뉴스를 적극적으로 받아들인다.',
         3: '거짓 이야기를 퍼뜨리다 들킨다는 내용은 본문에 없다.',
         4: '선거철에도 사람들은 후보에 관한 뉴스를 믿는다고 했으므로 정보를 찾지 못한다는 것은 틀리다.'})

q(id='Q17', set_id='mock3', number=3, type='순서', first='s31', last='s43',
  blocks=('s31', 's34', {'B': ('s35', 's37'), 'A': ('s38', 's40'), 'C': ('s41', 's43')}),
  question='주어진 글 다음에 이어질 글의 순서로 가장 적절한 것은?',
  answer=2,
  evidence='(B) “Second, don’t read the news at face value.” / (A) “Third, examine your biases.” / (C) “Finally, check the credibility of the source.”',
  explanation='주어진 글은 가짜 뉴스에 속지 않는 방법을 묻고 첫째 방법(헤드라인 너머 읽기)을 제시한다. 이어서 (B) 둘째, 뉴스를 곧이곧대로 읽지 말고 비판적으로 판단하기, (A) 셋째, 자신의 편견 점검하기, (C) 마지막으로 출처의 신뢰성 확인하기가 차례로 온다. 따라서 (B)-(A)-(C)이다.',
  wrong={1: '(A)의 Third가 (B)의 Second보다 먼저 나오게 된다.',
         3: '(C)의 Finally가 (A)의 Third보다 먼저 나와 마지막 방법 뒤에 또 방법이 이어진다.',
         4: '(C)의 Finally가 가장 먼저 오고 Third가 Second보다 앞선다.',
         5: '(C)의 Finally가 맨 앞에 오고, Third–Second 순서가 뒤바뀐다.'})

q(id='Q18', set_id='mock3', number=4, type='제목', first='s01', last='s14', group='G3',
  question='윗글의 제목으로 가장 적절한 것은?',
  choices=['From Critic to Spreader: How Anyone Can Pass On Fake News',
           'Why Gina Decided to Stop Using Social Media',
           'The Hidden Danger of Famous Rocks in National Parks',
           'How Reporters Make Money from Fake Headlines',
           'The Benefits of Sharing News as Quickly as Possible'],
  answer=1,
  evidence='At that time, Gina criticized those who had made and spread fake news … This time, however, Gina herself had accidentally contributed to the spread of fake news. Unfortunately, becoming an accidental distributor of fake news like Gina is not unusual.',
  explanation='가짜 뉴스를 비판하던 지나가 뜻하지 않게 가짜 뉴스를 퍼뜨린 경험을 소개하고, 이런 일이 드물지 않으며 가짜 뉴스가 사람들과 사회에 큰 해를 끼칠 수 있다고 설명한다. 따라서 ①이 제목으로 가장 적절하다.',
  choices_ko=['비판자에서 유포자로: 누구나 가짜 뉴스를 퍼뜨릴 수 있는 방식',
              '지나가 소셜 미디어 사용을 그만두기로 한 이유',
              '국립공원에 있는 유명한 바위의 숨겨진 위험',
              '기자들이 가짜 헤드라인으로 돈을 버는 방법',
              '뉴스를 가능한 한 빨리 공유하는 것의 이점'],
  wrong={2: '지나가 소셜 미디어를 그만두었다는 내용은 없다.',
         3: '흔들바위는 멀쩡했으며, 바위의 위험은 글의 내용이 아니다.',
         4: '돈을 벌려고 가짜 뉴스를 만든 것은 기자가 아니라 콘텐츠 제작자들이다.',
         5: '지나는 확인 없이 곧바로 공유했다가 가짜 뉴스를 퍼뜨렸으므로, 빠른 공유의 이점을 말하는 글이 아니다.'})

q(id='Q19', set_id='mock3', number=5, type='어휘', first='s01', last='s14', group='G3',
  marks=[('immediately', 's02'), ('undamaged', 's03'), ('embarrassed', 's04'), ('criticized', 's09'), ('deliberate', 's12')],
  replace=('embarrassed', 'pleased'),
  question='윗글의 밑줄 친 부분 중, 문맥상 낱말의 쓰임이 적절하지 않은 것은?',
  answer=3,
  evidence='Later, during the morning news on TV, a reporter … said, “Today’s Internet stories of the Heundeulbawi being damaged were fake.” Gina was … by the fact that she had spread the fake news.',
  explanation='지나가 공유한 흔들바위 소식이 가짜로 밝혀졌으므로, 자신이 가짜 뉴스를 퍼뜨렸다는 사실에 당황했다(embarrassed)는 흐름이어야 한다. ③의 pleased(기쁜)는 문맥에 맞지 않는다.',
  wrong={1: '헤드라인을 보고 확인 없이 곧바로(immediately) 공유했다는 흐름에 맞다.',
         2: '기자가 멀쩡한(undamaged) 흔들바위 옆에서 기사가 가짜라고 알리는 장면으로 적절하다.',
         4: '지나가 예전에 가짜 뉴스를 만들고 퍼뜨린 사람들을 비판했다(criticized)는 뜻으로 적절하다.',
         5: '가짜 뉴스는 사람들을 조종하려는 의도적인(deliberate) 시도라는 정의로 적절하다.'})


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
        'scope': {'kind': 'full', 'course': data['metadata']['course'], 'unit_ids': [u['id'] for u in data['units']]},
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
