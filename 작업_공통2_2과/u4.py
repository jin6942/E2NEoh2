"""공통 단위 4: s47~s61 (p20~p25) — 도와주겠다던 정장 차림 남자의 속셈.

사용자 결정(2026-09-28 “5단위, 작품 소개 합침”): 무소제목 소설 본문을 장면 기준으로 묶은 넷째 단위.
2026-09-28 사용자 결정 “50번 V만, 52번 전달절만”: s50은 주어 It 생략 구어라 V만, s52는 인사 관용 표현 Thank you를 S/V에서 제외.
"""
from author import S, link, verbless

W = {'ridiculously': 'u4-w1', 'impossible': 'u4-w2', 'suit': 'u4-w3', 'bring_out': 'u4-w4',
     'favor': 'u4-w5', 'deserve': 'u4-w6', 'fade': 'u4-w7', 'rest': 'u4-w8'}


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

    # ---------------- s47 ----------------
    s = S('s47', T['s47'])
    s.ch('The cart is ridiculously heavy now,', '카트는 이제 터무니없이 무겁다,')
    s.ch('and almost impossible', '그리고 거의 불가능하다')
    s.ch('to push.', '밀기에.')
    s.natural('카트는 이제 말도 안 되게 무거워서 밀기가 거의 불가능하다.')
    s.cl('main', 'The', subj='The cart', verbs=['is'])
    s.g('cart', 'cart', '카트')
    s.g('is', 'is', '~이다')
    s.g('ridiculously', 'ridiculously', '터무니없이, 어처구니없을 만큼', star=W['ridiculously'])
    s.g('heavy', 'heavy', '무거운')
    s.g('now', 'now', '이제')
    s.g('almost', 'almost', '거의')
    s.g('impossible', 'impossible', '불가능한', star=W['impossible'])
    f = s.g('to', 'to V', '~하기에', kind='function', combines_with=[])
    ps = s.g('push', 'push', '밀다')
    link(f, ps)
    s.hint('almost impossible [to push]', '[밀기에] 거의 불가능한', span='almost impossible to push', label='형용사를 꾸미는 to부정사',
           links=[(['to'], ['기에'])], meaning='밀기에 거의 불가능한',
           explanation='to push가 형용사 impossible을 뒤에서 꾸며 ‘밀기에 불가능한’. heavy와 impossible이 is의 보어로 and로 병렬.')
    s.review = ('단일 주절 The cart is + 병렬 보어 ridiculously heavy now, and almost impossible to push. to push는 형용사 impossible을 꾸미는 to부정사(~하기에). '
                '힌트 1개. 관계사·수동 없음.')
    out.append(s)

    # ---------------- s48 ----------------
    s = S('s48', T['s48'])
    s.ch('Then,', '그때,')
    s.ch('a man', '한 남자가')
    s.ch('in a business suit', '정장을 입은')
    s.ch('comes up behind us.', '우리 뒤로 다가온다.')
    s.natural('그때 정장 차림의 한 남자가 우리 뒤로 다가온다.')
    s.cl('main', 'a', subj='a man in a business suit', verbs=['comes'], disp='a man',
         disp_review='중심명사 man까지 표시하고 뒤에서 꾸미는 in a business suit는 제외')
    s.g('Then', 'then', '그때')
    s.g('man', 'man', '남자')
    s.g('in', 'in', '~을 입은')
    s.g('business|suit', 'business suit', '(사무용) 정장', star=W['suit'])
    s.g('comes|up', 'come up', '다가오다', verb_form=v3(s, 'comes', 'come', 'a man'))
    s.g('behind', 'behind', '~ 뒤로')
    s.g('us', 'us', '우리', referent_ko='Alyssa와 Garrett')
    s.brk('in', 'postnominal-preposition', 'in a business suit는 앞 명사 a man을 뒤에서 꾸미는 전치사구')
    s.hint('a man [in a business suit]', '[정장을 입은] 한 남자', span='a man in a business suit', label='전치사구 후치수식',
           links=[(['in'], ['을 입은'])], meaning='정장을 입은 한 남자',
           explanation='in a business suit(정장을 입은)가 앞 명사 a man을 뒤에서 꾸민다. 옷차림 앞의 in은 ‘~을 입은’.')
    s.review = ('단일 주절: 주어 a man in a business suit(표시는 a man) + V comes (up behind us). in 후치수식 앞에서 끊음. 힌트 1개. '
                '관계사·수동 없음.')
    out.append(s)

    # ---------------- s49 ----------------
    s = S('s49', T['s49'])
    s.ch('He smiles.', '그는 미소 짓는다.')
    s.natural('그는 미소를 짓는다.')
    s.cl('main', 'He', subj='He', verbs=['smiles'])
    s.g('He', 'he', '그는', referent_ko='정장 차림의 남자')
    s.g('smiles', 'smile', '미소 짓다', verb_form=v3(s, 'smiles', 'smile', 'He'))
    s.review = '단일 주절(S: He, V: smiles). 절 연결·수동 없음 → 힌트 없음.'
    out.append(s)

    # ---------------- s50 ----------------
    s = S('s50', T['s50'])
    s.ch('“Looks like', '“보아하니')
    s.ch('you could use some help.”', '너희가 도움이 좀 필요한 것 같구나.”')
    s.natural('“도움이 좀 필요한 것 같구나.”')
    s.cl('imperative', 'Looks', verbs=['Looks'])
    s.cl('subordinate', 'you', subj='you', verbs=['could', 'use'], marker='like')
    s.g('Looks|like', 'look like S′ V′', 'S′(이/가) V′하는 것 같다',
        verb_form=v3(s, 'Looks', 'look', '생략된 It'))
    s.g('could|use', 'could use', '~이 필요하다, ~이 있으면 좋겠다')
    s.g('some', 'some', '약간의, 좀')
    s.g('help', 'help', '도움')
    s.hint('[Looks like you could use]', '[너희[Alyssa와 Garrett]가 필요로 할 것 같다]', span='Looks like you could use',
           label='주어 It이 생략된 look like', links=[(['like'], ['가', '것 같다'])], refs=[('you', '너희', '[Alyssa와 Garrett]')],
           meaning='너희가 (도움을 좀) 필요로 할 것 같다',
           explanation='구어에서 It이 생략된 (It) looks like S′ V′: S′가 V′하는 것 같다. like는 접속사로 뒤 절 you could use를 이끈다. could use A = A가 필요하다. 목적어 some help는 제외.')
    s.review = ('주어 It이 생략된 구어 (It) Looks like + 접속사 like절(you could use some help; could use = ~이 필요하다). '
                '2026-09-28 사용자 결정으로 S/V는 명령문 표시 방식(주어 칸 없이 V만): V: Looks — 절 종류 imperative는 표시 장치상 기록이며 실제로는 주어 It 생략 구어(명령문 아님). '
                'like절은 [like] S′: you, V′: could use. 힌트 1개(생략 It의 look like 절 연결). 관계사·수동 없음.')
    out.append(s)

    # ---------------- s51 ----------------
    s = S('s51', T['s51'])
    s.ch('He doesn’t wait', '그는 기다리지 않는다')
    s.ch('for us to answer', '우리가 대답하기를')
    s.ch('before grabbing the cart’s handle.', '카트의 손잡이를 잡기 전에.')
    s.natural('그는 우리가 대답하기도 전에 카트 손잡이를 잡는다.')
    s.cl('main', 'He', subj='He', verbs=['doesn’t', 'wait'])
    s.g('He', 'he', '그는', referent_ko='정장 차림의 남자')
    fd = s.g('doesn’t', 'doesn’t V', '~하지 않는다 (= does not)', kind='function', combines_with=[])
    wt = s.g('wait|for|to', 'wait for A to V', 'A가 ~하기를 기다리다',
             verb_construction={'kind': 'verb-frame', 'verb_span': s.span_of('wait'), 'lemma': 'wait',
                                'link_spans': [s.span_of('for'), s.span_of('to')],
                                'review_record': 'wait for us to answer: A = us, V = answer.'})
    link(fd, wt)
    s.g('us', 'us', '우리가', referent_ko='Alyssa와 Garrett')
    s.g('answer', 'answer', '대답하다')
    fb = s.g('before', 'before V-ing', '~하기 전에', kind='function', combines_with=[])
    gb = s.g('grabbing', 'grab', '(갑자기) 잡다, 움켜쥐다', verb_form=pp('ing', s, 'grabbing', 'grab'))
    link(fb, gb)
    s.g('cart’s', 'cart’s', '카트의')
    s.g('handle', 'handle', '손잡이')
    s.hint('[before grabbing]', '[잡기 전에]', span='before grabbing', label='전치사 before + 동명사',
           links=[(['before', 'ing'], ['기 전에'])], meaning='(카트 손잡이를) 잡기 전에',
           explanation='전치사 before 뒤 동명사 grabbing: ~하기 전에. 목적어 the cart’s handle은 제외. 부정 doesn’t wait … before …는 ‘~하기 전에 기다리지 않는다’ → ‘대답도 하기 전에 잡는다’.')
    s.hint('doesn’t wait [for us to answer]', '[우리[Alyssa와 Garrett]가 대답하기를] 기다리지 않는다', span='doesn’t wait for us to answer',
           label='wait for A to V 구문', emphasis_policy='ko-only-verb-construction',
           links=[(['for', 'to'], ['가', '기를'])], refs=[('us', '우리', '[Alyssa와 Garrett]')],
           meaning='우리가 대답하기를 기다리지 않는다',
           explanation='wait for A to V: A가 ~하기를 기다리다. A = us(우리), V = answer. A 주어 조사 가와 연결 어미 기를만 강조(동사 구문, 후순위).')
    s.review = ('단일 주절 He doesn’t wait(doesn’t = does not) + wait for A to V(A = us) + 전치사 before + 동명사 grabbing. '
                '힌트 2개(before V-ing 우선, wait for A to V 동사 구문 후순위). 관계사·수동 없음.')
    out.append(s)

    # ---------------- s52 ----------------
    s = S('s52', T['s52'])
    s.ch('“Thank you for helping us,”', '“우리를 도와줘서 고마워요,”')
    s.ch('I tell him.', '나는 그에게 말한다.')
    s.natural('“도와주셔서 감사합니다.” 내가 그에게 말한다.')
    s.cl('main', 'I', subj='I', verbs=['tell'])
    s.g('Thank|you|for', 'thank you for V-ing', '~해 줘서 고마워요')
    s.g('helping', 'help', '돕다', verb_form=pp('ing', s, 'helping', 'help'))
    s.g('us', 'us', '우리를', referent_ko='Alyssa와 Garrett')
    s.g('I', 'I', '나는', referent_ko='Alyssa')
    s.g('tell', 'tell', '말하다')
    s.g('him', 'him', '그에게', referent_ko='정장 차림의 남자')
    s.review = ('인용 “Thank you for helping us,”(인사 관용 표현, thank you for V-ing가 V-ing 연결 뜻을 제공) + 전달절 I tell him. '
                '2026-09-28 사용자 결정 “52번 전달절만”으로 S/V는 전달절(S: I, V: tell)만 표시. 관계사·접속사절·수동 없음 → 힌트 없음.')
    out.append(s)

    # ---------------- s53 ----------------
    s = S('s53', T['s53'])
    s.ch('“Not a problem.', '“문제없어.')
    s.natural('“별거 아니야.')
    verbless(s, 's52', T['s52'], '고맙다는 인사(s52)에 대한 짧은 대답 명사구 Not a problem. 유한동사가 없어 S/V 줄을 생략한다.')
    s.g('Not|a|problem', 'not a problem', '별거 아니야, 괜찮아')
    s.review = ('유한동사가 없는 대답 표현(Not a problem). 2026-09-28 사용자 결정으로 S/V 줄과 안내문 생략(verbless-fragment). '
                '인용문 안의 마침표에서 문장을 나눔(s54로 인용 계속). 힌트 없음.')
    out.append(s)

    # ---------------- s54 ----------------
    s = S('s54', T['s54'])
    s.ch('We all need to help one another.”', '우리는 모두 서로를 도울 필요가 있어.”')
    s.natural('우리 모두 서로 도와야지.”')
    s.cl('main', 'We', subj='We', verbs=['need'])
    s.g('We', 'we', '우리는', referent_ko='모든 사람')
    s.g('all', 'all', '모두')
    s.g('need|to', 'need to V', '~할 필요가 있다, ~해야 한다',
        verb_construction={'kind': 'to-complement', 'verb_span': s.span_of('need'), 'lemma': 'need',
                           'link_spans': [s.span_of('to')], 'review_record': 'need to help: need의 목적어 to V.'})
    s.g('help', 'help', '돕다')
    s.g('one|another', 'one another', '서로')
    s.review = '앞 s53에서 이어지는 인용의 마지막 조각. 단일 절 We all need to help one another(all은 We와 동격). 절 연결·수동 없음 → 힌트 없음.'
    out.append(s)

    # ---------------- s55 ----------------
    s = S('s55', T['s55'])
    s.ch('He smiles again,', '그는 다시 미소 짓는다,')
    s.ch('and I return the smile.', '그리고 나는 미소로 답한다.')
    s.natural('그가 다시 미소를 짓고, 나도 미소로 답한다.')
    s.cl('main', 'He', subj='He', verbs=['smiles'])
    s.cl('main', 'I', subj='I', verbs=['return'], marker='and')
    s.g('He', 'he', '그는', referent_ko='정장 차림의 남자')
    s.g('smiles', 'smile', '미소 짓다', verb_form=v3(s, 'smiles', 'smile', 'He'))
    s.g('again', 'again', '다시')
    s.g('I', 'I', '나는', referent_ko='Alyssa')
    s.g('return|the|smile', 'return the smile', '(상대의) 미소에 미소로 답하다')
    s.review = '두 주절이 and로 연결(He smiles again / I return the smile). 관계사·수동 없음 → 힌트 없음.'
    out.append(s)

    # ---------------- s56 ----------------
    s = S('s56', T['s56'], key=True)
    s.ch('It is good', '좋다')
    s.ch('to know', '아는 것은')
    s.ch('that difficult times can bring out the best', '어려운 시기가 가장 좋은 면을 끌어낼 수 있다는 것을')
    s.ch('in people.', '사람들 안에 있는.')
    s.natural('어려운 시기가 사람들의 가장 좋은 면을 끌어낼 수 있다는 것을 알게 되니 좋다.')
    s.cl('main', 'It', subj='It', verbs=['is'])
    s.cl('subordinate', 'that', subj='difficult times', verbs=['can', 'bring'], marker='that')
    s.g('It|to', 'It … to V', '~하는 것은 (It은 뒤의 to V를 대신함)')
    s.g('is', 'is', '~이다')
    s.g('good', 'good', '좋은')
    s.g('know', 'know', '알다')
    s.g('that', 'that S′ V′', 'S′(이/가) V′라는 것 (접속사)')
    s.g('difficult', 'difficult', '어려운')
    s.g('times', 'times', '시기, 때 (흔한 뜻: 시간)')
    fc = s.g('can', 'can V', '~할 수 있다', kind='function', combines_with=[])
    bo = s.g('bring|out', 'bring out', '(좋은 점을) 끌어내다, 드러나게 하다', star=W['bring_out'])
    link(fc, bo)
    s.g('the|best', 'the best', '가장 좋은 면, 최선')
    s.g('in', 'in', '~ 안에 있는')
    s.g('people', 'people', '사람들')
    s.brk('in', 'postnominal-preposition', 'in people은 앞 명사 the best를 뒤에서 꾸미는 전치사구')
    s.hint('It is good [to know]', '[아는 것은] 좋다', span='It is good to know', label='가주어 It과 진주어 to부정사',
           links=[(['to'], ['는 것은'])], meaning='(어려운 시기가 … 끌어낼 수 있다는 것을) 아는 것은 좋다',
           explanation='It은 뒤의 to know that …을 대신하는 가주어. 진주어 to부정사의 목적어 that절은 표시에서 제외(다음 힌트).')
    s.hint('[that difficult times can bring out]', '[어려운 시기가 끌어낼 수 있다는 것]', span='that difficult times can bring out',
           label='명사절 접속사 that', links=[(['that'], ['가', '다는 것'])],
           meaning='어려운 시기가 (사람들 안의 가장 좋은 면을) 끌어낼 수 있다는 것',
           explanation='know의 목적어인 that 명사절. S′ difficult times, V′ can bring out까지 표시하고 목적어 the best in people은 제외.')
    s.review = ('가주어 It + 진주어 to know(It 뒤 to 앞에서 끊음) + know의 목적어 that 명사절(difficult times can bring out the best in people). '
                'the best를 in people이 꾸밈(in 앞에서 끊음). 힌트 2개(가주어–to 진주어, 명사절 that). 관계사·수동 없음.')
    out.append(s)

    # ---------------- s57 ----------------
    s = S('s57', T['s57'])
    s.ch('I decide', '나는 결심한다')
    s.ch('that one favor deserves another.', '하나의 호의는 또 다른 호의를 받을 만하다고.')
    s.natural('나는 호의에는 호의로 보답해야 한다고 마음먹는다.')
    s.cl('main', 'I', subj='I', verbs=['decide'])
    s.cl('subordinate', 'that', subj='one favor', verbs=['deserves'], marker='that')
    s.g('I', 'I', '나는', referent_ko='Alyssa')
    s.g('decide', 'decide', '결심하다, 마음먹다')
    s.g('that', 'that S′ V′', 'S′(이/가) V′라고 (접속사)')
    s.g('one', 'one', '하나의')
    s.g('favor', 'favor', '호의, 친절', star=W['favor'])
    s.g('deserves', 'deserve', '~을 받을 만하다', star=W['deserve'], verb_form=v3(s, 'deserves', 'deserve', 'one favor'))
    s.g('another', 'another', '또 다른 것 (또 하나의 호의)')
    s.hint('[that one favor deserves]', '[하나의 호의가 받을 만하다고]', span='that one favor deserves', label='명사절 접속사 that',
           links=[(['that'], ['가', '다고'])], meaning='하나의 호의가 (또 다른 호의를) 받을 만하다고',
           explanation='decide의 목적어인 that 명사절. S′ one favor, V′ deserves까지 표시하고 목적어 another(또 다른 호의)는 제외.')
    s.review = '주절 I decide + that 명사절(one favor deserves another: 호의에는 호의로 보답해야 한다). 힌트 1개. 관계사·수동 없음.'
    out.append(s)

    # ---------------- s58 ----------------
    s = S('s58', T['s58'])
    s.ch('“Why don’t you take a bag of ice', '“얼음 한 봉지를 가져가는 게 어때요')
    s.ch('for yourself,”', '당신 자신을 위해,”')
    s.ch('I suggest.', '나는 제안한다.')
    s.natural('“얼음 한 봉지 가져가세요.” 내가 제안한다.')
    s.cl_spans('main', s.at('Why')[0], subj=s.at('you'), verbs=[s.at('don’t'), s.at('take')])
    s.cl('main', 'I', subj='I', verbs=['suggest'])
    s.g('Why|don’t|you', 'Why don’t you V?', '~하는 게 어때요? (제안)')
    s.g('take', 'take', '가져가다')
    q = s.g('a bag of', 'a bag of', '한 봉지의')
    s.g('ice', 'ice', '얼음')
    s.g('for', 'for', '~을 위해')
    s.g('yourself', 'yourself', '당신 자신', referent_ko='정장 차림의 남자')
    s.g('I', 'I', '나는', referent_ko='Alyssa')
    s.g('suggest', 'suggest', '제안하다')
    s.prot('a bag of', 'quantity-kind-of', '수량 표현 a bag of가 뒤 명사 ice 앞에서 ‘한 봉지의’로 같은 어순 대응', gloss=q)
    s.review = ('인용된 제안 Why don’t you take a bag of ice for yourself(S: you, V: don’t take; 원문은 물음표 없이 콤마) + 전달절 I suggest. '
                '수량 표현 a bag of. 제안 고정 표현 Why don’t you V?는 그 자체 뜻을 익히는 표현이라 각주로 충분하고 u4-gp3에서 분석 → 힌트 없음(L-c Lc-17). 관계사·수동 없음.')
    out.append(s)

    # ---------------- s59 ----------------
    s = S('s59', T['s59'])
    s.ch('His smile does not fade.', '그의 미소는 사라지지 않는다.')
    s.natural('그의 미소는 사라지지 않는다.')
    s.cl('main', 'His', subj='His smile', verbs=['does', 'fade'])
    s.g('His', 'his', '그의', referent_ko='정장 차림의 남자')
    s.g('smile', 'smile', '미소')
    fn = s.g('does|not', 'does not V', '~하지 않는다', kind='function', combines_with=[])
    fa = s.g('fade', 'fade', '(점점) 사라지다, 희미해지다', star=W['fade'])
    link(fn, fa)
    s.review = '단일 주절(S: His smile, V: does fade — 부사 not은 V 칸에서 제외하고 각주 does not V로 부정 지원). 절 연결·수동 없음 → 힌트 없음.'
    out.append(s)

    # ---------------- s60 ----------------
    s = S('s60', T['s60'])
    s.ch('“I have a better idea,”', '“나에게 더 좋은 생각이 있어,”')
    s.ch('he says.', '그가 말한다.')
    s.natural('“더 좋은 생각이 있단다.” 그가 말한다.')
    s.cl('main', 'I', subj='I', verbs=['have'])
    s.cl('main', 'he', subj='he', verbs=['says'])
    s.g('I', 'I', '나는', referent_ko='정장 차림의 남자')
    s.g('have', 'have', '가지고 있다')
    s.g('better', 'better', '더 좋은 (good의 비교급)')
    s.g('idea', 'idea', '생각, 아이디어')
    s.g('he', 'he', '그가', referent_ko='정장 차림의 남자')
    s.g('says', 'say', '말하다', verb_form=v3(s, 'says', 'say', 'he'))
    s.review = '인용된 절 I have a better idea + 전달절 he says. 절 연결·관계사·수동 없음 → 힌트 없음.'
    out.append(s)

    # ---------------- s61 ----------------
    s = S('s61', T['s61'], key=True)
    s.ch('“Why don’t you take a bag of ice', '“너희가 얼음 한 봉지를 가져가는 게 어때')
    s.ch('for yourselves,', '너희 자신을 위해,')
    s.ch('and I’ll keep the rest.”', '그리고 내가 나머지를 가질게.”')
    s.natural('“너희가 얼음 한 봉지를 가져가는 게 어떠니, 나머지는 내가 가질게.”')
    s.cl_spans('main', s.at('Why')[0], subj=s.at('you'), verbs=[s.at('don’t'), s.at('take')])
    il = s.at('I’ll')
    s.cl_spans('main', s.at('and')[0], subj=[il[0], il[0] + 1], verbs=[[il[0] + 1, il[1]], s.at('keep')], marker='and')
    s.g('Why|don’t|you', 'Why don’t you V?', '~하는 게 어때? (제안)')
    s.g('take', 'take', '가져가다')
    q = s.g('a bag of', 'a bag of', '한 봉지의')
    s.g('ice', 'ice', '얼음')
    s.g('for', 'for', '~을 위해')
    s.g('yourselves', 'yourselves', '너희 자신', referent_ko='Alyssa와 Garrett')
    s.g('I’ll', 'I’ll', '나는 ~할 것이다 (= I will)', referent_ko='정장 차림의 남자')
    s.g('keep', 'keep', '가지다, 차지하다')
    s.g('the|rest', 'the rest', '나머지', star=W['rest'])
    s.prot('a bag of', 'quantity-kind-of', '수량 표현 a bag of가 뒤 명사 ice 앞에서 ‘한 봉지의’로 같은 어순 대응', gloss=q)
    s.review = ('인용된 두 절: 제안 Why don’t you take a bag of ice for yourselves(S: you, V: don’t take) + and I’ll keep the rest(’ll = will). '
                's58 Alyssa의 제안을 뒤집은 남자의 속셈. 제안 고정 표현은 각주로 충분하고 u4-gp3에서 분석 → 힌트 없음(L-c Lc-17). 관계사·수동 없음.')
    out.append(s)
    return out


