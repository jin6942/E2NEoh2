"""FR 공통 단위 1: s01~s09 (p01~p03) — 기아석(Hunger Stones)과 가뭄 경고.

사용자 결정(2026-09-28 “1단위 (추천)”): 소제목 없는 짧은 단락 3개(2·5·2문장)를 9문장 1단위로 묶는다.
"""
from author import S, link

W = {'retreat': 'u1-w1', 'visible': 'u1-w2', 'significant': 'u1-w3', 'bear': 'u1-w4',
     'hardship': 'u1-w5', 'urge': 'u1-w6', 'occasional': 'u1-w7', 'persist': 'u1-w8'}


def pp(usage, s, word, lemma, fid=None, occ_after=0, review=None):
    row = {'usage': usage, 'source_span': s.span_of(word, occ_after), 'lemma': lemma}
    if fid:
        row['function_gloss_id'] = fid
    if review:
        row['review_record'] = review
    return row


def sentences(T):
    out = []

    # ---------------- s01 ----------------
    s = S('s01', T['s01'])
    s.ch('In the summer', '여름에')
    s.ch('of 2022,', '2022년의,')
    s.ch('during the worst drought', '최악의 가뭄 동안')
    s.ch('in 500 years', '500년 만에')
    s.ch('in Europe,', '유럽의,')
    s.ch('a stone', '한 돌이')
    s.ch('known as a “hunger stone”', '‘기아석’으로 알려진')
    s.ch('was found', '발견되었다')
    s.ch('in a Czech town', '체코의 한 마을에서')
    s.ch('along the Elbe River.', '엘베강을 따라 있는.')
    s.natural('유럽에 500년 만에 최악의 가뭄이 닥친 2022년 여름, 엘베강을 따라 있는 체코의 한 마을에서 ‘기아석’으로 알려진 돌이 발견되었다.')
    s.cl('main', 'a', subj='a stone known as a “hunger stone”', verbs=['was', 'found'], disp='a stone',
         disp_review='중심명사 stone까지 표시하고 뒤에서 꾸미는 과거분사구 known as a “hunger stone”은 제외')
    s.g('In', 'in', '~에')
    s.g('summer', 'summer', '여름')
    s.g('of', 'of', '~의')
    s.g('during', 'during', '~ 동안')
    s.g('worst', 'worst', '최악의 (bad의 최상급)')
    s.g('drought', 'drought', '가뭄')
    s.g('in|500|years', 'in 500 years', '500년 만에', at=s.text.index('in 500'))
    s.g('in', 'in', '~의', at=s.text.index('in Europe'))
    s.g('Europe', 'Europe', 'Europe (유럽)', proper=True)
    s.g('stone', 'stone', '돌')
    kn = s.g('known', 'known', '알려진', verb_form=pp('past-participle', s, 'known', 'know'))
    s.g('as', 'as', '~으로')
    s.g('hunger|stone', 'hunger stone', '기아석 (가뭄 때 드러나 굶주림을 경고하는 돌)')
    f = s.g('was', 'be p.p.', '~되다', kind='function', combines_with=[])
    fd = s.g('found', 'found', '발견된', verb_form=pp('passive-participle', s, 'found', 'find', f['id']))
    link(f, fd)
    s.g('in', 'in', '~에서', at=s.text.index('in a Czech'))
    s.g('Czech', 'Czech', 'Czech (체코의)', proper=True)
    s.g('town', 'town', '마을, 소도시')
    s.g('along', 'along', '~을 따라 있는')
    s.g('Elbe|River', 'Elbe River', 'Elbe River (엘베강, 체코와 독일을 흐르는 강)', proper=True)
    s.brk('of', 'postnominal-preposition', 'of 2022는 앞 명사 the summer를 뒤에서 꾸미는 전치사구')
    s.brk('in', 'postnominal-preposition', 'in 500 years는 앞 명사 the worst drought를 뒤에서 꾸미는 전치사구', after=s.text.index('in 500'))
    s.brk('in', 'postnominal-preposition', 'in Europe은 앞 명사 the worst drought를 뒤에서 꾸미는 전치사구', after=s.text.index('in Europe'))
    s.brk('known', 'postpositive-adjective', 'known as a “hunger stone”은 앞 명사 a stone을 뒤에서 꾸미는 과거분사구')
    s.brk('along', 'postnominal-preposition', 'along the Elbe River는 앞 명사 a Czech town을 뒤에서 꾸미는 전치사구')
    s.hint('a stone [known as a “hunger stone”]', '[‘기아석’으로 알려진] 돌', span='a stone known as a “hunger stone”',
           label='과거분사 후치수식', links=[(['known'], ['알려진'])], participle_focus_gloss_id=kn['id'],
           meaning='‘기아석’으로 알려진 돌',
           explanation='과거분사구 known as a “hunger stone”이 앞 명사 a stone을 뒤에서 꾸민다. 돌이 ‘기아석’이라고 알려진(불리는) 쪽이라 과거분사. 독립 p.p. known ↔ 알려진 전체 대응.')
    s.review = ('문두 시간 부사구 In the summer of 2022(of 후치수식) + during the worst drought in 500 years in Europe(전치사구 후치수식 두 개) '
                '+ 주절 a stone known as a “hunger stone”(과거분사 후치수식) was found(과거 수동) in a Czech town along the Elbe River(along 후치수식). '
                '힌트 1개(과거분사 후치수식). 수동 was found는 분석 보충 u1-gp4로 연결. 관계사 없음.')
    out.append(s)

    # ---------------- s02 ----------------
    s = S('s02', T['s02'])
    s.ch('The stone had a sentence', '그 돌은 한 문장을 가지고 있었다')
    s.ch('written on it', '그것 위에 쓰인')
    s.ch('that read:', '다음과 같이 적혀 있던:')
    s.ch('“If you see me,', '“만약 네가 나를 본다면,')
    s.ch('then cry.”', '그러면 울어라.”')
    s.natural('그 돌에는 “나를 보면 울어라.”라는 문장이 새겨져 있었다.')
    s.cl('main', 'The', subj='The stone', verbs=['had'])
    s.cl('subject_relative', 'that', verbs=['read'], marker='that')
    s.cl('subordinate', 'If', subj='you', verbs=['see'], marker='If')
    s.cl('imperative', 'cry', verbs=['cry'])
    s.g('stone', 'stone', '돌')
    s.g('had', 'had', '가지고 있었다 (have의 과거)', verb_form=pp('irregular-past', s, 'had', 'have'))
    s.g('sentence', 'sentence', '문장')
    wr = s.g('written', 'written', '쓰인, 새겨진', verb_form=pp('past-participle', s, 'written', 'write'))
    s.g('on', 'on', '~ 위에')
    s.g('it', 'it', '그것', referent_ko='그 돌')
    rel = s.g('that', 'that V′', 'V′하던 (관계대명사)')
    s.g('read', 'read', '(~라고) 적혀 있었다 (흔한 뜻: 읽었다)', verb_form=pp('irregular-past', s, 'read', 'read'))
    s.g('If', 'if S′ V′', 'S′(이/가) V′한다면')
    s.g('see', 'see', '보다')
    s.g('me', 'me', '나를', referent_ko='기아석')
    s.g('then', 'then', '그러면')
    s.g('cry', 'cry', '울다')
    s.brk('written', 'postpositive-adjective', 'written on it은 앞 명사 a sentence를 뒤에서 꾸미는 과거분사구')
    s.hint('a sentence written on it [that read]', '그것[그 돌] 위에 쓰인, [적혀 있던] 문장',
           span='a sentence written on it that read', label='주격 관계대명사 that',
           links=[(['that'], ['던'])], refs=[(('it', 1), '그것', '[그 돌]')],
           meaning='그 돌 위에 쓰인, 적혀 있던 문장',
           explanation='선행사 a sentence를 주격 관계대명사 that이 받는다(과거분사구 written on it 뒤에 이어짐). 주격이라 별도 S′ 없이 V′ read(적혀 있었다)까지 표시하고 콜론 뒤 인용과 그 뜻(다음과 같이)은 제외.')
    s.hint('[If you see]', '[네[이 글을 읽는 사람]가 본다면]', span='If you see', label='조건 접속사 if',
           links=[(['If'], ['가', '본다면'])], refs=[('you', '네', '[이 글을 읽는 사람]')],
           meaning='네가 (나를) 본다면',
           explanation='인용문 안 조건절 if S′ V′: S′가 V′한다면. S′ you, V′ see까지 표시하고 목적어 me는 제외. then cry는 명령문 주절. '
                       'you는 돌에 새겨진 글을 보고 읽는 사람을 가리킨다(돌이 me로 자신을 말하며 그 글을 읽는 사람에게 말을 거는 문장).')
    s.relative_ids = [rel['id']]
    s.review = ('주절 The stone had a sentence + 과거분사 후치수식 written on it + 주격 관계대명사 that절(read: ~라고 적혀 있었다) + 콜론 뒤 인용 “If you see me, then cry.”(조건절 + 명령문 주절). '
                '힌트 2개(필수 관계사 that, 인용 속 조건절 if). written on it은 관계사 힌트 표시 안에 함께 보임. 수동 없음.')
    out.append(s)

    # ---------------- s03 ----------------
    s = S('s03', T['s03'])
    s.ch('The hunger stones,', '기아석들은,')
    s.ch('found in rivers', '강들에서 발견되는')
    s.ch('across central Europe,', '중부 유럽 전역의,')
    s.ch('typically remain underwater.', '보통 물속에 남아 있다.')
    s.natural('중부 유럽 곳곳의 강에서 발견되는 기아석들은 보통 물속에 잠겨 있다.')
    s.cl('main', 'The', subj='The hunger stones', verbs=['remain'])
    s.g('hunger|stones', 'hunger stones', '기아석들')
    fo = s.g('found', 'found', '발견되는', verb_form=pp('past-participle', s, 'found', 'find'))
    s.g('in', 'in', '~에서')
    s.g('rivers', 'rivers', '강들')
    s.g('across', 'across', '~ 전역의')
    s.g('central', 'central', '중부의')
    s.g('typically', 'typically', '보통, 일반적으로')
    s.g('remain', 'remain', '(~한 상태로) 남아 있다')
    s.g('underwater', 'underwater', '물속에')
    s.brk('found', 'postpositive-adjective', '콤마 사이 과거분사구 found in rivers …가 앞 명사 The hunger stones를 뒤에서 설명')
    s.brk('across', 'postnominal-preposition', 'across central Europe은 앞 명사 rivers를 뒤에서 꾸미는 전치사구')
    s.hint('The hunger stones, [found in rivers]', '[강들에서 발견되는] 기아석들', span='The hunger stones, found in rivers',
           label='과거분사 후치수식', links=[(['found'], ['발견되는'])], participle_focus_gloss_id=fo['id'],
           meaning='강들에서 발견되는 기아석들',
           explanation='콤마 사이의 과거분사구 found in rivers …가 주어 The hunger stones를 뒤에서 설명한다. 돌이 ‘발견되는’ 쪽이라 과거분사. 독립 p.p. found ↔ 발견되는 전체 대응. across central Europe은 제외.')
    s.review = ('주어 The hunger stones + 콤마 사이 과거분사구 found in rivers across central Europe + 동사 remain + 보어 역할 부사 underwater. '
                'Europe은 s01에서 제공한 고유명사 반복. 힌트 1개(과거분사 후치수식). 관계사·수동 없음.')
    out.append(s)

    # ---------------- s04 ----------------
    s = S('s04', T['s04'])
    s.ch('However,', '하지만,')
    # 2026-09-29 사용자 결정 “A 괄호 방식”(L 재검 LR-01): 본책 s73·s74와 같이 병렬 뒤 칸에 생략된 뜻을 괄호로 보충.
    s.ch('when droughts occur', '가뭄이 발생할 때')
    s.ch('and water levels retreat,', '그리고 수위가 낮아질 (때),')
    s.ch('these stones become visible.', '이 돌들은 눈에 보이게 된다.')
    s.natural('하지만 가뭄이 들어 수위가 낮아지면 이 돌들이 모습을 드러낸다.')
    s.cl('subordinate', 'when', subj='droughts', verbs=['occur'], marker='when')
    s.cl('subordinate', 'water', subj='water levels', verbs=['retreat'], marker='and')
    s.cl('main', 'these', subj='these stones', verbs=['become'])
    s.g('However', 'however', '하지만, 그러나')
    s.g('when', 'when S′ V′', 'S′(이/가) V′할 때')
    s.g('droughts', 'droughts', '가뭄들')
    s.g('occur', 'occur', '발생하다, 일어나다')
    s.g('water|levels', 'water levels', '수위')
    s.g('retreat', 'retreat', '(물이) 빠지다, 낮아지다 (흔한 뜻: 후퇴하다)', star=W['retreat'])
    s.g('these', 'these', '이')
    s.g('stones', 'stones', '돌들')
    s.g('become', 'become', '~하게 되다')
    s.g('visible', 'visible', '(눈에) 보이는', star=W['visible'])
    s.hint('[when droughts occur and water levels retreat]', '[가뭄이 발생하고 수위가 낮아질 때]',
           span='when droughts occur and water levels retreat', label='시간 접속사 when',
           links=[(['when'], ['이', ('가', 1), '질 때'])],
           meaning='가뭄이 발생하고 수위가 낮아질 때',
           explanation='when S′ V′: S′가 V′할 때. 두 절(droughts occur / water levels retreat)이 and로 이어져 모두 when에 걸린다. 각 S′·V′까지 표시.')
    s.review = ('문두 연결어 However + when절 두 개가 and로 병렬(droughts occur / water levels retreat, 뒤 절은 [and] S′·V′로 표시) + 주절 these stones become visible. '
                '힌트 1개(when절). 관계사·수동 없음.')
    out.append(s)

    # ---------------- s05 ----------------
    s = S('s05', T['s05'])
    s.ch('The stones are significant', '그 돌들은 중요하다')
    s.ch('because they bear records', '그것들이 기록들을 지니고 있기 때문에')
    s.ch('of the past severe droughts.', '과거의 극심한 가뭄들의.')
    s.natural('이 돌들이 중요한 이유는 과거에 있었던 극심한 가뭄의 기록을 담고 있기 때문이다.')
    s.cl('main', 'The', subj='The stones', verbs=['are'])
    s.cl('subordinate', 'because', subj='they', verbs=['bear'], marker='because')
    s.g('stones', 'stones', '돌들')
    s.g('are', 'are', '~이다')
    s.g('significant', 'significant', '중요한, 의미 있는', star=W['significant'])
    s.g('because', 'because S′ V′', 'S′(이/가) V′하기 때문에')
    s.g('they', 'they', '그것들이', referent_ko='기아석들')
    s.g('bear', 'bear', '(기록 등을) 지니다, 담고 있다 (흔한 뜻: 곰)', star=W['bear'])
    s.g('records', 'records', '기록들')
    s.g('of', 'of', '~의')
    s.g('past', 'past', '과거의')
    s.g('severe', 'severe', '극심한, 심각한')
    s.g('droughts', 'droughts', '가뭄들')
    s.brk('of', 'postnominal-preposition', 'of the past severe droughts는 앞 명사 records를 뒤에서 꾸미는 전치사구')
    s.hint('[because they bear]', '[그것들[기아석들]이 지니고 있기 때문에]', span='because they bear', label='이유 접속사 because',
           links=[(['because'], ['이', '기 때문에'])], refs=[('they', '그것들', '[기아석들]')],
           meaning='그것들이 (기록을) 지니고 있기 때문에',
           explanation='because S′ V′: S′가 V′하기 때문에. S′ they(기아석들), V′ bear까지 표시하고 목적어 records 이하는 제외.')
    s.review = '주절 The stones are significant + 이유 부사절 because they bear records of the past severe droughts(of 후치수식). 힌트 1개(because절). 관계사·수동 없음.'
    out.append(s)

    # ---------------- s06 ----------------
    s = S('s06', T['s06'])
    s.ch('Droughts cause reduced harvests,', '가뭄은 줄어든 수확량을 초래한다,')
    s.ch('food shortages, and hunger,', '식량 부족, 그리고 굶주림을,')
    s.ch('especially for the poor.', '특히 가난한 사람들에게.')
    s.natural('가뭄은 수확량 감소와 식량 부족을 불러오고, 특히 가난한 사람들에게는 굶주림을 가져온다.')
    s.cl('main', 'Droughts', subj='Droughts', verbs=['cause'])
    s.g('Droughts', 'droughts', '가뭄들')
    s.g('cause', 'cause', '초래하다, 일으키다')
    s.g('reduced', 'reduced', '줄어든', verb_form=pp('past-participle', s, 'reduced', 'reduce'))
    s.g('harvests', 'harvests', '수확량')
    s.g('food|shortages', 'food shortages', '식량 부족')
    s.g('hunger', 'hunger', '굶주림, 기아')
    s.g('especially', 'especially', '특히')
    s.g('for', 'for', '~에게')
    s.g('the|poor', 'the poor', '가난한 사람들')
    s.review = ('단일 주절 Droughts cause + 목적어 셋(reduced harvests, food shortages, hunger)의 나열 + especially for the poor. '
                'reduced는 명사 앞 독립 p.p.(각주 지원). the poor = 가난한 사람들(각주). 관계사·접속사절·수동 없음 → 힌트 없음(단순 나열은 억지 힌트 대상 아님).')
    out.append(s)

    # ---------------- s07 ----------------
    s = S('s07', T['s07'], key=True)
    s.ch('The words', '그 글귀들은')
    s.ch('on the hunger stones', '기아석들 위의')
    # 2026-09-29 사용자 결정 “A 괄호 방식”(L 재검 LR-01)
    s.ch('are believed to warn of these hardships', '이러한 어려움들에 대해 경고하는 것으로 여겨진다')
    s.ch('and to urge people to be prepared.', '그리고 사람들에게 대비하라고 촉구하는 것으로 (여겨진다).')
    s.natural('기아석에 새겨진 글귀는 이러한 어려움을 경고하고, 사람들에게 대비하라고 촉구하는 것으로 여겨진다.')
    s.cl('main', 'The', subj='The words on the hunger stones', verbs=['are', 'believed'], disp='The words',
         disp_review='중심명사 words까지 표시하고 뒤에서 꾸미는 전치사구 on the hunger stones는 제외')
    s.g('words', 'words', '글귀들, 말들')
    s.g('on', 'on', '~ 위의')
    s.g('hunger|stones', 'hunger stones', '기아석들')
    f = s.g('are', 'be p.p.', '~되다', kind='function', combines_with=[])
    # 2026-09-29 사용자 결정 “p.p.에 to V 결합”(L-05): 수동 분리(be p.p.)는 유지하고 보충 to V 두 개를 believed 쪽 각주에 묶는다.
    bl = s.g('believed|to|to', 'believed to V', '~하는 것으로 여겨지는',
             verb_form=pp('passive-participle', s, 'believed', 'believe', f['id']),
             verb_construction={'kind': 'to-complement', 'verb_span': s.span_of('believed'), 'lemma': 'believe',
                                'link_spans': [s.span_of('to'), s.span_of('to', s.text.index('to urge'))],
                                'review_record': 'are believed to warn … and to urge …: 수동 are believed 뒤 병렬 보충 to V 두 개(to warn, to urge).'})
    link(f, bl)
    s.g('warn|of', 'warn of', '~에 대해 경고하다')
    s.g('these', 'these', '이러한')
    s.g('hardships', 'hardships', '어려움들, 고난들', star=W['hardship'])
    s.g('urge|to', 'urge A to V', 'A에게 V하라고 촉구하다', star=W['urge'],
             verb_construction={'kind': 'verb-frame', 'verb_span': s.span_of('urge'), 'lemma': 'urge',
                                'link_spans': [s.span_of('to', s.text.index('to be'))],
                                'review_record': 'urge people to be prepared: A = people, V = be prepared.'})
    s.g('people', 'people', '사람들')
    s.g('be|prepared', 'be prepared', '대비하다, 준비가 되어 있다')
    s.brk('on', 'postnominal-preposition', 'on the hunger stones는 앞 명사 The words를 뒤에서 꾸미는 전치사구')
    s.hint('[are believed to warn]', '[경고하는 것으로 여겨진다]', span='are believed to warn', label='be believed to V 구문',
           emphasis_policy='ko-only-verb-construction', links=[(['to'], ['는 것으로'])],
           meaning='(이러한 어려움에 대해) 경고하는 것으로 여겨진다',
           explanation='be believed to V: ~하는 것으로 여겨지다(믿어지다). are believed 뒤 to warn과, and 뒤 to urge가 모두 are believed에 이어진다. 동사 결합이라 한국어 연결 어미 ‘는 것으로’만 강조.')
    s.hint('urge people [to be prepared]', '사람들에게 [대비하라고] 촉구하다', span='urge people to be prepared', label='urge A to V 구문',
           emphasis_policy='ko-only-verb-construction', links=[(['to'], ['에게', '라고'])],
           meaning='사람들에게 대비하라고 촉구하다',
           explanation='urge A to V: A에게 V하라고 촉구하다. A = people, V = be prepared(대비하다). A 조사 에게와 연결 어미 라고만 강조.')
    s.review = ('주어 The words on the hunger stones(on 후치수식) + are believed(현재 수동) + 병렬 to부정사 to warn of these hardships and to urge people to be prepared(be believed to V). '
                'urge A to V. 각주는 사용자 결정(2026-09-29 “p.p.에 to V 결합”)대로 be p.p. — ~되다 / believed to V — ~하는 것으로 여겨지는(병렬 to 두 개 연결). 힌트 2개(be believed to V, urge A to V). 수동 are believed는 두 힌트가 있어 분석 보충 u1-gp4(be p.p.)로 연결하고, be believed to V 자체는 u1-gp2에서 분석. 관계사 없음.')
    out.append(s)

    # ---------------- s08 ----------------
    s = S('s08', T['s08'], key=True)
    s.ch('Considering the continuation', '지속을 고려할 때')
    s.ch('of climate change,', '기후 변화의,')
    s.ch('experts warn', '전문가들은 경고한다')
    s.ch('that the situation', '상황이')
    s.ch('we face', '우리가 직면한')
    s.ch('is not just a simple, occasional drought', '단지 단순하고 가끔 일어나는 가뭄이 아니라')
    s.ch('but a severe drought', '심각한 가뭄이라고')
    s.ch('that could persist', '지속될 수 있는')
    s.ch('for decades.', '수십 년 동안.')
    s.natural('기후 변화가 계속되는 것을 고려할 때, 전문가들은 우리가 직면한 상황이 단순하고 가끔 찾아오는 가뭄이 아니라 수십 년 동안 이어질 수 있는 심각한 가뭄이라고 경고한다.')
    s.cl('main', 'experts', subj='experts', verbs=['warn'])
    s.cl('subordinate', 'that', subj='the situation we face', verbs=['is'], marker='that', disp='the situation',
         disp_review='중심명사 situation까지 표시하고 뒤에서 꾸미는 생략 관계절 (that) we face는 제외')
    s.cl('subordinate', 'we', subj='we', verbs=['face'], marker='that', omitted=True)
    th = s.at('that could')
    s.cl_spans('subject_relative', th[0], verbs=[s.at('could', after=th[0]), s.at('persist', after=th[0])], marker='that')
    s.g('Considering', 'considering', '~을 고려할 때')
    s.g('continuation', 'continuation', '지속, 계속')
    s.g('of', 'of', '~의')
    s.g('climate|change', 'climate change', '기후 변화')
    s.g('experts', 'experts', '전문가들')
    s.g('warn', 'warn', '경고하다')
    s.g('that', 'that S′ V′', 'S′(이/가) V′라고 (접속사)')
    s.g('situation', 'situation', '상황')
    s.g('we', 'we', '우리가', referent_ko='사람들, 인류')
    s.g('face', 'face', '직면하다 (흔한 뜻: 얼굴)')
    s.g('is', 'is', '~이다')
    s.g('not|just|but', 'not just A but B', '단지 A가 아니라 B')
    s.g('simple', 'simple', '단순한')
    s.g('occasional', 'occasional', '가끔 일어나는, 이따금의', star=W['occasional'])
    s.g('drought', 'drought', '가뭄', at=s.text.index('drought but'))
    s.g('severe', 'severe', '심각한, 극심한')
    s.g('drought', 'drought', '가뭄', at=s.text.index('drought that'))
    rel = s.g('that', 'that V′', 'V′하는 (관계대명사)', at=th[0])
    fc = s.g('could', 'could V', '~할 수 있을 것이다', kind='function', combines_with=[])
    ps = s.g('persist', 'persist', '지속되다, 계속되다', star=W['persist'])
    link(fc, ps)
    s.g('for', 'for', '~ 동안')
    s.g('decades', 'decades', '수십 년')
    s.brk('of', 'postnominal-preposition', 'of climate change는 앞 명사 the continuation을 뒤에서 꾸미는 전치사구')
    s.hint('the situation [(that) we face]', '[우리[사람들]가 직면한] 상황', span='the situation we face',
           label='목적격 관계대명사 that 생략', display_mode='omitted-relative', omitted_relative='that',
           links=[(['that'], ['가', '한'])], refs=[('we', '우리', '[사람들]')],
           meaning='우리가 직면한 상황',
           explanation='선행사 the situation 뒤에 목적격 관계대명사 that이 생략되었다(face의 목적어). 표시에서만 (that)을 보충. S′ we, V′ face.')
    s.hint('a severe drought [that could persist]', '[지속될 수 있는] 심각한 가뭄', span='a severe drought that could persist',
           label='주격 관계대명사 that', links=[(['that'], ['는'])],
           meaning='(수십 년 동안) 지속될 수 있는 심각한 가뭄',
           explanation='선행사 a severe drought를 주격 관계대명사 that이 받는다. 주격이라 별도 S′ 없이 V′ could persist까지 표시하고 for decades는 제외.')
    s.relative_ids = [rel['id']]
    s.review = ('문두 전치사 Considering the continuation of climate change(of 후치수식) + 주절 experts warn + 목적어 that 명사절(S′ the situation (that) we face, V′ is) '
                '+ not just A but B(A = a simple, occasional drought, B = a severe drought) + B를 꾸미는 주격 관계대명사 that절(could persist for decades). '
                '필수 관계사 힌트 2개(생략 목적격 that, 주격 that). that 명사절과 not just A but B는 문장당 2개 한도로 각주·S/V와 분석 u1-gp3으로 지원. 수동 없음.')
    out.append(s)

    # ---------------- s09 ----------------
    s = S('s09', T['s09'])
    s.ch('The United Nations has predicted', '유엔은 예측했다')
    s.ch('that by 2050,', '2050년까지')
    s.ch('75 percent', '75퍼센트가')
    s.ch('of the global population', '전 세계 인구의')
    s.ch('could suffer from the effects', '영향으로 고통받을 수 있다고')
    s.ch('of drought', '가뭄의')
    s.ch('unless significant action is taken', '중대한 조치가 취해지지 않는다면')
    s.ch('to address climate change.', '기후 변화에 대처하기 위해.')
    s.natural('유엔은 기후 변화에 대처하기 위한 중대한 조치가 취해지지 않으면 2050년까지 전 세계 인구의 75퍼센트가 가뭄의 영향으로 고통받을 수 있다고 예측했다.')
    s.cl('main', 'The', subj='The United Nations', verbs=['has', 'predicted'])
    s.cl('subordinate', 'that', subj='75 percent of the global population', verbs=['could', 'suffer'], marker='that')
    s.cl('subordinate', 'unless', subj='significant action', verbs=['is', 'taken'], marker='unless')
    s.g('United|Nations', 'United Nations', 'United Nations (유엔, 국제 연합)', proper=True)
    f = s.g('has', 'have p.p.', '~했다', kind='function', combines_with=[])
    pr = s.g('predicted', 'predict', '예측하다 (predicted는 predict의 p.p.형)',
             verb_form=pp('perfect-participle', s, 'predicted', 'predict', f['id']))
    link(f, pr)
    s.g('that', 'that S′ V′', 'S′(이/가) V′라고 (접속사)')
    s.g('by', 'by', '~까지')
    s.g('percent', 'percent', '퍼센트')
    s.g('of', 'of', '~의')
    s.g('global', 'global', '전 세계의')
    s.g('population', 'population', '인구')
    fc = s.g('could', 'could V', '~할 수 있을 것이다', kind='function', combines_with=[])
    sf = s.g('suffer|from', 'suffer from', '~으로 고통받다')
    link(fc, sf)
    s.g('effects', 'effects', '영향들')
    s.g('of', 'of', '~의', at=s.text.index('of drought'))
    s.g('drought', 'drought', '가뭄')
    s.g('unless', 'unless S′ V′', 'S′(이/가) V′하지 않는다면')
    s.g('significant', 'significant', '중대한, 상당한')
    s.g('action', 'action', '조치, 행동')
    fp = s.g('is', 'be p.p.', '~되다', kind='function', combines_with=[])
    tk = s.g('taken', 'taken', '취해진', verb_form=pp('passive-participle', s, 'taken', 'take', fp['id']))
    link(fp, tk)
    ft = s.g('to', 'to V', '~하기 위해', kind='function', combines_with=[])
    ad = s.g('address', 'address', '(문제를) 다루다, 대처하다 (흔한 뜻: 주소)')
    link(ft, ad)
    s.g('climate|change', 'climate change', '기후 변화')
    s.brk('of', 'postnominal-preposition', 'of the global population은 앞 명사 75 percent를 뒤에서 꾸미는 전치사구')
    s.brk('of', 'postnominal-preposition', 'of drought는 앞 명사 the effects를 뒤에서 꾸미는 전치사구', after=s.text.index('of drought'))
    s.hint('[that by 2050, 75 percent of the global population could suffer]', '[2050년까지 전 세계 인구의 75퍼센트가 고통받을 수 있다고]',
           span='that by 2050, 75 percent of the global population could suffer', label='명사절 접속사 that',
           links=[(['that'], ['가', '다고'])],
           meaning='2050년까지 전 세계 인구의 75퍼센트가 (가뭄의 영향으로) 고통받을 수 있다고',
           explanation='predicted의 목적어인 that 명사절. that 뒤 시간 부사구 by 2050이 먼저 오고, S′ 75 percent of the global population(수량 표현이라 전체 유지), V′ could suffer까지 표시. from the effects 이하는 제외.')
    s.hint('[unless significant action is taken]', '[중대한 조치가 취해지지 않는다면]', span='unless significant action is taken',
           label='조건 접속사 unless', links=[(['unless'], ['가', '지 않는다면'])],
           meaning='중대한 조치가 취해지지 않는다면',
           explanation='unless S′ V′ = if S′ not V′(~하지 않는다면). S′ significant action, V′ is taken(수동)까지 표시하고 목적의 to address 이하는 제외.')
    s.review = ('주절 The United Nations has predicted(현재완료) + 목적어 that 명사절(by 2050, S′ 75 percent of the global population, V′ could suffer from the effects of drought) '
                '+ 조건 부사절 unless significant action is taken(현재 수동) + 목적의 to address climate change. '
                'United Nations는 복수형이지만 단일 기관이라 has. 힌트 2개(that 명사절, unless절). 능동 완료 has predicted는 분석 보충 u1-gp5, 수동 is taken은 u1-gp4로 연결. 관계사 없음.')
    out.append(s)
    return out


