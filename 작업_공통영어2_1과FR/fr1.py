"""Further Reading 공통 단위 1: 소제목 없는 한 단락 p01(s01~s09) ‘Breaking Out of the Echo Chamber’.

단락이 하나(9문장)라 그대로 한 공통 단위로 둔다.
"""
from author import S, link

W = {'selectively': 'u1-w1', 'perspectives': 'u1-w2', 'alternative': 'u1-w3', 'echo_chamber': 'u1-w4',
     'enclosed': 'u1-w5', 'distort': 'u1-w6', 'collaboration': 'u1-w7', 'open_mind': 'u1-w8'}


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


def sentences(T):
    out = []

    # ---------------- s01 ----------------
    s = S('s01', T['s01'])
    s.ch('These days,', '요즘,')
    s.ch('everyone accesses the news', '모든 사람은 뉴스를 접한다')
    s.ch('through the Internet or social media,', '인터넷이나 소셜 미디어를 통해,')
    s.ch('and often selectively takes the information', '그리고 자주 선택적으로 정보를 받아들인다')
    s.ch('that suits their tastes or beliefs.', '자신들의 취향이나 신념에 맞는.')
    s.natural('요즘 모든 사람은 인터넷이나 소셜 미디어를 통해 뉴스를 접하고, 자신의 취향이나 신념에 맞는 정보를 자주 선택적으로 받아들인다.')
    s.cl('main', 'everyone', subj='everyone', verbs=['accesses', 'takes'])
    s.cl('subject_relative', 'that', verbs=['suits'], marker='that')
    s.g('These|days', 'these days', '요즘')
    s.g('everyone', 'everyone', '모든 사람')
    s.g('accesses', 'access', '접하다, 이용하다', verb_form=v3(s, 'accesses', 'access', 'everyone'))
    s.g('news', 'news', '뉴스')
    s.g('through', 'through', '~을 통해')
    s.g('Internet', 'Internet', '인터넷')
    s.g('or', 'or', '또는')
    s.g('social|media', 'social media', '소셜 미디어 (SNS)')
    s.g('often', 'often', '자주, 흔히')
    s.g('selectively', 'selectively', '선택적으로, 골라서', star=W['selectively'])
    s.g('takes', 'take', '받아들이다 (흔한 뜻: 가져가다)', verb_form=v3(s, 'takes', 'take', 'everyone'))
    s.g('information', 'information', '정보')
    rel = s.g('that', 'that V′', 'V′하는 (관계대명사)')
    s.g('suits', 'suit', '~에 맞다, 어울리다', verb_form=v3(s, 'suits', 'suit', 'the information(선행사)'))
    s.g('their', 'their', '그들의', referent_ko='모든 사람')
    s.g('tastes', 'tastes', '취향들')
    s.g('or', 'or', '또는', at=s.text.index('or beliefs'))
    s.g('beliefs', 'beliefs', '신념들, 믿음들')
    s.hint('the information [that suits]', '[맞는] 정보', span='the information that suits', label='주격 관계대명사 that',
           links=[(['that'], ['는'])], meaning='(자신의 취향이나 신념에) 맞는 정보',
           explanation='선행사 the information을 주격 관계대명사 that이 받아 suits their tastes or beliefs가 꾸민다. V′ suits까지 표시하고 목적어는 제외.')
    s.relative_ids = [rel['id']]
    s.review = ('주절 everyone accesses … and (often selectively) takes …(병렬 동사, 주어 everyone은 3인칭 단수) + 주격 관계절 that suits their tastes or beliefs(선행사 the information). '
                'their는 everyone을 받는 대명사(모든 사람). 힌트 1개(주격 관계사). 수동 없음.')
    out.append(s)

    # ---------------- s02 ----------------
    s = S('s02', T['s02'], key=True)
    s.ch('However,', '하지만,')
    s.ch('consistently encountering similar perspectives', '지속적으로 비슷한 관점들을 접하는 것은')
    s.ch('without considering alternative views', '대안적인 견해들을 고려하지 않고')
    s.ch('can lead you to be trapped', '당신이 갇히게 만들 수 있다')
    s.ch('in an “echo chamber.”', '‘에코 챔버’ 안에.')
    s.natural('하지만 대안적인 견해를 고려하지 않은 채 비슷한 관점만 계속 접하는 것은 당신을 ‘에코 챔버(반향실)’에 갇히게 만들 수 있다.')
    s.cl('main', 'consistently', subj='consistently encountering similar perspectives without considering alternative views',
         verbs=['can', 'lead'])
    s.g('However', 'however', '하지만, 그러나')
    s.g('consistently', 'consistently', '지속적으로, 꾸준히')
    fe = s.g('encountering', 'V-ing', '~하는 것', kind='function', combines_with=[])
    en = s.g('encountering', 'encounter', '접하다, 마주치다', same=True, verb_form=pp('ing', s, 'encountering', 'encounter'))
    link(fe, en)
    s.g('similar', 'similar', '비슷한, 유사한')
    s.g('perspectives', 'perspectives', '관점들, 시각들', star=W['perspectives'])
    fw = s.g('without', 'without V-ing', '~하지 않고', kind='function', combines_with=[])
    cs = s.g('considering', 'consider', '고려하다', verb_form=pp('ing', s, 'considering', 'consider'))
    link(fw, cs)
    s.g('alternative', 'alternative', '대안적인, 다른', star=W['alternative'])
    s.g('views', 'views', '견해들, 관점들')
    fc = s.g('can', 'can V', '~할 수 있다', kind='function', combines_with=[])
    ld = s.g('lead|to', 'lead A to V', 'A가 ~하게 이끌다, 만들다',
             verb_construction={'kind': 'verb-frame', 'verb_span': s.span_of('lead'), 'lemma': 'lead',
                                'link_spans': [s.span_of('to')],
                                'review_record': 'lead you to be trapped: A=you, to V=to be trapped(수동 부정사).'})
    link(fc, ld)
    fb = s.g('be', 'be p.p.', '~되다, ~당하다', kind='function', combines_with=[])
    tr = s.g('trapped', 'trapped', '갇힌', verb_form=pp('passive-participle', s, 'trapped', 'trap', fb['id']))
    link(fb, tr)
    s.g('in', 'in', '~ 안에')
    s.g('echo|chamber', 'echo chamber', '에코 챔버, 반향실 (자기와 같은 의견만 되풀이해 듣게 되는 환경)', star=W['echo_chamber'])
    s.hint('[consistently encountering] similar perspectives', '비슷한 관점들을 [지속적으로 접하는 것은]',
           span='consistently encountering similar perspectives', label='동명사 주어',
           links=[(['ing'], ['는 것은'])], meaning='비슷한 관점들을 지속적으로 접하는 것은',
           explanation='동명사 encountering(~하는 것)이 이끄는 구가 문장 전체의 주어다. 뒤의 without considering alternative views까지 주어에 포함되고, 동사는 can lead다.')
    s.hint('[without considering] alternative views', '대안적인 견해들을 [고려하지 않고]',
           span='without considering alternative views', label='전치사 without + 동명사',
           links=[(['without', 'ing'], ['지 않고'])], meaning='대안적인 견해들을 고려하지 않고',
           explanation='without + 동명사 considering: ~하지 않고. 주어 동명사구 안에서 어떻게 접하는지를 덧붙인다.')
    s.review = ('동명사 주어 consistently encountering similar perspectives without considering alternative views(전체 유지) + can lead + lead A to V(A=you, to be trapped 수동 부정사). '
                'without + 동명사는 주어 동명사구 안. 힌트 2개(동명사 주어, without + 동명사). 수동 부정사 be trapped는 분석 u1-gp1(lead A to V)·u1-gp4(be p.p.)에서 설명.')
    out.append(s)

    # ---------------- s03 ----------------
    s = S('s03', T['s03'])
    s.ch('An echo chamber refers to an enclosed space', '에코 챔버는 밀폐된 공간을 가리킨다')
    s.ch('where sound doesn’t leak out', '소리가 밖으로 새어 나가지 않는')
    s.ch('and returns as an echo.', '그리고 메아리로 되돌아오는.')
    s.natural('에코 챔버(반향실)는 소리가 밖으로 새어 나가지 않고 메아리로 되돌아오는 밀폐된 공간을 말한다.')
    s.cl('main', 'An', subj='An echo chamber', verbs=['refers'])
    s.cl('subordinate', 'where', subj='sound', verbs=['doesn’t', 'leak', 'returns'], marker='where')
    s.g('echo|chamber', 'echo chamber', '에코 챔버, 반향실')
    s.g('refers|to', 'refer to A', 'A를 가리키다, 말하다', verb_form=v3(s, 'refers', 'refer', 'An echo chamber'))
    s.g('enclosed', 'enclosed', '밀폐된, 둘러싸인', star=W['enclosed'], verb_form=pp('past-participle', s, 'enclosed', 'enclose'))
    s.g('space', 'space', '공간')
    rel = s.g('where', 'where S′ V′', 'S′(이/가) V′하는 (관계부사)')
    s.g('sound', 'sound', '소리')
    fd = s.g('doesn’t', 'does not V', '~하지 않다', kind='function', combines_with=[])
    lk = s.g('leak|out', 'leak out', '새어 나가다')
    link(fd, lk)
    s.g('returns', 'return', '되돌아오다', verb_form=v3(s, 'returns', 'return', 'sound'))
    s.g('as', 'as', '~로 (자격·형태)')
    s.g('echo', 'echo', '메아리, 울림', at=s.text.index('echo.'))
    s.hint('an enclosed space [where sound doesn’t leak out]', '[소리가 새어 나가지 않는] 밀폐된 공간',
           span='an enclosed space where sound doesn’t leak out', label='관계부사 where',
           links=[(['where'], ['가', '는'])], meaning='소리가 (밖으로) 새어 나가지 않는 밀폐된 공간',
           explanation='선행사 an enclosed space(장소)를 관계부사 where가 받아 그 공간에서 일어나는 일을 설명한다. S′ sound, V′ doesn’t leak out까지 표시하고 병렬 동사 and returns as an echo는 제외.')
    s.relative_ids = [rel['id']]
    s.review = ('주절 An echo chamber refers to + 목적어 an enclosed space + 관계부사 where절(S′ sound, V′ doesn’t leak out and returns, 병렬 동사). '
                'refer to A는 동사 구문으로 묶음. 힌트 1개(관계부사 where). 수동 없음.')
    out.append(s)

    # ---------------- s04 ----------------
    s = S('s04', T['s04'])
    s.ch('The term “echo chamber”', '‘에코 챔버’라는 용어는')
    s.ch('is also used', '또한 사용된다')
    s.ch('to describe any situation', '어떤 상황이든 설명하기 위해')
    s.ch('in which you only hear opinions', '당신이 의견들만 듣는')
    s.ch('you already agree with.', '당신이 이미 동의하는.')
    s.natural('‘에코 챔버’라는 용어는 당신이 이미 동의하는 의견만 듣게 되는 모든 상황을 설명할 때도 사용된다.')
    s.cl('main', 'The', subj='The term “echo chamber”', verbs=['is', 'used'])
    s.cl('subordinate', 'in', subj='you', verbs=['hear'], marker='in which')
    s.cl('subordinate', 'you', subj='you', verbs=['agree'], marker='that', omitted=True, occ=1)
    s.g('term', 'term', '용어')
    s.g('echo|chamber', 'echo chamber', '에코 챔버, 반향실')
    fb = s.g('is', 'be p.p.', '~되다', kind='function', combines_with=[])
    s.g('also', 'also', '또한')
    us = s.g('used', 'used', '사용된', verb_form=pp('passive-participle', s, 'used', 'use', fb['id']))
    link(fb, us)
    ft = s.g('to', 'to V', '~하기 위해', kind='function', combines_with=[])
    ds = s.g('describe', 'describe', '설명하다, 묘사하다')
    link(ft, ds)
    s.g('any', 'any', '어떤 ~이든, 모든')
    s.g('situation', 'situation', '상황')
    rel = s.g('in|which', 'in which S′ V′', 'S′(이/가) V′하는 (전치사 + 관계대명사)')
    s.g('only', 'only', '오직, ~만')
    s.g('hear', 'hear', '듣다')
    s.g('opinions', 'opinions', '의견들')
    s.g('already', 'already', '이미')
    s.g('agree|with', 'agree with A', 'A에 동의하다')
    s.hint('any situation [in which you only hear]', '[당신이 듣기만 하는] 모든 상황',
           span='any situation in which you only hear', label='전치사 + 관계대명사 in which',
           links=[(['in which'], ['이', '는'])], meaning='당신이 (의견들을) 듣기만 하는 모든 상황',
           explanation='선행사 any situation을 in which(그 상황 안에서)가 받아 you only hear opinions …가 꾸민다. S′ you, V′ hear까지 표시하고 부사 only는 보존, 목적어 opinions 이하는 제외.')
    s.hint('opinions [(that) you already agree with]', '[당신이 이미 동의하는] 의견들',
           span='opinions you already agree with', label='목적격 관계대명사 that 생략', display_mode='omitted-relative',
           omitted_relative='that', links=[(['that'], ['이', '는'])], meaning='당신이 이미 동의하는 의견들',
           explanation='선행사 opinions 뒤 목적격 관계대명사 that이 생략된 관계절. opinions가 agree with의 목적어 자리(전치사 with의 목적어). S′ you, V′ agree with까지 표시.')
    s.relative_ids = [rel['id']]
    s.review = ('주절 수동 is also used(사이 부사 also) + 목적의 to describe + 목적어 any situation + 전치사 + 관계대명사 in which절(S′ you, V′ hear) + '
                '그 안의 목적격 관계대명사 생략 관계절 you already agree with(선행사 opinions, 전치사 with의 목적어). 힌트 2개(in which, 생략 관계사). '
                '현재 수동 is used는 힌트 자리가 없어 분석 보충 u1-gp4(be p.p.)로 연결.')
    out.append(s)

    # ---------------- s05 ----------------
    s = S('s05', T['s05'])
    s.ch('This can distort your understanding', '이것은 당신의 이해를 왜곡할 수 있다')
    s.ch('of reality,', '현실에 대한,')
    s.ch('and limit your ability', '그리고 당신의 능력을 제한할 수 있다')
    s.ch('to think critically', '비판적으로 생각하는')
    s.ch('and engage in meaningful debates.', '그리고 의미 있는 토론에 참여하는.')
    s.natural('이는 현실에 대한 당신의 이해를 왜곡하고, 비판적으로 생각하고 의미 있는 토론에 참여하는 당신의 능력을 제한할 수 있다.')
    s.cl('main', 'This', subj='This', verbs=['can', 'distort', 'limit'])
    s.g('This', 'this', '이것은', referent_ko='이미 동의하는 의견만 듣게 되는 에코 챔버 상황')
    fc = s.g('can', 'can V', '~할 수 있다', kind='function', combines_with=[])
    dt = s.g('distort', 'distort', '왜곡하다, 비틀다', star=W['distort'])
    s.g('your', 'your', '당신의')
    s.g('understanding', 'understanding', '이해')
    s.g('of', 'of', '~에 대한')
    s.g('reality', 'reality', '현실')
    lm = s.g('limit', 'limit', '제한하다')
    link(fc, dt, lm)
    s.g('your', 'your', '당신의', at=s.text.index('your ability'))
    s.g('ability|to', 'ability to V', '~하는 능력')
    s.g('think', 'think', '생각하다')
    s.g('critically', 'critically', '비판적으로')
    s.g('engage|in', 'engage in A', 'A에 참여하다')
    s.g('meaningful', 'meaningful', '의미 있는')
    s.g('debates', 'debates', '토론들')
    s.brk('of', 'postnominal-preposition', 'of reality는 앞 명사 your understanding을 뒤에서 꾸미는 전치사구')
    s.hint('your ability [to think critically and engage]', '[비판적으로 생각하고 참여하는] 당신의 능력',
           span='your ability to think critically and engage', label='to부정사 후치수식',
           links=[(['to'], ['는'])], meaning='비판적으로 생각하고 (의미 있는 토론에) 참여하는 당신의 능력',
           explanation='to think critically and (to) engage …가 앞 명사 your ability를 뒤에서 꾸민다(~하는 능력). to 하나에 동사 think와 engage가 병렬로 이어진다. 대상 in meaningful debates는 제외.')
    s.review = ('단일 주절 This can distort … and limit …(조동사 can이 병렬 동사 둘을 모두 이끎). This는 앞 문장의 상황(이미 동의하는 의견만 듣는 것). '
                'of reality 앞 후치수식 경계. ability to V(병렬 think / engage in). 힌트 1개(to부정사 후치수식). 수동 없음.')
    out.append(s)

    # ---------------- s06 ----------------
    s = S('s06', T['s06'])
    s.ch('Worse still,', '더 나쁜 것은,')
    s.ch('an echo chamber may foster social division,', '에코 챔버가 사회적 분열을 조장할 수도 있다는 것이다,')
    s.ch('making collaboration', '협력을 만들면서')
    s.ch('on common issues', '공통 문제들에 대한')
    s.ch('challenging.', '어렵게.')
    s.natural('더 나쁜 것은, 에코 챔버가 공통 문제에 대한 협력을 어렵게 만들면서 사회적 분열을 조장할 수도 있다는 것이다.')
    s.cl('main', 'an', subj='an echo chamber', verbs=['may', 'foster'])
    s.g('Worse|still', 'worse still', '더 나쁜 것은, 설상가상으로')
    s.g('echo|chamber', 'echo chamber', '에코 챔버, 반향실')
    fm = s.g('may', 'may V', '~할 수도 있다', kind='function', combines_with=[])
    fs = s.g('foster', 'foster', '조장하다, 키우다')
    link(fm, fs)
    s.g('social', 'social', '사회적인')
    s.g('division', 'division', '분열')
    fi = s.g('making', 'V-ing', '~하면서', kind='function', combines_with=[])
    mk = s.g('making', 'make A B', 'A를 B하게 만들다', same=True, verb_form=pp('ing', s, 'making', 'make'),
             verb_construction={'kind': 'verb-frame', 'verb_span': s.span_of('making'), 'lemma': 'make', 'link_spans': [],
                                'review_record': 'making collaboration on common issues challenging: A=collaboration on common issues, B=challenging(형용사 보어).'})
    link(fi, mk)
    s.g('collaboration', 'collaboration', '협력, 공동 작업', star=W['collaboration'])
    s.g('on', 'on', '~에 대한')
    s.g('common', 'common', '공통의')
    s.g('issues', 'issues', '문제들, 쟁점들')
    s.g('challenging', 'challenging', '어려운, 힘든')
    s.brk('on', 'postnominal-preposition', 'on common issues는 앞 명사 collaboration을 뒤에서 꾸미는 전치사구')
    s.hint('making collaboration on common issues [challenging]', '공통 문제들에 대한 협력을 [어렵게] 만들면서',
           span='making collaboration on common issues challenging', label='make A B 구문',
           links=[(['making'], ['을', '게'])], emphasis_policy='ko-only-verb-construction',
           meaning='공통 문제들에 대한 협력을 어렵게 만들면서',
           explanation='콤마 뒤 분사구 making …이 앞 내용과 함께 일어나는 결과를 ‘~하면서’로 덧붙인다. make A B: A를 B하게 만들다. A=collaboration on common issues, B=challenging(형용사).')
    s.review = ('문두 Worse still(더 나쁜 것은) + 주절 an echo chamber may foster social division + 콤마 뒤 분사구 making A B(A=collaboration on common issues, B=challenging). '
                'on common issues 앞 후치수식 경계. 힌트 1개(분사구 속 make A B). 수동 없음.')
    out.append(s)

    # ---------------- s07 ----------------
    s = S('s07', T['s07'], key=True)
    s.ch('To avoid falling into this trap,', '이 함정에 빠지는 것을 피하기 위해,')
    s.ch('you must actively seek diverse sources', '당신은 다양한 출처들을 적극적으로 찾아야 한다')
    s.ch('of information', '정보의')
    s.ch('and engage with people', '그리고 사람들과 교류해야 한다')
    s.ch('who have different views.', '다른 견해를 가지고 있는.')
    s.natural('이러한 함정에 빠지지 않으려면, 당신은 다양한 정보 출처를 적극적으로 찾고 다른 견해를 가진 사람들과 교류해야 한다.')
    s.cl('main', 'you', subj='you', verbs=['must', 'seek', 'engage'])
    s.cl('subject_relative', 'who', verbs=['have'], marker='who')
    ft = s.g('To', 'to V', '~하기 위해', kind='function', combines_with=[])
    av = s.g('avoid', 'avoid V-ing', '~하는 것을 피하다')
    link(ft, av)
    s.g('falling|into', 'fall into A', 'A에 빠지다', verb_form=pp('ing', s, 'falling', 'fall'))
    s.g('this', 'this', '이')
    s.g('trap', 'trap', '함정, 덫')
    fm = s.g('must', 'must V', '~해야 한다', kind='function', combines_with=[])
    s.g('actively', 'actively', '적극적으로')
    sk = s.g('seek', 'seek', '찾다, 구하다')
    s.g('diverse', 'diverse', '다양한')
    s.g('sources', 'sources', '출처들, 원천들')
    s.g('of', 'of', '~의')
    s.g('information', 'information', '정보')
    eg = s.g('engage|with', 'engage with A', 'A와 교류하다, 관계를 맺다')
    link(fm, sk, eg)
    s.g('people', 'people', '사람들')
    rel = s.g('who', 'who V′', 'V′하는 (관계대명사)')
    s.g('have', 'have', '가지다')
    s.g('different', 'different', '다른')
    s.g('views', 'views', '견해들, 관점들')
    s.brk('of', 'postnominal-preposition', 'of information은 앞 명사 diverse sources를 뒤에서 꾸미는 전치사구')
    s.hint('[To avoid] falling into this trap', '이 함정에 빠지는 것을 [피하기 위해]', span='To avoid falling into this trap',
           label='목적의 to부정사', links=[(['To'], ['기 위해'])], meaning='이 함정에 빠지는 것을 피하기 위해',
           explanation='문두 To avoid …는 목적(~하기 위해)을 나타낸다. avoid V-ing: ~하는 것을 피하다(falling into this trap: 이 함정에 빠지는 것).')
    s.hint('people [who have]', '[가지고 있는] 사람들', span='people who have', label='주격 관계대명사 who',
           links=[(['who'], ['는'])], meaning='(다른 견해를) 가지고 있는 사람들',
           explanation='선행사 people을 주격 관계대명사 who가 받아 have different views가 꾸민다. V′ have까지 표시하고 목적어 different views는 제외.')
    s.relative_ids = [rel['id']]
    s.review = ('문두 목적의 to부정사 To avoid falling into this trap(avoid V-ing) + 주절 you must actively seek … and engage with …(조동사 must가 병렬 동사 둘을 이끎) + '
                '주격 관계절 who have different views(선행사 people). of information 앞 후치수식 경계. this trap은 앞 문장들의 에코 챔버. 힌트 2개(목적의 to부정사, 주격 관계사). 수동 없음.')
    out.append(s)

    # ---------------- s08 ----------------
    s = S('s08', T['s08'])
    s.ch('Always remember to check the information', '항상 정보를 확인할 것을 기억하라')
    s.ch('you receive,', '당신이 받는,')
    s.ch('and keep an open mind', '그리고 열린 마음을 유지하라')
    s.ch('when discussing new ideas.', '새로운 생각들을 논의할 때.')
    s.natural('항상 당신이 받은 정보를 잊지 말고 확인하고, 새로운 생각을 논의할 때는 열린 마음을 유지하라.')
    s.cl('imperative', 'Always', verbs=['remember', 'keep'])
    s.cl('subordinate', 'you', subj='you', verbs=['receive'], marker='that', omitted=True)
    s.g('Always', 'always', '항상')
    s.g('remember|to', 'remember to V', '~할 것을 기억하다, 잊지 않고 ~하다')
    s.g('check', 'check', '확인하다')
    s.g('information', 'information', '정보')
    s.g('receive', 'receive', '받다')
    s.g('keep|open|mind', 'keep an open mind', '열린 마음을 유지하다', star=W['open_mind'])
    fw = s.g('when', 'when V-ing', '~할 때', kind='function', combines_with=[])
    dc = s.g('discussing', 'discuss', '논의하다, 토론하다', verb_form=pp('ing', s, 'discussing', 'discuss'))
    link(fw, dc)
    s.g('new', 'new', '새로운')
    s.g('ideas', 'ideas', '생각들, 아이디어들')
    s.hint('the information [(that) you receive]', '[당신이 받는] 정보',
           span='the information you receive', label='목적격 관계대명사 that 생략', display_mode='omitted-relative',
           omitted_relative='that', links=[(['that'], ['이', '는'])], meaning='당신이 받는 정보',
           explanation='선행사 the information 뒤 목적격 관계대명사 that이 생략된 관계절(receive의 목적어 자리). S′ you, V′ receive.')
    s.hint('[when discussing]', '[논의할 때]', span='when discussing', label='축약된 when 부사절',
           links=[(['when', 'ing'], ['할 때'])], meaning='(새로운 생각들을) 논의할 때',
           explanation='접속사 when 뒤에 주어·be동사가 생략되고 V-ing가 이어진 형태(when you are discussing). ~할 때. 목적어 new ideas는 표시에서 제외.')
    s.review = ('명령문 Always remember to check … and keep an open mind …(병렬 명령 동사) + 목적격 관계대명사 생략 관계절 you receive(선행사 the information) + '
                '축약된 when 부사절 when discussing new ideas. remember to V(앞으로 할 일을 잊지 않다). 힌트 2개(생략 관계사, when + V-ing). 수동 없음.')
    out.append(s)

    # ---------------- s09 ----------------
    s = S('s09', T['s09'])
    s.ch('Even if you really want', '당신이 정말로 원하더라도')
    s.ch('something to be true,', '어떤 것이 사실이기를,')
    s.ch('it doesn’t always mean', '그것이 항상 의미하는 것은 아니다')
    s.ch('that it is true.', '그것이 사실이라는 것을.')
    s.natural('어떤 것이 사실이기를 당신이 정말로 원하더라도, 그렇다고 그것이 항상 사실이라는 뜻은 아니다.')
    s.cl('subordinate', 'Even', subj='you', verbs=['want'], marker='Even if')
    s.cl('main', 'it', subj='it', verbs=['doesn’t', 'mean'])
    s.cl('subordinate', 'that', subj='it', verbs=['is'], marker='that')
    s.g('Even|if', 'even if S′ V′', 'S′(이/가) V′하더라도')
    s.g('really', 'really', '정말로')
    s.g('want|to', 'want A to V', 'A가 ~하기를 원하다')
    s.g('something', 'something', '어떤 것, 무언가')
    s.g('be', 'be', '~이다')
    s.g('true', 'true', '사실인, 진실인')
    s.g('it', 'it', '그것은', referent_ko='어떤 것이 사실이기를 원하는 것')
    fd = s.g('doesn’t|always', 'not always', '항상 ~인 것은 아니다 (부분 부정)', kind='function', combines_with=[])
    mn = s.g('mean', 'mean', '의미하다, 뜻하다')
    link(fd, mn)
    s.g('that', 'that S′ V′', 'S′(이/가) V′라는 것')
    s.g('it', 'it', '그것이', referent_ko='사실이기를 원하는 어떤 것', at=s.text.index('it is true'))
    s.g('is', 'is', '~이다')
    s.g('true', 'true', '사실인, 진실인', at=s.text.index('true.'))
    s.hint('[Even if you really want]', '[당신이 정말로 원하더라도]', span='Even if you really want', label='양보 접속사 even if',
           links=[(['Even if'], ['이', '더라도'])], meaning='당신이 (어떤 것이 사실이기를) 정말로 원하더라도',
           explanation='even if S′ V′: S′가 V′하더라도(양보). S′ you, V′ want까지 표시하고 사이 부사 really는 보존, want A to V의 A·to V는 제외.')
    s.hint('[that it is true]', '[그것이 사실이라는 것]', span='that it is true', label='명사절 접속사 that',
           links=[(['that'], ['이', '라는 것'])], meaning='그것이 사실이라는 것',
           explanation='동사 mean의 목적어 that 명사절(S′ it, V′ is, 보어 true). 바깥의 doesn’t always mean(부분 부정)은 분석 u1-gp3에서 설명.')
    s.review = ('양보 부사절 Even if you really want something to be true(want A to V, A=something) + 주절 it doesn’t always mean + 목적어 that 명사절. '
                'doesn’t always = 부분 부정(항상 ~인 것은 아니다). 앞 it은 사실이기를 원하는 일, that절 it은 원하는 그 어떤 것. 힌트 2개(even if, 명사절 that). 수동 없음.')
    out.append(s)
    return out


