"""공통 단위 3: People love the subscriptions (s18~s36, 단락 p05~p07; 짧은 단락이 있어 소제목 전체 묶음)."""
from author import S, link
from u1 import pp, v3

W = {'ownership': 'u3-w1', 'customization': 'u3-w2', 'personalize': 'u3-w3', 'uniqueness': 'u3-w4',
     'stand_out': 'u3-w5', 'address': 'u3-w6', 'accessible': 'u3-w7', 'enhance': 'u3-w8'}


def sentences(T):
    out = []

    # ---------------- s18 ----------------
    s = S('s18', T['s18'])
    s.ch('The subscription economy is highly relevant to', '구독 경제는 ~와 상당히 관련이 있다')
    s.ch('how people consume goods and services nowadays.', '요즘 사람들이 어떻게 재화와 서비스를 소비하는지.')
    s.natural('구독 경제는 요즘 사람들이 재화와 서비스를 소비하는 방식과 밀접한 관련이 있다.')
    s.cl('main', 'The', subj='The subscription economy', verbs=['is'])
    s.cl('subordinate', 'how', subj='people', verbs=['consume'], marker='how')
    s.g('subscription|economy', 'subscription economy', '구독 경제')
    s.g('is|relevant|to', 'be relevant to', '~와 관련이 있다')
    s.g('highly', 'highly', '상당히, 매우')
    s.glosses.sort(key=lambda g: g['spans'][0][0])
    s.g('how', 'how S′ V′', '어떻게 S′(이/가) V′하는지', at=s.text.index('how'))
    s.g('people', 'people', '사람들')
    s.g('consume', 'consume', '소비하다')
    s.g('goods', 'goods', '재화, 상품')
    s.g('services', 'services', '서비스들')
    s.g('nowadays', 'nowadays', '요즘')
    s.hint('[how people consume]', '[사람들이 어떻게 소비하는지]', span='how people consume', label='의문사 how 간접의문문',
           links=[(['how'], ['이', '어떻게', '는지'])], meaning='사람들이 어떻게 (재화와 서비스를) 소비하는지',
           explanation='전치사 to의 목적어인 간접의문문 how S′ V′: 어떻게 S′가 V′하는지. S′ people, V′ consume까지 표시하고 목적어 goods and services·nowadays는 제외.')
    s.review = '주절 be relevant to(사이 부사 highly) + 전치사 to의 목적어 간접의문문 how people consume … → 힌트. 수동 없음.'
    out.append(s)

    # ---------------- s19 ----------------
    s = S('s19', T['s19'])
    s.ch('More and more people prioritize experiences over owning things.', '점점 더 많은 사람들이 물건들을 소유하는 것보다 경험을 우선시한다.')
    s.natural('점점 더 많은 사람이 물건을 소유하는 것보다 경험을 우선시한다.')
    s.cl('main', 'More', subj='More and more people', verbs=['prioritize'])
    s.g('More|and|more', 'more and more', '점점 더 많은')
    s.g('people', 'people', '사람들')
    s.g('prioritize|over', 'prioritize A over B', 'B보다 A를 우선시하다',
        verb_construction={'kind': 'verb-frame', 'verb_span': s.span_of('prioritize'), 'lemma': 'prioritize',
                           'link_spans': [s.span_of('over')],
                           'review_record': 'prioritize experiences over owning things: A=experiences, B=owning things(동명사구).'})
    s.g('experiences', 'experiences', '경험들')
    s.glosses.sort(key=lambda g: g['spans'][0][0])
    f = s.g('owning', 'V-ing', '~하는 것', kind='function', combines_with=[], at=s.text.index('owning'))
    ow = s.g('owning', 'own', '소유하다', same=True, verb_form=pp('ing', s, 'owning', 'own'))
    link(f, ow)
    s.g('things', 'things', '물건들')
    s.hint('prioritize experiences over [owning things]', '[물건들을 소유하는 것]보다 경험을 우선시한다',
           span='prioritize experiences over owning things', label='prioritize A over B 구문',
           links=[(['prioritize', 'over'], ['보다', ('을', 1)])], emphasis_policy='ko-only-verb-construction',
           meaning='물건을 소유하는 것보다 경험을 우선시한다',
           explanation='prioritize A over B: B보다 A를 우선시하다. A=experiences, B=owning things(동명사구). 영어와 한국어의 A·B 어순이 바뀌어 연결을 놓치기 쉬워 선정. 동사 결합이라 한국어 조사만 강조.')
    s.review = '단일 주절. prioritize A over B(B는 전치사 over 뒤 동명사구) → 동사 구문 힌트(상위 문법 연결 없음). 수동 없음.'
    out.append(s)

    # ---------------- s20 ----------------
    s = S('s20', T['s20'])
    s.ch('This makes the subscription economy attractive to them', '이것은 구독 경제를 그들에게 매력적이게 만든다')
    s.ch('because it offers access', '왜냐하면 그것이 접근을 제공하기 때문에')
    s.ch('to services or content', '서비스나 콘텐츠에 대한')
    s.ch('without the requirement', '필요 없이')
    s.ch('of ownership.', '소유의.')
    s.natural('이러한 경향은 구독 경제를 그들에게 매력적으로 만드는데, 구독 경제는 소유할 필요 없이 서비스나 콘텐츠를 이용할 수 있게 해 주기 때문이다.')
    s.cl('main', 'This', subj='This', verbs=['makes'])
    s.cl('subordinate', 'because', subj='it', verbs=['offers'], marker='because')
    s.g('This', 'this', '이것은', referent_ko='물건을 소유하는 것보다 경험을 우선시하는 것')
    s.g('makes', 'make A B', 'A를 B하게 만들다', verb_form=v3(s, 'makes', 'make', 'This'),
        verb_construction={'kind': 'verb-frame', 'verb_span': s.span_of('makes'), 'lemma': 'make', 'link_spans': [],
                           'review_record': 'makes the subscription economy attractive: A=the subscription economy, B=attractive(형용사 보어).'})
    s.g('subscription|economy', 'subscription economy', '구독 경제')
    s.g('attractive', 'attractive', '매력적인')
    s.g('to', 'to', '~에게')
    s.g('them', 'them', '그들', referent_ko='경험을 우선시하는 점점 더 많은 사람들')
    s.g('because', 'because S′ V′', 'S′(이/가) V′하기 때문에')
    s.g('it', 'it', '그것이', referent_ko='구독 경제')
    s.g('offers', 'offer', '제공하다', verb_form=v3(s, 'offers', 'offer', 'it'))
    s.g('access', 'access', '접근, 이용 (권한)')
    s.g('to', 'to', '~에 대한', at=s.text.index('to services'))
    s.g('services', 'services', '서비스들')
    s.g('or', 'or', '또는')
    s.g('content', 'content', '콘텐츠')
    s.g('without', 'without', '~ 없이')
    s.g('requirement', 'requirement', '필요, 필요 조건')
    s.g('of', 'of', '~의')
    s.g('ownership', 'ownership', '소유', star=W['ownership'])
    s.brk('to', 'postnominal-preposition', 'to services or content는 앞 명사 access를 뒤에서 꾸미는 전치사구', after=s.text.index('access'))
    s.brk('of', 'postnominal-preposition', 'of ownership은 앞 명사 the requirement를 뒤에서 꾸미는 전치사구')
    s.hint('[because it offers]', '[그것[구독 경제]이 제공하기 때문에]', span='because it offers', label='이유 접속사 because',
           links=[(['because'], ['이', '기 때문에'])], refs=[('it', '그것', '[구독 경제]')],
           meaning='그것이 (소유 없이 서비스나 콘텐츠에 대한 접근을) 제공하기 때문에',
           explanation='because S′ V′: S′가 V′하기 때문에. S′ it(구독 경제), V′ offers까지 표시하고 목적어 access 이하는 제외.')
    s.hint('makes the subscription economy [attractive]', '구독 경제를 [매력적이게] 만든다', span='makes the subscription economy attractive',
           label='make A B 구문', links=[(['makes'], ['를', '이게'])], emphasis_policy='ko-only-verb-construction',
           meaning='구독 경제를 매력적이게 만든다',
           explanation='make A B: A를 B하게 만들다. A=the subscription economy, B=attractive(형용사). 목적어 뒤 형용사가 A의 상태를 나타낸다.')
    s.review = ('주절 make A B(A=the subscription economy, B=attractive, to them은 attractive의 보충) + 이유 부사절 because. '
                'access to …, the requirement of … 후치수식 앞에서 끊음. 힌트 2개(because 절, make A B). 수동 없음.')
    out.append(s)

    # ---------------- s21 ----------------
    s = S('s21', T['s21'])
    s.ch('For example,', '예를 들어,')
    s.ch('by subscribing to a music streaming service,', '음악 스트리밍 서비스를 구독함으로써,')
    s.ch('consumers can enjoy limitless music', '소비자들은 무한한 음악을 즐길 수 있다')
    s.ch('without the need', '필요 없이')
    s.ch('for having disc albums.', '디스크 앨범들을 가지는 것에 대한.')
    s.natural('예를 들어, 음악 스트리밍 서비스를 구독하면 소비자들은 디스크 앨범을 가질 필요 없이 무한한 음악을 즐길 수 있다.')
    s.cl('main', 'For', subj='consumers', verbs=['can', 'enjoy'])
    s.g('For|example', 'for example', '예를 들어')
    f = s.g('by', 'by V-ing', '~함으로써', kind='function', combines_with=[])
    sb = s.g('subscribing|to', 'subscribe to', '~을 구독하다', verb_form=pp('ing', s, 'subscribing', 'subscribe'))
    link(f, sb)
    s.g('music', 'music', '음악')
    s.g('streaming', 'streaming', '스트리밍')
    s.g('service', 'service', '서비스')
    s.g('consumers', 'consumers', '소비자들')
    f2 = s.g('can', 'can V', '~할 수 있다', kind='function', combines_with=[])
    ej = s.g('enjoy', 'enjoy', '즐기다')
    link(f2, ej)
    s.g('limitless', 'limitless', '무한한, 끝없는')
    s.g('music', 'music', '음악', at=s.text.index('music without'))
    s.g('without', 'without', '~ 없이')
    s.g('need', 'need', '필요')
    s.g('for', 'for', '~에 대한')
    f3 = s.g('having', 'V-ing', '~하는 것', kind='function', combines_with=[])
    hv = s.g('having', 'have', '가지다', same=True, verb_form=pp('ing', s, 'having', 'have'))
    link(f3, hv)
    s.g('disc|albums', 'disc albums', '디스크 앨범들 (CD 음반)')
    s.brk('for', 'postnominal-preposition', 'for having disc albums는 앞 명사 the need를 뒤에서 꾸미는 전치사구')
    s.hint('[by subscribing to]', '[구독함으로써]', span='by subscribing to', label='전치사 by + 동명사',
           links=[(['by', 'ing'], ['함으로써'])], meaning='(음악 스트리밍 서비스를) 구독함으로써',
           explanation='문두 전치사 by + 동명사 subscribing to: ~함으로써(수단). 대상 a music streaming service는 표시에서 제외.')
    s.review = ('문두 by + 동명사구(수단) + 주절 can enjoy. the need for having …의 for 앞 후치수식 경계. 힌트 1개(by + 동명사). 관계사·수동 없음.')
    out.append(s)

    # ---------------- s22 ----------------
    s = S('s22', T['s22'])
    s.ch('Another example is subscribing to clothing services,', '또 다른 예는 의류 서비스들을 구독하는 것이다,')
    s.ch('where consumers can explore', '그리고 그곳에서 소비자들은 탐색할 수 있다')
    s.ch('a variety of clothing styles', '다양한 의류 스타일들을')
    s.ch('without filling up their drawers.', '그들의 서랍들을 가득 채우지 않고.')
    s.natural('또 다른 예는 의류 서비스를 구독하는 것인데, 거기서 소비자들은 서랍을 가득 채우지 않고도 다양한 의류 스타일을 탐색할 수 있다.')
    s.cl('main', 'Another', subj='Another example', verbs=['is'])
    s.cl('subordinate', 'where', subj='consumers', verbs=['can', 'explore'], marker='where')
    s.g('Another', 'another', '또 다른')
    s.g('example', 'example', '예, 사례')
    s.g('is', 'is', '~이다')
    f = s.g('subscribing', 'V-ing', '~하는 것', kind='function', combines_with=[])
    sb = s.g('subscribing|to', 'subscribe to', '~을 구독하다', same=True, verb_form=pp('ing', s, 'subscribing', 'subscribe'))
    link(f, sb)
    s.g('clothing', 'clothing', '의류, 옷')
    s.g('services', 'services', '서비스들')
    rel = s.g('where', ', where S′ V′', '그리고 그곳에서 S′(이/가) V′하다 (관계부사)')
    s.g('consumers', 'consumers', '소비자들')
    f2 = s.g('can', 'can V', '~할 수 있다', kind='function', combines_with=[])
    ex = s.g('explore', 'explore', '탐색하다, 둘러보다')
    link(f2, ex)
    q = s.g('a variety of', 'a variety of', '다양한')
    s.g('clothing', 'clothing', '의류, 옷', at=s.text.index('clothing styles'))
    s.g('styles', 'styles', '스타일들')
    f3 = s.g('without', 'without V-ing', '~하지 않고', kind='function', combines_with=[])
    fl = s.g('filling|up', 'fill up', '가득 채우다', verb_form=pp('ing', s, 'filling', 'fill'))
    link(f3, fl)
    s.g('their', 'their', '그들의', referent_ko='소비자들')
    s.g('drawers', 'drawers', '서랍들')
    s.prot('a variety of', 'quantity-kind-of', '수량·종류 표현 a variety of가 뒤 명사 clothing styles 앞에서 ‘다양한’으로 같은 어순 대응', gloss=q)
    s.hint('clothing services, [where consumers can explore]', '의류 서비스들, [그리고 그곳에서 소비자들이 탐색할 수 있다]',
           span='clothing services, where consumers can explore', label='계속적 관계부사 where',
           links=[(['where'], ['그리고 그곳에서', '이'])], meaning='의류 서비스들, 그리고 그곳에서 소비자들이 (다양한 의류 스타일을) 탐색할 수 있다',
           explanation='콤마 뒤 관계부사 where가 선행사 clothing services(구독하는 의류 서비스)를 받아 ‘그리고 그곳에서’로 설명을 덧붙인다. S′ consumers, V′ can explore까지 표시하고 목적어 a variety of … 이하는 제외.')
    s.hint('[without filling up]', '[가득 채우지 않고]', span='without filling up', label='전치사 without + 동명사',
           links=[(['without', 'ing'], ['지 않고'])], meaning='(그들의 서랍을) 가득 채우지 않고',
           explanation='without + 동명사 filling up: ~하지 않고. 목적어 their drawers는 표시에서 제외.')
    s.relative_ids = [rel['id']]
    s.review = ('주절 is + 보어 동명사구 subscribing to clothing services + 계속적 관계부사 where(선행사 clothing services, 서비스 안에서의 상황) + without + 동명사. '
                '관계부사 where의 뜻은 추가 설명 문맥이라 ‘그리고 그곳에서’. 힌트 2개(관계부사, without + 동명사). 수동 없음.')
    out.append(s)

    # ---------------- s23 ----------------
    s = S('s23', T['s23'])
    s.ch('Moreover,', '게다가,')
    s.ch('consumers value diversity and customization.', '소비자들은 다양성과 맞춤화를 가치 있게 여긴다.')
    s.natural('게다가 소비자들은 다양성과 맞춤화를 중요하게 여긴다.')
    s.cl('main', 'consumers', subj='consumers', verbs=['value'])
    s.g('Moreover', 'moreover', '게다가')
    s.g('consumers', 'consumers', '소비자들')
    s.g('value', 'value', '가치 있게 여기다, 중시하다 (흔한 뜻: 가치)')
    s.g('diversity', 'diversity', '다양성')
    s.g('customization', 'customization', '맞춤화 (개인에게 맞게 바꾸는 것)', star=W['customization'])
    s.review = '단일 주절, value는 동사(중시하다). 관계사·접속사절·수동 없음 → 힌트 없음.'
    out.append(s)

    # ---------------- s24 ----------------
    s = S('s24', T['s24'], key=True)
    s.ch('The subscription economy offers', '구독 경제는 제공한다')
    s.ch('a diverse range of subscription options,', '다양한 범위의 구독 선택지들을,')
    s.ch('enabling individuals to personalize their experiences', '개인들이 그들의 경험을 개인 맞춤화할 수 있게 해 주면서')
    s.ch('based on their own preferences and interests.', '그들 자신의 선호와 관심사에 기초하여.')
    s.natural('구독 경제는 다양한 구독 선택지를 제공하여, 개인들이 자신의 선호와 관심사에 따라 경험을 개인 맞춤화할 수 있게 해 준다.')
    s.cl('main', 'The', subj='The subscription economy', verbs=['offers'])
    s.g('subscription|economy', 'subscription economy', '구독 경제')
    s.g('offers', 'offer', '제공하다', verb_form=v3(s, 'offers', 'offer', 'The subscription economy'))
    q = s.g('a diverse range of', 'a diverse range of', '다양한 범위의')
    s.g('subscription', 'subscription', '구독', at=s.text.index('subscription options'))
    s.g('options', 'options', '선택지들, 선택 사항들')
    f = s.g('enabling', 'V-ing', '~하면서', kind='function', combines_with=[])
    en = s.g('enabling|to', 'enable A to V', 'A(이/가) ~할 수 있게 해 주다', same=True,
             verb_form=pp('ing', s, 'enabling', 'enable'),
             verb_construction={'kind': 'verb-frame', 'verb_span': s.span_of('enabling'), 'lemma': 'enable',
                                'link_spans': [s.span_of('to', s.text.index('enabling'))],
                                'review_record': 'enabling individuals to personalize: A=individuals, to V=to personalize.'})
    link(f, en)
    s.g('individuals', 'individuals', '개인들')
    s.glosses.sort(key=lambda g: g['spans'][0][0])
    s.g('personalize', 'personalize', '개인 맞춤화하다, 개인에게 맞추다', star=W['personalize'], at=s.text.index('personalize'))
    s.g('their', 'their', '그들의', referent_ko='개인들')
    s.g('experiences', 'experiences', '경험들')
    s.g('based|on', 'based on', '(~에) 기초하여', verb_form=pp('past-participle', s, 'based', 'base'))
    s.g('their|own', 'their own', '그들 자신의', referent_ko='개인들', at=s.text.index('their own'))
    s.g('preferences', 'preferences', '선호들, 취향들')
    s.g('interests', 'interests', '관심사들')
    s.prot('a diverse range of', 'quantity-kind-of', '범위 표현 a diverse range of가 뒤 명사 subscription options 앞에서 ‘다양한 범위의’로 같은 어순 대응', gloss=q)
    s.hint('enabling individuals [to personalize]', '개인들이 [개인 맞춤화할 수 있게] 해 주면서', span='enabling individuals to personalize',
           label='enable A to V 구문', links=[(['enabling', 'to'], ['이', '수 있게'])], emphasis_policy='ko-only-verb-construction',
           meaning='개인들이 (그들의 경험을) 개인 맞춤화할 수 있게 해 주면서',
           explanation='분사 enabling이 이끄는 부분에서 enable A to V: A가 ~할 수 있게 해 주다. A=individuals, to V=to personalize. 목적어 their experiences는 표시에서 제외.')
    s.review = ('단일 주절 offers + 콤마 뒤 분사구 enabling A to V(선택지를 제공하면서 덧붙는 일, ~하면서) + based on …(personalize의 기준). '
                'a diverse range of는 같은 어순 ~의 범위 표현. 힌트 1개(enable A to V; 분사 연결은 한국어 ~하면서로 함께 보임). 관계사·수동 없음.')
    out.append(s)

    # ---------------- s25 ----------------
    s = S('s25', T['s25'])
    s.ch('This aspect', '이 측면은')
    s.ch('of the subscription economy', '구독 경제의')
    s.ch('is more popular among younger generations,', '더 젊은 세대들 사이에서 더 인기가 있다,')
    s.ch('as they enjoy expressing their uniqueness', '그들이 그들의 고유함을 표현하는 것을 즐기기 때문에')
    s.ch('and discovering valuable content and services', '그리고 가치 있는 콘텐츠와 서비스들을 발견하는 것을')
    s.ch('that fit with their individual tastes.', '그들의 개인적인 취향에 맞는.')
    s.natural('구독 경제의 이러한 측면은 젊은 세대 사이에서 더 인기가 있는데, 그들은 자신의 고유함을 표현하고 개인 취향에 맞는 가치 있는 콘텐츠와 서비스를 발견하는 것을 즐기기 때문이다.')
    s.cl('main', 'This', subj='This aspect of the subscription economy', verbs=['is'], disp='This aspect',
         disp_review='중심명사 aspect까지 표시하고 뒤수식 of the subscription economy는 제외')
    s.cl('subordinate', 'as', subj='they', verbs=['enjoy'], marker='as')
    s.cl('subject_relative', 'that', verbs=['fit'], marker='that')
    s.g('This', 'this', '이')
    s.g('aspect', 'aspect', '측면')
    s.g('of', 'of', '~의')
    s.g('subscription|economy', 'subscription economy', '구독 경제')
    s.g('is', 'is', '~이다')
    s.g('more', 'more', '더')
    s.g('popular', 'popular', '인기 있는')
    s.g('among', 'among', '~ 사이에서')
    s.g('younger', 'younger', '더 젊은 (young의 비교급)')
    s.g('generations', 'generations', '세대들')
    s.g('as', 'as S′ V′', 'S′(이/가) V′하기 때문에')
    s.g('they', 'they', '그들이', referent_ko='젊은 세대들')
    s.g('enjoy', 'enjoy V-ing', 'V-ing하는 것을 즐기다',
        verb_construction={'kind': 'verb-frame', 'verb_span': s.span_of('enjoy'), 'lemma': 'enjoy', 'link_spans': [],
                           'review_record': 'enjoy expressing … and discovering …: 동명사 목적어 두 개. V-ing 연결 뜻은 이 구문이 제공.'})
    s.g('expressing', 'express', '표현하다', verb_form=pp('ing', s, 'expressing', 'express'))
    s.g('their', 'their', '그들의', referent_ko='젊은 세대들')
    s.g('uniqueness', 'uniqueness', '고유함, 독특함', star=W['uniqueness'])
    s.g('discovering', 'discover', '발견하다', verb_form=pp('ing', s, 'discovering', 'discover'))
    s.g('valuable', 'valuable', '가치 있는')
    s.g('content', 'content', '콘텐츠')
    s.g('services', 'services', '서비스들')
    rel = s.g('that', 'that V′', 'V′하는 (관계대명사)')
    s.g('fit|with', 'fit with', '~에 맞다, ~와 어울리다')
    s.g('their', 'their', '그들의', referent_ko='젊은 세대들', at=s.text.index('their individual'))
    s.g('individual', 'individual', '개인적인, 개개인의')
    s.g('tastes', 'tastes', '취향들 (흔한 뜻: 맛)')
    s.brk('of', 'postnominal-preposition', 'of the subscription economy는 앞 명사 This aspect를 뒤에서 꾸미는 전치사구')
    s.hint('[as they enjoy]', '[그들[젊은 세대들]이 즐기기 때문에]', span='as they enjoy', label='이유 접속사 as',
           links=[(['as'], ['이', '기 때문에'])], refs=[('they', '그들', '[젊은 세대들]')],
           meaning='그들이 (고유함을 표현하고 콘텐츠를 발견하는 것을) 즐기기 때문에',
           explanation='as S′ V′: S′가 V′하기 때문에(이유). 앞 절의 ‘젊은 세대 사이에서 더 인기 있다’의 이유를 댄다. S′ they, V′ enjoy까지 표시하고 동명사 목적어는 제외.')
    s.hint('valuable content and services [that fit with]', '[맞는] 가치 있는 콘텐츠와 서비스들', span='valuable content and services that fit with',
           label='주격 관계대명사 that', links=[(['that'], ['는'])],
           meaning='(그들의 개인적인 취향에) 맞는 가치 있는 콘텐츠와 서비스들',
           explanation='선행사 valuable content and services를 주격 관계대명사 that이 받아 fit with their individual tastes가 꾸민다. V′ fit with까지 표시하고 대상 their individual tastes는 제외.')
    s.relative_ids = [rel['id']]
    s.review = ('주절 is more popular(주어 표시 This aspect) + as 부사절(문맥상 이유: 젊은 세대가 더 좋아하는 까닭) + 동명사 목적어 expressing·discovering 병렬 + 주격 관계절 that fit with. '
                'as는 ‘~함에 따라’로도 읽을 수 있으나 앞 절의 이유를 대는 흐름이라 이유로 판정. 2단계 L 검수(Lb 특별 확인)에서 이유 유지로 판정: as절 enjoy는 상태동사 단순현재라 변화·비례 뜻이 없고 주절 more popular among younger generations는 세대 비교라 비례가 성립하지 않음. 힌트 2개(as 절, 필수 관계사). 수동 없음.')
    out.append(s)

    # ---------------- s26 ----------------
    s = S('s26', T['s26'])
    s.ch('A popular example', '인기 있는 사례는')
    s.ch('that has gained attention', '주목을 얻어 온')
    s.ch('is the cosmetics subscription service.', '화장품 구독 서비스이다.')
    s.natural('주목받고 있는 인기 사례는 화장품 구독 서비스이다.')
    s.cl('main', 'A', subj='A popular example that has gained attention', verbs=['is'], disp='A popular example',
         disp_review='앞수식어 popular와 중심명사 example까지 표시하고 뒤 관계절 that has gained attention은 제외')
    s.cl('subject_relative', 'that', verbs=['has', 'gained'], marker='that')
    s.g('popular', 'popular', '인기 있는')
    s.g('example', 'example', '사례, 예')
    rel = s.g('that', 'that V′', 'V′하는 (관계대명사)')
    f = s.g('has', 'have p.p.', '~해 왔다', kind='function', combines_with=[])
    gn = s.g('gained', 'gain', '얻다 (gained는 gain의 p.p.형)', verb_form=pp('perfect-participle', s, 'gained', 'gain', f['id']))
    link(f, gn)
    s.g('attention', 'attention', '주목, 관심')
    s.g('is', 'is', '~이다')
    s.g('cosmetics', 'cosmetics', '화장품')
    s.g('subscription', 'subscription', '구독')
    s.g('service', 'service', '서비스')
    s.hint('A popular example [that has gained]', '[얻어 온] 인기 있는 사례', span='A popular example that has gained',
           label='주격 관계대명사 that', links=[(['that'], ['온'])],
           meaning='(주목을) 얻어 온 인기 있는 사례',
           explanation='선행사 A popular example을 주격 관계대명사 that이 받아 has gained attention이 꾸민다. 주격이라 V′ has gained까지만 표시하고 목적어 attention은 제외.')
    s.relative_ids = [rel['id']]
    s.review = ('주절 is(주어 표시 A popular example) + 주격 관계절 that has gained attention → 필수 관계사 힌트. '
                '능동 완료 has gained는 관계사 힌트 표시 범위 안에 있어 결합 힌트를 따로 두지 않고 분석 보충 u3-gp4로 연결.')
    out.append(s)

    # ---------------- s27 ----------------
    s = S('s27', T['s27'], key=True)
    s.ch('It stands out', '그것은 두드러진다')
    s.ch('by thoroughly analyzing customers’ current skin conditions', '고객들의 현재 피부 상태를 철저히 분석함으로써')
    s.ch('and providing specialized recommendations,', '그리고 전문화된 추천들을 제공함으로써,')
    s.ch('including manufacturing cosmetics', '화장품을 제조하는 것을 포함하여')
    s.ch('created to address each individual’s unique skin concerns.', '각 개인의 고유한 피부 고민들을 해결하기 위해 만들어진.')
    s.natural('그것은 고객의 현재 피부 상태를 철저히 분석하고, 각 개인의 고유한 피부 고민을 해결하기 위해 만든 화장품의 제조까지 포함한 전문적인 추천을 제공한다는 점에서 돋보인다.')
    s.cl('main', 'It', subj='It', verbs=['stands out'])
    s.g('It', 'it', '그것은', referent_ko='화장품 구독 서비스')
    s.g('stands|out', 'stand out', '두드러지다, 돋보이다', star=W['stand_out'],
        verb_form=v3(s, 'stands', 'stand', 'It'))
    f = s.g('by', 'by V-ing', '~함으로써', kind='function', combines_with=[])
    s.g('thoroughly', 'thoroughly', '철저히')
    an = s.g('analyzing', 'analyze', '분석하다', verb_form=pp('ing', s, 'analyzing', 'analyze'))
    s.g('customers’', 'customers’', '고객들의')
    s.g('current', 'current', '현재의')
    s.g('skin', 'skin', '피부')
    s.g('conditions', 'conditions', '상태들 (흔한 뜻: 조건들)')
    pv = s.g('providing', 'provide', '제공하다', verb_form=pp('ing', s, 'providing', 'provide'))
    link(f, an, pv)
    s.g('specialized', 'specialized', '전문화된, 특화된', verb_form=pp('past-participle', s, 'specialized', 'specialize'))
    s.g('recommendations', 'recommendations', '추천들')
    s.g('including', 'including', '~을 포함하여')
    f2 = s.g('manufacturing', 'V-ing', '~하는 것', kind='function', combines_with=[])
    mf = s.g('manufacturing', 'manufacture', '제조하다', same=True, verb_form=pp('ing', s, 'manufacturing', 'manufacture'))
    link(f2, mf)
    s.g('cosmetics', 'cosmetics', '화장품')
    cr = s.g('created', 'created', '만들어진', verb_form=pp('past-participle', s, 'created', 'create'))
    f3 = s.g('to', 'to V', '~하기 위해', kind='function', combines_with=[])
    ad = s.g('address', 'address', '해결하다, 다루다 (흔한 뜻: 주소)', star=W['address'])
    link(f3, ad)
    s.g('each', 'each', '각각의')
    s.g('individual’s', 'individual’s', '개인의')
    s.g('unique', 'unique', '고유한, 독특한')
    s.g('skin', 'skin', '피부', at=s.text.index('skin concerns'))
    s.g('concerns', 'concerns', '고민들, 걱정거리들')
    s.brk('including', 'postnominal-preposition', 'including … 이하는 앞 명사 specialized recommendations의 예를 드는 전치사구')
    s.hint('[by thoroughly analyzing customers’ current skin conditions and providing]',
           '[고객들의 현재 피부 상태를 철저히 분석하고 제공함으로써]',
           span='by thoroughly analyzing customers’ current skin conditions and providing', label='전치사 by + 동명사',
           links=[(['by', 'ing', ('ing', 1)], ['함으로써'])],
           meaning='고객들의 현재 피부 상태를 철저히 분석하고 (전문화된 추천을) 제공함으로써',
           explanation='전치사 by 뒤에 동명사 analyzing과 providing이 and로 병렬되어 둘 다 ~함으로써에 걸린다. 병렬 두 동명사를 보이려고 providing까지 표시하고 그 목적어 이하는 제외.')
    s.hint('cosmetics [created to address]', '[해결하기 위해 만들어진] 화장품', span='cosmetics created to address',
           label='과거분사 후치수식', links=[(['created'], ['만들어진'])], participle_focus_gloss_id=cr['id'],
           meaning='(각 개인의 고유한 피부 고민을) 해결하기 위해 만들어진 화장품',
           explanation='과거분사 created가 이끄는 created to address …가 앞 명사 cosmetics를 뒤에서 꾸민다. address의 목적어 이하는 제외.')
    s.review = ('주절 stands out + by 뒤 병렬 동명사 analyzing … and providing …(수단) + including 전치사구(추천의 예) + cosmetics를 꾸미는 과거분사 created + 목적 to address. '
                '힌트 2개(by + 병렬 동명사, 과거분사 후치수식). 수동 없음(created·specialized는 독립 과거분사).')
    out.append(s)

    # ---------------- s28 ----------------
    s = S('s28', T['s28'])
    s.ch('To come to the point,', '요점을 말하자면,')
    s.ch('consumers receive a personalized experience', '소비자들은 개인 맞춤형 경험을 받는다')
    s.ch('that prioritizes their individual skin conditions,', '그들 개인의 피부 상태를 우선시하는,')
    s.ch('rather than a uniform purchasing process.', '획일적인 구매 과정 대신에.')
    s.natural('요컨대, 소비자들은 획일적인 구매 과정 대신 자기 개인의 피부 상태를 우선시하는 개인 맞춤형 경험을 얻는다.')
    s.cl('main', 'consumers', subj='consumers', verbs=['receive'])
    s.cl('subject_relative', 'that', verbs=['prioritizes'], marker='that')
    s.g('To|come|to|point', 'to come to the point', '요점을 말하자면')
    s.g('consumers', 'consumers', '소비자들')
    s.g('receive', 'receive', '받다, 얻다')
    s.g('personalized', 'personalized', '개인 맞춤형의', verb_form=pp('past-participle', s, 'personalized', 'personalize'))
    s.g('experience', 'experience', '경험')
    rel = s.g('that', 'that V′', 'V′하는 (관계대명사)')
    s.g('prioritizes', 'prioritize', '우선시하다', verb_form=v3(s, 'prioritizes', 'prioritize', '관계절 선행사 a personalized experience'))
    s.g('their', 'their', '그들의', referent_ko='소비자들')
    s.g('individual', 'individual', '개인의, 개개인의')
    s.g('skin', 'skin', '피부')
    s.g('conditions', 'conditions', '상태들 (흔한 뜻: 조건들)')
    s.g('rather|than', 'rather than', '~ 대신에')
    s.g('uniform', 'uniform', '획일적인, 똑같은 (흔한 뜻: 제복)')
    s.g('purchasing', 'purchasing', '구매의, 구매하는')
    s.g('process', 'process', '과정')
    s.hint('a personalized experience [that prioritizes]', '[우선시하는] 개인 맞춤형 경험', span='a personalized experience that prioritizes',
           label='주격 관계대명사 that', links=[(['that'], ['는'])],
           meaning='(그들 개인의 피부 상태를) 우선시하는 개인 맞춤형 경험',
           explanation='선행사 a personalized experience를 주격 관계대명사 that이 받아 prioritizes their individual skin conditions가 꾸민다. V′ prioritizes까지만 표시.')
    s.relative_ids = [rel['id']]
    s.review = ('주절 receive + 주격 관계절 that prioritizes → 필수 관계사 힌트. rather than이 앞 명사구와 a uniform purchasing process를 대조. '
                'purchasing은 명사 process를 꾸미는 동명사형 수식어. 수동 없음.')
    out.append(s)

    # ---------------- s29 ----------------
    s = S('s29', T['s29'])
    s.ch('Furthermore,', '게다가,')
    s.ch('consumers appreciate flexibility and convenience.', '소비자들은 유연성과 편리함을 높이 평가한다.')
    s.natural('게다가 소비자들은 유연성과 편리함을 높이 평가한다.')
    s.cl('main', 'consumers', subj='consumers', verbs=['appreciate'])
    s.g('Furthermore', 'furthermore', '게다가')
    s.g('consumers', 'consumers', '소비자들')
    s.g('appreciate', 'appreciate', '높이 평가하다, 진가를 알다 (흔한 뜻: 감사하다)')
    s.g('flexibility', 'flexibility', '유연성')
    s.g('convenience', 'convenience', '편리함, 편의성')
    s.review = '단일 주절. 관계사·접속사절·수동 없음 → 힌트 없음.'
    out.append(s)

    # ---------------- s30 ----------------
    s = S('s30', T['s30'])
    s.ch('In some subscription models,', '일부 구독 모델들에서는,')
    s.ch('consumers can experience', '소비자들은 경험할 수 있다')
    s.ch('a variety of products or services', '다양한 제품들이나 서비스들을')
    s.ch('for a fixed cost.', '고정된 비용으로.')
    s.natural('일부 구독 모델에서는 소비자들이 고정된 비용으로 다양한 제품이나 서비스를 경험할 수 있다.')
    s.cl('main', 'In', subj='consumers', verbs=['can', 'experience'])
    s.g('In', 'in', '~에서')
    s.g('some', 'some', '일부의')
    s.g('subscription|models', 'subscription models', '구독 모델들')
    s.g('consumers', 'consumers', '소비자들')
    f = s.g('can', 'can V', '~할 수 있다', kind='function', combines_with=[])
    ex = s.g('experience', 'experience', '경험하다')
    link(f, ex)
    q = s.g('a variety of', 'a variety of', '다양한')
    s.g('products', 'products', '제품들')
    s.g('or', 'or', '또는')
    s.g('services', 'services', '서비스들')
    s.g('for', 'for', '~으로 (값·대가)')
    s.g('fixed', 'fixed', '고정된', verb_form=pp('past-participle', s, 'fixed', 'fix'))
    s.g('cost', 'cost', '비용')
    s.prot('a variety of', 'quantity-kind-of', '수량·종류 표현 a variety of가 뒤 명사 products 앞에서 ‘다양한’으로 같은 어순 대응', gloss=q)
    s.review = '문두 부사구 In some subscription models + 주절 can experience. 관계사·접속사절·수동 없음 → 힌트 없음.'
    out.append(s)

    # ---------------- s31 ----------------
    s = S('s31', T['s31'])
    s.ch('In other models,', '다른 모델들에서는,')
    s.ch('they can flexibly adjust subscription fees', '그들은 구독 요금을 유연하게 조정할 수 있다')
    s.ch('by choosing only the necessary services or products', '필요한 서비스나 제품만을 선택함으로써')
    s.ch('when needed.', '필요할 때.')
    s.natural('다른 모델에서는 소비자들이 필요할 때 필요한 서비스나 제품만 골라 구독 요금을 유연하게 조정할 수 있다.')
    s.cl('main', 'In', subj='they', verbs=['can', 'adjust'])
    s.g('In', 'in', '~에서')
    s.g('other', 'other', '다른')
    s.g('models', 'models', '모델들')
    s.g('they', 'they', '그들은', referent_ko='소비자들')
    f = s.g('can', 'can V', '~할 수 있다', kind='function', combines_with=[])
    s.g('flexibly', 'flexibly', '유연하게')
    aj = s.g('adjust', 'adjust', '조정하다')
    link(f, aj)
    s.g('subscription', 'subscription', '구독')
    s.g('fees', 'fees', '요금들')
    f2 = s.g('by', 'by V-ing', '~함으로써', kind='function', combines_with=[])
    ch = s.g('choosing', 'choose', '선택하다, 고르다', verb_form=pp('ing', s, 'choosing', 'choose'))
    link(f2, ch)
    s.g('only', 'only', '~만')
    s.g('necessary', 'necessary', '필요한')
    s.g('services', 'services', '서비스들')
    s.g('or', 'or', '또는')
    s.g('products', 'products', '제품들')
    s.g('when|needed', 'when needed', '필요할 때')
    s.hint('[by choosing]', '[선택함으로써]', span='by choosing', label='전치사 by + 동명사',
           links=[(['by', 'ing'], ['함으로써'])], meaning='(필요한 서비스나 제품만) 선택함으로써',
           explanation='전치사 by + 동명사 choosing: ~함으로써(수단). 요금을 조정하는 방법. 목적어 only the necessary … 이하는 제외.')
    s.review = ('주절 can adjust(사이 부사 flexibly) + by + 동명사(수단). when needed는 when (they are) needed의 생략형으로 S/V 절을 따로 세우지 않고 한 각주(필요할 때)로 지원. '
                '힌트 1개(by + 동명사). 수동 없음.')
    out.append(s)

    # ---------------- s32 ----------------
    s = S('s32', T['s32'])
    s.ch('This means', '이것은 의미한다')
    s.ch('they can either enjoy a range of offerings', '그들이 다양한 제공물들을 즐기거나')
    s.ch('for a set price', '정해진 가격으로')
    s.ch('or save money', '또는 돈을 절약할 수 있다는 것을')
    s.ch('by selecting only what they really need.', '그들이 정말로 필요로 하는 것만을 선택함으로써.')
    s.natural('이것은 소비자들이 정해진 가격으로 다양한 상품을 누리거나, 정말 필요한 것만 골라 돈을 절약할 수 있다는 뜻이다.')
    s.cl('main', 'This', subj='This', verbs=['means'])
    s.cl('subordinate', 'they', subj='they', verbs=['can', 'enjoy', 'or', 'save'], marker='that', omitted=True)
    s.cl('subordinate', 'what', subj='they', verbs=['need'], marker='what', occ=0)
    s.g('This', 'this', '이것은', referent_ko='고정 비용으로 다양하게 누리거나 필요한 것만 골라 요금을 조정할 수 있는 것')
    s.g('means', 'mean', '의미하다', verb_form=v3(s, 'means', 'mean', 'This'))
    s.g('they', 'they', '그들이', referent_ko='소비자들')
    f = s.g('can', 'can V', '~할 수 있다', kind='function', combines_with=[])
    s.g('either|or', 'either A or B', 'A 또는 B 중 하나')
    ej = s.g('enjoy', 'enjoy', '즐기다, 누리다')
    q = s.g('a range of', 'a range of', '다양한')
    s.g('offerings', 'offerings', '제공물들, 상품들')
    s.g('for', 'for', '~으로 (값·대가)')
    s.g('set', 'set', '정해진', verb_form=pp('past-participle', s, 'set', 'set'))
    s.g('price', 'price', '가격')
    sv = s.g('save', 'save', '절약하다')
    link(f, ej, sv)
    s.g('money', 'money', '돈')
    f2 = s.g('by', 'by V-ing', '~함으로써', kind='function', combines_with=[])
    sl = s.g('selecting', 'select', '선택하다', verb_form=pp('ing', s, 'selecting', 'select'))
    link(f2, sl)
    s.g('only', 'only', '~만')
    rel = s.g('what', 'what S′ V′', 'S′(이/가) V′하는 것 (관계대명사)')
    s.g('they', 'they', '그들이', referent_ko='소비자들', at=s.text.index('they really'))
    s.g('really', 'really', '정말로')
    s.g('need', 'need', '필요로 하다')
    s.prot('a range of', 'quantity-kind-of', '범위 표현 a range of가 뒤 명사 offerings 앞에서 ‘다양한’으로 같은 어순 대응', gloss=q)
    a1 = s.span_of('either')
    a2 = s.span_of('enjoy')
    b1 = s.span_of('or', a2[1])
    b2 = s.span_of('save')
    s.hint('either enjoy … or save …', '즐기거나 … 절약하거나 …', span='either enjoy a range of offerings for a set price or save',
           links=[(['either', ('or', 0)], ['거나', ('거나', 1)])], category='paired-structure',
           display_spans=[[a1[0], a2[1]], [b1[0], b2[1]]],
           meaning='(다양한 제공물을) 즐기거나 (돈을) 절약하거나',
           explanation='either A or B: A 또는 B. can이 enjoy와 save 둘 다에 걸린다. 사이가 길어 두 선택지를 놓치기 쉬워 짝 구조로 표시.')
    s.hint('[what they really need]', '[그들[소비자들]이 정말로 필요로 하는 것]', span='what they really need', label='관계대명사 what',
           links=[(['what'], ['이', '는 것'])], refs=[('they', '그들', '[소비자들]')],
           meaning='그들이 정말로 필요로 하는 것',
           explanation='선행사를 포함한 관계대명사 what: ~하는 것. selecting only의 목적어. S′ they, V′ need(사이 부사 really 보존).')
    s.relative_ids = [rel['id']]
    s.review = ('주절 This means + 접속사 that이 생략된 명사절(they can either enjoy … or save …, can이 두 동사에 걸림) + by + 동명사 + 관계대명사 what절(selecting의 목적어). '
                '힌트 2개(either A or B 짝 구조, 관계대명사 what). 생략 that 명사절은 S/V 줄의 절 구분으로만 지원(별도 각주 없음). 2단계 L 검수(Lb-04): 생략 that 명사절(우선 검토)과 either A or B 짝 구조가 문장당 2개 한도에서 충돌 — 생략 that 표시는 V′가 either enjoy … or save로 갈라져 최소 연속 범위로 보여 줄 수 없어 현행 유지, 사용자 보고 대상. 수동 없음.')
    out.append(s)

    # ---------------- s33 ----------------
    s = S('s33', T['s33'])
    s.ch('Moreover,', '게다가,')
    s.ch('subscription services are made easily accessible', '구독 서비스들은 쉽게 접근할 수 있게 만들어진다')
    s.ch('by online platforms,', '온라인 플랫폼들에 의해,')
    s.ch('enhancing consumers’ convenience.', '소비자들의 편리함을 높이면서.')
    s.natural('게다가 구독 서비스는 온라인 플랫폼 덕분에 쉽게 이용할 수 있게 되어, 소비자의 편리함을 높인다.')
    s.cl('main', 'subscription', subj='subscription services', verbs=['are', 'made'])
    s.g('Moreover', 'moreover', '게다가')
    s.g('subscription', 'subscription', '구독')
    s.g('services', 'services', '서비스들')
    f = s.g('are', 'be p.p.', '~되다', kind='function', combines_with=[])
    md = s.g('made', 'made', '(~하게) 만들어진', verb_form=pp('passive-participle', s, 'made', 'make', f['id']))
    link(f, md)
    s.g('easily', 'easily', '쉽게')
    s.g('accessible', 'accessible', '접근할 수 있는, 이용할 수 있는', star=W['accessible'])
    s.g('by', 'by', '~에 의해')
    s.g('online', 'online', '온라인의')
    s.g('platforms', 'platforms', '플랫폼들')
    f2 = s.g('enhancing', 'V-ing', '~하면서', kind='function', combines_with=[])
    eh = s.g('enhancing', 'enhance', '높이다, 향상시키다', same=True, star=W['enhance'], verb_form=pp('ing', s, 'enhancing', 'enhance'))
    link(f2, eh)
    s.g('consumers’', 'consumers’', '소비자들의')
    s.g('convenience', 'convenience', '편리함, 편의성')
    s.brk('by', 'passive-agent-by', '수동 are made의 행위자(무엇에 의해)를 나타내는 by 구')
    s.hint('[enhancing consumers’ convenience]', '[소비자들의 편리함을 높이면서]', span='enhancing consumers’ convenience', label='분사구문',
           links=[(['ing'], ['면서'])], meaning='소비자들의 편리함을 높이면서',
           explanation='콤마 뒤 enhancing …은 앞 내용(쉽게 이용할 수 있게 됨)과 함께 일어나는 일을 ‘~하면서’로 덧붙이는 분사구. ing ↔ 면서.')
    s.vf_hint(fn=f, lex=md, en='are made', ko='만들어진다', formula='be p.p.', step_form='made', step_ko='만들어진',
              en_mark=['are'], ko_mark=['진다'], span='subscription services are made', meaning='(쉽게 접근할 수 있게) 만들어진다',
              explanation='make A B(A를 B하게 만들다)의 수동 be made B: B하게 만들어지다. 보어 easily accessible과 by 구는 표시에서 제외.')
    s.review = ('주절 수동 are made + 보어 easily accessible(make A B의 수동) + 행위자 by online platforms(by 앞에서 끊음) + 콤마 뒤 분사구 enhancing. '
                '힌트 2개(분사구, 수동 기능 결합).')
    out.append(s)

    # ---------------- s34 ----------------
    s = S('s34', T['s34'])
    s.ch('With just a few clicks,', '단지 몇 번의 클릭으로,')
    s.ch('consumers can receive services or products.', '소비자들은 서비스나 제품을 받을 수 있다.')
    s.natural('단 몇 번의 클릭만으로 소비자들은 서비스나 제품을 받을 수 있다.')
    s.cl('main', 'With', subj='consumers', verbs=['can', 'receive'])
    s.g('With', 'with', '~으로')
    s.g('just', 'just', '단지')
    s.g('a few', 'a few', '몇 번의, 몇몇의')
    s.g('clicks', 'clicks', '클릭들')
    s.g('consumers', 'consumers', '소비자들')
    f = s.g('can', 'can V', '~할 수 있다', kind='function', combines_with=[])
    rc = s.g('receive', 'receive', '받다')
    link(f, rc)
    s.g('services', 'services', '서비스들')
    s.g('or', 'or', '또는')
    s.g('products', 'products', '제품들')
    s.review = '문두 부사구 With just a few clicks + 주절 can receive. 관계사·접속사절·수동 없음 → 힌트 없음.'
    out.append(s)

    # ---------------- s35 ----------------
    s = S('s35', T['s35'])
    s.ch('If they wish to change their device model,', '만약 그들이 그들의 기기 모델을 바꾸기를 원한다면,')
    s.ch('they can do so.', '그들은 그렇게 할 수 있다.')
    s.natural('기기 모델을 바꾸고 싶다면 소비자들은 그렇게 할 수 있다.')
    s.cl('subordinate', 'If', subj='they', verbs=['wish'], marker='If')
    s.cl('main', 'they', subj='they', verbs=['can', 'do'], occ=1)
    s.g('If', 'if S′ V′', 'S′(이/가) V′한다면')
    s.g('they', 'they', '그들이', referent_ko='소비자들')
    s.g('wish|to', 'wish to V', '~하기를 원하다',
        verb_construction={'kind': 'to-complement', 'verb_span': s.span_of('wish'), 'lemma': 'wish',
                           'link_spans': [s.span_of('to')], 'review_record': 'wish to change: wish의 목적어 to V.'})
    s.g('change', 'change', '바꾸다')
    s.g('their', 'their', '그들의', referent_ko='소비자들')
    s.g('device', 'device', '기기')
    s.g('model', 'model', '모델')
    s.g('they', 'they', '그들은', referent_ko='소비자들', at=s.text.index('they can'))
    f = s.g('can', 'can V', '~할 수 있다', kind='function', combines_with=[])
    d = s.g('do', 'do', '하다')
    link(f, d)
    s.g('so', 'so', '그렇게')
    s.hint('[If they wish]', '[만약 그들[소비자들]이 원한다면]', span='If they wish', label='조건 접속사 if',
           links=[(['If'], ['만약', '이', '다면'])], refs=[('they', '그들', '[소비자들]')],
           meaning='만약 그들이 (기기 모델을 바꾸기를) 원한다면',
           explanation='if S′ V′: 만약 S′가 V′한다면. S′ they, V′ wish까지 표시하고 to change 이하는 제외.')
    s.review = '조건 부사절 If they wish to V + 주절 can do so(so는 앞의 기기 모델을 바꾸는 일). 힌트 1개(if 절). 수동 없음.'
    out.append(s)

    # ---------------- s36 ----------------
    s = S('s36', T['s36'])
    s.ch('Whoever desires an upgrade', '업그레이드를 원하는 사람은 누구든지')
    s.ch('can get it', '그것을 얻을 수 있다')
    s.ch('and experience the latest models.', '그리고 최신 모델들을 경험할 수 있다.')
    s.natural('업그레이드를 원하는 사람은 누구든지 그것을 받아 최신 모델을 경험할 수 있다.')
    s.cl('main', 'Whoever', subj='Whoever desires an upgrade', verbs=['can', 'get', 'and', 'experience'])
    s.cl('subject_relative', 'Whoever', verbs=['desires'], marker='Whoever')
    rel = s.g('Whoever', 'whoever V′', 'V′하는 사람은 누구든지')
    s.g('desires', 'desire', '원하다, 바라다', verb_form=v3(s, 'desires', 'desire', 'Whoever'))
    s.g('upgrade', 'upgrade', '업그레이드, (더 좋은 것으로의) 교체')
    f = s.g('can', 'can V', '~할 수 있다', kind='function', combines_with=[])
    gt = s.g('get', 'get', '얻다, 받다')
    s.g('it', 'it', '그것을', referent_ko='업그레이드')
    ex = s.g('experience', 'experience', '경험하다')
    link(f, gt, ex)
    s.g('latest', 'latest', '최신의')
    s.g('models', 'models', '모델들')
    s.hint('[Whoever desires]', '[원하는 사람은 누구든지]', span='Whoever desires', label='복합관계대명사 whoever',
           links=[(['Whoever'], ['는 사람은 누구든지'])], meaning='(업그레이드를) 원하는 사람은 누구든지',
           explanation='whoever V′: V′하는 사람은 누구든지. whoever절 전체(Whoever desires an upgrade)가 주절의 주어이며 whoever 자체가 desires의 주어라 별도 S′가 없다. 목적어 an upgrade는 표시에서 제외.')
    s.review = ('복합관계대명사 whoever절이 주어(명사절 주어라 S 표시는 전체 유지) + 병렬 동사 can get and experience. '
                'whoever는 선행사가 없는 복합관계사라 관계사 각주 목록에는 넣지 않고 힌트로 연결 제공. 수동 없음.')
    out.append(s)
    return out


