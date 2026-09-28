"""공통 단위 5: s62~s74 (p26~p32) — 남자의 위협과 삼촌의 등장 + 작품 소개.

사용자 결정(2026-09-28 “5단위, 작품 소개 합침”): 마지막 장면(p26~p31)과 별표 작품 소개 단락 p32를 한 단위로 묶는다.
"""
from author import S, link, verbless

W = {'serious': 'u5-w1', 'firmly': 'u5-w2', 'prove': 'u5-w3', 'disastrous': 'u5-w4',
     'resume': 'u5-w5', 'factor': 'u5-w6', 'shortage': 'u5-w7', 'address': 'u5-w8'}


def pp(usage, s, word, lemma, fid=None, occ_after=0, review=None):
    row = {'usage': usage, 'source_span': s.span_of(word, occ_after), 'lemma': lemma}
    if fid:
        row['function_gloss_id'] = fid
    if review:
        row['review_record'] = review
    return row


def v3(s, word, lemma, subj, occ_after=0):
    return pp('third-person-singular', s, word, lemma, occ_after=occ_after,
              review=f'주어 {subj}(3인칭 단수)의 일반동사 {word} → 원형 {lemma}.')


def sentences(T):
    out = []

    # ---------------- s62 ----------------
    s = S('s62', T['s62'])
    s.ch('For a moment', '잠시 동안')
    s.ch('I think he is joking,', '나는 그가 농담하고 있다고 생각한다,')
    s.ch('but then realize', '하지만 곧 깨닫는다')
    s.ch('he is serious.', '그가 진지하다는 것을.')
    s.natural('잠시 나는 그가 농담하는 거라고 생각하지만, 곧 그가 진지하다는 것을 깨닫는다.')
    s.cl('main', 'I', subj='I', verbs=['think', 'but', 'realize'])
    s.cl('subordinate', 'he', subj='he', verbs=['is', 'joking'], marker='that', omitted=True)
    s.cl('subordinate', 'he', subj='he', verbs=['is'], marker='that', omitted=True, occ=1)
    s.g('For|a|moment', 'for a moment', '잠시 동안')
    s.g('I', 'I', '나는', referent_ko='Alyssa')
    s.g('think', 'think', '생각하다')
    s.g('he', 'he', '그가', referent_ko='정장 차림의 남자')
    f = s.g('is', 'be V-ing', '~하고 있다', kind='function', combines_with=[])
    jk = s.g('joking', 'joke', '농담하다', verb_form=pp('ing', s, 'joking', 'joke'))
    link(f, jk)
    s.g('then', 'then', '곧, 그러고 나서')
    s.g('realize', 'realize', '깨닫다')
    s.g('he', 'he', '그가', referent_ko='정장 차림의 남자', at=s.text.index('he is serious'))
    s.g('is', 'is', '~이다', at=s.text.index('is serious'))
    s.g('serious', 'serious', '진지한', star=W['serious'])
    s.hint('[(that) he is joking]', '[그[정장 차림의 남자]가 농담하고 있다고]', span='he is joking',
           label='명사절 접속사 that 생략', display_mode='omitted-conjunction', omitted_conjunction='that',
           links=[(['that'], ['가', '다고'])], refs=[('he', '그', '[정장 차림의 남자]')],
           meaning='그가 농담하고 있다고',
           explanation='think의 목적어인 명사절 앞에 접속사 that이 생략되었다. S′ he, V′ is joking.')
    s.hint('[(that) he is serious]', '[그[정장 차림의 남자]가 진지하다는 것]', span='he is serious',
           label='명사절 접속사 that 생략', display_mode='omitted-conjunction', omitted_conjunction='that',
           links=[(['that'], ['가', '다는 것'])], refs=[('he', '그', '[정장 차림의 남자]')],
           meaning='그가 진지하다는 것',
           explanation='realize의 목적어인 명사절 앞에 접속사 that이 생략되었다. S′ he, V′ is에 be동사의 최소 보어 serious까지 표시.')
    s.review = ('한 주어 I의 두 동사 think와 realize를 but이 연결(then은 부사) + 각각의 목적어 명사절 he is joking / he is serious(둘 다 접속사 that 생략). '
                '생략 that 명사절 힌트 2개. 관계사·수동 없음.')
    out.append(s)

    # ---------------- s63 ----------------
    s = S('s63', T['s63'])
    s.ch('“Excuse me?”', '“뭐라고요?”')
    s.natural('“네? 뭐라고요?”')
    s.cl('imperative', 'Excuse', verbs=['Excuse'])
    s.g('Excuse|me', 'Excuse me?', '뭐라고요?, 네? (놀라거나 어이없어 되묻는 말)')
    s.review = '인용된 관용 표현 Excuse me?(명령문 형태, V: Excuse; 생략된 you는 보충하지 않음). 남자의 말에 놀라 되묻는 말. 절 연결·수동 없음 → 힌트 없음.'
    out.append(s)

    # ---------------- s64 ----------------
    s = S('s64', T['s64'])
    s.ch('He is still smiling,', '그는 여전히 웃고 있다,')
    s.ch('but his eyes scare me.', '하지만 그의 눈이 나를 겁먹게 한다.')
    s.natural('그는 여전히 웃고 있지만, 그의 눈빛이 나를 겁나게 한다.')
    s.cl('main', 'He', subj='He', verbs=['is', 'smiling'])
    s.cl('main', 'his', subj='his eyes', verbs=['scare'], marker='but')
    s.g('He', 'he', '그는', referent_ko='정장 차림의 남자')
    f = s.g('is', 'be V-ing', '~하고 있다', kind='function', combines_with=[])
    s.g('still', 'still', '여전히')
    sm = s.g('smiling', 'smile', '웃다, 미소 짓다', verb_form=pp('ing', s, 'smiling', 'smile'))
    link(f, sm)
    s.g('his', 'his', '그의', referent_ko='정장 차림의 남자')
    s.g('eyes', 'eyes', '눈들, 눈빛')
    s.g('scare', 'scare', '겁먹게 하다, 무섭게 하다')
    s.g('me', 'me', '나를', referent_ko='Alyssa')
    s.review = '두 주절이 but으로 대조(He is still smiling / his eyes scare me). 관계사·수동 없음 → 힌트 없음.'
    out.append(s)

    # ---------------- s65 ----------------
    s = S('s65', T['s65'], key=True)
    s.ch('As long as his hands are firmly locked', '그의 손이 단단히 고정되어 있는 한')
    s.ch('on the handle', '손잡이에')
    s.ch('of our cart,', '우리 카트의,')
    s.ch('there is nothing', '아무것도 없다')
    s.ch('to prove', '증명할')
    s.ch('that it’s ours and not his.', '그것이 그의 것이 아니라 우리의 것이라는 것을.')
    s.natural('그의 손이 우리 카트 손잡이를 단단히 붙잡고 있는 한, 카트가 그의 것이 아니라 우리 것이라는 걸 증명할 방법은 아무것도 없다.')
    s.cl('subordinate', 'As', subj='his hands', verbs=['are', 'locked'], marker='As long as')
    s.cl('main', 'there', subj='nothing to prove that it’s ours and not his', verbs=[], vfirst=['is'], disp='nothing',
         disp_review='중심 대명사 nothing까지 표시하고 뒤에서 꾸미는 to prove … 는 제외(유도부사 there는 주어 아님)')
    its = s.at('it’s')
    s.cl_spans('subordinate', s.at('that')[0], subj=[its[0], its[0] + 2], verbs=[[its[0] + 2, its[1]]], marker='that',
               readings=[{'span': [its[0] + 2, its[1]], 'expanded': 'is'}])
    s.g('As|long|as', 'as long as S′ V′', 'S′(이/가) V′하는 한')
    s.g('his', 'his', '그의', referent_ko='정장 차림의 남자')
    s.g('hands', 'hands', '손들')
    f = s.g('are', 'be p.p.', '~되다', kind='function', combines_with=[])
    s.g('firmly', 'firmly', '단단히, 꽉', star=W['firmly'])
    lk = s.g('locked', 'locked', '(꽉) 고정된 (흔한 뜻: 잠긴)', verb_form=pp('passive-participle', s, 'locked', 'lock', f['id']))
    link(f, lk)
    s.g('on', 'on', '~에')
    s.g('handle', 'handle', '손잡이')
    s.g('of', 'of', '~의')
    s.g('our', 'our', '우리의', referent_ko='Alyssa와 Garrett')
    s.g('cart', 'cart', '카트')
    s.g('is', 'is', '있다')
    s.g('nothing', 'nothing', '아무것도 ~ 않다(없다)')
    ft = s.g('to', 'to V', '~할', kind='function', combines_with=[])
    pr = s.g('prove', 'prove', '증명하다', star=W['prove'])
    link(ft, pr)
    s.g('that', 'that S′ V′', 'S′(이/가) V′라는 것 (접속사)')
    s.g('it’s', 'it’s', '그것이 ~이다 (= it is)', referent_ko='카트')
    s.g('ours', 'ours', '우리의 것', referent_ko='Alyssa와 Garrett')
    s.g('and|not', 'A and not B', 'B가 아니라 A')
    s.g('his', 'his', '그의 것', referent_ko='정장 차림의 남자', at=s.text.index('his.'))
    s.extra_cov[tuple(s.span_of('there'))] = {
        'exemption': 'below-middle1-unneeded', 'level': 'below-middle1',
        'reason': '유도부사 there(초등 기초어)는 따로 해석하지 않으며 뒤 is 각주의 ‘있다’로 뜻을 지원'}
    s.brk('of', 'postnominal-preposition', 'of our cart는 앞 명사 the handle을 뒤에서 꾸미는 전치사구')
    s.hint('[As long as his hands are firmly locked]', '[그[정장 차림의 남자]의 손이 단단히 고정되어 있는 한]',
           span='As long as his hands are firmly locked', label='조건 접속사 as long as',
           links=[(['As long as'], ['이', '는 한'])], refs=[('his', '그', '[정장 차림의 남자]')],
           meaning='그의 손이 단단히 고정되어 있는 한',
           explanation='as long as S′ V′: S′가 V′하는 한(조건). S′ his hands, V′ are firmly locked(사이 부사 보존)까지 표시하고 on the handle 이하는 제외. 수동 are locked는 이 힌트가 있어 분석 보충 u5-gp4로 연결.')
    s.hint('nothing [to prove]', '[증명할] 아무것도', span='nothing to prove', label='to부정사 후치수식',
           links=[(['to'], ['할'])], meaning='증명할 아무것도 (없다)',
           explanation='to prove가 앞 대명사 nothing을 뒤에서 꾸민다(증명할 것). there is nothing과 합치면 ‘증명할 것이 아무것도 없다’. 목적어 that절은 제외.')
    s.review = ('문두 조건 부사절 As long as his hands are firmly locked on the handle of our cart(수동, of 후치수식) + 유도부사 there + is + 주어 nothing to prove …(to부정사 후치수식) '
                '+ prove의 목적어 that 명사절(it’s ours and not his; ’s = is, A and not B). 힌트 2개(as long as절, to부정사 후치수식). that 명사절은 문장당 2개 한도로 힌트 대신 각주·S/V로 지원. '
                'are locked(be p.p.)는 분석 보충 u5-gp4로 연결.')
    out.append(s)

    # ---------------- s66 ----------------
    s = S('s66', T['s66'])
    s.ch('“Is there a problem here?”', '“여기에 문제가 있나요?”')
    s.natural('“무슨 문제라도 있나요?”')
    s.cl('main', 'Is', subj='a problem', verbs=[], vfirst=['Is'])
    s.g('Is|there', 'Is there A?', 'A가 있나요?')
    s.g('problem', 'problem', '문제')
    s.g('here', 'here', '여기에')
    s.review = '인용된 의문문 Is there a problem here?(유도부사 there, 주어 a problem, V Is). 절 연결·수동 없음 → 힌트 없음.'
    out.append(s)

    # ---------------- s67 ----------------
    s = S('s67', T['s67'])
    s.ch('It is Uncle Basil.', '그것은 Basil 삼촌이다.')
    s.natural('그 말을 한 사람은 Basil 삼촌이다.')
    s.cl('main', 'It', subj='It', verbs=['is'])
    s.g('It', 'it', '그것은', referent_ko='“Is there a problem here?”라고 말한 사람')
    s.g('is', 'is', '~이다')
    s.review = '단일 주절(S: It, V: is). It은 방금 말한 사람. Uncle Basil은 s10에서 제공한 고유명사 반복. 힌트 없음.'
    out.append(s)

    # ---------------- s68 ----------------
    s = S('s68', T['s68'])
    s.ch('He has arrived just in time.', '그는 딱 제때에 도착했다.')
    s.natural('삼촌이 마침 딱 맞춰 도착한 것이다.')
    s.cl('main', 'He', subj='He', verbs=['has', 'arrived'])
    s.g('He', 'he', '그는', referent_ko='Basil 삼촌')
    f = s.g('has', 'have p.p.', '~했다', kind='function', combines_with=[])
    ar = s.g('arrived', 'arrive', '도착하다 (arrived는 arrive의 p.p.형)',
             verb_form=pp('perfect-participle', s, 'arrived', 'arrive', f['id']))
    link(f, ar)
    s.g('just|in|time', 'just in time', '딱 제때에, 마침 알맞은 때에')
    s.vf_hint(fn=f, lex=ar, en='has arrived', ko='도착했다', formula='have p.p.', step_form='arrive', step_ko='도착하다',
              en_mark=['has'], ko_mark=['했다'], span='He has arrived', meaning='도착했다',
              explanation='빈 힌트 문장의 능동 완료 후보: has arrived(방금 도착한 결과). 주어 He와 just in time은 제외.')
    s.review = '단일 주절 현재완료 has arrived(능동 완료). 상위 문법 연결 없음 → 능동 완료 기능 결합 힌트.'
    out.append(s)

    # ---------------- s69 ----------------
    s = S('s69', T['s69'])
    s.ch('“Not at all.”', '“전혀 아니에요.”')
    s.natural('“아뇨, 전혀요.”')
    verbless(s, 's68', T['s68'], '66번 질문 “Is there a problem here?”에 대한 남자의 대답(사이에 67·68번 서술이 끼어 있음). 유한동사가 없어 S/V 줄을 생략한다.')
    s.g('Not|at|all', 'not at all', '전혀 아니다')
    s.review = ('유한동사가 없는 대답 표현 Not at all(66번 질문에 대한 남자의 대답). 2026-09-28 사용자 결정으로 S/V 줄과 안내문 생략(verbless-fragment). '
                '문맥 연결 필드는 계약상 바로 앞 s68이며 실제 질문은 s66. 힌트 없음.')
    out.append(s)

    # ---------------- s70 ----------------
    s = S('s70', T['s70'])
    s.ch('The man looks at the ice', '그 남자는 얼음을 바라본다')
    s.ch('with a bitter face,', '씁쓸한 얼굴로,')
    s.ch('then leaves.', '그러고 나서 떠난다.')
    s.natural('남자는 씁쓸한 얼굴로 얼음을 바라보다가 자리를 뜬다.')
    s.cl('main', 'The', subj='The man', verbs=['looks', 'then', 'leaves'])
    s.g('man', 'man', '남자')
    s.g('looks|at', 'look at', '~을 바라보다', verb_form=v3(s, 'looks', 'look', 'The man'))
    s.g('ice', 'ice', '얼음')
    s.g('with', 'with', '~로')
    s.g('bitter', 'bitter', '씁쓸한, 억울해하는 (흔한 뜻: (맛이) 쓴)')
    s.g('face', 'face', '얼굴, 표정')
    s.g('then', 'then', '그러고 나서')
    s.g('leaves', 'leave', '떠나다', verb_form=v3(s, 'leaves', 'leave', 'The man'))
    s.review = ('한 주어 The man의 두 동사 looks와 leaves를 then이 이어 줌(s35와 같은 기준으로 V 표시에 then 보존 — 2026-09-28 사용자 승인 예외, approved-exceptions.md 기록). '
                '관계사·접속사절·수동 없음 → 힌트 없음.')
    out.append(s)

    # ---------------- s71 ----------------
    s = S('s71', T['s71'])
    s.ch('*The above is a shortened version', '*위의 글은 줄인 판이다')
    s.ch('of the opening', '도입부의')
    s.ch('of the novel Dry (2018).', '소설 『Dry』(2018)의.')
    s.natural('*위 글은 소설 『Dry』(2018)의 도입부를 줄인 것이다.')
    s.cl('main', 'The', subj='The above', verbs=['is'])
    s.g('The|above', 'the above', '위의 글, 위의 것')
    s.g('is', 'is', '~이다')
    s.g('shortened', 'shortened', '줄인, 축약된', verb_form=pp('past-participle', s, 'shortened', 'shorten'))
    s.g('version', 'version', '판, 형태')
    s.g('of', 'of', '~의')
    s.g('opening', 'opening', '(작품의) 도입부, 첫 부분 (흔한 뜻: 열기)')
    s.g('of', 'of', '~의', at=s.text.index('of the novel'))
    s.g('novel', 'novel', '소설')
    s.g('Dry', 'Dry', '『Dry』 (드라이, 소설 제목)', proper=True)
    s.brk('of', 'postnominal-preposition', 'of the opening은 앞 명사 a shortened version을 뒤에서 꾸미는 전치사구')
    s.brk('of', 'postnominal-preposition', 'of the novel Dry (2018)는 앞 명사 the opening을 뒤에서 꾸미는 전치사구',
          after=s.text.index('of the novel'))
    s.hint('a shortened version [of the opening]', '[도입부의] 줄인 판', span='a shortened version of the opening',
           label='전치사구 후치수식', links=[(['of'], ['의'])], meaning='도입부의 줄인 판',
           explanation='of the opening이 앞 명사 a shortened version을 뒤에서 꾸민다. of ↔ 의. 뒤의 of the novel Dry도 같은 방식으로 the opening을 꾸민다.')
    s.review = ('작품 소개 단락 첫 문장(원문의 * 표시 보존). 주어 The above + is + 보어 a shortened version of the opening of the novel Dry (2018). '
                'of 후치수식 두 곳 앞에서 끊음. 힌트 1개(of the opening 전치사구 후치수식, of ↔ 의). shortened는 독립 p.p. 각주(줄인, 축약된)로 지원. 관계사·수동 없음.')
    out.append(s)

    # ---------------- s72 ----------------
    s = S('s72', T['s72'])
    s.ch('It tells the story', '그것은 이야기를 들려준다')
    s.ch('of a girl', '한 소녀의')
    s.ch('who has to make tough choices', '힘든 선택들을 해야 하는')
    s.ch('for her family', '그녀의 가족을 위해')
    s.ch('during a disastrous California drought.', '재앙과도 같은 캘리포니아 가뭄 동안.')
    s.natural('이 소설은 재앙과도 같은 캘리포니아 가뭄 속에서 가족을 위해 힘든 선택을 해야 하는 한 소녀의 이야기를 들려준다.')
    s.cl('main', 'It', subj='It', verbs=['tells'])
    s.cl('subject_relative', 'who', verbs=['has'], marker='who')
    s.g('It', 'it', '그것은', referent_ko='소설 『Dry』')
    s.g('tells', 'tell', '들려주다, 말하다', verb_form=v3(s, 'tells', 'tell', 'It'))
    s.g('story', 'story', '이야기')
    s.g('of', 'of', '~의')
    s.g('girl', 'girl', '소녀')
    rel = s.g('who', 'who V′', 'V′하는 (관계대명사)')
    s.g('has|to', 'have to V', '~해야 한다', verb_form=v3(s, 'has', 'have', '관계절 선행사 a girl'))
    s.g('make', 'make', '(선택을) 하다 (흔한 뜻: 만들다)')
    s.g('tough', 'tough', '힘든, 어려운')
    s.g('choices', 'choices', '선택들')
    s.g('for', 'for', '~을 위해')
    s.g('her', 'her', '그녀의', referent_ko='소녀')
    s.g('family', 'family', '가족')
    s.g('during', 'during', '~ 동안')
    s.g('disastrous', 'disastrous', '재앙과도 같은, 처참한', star=W['disastrous'])
    s.g('California', 'California', 'California (캘리포니아, 미국 서부의 주)', proper=True)
    s.g('drought', 'drought', '가뭄')
    s.brk('of', 'postnominal-preposition', 'of a girl은 앞 명사 the story를 뒤에서 꾸미는 전치사구')
    s.hint('a girl [who has to make]', '[해야 하는] 한 소녀', span='a girl who has to make', label='주격 관계대명사 who',
           links=[(['who'], ['는'])], meaning='(가족을 위해 힘든 선택을) 해야 하는 한 소녀',
           explanation='선행사 a girl을 주격 관계대명사 who가 받는다. 주격이라 별도 S′ 없이 V′ has(has to make: ~해야 한다)까지 표시하고 목적어 tough choices는 제외.')
    s.relative_ids = [rel['id']]
    s.review = ('주절 It tells the story of a girl(It = 소설 Dry) + 주격 관계대명사 who절(has to make tough choices for her family during a disastrous California drought). '
                'S/V의 V′는 has(have to의 has; be able to처럼 뒤 부정사는 제외). 필수 관계사 힌트 1개. 수동 없음.')
    out.append(s)

    # ---------------- s73 ----------------
    s = S('s73', T['s73'])
    s.ch('Her unwanted adventure ends', '그녀의 원치 않는 모험은 끝난다')
    s.ch('when the water supply resumes', '물 공급이 재개될 때')
    s.ch('and life is back to normal.', '그리고 생활이 정상으로 돌아올 (때).')
    s.natural('물 공급이 다시 시작되고 생활이 정상으로 돌아오면서 소녀의 원치 않던 모험은 끝이 난다.')
    s.cl('main', 'Her', subj='Her unwanted adventure', verbs=['ends'])
    s.cl('subordinate', 'when', subj='the water supply', verbs=['resumes'], marker='when')
    s.cl('subordinate', 'life', subj='life', verbs=['is'], marker='and')
    s.g('Her', 'her', '그녀의', referent_ko='소설 속 소녀')
    s.g('unwanted', 'unwanted', '원치 않는')
    s.g('adventure', 'adventure', '모험')
    s.g('ends', 'end', '끝나다', verb_form=v3(s, 'ends', 'end', 'Her unwanted adventure'))
    s.g('when', 'when S′ V′', 'S′(이/가) V′할 때')
    s.g('water|supply', 'water supply', '물 공급')
    s.g('resumes', 'resume', '재개되다, 다시 시작되다', star=W['resume'], verb_form=v3(s, 'resumes', 'resume', 'the water supply'))
    s.g('life', 'life', '생활, 삶')
    s.g('is|back|to|normal', 'be back to normal', '정상으로 돌아오다')
    s.hint('[when the water supply resumes]', '[물 공급이 재개될 때]', span='when the water supply resumes',
           label='시간 접속사 when', links=[(['when'], ['이', '때'])], meaning='물 공급이 재개될 때',
           explanation='when S′ V′: S′가 V′할 때. S′ the water supply, V′ resumes. and 뒤 life is back to normal도 같은 when에 걸리는 두 번째 절(생활이 정상으로 돌아올 때).')
    s.review = ('주절 Her unwanted adventure ends + when절 두 개가 and로 병렬(the water supply resumes / life is back to normal — 둘 다 when에 걸림, 뒤 절은 [and] S′·V′로 표시). '
                'be back to normal은 be 숙어. 힌트 1개(when절). 관계사·수동 없음.')
    out.append(s)

    # ---------------- s74 ----------------
    s = S('s74', T['s74'], key=True)
    s.ch('Provided that the factors', '만약 요인들이')
    s.ch('contributing to water shortages worldwide', '전 세계적으로 물 부족의 원인이 되는')
    s.ch('are not addressed,', '해결되지 않는다면,')
    s.ch('including climate change, population growth,', '기후 변화, 인구 증가를 포함하여,')
    s.ch('and using too much water for agriculture,', '그리고 농업을 위해 너무 많은 물을 사용하는 것(을 포함하여),')
    s.ch('it is possible that this story can become a reality.', '이 이야기가 현실이 될 수 있을 가능성이 있다.')
    s.natural('기후 변화, 인구 증가, 농업용수 과다 사용처럼 전 세계적으로 물 부족을 일으키는 요인들이 해결되지 않는다면, 이 이야기는 현실이 될 수도 있다.')
    s.cl('subordinate', 'Provided', subj='the factors contributing to water shortages worldwide', verbs=['are', 'addressed'],
         marker='Provided that', disp='the factors',
         disp_review='중심명사 factors까지 표시하고 뒤에서 꾸미는 현재분사구 contributing to water shortages worldwide는 제외')
    s.cl('main', 'it', subj='it', verbs=['is'])
    s.cl('subordinate', 'that', subj='this story', verbs=['can', 'become'], marker='that', occ=1)
    s.g('Provided|that', 'provided that S′ V′', 'S′(이/가) V′한다면 (= if)')
    s.g('factors', 'factors', '요인들', star=W['factor'])
    f = s.g('contributing', 'V-ing', '~하는', kind='function', combines_with=[])
    ct = s.g('contributing', 'contribute', '(원인이 되어) 기여하다', same=True, verb_form=pp('ing', s, 'contributing', 'contribute'))
    link(f, ct)
    s.g('to', 'to', '~에')
    s.g('water|shortages', 'water shortages', '물 부족', star=W['shortage'])
    s.g('worldwide', 'worldwide', '전 세계적으로')
    fn = s.g('are|not', 'be not p.p.', '~되지 않다', kind='function', combines_with=[])
    ad = s.g('addressed', 'addressed', '(문제가) 해결된, 다뤄진 (흔한 뜻: 주소)', star=W['address'],
             verb_form=pp('passive-participle', s, 'addressed', 'address', fn['id']))
    link(fn, ad)
    s.g('including', 'including', '~을 포함하여')
    s.g('climate|change', 'climate change', '기후 변화')
    s.g('population', 'population', '인구')
    s.g('growth', 'growth', '증가, 성장')
    fu = s.g('using', 'V-ing', '~하는 것', kind='function', combines_with=[])
    us = s.g('using', 'use', '사용하다', same=True, verb_form=pp('ing', s, 'using', 'use'))
    link(fu, us)
    s.g('too|much', 'too much', '너무 많은')
    s.g('water', 'water', '물', at=s.text.index('water for'))
    s.g('for', 'for', '~을 위해')
    s.g('agriculture', 'agriculture', '농업')
    it = s.g('it is possible that', 'It is possible that S′ V′', 'S′(이/가) V′할 가능성이 있다 (It은 뒤의 that절을 대신함)')
    s.g('this', 'this', '이')
    s.g('story', 'story', '이야기')
    fc = s.g('can', 'can V', '~할 수 있다', kind='function', combines_with=[])
    bc = s.g('become', 'become', '~이 되다')
    link(fc, bc)
    s.g('reality', 'reality', '현실')
    s.prot('it is possible that', 'dummy-it-prefix', '가주어 It과 진주어 that절(It is possible that S′ V′)은 It부터 that까지 끊지 않음', gloss=it)
    s.hint('[Provided that the factors contributing to water shortages worldwide are not addressed]',
           '[전 세계적으로 물 부족의 원인이 되는 요인들이 해결되지 않는다면]',
           span='Provided that the factors contributing to water shortages worldwide are not addressed', label='조건 접속사 provided that',
           links=[(['Provided that'], [('이', 1), '는다면'])],
           meaning='전 세계적으로 물 부족의 원인이 되는 요인들이 해결되지 않는다면',
           explanation='provided that S′ V′ = if S′ V′(~한다면). S′ the factors(현재분사구 contributing … worldwide가 꾸밈), V′ are not addressed(수동 부정). including 이하는 the factors의 예시로 표시에서 제외. 수동 are not addressed는 분석 보충 u5-gp5로 연결.')
    s.hint('it is possible that [this story can become a reality]', '[이 이야기가 현실이 될 수 있을] 가능성이 있다',
           span='it is possible that this story can become a reality', label='가주어 It과 진주어 that절',
           links=[(['that'], ['가', '을'])], meaning='이 이야기가 현실이 될 수 있을 가능성이 있다',
           explanation='가주어 it이 뒤의 that절을 대신한다. that절 S′ this story, V′ can become에 연결동사의 최소 보어 a reality까지 표시.')
    s.review = ('조건 부사절 Provided that the factors contributing to water shortages worldwide are not addressed(현재분사 후치수식, 수동 부정) '
                '+ the factors의 예시 including climate change, population growth, and using too much water for agriculture(동명사 using 포함) '
                '+ 주절 가주어 it is possible that this story can become a reality(It~that 끊지 않음). 힌트 2개(provided that절, 가주어–that절). '
                'are not addressed(be not p.p.)는 분석 보충 u5-gp5로 연결. 관계사 없음.')
    out.append(s)
    return out


