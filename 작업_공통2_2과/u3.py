"""공통 단위 3: s37~s46 (p16~p19) — 얼음도 물이다: 얼음 봉지를 카트에 쌓는 장면.

사용자 결정(2026-09-28 “5단위, 작품 소개 합침”): 무소제목 소설 본문을 장면 기준으로 묶은 셋째 단위.
"""
from author import S, link

W = {'frozen': 'u3-w1', 'case': 'u3-w2', 'packed': 'u3-w3', 'remind': 'u3-w4',
     'pile': 'u3-w5', 'one_after': 'u3-w6', 'notice': 'u3-w7', 'empty': 'u3-w8'}


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

    # ---------------- s37 ----------------
    s = S('s37', T['s37'])
    s.ch('I look for Garrett,', '나는 Garrett을 찾는다,')
    s.ch('whom I find', '그리고 그를 나는 발견한다')
    s.ch('in the frozen aisle.', '냉동식품 통로에서.')
    s.natural('나는 Garrett을 찾다가 냉동식품 통로에서 그를 발견한다.')
    s.cl('main', 'I', subj='I', verbs=['look'])
    s.cl('subordinate', 'whom', subj='I', verbs=['find'], marker='whom')
    s.g('I', 'I', '나는', referent_ko='Alyssa')
    s.g('look|for', 'look for', '~을 찾다')
    rel = s.g('whom', 'whom S′ V′', '그리고 그를 S′(이/가) V′하다 (관계대명사)')
    s.g('I', 'I', '내가', referent_ko='Alyssa', at=s.text.index('I find'))
    s.g('find', 'find', '발견하다')
    s.g('in', 'in', '~에서')
    s.g('frozen', 'frozen', '냉동식품(의)', verb_form=pp('past-participle', s, 'frozen', 'freeze'))
    s.g('aisle', 'aisle', '통로')
    s.hint('Garrett, [whom I find]', 'Garrett, [그리고 그를 내[Alyssa]가 발견한다]', span='Garrett, whom I find',
           label='계속적 관계대명사 whom', links=[(['whom'], ['그리고 그를', '가'])], refs=[('I', '내', '[Alyssa]')],
           meaning='Garrett, 그리고 그를(Garrett을) 내가 발견한다',
           explanation='콤마 뒤 목적격 관계대명사 whom이 선행사 Garrett을 받아 ‘그리고 그를’로 이어 준다(find의 목적어). S′ I, V′ find까지 표시하고 in the frozen aisle은 제외.')
    s.relative_ids = [rel['id']]
    s.review = ('주절 I look for Garrett + 콤마 뒤 계속적 목적격 관계대명사 whom절(I find in the frozen aisle). Garrett은 s11에서 제공한 고유명사 반복. '
                'frozen은 명사 앞 독립 p.p.로 the frozen aisle에서는 ‘냉동식품(의)’ 뜻이라 오늘의 낱말 frozen(냉동된, 얼린)과 뜻이 달라 ★ 없음(★는 s39 frozen vegetables, L-c Lc-01). 필수 관계사 힌트 1개. 수동 없음.')
    out.append(s)

    # ---------------- s38 ----------------
    s = S('s38', T['s38'])
    s.ch('Then I see something.', '그때 나는 무언가를 본다.')
    s.natural('그때 무언가가 눈에 들어온다.')
    s.cl('main', 'I', subj='I', verbs=['see'])
    s.g('Then', 'then', '그때, 그러고 나서')
    s.g('I', 'I', '나는', referent_ko='Alyssa')
    s.g('see', 'see', '보다')
    s.g('something', 'something', '무언가')
    s.review = '단일 주절(S: I, V: see). 절 연결·관계사·수동 없음 → 힌트 없음.'
    out.append(s)

    # ---------------- s39 ----------------
    s = S('s39', T['s39'], key=True)
    s.ch('Just past the frozen vegetables and ice cream,', '냉동 채소와 아이스크림을 바로 지나서,')
    s.ch('there is a case', '진열장이 있다')
    s.ch('packed with ice.', '얼음으로 가득 찬.')
    s.natural('냉동 채소와 아이스크림 코너를 바로 지나면 얼음이 가득 든 진열장이 있다.')
    s.cl('main', 'there', subj='a case packed with ice', verbs=[], vfirst=['is'], disp='a case',
         disp_review='중심명사 case까지 표시하고 뒤에서 꾸미는 과거분사구 packed with ice는 제외(유도부사 there는 주어 아님)')
    s.g('Just', 'just', '바로')
    s.g('past', 'past', '~을 지나서')
    s.g('frozen', 'frozen', '냉동된, 얼린', star=W['frozen'], verb_form=pp('past-participle', s, 'frozen', 'freeze'))
    s.g('vegetables', 'vegetables', '채소들')
    s.g('ice|cream', 'ice cream', '아이스크림')
    s.g('is', 'is', '있다')
    s.g('case', 'case', '(냉동) 진열장 (흔한 뜻: 경우)', star=W['case'])
    pk = s.g('packed', 'packed', '가득 찬, 꽉 채워진', star=W['packed'], verb_form=pp('past-participle', s, 'packed', 'pack'))
    s.g('with', 'with', '~으로')
    s.g('ice', 'ice', '얼음', at=s.text.index('ice.'))
    s.extra_cov[tuple(s.span_of('there'))] = {
        'exemption': 'below-middle1-unneeded', 'level': 'below-middle1',
        'reason': '유도부사 there(초등 기초어)는 따로 해석하지 않으며 뒤 is 각주의 ‘있다’로 뜻을 지원'}
    s.hint('a case [packed with ice]', '[얼음으로 가득 찬] 진열장', span='a case packed with ice', label='과거분사 후치수식',
           links=[(['packed'], ['가득 찬'])], participle_focus_gloss_id=pk['id'],
           meaning='얼음으로 가득 찬 진열장',
           explanation='과거분사구 packed with ice가 앞 명사 a case를 뒤에서 꾸민다. 진열장이 얼음으로 ‘채워진’ 쪽이라 과거분사. 독립 p.p. packed ↔ 가득 찬 전체 대응.')
    s.review = ('문두 장소 부사구 Just past the frozen vegetables and ice cream + 유도부사 there + is + 주어 a case packed with ice(과거분사 후치수식). '
                'case는 문이 달린 냉동 진열장(s40 I open the door). 힌트 1개(과거분사 후치수식). 관계사·유한 수동 없음.')
    out.append(s)

    # ---------------- s40 ----------------
    s = S('s40', T['s40'])
    s.ch('I open the door', '나는 문을 연다')
    s.ch('and reach for a bag.', '그리고 한 봉지를 향해 손을 뻗는다.')
    s.natural('나는 진열장 문을 열고 얼음 한 봉지를 향해 손을 뻗는다.')
    s.cl('main', 'I', subj='I', verbs=['open', 'and', 'reach'])
    s.g('I', 'I', '나는', referent_ko='Alyssa')
    s.g('open', 'open', '열다')
    s.g('door', 'door', '문')
    s.g('reach|for', 'reach for', '~을 향해 손을 뻗다')
    s.g('bag', 'bag', '(얼음) 봉지')
    s.review = '한 주어 I의 병렬 동사 open과 reach(and로 연결). 절 연결·관계사·수동 없음 → 힌트 없음.'
    out.append(s)

    # ---------------- s41 ----------------
    s = S('s41', T['s41'])
    s.ch('“What are you doing?', '“너는 무엇을 하고 있니?')
    s.natural('“뭐 하는 거야?')
    s.cl('main', 'What', subj='you', verbs=['doing'], vfirst=['are'])
    s.g('What', 'what', '무엇을')
    f = s.g('are', 'be V-ing', '~하고 있다', kind='function', combines_with=[])
    d = s.g('doing', 'do', '하다', verb_form=pp('ing', s, 'doing', 'do'))
    link(f, d)
    s.review = ('인용 속 의문사 의문문(S: you, V: are doing; 의문사 What은 doing의 목적어). 인용문 안의 물음표에서 문장을 나눔(s42로 인용 계속). '
                '단독 you 각주 제외. 절 연결·수동 없음 → 힌트 없음.')
    out.append(s)

    # ---------------- s42 ----------------
    s = S('s42', T['s42'])
    s.ch('We need water, not ice,”', '우리는 물이 필요해, 얼음이 아니라,”')
    s.ch('he reminds me.', '그가 나에게 일깨운다.')
    s.natural('우리한테 필요한 건 얼음이 아니라 물이야.” Garrett이 나에게 일깨워 준다.')
    s.cl('main', 'We', subj='We', verbs=['need'])
    s.cl('main', 'he', subj='he', verbs=['reminds'])
    s.g('We', 'we', '우리는', referent_ko='Alyssa와 Garrett')
    s.g('need', 'need', '필요하다')
    s.g('water', 'water', '물')
    s.g('not', 'not', '~이 아니라')
    s.g('ice', 'ice', '얼음')
    s.g('he', 'he', '그가', referent_ko='Garrett')
    s.g('reminds', 'remind', '(잊지 않도록) 일깨우다, 상기시키다', star=W['remind'], verb_form=v3(s, 'reminds', 'remind', 'he'))
    s.g('me', 'me', '나에게', referent_ko='Alyssa')
    s.hint('water, [not ice]', '[얼음이 아니라] 물', span='water, not ice', label='A, not B 구조',
           links=[(['not'], ['이 아니라'])], meaning='얼음이 아니라 물',
           explanation='A, not B: B가 아니라 A. A = water, B = ice. 한국어에서는 not ice를 앞으로 옮겨 ‘얼음이 아니라 물’로 읽는다.')
    s.review = ('앞 s41에서 이어지는 인용의 마지막 조각 We need water, not ice(A, not B) + 전달절 he reminds me(he = Garrett). '
                '힌트 1개(A, not B). 관계사·수동 없음.')
    out.append(s)

    # ---------------- s43 ----------------
    s = S('s43', T['s43'])
    s.ch('“Ice is water.', '“얼음은 물이야.')
    s.natural('“얼음도 물이잖아.')
    s.cl('main', 'Ice', subj='Ice', verbs=['is'])
    s.g('Ice', 'ice', '얼음')
    s.g('is', 'is', '~이다')
    s.g('water', 'water', '물')
    s.review = '인용 속 단일 절(S: Ice, V: is). 인용문 안의 마침표에서 문장을 나눔(s44로 인용 계속). 절 연결·수동 없음 → 힌트 없음.'
    out.append(s)

    # ---------------- s44 ----------------
    s = S('s44', T['s44'])
    s.ch('Just help me,”', '그냥 나를 도와줘,”')
    s.ch('I tell him.', '나는 그에게 말한다.')
    s.natural('그냥 좀 도와줘.” 내가 동생에게 말한다.')
    s.cl('imperative', 'Just', verbs=['help'])
    s.cl('main', 'I', subj='I', verbs=['tell'])
    s.g('Just', 'just', '그냥, 좀')
    s.g('help', 'help', '돕다')
    s.g('me', 'me', '나를', referent_ko='Alyssa')
    s.g('I', 'I', '나는', referent_ko='Alyssa')
    s.g('tell', 'tell', '말하다')
    s.g('him', 'him', '그에게', referent_ko='Garrett')
    s.review = '앞 s43에서 이어지는 인용: 명령문 Just help me(V: help, 생략된 you는 보충하지 않음) + 전달절 I tell him. 절 연결·수동 없음 → 힌트 없음.'
    out.append(s)

    # ---------------- s45 ----------------
    s = S('s45', T['s45'], key=True)
    s.ch('Garrett and I put one bag of ice after another', 'Garrett과 나는 얼음 봉지를 하나씩 차례로 넣는다')
    s.ch('into our cart,', '우리의 카트 안으로,')
    s.ch('until it is piled', '그것이 가득 쌓일 때까지')
    s.ch('as high as it can get.', '그것이 될 수 있는 만큼 높이.')
    s.natural('Garrett과 나는 카트가 더는 쌓을 수 없을 만큼 높이 가득 찰 때까지 얼음 봉지를 하나씩 카트에 담는다.')
    s.cl('main', 'Garrett', subj='Garrett and I', verbs=['put'])
    s.cl('subordinate', 'until', subj='it', verbs=['is', 'piled'], marker='until')
    a2 = s.at('as it can get')
    s.cl_spans('subordinate', a2[0], subj=s.at('it', after=a2[0]), verbs=[s.at('can', after=a2[0]), s.at('get', after=a2[0])],
               marker='as')
    s.g('I', 'I', '나는', referent_ko='Alyssa')
    s.g('put', 'put', '넣다, 놓다')
    s.g('one|after|another', 'one A after another', 'A를 하나씩 차례로', star=W['one_after'])
    q = s.g('bag of', 'bag of', '봉지의', at=s.text.index('bag of'))
    s.g('ice', 'ice', '얼음')
    s.g('into', 'into', '~ 안으로')
    s.g('our', 'our', '우리의', referent_ko='Alyssa와 Garrett')
    s.g('cart', 'cart', '카트')
    s.g('until', 'until S′ V′', 'S′(이/가) V′할 때까지')
    s.g('it', 'it', '그것이', referent_ko='카트')
    f = s.g('is', 'be p.p.', '~되다', kind='function', combines_with=[])
    pl = s.g('piled', 'piled', '(짐이) 가득 쌓인', star=W['pile'], verb_form=pp('passive-participle', s, 'piled', 'pile', f['id']))
    link(f, pl)
    s.g('as|high|as', 'as high as S′ V′', 'S′(이/가) V′하는 만큼 높이')
    s.g('it', 'it', '그것이', referent_ko='카트', at=a2[0] + 3)
    fc = s.g('can', 'can V', '~할 수 있다', kind='function', combines_with=[])
    gt = s.g('get', 'get', '(어떤 상태가) 되다')
    link(fc, gt)
    s.prot('bag of', 'quantity-kind-of', '수량 표현 bag of가 뒤 명사 ice 앞에서 ‘봉지의’로 같은 어순 대응(one … after another 안의 A)', gloss=q)
    s.hint('[until it is piled]', '[그것[카트]이 가득 쌓일 때까지]', span='until it is piled', label='시간 접속사 until',
           links=[(['until'], ['이', '때까지'])], refs=[('it', '그것', '[카트]')],
           meaning='그것(카트)이 (얼음으로) 가득 쌓일 때까지',
           explanation='until S′ V′: S′가 V′할 때까지. S′ it(카트), V′ is piled(가득 쌓이다, 수동)까지 표시하고 as high as 이하는 제외. 수동 is piled는 이 힌트가 있어 분석 보충 u3-gp4로 연결.')
    s.hint('[as high as it can get]', '[그것[카트]이 될 수 있는 만큼 높이]', span='as high as it can get', label='as ~ as 비교 구문',
           links=[(['as', ('as', 1)], ['이', '만큼'])], refs=[('it', '그것', '[카트]')],
           meaning='그것(카트)이 될 수 있는 만큼 높이(최대한 높이)',
           explanation='as + 부사 + as S′ V′: S′가 V′하는 만큼 ~하게. 뒤 as절의 S′ it, V′ can get(될 수 있다). 카트에 더 쌓을 수 없을 만큼 최대한 높이.')
    s.review = ('주절 Garrett and I put one bag of ice after another into our cart(one A after another, A = bag of ice) + until절(it is piled, 수동) '
                '+ 비교 as high as it can get(뒤 as절 S′ it, V′ can get). Garrett은 고유명사 반복. 힌트 2개(until절, as ~ as 비교). '
                'is piled(be p.p.)는 이 문장에 결합 힌트를 두지 않아 분석 보충 u3-gp4로 연결. 관계사 없음.')
    out.append(s)

    # ---------------- s46 ----------------
    s = S('s46', T['s46'])
    s.ch('By now', '이제쯤은')
    s.ch('other people have taken notice', '다른 사람들이 알아챘다')
    s.ch('and begin to empty the ice case.', '그리고 얼음 진열장을 비우기 시작한다.')
    s.natural('이쯤 되자 다른 사람들도 눈치를 채고 얼음 진열장을 비우기 시작한다.')
    s.cl('main', 'other', subj='other people', verbs=['have', 'taken', 'and', 'begin'])
    s.g('By|now', 'by now', '이제쯤은, 이쯤 되자')
    s.g('other', 'other', '다른')
    s.g('people', 'people', '사람들')
    f = s.g('have', 'have p.p.', '~했다', kind='function', combines_with=[])
    tk = s.g('taken', 'take', '하다 (taken은 take의 p.p.형)',
             verb_form=pp('perfect-participle', s, 'taken', 'take', f['id']))
    link(f, tk)
    s.g('notice', 'notice', '주목, 알아챔', star=W['notice'])
    s.g('begin|to', 'begin to V', '~하기 시작하다',
        verb_construction={'kind': 'to-complement', 'verb_span': s.span_of('begin'), 'lemma': 'begin',
                           'link_spans': [s.span_of('to')], 'review_record': 'begin to empty: begin의 목적어 to V.'})
    s.g('empty', 'empty', '비우다', star=W['empty'])
    s.g('ice|case', 'ice case', '얼음 진열장', star=W['case'])
    s.review = ('단일 주절: 주어 other people의 병렬 동사 have taken(현재완료) and begin(begin to V). take notice는 능동 완료 원형 각주 구조상 take(하다)·notice(주목) 두 각주로 두고 ‘주목을 했다 → 알아챘다’로 대입되게 함(L-c Lc-06 B안). ice case의 case는 오늘의 낱말 case와 같은 뜻이라 ★. '
                '상위 문법 연결·수동 없음. 능동 완료 have taken은 take notice 숙어 속이라 결합 힌트(take → have taken)가 오히려 뜻을 흐려 힌트로 선정하지 않고 분석 보충 u3-gp5로 연결. begin to V는 각주로 충분 → 힌트 없음.')
    out.append(s)
    return out


