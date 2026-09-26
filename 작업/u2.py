"""공통 단위 2: Classifying Galaxies (s07~s33, 단락 p02~p05; 짧은 단락이 있어 소제목 전체 묶음)."""
from author import S, link

W = {'classify': 'u2-w1', 'suggest': 'u2-w2', 'individually': 'u2-w3', 'complain': 'u2-w4',
     'tutorial': 'u2-w5', 'effectively': 'u2-w6', 'participants': 'u2-w7', 'platforms': 'u2-w8'}


def pp(usage, s, word, lemma, fid=None, occ_after=0):
    row = {'usage': usage, 'source_span': s.span_of(word, occ_after), 'lemma': lemma}
    if fid:
        row['function_gloss_id'] = fid
    return row


def sentences(T):
    out = []

    # ---------------- s07 ----------------
    s = S('s07', T['s07'])
    s.ch('Kevin Schawinski was a young astronomy researcher', 'Kevin Schawinski는 젊은 천문학 연구원이었다')
    s.ch('studying black holes and the evolution', '블랙홀과 진화를 연구하는')
    s.ch('of galaxies', '은하의')
    s.ch('at the University of Oxford.', '옥스퍼드 대학교에서.')
    s.natural('Kevin Schawinski는 옥스퍼드 대학교에서 블랙홀과 은하의 진화를 연구하는 젊은 천문학 연구원이었다.')
    s.cl('main', 'Kevin', subj='Kevin Schawinski', verbs=['was'])
    s.g('Kevin|Schawinski', 'Kevin Schawinski', '케빈 샤빈스키 (천문학 연구원)', proper=True)
    s.g('was', 'was', '~이었다 (be의 과거)', verb_form=pp('irregular-past', s, 'was', 'be'))
    s.g('young', 'young', '젊은')
    s.g('astronomy', 'astronomy', '천문학')
    s.g('researcher', 'researcher', '연구원')
    f = s.g('studying', 'V-ing', '~하는', kind='function', combines_with=[])
    st = s.g('studying', 'study', '연구하다', same=True, verb_form=pp('ing', s, 'studying', 'study'))
    link(f, st)
    s.g('black|holes', 'black holes', '블랙홀들')
    s.g('evolution', 'evolution', '진화')
    s.g('of', 'of', '~의')
    s.g('galaxies', 'galaxies', '은하들')
    s.g('at', 'at', '~에서')
    s.g('University|of|Oxford', 'the University of Oxford', '옥스퍼드 대학교 (영국의 대학)', proper=True)
    s.hint('a young astronomy researcher [studying black holes and the evolution of galaxies]',
           '[블랙홀과 은하의 진화를 연구하는] 젊은 천문학 연구원',
           span='a young astronomy researcher studying black holes and the evolution of galaxies',
           label='현재분사 후치수식', links=[(['ing'], ['는'])],
           meaning='블랙홀과 은하의 진화를 연구하는 젊은 천문학 연구원',
           explanation='현재분사 studying이 목적어 black holes and the evolution of galaxies를 거느리고 앞 명사 researcher를 뒤에서 꾸민다.')
    s.brk('of', 'postnominal-preposition', 'of galaxies는 앞 명사 the evolution을 꾸미는 전치사구', after=s.text.index('evolution'))
    s.review = ('단일 주절. studying 이하는 researcher를 꾸미는 현재분사구 → 힌트. the evolution of galaxies의 of 앞에서 끊음. '
                'at the University of Oxford는 장소 부사구(연구하는 곳)로 고유명사 내부 of는 끊지 않음. 수동·완료 없음.')
    out.append(s)

    # ---------------- s08 ----------------
    s = S('s08', T['s08'])
    s.ch('This might sound exciting,', '이것은 흥미롭게 들릴지도 모른다,')
    s.ch('but his job there was dull and time-consuming.', '하지만 그곳에서 그의 일은 따분하고 시간이 많이 걸렸다.')
    s.natural('이것이 흥미롭게 들릴지도 모르지만, 그곳에서 그의 일은 따분하고 시간이 많이 걸리는 일이었다.')
    s.cl('main', 'This', subj='This', verbs=['might', 'sound'])
    s.cl('main', 'his', subj='his job there', verbs=['was'], marker='but', disp='his job',
         disp_review='중심명사 job까지 표시하고 뒤에서 꾸미는 부사 there(그곳에서)는 제외')
    s.g('This', 'this', '이것은', referent_ko='옥스퍼드에서 블랙홀과 은하를 연구하는 천문학 연구원이라는 것')
    f = s.g('might', 'might V', '~할지도 모른다', kind='function', combines_with=[])
    so = s.g('sound', 'sound', '~하게 들리다')
    link(f, so)
    s.g('exciting', 'exciting', '흥미진진한, 신나는')
    s.g('his', 'his', '그의', referent_ko='Kevin Schawinski')
    s.g('job', 'job', '일, 직업')
    s.g('there', 'there', '그곳에서', referent_ko='옥스퍼드 대학교')
    s.g('was', 'was', '~이었다 (be의 과거)', verb_form=pp('irregular-past', s, 'was', 'be'))
    s.g('dull', 'dull', '따분한, 지루한')
    s.g('time-consuming', 'time-consuming', '시간이 많이 걸리는')
    s.review = '두 독립절(but). might V 추측, sound+형용사 보어. 접속사절·관계사·수동 없음 → 힌트 없음. 주어 his job there는 표시에서 there 제외.'
    out.append(s)

    # ---------------- s09 ----------------
    s = S('s09', T['s09'])
    s.ch('He had to classify around one million images', '그는 약 백만 장의 이미지를 분류해야 했다')
    s.ch('of galaxies', '은하의')
    s.ch('according to their shape.', '그것들의 모양에 따라.')
    s.natural('그는 약 백만 장의 은하 이미지를 모양에 따라 분류해야 했다.')
    s.cl('main', 'He', subj='He', verbs=['had to classify'])
    s.g('He', 'he', '그는', referent_ko='Kevin Schawinski')
    f = s.g('had|to', 'had to V', '~해야 했다', kind='function', combines_with=[])
    c = s.g('classify', 'classify', '분류하다', star=W['classify'])
    link(f, c)
    s.g('around', 'around', '약')
    s.g('one|million', 'one million', '백만')
    s.g('images', 'images', '이미지들, 사진들')
    s.g('of', 'of', '~의')
    s.g('galaxies', 'galaxies', '은하들')
    s.g('according|to', 'according to', '~에 따라')
    s.g('their', 'their', '그것들의', referent_ko='은하들')
    s.g('shape', 'shape', '모양')
    s.brk('of', 'postnominal-preposition', 'of galaxies는 앞 명사 images를 꾸미는 전치사구')
    s.review = '단일 주절, had to V 의무. 후치수식 of 앞에서 끊음. 관계사·접속사절·수동 없음 → 힌트 없음.'
    out.append(s)

    # ---------------- s10 ----------------
    s = S('s10', T['s10'])
    s.ch('Since they all looked similar', '그것들이 모두 비슷해 보였지만')
    s.ch('but were actually shaped slightly differently,', '실제로는 조금씩 다른 모양이었기 때문에,')
    s.ch('the best way to do this', '이것을 할 가장 좋은 방법은')
    s.ch('was to sort them', '그것들을 분류하는 것이었다')
    s.ch('while looking at each one individually.', '하나하나를 개별적으로 보면서.')
    s.natural('그것들은 모두 비슷해 보였지만 실제로는 모양이 조금씩 달랐기 때문에, 이 일을 하는 가장 좋은 방법은 하나하나를 개별적으로 보면서 분류하는 것이었다.')
    s.cl('subordinate', 'Since', subj='they all', verbs=['looked', 'but', 'were', 'shaped'], marker='Since')
    s.cl('main', 'the', subj='the best way to do this', verbs=['was'], disp='the best way',
         disp_review='중심명사 way까지 표시하고 뒤에서 꾸미는 to do this는 제외')
    s.g('Since', 'since S′ V′', 'S′(이/가) V′하기 때문에')
    s.g('they', 'they', '그것들은', referent_ko='은하 이미지들')
    s.g('all', 'all', '모두')
    s.g('looked', 'look', '~해 보이다', verb_form=pp('regular-past', s, 'looked', 'look'))
    s.g('similar', 'similar', '비슷한')
    f = s.g('were', 'be p.p.', '~되다', kind='function', combines_with=[])
    s.g('actually', 'actually', '실제로는')
    sh = s.g('shaped', 'shaped', '(~한) 모양으로 형성된', verb_form=pp('passive-participle', s, 'shaped', 'shape', f['id']))
    link(f, sh)
    s.g('slightly', 'slightly', '약간, 조금')
    s.g('differently', 'differently', '다르게')
    s.g('best', 'best', '가장 좋은 (good의 최상급)')
    s.g('way', 'way', '방법')
    f2 = s.g('to', 'to V', '~할', kind='function', combines_with=[])
    d = s.g('do', 'do', '하다')
    link(f2, d)
    s.g('this', 'this', '이것을', referent_ko='은하 이미지를 모양에 따라 분류하는 일', at=s.text.index('do this') + 3)
    s.g('was', 'was', '~이었다 (be의 과거)', verb_form=pp('irregular-past', s, 'was', 'be'))
    f3 = s.g('to', 'to V', '~하는 것', kind='function', combines_with=[], at=s.text.index('to sort'))
    so = s.g('sort', 'sort', '분류하다, 정리하다')
    link(f3, so)
    s.g('them', 'them', '그것들을', referent_ko='은하 이미지들')
    f4 = s.g('while', 'while V-ing', '~하면서', kind='function', combines_with=[])
    lk = s.g('looking|at', 'look at', '~을 보다', verb_form=pp('ing', s, 'looking', 'look'))
    link(f4, lk)
    s.g('each|one', 'each one', '각각, 하나하나')
    s.g('individually', 'individually', '개별적으로, 하나씩', star=W['individually'])
    s.hint('the best way [to do this]', '[이것[이미지를 모양별로 분류하는 일]을 할] 가장 좋은 방법',
           span='the best way to do this', label='to부정사 후치수식', links=[(['to'], ['할'])],
           refs=[('this', '이것', '[이미지를 모양별로 분류하는 일]')],
           meaning='이것을 할 가장 좋은 방법',
           explanation='to do this가 앞 명사 the best way를 뒤에서 꾸며 ‘~할 방법’. this는 앞 문장의 분류 작업을 가리킨다.')
    s.hint('[while looking at]', '[보면서]', span='while looking at each one individually',
           label='접속사 while + V-ing', links=[(['while', 'ing'], ['면서'])],
           meaning='하나하나를 개별적으로 보면서',
           explanation='접속사 while 뒤에 주어 없이 V-ing가 와서 ‘~하면서’의 동시 동작을 나타낸다. 목적어 each one은 표시에서 제외.')
    s.review = ('Since 이유 부사절 안에서 looked similar와 were actually shaped …가 but으로 병렬(같은 주어 they). '
                'Since 절은 각주 틀 S′(이/가) V′하기 때문에로 지원하고, 힌트는 문장당 2개 한도에서 to부정사 후치수식(way to do this)과 while+V-ing를 선정. '
                'to sort them은 was의 보어(~하는 것). 수동 were shaped는 이미 힌트가 있어 결합 힌트 대신 단위 분석 be p.p. 대표(u2-gp4)에 연결.')
    out.append(s)

    # ---------------- s11 ----------------
    s = S('s11', T['s11'])
    s.ch('Of course,', '물론,')
    s.ch('this would require a tremendous amount of time.', '이것은 엄청난 양의 시간을 필요로 할 것이었다.')
    s.natural('물론, 이것은 엄청난 시간이 필요할 것이었다.')
    s.cl('main', 'this', subj='this', verbs=['would', 'require'])
    s.g('Of|course', 'of course', '물론')
    s.g('this', 'this', '이것은', referent_ko='은하 이미지를 하나하나 보면서 분류하는 일')
    f = s.g('would', 'would V', '~할 것이다', kind='function', combines_with=[])
    r = s.g('require', 'require', '필요로 하다')
    link(f, r)
    q = s.g('a tremendous amount of', 'a tremendous amount of', '엄청난 양의')
    s.g('time', 'time', '시간', at=s.text.index('of time') + 3)
    s.prot('a tremendous amount of', 'quantity-kind-of', '수량 표현 a tremendous amount of가 뒤 명사 time 앞에서 ‘엄청난 양의’로 같은 어순 대응', gloss=q)
    s.review = '단일 주절, would V. a tremendous amount of는 같은 어순 ~의 수량 표현으로 한 각주·보호 범위. 힌트 불필요, 수동 없음.'
    out.append(s)

    # ---------------- s12 ----------------
    s = S('s12', T['s12'])
    s.ch('It took Schawinski a whole week', 'Schawinski가 꼬박 일주일이 걸렸다')
    s.ch('to classify just 50,000 galaxies.', '고작 5만 개의 은하를 분류하는 데.')
    s.natural('Schawinski가 고작 5만 개의 은하를 분류하는 데 꼬박 일주일이 걸렸다.')
    s.cl('main', 'It', subj='It', verbs=['took'])
    s.g('It|took|to', 'It takes A B to V', 'A(이/가) ~하는 데 B(시간)가 걸리다 (took은 take의 과거)')
    s.g('whole', 'whole', '꼬박, 전체의')
    s.g('week', 'week', '일주일')
    s.g('classify', 'classify', '분류하다', star=W['classify'])
    s.g('just', 'just', '고작, 겨우')
    s.g('galaxies', 'galaxies', '은하들')
    s.hint('It took Schawinski a whole week [to classify]', 'Schawinski가 [분류하는 데] 꼬박 일주일이 걸렸다',
           span='It took Schawinski a whole week to classify', label='It takes A B to V 구문',
           links=[(['It took', ('to', 1)], ['가', '는 데'])],
           meaning='Schawinski가 분류하는 데 꼬박 일주일이 걸렸다',
           explanation='It takes A B to V: A(Schawinski)가 ~하는 데 B(a whole week)가 걸리다. It은 뜻이 없는 형식상 주어이고 실제 내용은 to classify …이다. 목적어 galaxies는 표시에서 제외.')
    s.review = 'It takes A B to V 구문(It은 가주어, to classify가 진주어). 힌트 1개. Schawinski는 앞 문장 첫 등장 고유명사의 반복. 수동 없음.'
    out.append(s)

    # ---------------- s13 ----------------
    s = S('s13', T['s13'])
    s.ch('He thought,', '그는 생각했다,')
    s.ch('“But what about the remaining 950,000?”', '“하지만 남아 있는 95만 개는 어쩌지?”')
    s.natural('그는 ‘하지만 남아 있는 95만 개는 어쩌지?’라고 생각했다.')
    s.cl('main', 'He', subj='He', verbs=['thought'])
    s.g('He', 'he', '그는', referent_ko='Kevin Schawinski')
    s.g('thought', 'thought', '생각했다 (think의 과거)', verb_form=pp('irregular-past', s, 'thought', 'think'))
    s.g('what|about', 'what about ~?', '~은 어쩌지?, ~은 어떻게 하지?')
    s.g('remaining', 'remaining', '남아 있는, 나머지의')
    s.review = '주절 + 직접 인용(동사 없는 의문 표현 what about ~?). 인용 안 But은 일반 연결어. 힌트 불필요.'
    out.append(s)

    # ---------------- s14 ----------------
    s = S('s14', T['s14'])
    s.ch('One evening after work,', '어느 날 저녁 퇴근 후에,')
    s.ch('Schawinski met a friend', 'Schawinski는 한 친구를 만났다')
    s.ch('named Chris Lintott', 'Chris Lintott이라는 이름의')
    s.ch('and complained about the situation.', '그리고 그 상황에 대해 불평했다.')
    s.natural('어느 날 퇴근 후 저녁에, Schawinski는 Chris Lintott이라는 친구를 만나 그 상황에 대해 불평했다.')
    s.cl('main', 'Schawinski', subj='Schawinski', verbs=['met', 'and', 'complained'])
    s.g('One|evening', 'one evening', '어느 날 저녁')
    s.g('after|work', 'after work', '퇴근 후에')
    s.g('met', 'met', '만났다 (meet의 과거)', verb_form=pp('irregular-past', s, 'met', 'meet'))
    s.g('friend', 'friend', '친구')
    nm = s.g('named', 'named', '(~라는) 이름의', verb_form=pp('past-participle', s, 'named', 'name'))
    s.g('Chris|Lintott', 'Chris Lintott', '크리스 린톳 (Schawinski의 친구)', proper=True)
    s.g('complained', 'complain', '불평하다', star=W['complain'],
        verb_form=pp('regular-past', s, 'complained', 'complain'))
    s.g('about', 'about', '~에 대해')
    s.g('situation', 'situation', '상황')
    s.hint('a friend [named Chris Lintott]', '[Chris Lintott이라는 이름의] 친구', span='a friend named Chris Lintott',
           label='과거분사 후치수식', links=[(['named'], ['이름의'])], participle_focus_gloss_id=nm['id'],
           meaning='Chris Lintott이라는 이름의 친구',
           explanation='과거분사 named가 이끄는 구가 앞 명사 a friend를 뒤에서 꾸민다.')
    s.review = '주어 Schawinski의 병렬 동사 met and complained. named Chris Lintott은 a friend 후치수식 → 힌트. 수동 없음.'
    out.append(s)

    # ---------------- s15 ----------------
    s = S('s15', T['s15'])
    s.ch('Lintott suggested', 'Lintott은 제안했다')
    s.ch('that he turn to the Internet', '그가 인터넷에 의지해야 한다고')
    s.ch('to ask other people for help.', '다른 사람들에게 도움을 요청하기 위해.')
    s.natural('Lintott은 그에게 다른 사람들에게 도움을 요청하기 위해 인터넷에 의지해 보라고 제안했다.')
    s.cl('main', 'Lintott', subj='Lintott', verbs=['suggested'])
    s.cl('subordinate', 'that', subj='he', verbs=['turn'], marker='that')
    s.g('suggested', 'suggest', '제안하다', star=W['suggest'], verb_form=pp('regular-past', s, 'suggested', 'suggest'))
    s.g('that', 'that S′ (should) V′', 'S′(이/가) V′해야 한다고 (접속사)')
    s.g('he', 'he', '그가', referent_ko='Kevin Schawinski')
    s.g('turn|to', 'turn to', '~에 의지하다')
    s.g('Internet', 'the Internet', '인터넷')
    f = s.g('to', 'to V', '~하기 위해', kind='function', combines_with=[], at=s.text.index('to ask'))
    a = s.g('ask|for', 'ask A for B', 'A에게 B를 요청하다',
            verb_construction={'kind': 'verb-frame', 'verb_span': s.span_of('ask'), 'lemma': 'ask',
                               'link_spans': [s.span_of('for')], 'review_record': 'ask other people for help: A=other people, B=help.'})
    link(f, a)
    s.g('other', 'other', '다른')
    s.g('people', 'people', '사람들')
    s.g('help', 'help', '도움')
    s.hint('[that he turn]', '[그[Schawinski]가 의지해야 한다고]', span='that he turn',
           label='명사절 접속사 that', links=[(['that'], ['가', '야 한다고'])],
           refs=[('he', '그', '[Schawinski]')],
           meaning='그가 (인터넷에) 의지해야 한다고',
           explanation='suggest의 목적어 that절. 제안 동사 뒤라 (should) turn의 동사원형 turn이 쓰였다. S′ he, V′ turn까지만 표시하고 to the Internet은 제외.')
    s.review = ('suggest that S′ (should) V′: that절 동사가 원형 turn. 명사절 that 힌트. to ask …는 목적의 to부정사(각주로 지원). '
                'Lintott은 앞 문장 Chris Lintott의 반복. 수동 없음.')
    out.append(s)

    # ---------------- s16 ----------------
    s = S('s16', T['s16'])
    s.ch('Eventually,', '결국,')
    s.ch('the two men ended up launching', '그 두 남자는 시작하게 되었다')
    s.ch('a crowdsourced online project', '대중이 참여하는 온라인 프로젝트를')
    s.ch('known as Galaxy Zoo.', 'Galaxy Zoo라고 알려진.')
    s.natural('결국, 그 두 남자는 Galaxy Zoo라고 알려진, 대중이 참여하는(크라우드소싱) 온라인 프로젝트를 시작하게 되었다.')
    s.cl('main', 'the', subj='the two men', verbs=['ended up'])
    s.g('Eventually', 'eventually', '결국')
    s.g('two', 'two', '두')
    s.g('men', 'men', '남자들')
    s.g('ended|up', 'end up V-ing', '결국 ~하게 되다', verb_form=pp('regular-past', s, 'ended', 'end'))
    s.g('launching', 'launch', '시작하다, 개시하다', verb_form=pp('ing', s, 'launching', 'launch'))
    s.g('crowdsourced', 'crowdsourced', '대중이 참여하는(크라우드소싱 방식의)')
    s.g('online', 'online', '온라인의')
    s.g('project', 'project', '프로젝트')
    kn = s.g('known|as', 'known as', '(~라고) 알려진', verb_form=pp('past-participle', s, 'known', 'know'))
    s.g('Galaxy|Zoo', 'Galaxy Zoo', '갤럭시 주 (은하 분류 온라인 프로젝트 이름)', proper=True)
    s.hint('a crowdsourced online project [known as Galaxy Zoo]', '[Galaxy Zoo라고 알려진] 대중 참여 온라인 프로젝트',
           span='a crowdsourced online project known as Galaxy Zoo', label='과거분사 후치수식',
           links=[(['known'], ['알려진'])], participle_focus_gloss_id=kn['id'],
           meaning='Galaxy Zoo라고 알려진 대중 참여 온라인 프로젝트',
           explanation='과거분사 known이 이끄는 known as Galaxy Zoo가 앞 명사구 a crowdsourced online project를 꾸민다.')
    s.review = 'end up V-ing(결국 ~하게 되다), known as ~ 과거분사 후치수식 → 힌트. crowdsourced는 명사 앞 형용사. 수동 없음.'
    out.append(s)

    # ---------------- s17 ----------------
    s = S('s17', T['s17'])
    s.ch('The website was kept as simple as possible,', '그 웹사이트는 가능한 한 단순하게 유지되었다,')
    s.ch('with a very basic design', '매우 기본적인 디자인을 갖추고')
    s.ch('and an easy-to-use interface.', '그리고 사용하기 쉬운 인터페이스를 (갖추고).')
    s.natural('그 웹사이트는 매우 기본적인 디자인과 사용하기 쉬운 인터페이스를 갖추어 최대한 단순하게 유지되었다.')
    s.cl('main', 'The', subj='The website', verbs=['was', 'kept'])
    s.g('website', 'website', '웹사이트')
    f = s.g('was', 'be p.p.', '~되다', kind='function', combines_with=[])
    k = s.g('kept', 'kept', '유지된', verb_form=pp('passive-participle', s, 'kept', 'keep', f['id']))
    link(f, k)
    s.g('as|as|possible', 'as ~ as possible', '가능한 한 ~하게')
    s.g('simple', 'simple', '단순한')
    s.g('with', 'with', '~을 갖추고')
    s.g('very', 'very', '매우')
    s.g('basic', 'basic', '기본적인')
    s.g('design', 'design', '디자인')
    s.g('easy-to-use', 'easy-to-use', '사용하기 쉬운')
    s.g('interface', 'interface', '인터페이스(화면 구성)')
    s.hint('[as simple as possible]', '[가능한 한 단순하게]', span='as simple as possible',
           label='as ~ as possible 원급 구문', links=[(['as', ('as possible', 0)], ['가능한 한'])],
           meaning='가능한 한 단순하게',
           explanation='as + 형용사 + as possible: 가능한 한 ~하게. kept A 형용사(A를 ~하게 유지하다)의 수동이라 형용사 simple이 주어의 상태를 나타낸다.')
    s.review = ('수동 was kept + 보어 as simple as possible. 힌트는 as ~ as possible 원급 구문 1개. '
                '수동 was kept는 이미 힌트가 있어 결합 힌트를 추가하지 않고 단위 분석 be p.p. 대표 u2-gp4(바로 이 문장)로 연결. with 이하는 부대 상황.')
    out.append(s)

    # ---------------- s18 ----------------
    s = S('s18', T['s18'])
    s.ch('This allowed those', '이것은 사람들이')
    s.ch('who wanted to participate', '참여하기를 원했던')
    s.ch('to get started quickly.', '빨리 시작할 수 있게 해 주었다.')
    s.natural('이것은 참여하고 싶어 했던 사람들이 빨리 시작할 수 있게 해 주었다.')
    s.cl('main', 'This', subj='This', verbs=['allowed'])
    s.cl('subject_relative', 'who', verbs=['wanted'], marker='who')
    s.g('This', 'this', '이것은', referent_ko='매우 단순한 디자인과 사용하기 쉬운 인터페이스')
    s.g('allowed|to', 'allow A to V', 'A(이/가) ~할 수 있게 해 주다', at=s.text.index('allowed'),
        verb_form=pp('regular-past', s, 'allowed', 'allow'),
        verb_construction={'kind': 'verb-frame', 'verb_span': s.span_of('allowed'), 'lemma': 'allow',
                           'link_spans': [s.span_of('to', s.text.index('to get'))],
                           'review_record': 'allowed those who wanted to participate to get started: A=those(관계절 포함), to V=to get started.'})
    s.glosses[-1]['spans'] = [s.span_of('allowed'), s.span_of('to', s.text.index('to get'))]
    s.g('those', 'those', '사람들')
    rel = s.g('who', 'who V′', 'V′했던 (관계대명사)')
    s.g('wanted|to', 'want to V', '~하기를 원하다', verb_form=pp('regular-past', s, 'wanted', 'want'),
        verb_construction={'kind': 'to-complement', 'verb_span': s.span_of('wanted'), 'lemma': 'want',
                           'link_spans': [s.span_of('to', s.text.index('wanted'))], 'review_record': 'wanted to participate: want의 목적어 to V.'})
    s.g('participate', 'participate', '참여하다')
    s.g('get|started', 'get started', '시작하다')
    s.g('quickly', 'quickly', '빨리')
    s.hint('those [who wanted]', '[원했던] 사람들', span='those who wanted', label='주격 관계대명사 who',
           links=[(['who'], ['던'])], meaning='(참여하기를) 원했던 사람들',
           explanation='those(사람들)를 주격 관계대명사 who가 받아 wanted to participate가 꾸민다. V′ wanted까지만 표시.')
    s.relative_ids = [rel['id']]
    s.review = ('allow A to V에서 A가 those who wanted to participate(관계절 포함)라 길다. 필수 관계사 who 힌트. '
                'allow A to V는 동사 구문 후순위 후보이나 A와 to V가 관계절로 떨어져 있고 일반형 힌트는 연속 발췌만 가능해 각주로 지원. 수동 없음.')
    out.append(s)

    # ---------------- s19 ----------------
    s = S('s19', T['s19'])
    s.ch('New visitors were greeted', '새로운 방문자들은 환영을 받았다')
    s.ch('with a brief tutorial', '간단한 사용 지침과 함께')
    s.ch('that explained the project.', '그 프로젝트를 설명한.')
    s.natural('새로운 방문자들은 그 프로젝트를 설명하는 간단한 사용 지침과 함께 환영을 받았다.')
    s.cl('main', 'New', subj='New visitors', verbs=['were', 'greeted'])
    s.cl('subject_relative', 'that', verbs=['explained'], marker='that')
    s.g('New', 'new', '새로운')
    s.g('visitors', 'visitors', '방문자들')
    f = s.g('were', 'be p.p.', '~되다', kind='function', combines_with=[])
    gr = s.g('greeted', 'greeted', '환영받은, 맞이된', verb_form=pp('passive-participle', s, 'greeted', 'greet', f['id']))
    link(f, gr)
    s.g('with', 'with', '~와 함께')
    s.g('brief', 'brief', '간단한, 짧은')
    s.g('tutorial', 'tutorial', '사용 지침, 안내', star=W['tutorial'])
    rel = s.g('that', 'that V′', 'V′한 (관계대명사)')
    s.g('explained', 'explain', '설명하다', verb_form=pp('regular-past', s, 'explained', 'explain'))
    s.g('project', 'project', '프로젝트')
    s.hint('a brief tutorial [that explained]', '[설명한] 간단한 사용 지침', span='a brief tutorial that explained',
           label='주격 관계대명사 that', links=[(['that'], ['한'])], meaning='(그 프로젝트를) 설명한 간단한 사용 지침',
           explanation='a brief tutorial을 주격 관계대명사 that이 받아 explained the project가 꾸민다. V′ explained까지만 표시.')
    s.relative_ids = [rel['id']]
    s.review = '수동 were greeted + with 전치사구. 필수 관계사 that 힌트. 수동은 힌트가 이미 있어 단위 분석 be p.p. 대표(u2-gp4)로 연결.'
    out.append(s)

    # ---------------- s20 ----------------
    s = S('s20', T['s20'])
    s.ch('Then they were shown an image', '그런 다음 그들에게 이미지가 보여졌다')
    s.ch('of a galaxy', '은하의')
    s.ch('and asked to click buttons', '그리고 그들은 버튼을 클릭하도록 요청받았다')
    s.ch('that described its features.', '그것의 특징을 설명한.')
    s.natural('그런 다음 그들에게 은하 이미지 한 장이 보여졌고, 그들은 그 은하의 특징을 설명하는 버튼을 클릭하도록 요청받았다.')
    s.cl('main', 'they', subj='they', verbs=['were', 'shown', 'and', 'asked'])
    s.cl('subject_relative', 'that', verbs=['described'], marker='that')
    s.g('Then', 'then', '그런 다음')
    s.g('they', 'they', '그들은', referent_ko='새로운 방문자들')
    f = s.g('were', 'be p.p.', '~되다', kind='function', combines_with=[])
    sh = s.g('shown', 'shown', '보여진', verb_form=pp('passive-participle', s, 'shown', 'show', f['id']))
    s.g('image', 'image', '이미지')
    s.g('of', 'of', '~의')
    s.g('galaxy', 'galaxy', '은하')
    ak = s.g('asked', 'asked', '요청받은', verb_form=pp('passive-participle', s, 'asked', 'ask', f['id']))
    link(f, sh, ak)
    f2 = s.g('to', 'to V', '~하도록', kind='function', combines_with=[], at=s.text.index('to click'))
    cl = s.g('click', 'click', '클릭하다')
    link(f2, cl)
    s.g('buttons', 'buttons', '버튼들')
    rel = s.g('that', 'that V′', 'V′한 (관계대명사)')
    s.g('described', 'describe', '설명하다, 묘사하다', verb_form=pp('regular-past', s, 'described', 'describe'))
    s.g('its', 'its', '그것의', referent_ko='이미지 속 은하')
    s.g('features', 'features', '특징들')
    s.hint('buttons [that described]', '[설명한] 버튼들', span='buttons that described', label='주격 관계대명사 that',
           links=[(['that'], ['한'])], meaning='(그 은하의 특징을) 설명한 버튼들',
           explanation='buttons를 주격 관계대명사 that이 받아 described its features가 꾸민다. V′ described까지만 표시.')
    s.brk('of', 'postnominal-preposition', 'of a galaxy는 앞 명사 an image를 꾸미는 전치사구')
    s.relative_ids = [rel['id']]
    s.review = ('주어 they의 병렬 수동 were shown … and (were) asked to V: be는 한 번, p.p. 두 개가 같은 기능 각주에 연결. '
                '필수 관계사 that 힌트. 수동은 힌트가 있어 분석 be p.p. 대표로 연결. of a galaxy 후치수식 경계. '
                'to click은 수동 asked의 보충 to V이지만 수동 p.p. 각주 표제어는 실제형 asked만 허용되어 to V — ~하도록으로 분리(L2-6 검수자 수용).')
    out.append(s)

    # ---------------- s21 ----------------
    s = S('s21', T['s21'])
    s.ch('Is the galaxy smooth and rounded?', '그 은하는 매끄럽고 둥근가?')
    s.natural('그 은하는 매끄럽고 둥근가?')
    s.cl('main', 'Is', subj='the galaxy', verbs=[], vfirst=['Is'])
    s.g('Is', 'is', '~인가')
    s.g('galaxy', 'galaxy', '은하')
    s.g('smooth', 'smooth', '매끄러운')
    s.g('rounded', 'rounded', '둥근')
    s.review = 'be동사 의문문(버튼 질문 예시). 힌트 불필요.'
    out.append(s)

    # ---------------- s22 ----------------
    s = S('s22', T['s22'])
    s.ch('Is its shape an oval or a spiral?', '그것의 모양은 타원형인가 아니면 나선형인가?')
    s.natural('그 은하의 모양은 타원형인가, 아니면 나선형인가?')
    s.cl('main', 'Is', subj='its shape', verbs=[], vfirst=['Is'])
    s.g('Is', 'is', '~인가')
    s.g('its', 'its', '그것의', referent_ko='그 은하')
    s.g('shape', 'shape', '모양')
    s.g('oval', 'oval', '타원형')
    s.g('or', 'or', '아니면')
    s.g('spiral', 'spiral', '나선형')
    s.review = 'be동사 의문문(버튼 질문 예시). 힌트 불필요.'
    out.append(s)

    # ---------------- s23 ----------------
    s = S('s23', T['s23'])
    s.ch('After completion', '완료 후에')
    s.ch('of the tutorial', '사용 지침의')
    s.ch('and a little bit of practice,', '그리고 약간의 연습 (후에),')
    s.ch('the participants were able to classify galaxies effectively.', '참여자들은 은하를 효과적으로 분류할 수 있었다.')
    s.natural('사용 지침을 마치고 약간 연습한 뒤에, 참여자들은 은하를 효과적으로 분류할 수 있었다.')
    s.cl('main', 'the', subj='the participants', verbs=['were'], occ=1)
    s.g('After', 'after', '~후에')
    s.g('completion', 'completion', '완료, 끝마침')
    s.g('of', 'of', '~의')
    s.g('tutorial', 'tutorial', '사용 지침', star=W['tutorial'])
    q = s.g('a little bit of', 'a little bit of', '약간의')
    s.g('practice', 'practice', '연습', at=s.text.index('of practice') + 3)
    s.g('participants', 'participants', '참여자들', star=W['participants'])
    s.g('were|able|to', 'be able to V', '~할 수 있다')
    s.g('classify', 'classify', '분류하다', star=W['classify'])
    s.g('galaxies', 'galaxies', '은하들')
    s.g('effectively', 'effectively', '효과적으로', star=W['effectively'])
    s.brk('of', 'postnominal-preposition', 'of the tutorial은 앞 명사 completion을 꾸미는 전치사구')
    s.prot('a little bit of', 'quantity-kind-of', '수량 표현 a little bit of가 뒤 명사 practice 앞에서 ‘약간의’로 같은 어순 대응', gloss=q)
    s.review = ('After + [completion of the tutorial] and [a little bit of practice] 두 명사구. be able to V는 V 칸에 were만. '
                'completion of 후치수식 경계, a little bit of 수량 표현 보호. 접속사절·관계사·수동 없음 → 힌트 없음.')
    out.append(s)

    # ---------------- s24 ----------------
    s = S('s24', T['s24'], key=True)
    s.ch('It was online media', '바로 온라인 미디어였다')
    s.ch('that helped spread the word', '소문을 퍼뜨리는 것을 도운 것은')
    s.ch('about Galaxy Zoo,', 'Galaxy Zoo에 대한,')
    s.ch('bringing more and more participants', '점점 더 많은 참여자들을 데려오면서')
    s.ch('to the website.', '그 웹사이트로.')
    s.natural('Galaxy Zoo에 대한 소문을 퍼뜨리는 데 도움을 준 것은 바로 온라인 미디어였고, 이는 그 웹사이트에 점점 더 많은 참여자들을 불러 모았다.')
    s.cl('main', 'It', subj='It', verbs=['was'])
    s.cl('subject_relative', 'that', verbs=['helped'], marker='that')
    s.g('It|was|that', 'It was A that V′', 'V′한 것은 바로 A였다')
    s.g('online', 'online', '온라인')
    s.g('media', 'media', '미디어, 매체')
    s.g('helped', 'help V', '~하는 것을 돕다', verb_form=pp('regular-past', s, 'helped', 'help'),
        verb_construction={'kind': 'verb-frame', 'verb_span': s.span_of('helped'), 'lemma': 'help', 'link_spans': [],
                           'review_record': 'helped spread: help 뒤 원형부정사 spread.'})
    s.g('spread|word', 'spread the word', '소문을 퍼뜨리다')
    s.g('about', 'about', '~에 대한')
    f = s.g('bringing', 'V-ing', '~하면서 (분사구문)', kind='function', combines_with=[])
    br = s.g('bringing', 'bring', '데려오다', same=True, verb_form=pp('ing', s, 'bringing', 'bring'))
    link(f, br)
    s.g('more|and|more', 'more and more', '점점 더 많은')
    s.g('participants', 'participants', '참여자들', star=W['participants'])
    s.g('to', 'to', '~로', at=s.text.index('to the website'))
    s.g('website', 'website', '웹사이트')
    s.brk('about', 'postnominal-preposition', 'about Galaxy Zoo는 앞 명사 the word를 꾸미는 전치사구')
    s.hint('It was online media [that helped]', '[도운] 것은 바로 온라인 미디어였다', span='It was online media that helped',
           label='It ~ that 강조 구문', links=[(['It was', 'that'], ['것은 바로', '였다'])],
           meaning='(소문을 퍼뜨리는 것을) 도운 것은 바로 온라인 미디어였다',
           explanation='It was A that ~: A(online media)를 강조하는 구문. that 뒤 helped가 동사로 이어진다. 가주어 구문이 아니다.')
    s.hint('[bringing more and more participants]', '[점점 더 많은 참여자들을 데려오면서]',
           span='bringing more and more participants to the website', label='분사구문',
           links=[(['ing'], ['면서'])], meaning='점점 더 많은 참여자들을 (그 웹사이트로) 데려오면서',
           explanation='콤마 뒤 bringing …이 앞 절의 결과로 이어지는 동시 상황을 나타내는 분사구문. 주어는 앞 절의 online media.')
    s.review = ('It was A that 강조 구문(that은 관계대명사가 아닌 강조 구문의 that이라 relative_gloss_ids에 넣지 않음). '
                'help V(원형부정사 spread). bringing 분사구문. 힌트 2개. 수동 없음.')
    out.append(s)

    # ---------------- s25 ----------------
    s = S('s25', T['s25'])
    s.ch('Shortly after the website was launched,', '그 웹사이트가 개설된 직후에,')
    s.ch('nearly 70,000 classifications were being made', '거의 7만 건의 분류가 이루어지고 있었다')
    s.ch('per hour.', '시간당.')
    s.natural('그 웹사이트가 개설되고 얼마 되지 않아, 시간당 거의 7만 건의 분류가 이루어지고 있었다.')
    s.cl('subordinate', 'after', subj='the website', verbs=['was', 'launched'], marker='after')
    s.cl('main', 'nearly', subj='nearly 70,000 classifications', verbs=['were being made'])
    s.g('Shortly|after', 'shortly after S′ V′', 'S′(이/가) V′한 직후에')
    s.g('website', 'website', '웹사이트')
    f = s.g('was', 'be p.p.', '~되다', kind='function', combines_with=[])
    la = s.g('launched', 'launched', '개설된', verb_form=pp('passive-participle', s, 'launched', 'launch', f['id']))
    link(f, la)
    s.g('nearly', 'nearly', '거의')
    s.g('classifications', 'classifications', '분류(한 건수)')
    f2 = s.g('were|being', 'be being p.p.', '~되고 있다', kind='function', combines_with=[])
    md = s.g('made', 'made', '이루어진 (흔한 뜻: 만들어진)', verb_form=pp('passive-participle', s, 'made', 'make', f2['id']))
    link(f2, md)
    s.g('per', 'per', '~당')
    s.g('hour', 'hour', '시간')
    s.hint('[Shortly after the website was launched]', '[그 웹사이트가 개설된 직후에]', span='Shortly after the website was launched',
           label='시간 접속사 after', links=[(['Shortly after'], ['가', '직후에'])],
           meaning='그 웹사이트가 개설된 직후에',
           explanation='shortly after S′ V′: S′가 V′한 직후에. S′ the website, V′ was launched(수동)까지 표시.')
    s.vf_hint(fn=f2, lex=md, en='were being made', ko='이루어지고 있었다', formula='be being p.p.',
              step_form='made', step_ko='이루어진', en_mark=['were being'], ko_mark=['지고 있었다'],
              span='nearly 70,000 classifications were being made',
              meaning='(분류가) 이루어지고 있었다',
              explanation='주절의 진행 수동 were being made: 과거 시점에 계속 ‘이루어지고 있던’ 일. 주어·per hour는 표시에서 제외.')
    s.review = ('시간 부사절 shortly after + 주절 진행 수동. 힌트 1: after 절, 힌트 2: 주절 진행 수동(be being p.p.)은 해석의 핵심이라 후순위 기능 결합으로 선정. '
                '부사절 안 수동 was launched는 이미 힌트 2개라 단위 분석 be p.p. 대표 u2-gp4로 연결.')
    out.append(s)

    # ---------------- s26 ----------------
    s = S('s26', T['s26'])
    s.ch('In a year and a half,', '1년 반 만에,')
    s.ch('more than 80,000 individuals participated,', '8만 명이 넘는 개인들이 참여했다,')
    s.ch('and they made more than 75 million classifications.', '그리고 그들은 7,500만 건이 넘는 분류를 했다.')
    s.natural('1년 반 만에 8만 명이 넘는 사람들이 참여했고, 그들은 7,500만 건이 넘는 분류를 해냈다.')
    s.cl('main', 'more', subj='more than 80,000 individuals', verbs=['participated'])
    s.cl('main', 'they', subj='they', verbs=['made'], marker='and')
    s.g('In a year and a half', 'in a year and a half', '1년 반 만에')
    s.g('more|than', 'more than', '~보다 많은, ~ 넘는')
    s.g('individuals', 'individuals', '개인들, 사람들')
    s.g('participated', 'participate', '참여하다', verb_form=pp('regular-past', s, 'participated', 'participate'))
    s.g('they', 'they', '그들은', referent_ko='Galaxy Zoo에 참여한 8만 명이 넘는 사람들')
    s.g('made', 'made', '했다, 해냈다 (make의 과거)', verb_form=pp('irregular-past', s, 'made', 'make'))
    s.g('more|than', 'more than', '~보다 많은, ~ 넘는')
    s.g('million', 'million', '백만')
    s.g('classifications', 'classifications', '분류(한 건수)')
    s.review = '두 독립 주절(and). in + 기간 = ~만에(소요 기간). 수치 more than 유지. 힌트 불필요, 수동 없음.'
    out.append(s)

    # ---------------- s27 ----------------
    s = S('s27', T['s27'], key=True)
    s.ch('If it had not been for those participants,', '그 참여자들이 없었다면,')
    s.ch('Schawinski couldn’t have classified that many images.', 'Schawinski는 그렇게 많은 이미지를 분류할 수 없었을 것이다.')
    s.natural('그 참여자들이 없었다면, Schawinski는 그렇게 많은 이미지를 분류할 수 없었을 것이다.')
    s.cl('subordinate', 'If', subj='it', verbs=['had not been'], marker='If')
    s.cl('main', 'Schawinski', subj='Schawinski', verbs=['couldn’t have classified'])
    s.g('If|it|had|not|been|for', 'If it had not been for A', 'A(이/가) 없었다면')
    s.g('those', 'those', '그')
    s.g('participants', 'participants', '참여자들', star=W['participants'])
    f = s.g('couldn’t|have', 'couldn’t have p.p.', '~할 수 없었을 것이다', kind='function', combines_with=[])
    c = s.g('classified', 'classify', '분류하다 (classified는 classify의 p.p.형)', star=W['classify'],
            verb_form=pp('perfect-participle', s, 'classified', 'classify', f['id']))
    link(f, c)
    s.g('that|many', 'that many', '그렇게 많은')
    s.g('images', 'images', '이미지들')
    s.hint('[If it had not been for] those participants', '그 참여자들이 [없었다면]',
           span='If it had not been for those participants', label='가정법 과거완료 If it had not been for',
           links=[(['If it had not been for'], [('이', 0), '없었다면'])], meaning='그 참여자들이 없었다면',
           explanation='If it had not been for A: A가 없었다면(과거 사실의 반대). 주절 couldn’t have p.p.와 짝을 이룬다.')
    s.vf_hint(fn=f, lex=c, en='couldn’t have classified', ko='분류할 수 없었을 것이다', formula='couldn’t have p.p.',
              step_form='classify', step_ko='분류하다', en_mark=['couldn’t have'], ko_mark=['수 없었을 것이다'],
              span='Schawinski couldn’t have classified that many images',
              meaning='분류할 수 없었을 것이다',
              explanation='조동사 완료 couldn’t have p.p.: 과거에 ~할 수 없었을 것이다(가정법 과거완료 주절). 목적어 that many images 제외.')
    s.review = ('가정법 과거완료: If it had not been for A(A가 없었다면) + 주절 couldn’t have p.p. '
                '힌트 1: If it had not been for, 힌트 2: 주절 조동사 완료 기능 결합(해석 핵심). if절의 it은 가정 표현의 형식 주어로 숙어 각주에 포함.')
    s.relative_ids = []
    out.append(s)

    # ---------------- s28 ----------------
    s = S('s28', T['s28'])
    s.ch('In fact,', '사실,')
    s.ch('it would have taken him decades', '그에게 수십 년이 걸렸을 것이다')
    s.ch('on his own.', '그 혼자서는.')
    s.natural('사실, 그 혼자서는 수십 년이 걸렸을 것이다.')
    s.cl('main', 'it', subj='it', verbs=['would have taken'])
    s.g('In|fact', 'in fact', '사실')
    f = s.g('would|have', 'would have p.p.', '~했을 것이다', kind='function', combines_with=[])
    t = s.g('taken', 'take A B', 'A에게 B(시간)가 걸리다 (taken은 take의 p.p.형)',
            verb_form=pp('perfect-participle', s, 'taken', 'take', f['id']),
            verb_construction={'kind': 'verb-frame', 'verb_span': s.span_of('taken'), 'lemma': 'take', 'link_spans': [],
                               'review_record': 'it would have taken him decades: A=him, B=decades, 비인칭 it.'})
    link(f, t)
    s.g('him', 'him', '그에게', referent_ko='Kevin Schawinski')
    s.g('decades', 'decades', '수십 년')
    s.g('on|his|own', 'on his own', '그 혼자서', referent_ko='Kevin Schawinski')
    s.extra_cov[tuple(s.span_of('it'))] = {'exemption': 'below-middle1-unneeded', 'level': 'below-middle1',
        'reason': '시간이 걸림을 나타내는 비인칭 it(초등 기초어)은 따로 해석하지 않으며 take A B 각주로 뜻을 지원'}
    s.vf_hint(fn=f, lex=t, en='would have taken', ko='걸렸을 것이다', formula='would have p.p.',
              step_form='take', step_ko='걸리다', en_mark=['would have'], ko_mark=['렸을 것이다'],
              span='it would have taken him decades', meaning='(수십 년이) 걸렸을 것이다',
              explanation='would have p.p.: (참여자들이 없었다면) ~했을 것이다. 앞 문장 가정의 연속. 목적어 him decades 제외.')
    s.review = '비인칭 it + take A B(A에게 B가 걸리다), would have p.p.(과거 가정의 결과) → 기능 결합 힌트 1개. on his own 숙어.'
    out.append(s)

    # ---------------- s29 ----------------
    s = S('s29', T['s29'])
    s.ch('More than 15 years have passed', '15년이 넘게 지났다')
    s.ch('since the project first began in 2007.', '그 프로젝트가 2007년에 처음 시작된 이래로.')
    s.natural('그 프로젝트가 2007년에 처음 시작된 이래로 15년이 넘게 지났다.')
    s.cl('main', 'More', subj='More than 15 years', verbs=['have', 'passed'])
    s.cl('subordinate', 'since', subj='the project', verbs=['began'], marker='since')
    s.g('More|than', 'more than', '~보다 많은, ~ 넘는')
    s.g('years', 'years', '해, 년')
    f = s.g('have', 'have p.p.', '~했다', kind='function', combines_with=[])
    ps = s.g('passed', 'pass', '(시간이) 지나다 (passed는 pass의 p.p.형)', verb_form=pp('perfect-participle', s, 'passed', 'pass', f['id']))
    link(f, ps)
    s.g('since', 'since S′ V′', 'S′(이/가) V′한 이래로')
    s.g('project', 'project', '프로젝트')
    s.g('first', 'first', '처음')
    s.g('began', 'began', '시작했다 (begin의 과거)', verb_form=pp('irregular-past', s, 'began', 'begin'))
    s.g('in', 'in', '~에')
    s.hint('[since the project first began]', '[그 프로젝트가 처음 시작된 이래로]', span='since the project first began',
           label='시간 접속사 since', links=[(['since'], ['가', '이래로'])], meaning='그 프로젝트가 처음 시작된 이래로',
           explanation='since S′ V′: S′가 V′한 이래로(시간). S′ the project, V′ began까지 표시하고 in 2007은 제외.')
    s.vf_hint(fn=f, lex=ps, en='have passed', ko='지났다', formula='have p.p.', step_form='pass', step_ko='지나다',
              en_mark=['have'], ko_mark=['났다'], span='More than 15 years have passed', meaning='(15년이 넘게) 지났다',
              explanation='현재완료 have passed: 2007년부터 지금까지 시간이 흘러 15년이 넘었다. 주어 More than 15 years 제외.')
    s.review = '현재완료 주절 + since 시간 부사절. 힌트 1: since 절, 힌트 2: have passed 기능 결합(현재완료 계속 해석).'
    out.append(s)

    # ---------------- s30 ----------------
    s = S('s30', T['s30'])
    s.ch('Galaxy Zoo has now grown into Zooniverse,', 'Galaxy Zoo는 이제 Zooniverse로 성장했다,')
    s.ch('which is one of the most popular platforms', '그리고 그것은 가장 인기 있는 플랫폼 중 하나이다')
    s.ch('on the Internet', '인터넷에서')
    s.ch('for ordinary people', '평범한 사람들을 위한')
    s.ch('who want to participate', '참여하고 싶어 하는')
    s.ch('in science projects.', '과학 프로젝트에.')
    s.natural('Galaxy Zoo는 이제 Zooniverse로 성장했는데, 이것은 과학 프로젝트에 참여하고 싶어 하는 일반인들을 위한 인터넷에서 가장 인기 있는 플랫폼 중 하나이다.')
    s.cl('main', 'Galaxy', subj='Galaxy Zoo', verbs=['has', 'grown'])
    s.cl('subject_relative', 'which', verbs=['is'], marker='which')
    s.cl('subject_relative', 'who', verbs=['want'], marker='who')
    f = s.g('has', 'have p.p.', '~했다', kind='function', combines_with=[])
    s.g('now', 'now', '이제')
    gw = s.g('grown|into', 'grow into A', 'A로 성장하다 (grown은 grow의 p.p.형)',
             verb_form=pp('perfect-participle', s, 'grown', 'grow', f['id']),
             verb_construction={'kind': 'verb-frame', 'verb_span': s.span_of('grown'), 'lemma': 'grow',
                                'link_spans': [s.span_of('into')], 'review_record': 'has grown into Zooniverse: A=Zooniverse.'})
    link(f, gw)
    s.g('Zooniverse', 'Zooniverse', '주니버스 (시민 과학 온라인 플랫폼 이름)', proper=True)
    rel1 = s.g('which', ', which V′', '그리고 그것은 V′하다 (계속적 관계대명사)')
    s.g('is', 'is', '~이다')
    s.g('one|of', 'one of', '~ 중 하나')
    s.g('most', 'most', '가장')
    s.g('popular', 'popular', '인기 있는')
    s.g('platforms', 'platforms', '플랫폼들 (활동 공간이 되는 웹사이트)', star=W['platforms'])
    s.g('on', 'on', '~에서')
    s.g('Internet', 'the Internet', '인터넷')
    s.g('for', 'for', '~을 위한')
    s.g('ordinary', 'ordinary', '평범한')
    s.g('people', 'people', '사람들')
    rel2 = s.g('who', 'who V′', 'V′하는 (관계대명사)')
    s.g('want|to', 'want to V', '~하고 싶어 하다',
        verb_construction={'kind': 'to-complement', 'verb_span': s.span_of('want'), 'lemma': 'want',
                           'link_spans': [s.span_of('to', s.text.index('want'))], 'review_record': 'want to participate: want의 목적어 to V.'})
    s.g('participate', 'participate', '참여하다')
    s.g('in', 'in', '~에', at=s.text.index('in science'))
    s.g('science', 'science', '과학')
    s.g('projects', 'projects', '프로젝트들')
    s.hint('Zooniverse, [which is one]', 'Zooniverse, [그리고 그것은 하나이다]',
           span='Zooniverse, which is one', label='계속적 관계대명사 which',
           links=[(['which'], ['그리고 그것은'])], meaning='Zooniverse, 그리고 그것은 (가장 인기 있는 플랫폼 중) 하나이다',
           explanation='콤마 뒤 which가 Zooniverse를 받아 설명을 덧붙인다(추가 설명 → 그리고). be의 최소 보어 one까지만 표시.')
    s.hint('ordinary people [who want]', '[원하는] 평범한 사람들', span='ordinary people who want',
           label='주격 관계대명사 who', links=[(['who'], ['는'])], meaning='(과학 프로젝트에 참여하기를) 원하는 평범한 사람들',
           explanation='ordinary people을 주격 관계대명사 who가 받아 want to participate …가 꾸민다. V′ want까지만 표시.')
    s.brk('on', 'postnominal-preposition', 'on the Internet은 앞 명사 platforms를 꾸미는 전치사구')
    s.brk('for', 'postnominal-preposition', 'for ordinary people은 앞 명사 platforms를 꾸미는 전치사구')
    s.relative_ids = [rel1['id'], rel2['id']]
    s.review = ('현재완료 has grown into + 계속적 which(추가 설명: 그리고) + 주격 who. 필수 관계사 힌트 2개. '
                'has grown(have p.p.)은 힌트 한도로 단위 분석 have p.p. 대표 u2-gp5에 연결. on/for 후치수식 경계.')
    out.append(s)

    # ---------------- s31 ----------------
    s = S('s31', T['s31'])
    s.ch('It is more active than ever before,', '그것은 그 어느 때보다 더 활발하다,')
    s.ch('with about 2 million registered users worldwide.', '전 세계적으로 약 200만 명의 등록된 사용자들을 가진 채로.')
    s.natural('그것은 전 세계에 약 200만 명의 등록된 사용자를 두고 있으며, 그 어느 때보다 활발하다.')
    s.cl('main', 'It', subj='It', verbs=['is'])
    s.g('It', 'it', '그것은', referent_ko='Zooniverse')
    s.g('is', 'is', '~이다')
    s.g('more|than|ever|before', 'more ~ than ever before', '그 어느 때보다 더 ~한')
    s.g('active', 'active', '활발한')
    s.g('with', 'with', '~을 가진, ~이 있는')
    s.g('about', 'about', '약')
    s.g('million', 'million', '백만')
    s.g('registered', 'registered', '등록된', verb_form=pp('past-participle', s, 'registered', 'register'))
    s.g('users', 'users', '사용자들')
    s.g('worldwide', 'worldwide', '전 세계적으로')
    s.review = '단일 주절, 비교급 than ever before, with 부대 상황(명사구). registered는 명사 앞 과거분사. 힌트 불필요, 수동 없음.'
    out.append(s)

    # ---------------- s32 ----------------
    s = S('s32', T['s32'])
    s.ch('It now offers a wide range of projects', '그것은 현재 광범위한 프로젝트들을 제공한다')
    s.ch('in astronomy, biology, physics, and more.', '천문학, 생물학, 물리학 등 분야의.')
    s.natural('현재 그것은 천문학, 생물학, 물리학 등 다양한 분야의 프로젝트를 제공하고 있다.')
    s.cl('main', 'It', subj='It', verbs=['offers'])
    s.g('It', 'it', '그것은', referent_ko='Zooniverse')
    s.g('now', 'now', '현재')
    s.g('offers', 'offer', '제공하다', verb_form={'usage': 'third-person-singular', 'source_span': s.span_of('offers'),
        'lemma': 'offer', 'review_record': '주어 It(3인칭 단수)의 일반동사 offers → 원형 offer.'})
    q = s.g('a wide range of', 'a wide range of', '광범위한, 다양한')
    s.g('projects', 'projects', '프로젝트들', at=s.text.index('projects'))
    s.g('in', 'in', '~ 분야의 (흔한 뜻: ~안에)')
    s.g('astronomy', 'astronomy', '천문학')
    s.g('biology', 'biology', '생물학')
    s.g('physics', 'physics', '물리학')
    s.g('more', 'more', '그 밖의 것들')
    s.prot('a wide range of', 'quantity-kind-of', '수량·종류 표현 a wide range of가 뒤 명사 projects 앞에서 ‘광범위한’으로 같은 어순 대응', gloss=q)
    s.brk('in', 'postnominal-preposition', 'in astronomy … and more는 앞 명사 projects를 꾸미는 전치사구')
    s.hint('projects [in astronomy, biology, physics, and more]', '[천문학, 생물학, 물리학 등 분야의] 프로젝트들',
           span='projects in astronomy, biology, physics, and more', label='전치사구 후치수식',
           links=[(['in'], ['분야의'])], meaning='천문학, 생물학, 물리학 등 분야의 프로젝트들',
           explanation='전치사구 in astronomy, biology, physics, and more가 앞 명사 projects를 뒤에서 꾸민다(분야).')
    s.review = '단일 주절. a wide range of 수량 표현 보호, 전치사구 후치수식 → 힌트. 수동 없음.'
    out.append(s)

    # ---------------- s33 ----------------
    s = S('s33', T['s33'])
    s.ch('If you want to get involved,', '만약 여러분이 참여하고 싶다면,')
    s.ch('you should definitely check it out!', '여러분은 반드시 그것을 확인해 보아야 한다!')
    s.natural('만약 여러분이 참여하고 싶다면, 꼭 한번 확인해 보라!')
    s.cl('subordinate', 'If', subj='you', verbs=['want'], marker='If')
    s.cl('main', 'you', subj='you', verbs=['should', 'check'], occ=1)
    s.g('If', 'if S′ V′', 'S′(이/가) V′한다면')
    s.g('want|to', 'want to V', '~하고 싶다',
        verb_construction={'kind': 'to-complement', 'verb_span': s.span_of('want'), 'lemma': 'want',
                           'link_spans': [s.span_of('to')], 'review_record': 'want to get involved: want의 목적어 to V.'})
    s.g('get|involved', 'get involved', '참여하다, 관여하다')
    f = s.g('should', 'should V', '~해야 한다', kind='function', combines_with=[])
    s.g('definitely', 'definitely', '반드시, 꼭')
    ck = s.g('check|out', 'check A out', 'A를 확인해 보다', at=s.text.index('check'),
             verb_construction={'kind': 'verb-frame', 'verb_span': s.span_of('check'), 'lemma': 'check',
                                'link_spans': [s.span_of('out')], 'review_record': 'check it out: A=it(Zooniverse).'})
    link(f, ck)
    s.glosses.sort(key=lambda g: g['spans'][0][0])
    s.g('it', 'it', '그것을', referent_ko='Zooniverse', at=s.text.index('it out'))
    s.glosses.sort(key=lambda g: g['spans'][0][0])
    s.review = '조건 부사절 if + 주절 should V. check A out 분리 구동사(각주). 단순 구조라 힌트 없음. 수동 없음.'
    out.append(s)
    return out


