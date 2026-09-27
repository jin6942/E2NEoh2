"""Further Reading 공통 단위 1: p01~p02 s01~s12 (물건이 주는 행복이 빨리 사라지는 이유).

사용자 결정(2026-09-27 “2단위 (추천)”): 소제목 없는 단락 p01·p02를 한 단위로 묶는다.
"""
from author import S, link

W = {'long_term': 'u1-w1', 'conclusion': 'u1-w2', 'assume': 'u1-w3', 'fade': 'u1-w4',
     'used': 'u1-w5', 'possession': 'u1-w6', 'bar': 'u1-w7', 'stimulate': 'u1-w8'}


def pp(usage, s, word, lemma, fid=None, occ_after=0, review=None):
    row = {'usage': usage, 'source_span': s.span_of(word, occ_after), 'lemma': lemma}
    if fid:
        row['function_gloss_id'] = fid
    if review:
        row['review_record'] = review
    return row


def v3(s, word, lemma, subj, occ_after=0):
    """3인칭 단수 일반동사 원형 표제어 선언."""
    return pp('third-person-singular', s, word, lemma, occ_after=occ_after,
              review=f'주어 {subj}(3인칭 단수)의 일반동사 {word} → 원형 {lemma}.')


def contraction(s, clause, token, expanded):
    """it’s·there’s 같은 축약의 ’s 위치를 V로 지정하고 is/has 판정을 기록한다."""
    a = s.text.index(token)
    k = a + token.index('’')
    clause['verb_spans'] = [[k, k + 2]] + clause['verb_spans']
    clause['contraction_readings'] = [{'span': [k, k + 2], 'expanded': expanded}]


