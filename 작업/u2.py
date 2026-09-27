"""공통 단위 2: Subscriptions are everywhere (s07~s17, 단락 p02~p04; 짧은 단락이 있어 소제목 전체 묶음)."""
from author import S, link
from u1 import pp, v3

W = {'concept': 'u2-w1', 'initially': 'u2-w2', 'prioritize': 'u2-w3', 'revenue': 'u2-w4',
     'loyalty': 'u2-w5', 'perspective': 'u2-w6', 'drivers': 'u2-w7', 'consumption': 'u2-w8'}


def sentences(T):
    out = []

    # ---------------- s07 ----------------
    s = S('s07', T['s07'])
    s.ch('To be sure,', '분명히,')
    s.ch('the subscription economy is a popular economic model', '구독 경제는 인기 있는 경제 모델이다')
    s.ch('nowadays,', '요즘,')
    s.ch('and Jiyun is actively taking part in it.', '그리고 지윤이는 그것에 적극적으로 참여하고 있다.')
    s.natural('분명히 구독 경제는 요즘 인기 있는 경제 모델이며, 지윤이도 그것에 적극적으로 참여하고 있다.')
    s.cl('main', 'the', subj='the subscription economy', verbs=['is'])
    s.cl('main', 'Jiyun', subj='Jiyun', verbs=['is', 'taking'], marker='and')
    s.g('To|be|sure', 'to be sure', '분명히, 확실히')
    s.g('subscription|economy', 'subscription economy', '구독 경제 (정기적으로 이용료를 내고 상품·서비스를 이용하는 경제 방식)')
    s.g('is', 'is', '~이다')
    s.g('popular', 'popular', '인기 있는')
    s.g('economic', 'economic', '경제의')
    s.g('model', 'model', '모델, 방식')
    s.g('nowadays', 'nowadays', '요즘')
    f = s.g('is', 'be V-ing', '~하고 있다', kind='function', combines_with=[], at=s.text.index('is actively'))
    s.g('actively', 'actively', '적극적으로')
    tk = s.g('taking|part|in', 'take part in', '~에 참여하다', verb_form=pp('ing', s, 'taking', 'take'))
    link(f, tk)
    s.g('it', 'it', '그것', referent_ko='구독 경제')
    s.review = ('두 독립절(and). 둘째 절은 현재진행 is taking part in(사이 부사 actively). take part in 숙어 한 청크. '
                '관계사·접속사절·수동 없음 → 힌트 없음.')
    out.append(s)

    # ---------------- s08 ----------------
    s = S('s08', T['s08'])
    s.ch('The concept', '개념은')
    s.ch('of business models', '비즈니스 모델들의')
    s.ch('based on subscriptions', '구독에 기반한')
    s.ch('is not new.', '새롭지 않다.')
    s.natural('구독에 기반한 비즈니스 모델이라는 개념은 새로운 것이 아니다.')
    s.cl('main', 'The', subj='The concept of business models based on subscriptions', verbs=['is'], disp='The concept',
         disp_review='중심명사 concept까지 표시하고 뒤수식 of business models based on subscriptions는 제외')
    s.g('concept', 'concept', '개념', star=W['concept'])
    s.g('of', 'of', '~의')
    s.g('business|models', 'business models', '비즈니스 모델들, 사업 방식들')
    bs = s.g('based|on', 'based on', '(~에) 기반한', verb_form=pp('past-participle', s, 'based', 'base'))
    s.g('subscriptions', 'subscriptions', '구독들')
    s.g('is', 'is', '~이다')
    s.g('not', 'not', '~이 아닌')
    s.g('new', 'new', '새로운')
    s.brk('of', 'postnominal-preposition', 'of business models는 앞 명사 The concept을 뒤에서 꾸미는 전치사구')
    s.hint('business models [based on subscriptions]', '[구독에 기반한] 비즈니스 모델들', span='business models based on subscriptions',
           label='과거분사 후치수식', links=[(['based'], ['기반한'])], participle_focus_gloss_id=bs['id'],
           meaning='구독에 기반한 비즈니스 모델들',
           explanation='과거분사 based가 이끄는 based on subscriptions가 앞 명사 business models를 뒤에서 꾸민다.')
    s.review = ('단일 주절, 주어 The concept of business models based on subscriptions(표시는 The concept). of 앞 후치수식 경계, '
                'based on … 과거분사 후치수식 → 힌트. 수동 없음(based는 독립 과거분사).')
    out.append(s)

    # ---------------- s09 ----------------
    s = S('s09', T['s09'])
    s.ch('Initially', '처음에')
    s.ch('it was limited to products', '그것은 제품들에 한정되었다')
    s.ch('such as milk and newspapers.', '우유와 신문 같은.')
    s.natural('처음에 그것은 우유와 신문 같은 제품에 한정되었다.')
    s.cl('main', 'it', subj='it', verbs=['was', 'limited'])
    s.g('Initially', 'initially', '처음에', star=W['initially'])
    s.g('it', 'it', '그것은', referent_ko='구독에 기반한 비즈니스 모델이라는 개념')
    f = s.g('was', 'be p.p.', '~되다', kind='function', combines_with=[])
    lm = s.g('limited', 'limited', '한정된, 제한된', verb_form=pp('passive-participle', s, 'limited', 'limit', f['id']))
    link(f, lm)
    s.g('to', 'to', '~에')
    s.g('products', 'products', '제품들')
    s.g('such|as', 'such as', '~ 같은')
    s.g('milk', 'milk', '우유')
    s.g('newspapers', 'newspapers', '신문들')
    s.brk('such', 'postnominal-preposition', 'such as milk and newspapers는 앞 명사 products를 뒤에서 꾸미는 전치사구')
    s.vf_hint(fn=f, lex=lm, en='was limited', ko='한정되었다', formula='be p.p.', step_form='limited', step_ko='한정된',
              en_mark=['was'], ko_mark=['되었다'], span='it was limited', meaning='한정되었다',
              explanation='빈 힌트 문장의 수동태 후보: was limited(과거 수동). 주어 it과 to products 이하 제외.')
    s.review = ('단일 주절 수동 was limited to(to는 대표 뜻 ~에로 분리). such as … 후치수식 앞에서 끊음. '
                '관계사·접속사절 없음 → 빈 힌트 문장의 수동태 기능 결합 힌트.')
    out.append(s)

    # ---------------- s10 ----------------
    s = S('s10', T['s10'])
    s.ch('However,', '하지만,')
    s.ch('these business models have expanded to all industries,', '이 비즈니스 모델들은 모든 산업들로 확장되었다,')
    s.ch('including entertainment, technology, fashion, education, and much more.', '엔터테인먼트, 기술, 패션, 교육, 그리고 훨씬 더 많은 것을 포함하여.')
    s.natural('하지만 이 비즈니스 모델들은 엔터테인먼트, 기술, 패션, 교육을 비롯해 훨씬 더 많은 분야를 포함한 모든 산업으로 확장되었다.')
    s.cl('main', 'these', subj='these business models', verbs=['have', 'expanded'])
    s.g('However', 'however', '하지만')
    s.g('these', 'these', '이')
    s.g('business|models', 'business models', '비즈니스 모델들, 사업 방식들')
    f = s.g('have', 'have p.p.', '~했다', kind='function', combines_with=[])
    ex = s.g('expanded', 'expand', '확장되다, 넓어지다 (expanded는 expand의 p.p.형)',
             verb_form=pp('perfect-participle', s, 'expanded', 'expand', f['id']))
    link(f, ex)
    s.g('to', 'to', '~로')
    s.g('all', 'all', '모든')
    s.g('industries', 'industries', '산업들')
    s.g('including', 'including', '~을 포함하여')
    s.g('entertainment', 'entertainment', '엔터테인먼트, 오락')
    s.g('technology', 'technology', '기술')
    s.g('fashion', 'fashion', '패션')
    s.g('education', 'education', '교육')
    s.g('much|more', 'much more', '훨씬 더 많은 것')
    s.brk('including', 'postnominal-preposition', 'including … 이하는 앞 명사 all industries의 예를 드는 전치사구')
    s.vf_hint(fn=f, lex=ex, en='have expanded', ko='확장되었다', formula='have p.p.', step_form='expand', step_ko='확장되다',
              en_mark=['have'], ko_mark=['었다'], span='these business models have expanded', meaning='확장되었다',
              explanation='빈 힌트 문장의 능동 완료 후보: have expanded(과거부터 지금까지 넓어진 결과). 주어와 to all industries 이하 제외.')
    s.review = ('단일 주절 현재완료 have expanded(자동사 expand: 확장되다). including은 전치사로 예시 나열. '
                '관계사·접속사절 없음 → 능동 완료 기능 결합 힌트.')
    out.append(s)

    # ---------------- s11 ----------------
    s = S('s11', T['s11'], key=True)
    s.ch('Instead of creating a hit product', '히트 상품을 만들어 내는 것 대신에')
    s.ch('that will be sold once,', '한 번 팔릴,')
    s.ch('companies now prioritize providing continuing value,', '기업들은 이제 지속적인 가치를 제공하는 것을 우선시한다,')
    s.ch('such as new content, more personalization,', '새로운 콘텐츠, 더 많은 개인 맞춤화,')
    s.ch('or access', '또는 접근 같은')
    s.ch('to updates.', '업데이트에 대한.')
    s.natural('한 번 팔리고 끝날 히트 상품을 만드는 대신, 기업들은 이제 새로운 콘텐츠, 더 많은 개인 맞춤화, 업데이트 이용 같은 지속적인 가치를 제공하는 것을 우선시한다.')
    s.cl('main', 'Instead', subj='companies', verbs=['prioritize'])
    s.cl('subject_relative', 'that', verbs=['will be sold'], marker='that')
    s.g('Instead|of', 'instead of', '~ 대신에')
    f1 = s.g('creating', 'V-ing', '~하는 것', kind='function', combines_with=[])
    cr = s.g('creating', 'create', '만들어 내다', same=True, verb_form=pp('ing', s, 'creating', 'create'))
    link(f1, cr)
    s.g('hit|product', 'hit product', '히트 상품 (크게 성공한 상품)')
    rel = s.g('that', 'that V′', 'V′하는 (관계대명사)')
    fw = s.g('will', 'will V', '~할 것이다', kind='function', combines_with=[])
    fb = s.g('be', 'be p.p.', '~되다', kind='function', combines_with=[])
    sd = s.g('sold', 'sold', '팔린', verb_form=pp('passive-participle', s, 'sold', 'sell', fb['id']))
    link(fb, sd)
    link(fw, sd)
    s.g('once', 'once', '한 번')
    s.g('companies', 'companies', '기업들, 회사들')
    s.g('now', 'now', '이제')
    s.g('prioritize', 'prioritize', '우선시하다', star=W['prioritize'])
    f2 = s.g('providing', 'V-ing', '~하는 것', kind='function', combines_with=[])
    pv = s.g('providing', 'provide', '제공하다', same=True, verb_form=pp('ing', s, 'providing', 'provide'))
    link(f2, pv)
    s.g('continuing', 'continuing', '지속적인, 계속되는')
    s.g('value', 'value', '가치')
    s.g('such|as', 'such as', '~ 같은')
    s.g('new', 'new', '새로운')
    s.g('content', 'content', '콘텐츠, 내용물')
    s.g('more', 'more', '더 많은')
    s.g('personalization', 'personalization', '개인 맞춤화')
    s.g('or', 'or', '또는')
    s.g('access', 'access', '접근, 이용 (권한)')
    s.g('to', 'to', '~에 대한', at=s.text.index('to updates'))
    s.g('updates', 'updates', '업데이트들')
    s.brk('such', 'postnominal-preposition', 'such as … 이하는 앞 명사 continuing value의 예를 드는 전치사구')
    s.brk('to', 'postnominal-preposition', 'to updates는 앞 명사 access를 뒤에서 꾸미는 전치사구', after=s.text.index('access'))
    s.hint('a hit product [that will be sold]', '[팔릴] 히트 상품', span='a hit product that will be sold',
           label='주격 관계대명사 that', links=[(['that'], ['릴'])],
           meaning='(한 번) 팔릴 히트 상품',
           explanation='선행사 a hit product를 주격 관계대명사 that이 받아 will be sold once가 꾸민다. V′ will be sold까지만 표시하고 once는 제외. 미래 수동의 관형 연결 ‘팔릴’.')
    s.hint('[Instead of creating]', '[만들어 내는 것 대신에]', span='Instead of creating', label='전치사 instead of + 동명사',
           links=[(['Instead of', 'ing'], ['는 것 대신에'])],
           meaning='(히트 상품을) 만들어 내는 것 대신에',
           explanation='전치사구 instead of 뒤에 동명사 creating이 와서 ‘~하는 것 대신에’. 목적어 a hit product는 표시에서 제외.')
    s.relative_ids = [rel['id']]
    s.review = ('주절 companies now prioritize providing …(문두 Instead of + 동명사 부사구) + 주격 관계절 that will be sold once(선행사 a hit product). '
                '관계절 동사 will be sold는 조동사 will V와 수동 be p.p.를 각각 각주로 연결. 힌트 2개(필수 관계사, instead of + 동명사). '
                '수동 be p.p.는 결합 힌트를 두지 않고 단위 분석 보충 u2-gp4로 연결. access to updates는 to 앞 후치수식 경계.')
    out.append(s)

    # ---------------- s12 ----------------
    s = S('s12', T['s12'])
    s.ch('Customers pay for these benefits', '고객들은 이러한 혜택들에 대해 비용을 지불한다')
    s.ch('via a regular subscription.', '정기적인 구독을 통해.')
    s.natural('고객들은 정기 구독을 통해 이러한 혜택에 대한 비용을 지불한다.')
    s.cl('main', 'Customers', subj='Customers', verbs=['pay'])
    s.g('Customers', 'customers', '고객들')
    s.g('pay|for', 'pay for', '~에 대해 비용을 지불하다')
    s.g('these', 'these', '이러한')
    s.g('benefits', 'benefits', '혜택들, 이점들')
    s.g('via', 'via', '~을 통해')
    s.g('regular', 'regular', '정기적인')
    s.g('subscription', 'subscription', '구독')
    s.review = '단일 주절 pay for(숙어) + via 전치사구. 관계사·접속사절·수동 없음 → 힌트 없음.'
    out.append(s)

    # ---------------- s13 ----------------
    s = S('s13', T['s13'])
    s.ch('The subscription economy brings advantages', '구독 경제는 이점들을 가져다준다')
    s.ch('for both companies and consumers.', '기업과 소비자 둘 다에게.')
    s.natural('구독 경제는 기업과 소비자 모두에게 이점을 가져다준다.')
    s.cl('main', 'The', subj='The subscription economy', verbs=['brings'])
    s.g('subscription|economy', 'subscription economy', '구독 경제')
    s.g('brings', 'bring', '가져다주다', verb_form=v3(s, 'brings', 'bring', 'The subscription economy'))
    s.g('advantages', 'advantages', '이점들, 장점들')
    s.g('for', 'for', '~에게')
    s.g('both|and', 'both A and B', 'A와 B 둘 다')
    s.g('companies', 'companies', '기업들, 회사들')
    s.g('consumers', 'consumers', '소비자들')
    s.hint('[both companies and consumers]', '[기업과 소비자 둘 다]', span='both companies and consumers',
           label='상관접속사 both A and B', links=[(['both', 'and'], ['과', '둘 다'])],
           meaning='기업과 소비자 둘 다',
           explanation='both A and B: A와 B 둘 다. A=companies, B=consumers. 이점을 받는 쪽이 한쪽이 아니라 양쪽이라는 점이 뒤 두 문장(기업의 이점, 소비자의 이점)으로 이어진다.')
    s.review = '단일 주절. both A and B 상관접속사(뒤 s14 기업·s15~s16 소비자 이점으로 전개) → 힌트. 수동 없음.'
    out.append(s)

    # ---------------- s14 ----------------
    s = S('s14', T['s14'])
    s.ch('Companies can have a stable revenue', '기업들은 안정적인 수입을 가질 수 있다')
    s.ch('and build customer loyalty', '그리고 고객 충성도를 쌓을 수 있다')
    s.ch('by using the subscription model.', '구독 모델을 사용함으로써.')
    s.natural('기업들은 구독 모델을 사용함으로써 안정적인 수입을 얻고 고객 충성도를 쌓을 수 있다.')
    s.cl('main', 'Companies', subj='Companies', verbs=['can', 'have', 'and', 'build'])
    s.g('Companies', 'companies', '기업들, 회사들')
    f = s.g('can', 'can V', '~할 수 있다', kind='function', combines_with=[])
    hv = s.g('have', 'have', '가지다, 얻다')
    s.g('stable', 'stable', '안정적인')
    s.g('revenue', 'revenue', '수입, 수익', star=W['revenue'])
    bd = s.g('build', 'build', '쌓다, 구축하다')
    link(f, hv, bd)
    s.g('customer|loyalty', 'customer loyalty', '고객 충성도 (고객이 한 기업을 꾸준히 이용하는 마음)', star=W['loyalty'])
    f2 = s.g('by', 'by V-ing', '~함으로써', kind='function', combines_with=[])
    us = s.g('using', 'use', '사용하다', verb_form=pp('ing', s, 'using', 'use'))
    link(f2, us)
    s.g('subscription|model', 'subscription model', '구독 모델, 구독 방식')
    s.hint('[by using]', '[사용함으로써]', span='by using', label='전치사 by + 동명사',
           links=[(['by', 'ing'], ['함으로써'])], meaning='(구독 모델을) 사용함으로써',
           explanation='전치사 by + 동명사 using: ~함으로써(수단). 기업이 이점을 얻는 방법. 목적어 the subscription model은 표시에서 제외.')
    s.review = '주어 Companies의 병렬 동사 can have and build(can이 둘 다에 걸림). by + 동명사(수단) → 힌트. 관계사·수동 없음.'
    out.append(s)

    # ---------------- s15 ----------------
    s = S('s15', T['s15'])
    s.ch('From the consumers’ perspective,', '소비자들의 관점에서,')
    s.ch('they can enjoy a wider range of choices', '그들은 더 넓은 범위의 선택을 누릴 수 있다')
    s.ch('and personalized experiences.', '그리고 개인 맞춤형 경험을.')
    s.natural('소비자의 관점에서 보면, 그들은 더 다양한 선택과 개인 맞춤형 경험을 누릴 수 있다.')
    s.cl('main', 'they', subj='they', verbs=['can', 'enjoy'])
    s.g('From', 'from', '~에서')
    s.g('consumers’', 'consumers’', '소비자들의')
    s.g('perspective', 'perspective', '관점', star=W['perspective'])
    s.g('they', 'they', '그들은', referent_ko='소비자들')
    f = s.g('can', 'can V', '~할 수 있다', kind='function', combines_with=[])
    ej = s.g('enjoy', 'enjoy', '누리다, 즐기다')
    link(f, ej)
    q = s.g('a wider range of', 'a wider range of', '더 넓은 범위의, 더 다양한')
    s.g('choices', 'choices', '선택(들)')
    s.g('personalized', 'personalized', '개인 맞춤형의, 개인에게 맞춘', verb_form=pp('past-participle', s, 'personalized', 'personalize'))
    s.g('experiences', 'experiences', '경험들')
    s.prot('a wider range of', 'quantity-kind-of', '범위 표현 a wider range of가 뒤 명사 choices 앞에서 ‘더 넓은 범위의’로 같은 어순 대응', gloss=q)
    s.review = ('단일 주절 can enjoy(목적어 a wider range of choices와 personalized experiences 병렬). a wider range of는 같은 어순 ~의 수량·범위 표현. '
                'personalized는 명사 앞 독립 과거분사. 관계사·접속사절·수동 없음 → 힌트 없음.')
    out.append(s)

    # ---------------- s16 ----------------
    s = S('s16', T['s16'])
    s.ch('They can also save money', '그들은 또한 돈을 절약할 수 있다')
    s.ch('by having flexible subscription contracts.', '유연한 구독 계약을 가짐으로써.')
    s.natural('그들은 또한 융통성 있는 구독 계약을 맺어 돈을 절약할 수 있다.')
    s.cl('main', 'They', subj='They', verbs=['can', 'save'])
    s.g('They', 'they', '그들은', referent_ko='소비자들')
    f = s.g('can', 'can V', '~할 수 있다', kind='function', combines_with=[])
    s.g('also', 'also', '또한')
    sv = s.g('save', 'save', '절약하다')
    link(f, sv)
    s.g('money', 'money', '돈')
    f2 = s.g('by', 'by V-ing', '~함으로써', kind='function', combines_with=[])
    hv = s.g('having', 'have', '가지다', verb_form=pp('ing', s, 'having', 'have'))
    link(f2, hv)
    s.g('flexible', 'flexible', '유연한, 융통성 있는')
    s.g('subscription', 'subscription', '구독')
    s.g('contracts', 'contracts', '계약들')
    s.hint('[by having]', '[가짐으로써]', span='by having', label='전치사 by + 동명사',
           links=[(['by', 'ing'], ['짐으로써'])], meaning='(유연한 구독 계약을) 가짐으로써',
           explanation='전치사 by + 동명사 having: ~함으로써(수단). 돈을 절약하는 방법. 목적어 flexible subscription contracts는 표시에서 제외.')
    s.review = '단일 주절 can also save(사이 부사 also). by + 동명사(수단) → 힌트. 관계사·수동 없음.'
    out.append(s)

    # ---------------- s17 ----------------
    s = S('s17', T['s17'], key=True)
    s.ch('The rise', '부상은')
    s.ch('of the subscription economy', '구독 경제의')
    s.ch('is closely connected to two major drivers:', '두 가지 주요 동인에 밀접하게 연결되어 있다:')
    s.ch('changes', '변화들')
    s.ch('in consumption trends', '소비 추세에서의')
    s.ch('and the rapid growth', '그리고 급속한 성장')
    s.ch('of online platforms.', '온라인 플랫폼들의.')
    s.natural('구독 경제의 부상은 두 가지 주요 동인, 즉 소비 추세의 변화와 온라인 플랫폼의 급속한 성장과 밀접하게 연결되어 있다.')
    s.cl('main', 'The', subj='The rise of the subscription economy', verbs=['is', 'connected'], disp='The rise',
         disp_review='중심명사 rise까지 표시하고 뒤수식 of the subscription economy는 제외')
    s.g('rise', 'rise', '부상, 성장 (흔한 뜻: 오르다)')
    s.g('of', 'of', '~의')
    s.g('subscription|economy', 'subscription economy', '구독 경제')
    f = s.g('is', 'be p.p.', '~되어 있다', kind='function', combines_with=[])
    s.g('closely', 'closely', '밀접하게')
    cn = s.g('connected', 'connected', '연결된, 관련된', verb_form=pp('passive-participle', s, 'connected', 'connect', f['id']))
    link(f, cn)
    s.g('to', 'to', '~에')
    s.g('two', 'two', '두')
    s.g('major', 'major', '주요한')
    s.g('drivers', 'drivers', '동인들, 원동력들 (흔한 뜻: 운전자들)', star=W['drivers'])
    s.g('changes', 'changes', '변화들')
    s.g('in', 'in', '~에서의')
    s.g('consumption', 'consumption', '소비', star=W['consumption'])
    s.g('trends', 'trends', '추세들, 경향들')
    s.g('rapid', 'rapid', '급속한, 빠른')
    s.g('growth', 'growth', '성장')
    s.g('of', 'of', '~의', at=s.text.index('of online'))
    s.g('online', 'online', '온라인의')
    s.g('platforms', 'platforms', '플랫폼들 (서비스가 이루어지는 온라인 공간)')
    s.brk('of', 'postnominal-preposition', 'of the subscription economy는 앞 명사 The rise를 뒤에서 꾸미는 전치사구')
    s.brk('in', 'postnominal-preposition', 'in consumption trends는 앞 명사 changes를 뒤에서 꾸미는 전치사구', after=s.text.index('changes'))
    s.brk('of', 'postnominal-preposition', 'of online platforms는 앞 명사 the rapid growth를 뒤에서 꾸미는 전치사구', after=s.text.index('growth'))
    s.vf_hint(fn=f, lex=cn, en='is closely connected', ko='밀접하게 연결되어 있다', formula='be p.p.', step_form='connected', step_ko='연결된',
              en_mark=['is'], ko_mark=['되어 있다'], span='The rise of the subscription economy is closely connected',
              meaning='밀접하게 연결되어 있다',
              explanation='빈 힌트 문장의 수동태 후보: is closely connected(상태 수동, 표시 범위 안 부사 closely 보존). 주어와 to two major drivers 이하 제외.')
    s.review = ('단일 주절 수동 is closely connected to(to는 대표 뜻 ~에로 분리). 콜론 뒤 changes … and the rapid growth …는 two major drivers의 내용을 풀어 쓴 동격. '
                'of·in·of 앞 후치수식 경계. 관계사·접속사절 없음 → 빈 힌트 문장의 수동태 기능 결합 힌트.')
    out.append(s)
    return out