UNIT = {
    'id': 'u4', 'source_id': 'src', 'paragraph_ids': ['p20', 'p21', 'p22', 'p23', 'p24', 'p25'],
    'sentence_ids': [f's{n:02d}' for n in range(47, 62)],
    'today_words': [
        {'id': W['ridiculously'], 'text': 'ridiculously', 'meaning_ko': '터무니없이, 어처구니없을 만큼'},
        {'id': W['impossible'], 'text': 'impossible', 'meaning_ko': '불가능한'},
        {'id': W['suit'], 'text': 'business suit', 'meaning_ko': '(사무용) 정장'},
        {'id': W['bring_out'], 'text': 'bring out', 'meaning_ko': '(좋은 점을) 끌어내다, 드러나게 하다'},
        {'id': W['favor'], 'text': 'favor', 'meaning_ko': '호의, 친절'},
        {'id': W['deserve'], 'text': 'deserve', 'meaning_ko': '~을 받을 만하다'},
        {'id': W['fade'], 'text': 'fade', 'meaning_ko': '(점점) 사라지다, 희미해지다'},
        {'id': W['rest'], 'text': 'the rest', 'meaning_ko': '나머지'},
    ],
}


def analysis(_):
    return {
        'heading_kind': '제목',
        'title_or_topic_en': 'Help with a Catch',
        'title_or_topic_ko': '속셈이 있는 도움',
        'intent_ko': '친절하게 도와주던 남자가 사실은 얼음을 차지하려는 속셈이었다는 반전을 통해, 어려운 시기의 호의가 늘 순수하지만은 않다는 것을 보여 준다.',
        'flow': [
            {'sentence_ids': ['s47', 's48', 's49', 's50', 's51'], 'label': '낯선 남자의 등장',
             'text_ko': '카트가 너무 무거워 밀기 어려울 때 정장 차림의 남자가 다가와 웃으며 도와주겠다고 한다. 그는 대답도 듣기 전에 카트 손잡이를 잡는다.'},
            {'sentence_ids': ['s52', 's53', 's54', 's55', 's56', 's57'], 'label': '감사와 믿음',
             'text_ko': 'Alyssa가 고맙다고 하자 남자는 서로 도와야 한다고 말한다. Alyssa는 어려운 시기가 사람들의 좋은 면을 끌어낼 수 있다고 느끼며 호의에 보답하기로 한다.'},
            {'sentence_ids': ['s58', 's59', 's60', 's61'], 'label': '반전',
             'text_ko': 'Alyssa가 얼음 한 봉지를 가져가라고 권하자, 남자는 여전히 웃으며 오히려 아이들이 한 봉지만 가져가고 나머지는 자기가 갖겠다고 한다.'},
        ],
        'easy_explanations': [
            {'sentence_id': 's50', 'explanatory_sentences': [
                '50번 문장은 49번에서 미소 지은 남자가 처음 건네는 말이다.',
                '남자는 아이들이 무거운 카트 때문에 힘들어 보인다고 말한다.',
                '겉으로는 친절하게 도움을 제안하는 말이다.',
                '하지만 뒤에서 이 도움에 다른 속셈이 있었다는 것이 드러난다.']},
            {'sentence_id': 's56', 'explanatory_sentences': [
                '56번 문장은 남자의 말을 들은 Alyssa의 생각이다.',
                '힘든 일이 생기면 사람들이 서로 돕는 좋은 모습을 보일 수 있다는 뜻이다.',
                '앞 장면에서 Alyssa는 한 여자에게 생수를 빼앗겼다.',
                'Hali도 물을 나눠 달라는 부탁을 거절했다.',
                '그런 Alyssa에게 이 남자의 친절은 다시 사람을 믿게 해 준다.',
                '그래서 뒤에 나올 남자의 속셈이 더 큰 반전이 된다.']},
            {'sentence_id': 's61', 'explanatory_sentences': [
                '61번 문장은 이 장면의 반전이다.',
                '58번에서 Alyssa는 남자에게 얼음 한 봉지를 가져가라고 했다.',
                '남자는 그 말을 뒤집어 아이들이 한 봉지만 가져가라고 한다.',
                '그리고 카트에 가득한 나머지 얼음은 자기가 갖겠다고 한다.',
                '남자가 카트를 잡아 준 것은 친절이 아니라 얼음을 차지하려는 속셈이었다.']},
        ],
        'grammar_points': [
            {'id': 'u4-gp1', 'sentence_id': 's47', 'span': 'almost impossible to push',
             'title': '형용사 + to V: ~하기에 (형용사)한', 'formula_key': '형용사 + to V',
             'explanation': '공식: 형용사 + to V — V하기에 (형용사)한. 형용사 = impossible(불가능한), 앞의 almost = 거의, to V = to push(밀기에; push = 밀다). '
                            '→ 밀기에 거의 불가능한. 앞의 The cart is(카트는 ~이다)와 합치면 ‘카트는 밀기가 거의 불가능하다’.',
             'practice': {'span': 'almost impossible to push',
                          'formula_support': {'en': '형용사 + to V', 'ko': 'V하기에 (형용사)한'},
                          'support': [('s47', 'almost'), ('s47', 'impossible'), ('s47', 'push')],
                          'answer_ko': '밀기에 거의 불가능한'}},
            {'id': 'u4-gp2', 'sentence_id': 's56', 'span': 'It is good to know that difficult times can bring out the best in people',
             'title': 'It is 형용사 to V: V하는 것은 (형용사)하다', 'formula_key': 'It is 형용사 to V',
             'explanation': '공식: It is 형용사 to V — V하는 것은 (형용사)하다. It = 가주어(뒤의 to know …를 대신함), 형용사 = good(좋은), '
                            'to V = to know(아는 것), 아는 내용 = that difficult times can bring out the best in people(어려운 시기가 사람들 안의 가장 좋은 면을 끌어낼 수 있다는 것). '
                            '→ 어려운 시기가 사람들의 가장 좋은 면을 끌어낼 수 있다는 것을 아는 것은 좋다.',
             'practice': {'span': 'It is good to know',
                          'formula_support': {'en': 'It is 형용사 to V', 'ko': 'V하는 것은 (형용사)하다'},
                          'support': [('s56', 'good'), ('s56', 'know')],
                          'answer_ko': '아는 것은 좋다'}},
            {'id': 'u4-gp3', 'sentence_id': 's61', 'span': 'Why don’t you take a bag of ice for yourselves',
             'title': 'Why don’t you V?: ~하는 게 어때?', 'formula_key': 'Why don’t you V?',
             'explanation': '공식: Why don’t you V? — (너희가) V하는 게 어때?(제안). V = take(가져가다), a bag of ice = 얼음 한 봉지, for yourselves = 너희 자신을 위해. '
                            '→ 너희가 너희 자신을 위해 얼음 한 봉지를 가져가는 게 어때? 이유를 묻는 ‘왜 ~하지 않니?’가 아니라 권하는 말이다.',
             'practice': {'span': 'Why don’t you take a bag of ice for yourselves',
                          'formula_support': {'en': 'Why don’t you V?', 'ko': '~하는 게 어때?'},
                          'support': [('s61', 'take'), ('s61', 'a bag of'), ('s61', 'ice'), ('s61', 'for'), ('s61', 'yourselves')],
                          'answer_ko': '너희가 너희 자신을 위해 얼음 한 봉지를 가져가는 게 어때'}},
        ],
        'formula_routes': [],
        'relations': [
            {'head': {'id': 'u4-r1h', 'text': 'heavy', 'meaning_ko': '무거운'},
             'synonym': {'id': 'u4-r1s', 'text': 'weighty', 'meaning_ko': '무거운, 묵직한'},
             'antonym': {'id': 'u4-r1a', 'text': 'light', 'meaning_ko': '가벼운'}},
            {'head': {'id': 'u4-r2h', 'text': 'difficult', 'meaning_ko': '어려운, 힘든'},
             'synonym': {'id': 'u4-r2s', 'text': 'hard', 'meaning_ko': '어려운, 힘든'},
             'antonym': {'id': 'u4-r2a', 'text': 'easy', 'meaning_ko': '쉬운, 편한'}},
            {'head': {'id': 'u4-r3h', 'text': 'best', 'meaning_ko': '가장 좋은 것'},
             'synonym': {'id': 'u4-r3s', 'text': 'finest', 'meaning_ko': '가장 훌륭한 것'},
             'antonym': {'id': 'u4-r3a', 'text': 'worst', 'meaning_ko': '가장 나쁜 것'}},
        ],
    }


def workbook():
    return {
        'relation_order': ['u4-r3s', 'u4-r1a', 'u4-r2h', 'u4-r3a', 'u4-r1s', 'u4-r2a', 'u4-r3h', 'u4-r1h', 'u4-r2s'],
        'key_sentence_ids': ['s56', 's61'],
        'question_id': 'Q04',
        'syntax_point_ids': ['u4-gp1', 'u4-gp2', 'u4-gp3'],
    }