def sentences(T):
    out = []

    # ---------------- s01 ----------------
    s = S('s01', T['s01'])
    s.ch('A long-term study', '장기적인 연구는')
    s.ch('conducted', '수행된')
    s.ch('by Thomas Gilovich,', '토머스 길로비치에 의해,')
    s.ch('a psychology professor', '심리학 교수인')
    s.ch('at Cornell University,', '코넬 대학교의,')
    s.ch('reached a powerful and clear conclusion:', '강력하고 분명한 결론에 도달했다:')
    s.ch('Don’t spend your money', '여러분의 돈을 쓰지 마라')
    s.ch('on things.', '물건들에.')
    s.natural('코넬 대학교의 심리학 교수인 토머스 길로비치가 수행한 장기적인 연구는 강력하고 분명한 결론에 도달했는데, 그것은 물건에 돈을 쓰지 말라는 것이다.')
    s.cl('main', 'A', subj='A long-term study conducted by Thomas Gilovich, a psychology professor at Cornell University',
         verbs=['reached'], disp='A long-term study',
         disp_review='중심명사 study까지 표시하고 뒤에서 꾸미는 과거분사구 conducted by …와 동격 a psychology professor …는 제외')
    s.cl('imperative', 'Don’t', verbs=['Don’t', 'spend'])
    s.g('long-term', 'long-term', '장기적인, 오랜 기간의', star=W['long_term'])
    s.g('study', 'study', '연구')
    cd = s.g('conducted', 'conducted', '수행된, 실시된', verb_form=pp('past-participle', s, 'conducted', 'conduct'))
    s.g('by', 'by', '~에 의해')
    s.g('Thomas Gilovich', 'Thomas Gilovich', '토머스 길로비치 (코넬 대학교 심리학 교수)', proper=True)
    s.g('psychology', 'psychology', '심리학')
    s.g('professor', 'professor', '교수')
    s.g('at', 'at', '~의')
    s.g('Cornell University', 'Cornell University', '코넬 대학교', proper=True)
    s.g('reached', 'reach', '~에 도달하다, 이르다', verb_form=pp('regular-past', s, 'reached', 'reach'))
    s.g('powerful', 'powerful', '강력한')
    s.g('clear', 'clear', '분명한')
    s.g('conclusion', 'conclusion', '결론', star=W['conclusion'])
    s.g('Don’t', 'don’t V', '~하지 마라')
    s.g('spend|on', 'spend A on B', 'B에 A를 쓰다',
        verb_construction={'kind': 'verb-frame', 'verb_span': s.span_of('spend'), 'lemma': 'spend',
                           'link_spans': [s.span_of('on')],
                           'review_record': 'spend your money on things: A=your money, B=things.'})
    s.g('your', 'your', '여러분의', referent_ko='독자')
    s.g('money', 'money', '돈')
    s.g('things', 'things', '물건들')
    s.brk('by', 'passive-agent-by', 'conducted의 행위자(누구에 의해)를 나타내는 by 구 앞에서 끊음')
    s.brk('at', 'postnominal-preposition', 'at Cornell University는 앞 명사 a psychology professor를 뒤에서 꾸미는 전치사구')
    s.hint('A long-term study [conducted by Thomas Gilovich]', '[토머스 길로비치에 의해 수행된] 장기적인 연구',
           span='A long-term study conducted by Thomas Gilovich', label='과거분사 후치수식',
           links=[(['conducted'], ['수행된'])], participle_focus_gloss_id=cd['id'],
           meaning='토머스 길로비치에 의해 수행된 장기적인 연구',
           explanation='과거분사구 conducted by Thomas Gilovich가 앞 명사 A long-term study를 뒤에서 꾸민다. conducted ↔ 수행된.')
    s.review = ('주절 주어 A long-term study(과거분사구 conducted by …와 동격 a psychology professor at Cornell University가 뒤에서 꾸밈) + reached. '
                '콜론 뒤 부정 명령문 Don’t spend A on B는 결론의 내용. 힌트 1개(과거분사 후치수식). spend A on B는 각주로 지원. '
                'by Thomas Gilovich는 과거분사 conducted의 행위자(실제 수동 관계) → passive-agent-by 경계. 유한 수동태·관계사 없음.')
    out.append(s)

    # ---------------- s02 ----------------
    s = S('s02', T['s02'])
    s.ch('We assume', '우리는 생각한다')
    s.ch('that the happiness', '행복이')
    s.ch('we get', '우리가 얻는')
    s.ch('from buying something', '무언가를 사는 것으로부터')
    s.ch('will last', '지속될 것이라고')
    s.ch('as long as the thing itself.', '그 물건 자체만큼 오래.')
    s.natural('우리는 무언가를 사서 얻는 행복이 그 물건 자체만큼 오래 지속될 것이라고 생각한다.')
    s.cl('main', 'We', subj='We', verbs=['assume'])
    s.cl('subordinate', 'that', subj='the happiness we get from buying something', verbs=['will', 'last'], marker='that',
         disp='the happiness', disp_review='중심명사 happiness까지 표시하고 뒤에서 꾸미는 관계절 we get from buying something은 제외')
    s.cl('subordinate', 'we', subj='we', verbs=['get'], marker='that', omitted=True)
    s.g('We', 'we', '우리는', referent_ko='사람들')
    s.g('assume', 'assume', '가정하다, 생각하다', star=W['assume'])
    s.g('that', 'that S′ V′', 'S′(이/가) V′라고')
    s.g('happiness', 'happiness', '행복')
    s.g('we', 'we', '우리가', referent_ko='사람들', at=s.text.index('we get'))
    s.g('get', 'get', '얻다')
    s.g('from', 'from', '~로부터')
    f = s.g('buying', 'V-ing', '~하는 것', kind='function', combines_with=[])
    by = s.g('buying', 'buy', '사다', same=True, verb_form=pp('ing', s, 'buying', 'buy'))
    link(f, by)
    s.g('something', 'something', '무언가')
    f = s.g('will', 'will V', '~할 것이다', kind='function', combines_with=[])
    ls = s.g('last', 'last', '지속되다')
    link(f, ls)
    s.g('as|long|as', 'as long as A', 'A만큼 오래')
    s.g('thing', 'thing', '물건')
    s.g('itself', 'itself', '그 자체', referent_ko='물건')
    s.hint('the happiness [(that) we get]', '[우리[사람들]가 얻는] 행복',
           span='the happiness we get', label='목적격 관계대명사 that 생략', display_mode='omitted-relative',
           omitted_relative='that', links=[(['that'], ['가', '는'])], refs=[('we', '우리', '[사람들]')],
           meaning='우리가 얻는 행복',
           explanation='선행사 the happiness 뒤 목적격 관계대명사 that이 생략된 관계절. the happiness가 get의 목적어 자리. S′ we, V′ get까지 표시하고 from buying something은 제외.')
    s.hint('will last [as long as] the thing itself', '그 물건 자체[만큼 오래] 지속될 것이다',
           span='will last as long as the thing itself', label='원급 비교 as ~ as',
           links=[([('as', 1), ('as', 2)], ['만큼'])],
           meaning='그 물건 자체만큼 오래 지속될 것이다',
           explanation='as long as A: A만큼 오래(원급 비교). 조건의 ‘~하는 한’이 아니라 행복이 지속되는 길이를 물건과 비교한다.')
    s.review = ('주절 We assume + 명사절 접속사 that절(S′ the happiness …, V′ will last) + that절 주어 안의 목적격 관계대명사 생략 관계절 we get from buying something. '
                'as long as the thing itself는 원급 비교(조건 아님). 힌트 2개(생략 관계사, 원급 비교). that 명사절은 각주·S/V로 지원. 수동 없음.')
    out.append(s)

    # ---------------- s03 ----------------
    s = S('s03', T['s03'])
    s.ch('But it’s wrong.', '하지만 그것은 틀렸다.')
    s.natural('하지만 그 생각은 틀렸다.')
    s.cl('main', 'it’s', subj='it', verbs=[])
    contraction(s, s.clauses[-1], 'it’s', 'is')
    s.g('it’s', 'it’s (= it is)', '그것은 ~이다', referent_ko='물건만큼 행복이 오래간다는 생각')
    s.g('wrong', 'wrong', '틀린')
    s.review = '단일 절 it’s(= it is) wrong. it은 앞 문장의 생각을 가리킴. 연결·관계사·수동 없음 → 힌트 없음.'
    out.append(s)

    # ---------------- s04 ----------------
    s = S('s04', T['s04'], key=True)
    s.ch('The trouble', '문제는')
    s.ch('with things', '물건들의')
    s.ch('is that the happiness', '행복이')
    s.ch('they provide', '그것들이 제공하는')
    s.ch('fades quickly.', '빨리 사라진다는 것이다.')
    s.natural('물건의 문제는 물건이 주는 행복이 빨리 사라진다는 것이다.')
    s.cl('main', 'The', subj='The trouble with things', verbs=['is'], disp='The trouble',
         disp_review='중심명사 trouble까지 표시하고 뒤에서 꾸미는 with things는 제외')
    s.cl('subordinate', 'that', subj='the happiness they provide', verbs=['fades'], marker='that',
         disp='the happiness', disp_review='중심명사 happiness까지 표시하고 뒤에서 꾸미는 관계절 they provide는 제외')
    s.cl('subordinate', 'they', subj='they', verbs=['provide'], marker='that', omitted=True)
    s.g('trouble', 'trouble', '문제, 골칫거리')
    s.g('with', 'with', '~의')
    s.g('things', 'things', '물건들')
    s.g('is', 'is', '~이다')
    s.g('that', 'that S′ V′', 'S′(이/가) V′라는 것')
    s.g('happiness', 'happiness', '행복')
    s.g('they', 'they', '그것들이', referent_ko='물건들')
    s.g('provide', 'provide', '제공하다')
    s.g('fades', 'fade', '사라지다, 희미해지다', star=W['fade'], verb_form=v3(s, 'fades', 'fade', 'the happiness'))
    s.g('quickly', 'quickly', '빨리')
    s.brk('with', 'postnominal-preposition', 'with things는 앞 명사 The trouble을 뒤에서 꾸미는 전치사구')
    s.hint('the happiness [(that) they provide]', '[그것들[물건들]이 제공하는] 행복',
           span='the happiness they provide', label='목적격 관계대명사 that 생략', display_mode='omitted-relative',
           omitted_relative='that', links=[(['that'], ['이', '는'])], refs=[('they', '그것들', '[물건들]')],
           meaning='그것들이 제공하는 행복',
           explanation='선행사 the happiness 뒤 목적격 관계대명사 that이 생략된 관계절(provide의 목적어 자리). S′ they, V′ provide.')
    s.review = ('주어 The trouble with things(with 앞 후치수식 경계) + is + 보어 that 명사절(S′ the happiness they provide, V′ fades). '
                'that절 주어 안에 목적격 관계대명사 생략 관계절 they provide. 보어 that절 힌트는 관계절 힌트를 포함해 합쳐야 하므로 필수 관계사 힌트 1개만 두고, that절은 각주·S/V·u1-gp2로 지원. 수동 없음.')
    out.append(s)

    # ---------------- s05 ----------------
    s = S('s05', T['s05'])
    s.ch('There are three critical reasons', '세 가지 결정적인 이유들이 있다')
    s.ch('for this.', '이것에 대한.')
    s.natural('여기에는 세 가지 결정적인 이유가 있다.')
    s.cl('main', 'There', subj='three critical reasons for this', verbs=[], vfirst=['are'], disp='three critical reasons',
         disp_review='중심명사 reasons까지 표시하고 뒤에서 꾸미는 for this는 제외(유도부사 There는 주어 아님)')
    s.g('are', 'are', '있다')
    s.g('three', 'three', '세 가지의')
    s.g('critical', 'critical', '결정적인, 매우 중요한')
    s.g('reasons', 'reasons', '이유들')
    s.g('for', 'for', '~에 대한')
    s.g('this', 'this', '이것', referent_ko='물건이 주는 행복이 빨리 사라지는 것')
    s.extra_cov[tuple(s.span_of('There'))] = {'exemption': 'below-middle1-unneeded', 'level': 'below-middle1',
        'reason': '유도부사 There(초등 기초어)는 따로 해석하지 않으며 뒤 are 각주의 ‘있다’로 뜻을 지원'}
    s.brk('for', 'postnominal-preposition', 'for this는 앞 명사 three critical reasons를 뒤에서 꾸미는 전치사구')
    s.review = '유도부사 There + are + 주어 three critical reasons for this. for this의 this는 앞 문장 내용. 연결·관계사·수동 없음 → 힌트 없음.'
    out.append(s)

    # ---------------- s06 ----------------
    s = S('s06', T['s06'])
    s.ch('First,', '첫째,')
    s.ch('we get used to new possessions.', '우리는 새로운 소유물들에 익숙해진다.')
    s.natural('첫째, 우리는 새로 가진 물건에 익숙해진다.')
    s.cl('main', 'we', subj='we', verbs=['get'])
    s.g('First', 'first', '첫째')
    s.g('we', 'we', '우리는', referent_ko='사람들')
    s.g('get|used|to', 'get used to', '~에 익숙해지다', star=W['used'])
    s.g('new', 'new', '새로운')
    s.g('possessions', 'possessions', '소유물들, 가진 물건들', star=W['possession'])
    s.review = ('단일 절. get used to(~에 익숙해지다)는 used to를 따로 떼면 뜻이 달라지는 고정 표현이라 한 각주. '
                '연결·관계사·수동 없음 → 힌트 없음.')
    out.append(s)

    # ---------------- s07 ----------------
    s = S('s07', T['s07'])
    s.ch('What once seemed novel and exciting', '한때 새롭고 신나 보였던 것이')
    s.ch('quickly becomes the norm.', '빨리 일상적인 것이 된다.')
    s.natural('한때 새롭고 신나 보였던 것은 금방 평범한 일상이 된다.')
    s.cl('main', 'What', subj='What once seemed novel and exciting', verbs=['becomes'])
    s.cl('subject_relative', 'What', verbs=['seemed'], marker='What')
    rel = s.g('What', 'what V′', 'V′했던 것 (관계대명사)')
    s.g('once', 'once', '한때')
    s.g('seemed', 'seem', '~해 보이다', verb_form=pp('regular-past', s, 'seemed', 'seem'))
    s.g('novel', 'novel', '새로운, 참신한 (흔한 뜻: 소설)')
    s.g('exciting', 'exciting', '신나는, 흥미진진한')
    s.g('quickly', 'quickly', '빨리')
    s.g('becomes', 'become', '~이 되다', verb_form=v3(s, 'becomes', 'become', 'What 관계절'))
    s.g('norm', 'norm', '일상적인 것, 표준')
    s.hint('[What once seemed novel and exciting]', '[한때 새롭고 신나 보였던 것]', span='What once seemed novel and exciting',
           label='관계대명사 what', links=[(['What'], ['던 것'])],
           meaning='한때 새롭고 신나 보였던 것',
           explanation='선행사를 포함한 관계대명사 what이 이끄는 절이 문장 전체의 주어다. what이 seemed의 주어라 V′ seemed와 뜻을 잡는 최소 보어 novel and exciting까지 표시.')
    s.relative_ids = [rel['id']]
    s.review = ('관계대명사 what절(What once seemed novel and exciting)이 주어 + becomes the norm. what은 seemed의 주어. '
                'seem은 보어 없이 뜻이 잡히지 않아 최소 보어까지 표시(s50 결정 “현행 유지”와 같은 기준). 힌트 1개(필수 관계사). 수동 없음.')
    out.append(s)

    # ---------------- s08 ----------------
    s = S('s08', T['s08'])
    s.ch('Second,', '둘째,')
    s.ch('we keep raising the bar.', '우리는 계속 기준을 높인다.')
    s.natural('둘째, 우리는 계속 기준을 높인다.')
    s.cl('main', 'we', subj='we', verbs=['keep'])
    s.g('Second', 'second', '둘째')
    s.g('we', 'we', '우리는', referent_ko='사람들')
    s.g('keep', 'keep V-ing', '계속 ~하다',
        verb_construction={'kind': 'verb-frame', 'verb_span': s.span_of('keep'), 'lemma': 'keep', 'link_spans': [],
                           'review_record': 'keep raising the bar: keep의 목적어 V-ing. V-ing 연결 뜻은 이 구문이 제공.'})
    s.g('raising the bar', 'raise the bar', '기준을 높이다', star=W['bar'], verb_form=pp('ing', s, 'raising', 'raise'))
    s.review = '단일 절 keep V-ing(raising the bar, 기준을 높이다 — 한 덩어리 표현). 연결·관계사·수동 없음 → 힌트 없음.'
    out.append(s)

    # ---------------- s09 ----------------
    s = S('s09', T['s09'])
    s.ch('New purchases lead to new expectations.', '새로운 구매들은 새로운 기대들로 이어진다.')
    s.natural('새로 산 물건은 새로운 기대로 이어진다.')
    s.cl('main', 'New', subj='New purchases', verbs=['lead'])
    s.g('New', 'new', '새로운')
    s.g('purchases', 'purchases', '구매들, 구매한 물건들')
    s.g('lead', 'lead', '이어지다')
    s.g('to', 'to', '~로')
    s.g('new', 'new', '새로운')
    s.g('expectations', 'expectations', '기대들')
    s.review = '단일 절. lead와 to는 대표 뜻(~로)으로 이해되어 분리. 연결·관계사·수동 없음 → 힌트 없음.'
    out.append(s)

    # ---------------- s10 ----------------
    s = S('s10', T['s10'], key=True)
    s.ch('As soon as we get used to a new possession,', '우리가 새로운 소유물에 익숙해지자마자,')
    s.ch('we look for an even better one.', '우리는 훨씬 더 좋은 것을 찾는다.')
    s.natural('새로 가진 물건에 익숙해지자마자 우리는 훨씬 더 좋은 것을 찾는다.')
    s.cl('subordinate', 'As', subj='we', verbs=['get'], marker='As soon as')
    s.cl('main', 'we', subj='we', verbs=['look'], occ=1)
    s.g('As|soon|as', 'as soon as S′ V′', 'S′(이/가) V′하자마자')
    s.g('we', 'we', '우리가', referent_ko='사람들')
    s.g('get|used|to', 'get used to', '~에 익숙해지다', star=W['used'])
    s.g('new', 'new', '새로운')
    s.g('possession', 'possession', '소유물, 가진 물건', star=W['possession'])
    s.g('we', 'we', '우리는', referent_ko='사람들')
    s.g('look|for', 'look for', '~을 찾다')
    s.g('even', 'even', '훨씬')
    s.g('better', 'better', '더 좋은 (good의 비교급)')
    s.g('one', 'one', '것', referent_ko='소유물')
    s.hint('[As soon as we get used]', '[우리[사람들]가 익숙해지자마자]', span='As soon as we get used',
           label='접속사 as soon as', links=[(['As soon as'], ['가', '자마자'])], refs=[('we', '우리', '[사람들]')],
           meaning='우리가 (새로운 소유물에) 익숙해지자마자',
           explanation='as soon as S′ V′: S′가 V′하자마자. S′ we, V′ get used까지 표시하고 to a new possession은 제외.')
    s.review = ('시간 부사절 As soon as(S′ we, V′ get) + 주절 we look for an even better one. one은 possession을 대신함. '
                '힌트 1개(as soon as). 관계사·수동 없음.')
    out.append(s)

    # ---------------- s11 ----------------
    s = S('s11', T['s11'])
    s.ch('Third,', '셋째,')
    s.ch('possessions stimulate humans', '소유물들은 인간들을 자극한다')
    s.ch('to compare themselves with others.', '그들 자신을 다른 사람들과 비교하도록.')
    s.natural('셋째, 소유물은 인간이 자신을 다른 사람과 비교하도록 자극한다.')
    s.cl('main', 'possessions', subj='possessions', verbs=['stimulate'])
    s.g('Third', 'third', '셋째')
    s.g('possessions', 'possessions', '소유물들, 가진 물건들', star=W['possession'])
    s.g('stimulate|to', 'stimulate A to V', 'A(이/가) ~하도록 자극하다', star=W['stimulate'],
        verb_construction={'kind': 'verb-frame', 'verb_span': s.span_of('stimulate'), 'lemma': 'stimulate',
                           'link_spans': [s.span_of('to')],
                           'review_record': 'stimulate humans to compare: A=humans, to V=to compare.'})
    s.g('humans', 'humans', '인간들')
    s.g('compare|with', 'compare A with B', 'A를 B와 비교하다')
    s.g('themselves', 'themselves', '그들 자신을', referent_ko='인간들')
    s.g('others', 'others', '다른 사람들')
    s.hint('stimulate humans [to compare]', '인간들이 [비교하도록] 자극한다', span='stimulate humans to compare',
           label='stimulate A to V 구문', links=[(['stimulate', 'to'], ['이', '도록'])],
           emphasis_policy='ko-only-verb-construction',
           meaning='인간들이 (자신을 다른 사람들과) 비교하도록 자극한다',
           explanation='stimulate A to V: A가 ~하도록 자극하다. A=humans, to V=to compare. 목적어 themselves와 with others는 표시에서 제외.')
    s.review = ('단일 절 stimulate A to V(A=humans, to V=to compare) + compare A with B(A=themselves, B=others). '
                '상위 문법 연결이 없어 동사 구문 stimulate A to V를 힌트로 선정. 관계사·수동 없음.')
    out.append(s)

    # ---------------- s12 ----------------
    s = S('s12', T['s12'])
    s.ch('We buy a new car', '우리는 새 차를 산다')
    s.ch('and are thrilled with it', '그리고 그것에 몹시 기뻐한다')
    s.ch('until a friend buys a better one,', '친구가 더 좋은 것을 살 때까지,')
    s.ch('and there’s always someone', '그리고 항상 누군가가 있다')
    s.ch('with a better one.', '더 좋은 것을 가진.')
    s.natural('우리는 새 차를 사서 친구가 더 좋은 차를 살 때까지 그 차에 몹시 기뻐하는데, 더 좋은 차를 가진 사람은 언제나 있다.')
    s.cl('main', 'We', subj='We', verbs=['buy', 'and', 'are'])
    s.cl('subordinate', 'until', subj='a friend', verbs=['buys'], marker='until')
    s.cl('main', 'there’s', subj='someone with a better one', verbs=[], marker='and', disp='someone',
         disp_review='중심 대명사 someone까지 표시하고 뒤에서 꾸미는 with a better one은 제외(유도부사 there는 주어 아님)')
    contraction(s, s.clauses[-1], 'there’s', 'is')
    s.g('We', 'we', '우리는', referent_ko='사람들')
    s.g('buy', 'buy', '사다')
    s.g('new', 'new', '새로운')
    s.g('car', 'car', '차')
    s.g('are|thrilled|with', 'be thrilled with', '~에 몹시 기뻐하다')
    s.g('it', 'it', '그것', referent_ko='새 차')
    s.g('until', 'until S′ V′', 'S′(이/가) V′할 때까지')
    s.g('friend', 'friend', '친구')
    s.g('buys', 'buy', '사다', verb_form=v3(s, 'buys', 'buy', 'a friend'))
    s.g('better', 'better', '더 좋은 (good의 비교급)')
    s.g('one', 'one', '것', referent_ko='차')
    s.g('there’s', 'there’s (= there is)', '~이 있다')
    s.g('always', 'always', '항상')
    s.g('someone', 'someone', '누군가')
    s.g('with', 'with', '~을 가진')
    s.g('better', 'better', '더 좋은 (good의 비교급)', at=s.text.index('better one.'))
    s.g('one', 'one', '것', referent_ko='차', at=s.text.index('one.'))
    s.brk('with', 'postnominal-preposition', 'with a better one은 앞 대명사 someone을 뒤에서 꾸미는 전치사구',
          after=s.text.index('someone'))
    s.hint('[until a friend buys]', '[친구가 살 때까지]', span='until a friend buys', label='접속사 until',
           links=[(['until'], ['가', '때까지'])], meaning='친구가 (더 좋은 것을) 살 때까지',
           explanation='until S′ V′: S′가 V′할 때까지. S′ a friend, V′ buys까지 표시하고 목적어 a better one은 제외.')
    s.review = ('첫 절 We buy … and are thrilled with it(동사 buy와 are가 and로 병렬, be thrilled with는 한 각주) + 시간 부사절 until(S′ a friend, V′ buys) '
                '+ and 뒤 둘째 절 there’s(= there is) always someone with a better one. one은 car를 대신함. 힌트 1개(until). 관계사·수동 없음.')
    out.append(s)
    return out


