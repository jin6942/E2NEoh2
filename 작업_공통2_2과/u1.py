"""공통 단위 1: s01~s17 (p01~p08) — 수돗물이 끊기고 쇼핑몰로 가는 장면.

사용자 결정(2026-09-28 “5단위, 작품 소개 합침”): 무소제목 소설 본문을 장면 기준으로 묶은 첫 단위.
"""
from author import S, link, verbless

W = {'tap': 'u1-w1', 'crisis': 'u1-w2', 'drought': 'u1-w3', 'stage': 'u1-w4',
     'running': 'u1-w5', 'crowd': 'u1-w6', 'checkout': 'u1-w7', 'essentials': 'u1-w8'}


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
    s.ch('The kitchen tap', '주방 수도꼭지가')
    s.ch('makes strange sounds.', '이상한 소리들을 낸다.')
    s.natural('주방 수도꼭지가 이상한 소리를 낸다.')
    s.cl('main', 'The', subj='The kitchen tap', verbs=['makes'])
    s.g('kitchen', 'kitchen', '주방, 부엌')
    s.g('tap', 'tap', '수도꼭지 (흔한 뜻: 톡톡 두드리기)', star=W['tap'])
    s.g('makes', 'make', '(소리를) 내다 (흔한 뜻: 만들다)', verb_form=v3(s, 'makes', 'make', 'The kitchen tap'))
    s.g('strange', 'strange', '이상한')
    s.g('sounds', 'sounds', '소리들')
    s.review = '단일 주절 현재형(S: The kitchen tap, V: makes). 관계사·접속사절·준동사·수동 없음 → 힌트 없음.'
    out.append(s)

    # ---------------- s02 ----------------
    s = S('s02', T['s02'])
    s.ch('It coughs.', '그것은 기침을 한다.')
    s.natural('수도꼭지가 기침을 한다.')
    s.cl('main', 'It', subj='It', verbs=['coughs'])
    s.g('It', 'it', '그것은', referent_ko='주방 수도꼭지')
    s.g('coughs', 'cough', '기침하다', verb_form=v3(s, 'coughs', 'cough', 'It(수도꼭지)'))
    s.review = '단일 주절. 수도꼭지를 사람처럼 표현(기침하다). 절 연결·수동 없음 → 힌트 없음.'
    out.append(s)

    # ---------------- s03 ----------------
    s = S('s03', T['s03'])
    s.ch('It spits once,', '그것은 한 번 침을 뱉는다,')
    s.ch('and then goes silent.', '그러고 나서 조용해진다.')
    s.natural('수도꼭지는 한 번 침을 뱉더니 이내 조용해진다.')
    s.cl('main', 'It', subj='It', verbs=['spits', 'and', 'goes'])
    s.g('It', 'it', '그것은', referent_ko='주방 수도꼭지')
    s.g('spits', 'spit', '(침을) 뱉다', verb_form=v3(s, 'spits', 'spit', 'It(수도꼭지)'))
    s.g('once', 'once', '한 번')
    s.g('then', 'then', '그러고 나서')
    s.g('goes|silent', 'go silent', '조용해지다', verb_form=v3(s, 'goes', 'go', 'It(수도꼭지)'))
    s.review = ('한 주어 It에 병렬 동사 spits와 goes(and로 연결, then은 부사). go silent는 go + 형용사(~해지다)로 각주에서 묶음. '
                '절 연결·관계사·수동 없음 → 힌트 없음.')
    out.append(s)

    # ---------------- s04 ----------------
    s = S('s04', T['s04'])
    s.ch('“Mom,”', '“엄마,”')
    s.ch('I shout out', '나는 소리쳐 외친다')
    s.ch('into the living room,', '거실 안으로,')
    s.ch('“water is not coming out.”', '“물이 나오고 있지 않아요.”')
    s.natural('“엄마,” 나는 거실을 향해 소리친다. “물이 안 나와요.”')
    s.cl('main', 'I', subj='I', verbs=['shout'])
    s.cl('main', 'water', subj='water', verbs=['is', 'coming'])
    s.g('Mom', 'Mom', '엄마')
    s.g('I', 'I', '나는', referent_ko='이야기하는 소녀 Alyssa')
    s.g('shout|out', 'shout out', '소리쳐 외치다')
    s.g('into', 'into', '~ 안으로')
    s.g('living|room', 'living room', '거실')
    s.g('water', 'water', '물')
    f = s.g('is|not', 'be not V-ing', '~하고 있지 않다', kind='function', combines_with=[])
    c = s.g('coming|out', 'come out', '나오다', verb_form=pp('ing', s, 'coming', 'come'))
    link(f, c)
    s.review = ('호격 “Mom,”과 전달절 I shout out into the living room이 인용문 사이에 끼어 있는 구조. 절은 전달절(S: I, V: shout)과 '
                '인용된 절(S: water, V: is coming; not은 부사라 V 칸에서 제외)의 두 주절. 관계사·접속사절·수동 없음 → 힌트 없음.')
    out.append(s)

    # ---------------- s05 ----------------
    s = S('s05', T['s05'])
    s.ch('“Alyssa, shush!”', '“Alyssa, 쉿!”')
    s.ch('Mom says.', '엄마가 말한다.')
    s.natural('“Alyssa, 조용히 해!” 엄마가 말한다.')
    s.cl('main', 'Mom', subj='Mom', verbs=['says'])
    s.g('Alyssa', 'Alyssa', 'Alyssa (이 이야기를 들려주는 소녀)', proper=True)
    s.g('shush', 'shush', '쉿, 조용히 해')
    s.g('Mom', 'Mom', '엄마')
    s.g('says', 'say', '말하다', verb_form=v3(s, 'says', 'say', 'Mom'))
    s.review = ('인용 “Alyssa, shush!”(호격 + 감탄사 shush, 유한동사 없음) + 전달절 Mom says. S/V는 전달절만 표시. '
                '절 연결·수동 없음 → 힌트 없음.')
    out.append(s)

    # ---------------- s06 ----------------
    s = S('s06', T['s06'])
    s.ch('She is watching the TV,', '그녀는 TV를 보고 있다,')
    s.ch('where a news anchor is talking', '그리고 거기에서 뉴스 앵커가 이야기하고 있다')
    s.ch('about the “flow crisis.”', '‘물 공급 위기’에 관해.')
    s.natural('엄마는 TV를 보고 있는데, TV에서는 뉴스 앵커가 ‘물 공급 위기’에 관해 이야기하고 있다.')
    s.cl('main', 'She', subj='She', verbs=['is', 'watching'])
    s.cl('subordinate', 'where', subj='a news anchor', verbs=['is', 'talking'], marker='where')
    s.g('She', 'she', '그녀는', referent_ko='엄마')
    f = s.g('is', 'be V-ing', '~하고 있다', kind='function', combines_with=[])
    w = s.g('watching', 'watch', '보다', verb_form=pp('ing', s, 'watching', 'watch'))
    link(f, w)
    s.g('TV', 'TV', '텔레비전')
    rel = s.g('where', 'where S′ V′', '그리고 거기에서 S′(이/가) V′하다 (관계부사)')
    s.g('news', 'news', '뉴스')
    s.g('anchor', 'anchor', '(뉴스) 앵커, 진행자')
    f = s.g('is', 'be V-ing', '~하고 있다', kind='function', combines_with=[])
    t = s.g('talking', 'talk', '이야기하다', verb_form=pp('ing', s, 'talking', 'talk'))
    link(f, t)
    s.g('about', 'about', '~에 관해')
    s.g('flow|crisis', 'flow crisis', '물 공급 위기')
    s.hint('the TV, [where a news anchor is talking]', 'TV, [그리고 거기에서 뉴스 앵커가 이야기하고 있다]',
           span='the TV, where a news anchor is talking', label='계속적 관계부사 where',
           links=[(['where'], ['그리고 거기에서', '가'])],
           meaning='TV, 그리고 거기에서(TV에서) 뉴스 앵커가 이야기하고 있다',
           explanation='콤마 뒤 관계부사 where가 앞의 the TV(장소처럼 쓰인 방송 화면)를 받아 ‘그리고 거기에서’로 설명을 덧붙인다. S′ a news anchor, V′ is talking까지 표시하고 about 이하 대상은 제외.')
    s.relative_ids = [rel['id']]
    s.review = ('주절 She is watching the TV + 콤마 뒤 계속적 관계부사 where절(선행사 the TV, S′ a news anchor, V′ is talking). '
                '필수 관계사 힌트 1개. 진행형 두 곳(be V-ing 기능/낱말 분리). 수동 없음.')
    out.append(s)

    # ---------------- s07 ----------------
    s = S('s07', T['s07'], key=True)
    s.ch('This is', '이것은')
    s.ch('what the media has been calling the drought', '언론이 가뭄을 계속 불러 온 것이다')
    s.ch('ever since people got tired', '사람들이 싫증이 난 이후로 줄곧')
    s.ch('of hearing the word “drought.”', '‘가뭄’이라는 단어를 듣는 것에.')
    s.natural('이것은 사람들이 ‘가뭄’이라는 단어를 듣는 데 싫증이 난 이후로 언론이 가뭄을 줄곧 불러 온 이름이다.')
    s.cl('main', 'This', subj='This', verbs=['is'])
    s.cl('subordinate', 'what', subj='the media', verbs=['has', 'been', 'calling'], marker='what')
    s.cl('subordinate', 'ever', subj='people', verbs=['got'], marker='ever since')
    s.g('This', 'this', '이것은', referent_ko='‘물 공급 위기’라는 말')
    s.g('is', 'is', '~이다')
    rel = s.g('what', 'what S′ V′', 'S′(이/가) V′하는 것 (관계대명사)')
    s.g('media', 'media', '언론, 대중 매체')
    cl = s.span_of('calling')
    s.g('has|been|calling', 'has been calling A B', 'A를 B라고 (계속) 불러 오고 있다', kind='lexical',
        verb_phrase={'formula_label': 'have been V-ing',
                     'source_spans': [s.span_of('has'), s.span_of('been'), cl], 'verb_span': cl})
    s.g('drought', 'drought', '가뭄', star=W['drought'])
    s.g('ever|since', 'ever since S′ V′', 'S′(이/가) V′한 이후로 줄곧')
    s.g('people', 'people', '사람들')
    s.g('got|tired|of', 'get tired of', '~에 싫증이 나다 (got은 get의 과거)')
    f = s.g('hearing', 'V-ing', '~하는 것', kind='function', combines_with=[])
    h = s.g('hearing', 'hear', '듣다', same=True, verb_form=pp('ing', s, 'hearing', 'hear'))
    link(f, h)
    s.g('word', 'word', '단어')
    s.g('drought', 'drought', '가뭄', star=W['drought'], at=s.text.index('drought.”'))
    s.hint('[what the media has been calling]', '[언론이 계속 불러 온 것]', span='what the media has been calling',
           label='관계대명사 what', links=[(['what'], ['이', '온 것'])],
           meaning='언론이 (가뭄을) 계속 불러 온 것(이름)',
           explanation='선행사를 포함한 관계대명사 what이 이끄는 절이 is의 보어다. what은 call A B(A를 B라고 부르다)의 B 자리(부르는 이름). S′ the media, V′ has been calling까지 표시하고 A(the drought)는 제외.')
    s.hint('[ever since people got tired]', '[사람들이 싫증이 난 이후로 줄곧]', span='ever since people got tired',
           label='접속사 ever since', links=[(['ever since'], ['이', '이후로 줄곧'])],
           meaning='사람들이 (‘가뭄’이라는 말을 듣는 데) 싫증이 난 이후로 줄곧',
           explanation='ever since S′ V′: S′가 V′한 이후로 줄곧. S′ people, V′ got에 뜻을 잡는 최소 보어 tired까지 표시(연결동사 get + 형용사). of hearing 이하 제외.')
    s.relative_ids = [rel['id']]
    s.review = ('주절 This is + 보어 자리 관계대명사 what절(the media has been calling the drought: call A B, A=the drought, B=what; 완료진행) '
                '+ 접속사 ever since절(people got tired of hearing …). 힌트 2개(필수 관계사 what, 접속사 ever since). '
                'has been calling은 완료진행이라 기존 결합 각주(verb_phrase have been V-ing) 유지. This는 앞 문장의 “flow crisis”라는 말을 가리킴. 수동 없음.')
    out.append(s)

    # ---------------- s08 ----------------
    s = S('s08', T['s08'])
    s.ch('Now', '이제')
    s.ch('the crisis is entering a new stage.', '그 위기는 새로운 단계로 접어들고 있다.')
    s.natural('이제 위기는 새로운 단계로 접어들고 있다.')
    s.cl('main', 'the', subj='the crisis', verbs=['is', 'entering'])
    s.g('Now', 'now', '이제')
    s.g('crisis', 'crisis', '위기', star=W['crisis'])
    f = s.g('is', 'be V-ing', '~하고 있다', kind='function', combines_with=[])
    e = s.g('entering', 'enter', '(새 시기에) 접어들다, 들어가다', verb_form=pp('ing', s, 'entering', 'enter'))
    link(f, e)
    s.g('new', 'new', '새로운')
    s.g('stage', 'stage', '단계 (흔한 뜻: 무대)', star=W['stage'])
    s.review = '단일 주절 현재진행(is entering). 절 연결·관계사·수동 없음 → 힌트 없음.'
    out.append(s)

    # ---------------- s09 ----------------
    s = S('s09', T['s09'])
    s.ch('We have no running water', '우리는 수돗물을 전혀 갖고 있지 않다')
    s.ch('out of the tap.', '수도꼭지에서 나오는.')
    s.natural('수도꼭지에서 수돗물이 나오지 않는다.')
    s.cl('main', 'We', subj='We', verbs=['have'])
    s.g('We', 'we', '우리는', referent_ko='Alyssa의 가족')
    s.g('have', 'have', '가지고 있다')
    s.g('no', 'no', '어떤 ~도 없는')
    s.g('running|water', 'running water', '수돗물', star=W['running'])
    s.g('out|of', 'out of', '~에서 나오는')
    s.g('tap', 'tap', '수도꼭지 (흔한 뜻: 톡톡 두드리기)', star=W['tap'])
    s.brk('out', 'postnominal-preposition', 'out of the tap은 앞 명사 running water를 뒤에서 꾸미는 전치사구')
    s.hint('running water [out of the tap]', '[수도꼭지에서 나오는] 수돗물', span='running water out of the tap',
           label='전치사구 후치수식', links=[(['out of'], ['에서 나오는'])],
           meaning='수도꼭지에서 나오는 수돗물',
           explanation='out of the tap이 앞 명사 running water를 뒤에서 꾸민다. 한국어에서는 명사 앞으로 옮겨 ‘수도꼭지에서 나오는’으로 붙여 읽는다.')
    s.review = ('단일 주절 We have no running water. out of the tap은 running water를 꾸미는 후치 전치사구(out 앞에서 끊음) → 힌트 1개. '
                '관계사·수동 없음.')
    out.append(s)

    # ---------------- s10 ----------------
    s = S('s10', T['s10'])
    s.ch('“To the mall!”', '“쇼핑몰로!”')
    s.ch('says Uncle Basil.', 'Basil 삼촌이 말한다.')
    s.natural('“쇼핑몰로 가자!” Basil 삼촌이 말한다.')
    s.cl('main', 'says', subj='Uncle Basil', verbs=[], vfirst=['says'])
    s.g('To', 'to', '~로')
    s.g('mall', 'mall', '쇼핑몰')
    s.g('says', 'say', '말하다', verb_form=v3(s, 'says', 'say', 'Uncle Basil'))
    s.g('Uncle|Basil', 'Uncle Basil', 'Basil 삼촌', proper=True)
    s.hint('[says Uncle Basil]', '[Basil 삼촌이 말한다]', span='says Uncle Basil', label='인용 뒤 동사·주어 도치',
           links=[(['says'], ['말한다'])], meaning='Basil 삼촌이 말한다',
           explanation='직접 인용 뒤에서 동사 says가 주어 Uncle Basil 앞에 온 도치. 해석은 주어부터 ‘Basil 삼촌이 말한다’. 앞으로 나간 says ↔ 말한다를 강조(영어2 YBM 2과 FR s16 선례와 같은 기준).')
    s.review = ('인용 “To the mall!”(유한동사 없는 전치사구 외침) + 도치된 전달절 says Uncle Basil. S/V는 전달절(S: Uncle Basil, V: says). '
                '도치 힌트 1개. 관계사·수동 없음.')
    out.append(s)

    # ---------------- s11 ----------------
    s = S('s11', T['s11'])
    s.ch('My little brother Garrett and I', '내 남동생 Garrett과 나는')
    s.ch('jump in our uncle’s truck.', '우리 삼촌의 트럭에 올라탄다.')
    s.natural('남동생 Garrett과 나는 삼촌의 트럭에 올라탄다.')
    s.cl('main', 'My', subj='My little brother Garrett and I', verbs=['jump'])
    s.g('My', 'my', '나의', referent_ko='Alyssa')
    s.g('little|brother', 'little brother', '남동생')
    s.g('Garrett', 'Garrett', 'Garrett (Alyssa의 남동생)', proper=True)
    s.g('I', 'I', '나는', referent_ko='Alyssa')
    s.g('jump|in', 'jump in', '(차에) 올라타다')
    s.g('our', 'our', '우리의', referent_ko='Alyssa와 Garrett')
    s.g('uncle’s', 'uncle’s', '삼촌의')
    s.g('truck', 'truck', '트럭')
    s.review = '등위 주어 My little brother Garrett and I(전체 유지) + V jump. 절 연결·관계사·수동 없음 → 힌트 없음.'
    out.append(s)

    # ---------------- s12 ----------------
    s = S('s12', T['s12'])
    s.ch('As we pull into the parking lot,', '우리가 주차장에 차를 몰고 들어설 때,')
    s.ch('we can see the crowd.', '우리는 사람들의 무리를 볼 수 있다.')
    s.natural('우리가 주차장에 들어서자 많은 사람들이 몰려 있는 것이 보인다.')
    s.cl('subordinate', 'As', subj='we', verbs=['pull'], marker='As')
    s.cl('main', 'we', subj='we', verbs=['can', 'see'], occ=1)
    s.g('As', 'as S′ V′', 'S′(이/가) V′할 때')
    s.g('we', 'we', '우리가', referent_ko='Alyssa, Garrett, Basil 삼촌')
    s.g('pull|into', 'pull into', '(차를 몰고) ~에 들어서다')
    s.g('parking|lot', 'parking lot', '주차장')
    s.g('we', 'we', '우리는', referent_ko='Alyssa, Garrett, Basil 삼촌', at=s.text.index('we can'))
    f = s.g('can', 'can V', '~할 수 있다', kind='function', combines_with=[])
    se = s.g('see', 'see', '보다')
    link(f, se)
    s.g('crowd', 'crowd', '(모여 있는) 사람들, 군중', star=W['crowd'])
    s.hint('[As we pull]', '[우리[Alyssa 일행]가 들어설 때]', span='As we pull', label='시간 접속사 as',
           links=[(['As'], ['가', '때'])], refs=[('we', '우리', '[Alyssa 일행]')],
           meaning='우리가 (주차장에) 들어설 때',
           explanation='시간의 접속사 as(~할 때). S′ we, V′ pull까지 표시하고 into the parking lot은 제외. pull into는 차를 몰고 어떤 곳에 들어서는 것.')
    s.review = ('문두 부사절 As we pull into the parking lot(시간) + 주절 we can see the crowd. 접속사절 힌트 1개. '
                'can V는 기능/낱말 분리. 관계사·수동 없음.')
    out.append(s)

    # ---------------- s13 ----------------
    s = S('s13', T['s13'])
    s.ch('“You two go in.', '“너희 둘은 들어가.')
    s.natural('“너희 둘은 먼저 들어가.')
    s.cl('imperative', 'You', subj='You two', verbs=['go'])
    s.g('two', 'two', '둘')
    s.g('go|in', 'go in', '들어가다')
    s.review = ('주어 You two가 드러난 명령문(S: You two, V: go — 실제 주어가 있으므로 지우지 않음). 단독 you 각주 제외. '
                '인용문 안의 마침표에서 문장을 나눔(다음 s14로 인용 계속). 절 연결·수동 없음 → 힌트 없음.')
    out.append(s)

    # ---------------- s14 ----------------
    s = S('s14', T['s14'])
    s.ch('I’ll meet you inside,”', '내가 너희를 안에서 만날게,”')
    s.ch('Uncle Basil says.', 'Basil 삼촌이 말한다.')
    s.natural('안에서 만나자.” Basil 삼촌이 말한다.')
    s.cl_spans('main', 0, subj=s.at('I'), verbs=[s.at('’ll'), s.at('meet')])
    s.cl('main', 'Uncle', subj='Uncle Basil', verbs=['says'])
    s.g('I’ll', 'I’ll', '나는 ~할 것이다 (= I will)', referent_ko='Basil 삼촌')
    s.g('meet', 'meet', '만나다')
    s.g('inside', 'inside', '안에서')
    s.g('says', 'say', '말하다', verb_form=v3(s, 'says', 'say', 'Uncle Basil'))
    s.review = ('앞 s13에서 이어지는 인용의 마지막 조각 I’ll meet you inside(’ll = will) + 전달절 Uncle Basil says. '
                '인용 속 I는 Basil 삼촌. Uncle Basil은 s10에서 제공한 고유명사 반복. 절 연결·수동 없음 → 힌트 없음.')
    out.append(s)

    # ---------------- s15 ----------------
    s = S('s15', T['s15'], key=True)
    s.ch('Inside', '안은')
    s.ch('it’s like Black Friday', '블랙 프라이데이 같다')
    s.ch('at its worst', '최악일 때의')
    s.ch('— but today', '— 하지만 오늘')
    s.ch('it’s not televisions and video games', '텔레비전과 비디오 게임이 아니다')
    s.ch('people are after.', '사람들이 찾고 있는 것은.')
    s.natural('매장 안은 최악의 블랙 프라이데이 같다. 하지만 오늘 사람들이 찾는 것은 텔레비전이나 비디오 게임이 아니다.')
    first = s.at('it’s')
    s.cl_spans('main', first[0], subj=[first[0], first[0] + 2], verbs=[[first[0] + 2, first[1]]],
               readings=[{'span': [first[0] + 2, first[1]], 'expanded': 'is'}])
    second = s.at('it’s', occ=1)
    s.cl_spans('main', s.at('but')[0], subj=[second[0], second[0] + 2], verbs=[[second[0] + 2, second[1]]],
               marker='but', readings=[{'span': [second[0] + 2, second[1]], 'expanded': 'is'}])
    s.cl('subordinate', 'people', subj='people', verbs=['are'], marker='that', omitted=True)
    s.g('Inside', 'inside', '안은, 안에서는')
    s.g('it’s|like', 'it’s like', '(상황이) ~와 같다 (it’s = it is)')
    s.g('Black|Friday', 'Black Friday', '블랙 프라이데이 (미국의 대규모 할인 행사일로, 매장이 몹시 붐빔)', proper=True)
    s.g('at|its|worst', 'at its worst', '가장 심할 때의, 최악일 때의', referent_ko='its = 블랙 프라이데이의')
    s.g('today', 'today', '오늘은')
    s.g('it’s|not', 'it’s not A (that) S′ V′', 'S′(이/가) V′하는 것은 A가 아니다 (it’s = it is)', at=second[0])
    s.g('televisions', 'televisions', '텔레비전들')
    s.g('video|games', 'video games', '비디오 게임들')
    s.g('people', 'people', '사람들')
    s.g('are|after', 'be after', '~을 찾다, 구하려 하다')
    s.brk('at', 'postnominal-preposition', 'at its worst는 앞 명사 Black Friday를 뒤에서 꾸며 ‘최악일 때의 블랙 프라이데이’를 나타내는 전치사구')
    s.hint('it’s not televisions and video games [(that) people are after]',
           '[사람들이 찾는] 것은 텔레비전과 비디오 게임이 아니다',
           span='it’s not televisions and video games people are after', label='강조구문의 관계사 that 생략',
           display_mode='omitted-relative', omitted_relative='that', links=[(['that'], ['이', '는'])],
           meaning='사람들이 찾는 것은 텔레비전과 비디오 게임이 아니다',
           explanation='It is not A that S′ V′ 강조구문: 강조 대상 A = televisions and video games, that 뒤 S′ people, V′ are (after). '
                       'that이 생략되어 있어 표시에서만 (that)을 보충. be after(~을 찾다)의 대상이 A. It~that 틀을 유지하고 V′ are에 뜻을 잡는 after까지 표시.')
    s.review = ('두 절이 but으로 연결: ① Inside it’s like Black Friday at its worst(상황의 it, ’s = is; at its worst가 Black Friday를 후치수식) '
                '② today it’s not televisions and video games (that) people are after(It is not A that … 강조구문, that 생략, ’s = is). '
                'S/V는 it / ’s 두 주절과 생략 that절(S′ people, V′ are). 강조구문의 생략 that은 관계사처럼 A를 받아 be after의 대상이 되므로 omitted-relative 힌트 1개. '
                'people are after = 사람들이 찾는 것. 수동 없음.')
    out.append(s)

    # ---------------- s16 ----------------
    s = S('s16', T['s16'])
    s.ch('What I see', '내가 보는 것은')
    s.ch('in the carts', '카트들 안에서')
    s.ch('in the checkout line', '계산대 줄에 서 있는')
    s.ch('are mostly water bottles.', '대부분 생수병들이다.')
    s.natural('계산대 줄에 선 카트들 안에 보이는 것은 대부분 생수병이다.')
    s.cl('main', 'What', subj='What I see in the carts in the checkout line', verbs=['are'])
    s.cl('subordinate', 'I', subj='I', verbs=['see'], marker='What')
    rel = s.g('What', 'what S′ V′', 'S′(이/가) V′하는 것 (관계대명사)')
    s.g('I', 'I', '내가', referent_ko='Alyssa')
    s.g('see', 'see', '보다')
    s.g('in', 'in', '~ 안에서')
    s.g('carts', 'carts', '카트들')
    s.g('in', 'in', '~에 (서 있는)', at=s.text.index('in the checkout'))
    s.g('checkout|line', 'checkout line', '계산대 줄', star=W['checkout'])
    s.g('are', 'are', '~이다')
    s.g('mostly', 'mostly', '대부분')
    s.g('water|bottles', 'water bottles', '생수병들, 물병들')
    s.brk('in', 'postnominal-preposition', 'in the checkout line은 앞 명사 the carts를 뒤에서 꾸미는 전치사구',
          after=s.text.index('in the checkout'))
    s.hint('[What I see]', '[내[Alyssa]가 보는 것]', span='What I see', label='관계대명사 what',
           links=[(['What'], ['가', '는 것'])], refs=[('I', '내', '[Alyssa]')],
           meaning='내가 보는 것',
           explanation='선행사를 포함한 관계대명사 what절(What I see in the carts in the checkout line)이 문장 전체의 주어. what은 see의 목적어. S′ I, V′ see까지 표시하고 in 이하 장소 부사구는 제외. 보어 water bottles가 복수라 동사 are.')
    s.relative_ids = [rel['id']]
    s.review = ('관계대명사 what절 주어(명사절 주어라 S/V 주어 전체 유지) + V are + 보어 mostly water bottles. in the carts는 see의 장소, '
                'in the checkout line은 the carts를 꾸미는 후치 전치사구(in 앞에서 끊음). 필수 관계사 힌트 1개. 수동 없음.')
    out.append(s)

    # ---------------- s17 ----------------
    s = S('s17', T['s17'])
    s.ch('The essentials', '그 필수품들')
    s.ch('of life.', '삶의.')
    s.natural('삶에 꼭 필요한 필수품들이다.')
    verbless(s, 's16', T['s16'], '앞 16번 문장의 water bottles를 다시 풀어 말하는 명사구 조각(동격). 유한동사가 없어 S/V 줄을 생략한다.')
    s.g('essentials', 'essentials', '필수품들, 꼭 필요한 것들', star=W['essentials'])
    s.g('of', 'of', '~의')
    s.g('life', 'life', '삶, 생활')
    s.brk('of', 'postnominal-preposition', 'of life는 앞 명사 The essentials를 뒤에서 꾸미는 전치사구')
    s.review = ('유한동사가 없는 명사구 조각(s16 water bottles의 동격 설명). 2026-09-28 사용자 결정으로 S/V 줄과 안내문 생략(verbless-fragment). '
                'of life 후치수식(of 앞에서 끊음). 절 연결·관계사·수동 없음 → 힌트 없음.')
    out.append(s)
    return out