UNIT = {
    'id': 'u2', 'source_id': 'src', 'paragraph_ids': ['p02', 'p03', 'p04'],
    'sentence_ids': [f's{n:02d}' for n in range(7, 18)],
    'today_words': [
        {'id': W['concept'], 'text': 'concept', 'meaning_ko': '개념'},
        {'id': W['initially'], 'text': 'initially', 'meaning_ko': '처음에'},
        {'id': W['prioritize'], 'text': 'prioritize', 'meaning_ko': '우선시하다'},
        {'id': W['revenue'], 'text': 'revenue', 'meaning_ko': '수입, 수익'},
        {'id': W['loyalty'], 'text': 'customer loyalty', 'meaning_ko': '고객 충성도'},
        {'id': W['perspective'], 'text': 'perspective', 'meaning_ko': '관점'},
        {'id': W['drivers'], 'text': 'drivers', 'meaning_ko': '동인들, 원동력들'},
        {'id': W['consumption'], 'text': 'consumption', 'meaning_ko': '소비'},
    ],
}


def analysis(_):
    return {
        'heading_kind': '주제',
        'title_or_topic_en': 'The Spread and Benefits of the Subscription Economy',
        'title_or_topic_ko': '구독 경제의 확산과 이점',
        'intent_ko': '구독 경제는 오래된 개념이지만 이제 모든 산업으로 퍼져 기업과 소비자 모두에게 이점을 주고 있으며, 그 성장은 소비 추세의 변화와 온라인 플랫폼의 성장이라는 두 동인과 관련된다는 점을 설명하는 글이다.',
        'flow': [
            {'sentence_ids': ['s07', 's08', 's09', 's10'], 'label': '확산',
             'text_ko': '구독 경제는 지윤이처럼 많은 사람이 참여하는 인기 모델이다. 처음에는 우유·신문 같은 제품에만 쓰였지만 지금은 모든 산업으로 퍼졌다.'},
            {'sentence_ids': ['s11', 's12'], 'label': '사업 방식의 변화',
             'text_ko': '기업들은 한 번 팔고 끝나는 히트 상품 대신 새 콘텐츠·맞춤화·업데이트 같은 지속적인 가치를 제공하고, 고객은 정기 구독으로 그 값을 낸다.'},
            {'sentence_ids': ['s13', 's14', 's15', 's16', 's17'], 'label': '이점과 동인',
             'text_ko': '구독 경제는 기업(안정적 수입·고객 충성도)과 소비자(다양한 선택·맞춤 경험·절약) 모두에게 이점을 준다. 끝으로 구독 경제의 부상을 이끈 두 동인을 제시하며 다음 내용을 예고한다.'},
        ],
        'easy_explanations': [
            {'sentence_id': 's11', 'explanatory_sentences': [
                '11번 문장은 10번에서 말한 구독 모델이 기업의 판매 방식을 어떻게 바꿨는지 보여 준다.',
                '예전에는 크게 인기를 끄는 상품 하나를 만들어 한 번 팔면 거래가 끝났다.',
                '이제 기업들은 고객이 계속 돈을 낼 만한 가치를 꾸준히 제공하는 데 힘을 쏟는다.',
                '새 콘텐츠, 나에게 맞춘 서비스, 업데이트를 받을 권리 같은 것이 그런 가치다.']},
            {'sentence_id': 's14', 'explanatory_sentences': [
                '14번 문장은 13번에서 말한 이점 중 기업이 얻는 이점을 먼저 설명한다.',
                '구독자는 매달 정해진 돈을 내기 때문에 기업은 수입을 미리 예상할 수 있다.',
                '이것이 안정적인 수입이다.',
                '또 고객이 한 서비스를 오래 쓰면서 그 기업을 계속 찾게 되는데, 이것을 고객 충성도라고 한다.']},
            {'sentence_id': 's17', 'explanatory_sentences': [
                '17번 문장은 이 부분을 마무리하면서 구독 경제가 커진 두 가지 이유를 꺼낸다.',
                '동인은 어떤 일이 일어나게 만드는 힘을 말한다.',
                '첫째 동인은 사람들이 물건을 사고 쓰는 방식이 달라진 것이다.',
                '둘째 동인은 온라인 플랫폼이 빠르게 성장한 것이다.',
                '뒤 소제목들에서 이 두 가지를 하나씩 자세히 다룬다.']},
        ],
        'grammar_points': [
            {'id': 'u2-gp1', 'sentence_id': 's08', 'span': 'business models based on subscriptions',
             'title': '명사 + 과거분사구: ~된(한) 명사', 'formula_key': 'N + p.p.',
             'explanation': '공식: 명사(N) + p.p.구 — p.p.된(한) N. N = business models(비즈니스 모델들), p.p. = based on(~에 기반한), '
                            'on의 대상 = subscriptions(구독). → 구독에 기반한 비즈니스 모델들. 비즈니스 모델이 구독을 바탕으로 ‘짜인’ 쪽이라 수동의 뜻을 가진 과거분사 based를 쓴다.',
             'practice': {'span': 'business models based on subscriptions',
                          'formula_support': {'en': 'N + p.p.', 'ko': 'p.p.된(한) N'},
                          'support': [('s08', 'business models'), ('s08', 'based on'), ('s08', 'subscriptions')],
                          'answer_ko': '구독에 기반한 비즈니스 모델들'}},
            {'id': 'u2-gp2', 'sentence_id': 's11', 'span': 'Instead of creating a hit product',
             'title': 'instead of + V-ing: ~하는 것 대신에', 'formula_key': 'instead of V-ing',
             'explanation': '공식: instead of + V-ing — ~하는 것 대신에. V-ing = creating(만들어 내다), 목적어 = a hit product(히트 상품). '
                            '→ 히트 상품을 만들어 내는 것 대신에. 전치사 of 뒤라 동사가 -ing(동명사)로 바뀌었다.',
             'practice': {'span': 'Instead of creating a hit product',
                          'formula_support': {'en': 'instead of V-ing', 'ko': '~하는 것 대신에'},
                          'support': [('s11', 'create'), ('s11', 'hit product')],
                          'answer_ko': '히트 상품을 만들어 내는 것 대신에'}},
            {'id': 'u2-gp3', 'sentence_id': 's13', 'span': 'for both companies and consumers',
             'title': 'both A and B: A와 B 둘 다', 'formula_key': 'both A and B',
             'explanation': '공식: both A and B — A와 B 둘 다. A = companies(기업들), B = consumers(소비자들), 앞의 for = ~에게. '
                            '→ 기업과 소비자 둘 다에게. 이점을 받는 쪽이 양쪽 모두라는 뜻이다.',
             'practice': {'span': 'for both companies and consumers',
                          'formula_support': {'en': 'both A and B', 'ko': 'A와 B 둘 다'},
                          'support': [('s13', 'for'), ('s13', 'companies'), ('s13', 'consumers')],
                          'answer_ko': '기업과 소비자 둘 다에게'}},
            {'id': 'u2-gp4', 'sentence_id': 's11', 'span': 'a hit product that will be sold once',
             'title': 'be p.p.: ~되다 (will be sold: 팔릴 것이다)', 'formula_key': 'be p.p.',
             'explanation': '공식: be p.p. — ~되다. p.p. = sold(팔린, sell의 p.p.형), 앞의 will = ~할 것이다, 뒤의 once = 한 번. '
                            '→ 한 번 팔릴 것이다. 상품은 스스로 파는 것이 아니라 ‘팔리는’ 대상이라 수동을 쓴다. 관계사 that과 이으면 ‘한 번 팔릴 히트 상품’이 된다.',
             'supplemental': {'function': ('s11', 'be p.p.', 0),
                              'reason': 's11의 수동 will be sold는 관계사·instead of 힌트가 이미 있어 결합 힌트로 선정하지 않았고, 기본 분석 3개에 be p.p. 설명이 없어 이 단위 대표 사례로 1회 보충'},
             'practice': {'span': 'will be sold once',
                          'formula_support': {'en': 'be p.p.', 'ko': '~되다'},
                          'support': [('s11', 'will V'), ('s11', 'sold'), ('s11', 'once')],
                          'answer_ko': '한 번 팔릴 것이다'}},
        ],
        'formula_routes': [
            {'function': ('s09', 'be p.p.', 0), 'route': 'hint', 'hint_index': 0,
             'review_record': 'was limited: 빈 힌트 문장의 수동태 기능 결합 힌트'},
            {'function': ('s10', 'have p.p.', 0), 'route': 'hint', 'hint_index': 0,
             'review_record': 'have expanded: 능동 완료 기능 결합 힌트'},
            {'function': ('s11', 'be p.p.', 0), 'route': 'analysis', 'grammar_point_id': 'u2-gp4',
             'review_record': 'will be sold: 관계사·instead of 힌트가 있어 분석 보충 u2-gp4로 연결'},
            {'function': ('s17', 'be p.p.', 0), 'route': 'hint', 'hint_index': 0,
             'review_record': 'is closely connected: 빈 힌트 문장의 수동태 기능 결합 힌트'},
        ],
        'relations': [
            {'head': {'id': 'u2-r1h', 'text': 'stable', 'meaning_ko': '안정적인'},
             'synonym': {'id': 'u2-r1s', 'text': 'steady', 'meaning_ko': '꾸준한, 안정된'},
             'antonym': {'id': 'u2-r1a', 'text': 'unstable', 'meaning_ko': '불안정한'}},
            {'head': {'id': 'u2-r2h', 'text': 'flexible', 'meaning_ko': '유연한, 융통성 있는'},
             'synonym': {'id': 'u2-r2s', 'text': 'adaptable', 'meaning_ko': '적응할 수 있는, 융통성 있는'},
             'antonym': {'id': 'u2-r2a', 'text': 'rigid', 'meaning_ko': '엄격한, 융통성 없는'}},
            {'head': {'id': 'u2-r3h', 'text': 'rapid', 'meaning_ko': '급속한, 빠른'},
             'synonym': {'id': 'u2-r3s', 'text': 'swift', 'meaning_ko': '신속한, 빠른'},
             'antonym': {'id': 'u2-r3a', 'text': 'gradual', 'meaning_ko': '점진적인, 서서히 일어나는'}},
        ],
    }


def workbook():
    return {
        'relation_order': ['u2-r3s', 'u2-r1a', 'u2-r2h', 'u2-r3a', 'u2-r1s', 'u2-r2a', 'u2-r3h', 'u2-r1h', 'u2-r2s'],
        'key_sentence_ids': ['s11', 's17'],
        'question_id': 'Q02',
        'syntax_point_ids': ['u2-gp1', 'u2-gp2', 'u2-gp3', 'u2-gp4'],
    }
