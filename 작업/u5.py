"""공통 단위 5: Limitations of the subscription economy (s44~s58, 단락 p10~p13; 짧은 단락이 있어 소제목 전체 묶음, 결론 단락 포함)."""
from author import S, link
from u1 import pp, v3

W = {'limitations': 'u5-w1', 'overconsumption': 'u5-w2', 'sign_up': 'u5-w3', 'excessive': 'u5-w4',
     'burden': 'u5-w5', 'affordable': 'u5-w6', 'add_up': 'u5-w7', 'eco': 'u5-w8'}


def sentences(T):
    out = []

    # ---------------- s44 ----------------
    s = S('s44', T['s44'])
    s.ch('Although the subscription economy offers many advantages,', '비록 구독 경제가 많은 장점들을 제공하지만,')
    s.ch('there are also some disadvantages', '또한 몇몇 단점들이 있다')
    s.ch('to consider.', '고려할.')
    s.natural('구독 경제는 많은 장점이 있지만, 고려해야 할 단점도 몇 가지 있다.')
    s.cl('subordinate', 'Although', subj='the subscription economy', verbs=['offers'], marker='Although')
    s.cl('main', 'there', subj='some disadvantages to consider', verbs=[], vfirst=['are'], disp='some disadvantages',
         disp_review='중심명사 disadvantages까지 표시하고 뒤에서 꾸미는 to consider는 제외(유도부사 there는 주어 아님)')
    s.g('Although', 'although S′ V′', '비록 S′(이/가) V′하지만')
    s.g('subscription|economy', 'subscription economy', '구독 경제')
    s.g('offers', 'offer', '제공하다', verb_form=v3(s, 'offers', 'offer', 'the subscription economy'))
    s.g('many', 'many', '많은')
    s.g('advantages', 'advantages', '장점들, 이점들')
    s.g('are', 'are', '있다')
    s.g('also', 'also', '또한')
    s.g('some', 'some', '몇몇의')
    s.g('disadvantages', 'disadvantages', '단점들')
    f = s.g('to', 'to V', '~할', kind='function', combines_with=[])
    cs = s.g('consider', 'consider', '고려하다')
    link(f, cs)
    s.extra_cov[tuple(s.span_of('there'))] = {'exemption': 'below-middle1-unneeded', 'level': 'below-middle1',
        'reason': '유도부사 there(초등 기초어)는 따로 해석하지 않으며 뒤 are 각주의 ‘있다’로 뜻을 지원'}
    s.hint('[Although the subscription economy offers]', '[비록 구독 경제가 제공하지만]', span='Although the subscription economy offers',
           label='양보 접속사 although', links=[(['Although'], ['비록', '가', '지만'])],
           meaning='비록 구독 경제가 (많은 장점을) 제공하지만',
           explanation='although S′ V′: 비록 S′가 V′하지만(양보). S′ the subscription economy, V′ offers까지 표시하고 목적어 many advantages는 제외.')
    s.hint('some disadvantages [to consider]', '[고려할] 몇몇 단점들', span='some disadvantages to consider',
           label='to부정사 후치수식', links=[(['to'], ['할'])], meaning='고려할 몇몇 단점들',
           explanation='to consider가 앞 명사 some disadvantages를 뒤에서 꾸며 ‘고려할 단점들’.')
    s.review = ('양보 부사절 Although + 주절 there are(유도부사 there, 주어 some disadvantages to consider). to consider는 to부정사 후치수식. '
                '힌트 2개(양보절, to부정사 후치수식). 수동 없음.')
    out.append(s)

    # ---------------- s45 ----------------
    s = S('s45', T['s45'])
    s.ch('One concern is the potential', '한 가지 우려는 가능성이다')
    s.ch('for overconsumption.', '과소비의.')
    s.natural('한 가지 우려는 과소비의 가능성이다.')
    s.cl('main', 'One', subj='One concern', verbs=['is'])
    s.g('One', 'one', '한 가지')
    s.g('concern', 'concern', '우려, 걱정거리')
    s.g('is', 'is', '~이다')
    s.g('potential', 'potential', '가능성, 잠재성')
    s.g('for', 'for', '~의')
    s.g('overconsumption', 'overconsumption', '과소비', star=W['overconsumption'])
    s.brk('for', 'postnominal-preposition', 'for overconsumption은 앞 명사 the potential을 뒤에서 꾸미는 전치사구')
    s.review = '단일 주절. the potential for …의 for 앞 후치수식 경계. 관계사·접속사절·수동 없음 → 힌트 없음.'
    out.append(s)

    # ---------------- s46 ----------------
    s = S('s46', T['s46'])
    s.ch('The convenience and accessibility', '편리함과 접근성은')
    s.ch('of the subscription model', '구독 모델의')
    s.ch('make it easy for consumers to sign up for', '소비자들이 가입하는 것을 쉽게 만든다')
    s.ch('multiple services', '여러 서비스에')
    s.ch('and use a lot of content or products.', '그리고 많은 콘텐츠나 제품을 사용하는 것을.')
    s.natural('구독 모델의 편리함과 접근성 때문에 소비자들은 여러 서비스에 쉽게 가입하고 많은 콘텐츠나 제품을 쉽게 사용하게 된다.')
    s.cl('main', 'The', subj='The convenience and accessibility of the subscription model', verbs=['make'])
    s.g('convenience', 'convenience', '편리함, 편의성')
    s.g('accessibility', 'accessibility', '접근성, 이용하기 쉬움')
    s.g('of', 'of', '~의')
    s.g('subscription|model', 'subscription model', '구독 모델')
    s.g('make|it|easy|for|to', 'make it easy for A to V', 'A(이/가) ~하는 것을 쉽게 만들다')
    s.g('consumers', 'consumers', '소비자들')
    s.glosses.sort(key=lambda g: g['spans'][0][0])
    s.g('sign|up|for', 'sign up for', '~에 가입하다, ~을 신청하다', star=W['sign_up'], at=s.text.index('sign'))
    s.g('multiple', 'multiple', '여러, 다수의')
    s.g('services', 'services', '서비스들')
    s.g('use', 'use', '사용하다')
    q = s.g('a lot of', 'a lot of', '많은')
    s.g('content', 'content', '콘텐츠')
    s.g('or', 'or', '또는')
    s.g('products', 'products', '제품들')
    s.brk('of', 'postnominal-preposition', 'of the subscription model은 앞 명사 The convenience and accessibility를 뒤에서 꾸미는 전치사구')
    s.prot('a lot of', 'quantity-kind-of', '수량 표현 a lot of가 뒤 명사 content 앞에서 ‘많은’으로 같은 어순 대응', gloss=q)
    s.hint('make it easy [for consumers to sign up for]', '[소비자들이 가입하는 것을] 쉽게 만든다', span='make it easy for consumers to sign up for',
           label='가목적어 it과 진목적어 to부정사', links=[(['for', 'to'], ['이', '는 것을'])],
           meaning='소비자들이 (여러 서비스에) 가입하는 것을 쉽게 만든다',
           explanation='make it easy for A to V: it은 뒤의 for consumers to sign up for … and use …를 대신하는 가목적어이고, for A(consumers)는 to V의 의미상 주어. and use도 to에 걸린다. 대상 multiple services 이하는 표시에서 제외.')
    s.review = ('주어 The convenience and accessibility of …(등위 주어라 S 표시는 전체 유지) + make it easy for A to V(가목적어, to 뒤 sign up for와 use 병렬). '
                '힌트 1개(가목적어 구문). 관계사·수동 없음.')
    out.append(s)

    # ---------------- s47 ----------------
    s = S('s47', T['s47'])
    s.ch('This can result in excessive consumption', '이것은 과도한 소비를 초래할 수 있다')
    s.ch('and using more subscription services', '그리고 더 많은 구독 서비스들을 사용하는 것을')
    s.ch('than actually needed.', '실제로 필요한 것보다.')
    s.natural('이것은 과도한 소비로 이어지고, 실제로 필요한 것보다 더 많은 구독 서비스를 이용하게 만들 수 있다.')
    s.cl('main', 'This', subj='This', verbs=['can', 'result'])
    s.g('This', 'this', '이것은', referent_ko='구독 모델이 편리해서 여러 서비스에 쉽게 가입하고 많이 사용하게 되는 것')
    f = s.g('can', 'can V', '~할 수 있다', kind='function', combines_with=[])
    ri = s.g('result|in', 'result in', '~을 초래하다')
    link(f, ri)
    s.g('excessive', 'excessive', '과도한, 지나친', star=W['excessive'])
    s.g('consumption', 'consumption', '소비')
    f2 = s.g('using', 'V-ing', '~하는 것', kind='function', combines_with=[])
    us = s.g('using', 'use', '사용하다', same=True, verb_form=pp('ing', s, 'using', 'use'))
    link(f2, us)
    s.g('more', 'more', '더 많은')
    s.g('subscription', 'subscription', '구독')
    s.g('services', 'services', '서비스들')
    s.g('than', 'than', '~보다')
    s.g('actually', 'actually', '실제로')
    s.g('needed', 'needed', '필요한, 필요로 되는', verb_form=pp('past-participle', s, 'needed', 'need'))
    s.hint('[more subscription services than actually needed]', '[실제로 필요한 것보다 더 많은 구독 서비스들]',
           span='more subscription services than actually needed', label='비교급 more ~ than',
           links=[(['more', 'than'], ['보다', '더 많은'])], meaning='실제로 필요한 것보다 더 많은 구독 서비스들',
           explanation='more A than …: …보다 더 많은 A. than 뒤 actually needed는 than (is) actually needed에서 주어·be가 생략된 형태. 비교 대상의 어순이 영어와 한국어에서 반대라 선정.')
    s.review = ('단일 주절 can result in(목적어 excessive consumption과 동명사구 using … 병렬). than actually needed는 생략된 비교 절. '
                '힌트 1개(비교급 more ~ than). 관계사·수동 없음(needed는 생략 절의 과거분사).')
    out.append(s)

    # ---------------- s48 ----------------
    s = S('s48', T['s48'])
    s.ch('It is crucial', '매우 중요하다')
    s.ch('to subscribe only to services', '서비스들만을 구독하는 것이')
    s.ch('that are truly necessary', '정말로 필요한')
    s.ch('and avoid subscribing to similar services.', '그리고 비슷한 서비스들을 구독하는 것을 피하는 것이.')
    s.natural('정말로 필요한 서비스만 구독하고, 비슷한 서비스를 구독하는 것은 피하는 것이 매우 중요하다.')
    s.cl('main', 'It', subj='It', verbs=['is'])
    s.cl('subject_relative', 'that', verbs=['are'], marker='that')
    s.g('It|to', 'It … to V', '~하는 것은 (It은 뒤의 to V를 대신함)')
    s.g('is', 'is', '~이다')
    s.g('crucial', 'crucial', '매우 중요한, 결정적인')
    sb = s.g('subscribe|to', 'subscribe to', '~을 구독하다')
    s.g('only', 'only', '~만', at=s.text.index('only'))
    s.glosses.sort(key=lambda g: g['spans'][0][0])
    s.g('services', 'services', '서비스들', at=s.text.index('services'))
    rel = s.g('that', 'that V′', 'V′하는 (관계대명사)')
    s.g('are', 'are', '~이다')
    s.g('truly', 'truly', '정말로')
    s.g('necessary', 'necessary', '필요한')
    s.g('avoid', 'avoid V-ing', 'V-ing하는 것을 피하다',
        verb_construction={'kind': 'verb-frame', 'verb_span': s.span_of('avoid'), 'lemma': 'avoid', 'link_spans': [],
                           'review_record': 'avoid subscribing to similar services: 동명사 목적어. V-ing 연결 뜻은 이 구문이 제공.'})
    s.g('subscribing|to', 'subscribe to', '~을 구독하다', verb_form=pp('ing', s, 'subscribing', 'subscribe'))
    s.g('similar', 'similar', '비슷한')
    s.g('services', 'services', '서비스들', at=s.text.index('similar services') + 8)
    s.hint('It is crucial [to subscribe]', '[구독하는 것이] 매우 중요하다', span='It is crucial to subscribe',
           label='가주어 It과 진주어 to부정사', links=[(['to'], ['는 것이'])],
           meaning='(필요한 서비스만) 구독하는 것이 매우 중요하다',
           explanation='It은 뒤의 to subscribe … and avoid …를 대신하는 가주어. to 뒤 subscribe와 avoid가 and로 병렬. 대상 only to services 이하는 표시에서 제외.')
    s.hint('services [that are truly necessary]', '[정말로 필요한] 서비스들', span='services that are truly necessary',
           label='주격 관계대명사 that', links=[(['that'], ['한'])],
           meaning='정말로 필요한 서비스들',
           explanation='선행사 services를 주격 관계대명사 that이 받아 are truly necessary가 꾸민다. be동사라 최소 보어 necessary까지 표시(사이 부사 truly 보존).')
    s.relative_ids = [rel['id']]
    s.review = ('가주어 It + 진주어 to부정사(to subscribe … and avoid …, 두 동사원형 병렬) + 주격 관계절 that are truly necessary. '
                'to 진주어라 It 뒤 to 앞에서 끊음. 힌트 2개(가주어–to 진주어, 필수 관계사). 수동 없음.')
    out.append(s)

    # ---------------- s49 ----------------
    s = S('s49', T['s49'])
    s.ch('Related to the concern', '우려와 관련된 것은')
    s.ch('of overconsumption', '과소비의')
    s.ch('is the financial burden', '재정적 부담이다')
    s.ch('that subscriptions can create.', '구독들이 만들어 낼 수 있는.')
    s.natural('과소비에 대한 우려와 관련된 것으로, 구독이 만들어 낼 수 있는 재정적 부담이 있다.')
    s.cl('main', 'Related', subj='the financial burden that subscriptions can create', verbs=[], vfirst=['is'],
         disp='the financial burden',
         disp_review='도치된 주어 the financial burden that subscriptions can create에서 앞수식어 financial과 중심명사 burden까지 표시하고 뒤 관계절은 제외')
    s.cl('subordinate', 'that', subj='subscriptions', verbs=['can', 'create'], marker='that')
    rl = s.g('Related|to', 'related to', '(~와) 관련된', verb_form=pp('past-participle', s, 'Related', 'relate'))
    s.g('concern', 'concern', '우려, 걱정거리')
    s.g('of', 'of', '~의')
    s.g('overconsumption', 'overconsumption', '과소비', star=W['overconsumption'])
    s.g('is', 'is', '~이다')
    s.g('financial', 'financial', '재정적인, 금전적인')
    s.g('burden', 'burden', '부담, 짐', star=W['burden'])
    rel = s.g('that', 'that S′ V′', 'S′(이/가) V′하는 (관계대명사)')
    s.g('subscriptions', 'subscriptions', '구독들')
    f = s.g('can', 'can V', '~할 수 있다', kind='function', combines_with=[])
    cr = s.g('create', 'create', '만들어 내다')
    link(f, cr)
    s.brk('of', 'postnominal-preposition', 'of overconsumption은 앞 명사 the concern을 뒤에서 꾸미는 전치사구')
    s.hint('[Related to the concern of overconsumption] is the financial burden', '[과소비의 우려와 관련된] 것은 재정적 부담이다',
           span='Related to the concern of overconsumption is the financial burden', label='보어 도치',
           links=[(['Related'], ['관련된'])], participle_focus_gloss_id=rl['id'],
           meaning='과소비의 우려와 관련된 것은 재정적 부담이다',
           explanation='원래 The financial burden … is related to the concern of overconsumption에서 보어 Related to …가 문장 맨 앞으로 나가고 주어와 동사 is의 자리가 바뀌었다. 진짜 주어는 is 뒤의 the financial burden.')
    s.hint('the financial burden [that subscriptions can create]', '[구독들이 만들어 낼 수 있는] 재정적 부담',
           span='the financial burden that subscriptions can create', label='목적격 관계대명사 that',
           links=[(['that'], ['이', '는'])], meaning='구독들이 만들어 낼 수 있는 재정적 부담',
           explanation='선행사 the financial burden을 목적격 관계대명사 that이 받는다(create의 목적어). S′ subscriptions, V′ can create.')
    s.relative_ids = [rel['id']]
    s.review = ('보어 Related to the concern of overconsumption이 앞으로 나간 도치 문장: V is, S the financial burden that … (관계절 포함). '
                '목적격 관계절 that subscriptions can create. 힌트 2개(보어 도치, 필수 관계사). 수동 없음(Related는 보어 과거분사).')
    out.append(s)

    # ---------------- s50 ----------------
    s = S('s50', T['s50'], key=True)
    s.ch('While the cost', '비용은')
    s.ch('of individual subscriptions', '개별 구독들의')
    s.ch('may seem affordable,', '감당할 만해 보일 수도 있지만,')
    s.ch('subscribing to multiple services', '여러 서비스들을 구독하는 것은')
    s.ch('can add up quickly.', '(비용이) 빠르게 불어날 수 있다.')
    s.natural('개별 구독 비용은 감당할 만해 보일 수도 있지만, 여러 서비스를 구독하면 비용이 빠르게 불어날 수 있다.')
    s.cl('subordinate', 'While', subj='the cost of individual subscriptions', verbs=['may', 'seem'], marker='While',
         disp='the cost', disp_review='중심명사 cost까지 표시하고 뒤수식 of individual subscriptions는 제외')
    s.cl('main', 'subscribing', subj='subscribing to multiple services', verbs=['can', 'add up'])
    s.g('While', 'while S′ V′', 'S′는 V′하지만')
    s.g('cost', 'cost', '비용')
    s.g('of', 'of', '~의')
    s.g('individual', 'individual', '개별의, 개개의')
    s.g('subscriptions', 'subscriptions', '구독들')
    f = s.g('may', 'may V', '~할 수도 있다', kind='function', combines_with=[])
    sm = s.g('seem', 'seem', '~해 보이다')
    link(f, sm)
    s.g('affordable', 'affordable', '(값이) 감당할 수 있는, 적당한', star=W['affordable'])
    f2 = s.g('subscribing', 'V-ing', '~하는 것', kind='function', combines_with=[])
    sb = s.g('subscribing|to', 'subscribe to', '~을 구독하다', same=True, verb_form=pp('ing', s, 'subscribing', 'subscribe'))
    link(f2, sb)
    s.g('multiple', 'multiple', '여러, 다수의')
    s.g('services', 'services', '서비스들')
    f3 = s.g('can', 'can V', '~할 수 있다', kind='function', combines_with=[])
    ad = s.g('add|up', 'add up', '(합계가) 불어나다, 쌓이다', star=W['add_up'])
    link(f3, ad)
    s.g('quickly', 'quickly', '빠르게')
    s.brk('of', 'postnominal-preposition', 'of individual subscriptions는 앞 명사 the cost를 뒤에서 꾸미는 전치사구')
    s.hint('[While the cost of individual subscriptions may seem affordable]', '[개별 구독들의 비용은 감당할 만해 보일 수도 있지만]',
           span='While the cost of individual subscriptions may seem affordable', label='대조 접속사 while',
           links=[(['While'], ['은', '지만'])], meaning='개별 구독들의 비용은 감당할 만해 보일 수도 있지만',
           explanation='while S′ V′: S′는 V′하지만(대조). S′ the cost of individual subscriptions, V′ may seem. seem은 be처럼 보어가 있어야 뜻이 잡혀 최소 보어 affordable까지 표시.')
    s.hint('[subscribing to multiple services] can add up', '[여러 서비스들을 구독하는 것은] 불어날 수 있다',
           span='subscribing to multiple services can add up', label='동명사 주어',
           links=[(['ing'], ['는 것은'])], meaning='여러 서비스들을 구독하는 것은 (비용이) 불어날 수 있다',
           explanation='동명사구 subscribing to multiple services가 주절의 주어(~하는 것은). 동사 can add up과 연결.')
    s.review = ('대조 부사절 While(주어 표시 the cost, V′ may seem + 보어 affordable) + 주절 동명사 주어 subscribing to multiple services(전체 유지) + can add up. '
                '힌트 2개(while 절, 동명사 주어). 관계사·수동 없음.')
    out.append(s)

    # ---------------- s51 ----------------
    s = S('s51', T['s51'])
    s.ch('It is important', '중요하다')
    s.ch('to carefully consider the costs', '비용들을 신중하게 고려하는 것이')
    s.ch('of these subscriptions', '이 구독들의')
    s.ch('to avoid financial strain.', '재정적 압박을 피하기 위해.')
    s.natural('재정적 압박을 피하려면 이러한 구독 비용을 신중하게 따져 보는 것이 중요하다.')
    s.cl('main', 'It', subj='It', verbs=['is'])
    s.g('It|to', 'It … to V', '~하는 것은 (It은 뒤의 to V를 대신함)')
    s.g('is', 'is', '~이다')
    s.g('important', 'important', '중요한')
    s.g('carefully', 'carefully', '신중하게')
    s.glosses.sort(key=lambda g: g['spans'][0][0])
    s.g('consider', 'consider', '고려하다, 따져 보다', at=s.text.index('consider'))
    s.g('costs', 'costs', '비용들')
    s.g('of', 'of', '~의')
    s.g('these', 'these', '이')
    s.g('subscriptions', 'subscriptions', '구독들')
    f = s.g('to', 'to V', '~하기 위해', kind='function', combines_with=[], at=s.text.index('to avoid'))
    av = s.g('avoid', 'avoid', '피하다')
    link(f, av)
    s.g('financial', 'financial', '재정적인')
    s.g('strain', 'strain', '압박, 부담')
    s.brk('of', 'postnominal-preposition', 'of these subscriptions는 앞 명사 the costs를 뒤에서 꾸미는 전치사구')
    s.hint('It is important [to carefully consider]', '[신중하게 고려하는 것이] 중요하다', span='It is important to carefully consider',
           label='가주어 It과 진주어 to부정사', links=[(['to'], ['는 것이'])],
           meaning='(이 구독들의 비용을) 신중하게 고려하는 것이 중요하다',
           explanation='It은 뒤의 to carefully consider …를 대신하는 가주어. 목적어 the costs 이하는 표시에서 제외.')
    s.hint('[to avoid]', '[피하기 위해]', span='to avoid', label='목적의 to부정사',
           links=[(['to'], ['기 위해'])], meaning='(재정적 압박을) 피하기 위해',
           explanation='문장 끝 to avoid financial strain은 비용을 신중히 고려하는 목적. 진주어 to와 구별.')
    s.review = ('가주어 It + 진주어 to carefully consider …(It 뒤 to 앞에서 끊음) + 목적의 to avoid …. of these subscriptions 후치수식 경계. '
                '힌트 2개(가주어–to 진주어, 목적 to부정사). 관계사·수동 없음.')
    out.append(s)

    # ---------------- s52 ----------------
    s = S('s52', T['s52'])
    s.ch('Regularly reviewing and canceling unnecessary subscriptions', '불필요한 구독들을 정기적으로 검토하고 취소하는 것은')
    s.ch('can be beneficial.', '유익할 수 있다.')
    s.natural('불필요한 구독을 정기적으로 점검하고 취소하는 것이 도움이 될 수 있다.')
    s.cl('main', 'Regularly', subj='Regularly reviewing and canceling unnecessary subscriptions', verbs=['can', 'be'])
    s.g('Regularly', 'regularly', '정기적으로')
    f = s.g('reviewing', 'V-ing', '~하는 것', kind='function', combines_with=[])
    rv = s.g('reviewing', 'review', '검토하다, 점검하다', same=True, verb_form=pp('ing', s, 'reviewing', 'review'))
    cn = s.g('canceling', 'cancel', '취소하다', verb_form=pp('ing', s, 'canceling', 'cancel'))
    link(f, rv, cn)
    s.g('unnecessary', 'unnecessary', '불필요한')
    s.g('subscriptions', 'subscriptions', '구독들')
    f2 = s.g('can', 'can V', '~할 수 있다', kind='function', combines_with=[])
    be = s.g('be', 'be', '~이다')
    link(f2, be)
    s.g('beneficial', 'beneficial', '유익한, 이로운')
    s.hint('[Regularly reviewing and canceling]', '[정기적으로 검토하고 취소하는 것은]', span='Regularly reviewing and canceling',
           label='동명사 주어', links=[(['ing', ('ing', 1)], ['는 것은'])],
           meaning='(불필요한 구독들을) 정기적으로 검토하고 취소하는 것은',
           explanation='동명사 reviewing과 canceling이 and로 병렬되어 주어가 된다(~하는 것은). 공통 목적어 unnecessary subscriptions는 표시에서 제외.')
    s.review = '동명사 주어(reviewing and canceling 병렬, 공통 목적어 unnecessary subscriptions, 전체 유지) + can be beneficial. 힌트 1개(동명사 주어). 관계사·수동 없음.'
    out.append(s)

    # ---------------- s53 ----------------
    s = S('s53', T['s53'])
    s.ch('Additionally,', '게다가,')
    s.ch('the subscription economy can contribute to environmental pollution.', '구독 경제는 환경 오염에 한몫할 수 있다.')
    s.natural('게다가 구독 경제는 환경 오염의 원인이 될 수 있다.')
    s.cl('main', 'the', subj='the subscription economy', verbs=['can', 'contribute'])
    s.g('Additionally', 'additionally', '게다가, 부가적으로')
    s.g('subscription|economy', 'subscription economy', '구독 경제')
    f = s.g('can', 'can V', '~할 수 있다', kind='function', combines_with=[])
    ct = s.g('contribute', 'contribute', '한몫하다, 기여하다')
    link(f, ct)
    s.g('to', 'to', '~에')
    s.g('environmental', 'environmental', '환경의')
    s.g('pollution', 'pollution', '오염')
    s.review = '단일 주절 can contribute to(to는 대표 뜻 ~에로 분리; 나쁜 결과에 한몫하다). 관계사·접속사절·수동 없음 → 힌트 없음.'
    out.append(s)

    # ---------------- s54 ----------------
    s = S('s54', T['s54'])
    s.ch('The regular delivery', '정기적인 배송은')
    s.ch('of products', '제품들의')
    s.ch('in packaging materials', '포장재에 담긴')
    s.ch('can increase the use', '사용을 증가시킬 수 있다')
    s.ch('of disposable packaging,', '일회용 포장의,')
    s.ch('which harms the environment.', '그리고 그것은 환경을 해친다.')
    s.natural('포장재에 담긴 제품을 정기적으로 배송하면 일회용 포장의 사용이 늘어날 수 있는데, 이는 환경을 해친다.')
    s.cl('main', 'The', subj='The regular delivery of products in packaging materials', verbs=['can', 'increase'],
         disp='The regular delivery', disp_review='앞수식어 regular와 중심명사 delivery까지 표시하고 뒤수식 of products in packaging materials는 제외')
    s.cl('subject_relative', 'which', verbs=['harms'], marker='which')
    s.g('regular', 'regular', '정기적인')
    s.g('delivery', 'delivery', '배송, 배달')
    s.g('of', 'of', '~의')
    s.g('products', 'products', '제품들')
    s.g('in', 'in', '~에 담긴')
    s.g('packaging|materials', 'packaging materials', '포장재')
    f = s.g('can', 'can V', '~할 수 있다', kind='function', combines_with=[])
    ic = s.g('increase', 'increase', '증가시키다, 늘리다')
    link(f, ic)
    s.g('use', 'use', '사용')
    s.g('of', 'of', '~의', at=s.text.index('of disposable'))
    s.g('disposable', 'disposable', '일회용의')
    s.g('packaging', 'packaging', '포장', at=s.text.index('packaging,'))
    rel = s.g('which', ', which V′', '그리고 그것은 V′하다 (계속적 관계대명사)')
    s.g('harms', 'harm', '해치다', verb_form=v3(s, 'harms', 'harm', 'which(일회용 포장 사용의 증가)'))
    s.g('environment', 'environment', '환경')
    s.brk('of', 'postnominal-preposition', 'of products는 앞 명사 The regular delivery를 뒤에서 꾸미는 전치사구')
    s.brk('in', 'postnominal-preposition', 'in packaging materials는 앞 명사 products를 뒤에서 꾸미는 전치사구')
    s.brk('of', 'postnominal-preposition', 'of disposable packaging은 앞 명사 the use를 뒤에서 꾸미는 전치사구', after=s.text.index('use'))
    s.hint('disposable packaging, [which harms]', '일회용 포장, [그리고 그것은 해친다]', span='disposable packaging, which harms',
           label='계속적 관계대명사 which', links=[(['which'], ['그리고 그것은'])],
           meaning='일회용 포장(의 사용 증가), 그리고 그것은 (환경을) 해친다',
           explanation='콤마 뒤 계속적 관계대명사 which가 앞의 일회용 포장 사용 증가를 받아 결과를 덧붙인다(추가 설명이라 그리고). 주격이라 V′ harms까지 표시하고 목적어 the environment는 제외.')
    s.relative_ids = [rel['id']]
    s.review = ('주어 The regular delivery of products in packaging materials(표시 The regular delivery) + can increase + 계속적 관계대명사 which(앞 절의 일회용 포장 사용 증가를 받음). '
                'of·in·of 앞 후치수식 경계. 필수 관계사 힌트 1개. 수동 없음.')
    out.append(s)

    # ---------------- s55 ----------------
    s = S('s55', T['s55'])
    s.ch('Using environmentally friendly packaging materials', '친환경적인 포장재를 사용하는 것')
    s.ch('and opting for reusable packaging', '그리고 재사용 가능한 포장을 선택하는 것은')
    s.ch('can help reduce this problem.', '이 문제를 줄이는 것을 도울 수 있다.')
    s.natural('친환경 포장재를 사용하고 재사용할 수 있는 포장을 선택하는 것은 이 문제를 줄이는 데 도움이 될 수 있다.')
    s.cl('main', 'Using', subj='Using environmentally friendly packaging materials and opting for reusable packaging', verbs=['can', 'help'])
    f = s.g('Using', 'V-ing', '~하는 것', kind='function', combines_with=[])
    us = s.g('Using', 'use', '사용하다', same=True, verb_form=pp('ing', s, 'Using', 'use'))
    s.g('environmentally|friendly', 'environmentally friendly', '친환경적인, 환경 친화적인', star=W['eco'])
    s.g('packaging|materials', 'packaging materials', '포장재')
    op = s.g('opting|for', 'opt for', '~을 선택하다', verb_form=pp('ing', s, 'opting', 'opt'))
    link(f, us, op)
    s.g('reusable', 'reusable', '재사용 가능한')
    s.g('packaging', 'packaging', '포장', at=s.text.index('packaging can'))
    f2 = s.g('can', 'can V', '~할 수 있다', kind='function', combines_with=[])
    hp = s.g('help', 'help V', '~하는 것을 돕다',
             verb_construction={'kind': 'verb-frame', 'verb_span': s.span_of('help'), 'lemma': 'help', 'link_spans': [],
                                'review_record': 'help reduce this problem: help 뒤 원형부정사 reduce.'})
    link(f2, hp)
    s.g('reduce', 'reduce', '줄이다')
    s.g('this', 'this', '이')
    s.g('problem', 'problem', '문제')
    s.hint('[Using environmentally friendly packaging materials and opting for reusable packaging]',
           '[친환경적인 포장재를 사용하고 재사용 가능한 포장을 선택하는 것은]',
           span='Using environmentally friendly packaging materials and opting for reusable packaging', label='동명사 주어',
           links=[(['ing', ('ing', 2)], ['는 것은'])],
           meaning='친환경적인 포장재를 사용하고 재사용 가능한 포장을 선택하는 것은',
           explanation='동명사구 Using …와 opting for …가 and로 병렬되어 주절의 주어가 된다(~하는 것은). 동사 can help와 연결.')
    s.hint('help [reduce]', '[줄이는 것을] 돕다', span='help reduce', label='help V 구문',
           links=[(['help'], ['는 것을'])], emphasis_policy='ko-only-verb-construction',
           meaning='(이 문제를) 줄이는 것을 돕다',
           explanation='help V: ~하는 것을 돕다. help 뒤 to 없이 원형 reduce가 온다. 목적어 this problem은 표시에서 제외.')
    s.review = ('병렬 동명사 주어(Using … and opting for …, 전체 유지) + can help V(원형부정사 reduce). '
                '힌트 2개(동명사 주어, help V). 관계사·수동 없음.')
    out.append(s)

    # ---------------- s56 ----------------
    s = S('s56', T['s56'])
    s.ch('Despite the potential limitations', '잠재적인 한계들에도 불구하고')
    s.ch('of subscription services,', '구독 서비스들의,')
    s.ch('they have become deeply embedded in our lives', '그것들은 우리의 삶에 깊이 자리 잡게 되었다')
    s.ch('and more and more businesses are jumping onto', '그리고 점점 더 많은 기업들이 올라타고 있다')
    s.ch('the subscription economy model.', '구독 경제 모델에.')
    s.natural('구독 서비스의 잠재적 한계에도 불구하고, 구독 서비스는 우리 삶에 깊이 자리 잡았고 점점 더 많은 기업이 구독 경제 모델에 뛰어들고 있다.')
    s.cl('main', 'Despite', subj='they', verbs=['have', 'become'])
    s.cl('main', 'more', subj='more and more businesses', verbs=['are', 'jumping'], marker='and')
    s.g('Despite', 'despite', '~에도 불구하고')
    s.g('potential', 'potential', '잠재적인')
    s.g('limitations', 'limitations', '한계들, 제한점들', star=W['limitations'])
    s.g('of', 'of', '~의')
    s.g('subscription', 'subscription', '구독')
    s.g('services', 'services', '서비스들')
    s.g('they', 'they', '그것들은', referent_ko='구독 서비스들')
    f = s.g('have', 'have p.p.', '~하게 되었다', kind='function', combines_with=[])
    bc = s.g('become', 'become', '되다 (become은 become의 p.p.형)', verb_form=pp('perfect-participle', s, 'become', 'become', f['id']))
    link(f, bc)
    s.g('deeply', 'deeply', '깊이')
    s.g('embedded', 'embedded', '자리 잡은, 깊이 박힌', verb_form=pp('past-participle', s, 'embedded', 'embed'))
    s.g('in', 'in', '~에')
    s.g('our', 'our', '우리의', referent_ko='글쓴이와 독자를 포함한 우리 모두')
    s.g('lives', 'lives', '삶들')
    s.g('more|and|more', 'more and more', '점점 더 많은')
    s.g('businesses', 'businesses', '기업들, 사업체들')
    f2 = s.g('are', 'be V-ing', '~하고 있다', kind='function', combines_with=[])
    jp = s.g('jumping|onto', 'jump onto', '~에 올라타다, ~에 뛰어들다', verb_form=pp('ing', s, 'jumping', 'jump'))
    link(f2, jp)
    s.g('subscription|economy', 'subscription economy', '구독 경제')
    s.g('model', 'model', '모델')
    s.brk('of', 'postnominal-preposition', 'of subscription services는 앞 명사 the potential limitations를 뒤에서 꾸미는 전치사구')
    s.vf_hint(fn=f, lex=bc, en='have become', ko='되었다', formula='have p.p.', step_form='become', step_ko='되다',
              en_mark=['have'], ko_mark=['었다'], span='they have become', meaning='(깊이 자리 잡게) 되었다',
              explanation='빈 힌트 문장의 능동 완료 후보: have become(지금은 그렇게 된 결과). 주어와 보어 deeply embedded … 이하는 제외.')
    s.review = ('문두 Despite 전치사구 + 두 독립절: they have become deeply embedded …(현재완료, become + 과거분사 보어) [and] more and more businesses are jumping onto …(현재진행). '
                '관계사·접속사절 없음 → 능동 완료 기능 결합 힌트. jump onto는 한 각주.')
    out.append(s)

    # ---------------- s57 ----------------
    s = S('s57', T['s57'])
    s.ch('It is expected that new subscription services', '새로운 구독 서비스들이 ~라고 예상된다')
    s.ch('will be continuously provided', '지속적으로 제공될 것이라고')
    s.ch('to consumers', '소비자들에게')
    s.ch('in new areas', '새로운 영역들에서')
    s.ch('in the future.', '미래에.')
    s.natural('앞으로 새로운 영역에서 새로운 구독 서비스가 소비자에게 계속 제공될 것으로 예상된다.')
    s.cl('main', 'It', subj='It', verbs=['is', 'expected'])
    s.cl('subordinate', 'that', subj='new subscription services', verbs=['will be', 'provided'], marker='that')
    it = s.g('It is expected that', 'It is expected that S′ V′', 'S′(이/가) V′할 것으로 예상된다')
    s.g('new', 'new', '새로운')
    s.g('subscription', 'subscription', '구독')
    s.g('services', 'services', '서비스들')
    fw = s.g('will', 'will V', '~할 것이다', kind='function', combines_with=[])
    fb = s.g('be', 'be p.p.', '~되다', kind='function', combines_with=[])
    s.g('continuously', 'continuously', '지속적으로, 계속')
    pv = s.g('provided', 'provided', '제공된', verb_form=pp('passive-participle', s, 'provided', 'provide', fb['id']))
    link(fb, pv)
    link(fw, pv)
    s.g('to', 'to', '~에게')
    s.g('consumers', 'consumers', '소비자들')
    s.g('in', 'in', '~에서')
    s.g('new', 'new', '새로운', at=s.text.index('new areas'))
    s.g('areas', 'areas', '영역들, 분야들')
    s.g('in|the|future', 'in the future', '미래에, 앞으로')
    s.prot('It is expected that', 'dummy-it-prefix', '가주어 It과 진주어 that절(It is expected that S′ V′)은 It부터 that까지 끊지 않음', gloss=it)
    s.hint('It is expected that [new subscription services will be continuously provided]',
           '[새로운 구독 서비스들이 지속적으로 제공될 것이라고] 예상된다',
           span='It is expected that new subscription services will be continuously provided', label='가주어 It과 진주어 that절',
           links=[(['that'], ['이', '라고'])], meaning='새로운 구독 서비스들이 지속적으로 제공될 것이라고 예상된다',
           explanation='가주어 It이 뒤의 that절을 대신한다. that절 S′ new subscription services, V′ will be continuously provided까지 표시(사이 부사 보존)하고 to consumers 이하는 제외.')
    s.review = ('가주어 It + 진주어 that절(It is expected that 한 각주, It~that 끊지 않음). that절 동사 will be provided는 조동사 will V와 수동 be p.p.를 각각 연결. '
                '힌트 1개(가주어–that절). 수동 be p.p.는 가주어 힌트 표시 범위 안이라 분석 보충 u5-gp4로 연결.')
    out.append(s)

    # ---------------- s58 ----------------
    s = S('s58', T['s58'], key=True)
    s.ch('We need to have a deeper understanding', '우리는 더 깊은 이해를 가질 필요가 있다')
    s.ch('of the subscription economy', '구독 경제에 대한')
    s.ch('and become wise consumers', '그리고 현명한 소비자들이 될 (필요가 있다)')
    s.ch('who receive the services', '서비스들을 받는')
    s.ch('that are really needed.', '정말로 필요한.')
    s.natural('우리는 구독 경제를 더 깊이 이해하고, 정말 필요한 서비스를 받는 현명한 소비자가 되어야 한다.')
    s.cl('main', 'We', subj='We', verbs=['need'])
    s.cl('subject_relative', 'who', verbs=['receive'], marker='who')
    s.cl('subject_relative', 'that', verbs=['are', 'needed'], marker='that')
    s.g('We', 'we', '우리는', referent_ko='글쓴이와 독자를 포함한 소비자들')
    s.g('need|to', 'need to V', '~할 필요가 있다',
        verb_construction={'kind': 'to-complement', 'verb_span': s.span_of('need'), 'lemma': 'need',
                           'link_spans': [s.span_of('to')], 'review_record': 'need to have … and become …: need의 목적어 to V(두 동사원형 병렬).'})
    s.g('have', 'have', '가지다')
    s.g('deeper', 'deeper', '더 깊은 (deep의 비교급)')
    s.g('understanding', 'understanding', '이해')
    s.g('of', 'of', '~에 대한')
    s.g('subscription|economy', 'subscription economy', '구독 경제')
    s.g('become', 'become', '~이 되다')
    s.g('wise', 'wise', '현명한')
    s.g('consumers', 'consumers', '소비자들')
    r1 = s.g('who', 'who V′', 'V′하는 (관계대명사)')
    s.g('receive', 'receive', '받다')
    s.g('services', 'services', '서비스들')
    r2 = s.g('that', 'that V′', 'V′하는 (관계대명사)')
    fb = s.g('are', 'be p.p.', '~되다', kind='function', combines_with=[])
    s.g('really', 'really', '정말로')
    nd = s.g('needed', 'needed', '필요로 되는, 필요한', verb_form=pp('passive-participle', s, 'needed', 'need', fb['id']))
    link(fb, nd)
    s.brk('of', 'postnominal-preposition', 'of the subscription economy는 앞 명사 a deeper understanding을 뒤에서 꾸미는 전치사구')
    s.hint('wise consumers [who receive]', '[받는] 현명한 소비자들', span='wise consumers who receive', label='주격 관계대명사 who',
           links=[(['who'], ['는'])], meaning='(정말 필요한 서비스를) 받는 현명한 소비자들',
           explanation='선행사 wise consumers를 주격 관계대명사 who가 받아 receive the services …가 꾸민다. V′ receive까지만 표시.')
    s.hint('the services [that are really needed]', '[정말로 필요한] 서비스들', span='the services that are really needed',
           label='주격 관계대명사 that', links=[(['that'], ['한'])], meaning='정말로 필요한 서비스들',
           explanation='선행사 the services를 주격 관계대명사 that이 받아 are really needed(수동: 정말로 필요로 되는 → 정말로 필요한)가 꾸민다. V′ are really needed.')
    s.relative_ids = [r1['id'], r2['id']]
    s.review = ('주절 need to have … and become …(to 뒤 두 동사원형 병렬) + 주격 관계절 who receive + 그 목적어 the services를 꾸미는 주격 관계절 that are really needed(수동). '
                '힌트 2개(필수 관계사 두 개). 수동 be p.p.는 관계사 힌트 표시 범위 안이라 분석 보충 u5-gp4로 연결.')
    out.append(s)
    return out