UNIT = {
    'id': 'u2', 'source_id': 'src', 'paragraph_ids': ['p02', 'p03', 'p04', 'p05'],
    'sentence_ids': [f's{n:02d}' for n in range(7, 34)],
    'today_words': [
        {'id': W['classify'], 'text': 'classify', 'meaning_ko': '분류하다'},
        {'id': W['suggest'], 'text': 'suggest', 'meaning_ko': '제안하다'},
        {'id': W['individually'], 'text': 'individually', 'meaning_ko': '개별적으로, 하나씩'},
        {'id': W['complain'], 'text': 'complain', 'meaning_ko': '불평하다'},
        {'id': W['tutorial'], 'text': 'tutorial', 'meaning_ko': '사용 지침, 안내'},
        {'id': W['effectively'], 'text': 'effectively', 'meaning_ko': '효과적으로'},
        {'id': W['participants'], 'text': 'participants', 'meaning_ko': '참여자들, 참가자들'},
        {'id': W['platforms'], 'text': 'platforms', 'meaning_ko': '플랫폼들'},
    ],
}


def analysis(_):
    return {
        'heading_kind': '제목',
        'title_or_topic_en': 'Galaxy Zoo: Classifying Galaxies Together',
        'title_or_topic_ko': '갤럭시 주: 함께 은하를 분류하다',
        'intent_ko': '혼자서는 수십 년이 걸릴 은하 분류 작업을 평범한 사람들이 온라인으로 함께 해낸 Galaxy Zoo의 사례를 통해, 시민의 참여가 과학에 큰 힘이 된다는 것을 보여 주는 글이다.',
        'flow': [
            {'sentence_ids': [f's{n:02d}' for n in range(7, 14)], 'label': '문제 상황',
             'text_ko': 'Schawinski는 약 백만 장의 은하 이미지를 모양별로 하나하나 분류해야 했지만, 일주일에 5만 장밖에 하지 못해 나머지를 어떻게 할지 막막했다.'},
            {'sentence_ids': [f's{n:02d}' for n in range(14, 24)], 'label': '해결책',
             'text_ko': '친구 Lintott의 제안으로 인터넷에서 도움을 구하는 Galaxy Zoo를 만들었고, 단순한 웹사이트와 사용 지침 덕분에 누구나 금방 은하 분류에 참여할 수 있었다.'},
            {'sentence_ids': [f's{n:02d}' for n in range(24, 29)], 'label': '성과',
             'text_ko': '온라인 미디어로 소문이 퍼져 참여자가 몰렸고, 짧은 기간에 엄청난 수의 분류가 이루어져 혼자서는 수십 년이 걸렸을 일을 해냈다.'},
            {'sentence_ids': [f's{n:02d}' for n in range(29, 34)], 'label': '현재',
             'text_ko': 'Galaxy Zoo는 인기 있는 시민 과학 플랫폼 Zooniverse로 성장해 여러 분야의 프로젝트를 제공하고 있으며, 글쓴이는 독자에게도 참여를 권한다.'},
        ],
        'easy_explanations': [
            {'sentence_id': 's10', 'explanatory_sentences': [
                '10번 문장은 9번에서 말한 분류 작업이 왜 그렇게 힘들었는지 설명한다.',
                '은하 사진들은 얼핏 보면 다 비슷하다.',
                '하지만 자세히 보면 모양이 조금씩 다르다.',
                '그래서 사진을 한 장씩 직접 보면서 나누는 것이 가장 좋은 방법이었다.',
                '이 점이 11번 문장의 ‘엄청난 시간이 든다’로 이어진다.']},
            {'sentence_id': 's24', 'explanatory_sentences': [
                '24번 문장은 Galaxy Zoo가 어떻게 많은 사람을 모았는지 보여 준다.',
                '사람들이 인터넷 기사나 게시물로 Galaxy Zoo 소식을 서로 전했다.',
                '그 소식을 본 사람들이 점점 더 많이 웹사이트에 찾아왔다.',
                '글쓴이는 소문이 퍼지도록 도운 것이 바로 온라인 미디어였다고 힘주어 말한다.']},
            {'sentence_id': 's27', 'explanatory_sentences': [
                '27번 문장은 24~26번에서 본 참여자들의 힘을 한 번 더 강조한다.',
                '실제로는 참여자들이 있었기 때문에 약 백만 장이나 되는 이미지를 분류할 수 있었다.',
                '이 문장은 반대로 ‘만약 그들이 없었다면’이라고 상상해 본다.',
                '그랬다면 Schawinski 혼자서는 그만큼 분류하지 못했을 것이다.',
                '28번 문장은 혼자였다면 수십 년이 걸렸을 거라고 덧붙인다.']},
        ],
        'grammar_points': [
            {'id': 'u2-gp1', 'sentence_id': 's12', 'span': 'It took Schawinski a whole week to classify just 50,000 galaxies',
             'title': 'It takes A B to V: A(이/가) ~하는 데 B(시간)가 걸리다', 'formula_key': 'It takes A B to V',
             'explanation': '공식: It takes A B to V — A(이/가) ~하는 데 B(시간)가 걸리다. It은 따로 해석하지 않는 형식상 주어다. '
                            'took = take의 과거, A = Schawinski, B = a whole week(꼬박 일주일), to V = to classify just 50,000 galaxies(고작 5만 개의 은하를 분류하다). '
                            '→ Schawinski가 고작 5만 개의 은하를 분류하는 데 꼬박 일주일이 걸렸다.',
             'practice': {'span': 'It took Schawinski a whole week to classify',
                          'formula_support': {'en': 'It takes A B to V', 'ko': 'A(이/가) ~하는 데 B(시간)가 걸리다'},
                          'support': [('s12', 'whole'), ('s12', 'week'), ('s12', 'classify')],
                          'answer_ko': 'Schawinski가 분류하는 데 꼬박 일주일이 걸렸다'}},
            {'id': 'u2-gp2', 'sentence_id': 's24', 'span': 'It was online media that helped spread the word about Galaxy Zoo',
             'title': 'It was A that V′: V′한 것은 바로 A였다 (강조 구문)', 'formula_key': 'It was A that V′',
             'explanation': '공식: It was A that V′ — V′한 것은 바로 A였다. 강조하는 말 A = online media(온라인 미디어), '
                            'V′ = helped spread the word about Galaxy Zoo(Galaxy Zoo에 대한 소문을 퍼뜨리는 것을 도왔다). '
                            '→ Galaxy Zoo에 대한 소문을 퍼뜨리는 것을 도운 것은 바로 온라인 미디어였다. It was와 that을 빼도 Online media helped spread the word.라는 완전한 문장이 되므로 가주어가 아닌 강조 구문이다.',
             'practice': {'span': 'It was online media that helped spread the word',
                          'formula_support': {'en': 'It was A that V′', 'ko': 'V′한 것은 바로 A였다'},
                          'support': [('s24', 'online'), ('s24', 'media'), ('s24', 'help V'), ('s24', 'spread the word')],
                          'answer_ko': '소문을 퍼뜨리는 것을 도운 것은 바로 온라인 미디어였다'}},
            {'id': 'u2-gp3', 'sentence_id': 's27', 'span': 'If it had not been for those participants',
             'title': 'If it had not been for A: A(이/가) 없었다면', 'formula_key': 'If it had not been for A',
             'explanation': '공식: If it had not been for A — A(이/가) 없었다면(과거 사실과 반대로 가정). A = those participants(그 참여자들). '
                            '→ 그 참여자들이 없었다면. 뒤 주절은 couldn’t have p.p.(~할 수 없었을 것이다)로 짝을 이루어 “그 참여자들이 없었다면 Schawinski는 그렇게 많은 이미지를 분류할 수 없었을 것이다”가 된다. 실제로는 참여자들이 있었다는 뜻이다.',
             'practice': {'span': 'If it had not been for those participants',
                          'formula_support': {'en': 'If it had not been for A', 'ko': 'A(이/가) 없었다면'},
                          'support': [('s27', 'those'), ('s27', 'participants')],
                          'answer_ko': '그 참여자들이 없었다면'}},
            {'id': 'u2-gp4', 'sentence_id': 's17', 'span': 'The website was kept as simple as possible',
             'title': 'be p.p.: ~되다 (수동태)', 'formula_key': 'be p.p.',
             'explanation': '공식: be p.p. — ~되다. be = was(과거), p.p. = kept(유지된), 주어 = The website(그 웹사이트), 보어 = as simple as possible(가능한 한 단순하게). '
                            '→ 그 웹사이트는 가능한 한 단순하게 유지되었다. 누군가가 웹사이트를 단순하게 유지한 것이므로 주어는 동작을 받는 쪽이다.',
             'supplemental': {'function': ('s17', 'be p.p.', 0),
                              'reason': '이 단위의 수동 be p.p.(s10·s17·s19·s20·s25)는 각 문장에 이미 더 우선하는 힌트가 있어 결합 힌트로 선정하지 않았고, 기본 분석 3개에 be p.p. 설명이 없어 대표 사례를 1회 보충'},
             'practice': {'span': 'The website was kept as simple as possible',
                          'formula_support': {'en': 'be p.p.', 'ko': '~되다'},
                          'support': [('s17', 'website'), ('s17', 'kept'), ('s17', 'as ~ as possible'), ('s17', 'simple')],
                          'answer_ko': '그 웹사이트는 가능한 한 단순하게 유지되었다'}},
            {'id': 'u2-gp5', 'sentence_id': 's30', 'span': 'Galaxy Zoo has now grown into Zooniverse',
             'title': 'have p.p.: ~했다 (현재완료)', 'formula_key': 'have p.p.',
             'explanation': '공식: have p.p. — ~했다(지금까지 이어진 결과). have = has, p.p. = grown(grow의 p.p.형), grow into A = A로 성장하다, A = Zooniverse, 주어 = Galaxy Zoo. '
                            '→ Galaxy Zoo는 이제 Zooniverse로 성장했다. 2007년에 시작해 지금은 Zooniverse가 되어 있다는 결과를 나타낸다.',
             'supplemental': {'function': ('s30', 'have p.p.', 0),
                              'reason': 's30의 has grown은 필수 관계사 힌트 2개로 결합 힌트를 둘 수 없고, 기본 분석에 have p.p. 설명이 없어 대표 사례를 1회 보충(s29 have passed는 힌트로 연결)'},
             'practice': {'span': 'Galaxy Zoo has now grown into Zooniverse',
                          'formula_support': {'en': 'have p.p.', 'ko': '~했다'},
                          'support': [('s30', 'now'), ('s30', 'grow into A'), ('s30', 'Zooniverse')],
                          'answer_ko': 'Galaxy Zoo는 이제 Zooniverse로 성장했다'}},
        ],
        'formula_routes': [
            {'function': ('s10', 'be p.p.', 0), 'route': 'analysis', 'grammar_point_id': 'u2-gp4',
             'review_record': 'were shaped: 힌트 2개(to부정사·while)가 있어 분석 대표 u2-gp4로 연결'},
            {'function': ('s17', 'be p.p.', 0), 'route': 'analysis', 'grammar_point_id': 'u2-gp4',
             'review_record': 'was kept: 보충 분석 u2-gp4의 대표 사례'},
            {'function': ('s19', 'be p.p.', 0), 'route': 'analysis', 'grammar_point_id': 'u2-gp4',
             'review_record': 'were greeted: 관계사 힌트가 있어 분석 대표 u2-gp4로 연결'},
            {'function': ('s20', 'be p.p.', 0), 'route': 'analysis', 'grammar_point_id': 'u2-gp4',
             'review_record': 'were shown and asked: 관계사 힌트가 있어 분석 대표 u2-gp4로 연결'},
            {'function': ('s25', 'be p.p.', 0), 'route': 'analysis', 'grammar_point_id': 'u2-gp4',
             'review_record': 'was launched: 힌트 2개(after 절·진행 수동)라 분석 대표 u2-gp4로 연결'},
            {'function': ('s25', 'be being p.p.', 0), 'route': 'hint', 'hint_index': 1,
             'review_record': 'were being made: 주절 진행 수동을 기능 결합 힌트로 선정'},
            {'function': ('s27', 'couldn’t have p.p.', 0), 'route': 'hint', 'hint_index': 1,
             'review_record': 'couldn’t have classified: 가정법 주절 기능 결합 힌트'},
            {'function': ('s28', 'would have p.p.', 0), 'route': 'hint', 'hint_index': 0,
             'review_record': 'would have taken: 기능 결합 힌트'},
            {'function': ('s29', 'have p.p.', 0), 'route': 'hint', 'hint_index': 1,
             'review_record': 'have passed: 기능 결합 힌트'},
            {'function': ('s30', 'have p.p.', 0), 'route': 'analysis', 'grammar_point_id': 'u2-gp5',
             'review_record': 'has grown: 관계사 힌트 2개로 분석 보충 u2-gp5에 연결'},
        ],
        'relations': [
            {'head': {'id': 'u2-r1h', 'text': 'tremendous', 'meaning_ko': '엄청난'},
             'synonym': {'id': 'u2-r1s', 'text': 'enormous', 'meaning_ko': '거대한, 막대한'},
             'antonym': {'id': 'u2-r1a', 'text': 'tiny', 'meaning_ko': '아주 작은'}},
            {'head': {'id': 'u2-r2h', 'text': 'dull', 'meaning_ko': '따분한, 지루한'},
             'synonym': {'id': 'u2-r2s', 'text': 'boring', 'meaning_ko': '지루한'},
             'antonym': {'id': 'u2-r2a', 'text': 'exciting', 'meaning_ko': '흥미진진한, 신나는'}},
            {'head': {'id': 'u2-r3h', 'text': 'brief', 'meaning_ko': '간단한, 짧은'},
             'synonym': {'id': 'u2-r3s', 'text': 'short', 'meaning_ko': '짧은'},
             'antonym': {'id': 'u2-r3a', 'text': 'lengthy', 'meaning_ko': '긴, 장황한'}},
        ],
    }


def workbook():
    return {
        'relation_order': ['u2-r2s', 'u2-r1a', 'u2-r3h', 'u2-r2a', 'u2-r1h', 'u2-r3s', 'u2-r2h', 'u2-r3a', 'u2-r1s'],
        'key_sentence_ids': ['s24', 's27'],
        'question_id': 'Q02',
        'syntax_point_ids': ['u2-gp1', 'u2-gp2', 'u2-gp3', 'u2-gp4', 'u2-gp5'],
    }
