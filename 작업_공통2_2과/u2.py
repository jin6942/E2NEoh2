"""공통 단위 2: s18~s36 (p09~p15) — 텅 빈 진열대, 빼앗긴 생수 한 상자, 호의를 갚지 않는 Hali.

사용자 결정(2026-09-28 “5단위, 작품 소개 합침”): 무소제목 소설 본문을 장면 기준으로 묶은 둘째 단위.
"""
from author import S, link, verbless

W = {'impatience': 'u2-w1', 'hostility': 'u2-w2', 'politeness': 'u2-w3', 'aisle': 'u2-w4',
     'precious': 'u2-w5', 'commodity': 'u2-w6', 'favor': 'u2-w7', 'flush': 'u2-w8'}


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


def there_cov(s, piece='There'):
    s.extra_cov[tuple(s.span_of(piece))] = {
        'exemption': 'below-middle1-unneeded', 'level': 'below-middle1',
        'reason': '유도부사 There(초등 기초어)는 따로 해석하지 않으며 뒤 is 각주의 ‘있다’로 뜻을 지원'}


def sentences(T):
    out = []

    # ---------------- s18 ----------------
    s = S('s18', T['s18'])
    s.ch('There is a look', '표정이 있다')
    s.ch('of impatience', '조급함의')
    s.ch('on the faces', '얼굴들에')
    s.ch('of the people', '사람들의')
    s.ch('in line.', '줄을 선.')
    s.natural('줄을 선 사람들의 얼굴에는 조급한 표정이 역력하다.')
    s.cl('main', 'There', subj='a look of impatience', verbs=[], vfirst=['is'], disp='a look',
         disp_review='중심명사 look까지 표시하고 뒤에서 꾸미는 of impatience는 제외(유도부사 There는 주어 아님)')
    s.g('is', 'is', '있다')
    s.g('look', 'look', '표정, 얼굴빛 (흔한 뜻: 보다)')
    s.g('of', 'of', '~의')
    s.g('impatience', 'impatience', '조급함, 초조함', star=W['impatience'])
    s.g('on', 'on', '~에')
    s.g('faces', 'faces', '얼굴들')
    s.g('of', 'of', '~의', at=s.text.index('of the people'))
    s.g('people', 'people', '사람들')
    s.g('in|line', 'in line', '줄을 선')
    there_cov(s)
    s.brk('of', 'postnominal-preposition', 'of impatience는 앞 명사 a look을 뒤에서 꾸미는 전치사구')
    s.brk('of', 'postnominal-preposition', 'of the people은 앞 명사 the faces를 뒤에서 꾸미는 전치사구',
          after=s.text.index('of the people'))
    s.brk('in', 'postnominal-preposition', 'in line은 앞 명사 the people을 뒤에서 꾸미는 전치사구')
    s.hint('a look [of impatience]', '[조급함의] 표정', span='a look of impatience', label='전치사구 후치수식',
           links=[(['of'], ['의'])], meaning='조급함의 표정(조급한 표정)',
           explanation='of impatience가 앞 명사 a look을 뒤에서 꾸민다. of ↔ 의.')
    s.hint('the people [in line]', '[줄을 선] 사람들', span='the people in line', label='전치사구 후치수식',
           links=[(['in line'], ['줄을 선'])], meaning='줄을 선 사람들',
           explanation='in line(줄을 선)이 앞 명사 the people을 뒤에서 꾸민다. in line은 한 덩어리 뜻이라 전체를 대응.')
    s.review = ('유도부사 There + is + 주어 a look of impatience(표시는 a look). on the faces는 is(있다)의 장소. '
                '후치 전치사구 세 곳(of impatience, of the people, in line) 앞에서 끊음. 힌트 2개(후치수식 두 곳). 관계사·수동 없음.')
    out.append(s)

    # ---------------- s19 ----------------
    s = S('s19', T['s19'])
    s.ch('There is even hostility,', '심지어 적대감도 있다,')
    s.ch('hidden', '숨겨진')
    s.ch('by a thin layer', '얇은 층에 의해')
    s.ch('of politeness.', '공손함의.')
    s.natural('얇은 공손함 뒤에 숨은 적대감마저 느껴진다.')
    s.cl('main', 'There', subj='hostility', verbs=[], vfirst=['is'])
    s.g('is', 'is', '있다')
    s.g('even', 'even', '심지어')
    s.g('hostility', 'hostility', '적대감', star=W['hostility'])
    hd = s.g('hidden', 'hidden', '숨겨진', verb_form=pp('past-participle', s, 'hidden', 'hide'))
    s.g('by', 'by', '~에 의해')
    s.g('thin', 'thin', '얇은')
    s.g('layer', 'layer', '층, 겹')
    s.g('of', 'of', '~의')
    s.g('politeness', 'politeness', '공손함, 예의 바름', star=W['politeness'])
    there_cov(s)
    s.brk('by', 'passive-agent-by', 'by a thin layer of politeness는 hidden(숨겨진)의 행위 주체를 나타내는 by 구')
    s.brk('of', 'postnominal-preposition', 'of politeness는 앞 명사 a thin layer를 뒤에서 꾸미는 전치사구')
    s.hint('hostility, [hidden by a thin layer]', '[얇은 층에 의해 숨겨진] 적대감', span='hostility, hidden by a thin layer',
           label='과거분사 후치수식', links=[(['hidden'], ['숨겨진'])], participle_focus_gloss_id=hd['id'],
           meaning='(공손함의) 얇은 층에 의해 숨겨진 적대감',
           explanation='콤마 뒤 과거분사구 hidden by …가 앞 명사 hostility를 설명한다. 적대감이 ‘숨겨진’ 쪽이라 과거분사. 독립 p.p. hidden ↔ 숨겨진 전체 대응. of politeness는 표시에서 제외.')
    s.review = ('유도부사 There + is + 주어 hostility. 콤마 뒤 과거분사구 hidden by a thin layer of politeness가 hostility를 꾸밈(수동 관계의 by 앞에서 끊음). '
                'hidden은 독립 p.p.(be 없음). 힌트 1개(과거분사 후치수식). 관계사·유한 수동 없음.')
    out.append(s)

    # ---------------- s20 ----------------
    s = S('s20', T['s20'])
    s.ch('Even that politeness', '심지어 그 공손함조차')
    s.ch('is stretched thin.', '얇게 늘어나 있다.')
    s.natural('그 공손함마저 곧 끊어질 듯 얇게 늘어나 있다.')
    s.cl('main', 'Even', subj='that politeness', verbs=['is', 'stretched'])
    s.g('Even', 'even', '~조차, 심지어')
    s.g('that', 'that', '그')
    s.g('politeness', 'politeness', '공손함, 예의 바름', star=W['politeness'])
    f = s.g('is', 'be p.p.', '~되어 있다', kind='function', combines_with=[])
    st = s.g('stretched', 'stretched', '늘어난, 팽팽하게 당겨진', verb_form=pp('passive-participle', s, 'stretched', 'stretch', f['id']))
    link(f, st)
    s.g('thin', 'thin', '얇게')
    s.vf_hint(fn=f, lex=st, en='is stretched', ko='늘어나 있다', formula='be p.p.', step_form='stretched', step_ko='늘어난',
              en_mark=['is'], ko_mark=['있다'], span='that politeness is stretched', meaning='늘어나 있다',
              explanation='빈 힌트 문장의 수동태 후보: is stretched(현재 수동, 상태). 주어 that politeness와 보어 thin은 제외.')
    s.review = ('단일 주절 수동 is stretched + 결과 보어 thin(stretched thin: 얇게 늘어난 → 한계에 가까운). that은 지시 한정사(앞 문장 politeness). '
                '관계사·접속사절 없음 → 빈 힌트 문장의 수동태 기능 결합 힌트.')
    out.append(s)

    # ---------------- s21 ----------------
    s = S('s21', T['s21'])
    s.ch('As I approach the back', '내가 뒤편에 다가갈 때')
    s.ch('of the store', '가게의')
    s.ch('for water bottles,', '생수병들을 구하러,')
    s.ch('I realize', '나는 깨닫는다')
    s.ch('I am too late.', '내가 너무 늦었다는 것을.')
    s.natural('생수를 구하러 매장 뒤편으로 다가가던 나는 내가 너무 늦었다는 것을 깨닫는다.')
    s.cl('subordinate', 'As', subj='I', verbs=['approach'], marker='As')
    s.cl('main', 'I', subj='I', verbs=['realize'], occ=1)
    s.cl('subordinate', 'I', subj='I', verbs=['am'], marker='that', omitted=True, occ=2)
    s.g('As', 'as S′ V′', 'S′(이/가) V′할 때')
    s.g('I', 'I', '내가', referent_ko='Alyssa')
    s.g('approach', 'approach', '~에 다가가다')
    s.g('back', 'back', '뒤쪽, 뒤편')
    s.g('of', 'of', '~의')
    s.g('store', 'store', '가게, 매장')
    s.g('for', 'for', '~을 구하러')
    s.g('water|bottles', 'water bottles', '생수병들, 물병들')
    s.g('I', 'I', '나는', referent_ko='Alyssa', at=s.text.index('I realize'))
    s.g('realize', 'realize', '깨닫다')
    s.g('I', 'I', '내가', referent_ko='Alyssa', at=s.text.index('I am'))
    s.g('am', 'am', '~이다')
    s.g('too', 'too', '너무')
    s.g('late', 'late', '늦은')
    s.brk('of', 'postnominal-preposition', 'of the store는 앞 명사 the back을 뒤에서 꾸미는 전치사구')
    s.hint('[As I approach]', '[내[Alyssa]가 다가갈 때]', span='As I approach', label='시간 접속사 as',
           links=[(['As'], ['가', '갈 때'])], refs=[('I', '내', '[Alyssa]')],
           meaning='내가 (가게 뒤편에) 다가갈 때',
           explanation='시간의 접속사 as(~할 때). S′ I, V′ approach까지 표시하고 목적어 the back of the store는 제외.')
    s.hint('[(that) I am too late]', '[내[Alyssa]가 너무 늦었다는 것]', span='I am too late',
           label='명사절 접속사 that 생략', display_mode='omitted-conjunction', omitted_conjunction='that',
           links=[(['that'], ['가', '다는 것'])], refs=[('I', '내', '[Alyssa]')],
           meaning='내가 너무 늦었다는 것',
           explanation='realize의 목적어인 명사절 앞에 접속사 that이 생략되었다. S′ I, V′ am에 be동사의 최소 보어 too late까지 표시.')
    s.review = ('문두 부사절 As I approach the back of the store for water bottles(시간) + 주절 I realize + 생략 that 명사절 I am too late. '
                'of the store 후치수식(of 앞에서 끊음). for water bottles는 approach의 목적(~을 구하러). 힌트 2개(as절, 생략 that 명사절). 관계사·수동 없음.')
    out.append(s)

    # ---------------- s22 ----------------
    s = S('s22', T['s22'])
    s.ch('The shelves are already empty.', '선반들은 이미 비어 있다.')
    s.natural('진열대는 이미 텅 비어 있다.')
    s.cl('main', 'The', subj='The shelves', verbs=['are'])
    s.g('shelves', 'shelves', '선반들, 진열대들')
    s.g('are', 'are', '~이다')
    s.g('already', 'already', '이미')
    s.g('empty', 'empty', '비어 있는, 텅 빈')
    s.review = '단일 주절(S: The shelves, V: are + 보어 empty). 절 연결·관계사·수동 없음 → 힌트 없음.'
    out.append(s)

    # ---------------- s23 ----------------
    s = S('s23', T['s23'])
    s.ch('I manage my way', '나는 애써 나아간다')
    s.ch('to the side aisle,', '옆 통로로,')
    s.ch('trying my luck.', '내 운을 시험해 보면서.')
    s.natural('나는 운을 시험해 볼 겸 사람들 사이를 헤치고 옆 통로로 간다.')
    s.cl('main', 'I', subj='I', verbs=['manage'])
    s.g('I', 'I', '나는', referent_ko='Alyssa')
    s.g('manage|my|way', 'manage one’s way', '(사람들 사이를) 애써 헤치고 나아가다')
    s.g('to', 'to', '~로')
    s.g('side', 'side', '옆의, 측면의')
    s.g('aisle', 'aisle', '통로', star=W['aisle'])
    f = s.g('trying', 'V-ing', '~하면서', kind='function', combines_with=[])
    tr = s.g('trying|my|luck', 'try one’s luck', '운을 시험해 보다', same=True, verb_form=pp('ing', s, 'trying', 'try'))
    link(f, tr)
    s.hint('[trying my luck]', '[내[Alyssa] 운을 시험해 보면서]', span='trying my luck', label='분사구문',
           links=[(['ing'], ['면서'])], refs=[('my', '내', '[Alyssa]')],
           meaning='내 운을 시험해 보면서',
           explanation='콤마 뒤 trying my luck은 앞 동작과 동시에 일어나는 일을 덧붙이는 분사구문. ing ↔ 면서.')
    s.review = ('단일 주절 I manage my way to the side aisle(manage one’s way: 애써 헤치고 나아가다) + 콤마 뒤 분사구문 trying my luck(동시 동작). '
                '힌트 1개(분사구문). 관계사·수동 없음.')
    out.append(s)

    # ---------------- s24 ----------------
    s = S('s24', T['s24'])
    s.ch('Sometimes', '때때로')
    s.ch('people place unwanted items', '사람들은 원하지 않는 물건들을 놓는다')
    s.ch('in the wrong shelves.', '엉뚱한 선반들에.')
    s.natural('가끔 사람들은 필요 없어진 물건을 엉뚱한 진열대에 놓아 두기도 한다.')
    s.cl('main', 'people', subj='people', verbs=['place'])
    s.g('Sometimes', 'sometimes', '때때로, 가끔')
    s.g('people', 'people', '사람들')
    s.g('place', 'place', '놓다, 두다 (흔한 뜻: 장소)')
    s.g('unwanted', 'unwanted', '원하지 않는, 필요 없는')
    s.g('items', 'items', '물건들, 물품들')
    s.g('in', 'in', '~에')
    s.g('wrong', 'wrong', '잘못된, 엉뚱한')
    s.g('shelves', 'shelves', '선반들, 진열대들')
    s.review = '단일 주절(S: people, V: place). 관계사·접속사절·수동 없음 → 힌트 없음.'
    out.append(s)

    # ---------------- s25 ----------------
    s = S('s25', T['s25'])
    s.ch('Lucky!', '운이 좋다!')
    s.natural('운이 좋다!')
    verbless(s, 's24', T['s24'], '감탄 표현(형용사 Lucky 하나로 된 외침). 유한동사가 없어 S/V 줄을 생략한다.')
    s.g('Lucky', 'lucky', '운이 좋은')
    s.review = '유한동사가 없는 감탄 표현. 2026-09-28 사용자 결정으로 S/V 줄과 안내문 생략(verbless-fragment). 힌트 없음.'
    out.append(s)

    # ---------------- s26 ----------------
    s = S('s26', T['s26'], key=True)
    s.ch('I find a single case of water', '나는 딱 한 상자의 생수를 발견한다')
    s.ch('that someone abandoned there', '누군가가 그곳에 버려두었던')
    s.ch('maybe yesterday,', '아마 어제,')
    s.ch('when it wasn’t such a precious commodity.', '그리고 그때 그것은 그렇게 귀한 물건이 아니었다.')
    s.natural('누군가 아마 어제쯤 그곳에 두고 간 생수 한 상자를 발견한다. 그때만 해도 물은 그렇게 귀한 물건이 아니었다.')
    s.cl('main', 'I', subj='I', verbs=['find'])
    s.cl('subordinate', 'that', subj='someone', verbs=['abandoned'], marker='that')
    s.cl('subordinate', 'when', subj='it', verbs=['wasn’t'], marker='when')
    s.g('I', 'I', '나는', referent_ko='Alyssa')
    s.g('find', 'find', '발견하다')
    q = s.g('a single case of', 'a single case of', '(딱) 한 상자의')
    s.g('water', 'water', '생수, 물')
    rel1 = s.g('that', 'that S′ V′', 'S′(이/가) V′했던 (관계대명사)')
    s.g('someone', 'someone', '누군가')
    s.g('abandoned', 'abandon', '버리다, 버려두다', verb_form=pp('regular-past', s, 'abandoned', 'abandon'))
    s.g('there', 'there', '그곳에')
    s.g('maybe', 'maybe', '아마')
    s.g('yesterday', 'yesterday', '어제')
    rel2 = s.g('when', 'when S′ V′', '그리고 그때 S′(이/가) V′하다 (관계부사)')
    s.g('it', 'it', '그것이', referent_ko='생수')
    s.g('wasn’t', 'wasn’t', '~이 아니었다 (= was not)')
    s.g('such|a', 'such a', '그렇게, 그토록')
    s.g('precious', 'precious', '귀한, 귀중한', star=W['precious'])
    s.g('commodity', 'commodity', '상품, 물건', star=W['commodity'])
    s.prot('a single case of', 'quantity-kind-of', '수량 표현 a single case of가 뒤 명사 water 앞에서 ‘(딱) 한 상자의’로 같은 어순 대응', gloss=q)
    s.hint('a single case of water [that someone abandoned]', '[누군가가 버려두었던] 한 상자의 생수',
           span='a single case of water that someone abandoned', label='목적격 관계대명사 that',
           links=[(['that'], [('가', 1), '던'])], meaning='누군가가 (그곳에) 버려두었던 생수 한 상자',
           explanation='선행사 a single case of water를 목적격 관계대명사 that이 받는다(abandon의 목적어). S′ someone, V′ abandoned까지 표시하고 there maybe yesterday는 제외. 과거의 일이라 ‘버려두었던’.')
    s.hint('yesterday, [when it wasn’t such a precious commodity]', '어제, [그리고 그때 그것[생수]이 그렇게 귀한 물건이 아니었다]',
           span='yesterday, when it wasn’t such a precious commodity', label='계속적 관계부사 when',
           links=[(['when'], ['그리고 그때', '이'])], refs=[('it', '그것', '[생수]')],
           meaning='어제, 그리고 그때(어제) 그것(생수)은 그렇게 귀한 물건이 아니었다',
           explanation='콤마 뒤 관계부사 when이 선행사 yesterday를 받아 ‘그리고 그때’로 설명을 덧붙인다. S′ it, V′ wasn’t에 be동사의 최소 보어 such a precious commodity까지 표시.')
    s.relative_ids = [rel1['id'], rel2['id']]
    s.review = ('주절 I find a single case of water(수량 표현 a single case of) + 목적격 관계대명사 that절(someone abandoned there maybe yesterday) '
                '+ 콤마 뒤 계속적 관계부사 when절(선행사 yesterday, it = 생수, wasn’t = was not). 필수 관계사 힌트 2개. abandoned는 일반 과거. 수동 없음.')
    out.append(s)

    # ---------------- s27 ----------------
    s = S('s27', T['s27'], key=True)
    s.ch('I reach for it,', '나는 그것을 향해 손을 뻗는다,')
    s.ch('only to find it pulled away', '그러나 결국 그것이 당겨져 가 버린 것을 발견할 뿐이다')
    s.ch('at the last second', '마지막 순간에')
    s.ch('by a woman.', '한 여자에 의해.')
    s.natural('나는 그 상자를 향해 손을 뻗지만, 마지막 순간에 한 여자가 그것을 끌어가 버린다.')
    s.cl('main', 'I', subj='I', verbs=['reach'])
    s.g('I', 'I', '나는', referent_ko='Alyssa')
    s.g('reach|for', 'reach for', '~을 향해 손을 뻗다')
    s.g('it', 'it', '그것', referent_ko='생수 한 상자')
    f = s.g('only|to', 'only to V', '(그러나) 결국 ~할 뿐이다', kind='function', combines_with=[])
    fd = s.g('find', 'find', '발견하다, 알게 되다')
    link(f, fd)
    s.g('it', 'it', '그것이', referent_ko='생수 한 상자', at=s.text.index('it pulled'))
    s.g('pulled|away', 'pulled away', '당겨져 가 버린, 끌려간', verb_form={
        'usage': 'past-participle', 'source_span': s.span_of('pulled'), 'lemma': 'pull'})
    s.g('at|the|last|second', 'at the last second', '마지막 순간에')
    s.g('by', 'by', '~에 의해')
    s.g('woman', 'woman', '여자')
    s.brk('by', 'passive-agent-by', 'by a woman은 pulled away(당겨져 간)의 행위 주체를 나타내는 by 구')
    s.hint('[only to find]', '[그러나 결국 발견할 뿐이다]', span='only to find', label='결과의 to부정사 only to',
           links=[(['only to'], ['그러나 결국', '할 뿐이다'])],
           meaning='(손을 뻗었지만) 결국 (그것이 당겨져 가는 것을) 발견할 뿐이다',
           explanation='only to V는 앞 동작 뒤에 기대와 다른 결과가 이어짐을 나타낸다(~했지만 결국 …할 뿐이다). 목적어 it pulled away 이하는 표시에서 제외.')
    s.hint('find [it pulled away]', '[그것[생수 한 상자]이 당겨져 가 버린 것을] 발견하다', span='find it pulled away',
           label='find A p.p. 구문', emphasis_policy='ko-only-verb-construction',
           links=[(['find', 'pulled'], ['이', '것을'])], refs=[('it', '그것', '[생수 한 상자]')],
           meaning='그것이 당겨져 가 버린 것을 발견하다',
           explanation='find A p.p.: A가 ~된 것을 발견하다(알게 되다). A = it(생수 한 상자), p.p. = pulled away(당겨져 간). A 주어 조사 이와 연결 것을만 강조. only to 힌트와 다른 초점(동사 구문, 후순위).')
    s.review = ('단일 주절 I reach for it + 결과의 to부정사 only to find it pulled away(find A p.p.) + 행위 주체 by a woman(수동 관계, by 앞에서 끊음). '
                'pulled away는 독립 p.p.(be 없음). 힌트 2개(only to 결과, find A p.p. 동사 구문). 관계사·유한 수동 없음.')
    out.append(s)

    # ---------------- s28 ----------------
    s = S('s28', T['s28'])
    s.ch('She stacks it', '그녀는 그것을 쌓아 올린다')
    s.ch('on top of her cart', '그녀의 카트 맨 위에')
    s.ch('like a crown', '왕관처럼')
    s.ch('on top of her canned goods.', '그녀의 통조림 식품들 위의.')
    s.natural('그녀는 그 상자를 카트에 담긴 통조림 위에 왕관처럼 올려놓는다.')
    s.cl('main', 'She', subj='She', verbs=['stacks'])
    s.g('She', 'she', '그녀는', referent_ko='생수 상자를 가져간 여자')
    s.g('stacks', 'stack', '쌓다, 쌓아 올리다', verb_form=v3(s, 'stacks', 'stack', 'She'))
    s.g('it', 'it', '그것을', referent_ko='생수 한 상자')
    s.g('on|top|of', 'on top of', '~의 맨 위에')
    s.g('her', 'her', '그녀의', referent_ko='그 여자')
    s.g('cart', 'cart', '카트')
    s.g('like', 'like', '~처럼')
    s.g('crown', 'crown', '왕관')
    s.g('on|top|of', 'on top of', '~ 위의', at=s.text.index('on top of her canned'))
    s.g('her', 'her', '그녀의', referent_ko='그 여자', at=s.text.index('her canned'))
    s.g('canned|goods', 'canned goods', '통조림 식품들')
    s.brk('on', 'postnominal-preposition', 'on top of her canned goods는 앞 명사 a crown을 뒤에서 꾸미는 전치사구',
          after=s.text.index('on top of her canned'))
    s.review = ('단일 주절 She stacks it on top of her cart. like a crown on top of her canned goods는 비유(왕관처럼)이며 on top of her canned goods가 '
                'a crown을 꾸민다(on 앞에서 끊음). 관계사·접속사절·수동 없음. 비유의 뜻은 분석지 쉬운 풀이에서 설명 → 힌트 없음.')
    out.append(s)

    # ---------------- s29 ----------------
    s = S('s29', T['s29'])
    s.ch('“I’m sorry,', '“미안해요,')
    s.ch('but we were here first,”', '하지만 우리가 여기에 먼저 있었어요,”')
    s.ch('she says.', '그녀가 말한다.')
    s.natural('“미안하지만 우리가 먼저 왔어요.” 그 여자가 말한다.')
    im = s.at('I’m')
    s.cl_spans('main', im[0], subj=[im[0], im[0] + 1], verbs=[[im[0] + 1, im[1]]])
    s.cl('main', 'we', subj='we', verbs=['were'], marker='but')
    s.cl('main', 'she', subj='she', verbs=['says'])
    s.g('I’m', 'I’m', '나는 ~이다 (= I am)', referent_ko='그 여자')
    s.g('sorry', 'sorry', '미안한')
    s.g('we', 'we', '우리가', referent_ko='그 여자와 딸')
    s.g('were', 'were', '(~에) 있었다')
    s.g('here', 'here', '여기에')
    s.g('first', 'first', '먼저')
    s.g('she', 'she', '그녀가', referent_ko='그 여자')
    s.g('says', 'say', '말하다', verb_form=v3(s, 'says', 'say', 'she'))
    s.review = ('인용된 두 절 I’m sorry(’m = am) / but we were here first + 전달절 she says. S/V는 세 주절. 절 사이 but은 대조. '
                '관계사·수동 없음 → 힌트 없음.')
    out.append(s)

    # ---------------- s30 ----------------
    s = S('s30', T['s30'])
    s.ch('And then', '그러고 나서')
    s.ch('her daughter steps forward', '그녀의 딸이 앞으로 나온다')
    s.ch('— a girl', '— 한 소녀')
    s.ch('I recognize from soccer', '내가 축구부에서 알아보는')
    s.ch('— Hali Hartling.', '— Hali Hartling이다.')
    s.natural('그러자 그녀의 딸이 앞으로 나오는데, 내가 축구부에서 알고 지내는 Hali Hartling이다.')
    s.cl('main', 'her', subj='her daughter', verbs=['steps'])
    s.cl('subordinate', 'I', subj='I', verbs=['recognize'], marker='that', omitted=True)
    s.g('then', 'then', '그러고 나서, 그러자')
    s.g('her', 'her', '그녀의', referent_ko='그 여자')
    s.g('daughter', 'daughter', '딸')
    s.g('steps|forward', 'step forward', '앞으로 나오다', verb_form=v3(s, 'steps', 'step', 'her daughter'))
    s.g('girl', 'girl', '소녀')
    s.g('I', 'I', '내가', referent_ko='Alyssa')
    s.g('recognize', 'recognize', '(누구인지) 알아보다')
    s.g('from', 'from', '~에서')
    s.g('soccer', 'soccer', '축구부 (흔한 뜻: 축구)')
    s.g('Hali|Hartling', 'Hali Hartling', 'Hali Hartling (그 여자의 딸, Alyssa와 같은 축구부)', proper=True)
    s.hint('a girl [(that) I recognize]', '[내[Alyssa]가 알아보는] 한 소녀', span='a girl I recognize',
           label='목적격 관계대명사 that 생략', display_mode='omitted-relative', omitted_relative='that',
           links=[(['that'], ['가', '는'])], refs=[('I', '내', '[Alyssa]')],
           meaning='내가 (축구부에서) 알아보는 한 소녀',
           explanation='선행사 a girl 뒤 목적격 관계대명사 that이 생략된 관계절(I recognize from soccer). S′ I, V′ recognize까지 표시하고 from soccer는 제외. 줄표 사이의 a girl …은 her daughter를 다시 설명하는 동격.')
    s.review = ('주절 her daughter steps forward + 줄표 사이 동격 a girl (that) I recognize from soccer + 줄표 뒤 이름 Hali Hartling(her daughter의 동격). '
                '목적격 관계대명사가 생략된 관계절 → 생략 관계사 힌트 1개. 문두 And는 단독 각주 제외. 수동 없음.')
    out.append(s)

    # ---------------- s31 ----------------
    s = S('s31', T['s31'])
    s.ch('As her mother pulls their cart away,', '그녀의 엄마가 그들의 카트를 끌고 갈 때,')
    s.ch('Hali leans closer to me.', 'Hali는 나 쪽으로 더 가까이 몸을 기울인다.')
    s.natural('엄마가 카트를 끌고 가자 Hali가 내 쪽으로 몸을 기울인다.')
    s.cl('subordinate', 'As', subj='her mother', verbs=['pulls'], marker='As')
    s.cl('main', 'Hali', subj='Hali', verbs=['leans'])
    s.g('As', 'as S′ V′', 'S′(이/가) V′할 때')
    s.g('her', 'her', '그녀의', referent_ko='Hali')
    s.g('mother', 'mother', '엄마, 어머니')
    s.g('pulls|away', 'pull A away', 'A를 끌고 가다', verb_form=v3(s, 'pulls', 'pull', 'her mother'),
        verb_construction={'kind': 'verb-frame', 'verb_span': s.span_of('pulls'), 'lemma': 'pull',
                           'link_spans': [s.span_of('away')], 'review_record': 'pulls their cart away: A = their cart, away는 분리된 불변화사.'})
    s.g('their', 'their', '그들의', referent_ko='Hali와 엄마')
    s.g('cart', 'cart', '카트')
    s.g('leans', 'lean', '몸을 기울이다', verb_form=v3(s, 'leans', 'lean', 'Hali'))
    s.g('closer', 'closer', '더 가까이 (close의 비교급)')
    s.g('to', 'to', '~쪽으로')
    s.g('me', 'me', '나', referent_ko='Alyssa')
    ab = s.span_of('As her mother pulls')
    aw = s.span_of('away')
    s.hint('[As her mother pulls … away]', '[그녀[Hali]의 엄마가 끌고 갈 때]', span='As her mother pulls their cart away',
           label='시간 접속사 as', display_mode='split-phrasal-verb', display_spans=[ab, aw],
           links=[(['As'], ['가', '갈 때'])], refs=[('her', '그녀', '[Hali]')],
           meaning='그녀의 엄마가 (그들의 카트를) 끌고 갈 때',
           explanation='시간의 접속사 as(~할 때). S′ her mother, V′ pulls … away(pull A away: A를 끌고 가다)에서 사이 목적어 their cart만 생략해 표시.')
    s.review = ('문두 부사절 As her mother pulls their cart away(pull A away 분리 구동사) + 주절 Hali leans closer to me. Hali는 s30에서 제공한 고유명사 반복. '
                '접속사절 힌트 1개(분리 구동사 목적어 생략 표시). 관계사·수동 없음.')
    out.append(s)

    # ---------------- s32 ----------------
    s = S('s32', T['s32'])
    s.ch('“I’m sorry about that, Alyssa.”', '“그 일에 대해 미안해, Alyssa.”')
    s.natural('“그 일은 미안해, Alyssa.”')
    im = s.at('I’m')
    s.cl_spans('main', im[0], subj=[im[0], im[0] + 1], verbs=[[im[0] + 1, im[1]]])
    s.g('I’m', 'I’m', '나는 ~이다 (= I am)', referent_ko='Hali')
    s.g('sorry', 'sorry', '미안한')
    s.g('about', 'about', '~에 대해')
    s.g('that', 'that', '그것, 그 일', referent_ko='엄마가 생수 상자를 가져간 일')
    s.review = '인용된 단일 절 I’m sorry about that(’m = am). Alyssa는 호격(s05 고유명사 반복). 절 연결·수동 없음 → 힌트 없음.'
    out.append(s)

    # ---------------- s33 ----------------
    s = S('s33', T['s33'])
    s.ch('“Didn’t I share my water with you', '“내가 너와 내 물을 나누지 않았니')
    s.ch('at the practice', '연습 때')
    s.ch('last week?”', '지난주?”')
    s.ch('I point out to her.', '나는 그녀에게 짚어 말한다.')
    s.natural('“지난주 연습 때 내가 너한테 물을 나눠 주지 않았니?” 나는 그녀에게 짚어 말한다.')
    dn = s.at('Didn’t')
    s.cl_spans('main', dn[0], subj=s.at('I'), verbs=[dn, s.at('share')])
    s.cl('main', 'I', subj='I', verbs=['point'], occ=1)
    s.g('Didn’t', 'didn’t V', '~하지 않았니? (= did not)')
    s.g('I', 'I', '내가', referent_ko='Alyssa')
    s.g('share|with', 'share A with B', 'A를 B와 나누다',
        verb_construction={'kind': 'verb-frame', 'verb_span': s.span_of('share'), 'lemma': 'share',
                           'link_spans': [s.span_of('with')], 'review_record': 'share my water with you: A = my water, B = you.'})
    s.g('my', 'my', '나의', referent_ko='Alyssa')
    s.g('water', 'water', '물')
    s.g('at', 'at', '~ 때')
    s.g('practice', 'practice', '(축구) 연습')
    s.g('last|week', 'last week', '지난주')
    s.g('I', 'I', '나는', referent_ko='Alyssa', at=s.text.index('I point'))
    s.g('point|out', 'point out', '(사실을) 짚어 말하다, 지적하다')
    s.g('to', 'to', '~에게')
    s.g('her', 'her', '그녀', referent_ko='Hali')
    s.review = ('인용된 부정 의문문 Didn’t I share my water with you …?(S: I, V: Didn’t share; share A with B) + 전달절 I point out to her. '
                '관계사·접속사절·수동 없음. 부정 의문의 뜻은 각주 didn’t V로 지원 → 힌트 없음.')
    out.append(s)

    # ---------------- s34 ----------------
    s = S('s34', T['s34'])
    s.ch('“Maybe you could return the favor', '“아마 너는 그 호의를 갚을 수 있을 거야')
    s.ch('and share a few bottles with me.”', '그리고 나와 몇 병을 나눌 수 있을 거야.”')
    s.natural('“너도 그 호의를 갚는 셈 치고 나랑 물 몇 병 나눠 주면 좋겠어.”')
    s.cl('main', 'you', subj='you', verbs=['could', 'return', 'and', 'share'])
    s.g('Maybe', 'maybe', '아마, 어쩌면')
    f = s.g('could', 'could V', '~할 수 있을 것이다', kind='function', combines_with=[])
    rt = s.g('return|the|favor', 'return the favor', '(받은) 호의를 갚다', star=W['favor'])
    sh = s.g('share|with', 'share A with B', 'A를 B와 나누다',
             verb_construction={'kind': 'verb-frame', 'verb_span': s.span_of('share'), 'lemma': 'share',
                                'link_spans': [s.span_of('with')], 'review_record': 'share a few bottles with me: A = a few bottles, B = me.'})
    link(f, rt, sh)
    s.g('a|few', 'a few', '몇몇의, 몇 개의')
    s.g('bottles', 'bottles', '병들')
    s.g('me', 'me', '나', referent_ko='Alyssa')
    s.hint('could [return the favor and share]', '[호의를 갚고 나눌] 수 있을 것이다', span='could return the favor and share',
           label='조동사 could의 병렬 동사', links=[(['could'], ['수 있을 것이다'])],
           meaning='호의를 갚고 (몇 병을) 나눌 수 있을 것이다',
           explanation='조동사 could 뒤에 return the favor와 share가 and로 병렬되어 둘 다 could에 걸린다. share 앞에 could가 없어 놓치기 쉬워 병렬 두 동사까지 표시하고 a few bottles with me는 제외. Maybe you could …는 부드러운 제안.')
    s.review = ('인용된 단일 절: 조동사 could + 병렬 동사 return the favor and share a few bottles with me(share A with B). Maybe you could …는 완곡한 제안. '
                'could를 과거로 고정하지 않음. 힌트 1개(could의 병렬 동사). 관계사·수동 없음.')
    out.append(s)

    # ---------------- s35 ----------------
    s = S('s35', T['s35'])
    s.ch('She looks back to her mother,', '그녀는 그녀의 엄마를 돌아본다,')
    s.ch('who’s already moving down the aisle,', '그리고 그 사람은 이미 통로를 따라 이동하고 있다,')
    s.ch('then turns back to me', '그러고 나서 나에게로 다시 돌아선다')
    s.ch('shaking her head.', '그녀의 고개를 저으면서.')
    s.natural('Hali는 이미 통로를 따라 걸어가고 있는 엄마를 돌아보더니, 고개를 저으며 다시 내 쪽으로 돌아선다.')
    s.cl('main', 'She', subj='She', verbs=['looks', 'then', 'turns'])
    who = s.at('who’s')
    s.cl_spans('subject_relative', who[0], verbs=[[who[0] + 3, who[1]], s.at('moving')], marker='who',
               readings=[{'span': [who[0] + 3, who[1]], 'expanded': 'is'}])
    s.g('She', 'she', '그녀는', referent_ko='Hali')
    s.g('looks|back|to', 'look back to', '~을 돌아보다', verb_form=v3(s, 'looks', 'look', 'She'))
    s.g('her', 'her', '그녀의', referent_ko='Hali')
    s.g('mother', 'mother', '엄마, 어머니')
    rel = s.g('who’s', 'who’s V-ing', '그리고 그 사람은 ~하고 있다 (관계대명사, who’s = who is)')
    s.g('already', 'already', '이미')
    s.g('moving', 'move', '이동하다, 움직이다', verb_form=pp('ing', s, 'moving', 'move'))
    s.g('down', 'down', '~을 따라')
    s.g('aisle', 'aisle', '통로', star=W['aisle'])
    s.g('then', 'then', '그러고 나서')
    s.g('turns|back', 'turn back', '다시 돌아서다', verb_form=v3(s, 'turns', 'turn', 'She'))
    s.g('to', 'to', '~쪽으로', at=s.text.index('to me'))
    s.g('me', 'me', '나', referent_ko='Alyssa')
    f = s.g('shaking', 'V-ing', '~하면서', kind='function', combines_with=[])
    sk = s.g('shaking', 'shake', '(고개를) 젓다, 흔들다', same=True, verb_form=pp('ing', s, 'shaking', 'shake'))
    link(f, sk)
    s.g('her', 'her', '그녀의', referent_ko='Hali', at=s.text.index('her head'))
    s.g('head', 'head', '머리, 고개')
    s.hint('her mother, [who’s already moving]', '그녀[Hali]의 엄마, [그리고 그 사람은 이미 이동하고 있다]',
           span='her mother, who’s already moving', label='계속적 관계대명사 who',
           links=[(['who'], ['그리고 그 사람은'])], refs=[('her', '그녀', '[Hali]')],
           meaning='그녀의 엄마, 그리고 그 사람(엄마)은 이미 (통로를 따라) 이동하고 있다',
           explanation='콤마 뒤 주격 관계대명사 who가 선행사 her mother를 받아 설명을 덧붙인다(who’s = who is, 진행형). 주격이라 별도 S′ 없이 V′ ’s moving까지 표시하고 down the aisle은 제외.')
    s.hint('[shaking her head]', '[그녀[Hali]의 고개를 저으면서]', span='shaking her head', label='분사구문',
           links=[(['ing'], ['면서'])], refs=[('her', '그녀', '[Hali]')],
           meaning='그녀의 고개를 저으면서',
           explanation='shaking her head는 turns back과 동시에 일어나는 동작을 덧붙이는 분사구문. ing ↔ 면서.')
    s.relative_ids = [rel['id']]
    s.review = ('주절 She looks back to her mother …, then turns back to me(한 주어 She의 두 동사 looks·turns를 then이 이어 줌 — then은 부사지만 and 없이 두 동사를 잇는 연결 자리라 V 표시에 보존 — 2026-09-28 사용자 승인 예외, approved-exceptions.md 기록) '
                '+ 콤마 뒤 계속적 관계대명사 who절(who’s = who is, V′ ’s moving) + 분사구문 shaking her head. 힌트 2개(필수 관계사, 분사구문). 수동 없음.')
    out.append(s)

    # ---------------- s36 ----------------
    s = S('s36', T['s36'])
    s.ch('And then', '그러고 나서')
    s.ch('she gets a little bit red in the face,', '그녀는 얼굴이 조금 빨개진다,')
    s.ch('and turns to leave', '그리고 떠나기 위해 돌아선다')
    s.ch('before it becomes a deep flush.', '그것이 짙은 홍조가 되기 전에.')
    s.natural('그러고는 얼굴이 살짝 붉어지더니, 얼굴이 새빨개지기 전에 자리를 뜨려고 돌아선다.')
    s.cl('main', 'she', subj='she', verbs=['gets', 'and', 'turns'])
    s.cl('subordinate', 'before', subj='it', verbs=['becomes'], marker='before')
    s.g('then', 'then', '그러고 나서')
    s.g('she', 'she', '그녀는', referent_ko='Hali')
    s.g('gets', 'get', '(~한 상태가) 되다, ~해지다', verb_form=v3(s, 'gets', 'get', 'she'))
    s.g('a|little|bit', 'a little bit', '조금, 약간')
    s.g('red|in|the|face', 'red in the face', '얼굴이 빨개진')
    s.g('turns', 'turn', '돌아서다', verb_form=v3(s, 'turns', 'turn', 'she'))
    f = s.g('to', 'to V', '~하기 위해', kind='function', combines_with=[])
    lv = s.g('leave', 'leave', '떠나다')
    link(f, lv)
    s.g('before', 'before S′ V′', 'S′(이/가) V′하기 전에')
    s.g('it', 'it', '그것이', referent_ko='얼굴의 붉은 기')
    s.g('becomes', 'become', '~이 되다', verb_form=v3(s, 'becomes', 'become', 'it'))
    s.g('deep', 'deep', '짙은, 깊은')
    s.g('flush', 'flush', '(얼굴의) 홍조, 붉어짐', star=W['flush'])
    s.hint('[to leave]', '[떠나기 위해]', span='to leave', label='목적의 to부정사',
           links=[(['to'], ['기 위해'])], meaning='떠나기 위해(자리를 뜨려고)',
           explanation='turns to leave에서 to leave는 돌아서는 목적(떠나려고).')
    s.hint('[before it becomes a deep flush]', '[그것[얼굴의 붉은 기]이 짙은 홍조가 되기 전에]', span='before it becomes a deep flush',
           label='시간 접속사 before', links=[(['before'], ['이', '기 전에'])], refs=[('it', '그것', '[얼굴의 붉은 기]')],
           meaning='그것(얼굴의 붉은 기)이 짙은 홍조가 되기 전에',
           explanation='before S′ V′: S′가 V′하기 전에. S′ it(얼굴의 붉은 기), V′ becomes에 뜻을 잡는 최소 보어 a deep flush까지 표시(연결동사 become; 연결동사 최소 보어 표시는 2026-09-28 사용자 결정).')
    s.review = ('주절 she gets a little bit red in the face, and turns to leave(한 주어의 병렬 동사 gets·turns) + before절(it becomes a deep flush). '
                'to leave는 목적. 힌트 2개(목적 to V, before절). 문두 And는 단독 각주 제외. 관계사·수동 없음.')
    out.append(s)
    return out