UNIT = {
    'id': 'u3', 'source_id': 'src', 'paragraph_ids': ['p16', 'p17', 'p18', 'p19'],
    'sentence_ids': [f's{n:02d}' for n in range(37, 47)],
    'today_words': [
        {'id': W['frozen'], 'text': 'frozen', 'meaning_ko': '냉동된, 얼린'},
        {'id': W['case'], 'text': 'case', 'meaning_ko': '(냉동) 진열장'},
        {'id': W['packed'], 'text': 'packed', 'meaning_ko': '가득 찬, 꽉 채워진'},
        {'id': W['remind'], 'text': 'remind', 'meaning_ko': '(잊지 않도록) 일깨우다, 상기시키다'},
        {'id': W['pile'], 'text': 'piled', 'meaning_ko': '(짐이) 가득 쌓인'},
        {'id': W['one_after'], 'text': 'one after another', 'meaning_ko': '하나씩 차례로'},
        {'id': W['notice'], 'text': 'notice', 'meaning_ko': '주목, 알아챔'},
        {'id': W['empty'], 'text': 'empty', 'meaning_ko': '비우다'},
    ],
}


def analysis(_):
    return {
        'heading_kind': '제목',
        'title_or_topic_en': 'Ice Is Water, Too',
        'title_or_topic_ko': '얼음도 물이다',
        'intent_ko': '생수를 구하지 못한 Alyssa가 얼음도 결국 물이라는 점을 떠올려 얼음을 모으는 장면이다. 위기 속에서 재치 있게 해결책을 찾는 모습과, 그것을 보고 곧바로 따라 하는 사람들을 보여 준다.',
        'flow': [
            {'sentence_ids': ['s37', 's38', 's39', 's40'], 'label': '발견',
             'text_ko': 'Alyssa는 냉동식품 통로에서 Garrett을 찾고, 그 옆에 얼음이 가득 든 진열장을 발견한다. 문을 열고 얼음 봉지를 집으려 한다.'},
            {'sentence_ids': ['s41', 's42', 's43', 's44'], 'label': '대화',
             'text_ko': 'Garrett은 필요한 것은 얼음이 아니라 물이라고 말한다. Alyssa는 얼음도 물이라며 도와 달라고 한다.'},
            {'sentence_ids': ['s45', 's46'], 'label': '행동과 반응',
             'text_ko': '두 사람은 카트가 더는 쌓을 수 없을 만큼 가득 찰 때까지 얼음 봉지를 담는다. 이를 본 다른 사람들도 얼음 진열장을 비우기 시작한다.'},
        ],
        'easy_explanations': [
            {'sentence_id': 's43', 'explanatory_sentences': [
                '43번 문장은 42번에서 물이 필요하다는 Garrett의 말에 대한 Alyssa의 대답이다.',
                '얼음은 물이 얼어서 굳은 것이다.',
                '녹이면 다시 마실 수 있는 물이 된다.',
                'Alyssa는 생수가 없으면 얼음을 대신 가져가면 된다는 것을 떠올렸다.']},
            {'sentence_id': 's45', 'explanatory_sentences': [
                '45번 문장은 Alyssa의 생각을 곧바로 행동으로 옮기는 장면이다.',
                '두 사람은 카트에 더 쌓을 자리가 없을 때까지 얼음 봉지를 담는다.',
                '얼음을 많이 모을수록 나중에 쓸 물도 많아진다.',
                '물을 조금이라도 더 확보하려는 두 사람의 절박함이 드러난다.']},
            {'sentence_id': 's46', 'explanatory_sentences': [
                '46번 문장은 두 사람의 행동을 본 다른 사람들의 반응이다.',
                '다른 사람들도 얼음이 물을 대신할 수 있다는 것을 눈치챈다.',
                '그래서 그들도 얼음 진열장을 비우기 시작한다.',
                '물이 부족하자 사람들이 얼음까지 서둘러 차지하려 한다는 것을 보여 준다.']},
        ],
        'grammar_points': [
            {'id': 'u3-gp1', 'sentence_id': 's37', 'span': 'I look for Garrett, whom I find in the frozen aisle',
             'title': '콤마 + whom S′ V′: 그리고 그를 S′가 V′하다', 'formula_key': ', whom S′ V′',
             'explanation': '공식: 명사, whom S′ V′ — 명사, 그리고 그를 S′(이/가) V′하다. 앞 명사 = Garrett, whom = 그리고 그를(Garrett을), '
                            'S′ = I(내가), V′ = find(발견하다), in the frozen aisle = 냉동식품 통로에서. '
                            '→ Garrett, 그리고 그를 나는 냉동식품 통로에서 발견한다. whom은 find의 목적어 자리를 대신하며, 콤마 뒤라 앞 명사에 설명을 이어 준다.',
             'practice': {'span': 'Garrett, whom I find in the frozen aisle',
                          'formula_support': {'en': ', whom S′ V′', 'ko': '그리고 그를 S′(이/가) V′하다'},
                          'support': [('s37', 'I', 1), ('s37', 'find'), ('s37', 'in'), ('s37', 'frozen'), ('s37', 'aisle')],
                          'answer_ko': 'Garrett, 그리고 그를 나는 냉동식품 통로에서 발견한다'}},
            {'id': 'u3-gp2', 'sentence_id': 's39', 'span': 'there is a case packed with ice',
             'title': '명사 + p.p.: ~된(한) 명사', 'formula_key': 'N + p.p.',
             'explanation': '공식: 명사(N) + p.p. — p.p.된(한) N. N = a case(진열장), p.p. = packed(가득 찬, 채워진), with ice = 얼음으로. '
                            '→ 얼음으로 가득 찬 진열장. 진열장이 얼음을 채우는 것이 아니라 얼음으로 ‘채워진’ 쪽이라 과거분사 packed가 뒤에서 꾸민다. there is와 합치면 ‘얼음으로 가득 찬 진열장이 있다’.',
             'practice': {'span': 'a case packed with ice',
                          'formula_support': {'en': 'N + p.p.', 'ko': 'p.p.된(한) N'},
                          'support': [('s39', 'case'), ('s39', 'packed'), ('s39', 'with'), ('s39', 'ice')],
                          'answer_ko': '얼음으로 가득 찬 진열장'}},
            {'id': 'u3-gp3', 'sentence_id': 's45', 'span': 'as high as it can get',
             'title': 'as + 부사 + as S′ V′: S′가 V′하는 만큼 ~하게', 'formula_key': 'as high as S′ V′',
             'explanation': '공식: as + 부사 + as S′ V′ — S′(이/가) V′하는 만큼 ~하게. 부사 = high(높이), S′ = it(카트), V′ = can get(될 수 있다; can = ~할 수 있다, get = 되다). '
                            '→ 카트가 될 수 있는 만큼 높이, 곧 더는 쌓을 수 없을 만큼 최대한 높이.',
             'practice': {'span': 'as high as it can get',
                          'formula_support': {'en': 'as high as S′ V′', 'ko': 'S′(이/가) V′하는 만큼 높이'},
                          'support': [('s45', 'it', 1), ('s45', 'can V'), ('s45', 'get')],
                          'answer_ko': '그것(카트)이 될 수 있는 만큼 높이'}},
            {'id': 'u3-gp4', 'sentence_id': 's45', 'span': 'until it is piled',
             'title': 'be p.p.: ~되다 (is piled: 가득 쌓이다)', 'formula_key': 'be p.p.',
             'explanation': '공식: be p.p. — ~되다. be = is(현재), p.p. = piled((짐이) 가득 쌓인, pile의 p.p.형). → is piled = 가득 쌓이다. '
                            '카트(it)가 무언가를 쌓는 것이 아니라, 두 사람이 얼음을 쌓아서 카트가 (얼음으로) 가득 쌓이는 쪽이라 수동 is piled를 쓴다. 앞의 until it과 이으면 ‘그것(카트)이 가득 쌓일 때까지’.',
             'supplemental': {'function': ('s45', 'be p.p.', 0),
                              'reason': 's45의 수동 is piled는 until절·as ~ as 힌트가 이미 있어 결합 힌트로 선정하지 않았고, 기본 분석 3개에 be p.p. 설명이 없어 이 단위 대표 사례로 1회 보충'},
             'practice': {'span': 'it is piled',
                          'formula_support': {'en': 'be p.p.', 'ko': '~되다'},
                          'support': [('s45', 'it', 0), ('s45', 'piled')],
                          'answer_ko': '그것(카트)이 가득 쌓인다'}},
            {'id': 'u3-gp5', 'sentence_id': 's46', 'span': 'other people have taken notice',
             'title': 'have p.p.: ~했다 (have taken notice: 알아챘다)', 'formula_key': 'have p.p.',
             'explanation': '공식: have p.p. — ~했다. have = 현재완료의 조동사, p.p. = taken(take의 p.p.형; take notice = 알아차리다). '
                            '→ have taken notice = 알아챘다(이미 알아차린 상태). 주어 other people(다른 사람들)과 합치면 ‘다른 사람들이 알아챘다’.',
             'supplemental': {'function': ('s46', 'have p.p.', 0),
                              'reason': 's46의 능동 완료 have taken은 take notice 숙어 속이라 결합 힌트로 선정하지 않았고, 기본 분석 3개에 have p.p. 설명이 없어 이 단위 대표 사례로 1회 보충'},
             'practice': {'span': 'other people have taken notice',
                          'formula_support': {'en': 'have p.p.', 'ko': '~했다'},
                          'support': [('s46', 'other'), ('s46', 'people'), ('s46', 'take'), ('s46', 'notice')],
                          'answer_ko': '다른 사람들이 알아챘다'}},
        ],
        'formula_routes': [
            {'function': ('s45', 'be p.p.', 0), 'route': 'analysis', 'grammar_point_id': 'u3-gp4',
             'review_record': 'is piled: until절·as ~ as 힌트가 있어 분석 보충 u3-gp4로 연결'},
            {'function': ('s46', 'have p.p.', 0), 'route': 'analysis', 'grammar_point_id': 'u3-gp5',
             'review_record': 'have taken (notice): 숙어 속 완료라 결합 힌트 대신 분석 보충 u3-gp5로 연결'},
        ],
        'relations': [
            {'head': {'id': 'u3-r1h', 'text': 'packed', 'meaning_ko': '가득 찬'},
             'synonym': {'id': 'u3-r1s', 'text': 'filled', 'meaning_ko': '가득 찬, 채워진'},
             'antonym': {'id': 'u3-r1a', 'text': 'empty', 'meaning_ko': '비어 있는'}},
            {'head': {'id': 'u3-r2h', 'text': 'find', 'meaning_ko': '발견하다, 찾아내다'},
             'synonym': {'id': 'u3-r2s', 'text': 'discover', 'meaning_ko': '발견하다'},
             'antonym': {'id': 'u3-r2a', 'text': 'lose', 'meaning_ko': '잃어버리다'}},
            {'head': {'id': 'u3-r3h', 'text': 'notice', 'meaning_ko': '주목, 알아챔'},
             'synonym': {'id': 'u3-r3s', 'text': 'note', 'meaning_ko': '주목, 주의'},
             'antonym': {'id': 'u3-r3a', 'text': 'disregard', 'meaning_ko': '무시, 묵살'}},
        ],
    }


def workbook():
    return {
        'relation_order': ['u3-r2s', 'u3-r3a', 'u3-r1h', 'u3-r2a', 'u3-r3s', 'u3-r1s', 'u3-r2h', 'u3-r1a', 'u3-r3h'],
        'key_sentence_ids': ['s39', 's45'],
        'question_id': 'Q03',
        'syntax_point_ids': ['u3-gp1', 'u3-gp2', 'u3-gp3', 'u3-gp4', 'u3-gp5'],
    }