UNIT = {
    'id': 'u3', 'source_id': 'src', 'paragraph_ids': ['p05', 'p06', 'p07'],
    'sentence_ids': [f's{n:02d}' for n in range(18, 37)],
    'today_words': [
        {'id': W['ownership'], 'text': 'ownership', 'meaning_ko': '소유'},
        {'id': W['customization'], 'text': 'customization', 'meaning_ko': '맞춤화'},
        {'id': W['personalize'], 'text': 'personalize', 'meaning_ko': '개인 맞춤화하다, 개인에게 맞추다'},
        {'id': W['uniqueness'], 'text': 'uniqueness', 'meaning_ko': '고유함, 독특함'},
        {'id': W['stand_out'], 'text': 'stand out', 'meaning_ko': '두드러지다, 돋보이다'},
        {'id': W['address'], 'text': 'address', 'meaning_ko': '해결하다, 다루다'},
        {'id': W['accessible'], 'text': 'accessible', 'meaning_ko': '접근할 수 있는, 이용할 수 있는'},
        {'id': W['enhance'], 'text': 'enhance', 'meaning_ko': '높이다, 향상시키다'},
    ],
}


def analysis(_):
    return {
        'heading_kind': '주제',
        'title_or_topic_en': 'Why People Love Subscriptions',
        'title_or_topic_ko': '사람들이 구독을 좋아하는 이유',
        'intent_ko': '사람들이 구독 경제를 좋아하는 이유를 소유보다 경험을 중시하는 태도, 다양성과 맞춤화, 유연성과 편리함의 세 가지로 나누어 설명하고, 이유마다 구체적인 예를 드는 글이다.',
        'flow': [
            {'sentence_ids': ['s18', 's19', 's20', 's21', 's22'], 'label': '이유 1: 소유보다 경험',
             'text_ko': '구독 경제는 요즘 사람들이 소비하는 방식, 곧 17번에서 말한 첫째 동인인 소비 추세의 변화와 밀접하게 관련된다. 사람들은 물건을 갖는 것보다 경험을 중시하게 되었고, 구독은 소유하지 않고도 서비스를 쓸 수 있게 해 주어 매력적이다. 음악 스트리밍과 의류 구독이 그 예다.'},
            {'sentence_ids': ['s23', 's24', 's25', 's26', 's27', 's28'], 'label': '이유 2: 다양성과 맞춤화',
             'text_ko': '소비자들은 다양성과 맞춤화를 중시하는데, 구독 경제는 취향에 맞게 경험을 고를 수 있게 해 준다. 특히 젊은 세대가 좋아하며, 피부 상태를 분석해 맞춤 화장품까지 추천하는 화장품 구독 서비스가 대표적인 예다.'},
            {'sentence_ids': ['s29', 's30', 's31', 's32', 's33', 's34', 's35', 's36'], 'label': '이유 3: 유연성과 편리함',
             'text_ko': '고정 비용으로 다양하게 누리거나 필요한 것만 골라 요금을 줄일 수 있어 유연하다. 또 온라인 플랫폼 덕분에 몇 번의 클릭으로 서비스를 받고 기기도 쉽게 바꾸거나 업그레이드할 수 있어 편리하다.'},
        ],
        'easy_explanations': [
            {'sentence_id': 's20', 'explanatory_sentences': [
                '20번 문장은 19번에서 말한 변화가 왜 구독 경제에 유리한지 설명한다.',
                '요즘은 물건을 갖는 것보다 무언가를 경험하는 것을 더 중요하게 여기는 사람이 점점 늘고 있다.',
                '구독을 하면 물건을 사서 가지지 않아도 서비스나 콘텐츠를 쓸 수 있다.',
                '그래서 경험을 중시하는 사람들에게 구독 경제가 매력적으로 보인다.']},
            {'sentence_id': 's27', 'explanatory_sentences': [
                '27번 문장은 26번에서 소개한 화장품 구독 서비스가 어떤 점에서 눈에 띄는지 알려 준다.',
                '이 서비스는 먼저 고객의 지금 피부 상태를 꼼꼼히 살핀다.',
                '그다음 그 사람에게 맞는 제품을 추천한다.',
                '추천에는 그 사람의 피부 고민을 해결하도록 만든 화장품을 제조해 주는 것까지 들어 있다.',
                '모두에게 같은 제품을 파는 것이 아니라 한 사람 한 사람에게 맞춰 준다는 점이 핵심이다.']},
            {'sentence_id': 's32', 'explanatory_sentences': [
                '32번 문장은 30번과 31번에서 말한 두 가지 구독 방식을 정리한다.',
                '첫째 방식은 정해진 돈을 내고 여러 가지 상품을 누리는 것이다.',
                '둘째 방식은 정말 필요한 것만 골라서 돈을 아끼는 것이다.',
                '소비자는 자기 상황에 맞는 방식을 고를 수 있다.',
                '이것이 구독의 유연성이다.']},
        ],
        'grammar_points': [
            {'id': 'u3-gp1', 'sentence_id': 's18', 'span': 'how people consume goods and services',
             'title': 'how S′ V′: 어떻게 S′가 V′하는지 (간접의문문)', 'formula_key': 'how S′ V′',
             'explanation': '공식: how S′ V′ — 어떻게 S′(이/가) V′하는지. S′ = people(사람들), V′ = consume(소비하다), 목적어 = goods and services(재화와 서비스). '
                            '→ 사람들이 어떻게 재화와 서비스를 소비하는지. 앞의 be relevant to(~와 관련이 있다)의 to 뒤에 명사 대신 이 의문사절이 왔다.',
             'practice': {'span': 'how people consume goods and services',
                          'formula_support': {'en': 'how S′ V′', 'ko': '어떻게 S′(이/가) V′하는지'},
                          'support': [('s18', 'people'), ('s18', 'consume'), ('s18', 'goods'), ('s18', 'services')],
                          'answer_ko': '사람들이 어떻게 재화와 서비스를 소비하는지'}},
            {'id': 'u3-gp2', 'sentence_id': 's24', 'span': 'enabling individuals to personalize their experiences',
             'title': 'enable A to V: A가 ~할 수 있게 해 주다', 'formula_key': 'enable A to V',
             'explanation': '공식: enable A to V — A(이/가) ~할 수 있게 해 주다. A = individuals(개인들), to V = to personalize(개인 맞춤화하다), '
                            'personalize의 목적어 = their experiences(그들의 경험). → 개인들이 그들의 경험을 개인 맞춤화할 수 있게 해 주다. '
                            '콤마 뒤 enabling은 앞 절(다양한 선택지를 제공한다)에 이어지는 일을 ‘~하면서’로 덧붙인다.',
             'practice': {'span': 'enabling individuals to personalize their experiences',
                          'formula_support': {'en': 'enable A to V', 'ko': 'A(이/가) ~할 수 있게 해 주다'},
                          'support': [('s24', 'V-ing'), ('s24', 'individuals'), ('s24', 'personalize'), ('s24', 'their'), ('s24', 'experiences')],
                          'answer_ko': '개인들이 그들의 경험을 개인 맞춤화할 수 있게 해 주면서'}},
            {'id': 'u3-gp3', 'sentence_id': 's32', 'span': 'by selecting only what they really need',
             'title': 'what S′ V′: S′가 V′하는 것 (관계대명사 what)', 'formula_key': 'what S′ V′',
             'explanation': '공식: what S′ V′ — S′(이/가) V′하는 것. S′ = they(소비자들), V′ = need(필요로 하다), really = 정말로. '
                            '→ 그들이 정말로 필요로 하는 것. what은 ‘~하는 것’이라는 명사 덩어리를 만들어 selecting only(~만을 선택하는 것)의 목적어가 된다.',
             'practice': {'span': 'what they really need',
                          'formula_support': {'en': 'what S′ V′', 'ko': 'S′(이/가) V′하는 것'},
                          'support': [('s32', 'they', 1), ('s32', 'really'), ('s32', 'need')],
                          'answer_ko': '그들이 정말로 필요로 하는 것'}},
            {'id': 'u3-gp4', 'sentence_id': 's26', 'span': 'A popular example that has gained attention',
             'title': 'have p.p.: ~해 왔다 (has gained attention: 주목을 얻어 왔다)', 'formula_key': 'have p.p.',
             'explanation': '공식: have p.p. — ~해 왔다. p.p. = gained(gain의 p.p.형, 얻다), 목적어 = attention(주목). '
                            '→ 주목을 얻어 왔다. 과거부터 지금까지 관심을 받고 있다는 뜻이다. 관계사 that과 이으면 ‘주목을 얻어 온 인기 있는 사례’가 된다.',
             'supplemental': {'function': ('s26', 'have p.p.', 0),
                              'reason': 's26의 능동 완료 has gained는 필수 관계사 힌트 표시 범위 안에 있어 결합 힌트로 선정하지 않았고, 기본 분석 3개에 have p.p. 설명이 없어 이 단위 대표 사례로 1회 보충'},
             'practice': {'span': 'has gained attention',
                          'formula_support': {'en': 'have p.p.', 'ko': '~해 왔다'},
                          'support': [('s26', 'gain'), ('s26', 'attention')],
                          'answer_ko': '주목을 얻어 왔다'}},
        ],
        'formula_routes': [
            {'function': ('s26', 'have p.p.', 0), 'route': 'analysis', 'grammar_point_id': 'u3-gp4',
             'review_record': 'has gained: 관계사 힌트 표시 범위 안이라 분석 보충 u3-gp4로 연결'},
            {'function': ('s33', 'be p.p.', 0), 'route': 'hint', 'hint_index': 1,
             'review_record': 'are made: 분사구 힌트 뒤 수동 기능 결합 힌트'},
        ],
        'relations': [
            {'head': {'id': 'u3-r1h', 'text': 'diverse', 'meaning_ko': '다양한'},
             'synonym': {'id': 'u3-r1s', 'text': 'varied', 'meaning_ko': '다양한, 여러 가지의'},
             'antonym': {'id': 'u3-r1a', 'text': 'uniform', 'meaning_ko': '획일적인, 똑같은'}},
            {'head': {'id': 'u3-r2h', 'text': 'limitless', 'meaning_ko': '무한한, 끝없는'},
             'synonym': {'id': 'u3-r2s', 'text': 'endless', 'meaning_ko': '끝없는'},
             'antonym': {'id': 'u3-r2a', 'text': 'limited', 'meaning_ko': '제한된, 한정된'}},
            {'head': {'id': 'u3-r3h', 'text': 'valuable', 'meaning_ko': '가치 있는'},
             'synonym': {'id': 'u3-r3s', 'text': 'precious', 'meaning_ko': '소중한, 귀중한'},
             'antonym': {'id': 'u3-r3a', 'text': 'worthless', 'meaning_ko': '가치 없는'}},
        ],
    }


def workbook():
    return {
        'relation_order': ['u3-r2s', 'u3-r1a', 'u3-r3h', 'u3-r2a', 'u3-r1h', 'u3-r3s', 'u3-r2h', 'u3-r3a', 'u3-r1s'],
        'key_sentence_ids': ['s24', 's27'],
        'question_id': 'Q03',
        'syntax_point_ids': ['u3-gp1', 'u3-gp2', 'u3-gp3', 'u3-gp4'],
    }
