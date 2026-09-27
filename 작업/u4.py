"""공통 단위 4: Online platforms drive the subscription economy (s37~s43, 단락 p08~p09; 짧은 단락이 있어 소제목 전체 묶음)."""
from author import S, link
from u1 import pp, v3

W = {'development': 'u4-w1', 'devices': 'u4-w2', 'centered': 'u4-w3', 'no_choice': 'u4-w4',
     'access': 'u4-w5', 'identify': 'u4-w6', 'in_turn': 'u4-w7', 'satisfaction': 'u4-w8'}


def sentences(T):
    out = []

    # ---------------- s37 ----------------
    s = S('s37', T['s37'])
    s.ch('With the development', '발전과 함께')
    s.ch('of various digital devices', '다양한 디지털 기기들의')
    s.ch('centered on smartphones,', '스마트폰을 중심으로 한,')
    s.ch('consumers have been able to do numerous things', '소비자들은 수많은 일들을 할 수 있어 왔다')
    s.ch('with great ease.', '아주 쉽게.')
    s.natural('스마트폰을 중심으로 한 다양한 디지털 기기가 발전하면서 소비자들은 수많은 일을 아주 쉽게 할 수 있게 되었다.')
    s.cl('main', 'With', subj='consumers', verbs=['have', 'been'])
    s.g('With', 'with', '~와 함께')
    s.g('development', 'development', '발전', star=W['development'])
    s.g('of', 'of', '~의')
    s.g('various', 'various', '다양한')
    s.g('digital', 'digital', '디지털의')
    s.g('devices', 'devices', '기기들, 장치들', star=W['devices'])
    ce = s.g('centered|on', 'centered on', '(~을) 중심으로 한', star=W['centered'],
             verb_form=pp('past-participle', s, 'centered', 'center'))
    s.g('smartphones', 'smartphones', '스마트폰들')
    s.g('consumers', 'consumers', '소비자들')
    f = s.g('have', 'have p.p.', '~해 왔다', kind='function', combines_with=[])
    ba = s.g('been|able|to', 'be able to V', '~할 수 있다 (been은 be의 p.p.형)',
             verb_form=pp('perfect-participle', s, 'been', 'be', f['id']),
             verb_construction={'kind': 'verb-frame', 'verb_span': s.span_of('been'), 'lemma': 'be',
                                'link_spans': [s.span_of('able'), s.span_of('to', s.text.index('able'))],
                                'review_record': 'have been able to do: be able to V의 be가 현재완료 p.p. been으로 쓰임. V=do.'})
    link(f, ba)
    s.g('do', 'do', '하다')
    s.g('numerous', 'numerous', '수많은')
    s.g('things', 'things', '일들, 것들')
    s.g('with|great|ease', 'with great ease', '아주 쉽게')
    s.brk('of', 'postnominal-preposition', 'of various digital devices는 앞 명사 the development를 뒤에서 꾸미는 전치사구')
    s.hint('various digital devices [centered on smartphones]', '[스마트폰을 중심으로 한] 다양한 디지털 기기들',
           span='various digital devices centered on smartphones', label='과거분사 후치수식',
           links=[(['centered'], ['중심으로 한'])], participle_focus_gloss_id=ce['id'],
           meaning='스마트폰을 중심으로 한 다양한 디지털 기기들',
           explanation='과거분사 centered가 이끄는 centered on smartphones가 앞 명사 various digital devices를 뒤에서 꾸민다.')
    s.review = ('문두 With 전치사구(발전과 함께) + 주절 현재완료 have been able to do(U57: V 칸은 have been, able to는 각주 be able to V로 지원). '
                'devices를 꾸미는 과거분사 centered on → 힌트. 능동 완료 have been은 힌트를 분사 후치수식에 쓰고 분석 보충 u4-gp4로 연결.')
    out.append(s)

    # ---------------- s38 ----------------
    s = S('s38', T['s38'])
    s.ch('In the past,', '과거에는,')
    s.ch('people had no choice but to go to the theater', '사람들은 극장에 갈 수밖에 없었다')
    s.ch('or purchase the videos', '또는 비디오들을 구매할 (수밖에 없었다)')
    s.ch('they wanted to watch.', '그들이 보기를 원했던.')
    s.natural('과거에는 사람들이 극장에 가거나 보고 싶은 비디오를 구매할 수밖에 없었다.')
    s.cl('main', 'people', subj='people', verbs=['had'])
    s.cl('subordinate', 'they', subj='they', verbs=['wanted'], marker='that', omitted=True)
    s.g('In|past', 'in the past', '과거에는')
    s.g('people', 'people', '사람들')
    s.g('had|no|choice|but|to', 'have no choice but to V', '~할 수밖에 없다 (had는 have의 과거)', star=W['no_choice'])
    s.g('go', 'go', '가다')
    s.g('to', 'to', '~에', at=s.text.index('to the theater'))
    s.g('theater', 'theater', '극장')
    s.g('or', 'or', '또는')
    s.g('purchase', 'purchase', '구매하다')
    s.g('videos', 'videos', '비디오들')
    s.g('they', 'they', '그들이', referent_ko='과거의 사람들')
    s.g('wanted|to', 'want to V', '~하기를 원하다', verb_form=pp('regular-past', s, 'wanted', 'want'),
        verb_construction={'kind': 'to-complement', 'verb_span': s.span_of('wanted'), 'lemma': 'want',
                           'link_spans': [s.span_of('to', s.text.index('wanted'))], 'review_record': 'wanted to watch: want의 목적어 to V.'})
    s.g('watch', 'watch', '보다')
    s.hint('the videos [(that) they wanted to watch]', '[그들[과거의 사람들]이 보기를 원했던] 비디오들',
           span='the videos they wanted to watch', label='목적격 관계대명사 that 생략', display_mode='omitted-relative',
           omitted_relative='that', links=[(['that'], ['이', '던'])], refs=[('they', '그들', '[과거의 사람들]')],
           meaning='그들이 보기를 원했던 비디오들',
           explanation='선행사 the videos 뒤 목적격 관계대명사 that이 생략된 관계절. the videos는 wanted가 아니라 to watch의 목적어이므로 빈자리가 있는 to watch까지 표시한다(S′ they, V′ wanted).')
    s.review = ('단일 주절 had no choice but to go … or purchase …(to 뒤 두 동사원형이 or로 병렬) + 목적격 관계대명사가 생략된 관계절 they wanted to watch(선행사 the videos). '
                '생략 관계사 힌트 1개. 수동 없음.')
    out.append(s)

    # ---------------- s39 ----------------
    s = S('s39', T['s39'])
    s.ch('Today,', '오늘날에는,')
    s.ch('whoever wants to watch a movie', '영화를 보기를 원하는 사람은 누구든지')
    s.ch('can access online media subscription platforms', '온라인 미디어 구독 플랫폼들에 접속할 수 있다')
    s.ch('and enjoy a vast selection of movies', '그리고 엄청나게 다양한 영화들을 즐길 수 있다')
    s.ch('on their smartphones or other digital devices.', '그들의 스마트폰이나 다른 디지털 기기들에서.')
    s.natural('오늘날에는 영화를 보고 싶은 사람은 누구나 온라인 미디어 구독 플랫폼에 접속해 스마트폰이나 다른 디지털 기기로 엄청나게 다양한 영화를 즐길 수 있다.')
    s.cl('main', 'Today', subj='whoever wants to watch a movie', verbs=['can', 'access', 'and', 'enjoy'])
    s.cl('subject_relative', 'whoever', verbs=['wants'], marker='whoever')
    s.g('Today', 'today', '오늘날에는')
    s.g('whoever', 'whoever V′', 'V′하는 사람은 누구든지')
    s.g('wants|to', 'want to V', '~하기를 원하다', verb_form=v3(s, 'wants', 'want', 'whoever'),
        verb_construction={'kind': 'to-complement', 'verb_span': s.span_of('wants'), 'lemma': 'want',
                           'link_spans': [s.span_of('to')], 'review_record': 'wants to watch: want의 목적어 to V.'})
    s.g('watch', 'watch', '보다')
    s.g('movie', 'movie', '영화')
    f = s.g('can', 'can V', '~할 수 있다', kind='function', combines_with=[])
    ac = s.g('access', 'access', '접속하다, 이용하다', star=W['access'])
    s.g('online', 'online', '온라인의')
    s.g('media', 'media', '미디어')
    s.g('subscription', 'subscription', '구독')
    s.g('platforms', 'platforms', '플랫폼들')
    ej = s.g('enjoy', 'enjoy', '즐기다')
    link(f, ac, ej)
    q = s.g('a vast selection of', 'a vast selection of', '엄청나게 다양한')
    s.g('movies', 'movies', '영화들')
    s.g('on', 'on', '~에서')
    s.g('their', 'their', '그들의', referent_ko='영화를 보고 싶은 사람들')
    s.g('smartphones', 'smartphones', '스마트폰들')
    s.g('or', 'or', '또는', at=s.text.index('or other'))
    s.g('other', 'other', '다른')
    s.g('digital', 'digital', '디지털의')
    s.g('devices', 'devices', '기기들', star=W['devices'])
    s.prot('a vast selection of', 'quantity-kind-of', '수량·종류 표현 a vast selection of가 뒤 명사 movies 앞에서 ‘엄청나게 다양한’으로 같은 어순 대응', gloss=q)
    s.hint('[whoever wants]', '[원하는 사람은 누구든지]', span='whoever wants', label='복합관계대명사 whoever',
           links=[(['whoever'], ['는 사람은 누구든지'])], meaning='(영화를 보기를) 원하는 사람은 누구든지',
           explanation='whoever V′: V′하는 사람은 누구든지. whoever절 전체(whoever wants to watch a movie)가 주절의 주어이며 whoever 자체가 wants의 주어라 별도 S′가 없다. to watch 이하는 표시에서 제외.')
    s.review = ('복합관계대명사 whoever절이 주어(명사절 주어라 S 표시는 전체 유지) + 병렬 동사 can access and enjoy. '
                'a vast selection of는 같은 어순 ~의 수량 표현. whoever는 선행사 없는 복합관계사라 관계사 각주 목록에 넣지 않고 힌트로 연결. 수동 없음.')
    out.append(s)

    # ---------------- s40 ----------------
    s = S('s40', T['s40'], key=True)
    s.ch('At the same time,', '동시에,')
    s.ch('these platforms make it easy for companies to offer', '이 플랫폼들은 기업들이 제공하는 것을 쉽게 만든다')
    s.ch('customized products and services', '맞춤형 제품과 서비스를')
    s.ch('to customers.', '고객들에게.')
    s.natural('동시에 이 플랫폼들은 기업들이 고객에게 맞춤형 제품과 서비스를 쉽게 제공할 수 있게 해 준다.')
    s.cl('main', 'these', subj='these platforms', verbs=['make'])
    s.g('At|same|time', 'at the same time', '동시에')
    s.g('these', 'these', '이')
    s.g('platforms', 'platforms', '플랫폼들')
    s.g('make|it|easy|for|to', 'make it easy for A to V', 'A(이/가) ~하는 것을 쉽게 만들다')
    s.g('companies', 'companies', '기업들')
    s.glosses.sort(key=lambda g: g['spans'][0][0])
    s.g('offer', 'offer', '제공하다', at=s.text.index('offer'))
    s.g('customized', 'customized', '맞춤형의, 주문 제작된', verb_form=pp('past-participle', s, 'customized', 'customize'))
    s.g('products', 'products', '제품들')
    s.g('services', 'services', '서비스들')
    s.g('to', 'to', '~에게', at=s.text.index('to customers'))
    s.g('customers', 'customers', '고객들')
    s.hint('make it easy [for companies to offer]', '[기업들이 제공하는 것을] 쉽게 만든다', span='make it easy for companies to offer',
           label='가목적어 it과 진목적어 to부정사', links=[(['for', 'to'], ['이', '는 것을'])],
           meaning='기업들이 (맞춤형 제품과 서비스를) 제공하는 것을 쉽게 만든다',
           explanation='make it easy for A to V: it은 뒤의 for companies to offer …를 대신하는 가목적어이고, for A는 to V의 의미상 주어(A가). 목적어 customized products 이하는 표시에서 제외.')
    s.review = ('단일 주절 make it easy for A to V(가목적어 it, 진목적어 to offer, 의미상 주어 for companies). '
                'customized는 명사 앞 독립 과거분사. 힌트 1개(가목적어 구문). 관계사·수동 없음.')
    out.append(s)

    # ---------------- s41 ----------------
    s = S('s41', T['s41'])
    s.ch('By applying AI and big data algorithm technology,', '인공지능과 빅데이터 알고리즘 기술을 적용함으로써,')
    s.ch('companies identify consumers’ needs, tastes, and consumption patterns.', '기업들은 소비자들의 요구, 취향, 그리고 소비 패턴을 파악한다.')
    s.natural('인공지능과 빅데이터 알고리즘 기술을 적용해 기업들은 소비자의 요구와 취향, 소비 패턴을 파악한다.')
    s.cl('main', 'By', subj='companies', verbs=['identify'])
    f = s.g('By', 'by V-ing', '~함으로써', kind='function', combines_with=[])
    ap = s.g('applying', 'apply', '적용하다', verb_form=pp('ing', s, 'applying', 'apply'))
    link(f, ap)
    s.g('AI', 'AI', '인공지능')
    s.g('big|data', 'big data', '빅데이터 (아주 많은 양의 정보)')
    s.g('algorithm', 'algorithm', '알고리즘 (문제를 푸는 절차)')
    s.g('technology', 'technology', '기술')
    s.g('companies', 'companies', '기업들')
    s.g('identify', 'identify', '파악하다, 확인하다', star=W['identify'])
    s.g('consumers’', 'consumers’', '소비자들의')
    s.g('needs', 'needs', '요구들, 필요들')
    s.g('tastes', 'tastes', '취향들')
    s.g('consumption', 'consumption', '소비')
    s.g('patterns', 'patterns', '패턴들, 양식들')
    s.hint('[By applying]', '[적용함으로써]', span='By applying', label='전치사 by + 동명사',
           links=[(['By', 'ing'], ['함으로써'])], meaning='(인공지능과 빅데이터 알고리즘 기술을) 적용함으로써',
           explanation='문두 전치사 By + 동명사 applying: ~함으로써(수단). 기업이 소비자를 파악하는 방법. 목적어 AI and … technology는 표시에서 제외.')
    s.review = '문두 by + 동명사(수단) + 주절 identify(목적어 needs, tastes, and consumption patterns 나열). 힌트 1개(by + 동명사). 관계사·수동 없음.'
    out.append(s)

    # ---------------- s42 ----------------
    s = S('s42', T['s42'])
    s.ch('People appreciate having diverse choices and customization,', '사람들은 다양한 선택과 맞춤화를 가지는 것을 높이 평가한다,')
    s.ch('which in turn enhances their satisfaction.', '그리고 그것은 결과적으로 그들의 만족을 높인다.')
    s.natural('사람들은 다양한 선택과 맞춤화를 누리는 것을 좋게 여기며, 이는 결과적으로 그들의 만족도를 높인다.')
    s.cl('main', 'People', subj='People', verbs=['appreciate'])
    s.cl('subject_relative', 'which', verbs=['enhances'], marker='which')
    s.g('People', 'people', '사람들')
    s.g('appreciate', 'appreciate', '높이 평가하다, 좋게 여기다')
    f = s.g('having', 'V-ing', '~하는 것', kind='function', combines_with=[])
    hv = s.g('having', 'have', '가지다, 누리다', same=True, verb_form=pp('ing', s, 'having', 'have'))
    link(f, hv)
    s.g('diverse', 'diverse', '다양한')
    s.g('choices', 'choices', '선택(들)')
    s.g('customization', 'customization', '맞춤화')
    rel = s.g('which', ', which V′', '그리고 그것은 V′하다 (계속적 관계대명사)')
    s.g('in|turn', 'in turn', '결과적으로', star=W['in_turn'])
    s.g('enhances', 'enhance', '높이다, 향상시키다', verb_form=v3(s, 'enhances', 'enhance', 'which(다양한 선택과 맞춤화를 누리는 것)'))
    s.g('their', 'their', '그들의', referent_ko='사람들')
    s.g('satisfaction', 'satisfaction', '만족', star=W['satisfaction'])
    s.hint('customization, [which in turn enhances]', '맞춤화, [그리고 그것은 결과적으로 높인다]', span='customization, which in turn enhances',
           label='계속적 관계대명사 which', links=[(['which'], ['그리고 그것은'])],
           meaning='(다양한 선택과 맞춤화를 가지는 것), 그리고 그것은 결과적으로 (그들의 만족을) 높인다',
           explanation='콤마 뒤 계속적 관계대명사 which가 앞 절의 내용(다양한 선택과 맞춤화를 가지는 것)을 받아 결과를 덧붙인다. 추가 설명 문맥이라 ‘그리고’. 주격이라 V′ enhances까지(사이 부사 in turn 보존) 표시하고 목적어 their satisfaction은 제외.')
    s.relative_ids = [rel['id']]
    s.review = ('주절 appreciate + 동명사 목적어 having … + 계속적 관계대명사 which(앞 내용 전체를 받음, 추가 설명이라 그리고). '
                '필수 관계사 힌트 1개. 수동 없음.')
    out.append(s)

    # ---------------- s43 ----------------
    s = S('s43', T['s43'], key=True)
    s.ch('Services,', '서비스들은,')
    s.ch('such as suggesting personalized clothing styles', '개인 맞춤화된 의류 스타일을 제안하는 것 같은')
    s.ch('based on customers’ purchase history', '고객들의 구매 기록에 기초한')
    s.ch('or recommending videos', '또는 비디오들을 추천하는 것 (같은)')
    s.ch('that match their movie and video viewing history,', '그들의 영화 및 비디오 시청 기록에 맞는,')
    s.ch('bring them great satisfaction.', '그들에게 큰 만족을 가져다준다.')
    s.natural('고객의 구매 기록에 기초해 개인 맞춤 의류 스타일을 제안하거나, 고객의 영화·비디오 시청 기록에 맞는 비디오를 추천하는 것과 같은 서비스는 그들에게 큰 만족을 가져다준다.')
    s.cl('main', 'Services',
         subj='Services, such as suggesting personalized clothing styles based on customers’ purchase history or recommending videos that match their movie and video viewing history',
         verbs=['bring'], disp='Services',
         disp_review='중심명사 Services까지 표시하고 콤마 사이의 예시 such as … viewing history는 제외')
    s.cl('subject_relative', 'that', verbs=['match'], marker='that')
    s.g('Services', 'services', '서비스들')
    s.g('such|as', 'such as', '~ 같은')
    f = s.g('suggesting', 'V-ing', '~하는 것', kind='function', combines_with=[])
    sg = s.g('suggesting', 'suggest', '제안하다', same=True, verb_form=pp('ing', s, 'suggesting', 'suggest'))
    s.g('personalized', 'personalized', '개인 맞춤화된', verb_form=pp('past-participle', s, 'personalized', 'personalize'))
    s.g('clothing', 'clothing', '의류, 옷')
    s.g('styles', 'styles', '스타일들')
    s.g('based|on', 'based on', '(~에) 기초한', verb_form=pp('past-participle', s, 'based', 'base'))
    s.g('customers’', 'customers’', '고객들의')
    s.g('purchase|history', 'purchase history', '구매 기록')
    s.g('or', 'or', '또는')
    rc = s.g('recommending', 'recommend', '추천하다', verb_form=pp('ing', s, 'recommending', 'recommend'))
    link(f, sg, rc)
    s.g('videos', 'videos', '비디오들')
    rel = s.g('that', 'that V′', 'V′하는 (관계대명사)')
    s.g('match', 'match', '~에 맞다, ~와 일치하다')
    s.g('their', 'their', '그들의', referent_ko='고객들')
    s.g('movie', 'movie', '영화')
    s.g('video', 'video', '비디오')
    s.g('viewing|history', 'viewing history', '시청 기록')
    s.g('bring', 'bring A B', 'A에게 B를 가져다주다',
        verb_construction={'kind': 'verb-frame', 'verb_span': s.span_of('bring'), 'lemma': 'bring', 'link_spans': [],
                           'review_record': 'bring them great satisfaction: A=them(고객들), B=great satisfaction.'})
    s.g('them', 'them', '그들에게', referent_ko='고객들')
    s.g('great', 'great', '큰')
    s.g('satisfaction', 'satisfaction', '만족', star=W['satisfaction'])
    s.brk('such', 'postnominal-preposition', 'such as … 이하는 앞 명사 Services의 예를 드는 전치사구')
    s.hint('videos [that match]', '[맞는] 비디오들', span='videos that match', label='주격 관계대명사 that',
           links=[(['that'], ['는'])], meaning='(그들의 영화 및 비디오 시청 기록에) 맞는 비디오들',
           explanation='선행사 videos를 주격 관계대명사 that이 받아 match their movie and video viewing history가 꾸민다. V′ match까지만 표시.')
    s.hint('bring them [great satisfaction]', '그들[고객들]에게 [큰 만족을] 가져다준다', span='bring them great satisfaction',
           label='bring A B 구문', links=[(['bring'], ['에게', '을'])], emphasis_policy='ko-only-verb-construction',
           refs=[('them', '그들', '[고객들]')],
           meaning='그들에게 큰 만족을 가져다준다',
           explanation='bring A B: A에게 B를 가져다주다. A=them(고객들), B=great satisfaction. 주어가 길어 멀리 떨어진 동사 bring과 두 목적어의 연결을 놓치기 쉬워 선정.')
    s.relative_ids = [rel['id']]
    s.review = ('주절 주어 Services(콤마 사이 such as + 동명사 suggesting … or recommending … 예시 삽입) + 동사 bring A B. '
                'based on …은 clothing styles를 꾸미는 과거분사, that match …는 videos를 꾸미는 주격 관계절. 힌트 2개(필수 관계사, bring A B). 수동 없음.')
    out.append(s)
    return out