UNIT = {
    'id': 'u1', 'source_id': 'src', 'paragraph_ids': ['p01', 'p02', 'p03', 'p04', 'p05', 'p06', 'p07', 'p08'],
    'sentence_ids': [f's{n:02d}' for n in range(1, 18)],
    'today_words': [
        {'id': W['tap'], 'text': 'tap', 'meaning_ko': '수도꼭지'},
        {'id': W['crisis'], 'text': 'crisis', 'meaning_ko': '위기'},
        {'id': W['drought'], 'text': 'drought', 'meaning_ko': '가뭄'},
        {'id': W['stage'], 'text': 'stage', 'meaning_ko': '단계'},
        {'id': W['running'], 'text': 'running water', 'meaning_ko': '수돗물'},
        {'id': W['crowd'], 'text': 'crowd', 'meaning_ko': '(모여 있는) 사람들, 군중'},
        {'id': W['checkout'], 'text': 'checkout line', 'meaning_ko': '계산대 줄'},
        {'id': W['essentials'], 'text': 'essentials', 'meaning_ko': '필수품들, 꼭 필요한 것들'},
    ],
}


def analysis(_):
    return {
        'heading_kind': '제목',
        'title_or_topic_en': 'The Day the Tap Went Silent',
        'title_or_topic_ko': '수도꼭지가 조용해진 날',
        'intent_ko': '오랜 가뭄으로 마침내 수돗물까지 끊기자 Alyssa 가족이 물을 구하러 쇼핑몰로 가는 장면이다. 사람들이 물건 대신 생수만 찾는 모습으로 물이 생명의 필수품이 된 위기 상황을 보여 준다.',
        'flow': [
            {'sentence_ids': ['s01', 's02', 's03', 's04', 's05'], 'label': '발단',
             'text_ko': '주방 수도꼭지가 이상한 소리를 내더니 물이 끊긴다. Alyssa가 엄마를 부르지만 엄마는 조용히 하라고 한다.'},
            {'sentence_ids': ['s06', 's07', 's08', 's09'], 'label': '상황 설명',
             'text_ko': 'TV 뉴스는 가뭄을 ‘물 공급 위기’라고 부르며 전하고 있다. 위기가 새 단계에 접어들어 이제 수돗물이 나오지 않는다.'},
            {'sentence_ids': ['s10', 's11', 's12', 's13', 's14'], 'label': '전개',
             'text_ko': 'Basil 삼촌을 따라 Alyssa와 Garrett은 쇼핑몰로 간다. 주차장에는 사람들이 몰려 있고, 삼촌은 아이들에게 먼저 들어가라고 한다.'},
            {'sentence_ids': ['s15', 's16', 's17'], 'label': '장면 묘사',
             'text_ko': '매장 안은 최악의 블랙 프라이데이처럼 붐빈다. 그러나 사람들이 카트에 담은 것은 전자 제품이 아니라 대부분 생수, 곧 삶의 필수품이다.'},
        ],
        'easy_explanations': [
            {'sentence_id': 's02', 'explanatory_sentences': [
                '2번 문장은 1번에서 이상한 소리를 낸 수도꼭지를 사람처럼 표현한다.',
                '물이 거의 나오지 않는 수도꼭지는 공기와 물이 섞여 콜록거리는 소리를 낸다.',
                '글쓴이는 이 소리를 사람이 기침하는 모습에 빗댔다.',
                '물이 곧 끊길 것이라는 신호를 생생하게 보여 주는 문장이다.']},
            {'sentence_id': 's07', 'explanatory_sentences': [
                '7번 문장은 6번 뉴스에 나온 ‘물 공급 위기’라는 말이 어디서 나왔는지 알려 준다.',
                '가뭄이 너무 오래 이어져서 사람들은 ‘가뭄’이라는 말을 듣는 데 지쳐 버렸다.',
                '그래서 언론은 같은 가뭄을 ‘물 공급 위기’라는 새 이름으로 부르기 시작했다.',
                '이름만 바뀌었을 뿐 가뭄은 계속되고 있다는 뜻이다.']},
            {'sentence_id': 's15', 'explanatory_sentences': [
                '15번 문장은 쇼핑몰 안의 모습을 보여 준다.',
                '블랙 프라이데이는 미국에서 큰 할인 행사가 열리는 날이다.',
                '이날 매장은 싼 물건을 사려는 사람들로 몹시 붐빈다.',
                '오늘 매장은 그날처럼 붐비지만 사람들이 찾는 것은 텔레비전이나 게임기가 아니다.',
                '다음 16번 문장에서 사람들이 찾는 것이 물이라는 것이 드러난다.']},
        ],
        'grammar_points': [
            {'id': 'u1-gp1', 'sentence_id': 's06', 'span': 'the TV, where a news anchor is talking about the “flow crisis.”',
             'title': '콤마 + where S′ V′: 그리고 거기에서 S′가 V′하다', 'formula_key': ', where S′ V′',
             'explanation': '공식: 명사, where S′ V′ — 명사, 그리고 거기에서 S′(이/가) V′하다. 앞 명사 = the TV(TV), where = 그리고 거기에서(TV에서), '
                            'S′ = a news anchor(뉴스 앵커), V′ = is talking(이야기하고 있다), about the “flow crisis” = ‘물 공급 위기’에 관해. '
                            '→ TV, 그리고 거기에서 뉴스 앵커가 ‘물 공급 위기’에 관해 이야기하고 있다. 콤마 뒤 where는 앞 명사를 받아 설명을 이어 준다.',
             'practice': {'span': 'the TV, where a news anchor is talking about the “flow crisis.”',
                          'formula_support': {'en': ', where S′ V′', 'ko': '그리고 거기에서 S′(이/가) V′하다'},
                          'support': [('s06', 'TV'), ('s06', 'news'), ('s06', 'anchor'), ('s06', 'be V-ing', 1),
                                      ('s06', 'talk'), ('s06', 'about'), ('s06', 'flow crisis')],
                          'answer_ko': 'TV, 그리고 거기에서 뉴스 앵커가 ‘물 공급 위기’에 관해 이야기하고 있다'}},
            {'id': 'u1-gp2', 'sentence_id': 's07', 'span': 'This is what the media has been calling the drought',
             'title': 'what S′ V′: S′가 V′하는 것', 'formula_key': 'what S′ V′',
             'explanation': '공식: what S′ V′ — S′(이/가) V′하는 것. S′ = the media(언론), V′ = has been calling(계속 불러 오고 있다; call A B = A를 B라고 부르다), '
                            'A = the drought(가뭄), B = what(부르는 것, 곧 이름). → 언론이 가뭄을 계속 불러 온 것(이름). '
                            '앞의 This is(이것은 ~이다)와 합치면 ‘이것은 언론이 가뭄을 계속 불러 온 이름이다’가 된다.',
             'practice': {'span': 'what the media has been calling the drought',
                          'formula_support': {'en': 'what S′ V′', 'ko': 'S′(이/가) V′하는 것'},
                          'support': [('s07', 'media'), ('s07', 'has been calling A B'), ('s07', 'drought')],
                          'answer_ko': '언론이 가뭄을 계속 불러 온 것'}},
            {'id': 'u1-gp3', 'sentence_id': 's15', 'span': 'today it’s not televisions and video games people are after',
             'title': 'It is not A that S′ V′: S′가 V′하는 것은 A가 아니다', 'formula_key': 'it is not A that S′ V′',
             'explanation': '공식: It is not A (that) S′ V′ — S′(이/가) V′하는 것은 A가 아니다. A = televisions and video games(텔레비전과 비디오 게임), '
                            'that = 생략됨, S′ = people(사람들), V′ = are after(찾고 있다; be after = ~을 찾다). '
                            '→ 사람들이 찾는 것은 텔레비전과 비디오 게임이 아니다. 앞의 today(오늘)와 합치면 ‘오늘 사람들이 찾는 것은 텔레비전과 비디오 게임이 아니다’.',
             'practice': {'span': 'it’s not televisions and video games people are after',
                          'formula_support': {'en': 'it is not A that S′ V′', 'ko': 'S′(이/가) V′하는 것은 A가 아니다'},
                          'support': [('s15', 'televisions'), ('s15', 'video games'), ('s15', 'people'), ('s15', 'be after')],
                          'answer_ko': '사람들이 찾는 것은 텔레비전과 비디오 게임이 아니다'}},
        ],
        'formula_routes': [],
        'relations': [
            {'head': {'id': 'u1-r1h', 'text': 'strange', 'meaning_ko': '이상한'},
             'synonym': {'id': 'u1-r1s', 'text': 'odd', 'meaning_ko': '이상한, 특이한'},
             'antonym': {'id': 'u1-r1a', 'text': 'normal', 'meaning_ko': '평범한, 정상적인'}},
            {'head': {'id': 'u1-r2h', 'text': 'silent', 'meaning_ko': '조용한, 소리 없는'},
             'synonym': {'id': 'u1-r2s', 'text': 'quiet', 'meaning_ko': '조용한'},
             'antonym': {'id': 'u1-r2a', 'text': 'noisy', 'meaning_ko': '시끄러운'}},
            {'head': {'id': 'u1-r3h', 'text': 'essentials', 'meaning_ko': '필수품들'},
             'synonym': {'id': 'u1-r3s', 'text': 'necessities', 'meaning_ko': '필수품들, 꼭 필요한 것들'},
             'antonym': {'id': 'u1-r3a', 'text': 'luxuries', 'meaning_ko': '사치품들'}},
        ],
    }


def workbook():
    return {
        'relation_order': ['u1-r2s', 'u1-r3a', 'u1-r1h', 'u1-r2a', 'u1-r3s', 'u1-r1s', 'u1-r2h', 'u1-r1a', 'u1-r3h'],
        'key_sentence_ids': ['s07', 's15'],
        'question_id': 'Q01',
        'syntax_point_ids': ['u1-gp1', 'u1-gp2', 'u1-gp3'],
    }