UNIT = {
    'id': 'u2', 'source_id': 'src', 'paragraph_ids': ['p09', 'p10', 'p11', 'p12', 'p13', 'p14', 'p15'],
    'sentence_ids': [f's{n:02d}' for n in range(18, 37)],
    'today_words': [
        {'id': W['impatience'], 'text': 'impatience', 'meaning_ko': '조급함, 초조함'},
        {'id': W['hostility'], 'text': 'hostility', 'meaning_ko': '적대감'},
        {'id': W['politeness'], 'text': 'politeness', 'meaning_ko': '공손함, 예의 바름'},
        {'id': W['aisle'], 'text': 'aisle', 'meaning_ko': '통로'},
        {'id': W['precious'], 'text': 'precious', 'meaning_ko': '귀한, 귀중한'},
        {'id': W['commodity'], 'text': 'commodity', 'meaning_ko': '상품, 물건'},
        {'id': W['favor'], 'text': 'return the favor', 'meaning_ko': '(받은) 호의를 갚다'},
        {'id': W['flush'], 'text': 'flush', 'meaning_ko': '(얼굴의) 홍조, 붉어짐'},
    ],
}


def analysis(_):
    return {
        'heading_kind': '제목',
        'title_or_topic_en': 'The Last Case of Water',
        'title_or_topic_ko': '마지막 생수 한 상자',
        'intent_ko': '물이 귀해지자 사람들은 겉으로는 예의를 지키지만 속으로는 적대감을 품고, Alyssa가 찾은 생수를 마지막 순간에 가로챈 여자도, 도움을 받았던 친구 Hali도 물을 나누지 않는 모습을 보여 준다.',
        'flow': [
            {'sentence_ids': ['s18', 's19', 's20'], 'label': '매장 분위기',
             'text_ko': '줄을 선 사람들의 얼굴에는 조급함이 가득하고, 얇은 예의 뒤에 적대감이 숨어 있다. 그 예의조차 곧 무너질 듯하다.'},
            {'sentence_ids': ['s21', 's22', 's23', 's24', 's25', 's26', 's27', 's28'], 'label': '생수 쟁탈',
             'text_ko': '진열대는 이미 비었지만 Alyssa는 옆 통로에서 누군가 두고 간 생수 한 상자를 찾아낸다. 그러나 손을 뻗는 순간 한 여자가 그것을 가져가 자기 카트 맨 위에 올려놓는다.'},
            {'sentence_ids': ['s29', 's30', 's31', 's32'], 'label': 'Hali의 등장',
             'text_ko': '여자는 자기들이 먼저 왔다고 말하고, 그 딸은 Alyssa가 축구부에서 아는 Hali다. Hali는 엄마가 떠나는 사이 Alyssa에게 미안하다고 말한다.'},
            {'sentence_ids': ['s33', 's34', 's35', 's36'], 'label': '거절',
             'text_ko': 'Alyssa는 지난주에 물을 나눠 준 일을 짚으며 몇 병만 나눠 달라고 한다. Hali는 엄마를 돌아본 뒤 고개를 젓고, 얼굴이 붉어진 채 자리를 뜬다.'},
        ],
        'easy_explanations': [
            {'sentence_id': 's20', 'explanatory_sentences': [
                '20번 문장은 19번에서 말한 ‘얇은 공손함’을 한 번 더 짚는다.',
                '사람들은 겉으로는 예의를 지키고 있다.',
                '하지만 그 예의는 고무줄처럼 팽팽하게 늘어나 있어서 조금만 더 당기면 끊어질 것 같다.',
                '물 때문에 사람들 사이의 다툼이 곧 터질 수 있다는 뜻이다.']},
            {'sentence_id': 's28', 'explanatory_sentences': [
                '28번 문장은 27번에서 생수 상자를 가져간 여자가 그 상자를 어떻게 다루는지 보여 준다.',
                '여자는 생수 상자를 카트 속 통조림 맨 위에 올려놓는다.',
                '글쓴이는 이 모습을 왕관을 머리에 올린 것에 빗댔다.',
                '왕관은 가장 귀한 보물을 떠올리게 한다.',
                '물이 그만큼 귀한 것이 되었다는 뜻이다.',
                '여자는 그 보물을 손에 넣은 사람처럼 보인다.']},
            {'sentence_id': 's36', 'explanatory_sentences': [
                '36번 문장은 35번에서 고개를 저은 Hali의 반응을 이어서 보여 준다.',
                'Hali는 지난주에 Alyssa에게 물을 나눠 받았다.',
                '그런데 이번에는 그 호의를 갚지 못하고 거절했다.',
                '그래서 Hali는 미안하고 부끄러웠을 것이다.',
                '얼굴이 새빨개지기 전에 Hali는 자리를 뜨려고 돌아선다.']},
        ],
        'grammar_points': [
            {'id': 'u2-gp1', 'sentence_id': 's21', 'span': 'I realize I am too late',
             'title': '(that) S′ V′: S′가 V′라는 것', 'formula_key': '(that) S′ V′',
             'explanation': '공식: realize (that) S′ V′ — S′(이/가) V′라는 것을 깨닫다. that = 생략된 명사절 접속사, S′ = I(내가), V′ = am(~이다), '
                            'too late = 너무 늦은. → 내가 너무 늦었다는 것(을 깨닫는다). realize 바로 뒤에 주어+동사가 오면 사이에 that이 빠진 것으로 보고 ‘~라는 것을’로 이어 읽는다.',
             'practice': {'span': 'I am too late',
                          'formula_support': {'en': '(that) S′ V′', 'ko': 'S′(이/가) V′라는 것'},
                          'support': [('s21', 'I', 2), ('s21', 'am'), ('s21', 'too'), ('s21', 'late')],
                          'answer_ko': '내가 너무 늦었다는 것'}},
            {'id': 'u2-gp2', 'sentence_id': 's26', 'span': 'a single case of water that someone abandoned there maybe yesterday',
             'title': '명사 + that S′ V′: S′가 V′했던 명사', 'formula_key': 'N + that S′ V′',
             'explanation': '공식: 명사(N) + that S′ V′ — S′(이/가) V′했던 N. N = a single case of water(생수 한 상자), that = 목적격 관계대명사(그 상자를), '
                            'S′ = someone(누군가), V′ = abandoned(버려두었다), there = 그곳에, maybe yesterday = 아마 어제. '
                            '→ 누군가가 아마 어제 그곳에 버려두었던 생수 한 상자. that 뒤에 abandon의 목적어가 비어 있어 that이 목적어 역할을 한다.',
             'practice': {'span': 'a single case of water that someone abandoned there maybe yesterday',
                          'formula_support': {'en': 'N + that S′ V′', 'ko': 'S′(이/가) V′했던 N'},
                          'support': [('s26', 'a single case of'), ('s26', 'water'), ('s26', 'someone'), ('s26', 'abandon'),
                                      ('s26', 'there'), ('s26', 'maybe'), ('s26', 'yesterday')],
                          'answer_ko': '누군가가 아마 어제 그곳에 버려두었던 생수 한 상자'}},
            {'id': 'u2-gp3', 'sentence_id': 's27', 'span': 'I reach for it, only to find it pulled away',
             'title': 'only to V: (그러나) 결국 ~할 뿐이다', 'formula_key': 'only to V',
             'explanation': '공식: 앞 동작, only to V — ~했지만 결국 V할 뿐이다. 앞 동작 = I reach for it(나는 그것을 향해 손을 뻗는다), V = find(발견하다), '
                            'find 뒤 내용 = it pulled away(그것이 당겨져 가 버린 것: it = 생수 한 상자, pulled away = 당겨져 가 버린). '
                            '→ 손을 뻗지만 결국 그것이 당겨져 가 버린 것을 발견할 뿐이다. 기대와 다른 결과가 이어짐을 보여 준다.',
             'practice': {'span': 'only to find it pulled away',
                          'formula_support': {'en': 'only to V', 'ko': '(그러나) 결국 ~할 뿐이다'},
                          'support': [('s27', 'find'), ('s27', 'it', 1), ('s27', 'pulled away')],
                          'answer_ko': '그러나 결국 그것이 당겨져 가 버린 것을 발견할 뿐이다'}},
        ],
        'formula_routes': [
            {'function': ('s20', 'be p.p.', 0), 'route': 'hint', 'hint_index': 0,
             'review_record': 'is stretched: 빈 힌트 문장의 수동태 기능 결합 힌트'},
        ],
        'relations': [
            {'head': {'id': 'u2-r1h', 'text': 'empty', 'meaning_ko': '비어 있는'},
             'synonym': {'id': 'u2-r1s', 'text': 'bare', 'meaning_ko': '텅 빈, 아무것도 없는'},
             'antonym': {'id': 'u2-r1a', 'text': 'full', 'meaning_ko': '가득 찬'}},
            {'head': {'id': 'u2-r2h', 'text': 'precious', 'meaning_ko': '귀한, 귀중한'},
             'synonym': {'id': 'u2-r2s', 'text': 'valuable', 'meaning_ko': '귀중한, 값비싼'},
             'antonym': {'id': 'u2-r2a', 'text': 'worthless', 'meaning_ko': '가치 없는, 쓸모없는'}},
            {'head': {'id': 'u2-r3h', 'text': 'politeness', 'meaning_ko': '공손함, 예의 바름'},
             'synonym': {'id': 'u2-r3s', 'text': 'courtesy', 'meaning_ko': '공손함, 예의'},
             'antonym': {'id': 'u2-r3a', 'text': 'rudeness', 'meaning_ko': '무례함'}},
        ],
    }


def workbook():
    return {
        'relation_order': ['u2-r3s', 'u2-r1a', 'u2-r2h', 'u2-r3a', 'u2-r1s', 'u2-r2a', 'u2-r3h', 'u2-r1h', 'u2-r2s'],
        'key_sentence_ids': ['s26', 's27'],
        'question_id': 'Q02',
        'syntax_point_ids': ['u2-gp1', 'u2-gp2', 'u2-gp3'],
    }