UNIT = {
    'id': 'u1', 'source_id': 'src', 'paragraph_ids': ['p01'],
    'sentence_ids': [f's{n:02d}' for n in range(1, 10)],
    'today_words': [
        {'id': W['selectively'], 'text': 'selectively', 'meaning_ko': '선택적으로, 골라서'},
        {'id': W['perspectives'], 'text': 'perspectives', 'meaning_ko': '관점들, 시각들'},
        {'id': W['alternative'], 'text': 'alternative', 'meaning_ko': '대안적인, 다른'},
        {'id': W['echo_chamber'], 'text': 'echo chamber', 'meaning_ko': '에코 챔버, 반향실'},
        {'id': W['enclosed'], 'text': 'enclosed', 'meaning_ko': '밀폐된, 둘러싸인'},
        {'id': W['distort'], 'text': 'distort', 'meaning_ko': '왜곡하다, 비틀다'},
        {'id': W['collaboration'], 'text': 'collaboration', 'meaning_ko': '협력, 공동 작업'},
        {'id': W['open_mind'], 'text': 'keep an open mind', 'meaning_ko': '열린 마음을 유지하다'},
    ],
}


def analysis(_):
    return {
        'heading_kind': '제목',
        'title_or_topic_en': 'Breaking Out of the Echo Chamber',
        'title_or_topic_ko': '에코 챔버에서 벗어나기',
        'intent_ko': '자기가 동의하는 의견만 듣게 되는 ‘에코 챔버’가 무엇이고 어떤 해를 끼치는지 설명한 뒤, 다양한 정보와 다른 견해를 적극적으로 접하며 열린 마음을 가지라고 당부하는 글이다.',
        'flow': [
            {'sentence_ids': ['s01', 's02'], 'label': '문제 제기',
             'text_ko': '요즘 사람들은 인터넷과 소셜 미디어로 뉴스를 접하면서 자신의 취향이나 신념에 맞는 정보만 골라 받아들이곤 한다. 다른 견해를 고려하지 않고 비슷한 관점만 계속 접하면 에코 챔버에 갇힐 수 있다.'},
            {'sentence_ids': ['s03', 's04'], 'label': '개념 설명',
             'text_ko': '에코 챔버는 원래 소리가 새지 않고 메아리로 되돌아오는 밀폐된 공간이다. 이 말은 이미 동의하는 의견만 듣는 상황을 가리킬 때도 쓰인다.'},
            {'sentence_ids': ['s05', 's06'], 'label': '문제점',
             'text_ko': '에코 챔버는 현실에 대한 이해를 왜곡하고 비판적으로 생각하고 토론하는 능력을 제한할 수 있다. 더 나아가 사회적 분열을 조장해 공통 문제에 대한 협력을 어렵게 만들 수 있다.'},
            {'sentence_ids': ['s07', 's08', 's09'], 'label': '해결 방법',
             'text_ko': '이 함정을 피하려면 다양한 정보 출처를 찾고 다른 견해를 가진 사람들과 교류해야 한다. 받은 정보를 확인하고 열린 마음을 유지하며, 원하는 것이 곧 사실은 아니라는 점을 기억해야 한다.'},
        ],
        'easy_explanations': [
            {'sentence_id': 's02', 'explanatory_sentences': [
                '2번 문장은 1번에서 말한 ‘골라 받아들이는 습관’이 어떤 결과를 낳는지 알려 준다.',
                '비슷한 관점만 계속 보고 다른 견해는 생각해 보지 않는 경우를 말한다.',
                '이런 습관이 이어지면 사람은 자신과 같은 생각만 듣는 공간에 갇힐 수 있다.',
                '글쓴이는 이 공간을 ‘에코 챔버’라고 부르며 글의 중심 소재로 삼는다.']},
            {'sentence_id': 's06', 'explanatory_sentences': [
                '6번 문장은 5번에 이어 에코 챔버의 더 큰 문제를 말한다.',
                '5번이 한 사람의 생각과 토론 능력에 미치는 영향을 말했다면, 6번은 사회 전체에 미치는 영향을 말한다.',
                '사람들이 각자 자기 생각만 들으면 서로 나뉘는 사회적 분열이 커질 수 있다.',
                '그러면 모두에게 걸린 공통 문제를 함께 해결하는 협력도 어려워진다.']},
            {'sentence_id': 's09', 'explanatory_sentences': [
                '9번 문장은 7~8번의 해결 방법을 마무리하며 기억할 점을 덧붙인다.',
                '사람은 어떤 소식이 사실이기를 바랄 때 그 소식을 쉽게 믿을 수 있다.',
                '하지만 바란다고 해서 그 소식이 항상 사실이 되는 것은 아니다.',
                '그래서 믿고 싶은 정보일수록 한 번 더 확인해야 한다는 뜻이다.']},
        ],
        'grammar_points': [
            {'id': 'u1-gp1', 'sentence_id': 's02', 'span': 'can lead you to be trapped in an “echo chamber',
             'title': 'lead A to V: A가 ~하게 만들다', 'formula_key': 'lead A to V',
             'explanation': '공식: lead A to V — A가 ~하게 이끌다(만들다). can = ~할 수 있다, A = you(당신), to V = to be trapped(갇히게 되다: be p.p. 수동), '
                            'in an “echo chamber” = 에코 챔버 안에. → 당신이 에코 챔버에 갇히게 만들 수 있다. '
                            '당신은 스스로 가두는 쪽이 아니라 ‘갇히는’ 쪽이라 to 뒤에 수동 be trapped를 쓴다.',
             'practice': {'span': 'can lead you to be trapped in an “echo chamber',
                          'formula_support': {'en': 'lead A to V', 'ko': 'A가 ~하게 만들다'},
                          'support': [('s02', 'can V'), ('s02', 'be p.p.'), ('s02', 'trapped'), ('s02', 'in'), ('s02', 'echo chamber')],
                          'answer_ko': '당신이 에코 챔버에 갇히게 만들 수 있다'}},
            {'id': 'u1-gp2', 'sentence_id': 's04', 'span': 'any situation in which you only hear opinions',
             'title': '전치사 + 관계대명사 in which: S′(이/가) V′하는 N', 'formula_key': 'in which S′ V′',
             'explanation': '공식: N + in which S′ V′ — S′(이/가) V′하는 N(그 N 안에서). N = any situation(모든 상황), in which = 그 상황 안에서, '
                            'S′ = you(당신), V′ = only hear(듣기만 하다), 목적어 = opinions(의견들). → 당신이 의견들만 듣는 모든 상황. '
                            'in which 뒤에는 주어와 목적어를 모두 갖춘 완전한 절이 온다.',
             'practice': {'span': 'any situation in which you only hear opinions',
                          'formula_support': {'en': 'in which S′ V′', 'ko': 'S′(이/가) V′하는 N'},
                          'support': [('s04', 'any'), ('s04', 'situation'), ('s04', 'only'), ('s04', 'hear'), ('s04', 'opinions')],
                          'answer_ko': '당신이 의견들만 듣는 모든 상황'}},
            {'id': 'u1-gp3', 'sentence_id': 's09', 'span': 'it doesn’t always mean that it is true',
             'title': 'not always: 항상 ~인 것은 아니다 (부분 부정)', 'formula_key': 'not always',
             'explanation': '공식: not always — 항상 ~인 것은 아니다(부분 부정). it = 그것(어떤 것이 사실이기를 원하는 것), doesn’t always mean = 항상 의미하는 것은 아니다, '
                            'that it is true = 그것이 사실이라는 것. → 그것이 항상 그것이 사실이라는 것을 의미하는 것은 아니다. '
                            '‘절대 아니다’가 아니라 ‘늘 그런 것은 아니다’라는 뜻이다.',
             'practice': {'span': 'it doesn’t always mean that it is true',
                          'formula_support': {'en': 'not always', 'ko': '항상 ~인 것은 아니다'},
                          'support': [('s09', 'it'), ('s09', 'mean'), ('s09', 'that S′ V′'), ('s09', 'true', 1)],
                          'answer_ko': '그것이 항상 그것이 사실이라는 것을 의미하는 것은 아니다'}},
            {'id': 'u1-gp4', 'sentence_id': 's04', 'span': 'The term “echo chamber” is also used',
             'title': 'be p.p.: ~되다 (현재 수동)', 'formula_key': 'be p.p.',
             'explanation': '공식: be p.p. — ~되다. S = The term “echo chamber”(‘에코 챔버’라는 용어), be = is, also = 또한, p.p. = used(use의 p.p.형, 사용하다). '
                            '→ ‘에코 챔버’라는 용어는 또한 사용된다. 용어는 스스로 사용하는 쪽이 아니라 사람들이 ‘사용하는’ 대상이라 수동을 쓴다.',
             'supplemental': {'function': ('s04', 'be p.p.', 0),
                              'reason': 's04의 현재 수동 is used는 필수 관계사 힌트 2개(in which, 생략 관계사)가 있어 결합 힌트로 선정하지 않았고, 기본 분석 3개에 현재 수동 be p.p. 설명이 없어 이 단위 대표 사례로 1회 보충'},
             'practice': {'span': 'The term “echo chamber” is also used',
                          'formula_support': {'en': 'be p.p.', 'ko': '~되다'},
                          'support': [('s04', 'term'), ('s04', 'echo chamber'), ('s04', 'also'), ('s04', 'used')],
                          'answer_ko': '‘에코 챔버’라는 용어는 또한 사용된다'}},
        ],
        'formula_routes': [
            {'function': ('s02', 'be p.p.', 0), 'route': 'analysis', 'grammar_point_id': 'u1-gp4',
             'review_record': 'to be trapped: 힌트 2개(동명사 주어, without)가 있어 같은 공식(be p.p.)의 단위 대표 분석 u1-gp4로 연결(u1-gp1 lead A to V 설명에도 수동 부정사로 언급)'},
            {'function': ('s04', 'be p.p.', 0), 'route': 'analysis', 'grammar_point_id': 'u1-gp4',
             'review_record': 'is used: 관계사 힌트 2개가 있어 분석 보충 u1-gp4로 연결'},
        ],
        'relations': [
            {'head': {'id': 'u1-r1h', 'text': 'limit', 'meaning_ko': '제한하다'},
             'synonym': {'id': 'u1-r1s', 'text': 'restrict', 'meaning_ko': '제한하다, 한정하다'},
             'antonym': {'id': 'u1-r1a', 'text': 'expand', 'meaning_ko': '넓히다, 확장하다'}},
            {'head': {'id': 'u1-r2h', 'text': 'foster', 'meaning_ko': '조장하다, 키우다'},
             'synonym': {'id': 'u1-r2s', 'text': 'encourage', 'meaning_ko': '부추기다, 촉진하다'},
             'antonym': {'id': 'u1-r2a', 'text': 'discourage', 'meaning_ko': '막다, 억제하다'}},
            {'head': {'id': 'u1-r3h', 'text': 'diverse', 'meaning_ko': '다양한'},
             'synonym': {'id': 'u1-r3s', 'text': 'various', 'meaning_ko': '여러 가지의, 다양한'},
             'antonym': {'id': 'u1-r3a', 'text': 'uniform', 'meaning_ko': '획일적인, 똑같은'}},
        ],
    }


def workbook():
    return {
        'relation_order': ['u1-r2s', 'u1-r3a', 'u1-r1h', 'u1-r2a', 'u1-r3s', 'u1-r1s', 'u1-r2h', 'u1-r1a', 'u1-r3h'],
        'key_sentence_ids': ['s02', 's07'],
        'question_id': 'Q01',
        'syntax_point_ids': ['u1-gp1', 'u1-gp2', 'u1-gp3', 'u1-gp4'],
    }