UNIT = {
    'id': 'u1', 'source_id': 'src', 'paragraph_ids': ['p01', 'p02', 'p03'],
    'sentence_ids': [f's{n:02d}' for n in range(1, 10)],
    'today_words': [
        {'id': W['retreat'], 'text': 'retreat', 'meaning_ko': '(물이) 빠지다, 낮아지다'},
        {'id': W['visible'], 'text': 'visible', 'meaning_ko': '(눈에) 보이는'},
        {'id': W['significant'], 'text': 'significant', 'meaning_ko': '중요한, 의미 있는'},
        {'id': W['bear'], 'text': 'bear', 'meaning_ko': '(기록 등을) 지니다, 담고 있다'},
        {'id': W['hardship'], 'text': 'hardship', 'meaning_ko': '어려움, 고난'},
        {'id': W['urge'], 'text': 'urge', 'meaning_ko': '촉구하다'},
        {'id': W['occasional'], 'text': 'occasional', 'meaning_ko': '가끔 일어나는, 이따금의'},
        {'id': W['persist'], 'text': 'persist', 'meaning_ko': '지속되다, 계속되다'},
    ],
}


def analysis(_):
    return {
        'heading_kind': '제목',
        'title_or_topic_en': 'Stones That Warn of Drought',
        'title_or_topic_ko': '가뭄을 경고하는 돌',
        'intent_ko': '가뭄으로 강물이 줄어들 때 드러나는 기아석을 소개하고, 그 돌이 과거 가뭄의 기록이자 대비하라는 경고임을 설명한다. 이어서 기후 변화로 앞으로 가뭄이 더 길고 심각해질 수 있다는 전문가와 유엔의 경고를 전한다.',
        'flow': [
            {'sentence_ids': ['s01', 's02'], 'label': '도입',
             'text_ko': '2022년 유럽의 극심한 가뭄 때 체코의 한 마을에서 기아석이 발견되었다. 그 돌에는 “나를 보면 울어라.”라고 적혀 있었다.'},
            {'sentence_ids': ['s03', 's04', 's05', 's06', 's07'], 'label': '설명',
             'text_ko': '기아석은 평소 물속에 있다가 가뭄으로 수위가 낮아지면 드러난다. 과거 가뭄의 기록을 담고 있어 중요하며, 가뭄이 가져오는 흉작·식량 부족·굶주림을 경고하고 대비를 촉구하는 것으로 여겨진다.'},
            {'sentence_ids': ['s08', 's09'], 'label': '경고',
             'text_ko': '전문가들은 기후 변화로 수십 년 동안 이어질 수 있는 심각한 가뭄을 경고한다. 유엔은 중대한 조치가 없으면 2050년까지 세계 인구의 75퍼센트가 가뭄의 영향을 받을 수 있다고 예측했다.'},
        ],
        'easy_explanations': [
            {'sentence_id': 's02', 'explanatory_sentences': [
                '2번 문장은 1번에서 발견된 기아석에 무엇이 적혀 있었는지 알려 준다.',
                '돌에는 “나를 보면 울어라.”라는 문장이 새겨져 있었다.',
                '여기서 ‘나’는 말하는 돌, 곧 기아석 자신이다.',
                '이 돌을 보게 되는 때는 울 만큼 힘든 때라는 경고다.',
                '왜 그런 때인지는 뒤의 4~7번 문장에서 설명된다.']},
            {'sentence_id': 's05', 'explanatory_sentences': [
                '5번 문장은 4번에서 모습을 드러낸 돌들이 왜 중요한지 설명한다.',
                '기아석에는 과거에 있었던 극심한 가뭄의 기록이 남아 있다.',
                '사람들은 이 기록을 보고 예전에도 이런 가뭄이 있었다는 것을 알 수 있다.',
                '그래서 기아석은 단순한 돌이 아니라 역사를 담은 자료가 된다.']},
            {'sentence_id': 's09', 'explanatory_sentences': [
                '9번 문장은 8번 전문가들의 경고에 유엔의 예측을 더한다.',
                '유엔은 2050년까지 세계 인구의 75퍼센트가 가뭄의 영향을 받을 수 있다고 예측했다.',
                '다만 이 예측에는 조건이 붙어 있다.',
                '기후 변화에 대처하는 중대한 조치를 취하지 않는 경우다.',
                '이 예측은 8번 전문가들의 경고를 숫자로 뒷받침한다.']},
        ],
        'grammar_points': [
            {'id': 'u1-gp1', 'sentence_id': 's01', 'span': 'a stone known as a “hunger stone”',
             'title': '명사 + p.p.: p.p.된(한) 명사', 'formula_key': 'N + p.p.',
             'explanation': '공식: 명사(N) + p.p. — p.p.된(한) N. N = a stone(한 돌), p.p. = known(알려진), as a “hunger stone” = ‘기아석’으로. '
                            '→ ‘기아석’으로 알려진 돌. 돌이 스스로 알리는 것이 아니라 ‘기아석’이라고 알려진(불리는) 쪽이라 과거분사 known이 뒤에서 꾸민다. '
                            '이 명사구 전체가 문장의 주어다.',
             'practice': {'span': 'a stone known as a “hunger stone”',
                          'formula_support': {'en': 'N + p.p.', 'ko': 'p.p.된(한) N'},
                          'support': [('s01', 'stone'), ('s01', 'known'), ('s01', 'as'), ('s01', 'hunger stone')],
                          'answer_ko': '‘기아석’으로 알려진 돌'}},
            {'id': 'u1-gp2', 'sentence_id': 's07', 'span': 'are believed to warn of these hardships and to urge people to be prepared',
             'title': 'be believed to V: V하는 것으로 여겨지다', 'formula_key': 'be believed to V',
             'explanation': '공식: be believed to V — V하는 것으로 여겨지다(믿어지다). be believed = are believed(여겨진다), '
                            'V = warn of these hardships(이러한 어려움들에 대해 경고하다)와 urge people to be prepared(사람들에게 대비하라고 촉구하다). '
                            '→ 이러한 어려움들에 대해 경고하고 사람들에게 대비하라고 촉구하는 것으로 여겨진다. and 뒤의 to urge도 같은 are believed에 이어진다.',
             'practice': {'span': 'are believed to warn of these hardships',
                          'formula_support': {'en': 'be believed to V', 'ko': 'V하는 것으로 여겨지다'},
                          'support': [('s07', 'warn of'), ('s07', 'these'), ('s07', 'hardships')],
                          'answer_ko': '이러한 어려움들에 대해 경고하는 것으로 여겨진다'}},
            {'id': 'u1-gp3', 'sentence_id': 's08', 'span': 'is not just a simple, occasional drought but a severe drought',
             'title': 'not just A but B: 단지 A가 아니라 B', 'formula_key': 'not just A but B',
             'explanation': '공식: not just A but B — 단지 A가 아니라 B. A = a simple, occasional drought(단순하고 가끔 일어나는 가뭄), '
                            'B = a severe drought(심각한 가뭄). → 단지 단순하고 가끔 일어나는 가뭄이 아니라 심각한 가뭄. '
                            '앞의 the situation … is(상황은 ~이다)와 합치면 ‘상황이 단지 단순하고 가끔 일어나는 가뭄이 아니라 심각한 가뭄이다’가 되며, 강조하려는 내용은 B다.',
             'practice': {'span': 'not just a simple, occasional drought but a severe drought',
                          'formula_support': {'en': 'not just A but B', 'ko': '단지 A가 아니라 B'},
                          'support': [('s08', 'simple'), ('s08', 'occasional'), ('s08', 'drought'), ('s08', 'severe')],
                          'answer_ko': '단지 단순하고 가끔 일어나는 가뭄이 아니라 심각한 가뭄'}},
            {'id': 'u1-gp4', 'sentence_id': 's01', 'span': 'was found',
             'title': 'be p.p.: ~되다 (was found: 발견되었다)', 'formula_key': 'be p.p.',
             'explanation': '공식: be p.p. — ~되다. be = was(과거), p.p. = found(발견된, find의 p.p.형). → was found = 발견되었다. '
                            '돌이 무언가를 발견한 것이 아니라 사람들에게 ‘발견된’ 쪽이라 수동(be p.p.)을 쓴다. 주어 a stone과 합치면 ‘돌이 발견되었다’.',
             'supplemental': {'function': ('s01', 'be p.p.', 0),
                              'reason': 's01의 수동 was found는 과거분사 후치수식 힌트가 이미 있어 결합 힌트로 선정하지 않았고, 기본 분석 3개에 be p.p. 설명이 없어 이 단위 대표 사례로 1회 보충(s07 are believed, s09 is taken도 이 항목에 연결)'},
             'practice': {'span': 'was found',
                          'formula_support': {'en': 'be p.p.', 'ko': '~되다'},
                          'support': [('s01', 'found')],
                          'answer_ko': '발견되었다'}},
            {'id': 'u1-gp5', 'sentence_id': 's09', 'span': 'The United Nations has predicted',
             'title': 'have p.p.: ~했다 (has predicted: 예측했다)', 'formula_key': 'have p.p.',
             'explanation': '공식: have p.p. — ~했다. have = has(주어가 단일 기관 The United Nations), p.p. = predicted(predict의 p.p.형; predict = 예측하다). '
                            '→ has predicted = 예측했다(이미 예측해 둔 상태). 주어 The United Nations(유엔)와 합치면 ‘유엔은 예측했다’.',
             'supplemental': {'function': ('s09', 'have p.p.', 0),
                              'reason': 's09의 능동 완료 has predicted는 that 명사절·unless절 힌트가 이미 있어 결합 힌트로 선정하지 않았고, 기본 분석 3개에 have p.p. 설명이 없어 이 단위 대표 사례로 1회 보충'},
             'practice': {'span': 'The United Nations has predicted',
                          'formula_support': {'en': 'have p.p.', 'ko': '~했다'},
                          'support': [('s09', 'United Nations'), ('s09', 'predict')],
                          'answer_ko': '유엔은 예측했다'}},
        ],
        'formula_routes': [
            {'function': ('s01', 'be p.p.', 0), 'route': 'analysis', 'grammar_point_id': 'u1-gp4',
             'review_record': 'was found: 과거분사 후치수식 힌트가 있어 분석 보충 u1-gp4로 연결'},
            {'function': ('s07', 'be p.p.', 0), 'route': 'analysis', 'grammar_point_id': 'u1-gp4',
             'review_record': 'are believed: be believed to V·urge A to V 힌트 2개가 있어 같은 단위 be p.p. 대표 사례 u1-gp4로 연결'},
            {'function': ('s09', 'have p.p.', 0), 'route': 'analysis', 'grammar_point_id': 'u1-gp5',
             'review_record': 'has predicted: that 명사절·unless절 힌트가 있어 분석 보충 u1-gp5로 연결'},
            {'function': ('s09', 'be p.p.', 0), 'route': 'analysis', 'grammar_point_id': 'u1-gp4',
             'review_record': 'is taken: 힌트 2개가 있어 같은 단위 be p.p. 대표 사례 u1-gp4로 연결'},
        ],
        'relations': [
            {'head': {'id': 'u1-r1h', 'text': 'visible', 'meaning_ko': '눈에 보이는'},
             'synonym': {'id': 'u1-r1s', 'text': 'noticeable', 'meaning_ko': '눈에 띄는'},
             'antonym': {'id': 'u1-r1a', 'text': 'invisible', 'meaning_ko': '보이지 않는'}},
            {'head': {'id': 'u1-r2h', 'text': 'significant', 'meaning_ko': '중요한, 의미 있는'},
             'synonym': {'id': 'u1-r2s', 'text': 'important', 'meaning_ko': '중요한'},
             'antonym': {'id': 'u1-r2a', 'text': 'insignificant', 'meaning_ko': '사소한, 하찮은'}},
            {'head': {'id': 'u1-r3h', 'text': 'persist', 'meaning_ko': '지속되다, 계속되다'},
             'synonym': {'id': 'u1-r3s', 'text': 'continue', 'meaning_ko': '계속되다'},
             'antonym': {'id': 'u1-r3a', 'text': 'cease', 'meaning_ko': '그치다, 멈추다'}},
        ],
    }


def workbook():
    return {
        'relation_order': ['u1-r2s', 'u1-r3a', 'u1-r1h', 'u1-r2a', 'u1-r3s', 'u1-r1s', 'u1-r2h', 'u1-r1a', 'u1-r3h'],
        'key_sentence_ids': ['s07', 's08'],
        'question_id': 'Q01',
        'syntax_point_ids': ['u1-gp1', 'u1-gp2', 'u1-gp3', 'u1-gp4', 'u1-gp5'],
    }