UNIT = {
    'id': 'u5', 'source_id': 'src', 'paragraph_ids': ['p10', 'p11', 'p12', 'p13'],
    'sentence_ids': [f's{n:02d}' for n in range(44, 59)],
    'today_words': [
        {'id': W['limitations'], 'text': 'limitations', 'meaning_ko': '한계들, 제한점들'},
        {'id': W['overconsumption'], 'text': 'overconsumption', 'meaning_ko': '과소비'},
        {'id': W['sign_up'], 'text': 'sign up for', 'meaning_ko': '~에 가입하다, ~을 신청하다'},
        {'id': W['excessive'], 'text': 'excessive', 'meaning_ko': '과도한, 지나친'},
        {'id': W['burden'], 'text': 'burden', 'meaning_ko': '부담, 짐'},
        {'id': W['affordable'], 'text': 'affordable', 'meaning_ko': '(값이) 감당할 수 있는, 적당한'},
        {'id': W['add_up'], 'text': 'add up', 'meaning_ko': '(합계가) 불어나다, 쌓이다'},
        {'id': W['eco'], 'text': 'environmentally friendly', 'meaning_ko': '친환경적인'},
    ],
}


def analysis(_):
    return {
        'heading_kind': '주제',
        'title_or_topic_en': 'The Limitations of the Subscription Economy and Wise Consumers',
        'title_or_topic_ko': '구독 경제의 한계와 현명한 소비자',
        'intent_ko': '구독 경제의 단점으로 과소비, 재정적 부담, 환경 오염을 들고 각각의 대처법을 제시한 뒤, 구독 경제가 계속 커질 것이므로 필요한 서비스만 받는 현명한 소비자가 되어야 한다고 주장하는 글이다.',
        'flow': [
            {'sentence_ids': ['s44', 's45', 's46', 's47', 's48'], 'label': '한계 1: 과소비',
             'text_ko': '장점만 있는 것은 아니다. 구독은 편리해서 여러 서비스에 쉽게 가입하게 되고, 필요보다 많이 쓰는 과소비로 이어질 수 있다. 그래서 정말 필요한 서비스만 구독하고 비슷한 서비스는 피해야 한다.'},
            {'sentence_ids': ['s49', 's50', 's51', 's52'], 'label': '한계 2: 재정 부담',
             'text_ko': '과소비와 이어지는 문제로 재정적 부담이 있다. 하나하나는 싸 보여도 여러 개를 구독하면 비용이 빠르게 불어나므로, 비용을 신중히 따지고 불필요한 구독을 정기적으로 정리하는 것이 좋다.'},
            {'sentence_ids': ['s53', 's54', 's55'], 'label': '한계 3: 환경 오염',
             'text_ko': '정기 배송은 일회용 포장을 늘려 환경을 해칠 수 있다. 친환경 포장재나 재사용 포장을 쓰면 이 문제를 줄일 수 있다.'},
            {'sentence_ids': ['s56', 's57', 's58'], 'label': '결론',
             'text_ko': '이런 한계에도 구독은 이미 우리 삶에 깊이 자리 잡았고 앞으로 더 많은 분야로 퍼질 것이다. 그러므로 구독 경제를 깊이 이해하고 필요한 서비스만 받는 현명한 소비자가 되어야 한다.'},
        ],
        'easy_explanations': [
            {'sentence_id': 's46', 'explanatory_sentences': [
                '46번 문장은 45번에서 말한 과소비가 왜 생기는지 설명한다.',
                '구독은 클릭 몇 번이면 가입할 수 있을 만큼 편리하다.',
                '그래서 별생각 없이 여러 서비스에 가입하기 쉽다.',
                '가입한 뒤에는 콘텐츠나 제품도 많이 쓰게 된다.',
                '편리함이 오히려 지나치게 쓰는 원인이 될 수 있다는 뜻이다.']},
            {'sentence_id': 's50', 'explanatory_sentences': [
                '50번 문장은 49번에서 말한 재정적 부담이 어떻게 생기는지 보여 준다.',
                '구독 하나의 요금은 크지 않아서 부담이 없어 보인다.',
                '하지만 음악, 영상, 옷처럼 여러 개를 구독하면 매달 나가는 돈이 합쳐져 금방 커진다.',
                'add up은 작은 것들이 더해져 점점 불어난다는 뜻이다.']},
            {'sentence_id': 's58', 'explanatory_sentences': [
                '58번 문장은 글 전체의 결론이다.',
                '56~57번에서 구독 경제는 한계가 있어도 계속 커질 것이라고 했다.',
                '그래서 글쓴이는 무조건 구독을 피하라고 하지 않는다.',
                '구독 경제를 잘 알고, 정말 필요한 서비스만 골라 받는 현명한 소비자가 되자고 말한다.']},
        ],
        'grammar_points': [
            {'id': 'u5-gp1', 'sentence_id': 's44', 'span': 'Although the subscription economy offers many advantages',
             'title': 'although S′ V′: 비록 S′가 V′하지만', 'formula_key': 'although S′ V′',
             'explanation': '공식: although S′ V′ — 비록 S′(이/가) V′하지만. S′ = the subscription economy(구독 경제), V′ = offers(제공하다), 목적어 = many advantages(많은 장점들). '
                            '→ 비록 구독 경제가 많은 장점들을 제공하지만. 뒤 주절(단점도 있다)과 반대되는 내용이다.',
             'practice': {'span': 'Although the subscription economy offers many advantages',
                          'formula_support': {'en': 'although S′ V′', 'ko': '비록 S′(이/가) V′하지만'},
                          'support': [('s44', 'subscription economy'), ('s44', 'offer'), ('s44', 'many'), ('s44', 'advantages')],
                          'answer_ko': '비록 구독 경제가 많은 장점들을 제공하지만'}},
            {'id': 'u5-gp2', 'sentence_id': 's49', 'span': 'Related to the concern of overconsumption is the financial burden',
             'title': '보어 도치: Related to A is B — A와 관련된 것은 B이다', 'formula_key': 'Related to A is B',
             'explanation': '공식: Related to A + is + B — A와 관련된 것은 B이다(B가 A와 관련되어 있다). 보어 = Related to(~와 관련된), '
                            'A = the concern of overconsumption(과소비의 우려), 동사 = is, 진짜 주어 B = the financial burden(재정적 부담). '
                            '→ 과소비의 우려와 관련된 것은 재정적 부담이다. 원래 순서는 The financial burden is related to the concern of overconsumption이다.',
             'practice': {'span': 'Related to the concern of overconsumption is the financial burden',
                          'formula_support': {'en': 'Related to A is B', 'ko': 'A와 관련된 것은 B이다'},
                          'support': [('s49', 'concern'), ('s49', 'overconsumption'), ('s49', 'financial'), ('s49', 'burden')],
                          'answer_ko': '과소비의 우려와 관련된 것은 재정적 부담이다'}},
            {'id': 'u5-gp3', 'sentence_id': 's50', 'span': 'subscribing to multiple services can add up quickly',
             'title': '동명사 주어: V-ing ~ — ~하는 것은', 'formula_key': 'V-ing 주어',
             'explanation': '공식: V-ing(동명사구) + V — ~하는 것은 V하다. 주어 = subscribing to multiple services(여러 서비스를 구독하는 것), '
                            'V = can add up(불어날 수 있다), quickly = 빠르게. → 여러 서비스들을 구독하는 것은 빠르게 불어날 수 있다. 곧 여러 개를 구독하면 비용이 빠르게 쌓인다는 뜻이다.',
             'practice': {'span': 'subscribing to multiple services can add up quickly',
                          'formula_support': {'en': 'V-ing 주어', 'ko': '~하는 것은'},
                          'support': [('s50', 'subscribe to'), ('s50', 'multiple'), ('s50', 'services'), ('s50', 'can V'),
                                      ('s50', 'add up'), ('s50', 'quickly')],
                          'answer_ko': '여러 서비스들을 구독하는 것은 빠르게 불어날 수 있다'}},
            {'id': 'u5-gp4', 'sentence_id': 's57', 'span': 'new subscription services will be continuously provided to consumers',
             'title': 'be p.p.: ~되다 (will be provided: 제공될 것이다)', 'formula_key': 'be p.p.',
             'explanation': '공식: be p.p. — ~되다. p.p. = provided(제공된, provide의 p.p.형), 앞의 will = ~할 것이다, continuously = 지속적으로, to consumers = 소비자들에게. '
                            '→ 소비자들에게 지속적으로 제공될 것이다. 서비스는 스스로 제공하는 것이 아니라 ‘제공되는’ 대상이라 수동을 쓴다.',
             'supplemental': {'function': ('s57', 'be p.p.', 0),
                              'reason': 's57의 수동 will be provided와 s58의 수동 are needed는 각각 가주어·관계사 힌트 표시 범위 안이라 결합 힌트로 두지 않았고, 기본 분석 3개에 be p.p. 설명이 없어 이 단위 대표 사례로 1회 보충'},
             'practice': {'span': 'will be continuously provided to consumers',
                          'formula_support': {'en': 'be p.p.', 'ko': '~되다'},
                          'support': [('s57', 'will V'), ('s57', 'continuously'), ('s57', 'provided'), ('s57', 'to'), ('s57', 'consumers')],
                          'answer_ko': '소비자들에게 지속적으로 제공될 것이다'}},
        ],
        'formula_routes': [
            {'function': ('s56', 'have p.p.', 0), 'route': 'hint', 'hint_index': 0,
             'review_record': 'have become: 빈 힌트 문장의 능동 완료 기능 결합 힌트'},
            {'function': ('s57', 'be p.p.', 0), 'route': 'analysis', 'grammar_point_id': 'u5-gp4',
             'review_record': 'will be continuously provided: 가주어 힌트 표시 범위 안이라 분석 보충 u5-gp4로 연결'},
            {'function': ('s58', 'be p.p.', 0), 'route': 'analysis', 'grammar_point_id': 'u5-gp4',
             'review_record': 'are really needed: 관계사 힌트 표시 범위 안이라 같은 공식의 단위 대표 u5-gp4로 연결'},
        ],
        'relations': [
            {'head': {'id': 'u5-r1h', 'text': 'disposable', 'meaning_ko': '일회용의'},
             'synonym': {'id': 'u5-r1s', 'text': 'single-use', 'meaning_ko': '한 번 쓰고 버리는'},
             'antonym': {'id': 'u5-r1a', 'text': 'reusable', 'meaning_ko': '재사용 가능한'}},
            {'head': {'id': 'u5-r2h', 'text': 'beneficial', 'meaning_ko': '유익한, 이로운'},
             'synonym': {'id': 'u5-r2s', 'text': 'helpful', 'meaning_ko': '도움이 되는'},
             'antonym': {'id': 'u5-r2a', 'text': 'harmful', 'meaning_ko': '해로운'}},
            {'head': {'id': 'u5-r3h', 'text': 'crucial', 'meaning_ko': '매우 중요한, 결정적인'},
             'synonym': {'id': 'u5-r3s', 'text': 'vital', 'meaning_ko': '필수적인, 매우 중요한'},
             'antonym': {'id': 'u5-r3a', 'text': 'trivial', 'meaning_ko': '사소한, 하찮은'}},
        ],
    }


def workbook():
    return {
        'relation_order': ['u5-r2s', 'u5-r1a', 'u5-r3h', 'u5-r2a', 'u5-r1h', 'u5-r3s', 'u5-r2h', 'u5-r3a', 'u5-r1s'],
        'key_sentence_ids': ['s50', 's58'],
        'question_id': 'Q05',
        'syntax_point_ids': ['u5-gp1', 'u5-gp2', 'u5-gp3', 'u5-gp4'],
    }