UNIT = {
    'id': 'u5', 'source_id': 'src', 'paragraph_ids': ['p26', 'p27', 'p28', 'p29', 'p30', 'p31', 'p32'],
    'sentence_ids': [f's{n:02d}' for n in range(62, 75)],
    'today_words': [
        {'id': W['serious'], 'text': 'serious', 'meaning_ko': '진지한'},
        {'id': W['firmly'], 'text': 'firmly', 'meaning_ko': '단단히, 꽉'},
        {'id': W['prove'], 'text': 'prove', 'meaning_ko': '증명하다'},
        {'id': W['disastrous'], 'text': 'disastrous', 'meaning_ko': '재앙과도 같은, 처참한'},
        {'id': W['resume'], 'text': 'resume', 'meaning_ko': '재개되다, 다시 시작되다'},
        {'id': W['factor'], 'text': 'factor', 'meaning_ko': '요인'},
        {'id': W['shortage'], 'text': 'water shortage', 'meaning_ko': '물 부족'},
        {'id': W['address'], 'text': 'addressed', 'meaning_ko': '(문제가) 해결된, 다뤄진'},
    ],
}


def analysis(_):
    return {
        'heading_kind': '제목',
        'title_or_topic_en': 'Timely Help and a Warning',
        'title_or_topic_ko': '때맞춘 도움, 그리고 경고',
        'intent_ko': 'Basil 삼촌이 제때 나타나 남자가 얼음을 가져가지 못하고 떠나는 장면으로 소설 도입부 발췌가 끝난다. 이어서 작품 소개를 통해 물 부족의 원인이 해결되지 않으면 이 소설 속 가뭄이 현실이 될 수 있다고 경고한다.',
        'flow': [
            {'sentence_ids': ['s62', 's63', 's64', 's65'], 'label': '위협',
             'text_ko': 'Alyssa는 처음에 남자가 농담한다고 생각하지만 곧 진지하다는 것을 깨닫는다. 남자는 웃고 있지만 눈빛이 무섭고, 그가 카트 손잡이를 쥐고 있는 한 카트가 아이들 것임을 증명할 방법이 없다.'},
            {'sentence_ids': ['s66', 's67', 's68', 's69', 's70'], 'label': '해결',
             'text_ko': '그때 Basil 삼촌이 나타나 무슨 문제가 있느냐고 묻는다. 남자는 전혀 아니라고 하고는 씁쓸한 얼굴로 얼음을 바라보다 떠난다.'},
            {'sentence_ids': ['s71', 's72', 's73', 's74'], 'label': '작품 소개',
             'text_ko': '이 글은 소설 『Dry』의 도입부를 줄인 것으로, 가뭄 속에서 가족을 위해 힘든 선택을 해야 하는 소녀의 이야기다. 물 공급이 다시 시작되며 모험은 끝나지만, 물 부족의 원인이 해결되지 않으면 이 이야기는 현실이 될 수 있다.'},
        ],
        'easy_explanations': [
            {'sentence_id': 's65', 'explanatory_sentences': [
                '65번 문장은 64번에서 무서워진 Alyssa가 왜 겁이 나는지 보여 준다.',
                '남자는 카트 손잡이를 꽉 붙잡고 있다.',
                '카트를 붙잡고 있는 사람이 주인처럼 보이기 쉽다.',
                '카트가 아이들 것이라는 증거는 따로 없다.',
                '그래서 남자가 손잡이를 놓지 않는 한 아이들은 얼음이 담긴 카트를 지키기 어렵다.']},
            {'sentence_id': 's70', 'explanatory_sentences': [
                '70번 문장은 삼촌이 나타난 뒤 남자의 반응이다.',
                '69번에서 남자는 문제가 전혀 없다고 대답했다.',
                '하지만 남자는 얼음을 놓치게 되어 억울하고 아쉬운 얼굴로 얼음을 바라본다.',
                '어른인 삼촌 앞에서는 아이들의 얼음을 가져갈 수 없어서 결국 떠난다.']},
            {'sentence_id': 's74', 'explanatory_sentences': [
                '74번 문장은 작품 소개의 마지막 문장으로, 글 전체가 전하려는 경고다.',
                '실제 세계에서도 물이 부족해지는 원인들이 있다.',
                '기후 변화, 늘어나는 인구, 농사에 물을 너무 많이 쓰는 일이 그 예다.',
                '이런 원인을 해결하지 않으면 소설 속 가뭄 이야기가 우리 현실이 될 수도 있다.']},
        ],
        'grammar_points': [
            {'id': 'u5-gp1', 'sentence_id': 's65', 'span': 'As long as his hands are firmly locked on the handle of our cart',
             'title': 'as long as S′ V′: S′가 V′하는 한', 'formula_key': 'as long as S′ V′',
             'explanation': '공식: as long as S′ V′ — S′(이/가) V′하는 한. S′ = his hands(그의 손), V′ = are firmly locked(단단히 고정되어 있다), '
                            'on the handle of our cart = 우리 카트의 손잡이에. → 그의 손이 우리 카트의 손잡이에 단단히 고정되어 있는 한. '
                            '‘~하는 동안에는 계속’이라는 조건을 나타내며, 뒤 주절(증명할 방법이 없다)이 그 조건 아래에서 성립한다.',
             'practice': {'span': 'As long as his hands are firmly locked on the handle of our cart',
                          'formula_support': {'en': 'as long as S′ V′', 'ko': 'S′(이/가) V′하는 한'},
                          'support': [('s65', 'his'), ('s65', 'hands'), ('s65', 'be p.p.'), ('s65', 'firmly'), ('s65', 'locked'),
                                      ('s65', 'on'), ('s65', 'handle'), ('s65', 'of'), ('s65', 'our'), ('s65', 'cart')],
                          'answer_ko': '그의 손이 우리 카트의 손잡이에 단단히 고정되어 있는 한'}},
            {'id': 'u5-gp2', 'sentence_id': 's72', 'span': 'a girl who has to make tough choices for her family',
             'title': '명사 + who V′: V′하는 명사', 'formula_key': 'N + who V′',
             'explanation': '공식: 명사(N) + who V′ — V′하는 N. N = a girl(한 소녀), who = 주격 관계대명사(그 소녀가), V′ = has(S/V 표시; has to make = 해야 하다, have to V = ~해야 한다, make = 하다), '
                            'tough choices = 힘든 선택들, for her family = 그녀의 가족을 위해. → 그녀의 가족을 위해 힘든 선택들을 해야 하는 한 소녀.',
             'practice': {'span': 'a girl who has to make tough choices for her family',
                          'formula_support': {'en': 'N + who V′', 'ko': 'V′하는 N'},
                          'support': [('s72', 'girl'), ('s72', 'have to V'), ('s72', 'make'), ('s72', 'tough'), ('s72', 'choices'),
                                      ('s72', 'for'), ('s72', 'her'), ('s72', 'family')],
                          'answer_ko': '그녀의 가족을 위해 힘든 선택들을 해야 하는 한 소녀'}},
            {'id': 'u5-gp3', 'sentence_id': 's74', 'span': 'Provided that the factors contributing to water shortages worldwide are not addressed',
             'title': 'provided that S′ V′: S′가 V′한다면', 'formula_key': 'provided that S′ V′',
             'explanation': '공식: provided that S′ V′ — S′(이/가) V′한다면(= if). S′ = the factors(요인들), 이를 꾸미는 contributing to water shortages worldwide = 전 세계적으로 물 부족의 원인이 되는, '
                            'V′ = are not addressed(해결되지 않다). → 전 세계적으로 물 부족의 원인이 되는 요인들이 해결되지 않는다면.',
             'practice': {'span': 'Provided that the factors contributing to water shortages worldwide are not addressed',
                          'formula_support': {'en': 'provided that S′ V′', 'ko': 'S′(이/가) V′한다면'},
                          'support': [('s74', 'factors'), ('s74', 'V-ing'), ('s74', 'contribute'), ('s74', 'to'), ('s74', 'water shortages'),
                                      ('s74', 'worldwide'), ('s74', 'be not p.p.'), ('s74', 'addressed')],
                          'answer_ko': '전 세계적으로 물 부족의 원인이 되는 요인들이 해결되지 않는다면'}},
            {'id': 'u5-gp4', 'sentence_id': 's65', 'span': 'his hands are firmly locked',
             'title': 'be p.p.: ~되다 (are locked: 고정되어 있다)', 'formula_key': 'be p.p.',
             'explanation': '공식: be p.p. — ~되다. be = are(현재), p.p. = locked(고정된, lock의 p.p.형), 사이의 firmly = 단단히. '
                            '→ are firmly locked = 단단히 고정되어 있다. 주어 his hands가 무엇을 고정하는 것이 아니라 손잡이에 ‘고정된’ 상태이므로 수동(be p.p.)을 쓴다. 주어 his hands와 합치면 ‘그의 손이 단단히 고정되어 있다’.',
             'supplemental': {'function': ('s65', 'be p.p.', 0),
                              'reason': 's65의 수동 are firmly locked는 as long as절·to부정사 후치수식 힌트가 이미 있어 결합 힌트로 선정하지 않았고, 기본 분석 3개에 be p.p. 설명이 없어 이 단위 대표 사례로 1회 보충'},
             'practice': {'span': 'his hands are firmly locked',
                          'formula_support': {'en': 'be p.p.', 'ko': '~되다'},
                          'support': [('s65', 'his'), ('s65', 'hands'), ('s65', 'firmly'), ('s65', 'locked')],
                          'answer_ko': '그의 손이 단단히 고정되어 있다'}},
            {'id': 'u5-gp5', 'sentence_id': 's74', 'span': 'the factors contributing to water shortages worldwide are not addressed',
             'title': 'be not p.p.: ~되지 않다 (are not addressed: 해결되지 않다)', 'formula_key': 'be not p.p.',
             'explanation': '공식: be not p.p. — ~되지 않다. be = are(현재), not = 부정, p.p. = addressed(해결된, address의 p.p.형). '
                            '→ are not addressed = 해결되지 않다. 요인들은 사람들이 ‘해결해야 하는’ 대상이라 수동을 쓴다. 주어 the factors와 합치면 ‘요인들이 해결되지 않는다’.',
             'supplemental': {'function': ('s74', 'be not p.p.', 0),
                              'reason': 's74의 수동 부정 are not addressed는 provided that절·가주어 힌트가 이미 있어 결합 힌트로 선정하지 않았고, 기본 분석 3개와 u5-gp4(be p.p.)와 다른 공식이라 이 단위 대표 사례로 1회 보충'},
             'practice': {'span': 'the factors contributing to water shortages worldwide are not addressed',
                          'formula_support': {'en': 'be not p.p.', 'ko': '~되지 않다'},
                          'support': [('s74', 'factors'), ('s74', 'V-ing'), ('s74', 'contribute'), ('s74', 'to'),
                                      ('s74', 'water shortages'), ('s74', 'worldwide'), ('s74', 'addressed')],
                          'answer_ko': '전 세계적으로 물 부족의 원인이 되는 요인들이 해결되지 않는다'}},
        ],
        'formula_routes': [
            {'function': ('s65', 'be p.p.', 0), 'route': 'analysis', 'grammar_point_id': 'u5-gp4',
             'review_record': 'are firmly locked: as long as절·to부정사 힌트가 있어 분석 보충 u5-gp4로 연결'},
            {'function': ('s68', 'have p.p.', 0), 'route': 'hint', 'hint_index': 0,
             'review_record': 'has arrived: 빈 힌트 문장의 능동 완료 기능 결합 힌트'},
            {'function': ('s74', 'be not p.p.', 0), 'route': 'analysis', 'grammar_point_id': 'u5-gp5',
             'review_record': 'are not addressed: provided that절·가주어 힌트가 있어 분석 보충 u5-gp5로 연결'},
        ],
        'relations': [
            {'head': {'id': 'u5-r1h', 'text': 'serious', 'meaning_ko': '진지한'},
             'synonym': {'id': 'u5-r1s', 'text': 'earnest', 'meaning_ko': '진지한, 진심 어린'},
             'antonym': {'id': 'u5-r1a', 'text': 'playful', 'meaning_ko': '장난스러운, 장난기 있는'}},
            {'head': {'id': 'u5-r2h', 'text': 'resume', 'meaning_ko': '재개되다, 다시 시작되다'},
             'synonym': {'id': 'u5-r2s', 'text': 'restart', 'meaning_ko': '다시 시작되다'},
             'antonym': {'id': 'u5-r2a', 'text': 'halt', 'meaning_ko': '멈추다, 중단되다'}},
            {'head': {'id': 'u5-r3h', 'text': 'growth', 'meaning_ko': '증가, 성장'},
             'synonym': {'id': 'u5-r3s', 'text': 'increase', 'meaning_ko': '증가'},
             'antonym': {'id': 'u5-r3a', 'text': 'decline', 'meaning_ko': '감소, 하락'}},
        ],
    }


def workbook():
    return {
        'relation_order': ['u5-r2s', 'u5-r3a', 'u5-r1h', 'u5-r2a', 'u5-r3s', 'u5-r1s', 'u5-r2h', 'u5-r1a', 'u5-r3h'],
        'key_sentence_ids': ['s65', 's74'],
        'question_id': 'Q05',
        'syntax_point_ids': ['u5-gp1', 'u5-gp2', 'u5-gp3', 'u5-gp4', 'u5-gp5'],
    }
