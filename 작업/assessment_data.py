"""워크북 실전문제(Q01~Q05)와 미니 모의고사 3회(Q06~Q26) 원고.

지문·정답 위치는 원문에서 계산하고 question_source.build_view로 복원을 검증한다.
조립 코드는 영어2 능률(오) 2과 작업의 assessment_data.py와 같은 방식이다.

회차 편성 원칙: 한 회차 안에서 빈칸·어휘·순서·삽입·무관 문항의 정답 근거가 다른 문항 지문에
원형으로 드러나지 않도록 원문 구간을 나눈다(능률 2과 4단계 M·N 지적에서 얻은 기준).
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
q(id='Q01', set_id='workbook', number=1, unit_id='u1', type='주제', first='s01', last='s12',
  question='다음 글의 주제로 가장 적절한 것은?',
  choices=['the need to narrow the range of products sold through subscriptions',
           'the reasons outdated business models still work better than subscriptions',
           'ways for customers to obtain products without paying regularly',
           'the broadening of subscription services into many areas of daily life',
           'the latest technologies used to send fresh food to people’s homes'],
  answer=4,
  uses=[('u1-r2a', 1, 'narrow', '범위를 좁혀야 한다는 말이 모든 산업으로 넓어졌다는 본문과 반대임을 판단해야 함'),
        ('u1-r3a', 2, 'outdated', '구식(outdated) 사업 모델이 더 낫다는 말이 본문 흐름과 어긋남을 판단해야 함'),
        ('u1-r1s', 3, 'obtain', '정기적으로 돈을 내지 않고 얻는다(obtain)는 말이 정기 구독으로 비용을 낸다는 본문과 어긋남'),
        ('u1-r2s', 4, 'broadening', 'broaden(넓히다)의 뜻을 알아야 구독 서비스가 생활 곳곳으로 넓어졌다는 주제를 판단할 수 있음'),
        ('u1-r3h', 5, 'latest', '최신(latest) 기술은 본문에 없는 내용임을 판단해야 함'),
        ('u1-r1a', 5, 'send', '신선한 음식을 보내는(send) 일은 하루의 한 예일 뿐 주제가 아님')],
  evidence='To be sure, the subscription economy is a popular economic model nowadays, and Jiyun is actively taking part in it. / However, these business models have expanded to all industries, including entertainment, technology, fashion, education, and much more.',
  explanation='지윤이는 음악·아침 식사·공부·여가까지 하루 대부분을 구독 서비스로 채우고, 구독 경제는 요즘 인기 있는 모델이며, 처음에는 우유·신문에 한정되던 구독 모델이 이제 모든 산업으로 확장되었다고 한다. 따라서 구독 서비스가 일상생활의 많은 영역으로 넓어졌다는 ④가 주제다.',
  choices_ko=['구독으로 판매되는 제품의 범위를 좁혀야 할 필요성',
              '구식 사업 모델이 여전히 구독보다 더 잘 통하는 이유',
              '고객이 정기적으로 돈을 내지 않고 제품을 얻는 방법',
              '구독 서비스가 일상생활의 많은 영역으로 넓어지는 것',
              '사람들의 집으로 신선한 음식을 보내는 데 쓰이는 최신 기술'],
  wrong={1: '구독 모델이 모든 산업으로 확장되었다고 했으므로 범위를 좁혀야 한다는 것은 반대 내용이다.',
         2: '기업들이 한 번 팔고 끝나는 히트 상품 대신 지속적인 가치를 우선시한다고 했을 뿐, 구식 모델이 더 낫다는 내용은 없다.',
         3: '고객은 정기 구독을 통해 혜택의 비용을 지불한다고 했으므로 반대 내용이다.',
         5: '신선한 채소와 과일 배송은 지윤이 하루의 한 예일 뿐이고, 최신 기술은 언급되지 않는다.'})

q(id='Q02', set_id='workbook', number=2, unit_id='u2', type='내용', first='s07', last='s17',
  question='다음 글의 내용과 일치하지 않는 것은?',
  choices=['Companies can earn a steady rather than unstable income through subscriptions.',
           'Subscription models were at first limited to products like milk and newspapers.',
           'Companies now focus on offering continuing value instead of one-time hits.',
           'Consumers can save money by choosing adaptable subscription contracts.',
           'The growth of online platforms is described as gradual rather than swift.'],
  answer=5,
  uses=[('u2-r1s', 1, 'steady', 'stable(안정적인)과 같은 뜻인지 판단해야 일치 여부를 알 수 있음'),
        ('u2-r1a', 1, 'unstable', 'stable의 반대인 unstable을 부정하는 표현이 본문과 맞는지 판단해야 함'),
        ('u2-r2s', 4, 'adaptable', 'flexible(유연한)과 같은 뜻인지 판단해야 함'),
        ('u2-r3a', 5, 'gradual', 'rapid(급속한)와 반대되는 gradual(점진적인)이 본문과 어긋남을 알아야 함'),
        ('u2-r3s', 5, 'swift', 'swift(빠른)가 rapid와 같은 뜻임을 알아야 ‘빠르기보다 점진적’이라는 말이 틀렸음을 판단할 수 있음')],
  evidence='The rise of the subscription economy is closely connected to two major drivers: changes in consumption trends and the rapid growth of online platforms.',
  explanation='본문은 구독 경제의 부상이 소비 추세의 변화와 온라인 플랫폼의 급속한(rapid) 성장과 관련된다고 했다. 따라서 온라인 플랫폼의 성장이 빠르기보다 점진적이라고 한 ⑤는 본문과 일치하지 않는다.',
  choices_ko=['기업들은 구독을 통해 불안정한 수입이 아닌 꾸준한 수입을 얻을 수 있다.',
              '구독 모델은 처음에 우유와 신문 같은 제품에 한정되었다.',
              '기업들은 이제 일회성 히트 상품 대신 지속적인 가치를 제공하는 데 집중한다.',
              '소비자들은 융통성 있는 구독 계약을 선택해 돈을 절약할 수 있다.',
              '온라인 플랫폼의 성장은 빠르기보다 점진적인 것으로 묘사된다.'],
  wrong={1: '“Companies can have a stable revenue … by using the subscription model.”과 일치한다(stable = steady).',
         2: '“Initially it was limited to products such as milk and newspapers.”와 일치한다.',
         3: '“Instead of creating a hit product that will be sold once, companies now prioritize providing continuing value …”와 일치한다.',
         4: '“They can also save money by having flexible subscription contracts.”와 일치한다(flexible = adaptable).'})

q(id='Q03', set_id='workbook', number=3, unit_id='u3', type='제목', first='s18', last='s28',
  question='다음 글의 제목으로 가장 적절한 것은?',
  choices=['Owning More: The Limited Joy of Collecting Things',
           'Access over Ownership: Varied Experiences for Every Individual',
           'Uniform Products for Consumers with Uniform Tastes',
           'Why Precious Music Albums Are Still Worth Buying',
           'The Worthless Promise of Personalized Cosmetics'],
  answer=2,
  uses=[('u3-r2a', 1, 'Limited', 'limited(제한된)가 들어간 소유의 즐거움 이야기는 본문(소유보다 경험)과 초점이 다름을 판단해야 함'),
        ('u3-r1s', 2, 'Varied', 'diverse(다양한)와 같은 뜻의 varied가 다양성과 맞춤화라는 본문 내용을 담는지 판단해야 함'),
        ('u3-r1a', 3, 'Uniform', 'uniform(획일적인)이 개인 맞춤을 강조한 본문과 반대임을 알아야 함'),
        ('u3-r3s', 4, 'Precious', 'precious(소중한) 앨범을 사야 한다는 말이 앨범 없이 음악을 즐긴다는 본문과 어긋남'),
        ('u3-r3a', 5, 'Worthless', 'worthless(가치 없는)가 주목받는 인기 사례라는 본문과 반대임을 알아야 함')],
  evidence='More and more people prioritize experiences over owning things. / … it offers access to services or content without the requirement of ownership. / Moreover, consumers value diversity and customization. / … consumers receive a personalized experience that prioritizes their individual skin conditions …',
  explanation='사람들은 물건을 소유하기보다 경험을 중시하고, 구독은 소유 없이 서비스에 접근하게 해 준다. 또 소비자들은 다양성과 맞춤화를 중시해 자신의 취향에 맞는 경험을 고르며, 화장품 구독 서비스가 그 예다. 따라서 ‘소유보다 접근: 모든 개인을 위한 다양한 경험’이라는 ②가 제목으로 가장 적절하다.',
  choices_ko=['더 많이 소유하기: 물건 수집의 제한된 즐거움',
              '소유보다 접근: 모든 개인을 위한 다양한 경험',
              '획일적인 취향을 가진 소비자를 위한 획일적인 제품',
              '소중한 음악 앨범이 여전히 살 가치가 있는 이유',
              '개인 맞춤 화장품의 가치 없는 약속'],
  wrong={1: '본문은 사람들이 소유보다 경험을 중시한다는 점을 말할 뿐, 물건 수집의 즐거움을 다루지 않는다.',
         3: '소비자들이 다양성과 맞춤화를 중시하고 개인 취향에 맞는 경험을 받는다고 했으므로 반대 내용이다.',
         4: '음악 스트리밍 서비스를 구독하면 디스크 앨범을 가질 필요가 없다고 했으므로 반대 내용이다.',
         5: '화장품 구독 서비스는 주목받는 인기 사례로 소개되었으므로 가치 없다는 말은 반대 내용이다.'})

q(id='Q04', set_id='workbook', number=4, unit_id='u4', type='요지', first='s37', last='s43',
  question='다음 글의 요지로 가장 적절한 것은?',
  choices=['Online platforms offer only a tiny selection of standardized content.',
           'Consumers today still have few choices other than going to the theater.',
           'Online platforms make consumption easier and help companies offer tailored services that satisfy people.',
           'Companies need countless experts before they can build online platforms.',
           'An enormous number of choices lowers people’s satisfaction with services.'],
  answer=3,
  uses=[('u4-r2a', 1, 'tiny', 'vast(방대한)와 반대인 tiny(아주 작은)가 본문과 어긋남을 판단해야 함'),
        ('u4-r3a', 1, 'standardized', 'customized(맞춤형의)와 반대인 standardized(표준화된)가 본문과 어긋남을 판단해야 함'),
        ('u4-r1a', 2, 'few', '오늘날에는 누구나 방대한 영화를 즐길 수 있다는 본문과 few(거의 없는) 선택이 어긋남'),
        ('u4-r3s', 3, 'tailored', 'customized와 같은 뜻의 tailored를 알아야 맞춤형 서비스라는 요지를 판단할 수 있음'),
        ('u4-r1s', 4, 'countless', 'numerous와 같은 뜻의 countless(셀 수 없이 많은)가 본문에 없는 내용과 결합했음을 판단해야 함'),
        ('u4-r2s', 5, 'enormous', 'vast와 같은 뜻의 enormous가 들어 있어도 만족을 낮춘다는 내용은 본문과 반대임을 판단해야 함')],
  evidence='With the development of various digital devices centered on smartphones, consumers have been able to do numerous things with great ease. / At the same time, these platforms make it easy for companies to offer customized products and services to customers. / People appreciate having diverse choices and customization, which in turn enhances their satisfaction.',
  explanation='디지털 기기와 온라인 플랫폼 덕분에 소비자는 많은 일을 쉽게 할 수 있게 되었고, 플랫폼은 기업이 인공지능과 빅데이터로 소비자를 파악해 맞춤형 상품과 서비스를 제공하기 쉽게 해 주며, 이는 사람들의 만족을 높인다. 따라서 ③이 요지다.',
  choices_ko=['온라인 플랫폼은 표준화된 콘텐츠를 아주 조금만 제공한다.',
              '오늘날의 소비자들은 극장에 가는 것 말고는 여전히 선택권이 거의 없다.',
              '온라인 플랫폼은 소비를 더 쉽게 만들고 기업이 사람들을 만족시키는 맞춤형 서비스를 제공하도록 돕는다.',
              '기업들은 온라인 플랫폼을 만들기 전에 셀 수 없이 많은 전문가가 필요하다.',
              '엄청나게 많은 선택지는 서비스에 대한 사람들의 만족을 떨어뜨린다.'],
  wrong={1: '오늘날 누구나 엄청나게 다양한 영화를 즐길 수 있고 기업은 맞춤형 상품을 제공한다고 했으므로 반대 내용이다.',
         2: '극장에 가거나 비디오를 사야만 했던 것은 과거의 일이고, 오늘날에는 구독 플랫폼으로 영화를 즐긴다고 했다.',
         4: '플랫폼을 만드는 데 필요한 전문가 수는 본문에 나오지 않는다.',
         5: '다양한 선택과 맞춤화가 결과적으로 만족을 높인다고 했으므로 반대 내용이다.'})

q(id='Q05', set_id='workbook', number=5, unit_id='u5', type='주장', first='s49', last='s58',
  question='다음 글에서 필자가 주장하는 바로 가장 적절한 것은?',
  choices=['It is vital to be a wise consumer who subscribes only to what is really needed.',
           'Subscription services are so harmful that we should stop using them.',
           'Single-use packaging is the most helpful choice for regular deliveries.',
           'The cost of each subscription is too trivial to worry about.',
           'Companies should replace reusable packaging with cheaper materials.'],
  answer=1,
  uses=[('u5-r3s', 1, 'vital', 'crucial과 같은 뜻의 vital(매우 중요한)을 알아야 필자의 강조점을 판단할 수 있음'),
        ('u5-r2a', 2, 'harmful', 'beneficial의 반대인 harmful이 들어간 극단적 주장이 필자의 결론과 다름을 판단해야 함'),
        ('u5-r1s', 3, 'Single-use', 'disposable과 같은 뜻의 single-use 포장이 환경을 해친다는 본문과 어긋남을 판단해야 함'),
        ('u5-r2s', 3, 'helpful', 'helpful(도움이 되는)이 일회용 포장과 결합해 본문과 반대가 됨을 판단해야 함'),
        ('u5-r3a', 4, 'trivial', 'crucial의 반대인 trivial(사소한)이 비용을 신중히 고려하라는 본문과 어긋남'),
        ('u5-r1a', 5, 'reusable', 'reusable 포장을 쓰라는 본문과 반대되는 주장임을 판단해야 함')],
  evidence='It is important to carefully consider the costs of these subscriptions to avoid financial strain. / We need to have a deeper understanding of the subscription economy and become wise consumers who receive the services that are really needed.',
  explanation='필자는 구독의 재정적 부담과 환경 문제를 지적하고 비용을 신중히 따지며 불필요한 구독을 정리하라고 한 뒤, 구독 경제를 깊이 이해하고 정말 필요한 서비스만 받는 현명한 소비자가 되어야 한다고 결론짓는다. 따라서 ①이 필자의 주장이다.',
  choices_ko=['정말 필요한 것만 구독하는 현명한 소비자가 되는 것이 매우 중요하다.',
              '구독 서비스는 너무 해로워서 우리는 그것을 그만 써야 한다.',
              '일회용 포장은 정기 배송에 가장 도움이 되는 선택이다.',
              '구독 하나하나의 비용은 너무 사소해서 걱정할 필요가 없다.',
              '기업들은 재사용 가능한 포장을 더 값싼 재료로 바꿔야 한다.'],
  wrong={2: '필자는 구독 서비스가 이미 우리 삶에 깊이 자리 잡았다고 보고, 그만 쓰라는 것이 아니라 현명하게 쓰라고 한다.',
         3: '일회용 포장은 환경을 해친다고 했으므로 반대 내용이다.',
         4: '개별 비용은 감당할 만해 보여도 여러 개를 구독하면 빠르게 불어나므로 신중히 고려해야 한다고 했다.',
         5: '재사용 가능한 포장을 선택하는 것이 환경 문제를 줄이는 데 도움이 된다고 했으므로 반대 내용이다.'})


# ================================================================ 미니 모의고사 1회
q(id='Q06', set_id='mock1', number=1, type='내용', first='s13', last='s22',
  question='다음 글의 내용과 일치하는 것은?',
  choices=['Only consumers, not companies, benefit from the subscription economy.',
           'The subscription economy grew mainly because product prices fell.',
           'Fewer people today value experiences more than owning things.',
           'Music streaming requires consumers to buy disc albums first.',
           'Companies can gain a reliable income and keep customers loyal through subscriptions.'],
  answer=5,
  evidence='Companies can have a stable revenue and build customer loyalty by using the subscription model.',
  explanation='기업들은 구독 모델을 사용해 안정적인 수입을 얻고 고객 충성도를 쌓을 수 있다고 했다. 이를 ‘믿을 만한 수입을 얻고 고객을 충성스럽게 유지한다’로 바꾸어 표현한 ⑤가 본문과 일치한다.',
  choices_ko=['기업이 아니라 소비자만 구독 경제의 혜택을 받는다.',
              '구독 경제는 주로 제품 가격이 떨어졌기 때문에 성장했다.',
              '오늘날 소유보다 경험을 중시하는 사람은 더 적어지고 있다.',
              '음악 스트리밍을 이용하려면 소비자가 먼저 디스크 앨범을 사야 한다.',
              '기업들은 구독을 통해 믿을 만한 수입을 얻고 고객을 충성스럽게 유지할 수 있다.'],
  wrong={1: '구독 경제는 기업과 소비자 모두에게 이점을 가져다준다고 했다.',
         2: '구독 경제의 부상은 소비 추세의 변화와 온라인 플랫폼의 급속한 성장과 관련된다고 했을 뿐, 가격 하락은 나오지 않는다.',
         3: '점점 더 많은 사람이 소유보다 경험을 우선시한다고 했으므로 반대 내용이다.',
         4: '음악 스트리밍 서비스를 구독하면 디스크 앨범을 가질 필요 없이 음악을 즐긴다고 했다.'})

q(id='Q07', set_id='mock1', number=2, type='빈칸', first='s23', last='s32',
  blank='personalize their experiences based on their own preferences and interests',
  question='다음 빈칸에 들어갈 말로 가장 적절한 것은?',
  choices=['follow the same choices that most other people make',
           'tailor what they experience to their own tastes',
           'avoid sharing their personal information with companies',
           'own more products than they actually use',
           'stop paying for services they rarely use'],
  answer=2,
  evidence='Moreover, consumers value diversity and customization. / This aspect of the subscription economy is more popular among younger generations, as they enjoy expressing their uniqueness and discovering valuable content and services that fit with their individual tastes. / … consumers receive a personalized experience that prioritizes their individual skin conditions …',
  explanation='빈칸 앞에서 소비자들은 다양성과 맞춤화를 중시한다고 했고, 빈칸 뒤에서 젊은 세대가 고유함을 표현하고 개인 취향에 맞는 콘텐츠를 찾는 것을 즐긴다고 하며 개인 피부 상태에 맞춘 화장품 서비스를 예로 든다. 따라서 다양한 선택지가 개인이 자신의 취향에 맞게 경험을 맞출 수 있게 해 준다는 ②가 알맞다.',
  choices_ko=['대부분의 다른 사람들이 하는 것과 같은 선택을 따르다',
              '자신이 경험하는 것을 자신의 취향에 맞추다',
              '기업과 개인 정보를 공유하는 것을 피하다',
              '실제로 쓰는 것보다 더 많은 제품을 소유하다',
              '거의 쓰지 않는 서비스에 돈을 내는 것을 그만두다'],
  wrong={1: '뒤에서 고유함을 표현하고 개인 취향에 맞는 것을 찾는다고 했으므로 남들과 같은 선택을 따른다는 것은 반대다.',
         3: '개인 정보 공유는 본문에 나오지 않는다.',
         4: '글은 소유보다 맞춤화된 경험을 다루며, 더 많은 제품을 소유한다는 내용은 흐름과 맞지 않는다.',
         5: '필요한 것만 골라 돈을 절약하는 것은 뒤 단락의 유연성 이야기이고, 빈칸 뒤 This aspect가 가리키는 고유함·개인 취향과 이어지지 않는다.'})

q(id='Q08', set_id='mock1', number=3, type='순서', first='s01', last='s12',
  blocks=('s01', 's03', {'A': ('s10', 's12'), 'B': ('s04', 's06'), 'C': ('s07', 's09')}),
  question='주어진 글 다음에 이어질 글의 순서로 가장 적절한 것은?',
  answer=3,
  evidence='(B) “After school, Jiyun …”이 아침(주어진 글)에 이어지는 하루의 흐름 / (C) “To be sure, … Jiyun is actively taking part in it.”이 지윤이의 하루를 구독 경제로 일반화하고 “Initially it was limited …”로 끝남 / (A) “However, these business models have expanded …”가 (C)의 Initially와 대조됨.',
  explanation='주어진 글은 지윤이의 아침(음악 스트리밍, 아침 식사 배송)이다. (B) 방과 후와 주말의 구독 서비스 이용이 이어지고, (C) 구독 경제가 인기 있는 모델이며 지윤이도 참여하고 있다고 일반화한 뒤 처음에는 우유·신문에 한정되었다고 한다. (A) However로 이제 모든 산업으로 확장되었다는 내용이 온다. 따라서 (B)-(C)-(A)이다.',
  wrong={1: '(A)의 However, these business models …는 (C)의 “Initially it was limited …”와 대조되어야 하므로 주어진 글 바로 뒤에 올 수 없다.',
         2: '(B) 뒤에 (A)가 오면 these business models가 가리킬 대상과 Initially–However 대조가 없다.',
         4: '(C)를 주어진 글 바로 뒤에 두면 지윤이의 하루(방과 후·주말)가 일반화 뒤로 밀리고, (A) 뒤 (B)의 After school이 산업 확장 이야기와 이어지지 않는다.',
         5: '(C)–(B)–(A)는 (C)의 Initially 다음에 지윤이의 방과 후 이야기가 끼어 (A)의 However 대조가 끊긴다.'})

q(id='Q09', set_id='mock1', number=4, type='삽입', first='s33', last='s43', given='s38',
  slots=['s34', 's35', 's36', 's38', 's40'],
  question='글의 흐름으로 보아, 주어진 문장이 들어가기에 가장 적절한 곳은?',
  answer=4,
  evidence='With the development of various digital devices centered on smartphones, consumers have been able to do numerous things with great ease. ( ④ ) Today, whoever wants to watch a movie can access online media subscription platforms …',
  explanation='주어진 문장은 과거(In the past)에는 극장에 가거나 비디오를 사야만 했다는 내용이다. ④ 뒤의 Today(오늘날에는)로 시작하는 문장이 과거와 대비되는 오늘날의 모습을 보여 주므로, 기기 발전을 말한 문장과 Today 문장 사이인 ④에 들어가야 한다.',
  wrong={1: '앞뒤는 온라인 플랫폼 덕분에 몇 번의 클릭으로 서비스를 받는다는 편리함 이야기로, 과거의 영화 관람 방식이 끼어들 자리가 아니다.',
         2: '앞뒤는 클릭으로 서비스를 받고 기기 모델을 바꿀 수 있다는 내용으로 이어진다.',
         3: '앞뒤는 기기 변경과 업그레이드 이야기로 이어지며, 과거와 대비할 Today 문장이 바로 뒤에 오지 않는다.',
         5: '앞은 이미 Today로 오늘날을 말한 뒤이고, 뒤는 플랫폼이 기업에 주는 이점(At the same time)이라 과거 이야기가 들어갈 수 없다.'})

q(id='Q10', set_id='mock1', number=5, type='요지', first='s44', last='s52',
  question='다음 글의 요지로 가장 적절한 것은?',
  choices=['Since subscriptions can lead us to use and spend too much, we should manage them carefully.',
           'Subscriptions are the cheapest way to enjoy many different services.',
           'Signing up for similar services helps consumers compare their prices.',
           'The convenience of subscriptions has no effect on how much people consume.',
           'Companies should lower subscription fees to prevent overconsumption.'],
  answer=1,
  evidence='This can result in excessive consumption and using more subscription services than actually needed. It is crucial to subscribe only to services that are truly necessary … / It is important to carefully consider the costs of these subscriptions to avoid financial strain. Regularly reviewing and canceling unnecessary subscriptions can be beneficial.',
  explanation='구독의 편리함은 과소비로 이어질 수 있고, 여러 구독의 비용은 빠르게 불어나 재정적 부담이 된다. 그래서 필요한 서비스만 구독하고 비용을 신중히 따지며 불필요한 구독을 정리해야 한다고 한다. 따라서 ①이 요지다.',
  choices_ko=['구독은 우리가 너무 많이 쓰고 너무 많이 지출하게 할 수 있으므로 신중하게 관리해야 한다.',
              '구독은 많은 다양한 서비스를 즐기는 가장 저렴한 방법이다.',
              '비슷한 서비스에 가입하는 것은 소비자가 가격을 비교하는 데 도움이 된다.',
              '구독의 편리함은 사람들이 얼마나 소비하는지에 아무 영향을 주지 않는다.',
              '기업들은 과소비를 막기 위해 구독 요금을 낮춰야 한다.'],
  wrong={2: '개별 구독은 싸 보여도 여러 개를 구독하면 비용이 빠르게 불어난다고 했으므로 맞지 않는다.',
         3: '비슷한 서비스를 구독하는 것은 피하라고 했으므로 반대 내용이다.',
         4: '구독 모델의 편리함과 접근성 때문에 여러 서비스에 가입하고 많이 쓰게 된다고 했으므로 반대 내용이다.',
         5: '요금 인하는 본문에 나오지 않으며, 필자는 소비자가 구독을 관리해야 한다고 말한다.'})

q(id='Q11', set_id='mock1', number=6, type='제목', first='s44', last='s58', group='G1',
  question='윗글의 제목으로 가장 적절한 것은?',
  choices=['Subscriptions: Too Risky for Businesses to Adopt',
           'Eco-Friendly Packaging: The Secret of Subscription Success',
           'How to Earn Money by Offering More Subscriptions',
           'The Downsides of Subscriptions and How to Be a Smart Subscriber',
           'Why Subscription Prices Keep Falling Every Year'],
  answer=4,
  evidence='Although the subscription economy offers many advantages, there are also some disadvantages to consider. / … We need to have a deeper understanding of the subscription economy and become wise consumers who receive the services that are really needed.',
  explanation='구독 경제의 단점(과소비, 재정적 부담, 환경 오염)과 각각의 대처법을 제시한 뒤, 구독 경제를 깊이 이해하고 필요한 서비스만 받는 현명한 소비자가 되자고 결론짓는다. 따라서 ④가 제목으로 가장 적절하다.',
  choices_ko=['구독: 기업이 도입하기에는 너무 위험한 것',
              '친환경 포장: 구독 성공의 비밀',
              '더 많은 구독을 제공해 돈을 버는 방법',
              '구독의 단점과 현명한 구독자가 되는 방법',
              '구독 가격이 매년 계속 떨어지는 이유'],
  wrong={1: '점점 더 많은 기업이 구독 경제 모델에 뛰어들고 있다고 했으므로 맞지 않는다.',
         2: '친환경 포장은 환경 문제를 줄이는 한 가지 방법일 뿐 글 전체의 중심이 아니다.',
         3: '기업의 돈벌이 방법이 아니라 소비자가 겪는 단점과 현명한 소비를 다룬다.',
         5: '구독 가격이 떨어진다는 내용은 없으며, 오히려 여러 구독의 비용이 불어난다고 했다.'})

q(id='Q12', set_id='mock1', number=7, type='어휘', first='s44', last='s58', group='G1',
  marks=[('contribute', 's53'), ('increase', 's54'), ('reduce', 's55'), ('deeply', 's56'), ('wise', 's58')],
  replace=('increase', 'decrease'),
  question='윗글의 밑줄 친 부분 중, 문맥상 낱말의 쓰임이 적절하지 않은 것은?',
  answer=2,
  evidence='Additionally, the subscription economy can contribute to environmental pollution. / … which harms the environment. Using environmentally friendly packaging materials and opting for reusable packaging can help reduce this problem.',
  explanation='구독 경제가 환경 오염에 한몫할 수 있다고 한 뒤, 포장재에 담긴 제품의 정기 배송이 일회용 포장 사용을 늘려 환경을 해친다는 흐름이다. 따라서 ②의 decrease(줄이다)는 문맥에 맞지 않고 increase(늘리다)가 되어야 한다.',
  wrong={1: '구독 경제가 환경 오염에 한몫할(contribute) 수 있다는 단점 제시로 적절하다.',
         3: '친환경·재사용 포장이 이 문제를 줄이는(reduce) 데 도움이 된다는 흐름에 맞다.',
         4: '한계에도 불구하고 구독이 우리 삶에 깊이(deeply) 자리 잡았다는 뜻으로 적절하다.',
         5: '정말 필요한 서비스만 받는 현명한(wise) 소비자가 되자는 결론에 맞다.'})


# ================================================================ 미니 모의고사 2회
q(id='Q13', set_id='mock2', number=1, type='내용', first='s01', last='s09',
  question='다음 글의 내용과 일치하지 않는 것은?',
  choices=['Jiyun uses her smartphone to log in to a music service in the morning.',
           'A subscription service delivers fresh vegetables and fruits to Jiyun.',
           'Subscription-based business models are a completely new idea.',
           'Jiyun watches academic lectures to keep up with new knowledge.',
           'In the beginning, subscriptions covered only limited products like milk and newspapers.'],
  answer=3,
  evidence='The concept of business models based on subscriptions is not new.',
  explanation='구독에 기반한 비즈니스 모델의 개념은 새롭지 않다고 했으므로, 완전히 새로운 아이디어라고 한 ③은 본문과 일치하지 않는다.',
  choices_ko=['지윤이는 아침에 스마트폰으로 음악 서비스에 로그인한다.',
              '한 구독 서비스가 지윤이에게 신선한 채소와 과일을 배송한다.',
              '구독에 기반한 비즈니스 모델은 완전히 새로운 아이디어이다.',
              '지윤이는 새로운 지식을 따라잡기 위해 학술 강의를 시청한다.',
              '처음에는 구독이 우유와 신문 같은 한정된 제품에만 적용되었다.'],
  wrong={1: '“Jiyun … starts her day by logging in to a music streaming service on her smartphone.”과 일치한다.',
         2: '“Jiyun receives a delivery from a subscription service that provides fresh vegetables and fruits.”와 일치한다.',
         4: '“she watches various academic lectures to … stay updated about the latest knowledge …”와 일치한다.',
         5: '“Initially it was limited to products such as milk and newspapers.”와 일치한다.'})

q(id='Q14', set_id='mock2', number=2, type='빈칸', first='s07', last='s17',
  blank='expanded to all industries',
  question='다음 빈칸에 들어갈 말로 가장 적절한 것은?',
  choices=['disappeared from most modern markets',
           'stayed limited to milk and newspapers',
           'lost the trust of many companies',
           'become too expensive for consumers',
           'spread into almost every kind of business'],
  answer=5,
  evidence='Initially it was limited to products such as milk and newspapers. However, these business models have expanded to all industries, including entertainment, technology, fashion, education, and much more.',
  explanation='빈칸 앞 문장은 구독 모델이 처음에는 우유와 신문에 한정되었다고 하고, However로 방향을 바꾼 뒤 엔터테인먼트·기술·패션·교육 등을 예로 든다. 따라서 거의 모든 종류의 사업으로 퍼졌다는 ⑤가 알맞다.',
  choices_ko=['대부분의 현대 시장에서 사라졌다', '우유와 신문에 한정된 채로 남았다',
              '많은 기업의 신뢰를 잃었다', '소비자에게 너무 비싸졌다',
              '거의 모든 종류의 사업으로 퍼졌다'],
  wrong={1: '구독 경제가 요즘 인기 있는 모델이라고 했고 뒤에서 여러 산업을 예로 들었으므로 반대다.',
         2: 'However 앞의 ‘처음에는 한정되었다’와 대조되어야 하므로 그대로 한정되었다는 말은 흐름에 맞지 않는다.',
         3: '기업들은 이제 지속적인 가치를 우선시하며 구독 모델로 이점을 얻는다고 했다.',
         4: '뒤의 including 이하 산업 목록과 이어지지 않으며, 소비자는 유연한 계약으로 돈을 절약할 수 있다고 했다.'})

q(id='Q15', set_id='mock2', number=3, type='함축 의미', first='s11', last='s22',
  target='without filling up their drawers',
  question='밑줄 친 without filling up their drawers가 다음 글에서 의미하는 바로 가장 적절한 것은?',
  choices=['without having to buy and keep a lot of clothes',
           'without spending any money on clothing services',
           'without choosing the styles that they like',
           'without sharing their clothes with other people',
           'without cleaning their rooms on a regular basis'],
  answer=1,
  evidence='More and more people prioritize experiences over owning things. This makes the subscription economy attractive to them because it offers access to services or content without the requirement of ownership.',
  explanation='글은 사람들이 소유보다 경험을 중시하고, 구독이 소유할 필요 없이 서비스를 이용하게 해 준다고 설명한다. 의류 구독도 옷을 사서 서랍에 쌓아 두지 않고 여러 스타일을 경험하게 해 준다는 뜻이므로 ①이 알맞다.',
  choices_ko=['많은 옷을 사서 보관할 필요 없이', '의류 서비스에 돈을 전혀 쓰지 않고',
              '자신이 좋아하는 스타일을 고르지 않고', '다른 사람들과 옷을 나누어 입지 않고',
              '방을 정기적으로 청소하지 않고'],
  wrong={2: '고객은 정기 구독으로 혜택의 비용을 지불한다고 했으므로 돈을 전혀 쓰지 않는다는 것은 틀리다.',
         3: '소비자들이 다양한 의류 스타일을 탐색할 수 있다고 했으므로 스타일을 고르지 않는다는 말은 맞지 않는다.',
         4: '다른 사람과 옷을 나눈다는 내용은 본문에 없다.',
         5: '서랍은 옷을 소유해 쌓아 두는 것을 나타낸 말로, 방 청소와는 관계없다.'})

q(id='Q16', set_id='mock2', number=4, type='무관한 문장', first='s37', last='s43',
  addition='Movie theaters also sell popcorn and drinks to increase their profits.',
  add_before='s39', marks=['@added', 's39', 's40', 's41', 's42'],
  question='다음 글에서 전체 흐름과 관계 없는 문장은?',
  answer=1,
  evidence='In the past, people had no choice but to go to the theater or purchase the videos they wanted to watch. Today, whoever wants to watch a movie can access online media subscription platforms …',
  explanation='글은 디지털 기기와 온라인 플랫폼 덕분에 소비자는 쉽게 콘텐츠를 즐기고 기업은 맞춤형 서비스를 제공한다는 흐름이다. ①은 영화관이 팝콘과 음료를 팔아 이윤을 늘린다는 내용으로, 과거(In the past)와 오늘날(Today)을 대비하는 두 문장 사이를 끊는다.',
  wrong={2: '과거와 대비해 오늘날에는 누구나 구독 플랫폼으로 영화를 즐긴다는 핵심 내용이다.',
         3: '플랫폼이 기업의 맞춤형 상품 제공을 쉽게 해 준다는 둘째 요점을 연다.',
         4: '기업이 인공지능과 빅데이터로 소비자를 파악한다는 방법을 보여 준다.',
         5: '다양한 선택과 맞춤화가 만족을 높인다는 결과로 흐름을 잇는다.'})

q(id='Q17', set_id='mock2', number=5, type='순서', first='s44', last='s58',
  blocks=('s44', 's46', {'A': ('s49', 's52'), 'B': ('s53', 's58'), 'C': ('s47', 's48')}),
  question='주어진 글 다음에 이어질 글의 순서로 가장 적절한 것은?',
  answer=4,
  evidence='(C) “This can result in excessive consumption …”의 This가 주어진 글의 ‘여러 서비스에 쉽게 가입하고 많이 쓰게 되는 것’을 가리킴 / (A) “Related to the concern of overconsumption is the financial burden …” / (B) “Additionally, … environmental pollution.” → “Despite the potential limitations …”',
  explanation='주어진 글은 과소비 우려와 그 원인(쉽게 여러 서비스에 가입하고 많이 씀)을 말한다. (C) This로 그것이 과도한 소비로 이어진다고 하고 필요한 서비스만 구독하라고 한다. (A) 과소비 우려와 관련된 재정적 부담을 말하고, (B) Additionally로 환경 오염을 덧붙인 뒤 한계에도 불구하고 구독이 이미 삶에 깊이 자리 잡았고 앞으로도 커질 것으로 예상되므로 현명한 소비자가 되자고 결론짓는다. 따라서 (C)-(A)-(B)이다.',
  wrong={1: '(A) 다음에 (C)가 오면 (C)의 This가 (A) 끝의 ‘불필요한 구독을 검토하고 취소하는 것’을 가리키게 되어 과도한 소비를 초래한다는 말과 모순된다.',
         2: '(B)가 주어진 글 바로 뒤에 오면 Additionally가 첫 단점의 설명도 끝나기 전에 새 단점을 덧붙이고, 결론(Despite …) 뒤에 다시 단점이 이어진다.',
         3: '(B)의 결론 뒤에 (C)·(A)의 단점 설명이 이어질 수 없다.',
         5: '(C) 다음 (B)가 오면 결론(Despite … / We need to …) 뒤에 (A)의 재정적 부담이 이어져 흐름이 끊긴다.'})

q(id='Q18', set_id='mock2', number=6, type='제목', first='s23', last='s36', group='G2',
  question='윗글의 제목으로 가장 적절한 것은?',
  choices=['How Cosmetic Companies Test Their Products on Customers',
           'The Hidden Dangers of Online Shopping Platforms',
           'Personal and Flexible: What Consumers Love About Subscriptions',
           'Why Young People Avoid Subscription Services',
           'Fixed Prices: The End of Consumer Choice'],
  answer=3,
  evidence='Moreover, consumers value diversity and customization. / Furthermore, consumers appreciate flexibility and convenience.',
  explanation='소비자들이 구독을 좋아하는 이유로 다양성과 맞춤화(개인에게 맞춘 경험, 화장품 구독의 예), 유연성과 편리함(고정 비용 또는 필요한 것만 선택, 클릭 몇 번으로 이용·업그레이드)을 든다. 따라서 ③이 제목으로 가장 적절하다.',
  choices_ko=['화장품 회사들이 고객에게 제품을 시험하는 방법', '온라인 쇼핑 플랫폼의 숨겨진 위험',
              '개인 맞춤과 유연함: 소비자가 구독을 좋아하는 점', '젊은 사람들이 구독 서비스를 피하는 이유',
              '고정 가격: 소비자 선택의 종말'],
  wrong={1: '화장품 구독은 맞춤화의 한 예로, 제품 시험은 나오지 않는다.',
         2: '온라인 플랫폼 덕분에 클릭 몇 번으로 서비스나 제품을 받을 수 있다(With just a few clicks, consumers can receive services or products.)고 했으므로 반대 내용이다.',
         4: '구독의 이런 측면은 젊은 세대 사이에서 더 인기 있다고 했으므로 반대 내용이다.',
         5: '고정 비용 모델에서도 다양한 제품을 경험할 수 있고, 다른 모델에서는 필요한 것만 골라 조정할 수 있다고 했다.'})

q(id='Q19', set_id='mock2', number=7, type='어휘', first='s23', last='s36', group='G2',
  marks=[('diverse', 's24'), ('popular', 's25'), ('uniform', 's28'), ('flexibly', 's31'), ('easily', 's33')],
  replace=('easily', 'hardly'),
  question='윗글의 밑줄 친 부분 중, 문맥상 낱말의 쓰임이 적절하지 않은 것은?',
  answer=5,
  evidence='Moreover, subscription services are made easily accessible by online platforms, enhancing consumers’ convenience. With just a few clicks, consumers can receive services or products.',
  explanation='온라인 플랫폼이 구독 서비스를 이용하기 쉽게 만들어 소비자의 편리함을 높이고, 몇 번의 클릭만으로 서비스를 받을 수 있다는 흐름이다. 따라서 ⑤의 hardly(거의 ~않게)는 문맥에 맞지 않고 easily(쉽게)가 되어야 한다.',
  wrong={1: '구독 경제가 다양한(diverse) 구독 선택지를 제공한다는 흐름에 맞다.',
         2: '고유함을 표현하기 좋아하는 젊은 세대 사이에서 더 인기 있다(popular)는 흐름에 맞다.',
         3: '개인 맞춤 경험과 대비되는 획일적인(uniform) 구매 과정이라는 뜻으로 적절하다.',
         4: '필요한 것만 선택해 요금을 유연하게(flexibly) 조정한다는 흐름에 맞다.'})


# ================================================================ 미니 모의고사 3회
q(id='Q20', set_id='mock3', number=1, type='요약', first='s13', last='s22',
  summary='The subscription economy benefits both companies and consumers, and it is especially attractive to people who now value (A) more than (B).',
  question='다음 글의 내용을 한 문장으로 요약하고자 한다. 빈칸 (A), (B)에 들어갈 말로 가장 적절한 것은?',
  choices=['possession …… access',
           'access …… possession',
           'variety …… convenience',
           'access …… flexibility',
           'loyalty …… price'],
  answer=2,
  evidence='The subscription economy brings advantages for both companies and consumers. / More and more people prioritize experiences over owning things. This makes the subscription economy attractive to them because it offers access to services or content without the requirement of ownership.',
  explanation='구독 경제는 기업과 소비자 모두에게 이점을 주며, 사람들이 물건을 소유하는 것보다 경험을 중시하기 때문에 소유 없이 서비스에 접근하게 해 주는 구독이 매력적이다. 따라서 (A) access(접근), (B) possession(소유)인 ②가 알맞다.',
  choices_ko=['소유 …… 접근', '접근 …… 소유', '다양성 …… 편리함', '접근 …… 유연성', '충성도 …… 가격'],
  wrong={1: '사람들은 소유보다 경험(접근)을 중시한다고 했으므로 (A)와 (B)가 뒤바뀌었다.',
         3: '이 부분은 소유와 접근(경험)의 대비를 말하며, 다양성과 편리함의 비교는 나오지 않는다.',
         4: '(A) access는 맞지만 (B) flexibility는 사람들이 덜 중시하게 된 대상으로 본문에 나오지 않는다. 유연한 계약은 오히려 소비자의 이점이다.',
         5: '고객 충성도는 기업이 얻는 이점이고, 사람들이 충성도를 가격보다 중시한다는 내용은 없다.'})

q(id='Q21', set_id='mock3', number=2, type='순서', first='s23', last='s36',
  blocks=('s23', 's24', {'A': ('s29', 's32'), 'B': ('s25', 's28'), 'C': ('s33', 's36')}),
  question='주어진 글 다음에 이어질 글의 순서로 가장 적절한 것은?',
  answer=2,
  evidence='(B) “This aspect of the subscription economy …”가 주어진 글의 개인 맞춤(personalize) 측면을 가리킴 / (A) “Furthermore, consumers appreciate flexibility and convenience.” / (C) “Moreover, subscription services are made easily accessible …, enhancing consumers’ convenience.”',
  explanation='주어진 글은 소비자가 다양성과 맞춤화를 중시하고 구독 경제가 개인 맞춤을 가능하게 한다는 내용이다. (B) This aspect로 그 측면이 젊은 세대에게 인기라고 하고 화장품 구독을 예로 든다. (A) Furthermore로 유연성과 편리함이라는 새 이유를 내고 유연성의 예를 든 뒤, (C) Moreover로 편리함(온라인 플랫폼, 클릭 몇 번, 업그레이드)을 설명한다. 따라서 (B)-(A)-(C)이다.',
  wrong={1: '(A)가 주어진 글 바로 뒤에 오면 개인 맞춤 이야기가 끝나기 전에 Furthermore로 새 이유가 나오고, 맨 끝의 (B)에서 This aspect가 (C)의 온라인 접근성·기기 업그레이드를 가리키게 되어 고유함 표현·화장품 맞춤 이야기와 맞지 않는다.',
         3: '(C)가 (A)보다 앞서면 편리함을 먼저 설명한 뒤에야 (A)에서 ‘유연성과 편리함’이라는 이유가 처음 제시되어 어색하다.',
         4: '(C)가 주어진 글 바로 뒤에 올 수 없다. Moreover 다음 편리함 설명은 (A)의 ‘유연성과 편리함’ 제시 뒤에 와야 한다.',
         5: '(C)–(B)–(A)는 (B)의 This aspect가 (C)의 편리함을 가리키게 되어 맞지 않는다.'})

q(id='Q22', set_id='mock3', number=3, type='빈칸', first='s37', last='s43',
  blank='offer customized products and services to customers',
  question='다음 빈칸에 들어갈 말로 가장 적절한 것은?',
  choices=['sell exactly the same products to everyone',
           'hide their consumption patterns from customers',
           'reduce the number of choices for consumers',
           'provide goods and services suited to each person',
           'stop collecting information about customers'],
  answer=4,
  evidence='By applying AI and big data algorithm technology, companies identify consumers’ needs, tastes, and consumption patterns. / Services, such as suggesting personalized clothing styles … or recommending videos that match their movie and video viewing history …',
  explanation='빈칸 뒤에서 기업들은 인공지능과 빅데이터로 소비자의 요구와 취향을 파악하고, 구매 기록에 맞춘 옷 제안이나 시청 기록에 맞춘 영상 추천처럼 개인에게 맞춘 서비스를 제공한다. 따라서 플랫폼이 기업이 각 사람에게 맞는 상품과 서비스를 제공하기 쉽게 해 준다는 ④가 알맞다.',
  choices_ko=['모든 사람에게 정확히 같은 제품을 팔다', '고객에게 자신들의 소비 패턴을 숨기다',
              '소비자의 선택지 수를 줄이다', '각 사람에게 맞는 상품과 서비스를 제공하다',
              '고객에 관한 정보 수집을 멈추다'],
  wrong={1: '구매 기록과 시청 기록에 맞춘 개인 맞춤 서비스를 예로 들었으므로 모두에게 같은 제품을 판다는 것은 반대다.',
         2: '기업이 파악하는 것은 소비자의 소비 패턴이며, 기업이 무언가를 숨긴다는 내용은 없다.',
         3: '사람들은 다양한 선택을 환영하고 그것이 만족을 높인다고 했으므로 반대다.',
         5: '기업들은 인공지능과 빅데이터로 소비자 정보를 파악한다고 했으므로 반대다.'})

q(id='Q23', set_id='mock3', number=4, type='삽입', first='s44', last='s55', given='s47',
  slots=['s45', 's46', 's47', 's49', 's50'],
  question='글의 흐름으로 보아, 주어진 문장이 들어가기에 가장 적절한 곳은?',
  answer=3,
  evidence='The convenience and accessibility of the subscription model make it easy for consumers to sign up for multiple services and use a lot of content or products. ( ③ ) It is crucial to subscribe only to services that are truly necessary …',
  explanation='주어진 문장의 This는 여러 서비스에 쉽게 가입하고 콘텐츠·제품을 많이 쓰게 되는 상황을 가리키며, 그것이 과도한 소비로 이어진다고 말한다. 그 뒤에 필요한 서비스만 구독하라는 해결책이 이어지므로 ③에 들어가야 한다.',
  wrong={1: '앞은 단점이 있다는 도입이라 This가 가리킬 구체적 상황이 없고, 뒤 문장에서 비로소 과소비 우려가 제시된다.',
         2: '앞은 ‘과소비 가능성’이 우려라는 말뿐이라, 과소비가 과도한 소비를 초래한다는 동어 반복이 되며 원인 설명(편리함)보다 앞선다.',
         4: '앞은 필요한 서비스만 구독하라는 해결책이고 뒤는 재정적 부담이라는 새 우려로, 과도한 소비를 초래한다는 문장이 끼어들면 흐름이 끊긴다.',
         5: '앞뒤는 재정적 부담과 개별 비용 이야기로, This가 가리킬 대상이 맞지 않는다.'})

q(id='Q24', set_id='mock3', number=5, type='주장', first='s52', last='s58',
  question='다음 글에서 필자가 주장하는 바로 가장 적절한 것은?',
  choices=['Businesses should stop offering subscription services.',
           'Consumers should buy products instead of subscribing to them.',
           'Governments must ban all disposable packaging immediately.',
           'Companies should deliver products less often to cut costs.',
           'We should understand the subscription economy well and use only the services we need.'],
  answer=5,
  evidence='We need to have a deeper understanding of the subscription economy and become wise consumers who receive the services that are really needed.',
  explanation='불필요한 구독 정리, 친환경 포장 등 대처법을 말한 뒤, 구독 서비스가 삶에 깊이 자리 잡고 앞으로도 늘어날 것이므로 구독 경제를 깊이 이해하고 정말 필요한 서비스만 받는 현명한 소비자가 되어야 한다고 주장한다. 따라서 ⑤가 알맞다.',
  choices_ko=['기업들은 구독 서비스 제공을 멈춰야 한다.',
              '소비자들은 구독하는 대신 제품을 사야 한다.',
              '정부는 모든 일회용 포장을 즉시 금지해야 한다.',
              '기업들은 비용을 줄이기 위해 제품을 덜 자주 배송해야 한다.',
              '우리는 구독 경제를 잘 이해하고 필요한 서비스만 이용해야 한다.'],
  wrong={1: '점점 더 많은 기업이 구독 경제 모델에 뛰어들고 있다고 했을 뿐 멈추라고 하지 않았다.',
         2: '필자는 구독을 피하라는 것이 아니라 필요한 서비스를 현명하게 받으라고 한다.',
         3: '정부의 금지는 나오지 않으며, 친환경·재사용 포장을 쓰면 문제를 줄일 수 있다고 했다.',
         4: '배송 횟수를 줄이라는 내용은 없다.'})

q(id='Q25', set_id='mock3', number=6, type='제목', first='s01', last='s12', group='G3',
  question='윗글의 제목으로 가장 적절한 것은?',
  choices=['From Milk to Movies: Subscriptions in Everyday Life',
           'Jiyun’s Secret Recipe for a Healthy Breakfast',
           'Why Online Lectures Are Replacing Schools',
           'The Decline of the Subscription Economy',
           'How to Make a Hit Product That Sells Once'],
  answer=1,
  evidence='Jiyun is actively taking part in it. / Initially it was limited to products such as milk and newspapers. However, these business models have expanded to all industries …',
  explanation='지윤이의 하루(음악, 아침 식사, 강의, 영화)가 구독 서비스로 채워져 있고, 우유·신문에서 시작한 구독 모델이 이제 모든 산업으로 확장되었다는 내용이다. 따라서 ‘우유에서 영화까지: 일상 속 구독’이라는 ①이 제목으로 가장 적절하다.',
  choices_ko=['우유에서 영화까지: 일상생활 속 구독', '건강한 아침 식사를 위한 지윤이의 비밀 요리법',
              '온라인 강의가 학교를 대체하는 이유', '구독 경제의 쇠퇴',
              '한 번 팔리는 히트 상품을 만드는 방법'],
  wrong={2: '아침 식사는 구독 서비스 이용의 한 예일 뿐이다.',
         3: '지윤이는 학교 공부를 복습하려고 강의를 볼 뿐, 강의가 학교를 대체한다는 내용은 없다.',
         4: '구독 모델이 모든 산업으로 확장되었다고 했으므로 반대 내용이다.',
         5: '기업들은 한 번 팔리는 히트 상품 대신 지속적인 가치를 우선시한다고 했으므로 반대 내용이다.'})

q(id='Q26', set_id='mock3', number=7, type='어휘', first='s01', last='s12', group='G3',
  marks=[('healthy', 's03'), ('expand', 's04'), ('popular', 's07'), ('limited', 's09'), ('continuing', 's11')],
  replace=('popular', 'rare'),
  question='윗글의 밑줄 친 부분 중, 문맥상 낱말의 쓰임이 적절하지 않은 것은?',
  answer=3,
  evidence='To be sure, the subscription economy is a popular economic model nowadays, and Jiyun is actively taking part in it. / However, these business models have expanded to all industries …',
  explanation='지윤이처럼 하루 대부분을 구독 서비스로 채우는 사람이 있고, 구독 모델이 이제 모든 산업으로 확장되었다는 흐름이다. 따라서 ③의 rare(드문)는 문맥에 맞지 않고 popular(인기 있는)가 되어야 한다.',
  wrong={1: '건강한(healthy) 아침 식사를 위해 신선한 채소와 과일을 받는다는 흐름에 맞다.',
         2: '흥미로운 분야의 지식을 넓히기(expand) 위해 강의 서비스를 활용한다는 흐름에 맞다.',
         4: '처음에는 우유와 신문에 한정되었다(limited)는 뜻으로, 뒤의 However(모든 산업으로 확장)와 대조된다.',
         5: '한 번 팔리는 히트 상품과 대비되는 지속적인(continuing) 가치로 적절하다.'})


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