UNIT = {
    'id': 'u4', 'source_id': 'src', 'paragraph_ids': ['p08', 'p09'],
    'sentence_ids': [f's{n:02d}' for n in range(37, 44)],
    'today_words': [
        {'id': W['development'], 'text': 'development', 'meaning_ko': '발전'},
        {'id': W['devices'], 'text': 'devices', 'meaning_ko': '기기들, 장치들'},
        {'id': W['centered'], 'text': 'centered on', 'meaning_ko': '(~을) 중심으로 한'},
        {'id': W['no_choice'], 'text': 'have no choice but to V', 'meaning_ko': '~할 수밖에 없다'},
        {'id': W['access'], 'text': 'access', 'meaning_ko': '접속하다, 이용하다'},
        {'id': W['identify'], 'text': 'identify', 'meaning_ko': '파악하다, 확인하다'},
        {'id': W['in_turn'], 'text': 'in turn', 'meaning_ko': '결과적으로'},
        {'id': W['satisfaction'], 'text': 'satisfaction', 'meaning_ko': '만족'},
    ],
}


def analysis(_):
    return {
        'heading_kind': '주제',
        'title_or_topic_en': 'How Online Platforms Drive the Subscription Economy',
        'title_or_topic_ko': '온라인 플랫폼이 구독 경제를 이끄는 방식',
        'intent_ko': '디지털 기기와 온라인 플랫폼의 발전 덕분에 소비자는 원하는 서비스를 쉽게 이용하게 되었고, 기업은 인공지능과 빅데이터로 소비자에게 맞춤형 서비스를 제공해 만족을 높인다는 점을 설명하는 글이다.',
        'flow': [
            {'sentence_ids': ['s37', 's38', 's39'], 'label': '소비자의 편리함',
             'text_ko': '스마트폰 등 디지털 기기가 발전하면서 소비자는 많은 일을 쉽게 할 수 있게 되었다. 예전에는 극장에 가거나 비디오를 사야 했지만, 지금은 누구나 구독 플랫폼으로 수많은 영화를 즐긴다.'},
            {'sentence_ids': ['s40', 's41', 's42', 's43'], 'label': '기업의 맞춤 서비스와 만족',
             'text_ko': '플랫폼은 기업이 맞춤형 상품을 제공하기 쉽게 해 준다. 기업은 인공지능과 빅데이터로 소비자의 요구와 취향을 파악하고, 사람들은 다양한 선택과 맞춤화 덕분에 더 만족한다. 구매 기록 기반 의류 추천과 시청 기록 기반 영상 추천이 그 예다.'},
        ],
        'easy_explanations': [
            {'sentence_id': 's38', 'explanatory_sentences': [
                '38번 문장은 37번에서 말한 변화가 얼마나 큰지 보여 주려고 옛날 모습을 꺼낸다.',
                '예전에는 영화를 보려면 극장에 가야 했다.',
                '집에서 보려면 비디오를 직접 사야 했다.',
                '다른 방법이 없었다는 점이 39번의 오늘날 모습과 대비된다.']},
            {'sentence_id': 's40', 'explanatory_sentences': [
                '40번 문장은 앞의 소비자 이야기에서 기업 이야기로 넘어간다.',
                '온라인 플랫폼은 소비자에게만 편리한 것이 아니다.',
                '기업도 플랫폼을 이용하면 고객 한 사람 한 사람에게 맞춘 상품과 서비스를 쉽게 제공할 수 있다.']},
            {'sentence_id': 's42', 'explanatory_sentences': [
                '42번 문장은 41번에서 기업이 소비자를 파악한 결과가 어떻게 이어지는지 말한다.',
                '사람들은 고를 것이 많고 자기에게 맞춰 주는 서비스를 좋아한다.',
                '그렇게 좋아하는 서비스를 받으면 만족도 커진다.',
                'in turn은 한 일이 다음 결과로 이어진다는 것을 보여 주는 말이다.']},
        ],
        'grammar_points': [
            {'id': 'u4-gp1', 'sentence_id': 's38', 'span': 'the videos they wanted to watch',
             'title': '명사 + (that) S′ V′: S′가 V′하는 명사 (목적격 관계대명사 생략)', 'formula_key': 'N + (that) S′ V′',
             'explanation': '공식: 명사(N) + (that) S′ V′ — S′(이/가) V′하는 N. 선행사 = the videos(비디오들), 생략된 관계대명사 = that, '
                            'S′ = they(과거의 사람들), V′ = wanted(원했다; want to V = ~하기를 원하다), to V = to watch(보다). '
                            '→ 그들이 보기를 원했던 비디오들. the videos는 watch의 목적어 자리에서 앞으로 나간 말이다.',
             'practice': {'span': 'the videos they wanted to watch',
                          'formula_support': {'en': 'N + (that) S′ V′', 'ko': 'S′(이/가) V′하는 N'},
                          'support': [('s38', 'videos'), ('s38', 'they'), ('s38', 'want to V'), ('s38', 'watch')],
                          'answer_ko': '그들이 보기를 원했던 비디오들'}},
            {'id': 'u4-gp2', 'sentence_id': 's40', 'span': 'make it easy for companies to offer customized products and services',
             'title': 'make it easy for A to V: A가 ~하는 것을 쉽게 만들다 (가목적어 it)', 'formula_key': 'make it easy for A to V',
             'explanation': '공식: make it easy for A to V — A(이/가) ~하는 것을 쉽게 만들다. it = 뒤의 to V를 대신하는 가목적어, '
                            'A = companies(기업들), to V = to offer(제공하다), offer의 목적어 = customized products and services(맞춤형 제품과 서비스). '
                            '→ 기업들이 맞춤형 제품과 서비스를 제공하는 것을 쉽게 만들다.',
             'practice': {'span': 'make it easy for companies to offer customized products and services',
                          'formula_support': {'en': 'make it easy for A to V', 'ko': 'A(이/가) ~하는 것을 쉽게 만들다'},
                          'support': [('s40', 'companies'), ('s40', 'offer'), ('s40', 'customized'), ('s40', 'products'), ('s40', 'services')],
                          'answer_ko': '기업들이 맞춤형 제품과 서비스를 제공하는 것을 쉽게 만들다'}},
            {'id': 'u4-gp3', 'sentence_id': 's42', 'span': 'customization, which in turn enhances their satisfaction',
             'title': ', which V′: 그리고 그것은 V′하다 (계속적 관계대명사)', 'formula_key': ', which V′',
             'explanation': '공식: , which V′ — 그리고 그것은 V′하다. which = 앞 절 내용(다양한 선택과 맞춤화를 가지는 것), '
                            'in turn = 결과적으로, V′ = enhances(높이다), 목적어 = their satisfaction(그들의 만족). '
                            '→ 그리고 그것은 결과적으로 그들의 만족을 높인다. 콤마 뒤 which는 앞말을 받아 설명을 이어 간다.',
             'practice': {'span': 'which in turn enhances their satisfaction',
                          'formula_support': {'en': ', which V′', 'ko': '그리고 그것은 V′하다'},
                          'support': [('s42', 'in turn'), ('s42', 'enhance'), ('s42', 'their'), ('s42', 'satisfaction')],
                          'answer_ko': '그리고 그것은 결과적으로 그들의 만족을 높인다'}},
            {'id': 'u4-gp4', 'sentence_id': 's37', 'span': 'consumers have been able to do numerous things',
             'title': 'have p.p.: ~해 왔다 (have been able to V: ~할 수 있게 되었다)', 'formula_key': 'have p.p.',
             'explanation': '공식: have p.p. — ~해 왔다. p.p. = been(be의 p.p.형), be able to V = ~할 수 있다, V = do(하다), 목적어 = numerous things(수많은 일들). '
                            '→ 수많은 일들을 할 수 있어 왔다, 곧 할 수 있게 되었다. 기기가 발전한 뒤로 지금까지 계속 그렇다는 뜻이다.',
             'supplemental': {'function': ('s37', 'have p.p.', 0),
                              'reason': 's37의 능동 완료 have been (able to)은 과거분사 후치수식 힌트를 선정해 결합 힌트로 두지 않았고, 기본 분석 3개에 have p.p. 설명이 없어 이 단위 대표 사례로 1회 보충'},
             'practice': {'span': 'have been able to do numerous things',
                          'formula_support': {'en': 'have p.p.', 'ko': '~해 왔다'},
                          'support': [('s37', 'be able to V'), ('s37', 'do'), ('s37', 'numerous'), ('s37', 'things')],
                          'answer_ko': '수많은 일들을 할 수 있게 되었다'}},
        ],
        'formula_routes': [
            {'function': ('s37', 'have p.p.', 0), 'route': 'analysis', 'grammar_point_id': 'u4-gp4',
             'review_record': 'have been (able to): 과거분사 후치수식 힌트가 있어 분석 보충 u4-gp4로 연결'},
        ],
        'relations': [
            {'head': {'id': 'u4-r1h', 'text': 'numerous', 'meaning_ko': '수많은'},
             'synonym': {'id': 'u4-r1s', 'text': 'countless', 'meaning_ko': '셀 수 없이 많은'},
             'antonym': {'id': 'u4-r1a', 'text': 'few', 'meaning_ko': '거의 없는, 소수의'}},
            {'head': {'id': 'u4-r2h', 'text': 'vast', 'meaning_ko': '방대한, 엄청난'},
             'synonym': {'id': 'u4-r2s', 'text': 'enormous', 'meaning_ko': '거대한, 막대한'},
             'antonym': {'id': 'u4-r2a', 'text': 'tiny', 'meaning_ko': '아주 작은'}},
            {'head': {'id': 'u4-r3h', 'text': 'customized', 'meaning_ko': '맞춤형의'},
             'synonym': {'id': 'u4-r3s', 'text': 'tailored', 'meaning_ko': '맞춤의, 딱 맞춘'},
             'antonym': {'id': 'u4-r3a', 'text': 'standardized', 'meaning_ko': '표준화된, 규격화된'}},
        ],
    }


def workbook():
    return {
        'relation_order': ['u4-r2s', 'u4-r1a', 'u4-r3h', 'u4-r2a', 'u4-r1h', 'u4-r3s', 'u4-r2h', 'u4-r3a', 'u4-r1s'],
        'key_sentence_ids': ['s40', 's43'],
        'question_id': 'Q04',
        'syntax_point_ids': ['u4-gp1', 'u4-gp2', 'u4-gp3', 'u4-gp4'],
    }