UNIT = {
    'id': 'u1', 'source_id': 'src', 'paragraph_ids': ['p01', 'p02'],
    'sentence_ids': [f's{n:02d}' for n in range(1, 13)],
    'today_words': [
        {'id': W['long_term'], 'text': 'long-term', 'meaning_ko': '장기적인, 오랜 기간의'},
        {'id': W['conclusion'], 'text': 'conclusion', 'meaning_ko': '결론'},
        {'id': W['assume'], 'text': 'assume', 'meaning_ko': '가정하다, 생각하다'},
        {'id': W['fade'], 'text': 'fade', 'meaning_ko': '사라지다, 희미해지다'},
        {'id': W['used'], 'text': 'get used to', 'meaning_ko': '~에 익숙해지다'},
        {'id': W['possession'], 'text': 'possession', 'meaning_ko': '소유물, 가진 물건'},
        {'id': W['bar'], 'text': 'raise the bar', 'meaning_ko': '기준을 높이다'},
        {'id': W['stimulate'], 'text': 'stimulate A to V', 'meaning_ko': 'A가 ~하도록 자극하다'},
    ],
}


def analysis(_):
    return {
        'heading_kind': '제목',
        'title_or_topic_en': 'Why the Happiness from Things Fades Quickly',
        'title_or_topic_ko': '물건이 주는 행복이 빨리 사라지는 이유',
        'intent_ko': '물건에 돈을 쓰지 말라는 장기 연구의 결론을 소개하고, 물건이 주는 행복이 빨리 사라지는 세 가지 이유(새 물건에 익숙해짐, 계속 높아지는 기대, 남과의 비교)를 차례로 설명하는 글이다.',
        'flow': [
            {'sentence_ids': ['s01', 's02', 's03', 's04', 's05'], 'label': '연구 결론과 문제 제기',
             'text_ko': '길로비치 교수의 장기 연구는 물건에 돈을 쓰지 말라는 결론을 내렸다. 우리는 물건에서 얻는 행복이 물건만큼 오래간다고 생각하지만 그것은 틀렸다. 물건이 주는 행복은 빨리 사라지며, 여기에는 세 가지 이유가 있다.'},
            {'sentence_ids': ['s06', 's07', 's08', 's09', 's10', 's11', 's12'], 'label': '세 가지 이유',
             'text_ko': '첫째, 새 물건에 곧 익숙해져 새로움이 평범해진다. 둘째, 기준이 계속 높아져 익숙해지자마자 더 좋은 것을 찾는다. 셋째, 물건은 남과 비교하게 만드는데, 더 좋은 것을 가진 사람은 언제나 있다.'},
        ],
        'easy_explanations': [
            {'sentence_id': 's02', 'explanatory_sentences': [
                '2번 문장은 1번의 결론을 설명하려고 우리가 흔히 하는 생각을 먼저 꺼낸다.',
                '물건을 사면 기분이 좋아진다.',
                '우리는 이 좋은 기분이 그 물건만큼 오래갈 것이라고 생각한다.',
                '3번 문장에서 글쓴이는 이 생각이 틀렸다고 말한다.']},
            {'sentence_id': 's07', 'explanatory_sentences': [
                '7번 문장은 6번에서 말한 첫째 이유를 더 자세히 풀어 준다.',
                '새 물건을 처음 샀을 때는 새롭고 신나게 느껴진다.',
                '하지만 그 물건은 금방 늘 있는 평범한 것이 된다.',
                '그래서 처음 느꼈던 즐거움도 오래가지 않는다.']},
            {'sentence_id': 's12', 'explanatory_sentences': [
                '12번 문장은 11번에서 말한 셋째 이유인 남과의 비교를 새 차의 예로 보여 준다.',
                '우리는 새 차를 사면 몹시 기뻐한다.',
                '그런데 그 기쁨은 친구가 더 좋은 차를 살 때까지만 간다.',
                '게다가 더 좋은 것을 가진 사람은 언제나 있다.']},
        ],
        'grammar_points': [
            {'id': 'u1-gp1', 'sentence_id': 's02', 'span': 'the happiness we get from buying something',
             'title': '명사 + (that) S′ V′: S′가 V′하는 명사', 'formula_key': 'N + (that) S′ V′',
             'explanation': '공식: 명사(N) + (that) S′ V′ — S′(이/가) V′하는 N. 선행사 = the happiness(행복), 생략된 that = 목적격 관계대명사(get의 목적어 자리), '
                            'S′ = we(우리), V′ = get(얻다), from buying something = 무언가를 사는 것으로부터. '
                            '→ 우리가 무언가를 사는 것으로부터 얻는 행복. get 뒤에 목적어가 없는 것은 앞의 the happiness가 그 자리의 뜻을 맡기 때문이다.',
             'practice': {'span': 'the happiness we get from buying something',
                          'formula_support': {'en': 'N + (that) S′ V′', 'ko': 'S′(이/가) V′하는 N'},
                          'support': [('s02', 'happiness'), ('s02', 'we', 1), ('s02', 'get'), ('s02', 'from'),
                                      ('s02', 'V-ing'), ('s02', 'buy'), ('s02', 'something')],
                          'answer_ko': '우리가 무언가를 사는 것으로부터 얻는 행복'}},
            {'id': 'u1-gp2', 'sentence_id': 's04', 'span': 'The trouble with things is that the happiness they provide fades quickly',
             'title': 'A is that S′ V′: A는 S′가 V′한다는 것이다', 'formula_key': 'is that S′ V′',
             'explanation': '공식: A is that S′ V′ — A는 S′(이/가) V′한다는 것이다. A = The trouble with things(물건들의 문제), that = 명사절 접속사(~라는 것), '
                            'S′ = the happiness they provide(그것들[물건들]이 제공하는 행복), V′ = fades(사라지다), quickly = 빨리. '
                            '→ 물건들의 문제는 그것들이 제공하는 행복이 빨리 사라진다는 것이다. is 뒤 that절이 주어가 무엇인지 설명하는 보어다.',
             'practice': {'span': 'is that the happiness they provide fades quickly',
                          'formula_support': {'en': 'is that S′ V′', 'ko': 'S′(이/가) V′한다는 것이다'},
                          'support': [('s04', 'happiness'), ('s04', 'they'), ('s04', 'provide'), ('s04', 'fade'), ('s04', 'quickly')],
                          'answer_ko': '그것들이 제공하는 행복이 빨리 사라진다는 것이다'}},
            {'id': 'u1-gp3', 'sentence_id': 's11', 'span': 'possessions stimulate humans to compare themselves with others',
             'title': 'stimulate A to V: A가 ~하도록 자극하다', 'formula_key': 'stimulate A to V',
             'explanation': '공식: stimulate A to V — A(이/가) ~하도록 자극하다. A = humans(인간들), to V = to compare(비교하다; compare A with B = A를 B와 비교하다), '
                            'compare의 목적어 = themselves(그들 자신), with others = 다른 사람들과. '
                            '→ 인간들이 그들 자신을 다른 사람들과 비교하도록 자극하다.',
             'practice': {'span': 'stimulate humans to compare themselves with others',
                          'formula_support': {'en': 'stimulate A to V', 'ko': 'A(이/가) ~하도록 자극하다'},
                          'support': [('s11', 'humans'), ('s11', 'compare A with B'), ('s11', 'themselves'), ('s11', 'others')],
                          'answer_ko': '인간들이 그들 자신을 다른 사람들과 비교하도록 자극하다'}},
        ],
        'formula_routes': [],
        'relations': [
            {'head': {'id': 'u1-r1h', 'text': 'clear', 'meaning_ko': '분명한'},
             'synonym': {'id': 'u1-r1s', 'text': 'obvious', 'meaning_ko': '명백한'},
             'antonym': {'id': 'u1-r1a', 'text': 'vague', 'meaning_ko': '모호한, 희미한'}},
            {'head': {'id': 'u1-r2h', 'text': 'critical', 'meaning_ko': '결정적인, 매우 중요한'},
             'synonym': {'id': 'u1-r2s', 'text': 'essential', 'meaning_ko': '필수적인, 매우 중요한'},
             'antonym': {'id': 'u1-r2a', 'text': 'minor', 'meaning_ko': '사소한, 작은'}},
            {'head': {'id': 'u1-r3h', 'text': 'novel', 'meaning_ko': '새로운, 참신한'},
             'synonym': {'id': 'u1-r3s', 'text': 'fresh', 'meaning_ko': '새로운, 신선한'},
             'antonym': {'id': 'u1-r3a', 'text': 'familiar', 'meaning_ko': '익숙한, 친숙한'}},
        ],
    }


def workbook():
    return {
        'relation_order': ['u1-r2s', 'u1-r1a', 'u1-r3h', 'u1-r2a', 'u1-r1h', 'u1-r3s', 'u1-r2h', 'u1-r3a', 'u1-r1s'],
        'key_sentence_ids': ['s04', 's10'],
        'question_id': 'Q01',
        'syntax_point_ids': ['u1-gp1', 'u1-gp2', 'u1-gp3'],
    }
