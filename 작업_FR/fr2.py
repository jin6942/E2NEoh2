"""Further Reading 공통 단위 2: p03~p04 s13~s20 (경험이 더 오래가는 행복을 주는 이유).

사용자 결정(2026-09-27 “2단위 (추천)”): 소제목 없는 짧은 단락 p03·p04를 한 단위로 묶는다.
"""
from author import S, link
from fr1 import pp, v3, contraction

W = {'deliver': 'u2-w1', 'identity': 'u2-w2', 'accumulation': 'u2-w3', 'stuff': 'u2-w4',
     'nonetheless': 'u2-w5', 'remain': 'u2-w6', 'other_hand': 'u2-w7', 'sum_total': 'u2-w8'}


def ve(s, clause, index):
    """we’ve의 ’ve 위치를 V′ 앞에 넣는다(’ve는 have의 축약, has 병기 대상 아님)."""
    k = index + 2
    clause['verb_spans'] = [[k, k + 3]] + clause['verb_spans']


def sentences(T):
    out = []

    # ---------------- s13 ----------------
    s = S('s13', T['s13'], key=True)
    s.ch('Gilovich and other researchers have found', '길로비치와 다른 연구자들은 발견했다')
    s.ch('that experiences deliver longer lasting happiness', '경험들이 더 오래 지속되는 행복을 가져다준다는 것을')
    s.ch('than things.', '물건들보다.')
    s.natural('길로비치와 다른 연구자들은 경험이 물건보다 더 오래 지속되는 행복을 가져다준다는 것을 발견했다.')
    s.cl('main', 'Gilovich', subj='Gilovich and other researchers', verbs=['have', 'found'])
    s.cl('subordinate', 'that', subj='experiences', verbs=['deliver'], marker='that')
    s.g('other', 'other', '다른')
    s.g('researchers', 'researchers', '연구자들')
    f = s.g('have', 'have p.p.', '~했다', kind='function', combines_with=[])
    fd = s.g('found', 'find', '발견하다 (found는 find의 p.p.형)',
             verb_form=pp('perfect-participle', s, 'found', 'find', f['id']))
    link(f, fd)
    s.g('that', 'that S′ V′', 'S′(이/가) V′라는 것을')
    s.g('experiences', 'experiences', '경험들')
    s.g('deliver', 'deliver', '가져다주다, 전하다', star=W['deliver'])
    s.g('longer', 'longer', '더 오래 (long의 비교급)')
    s.g('lasting', 'lasting', '지속되는')
    s.g('happiness', 'happiness', '행복')
    s.g('than', 'than', '~보다')
    s.g('things', 'things', '물건들')
    s.hint('[that experiences deliver]', '[경험들이 가져다준다는 것을]',
           span='that experiences deliver', label='명사절 접속사 that',
           links=[(['that'], ['이', '다는 것을'])],
           meaning='경험들이 (더 오래 지속되는 행복을) 가져다준다는 것을',
           explanation='have found의 목적어 that절. S′ experiences, V′ deliver까지 표시하고 목적어 longer lasting happiness 이하는 제외.')
    s.review = ('등위 주어 Gilovich and other researchers(전체 유지) + 능동 완료 have found + 목적어 that 명사절(S′ experiences, V′ deliver). '
                'longer lasting happiness than things는 비교급. 힌트 1개(명사절 that). have p.p.는 힌트가 있는 문장이라 분석 보충 u2-gp4로 연결. 수동 없음.')
    out.append(s)

    # ---------------- s14 ----------------
    s = S('s14', T['s14'])
    s.ch('That’s because experiences become a part', '그것은 경험들이 일부가 되기 때문이다')
    s.ch('of our identity.', '우리의 정체성의.')
    s.natural('그것은 경험이 우리 정체성의 일부가 되기 때문이다.')
    s.cl('main', 'That’s', subj='That', verbs=[])
    contraction(s, s.clauses[-1], 'That’s', 'is')
    s.cl('subordinate', 'because', subj='experiences', verbs=['become'], marker='because')
    s.g('That’s|because', 'That’s because S′ V′', '그것은 S′(이/가) V′하기 때문이다',
        referent_ko='경험이 물건보다 더 오래 지속되는 행복을 가져다주는 것')
    s.g('experiences', 'experiences', '경험들')
    s.g('become', 'become', '~이 되다')
    s.g('part', 'part', '일부, 부분')
    s.g('of', 'of', '~의')
    s.g('our', 'our', '우리의', referent_ko='사람들')
    s.g('identity', 'identity', '정체성, 나다움', star=W['identity'])
    s.brk('of', 'postnominal-preposition', 'of our identity는 앞 명사 a part를 뒤에서 꾸미는 전치사구')
    s.hint('[That’s because experiences become a part]', '[그것[경험이 더 오래가는 행복을 주는 것]은 경험들이 일부가 되기 때문이다]',
           span='That’s because experiences become a part', label='이유 접속사 because',
           links=[(['because'], [('이', 1), '기 때문이다'])],
           refs=[('That', '그것', '[경험이 더 오래가는 행복을 주는 것]')],
           meaning='그것은 경험들이 (우리 정체성의) 일부가 되기 때문이다',
           explanation='That’s because S′ V′: 그것은 S′가 V′하기 때문이다. That은 앞 문장 내용. S′ experiences, V′ become과 뜻을 잡는 최소 보어 a part까지 표시하고 of our identity는 제외(연결동사 become은 seem과 같은 최소 보어 기준).')
    s.review = ('주절 That’s(= That is) + 이유 부사절 because(S′ experiences, V′ become). That은 13번 문장의 연구 결과를 가리킴. '
                'of our identity 앞 후치수식 경계. 힌트 1개(because). 관계사·수동 없음.')
    out.append(s)

    # ---------------- s15 ----------------
    s = S('s15', T['s15'], key=True)
    s.ch('We are not our possessions,', '우리는 우리의 소유물들이 아니다,')
    s.ch('but we are the accumulation', '하지만 우리는 축적이다')
    s.ch('of everything', '모든 것의')
    s.ch('we’ve seen,', '우리가 본,')
    s.ch('the things', '일들의')
    s.ch('we’ve done,', '우리가 한,')
    s.ch('and the places', '그리고 장소들의')
    s.ch('we’ve been to.', '우리가 가 본.')
    s.natural('우리는 우리가 가진 물건이 아니라, 우리가 본 모든 것, 우리가 한 일들, 우리가 가 본 장소들이 쌓인 존재이다.')
    t = s.text
    i1, i2, i3 = t.index('we’ve seen'), t.index('we’ve done'), t.index('we’ve been')
    s.cl('main', 'We', subj='We', verbs=['are'])
    s.cl('main', 'we', subj='we', verbs=['are'], marker='but')
    for n, (idx, pv) in enumerate([(i1, 'seen'), (i2, 'done'), (i3, 'been')]):
        s.cl('subordinate', 'we', subj='we', verbs=[pv], marker='that', omitted=True, occ=n + 1)
        ve(s, s.clauses[-1], idx)
    s.g('We', 'we', '우리는', referent_ko='사람들')
    s.g('are|not', 'are not', '~이 아니다')
    s.g('our', 'our', '우리의', referent_ko='사람들')
    s.g('possessions', 'possessions', '소유물들, 가진 물건들')
    s.g('we', 'we', '우리는', referent_ko='사람들', at=t.index('we are'))
    s.g('are', 'are', '~이다', at=t.index('are the'))
    s.g('accumulation', 'accumulation', '축적, 쌓인 것', star=W['accumulation'])
    s.g('of', 'of', '~의')
    s.g('everything', 'everything', '모든 것')
    f1 = s.g('we’ve', 'have p.p.', '~했다 (we’ve = we have, we = 우리가)', kind='function', combines_with=[], at=i1)
    l1 = s.g('seen', 'see', '보다 (seen은 see의 p.p.형)', verb_form=pp('perfect-participle', s, 'seen', 'see', f1['id']))
    link(f1, l1)
    s.g('things', 'things', '일들, 것들')
    f2 = s.g('we’ve', 'have p.p.', '~했다 (we’ve = we have, we = 우리가)', kind='function', combines_with=[], at=i2)
    l2 = s.g('done', 'do', '하다 (done은 do의 p.p.형)', verb_form=pp('perfect-participle', s, 'done', 'do', f2['id']))
    link(f2, l2)
    s.g('places', 'places', '장소들')
    f3 = s.g('we’ve', 'have p.p.', '~한 적이 있다 (we’ve = we have, we = 우리가)', kind='function', combines_with=[], at=i3)
    l3 = s.g('been', 'be', '가 있다 (been은 be의 p.p.형)', verb_form=pp('perfect-participle', s, 'been', 'be', f3['id']))
    link(f3, l3)
    s.g('to', 'to', '~에')
    s.hint('everything [(that) we’ve seen]', '[우리[사람들]가 본] 모든 것',
           span='everything we’ve seen', label='목적격 관계대명사 that 생략', display_mode='omitted-relative',
           omitted_relative='that', links=[(['that'], ['가', '본'])], refs=[('we', '우리', '[사람들]')],
           meaning='우리가 본 모든 것',
           explanation='선행사 everything 뒤 목적격 관계대명사 that이 생략된 관계절(seen의 목적어 자리). the things we’ve done도 같은 구조로 병렬.')
    s.hint('the places [(that) we’ve been to]', '[우리[사람들]가 가 본] 장소들',
           span='the places we’ve been to', label='목적격 관계대명사 that 생략', display_mode='omitted-relative',
           omitted_relative='that', links=[(['that'], ['가', '본'])], refs=[('we', '우리', '[사람들]')],
           meaning='우리가 가 본 장소들',
           explanation='선행사 the places 뒤 목적격 관계대명사 that이 생략된 관계절. the places는 전치사 to의 목적어 자리라, 빈자리가 있는 to까지 표시(사용자 확정 기준).')
    s.review = ('두 절이 but으로 연결(We are not our possessions / we are the accumulation of …). of의 목적어 세 개(everything, the things, the places)가 각각 목적격 관계대명사가 생략된 관계절 '
                'we’ve seen / we’ve done / we’ve been to의 꾸밈을 받음(’ve = have, 능동 완료). have been to는 ‘~에 가 본 적이 있다’. '
                '힌트 2개(생략 관계사 everything we’ve seen, the places we’ve been to). 생략 관계절이 셋이라 문장당 최대 2개 한도와 충돌 — the things we’ve done은 첫 힌트 설명에서 병렬로 안내하고 사용자 보고(2단계 L 검수 FLb-03). not A, but B는 u2-gp2로 지원. have p.p. 세 곳은 분석 보충 u2-gp4로 연결. 수동 없음.')
    out.append(s)

    # ---------------- s16 ----------------
    s = S('s16', T['s16'])
    s.ch('“Our experiences are a bigger part', '“우리의 경험들은 더 큰 부분이다')
    s.ch('of ourselves', '우리 자신의')
    s.ch('than our material goods,”', '우리의 물질적인 재화들보다,”')
    s.ch('says Gilovich.', '길로비치는 말한다.')
    s.natural('“우리의 경험은 물질적인 재화보다 우리 자신의 더 큰 부분이다.”라고 길로비치는 말한다.')
    s.cl('main', 'Our', subj='Our experiences', verbs=['are'])
    s.cl('main', 'says', subj='Gilovich', verbs=[], vfirst=['says'])
    s.g('Our', 'our', '우리의', referent_ko='사람들')
    s.g('experiences', 'experiences', '경험들')
    s.g('are', 'are', '~이다')
    s.g('bigger', 'bigger', '더 큰 (big의 비교급)')
    s.g('part', 'part', '부분, 일부')
    s.g('of', 'of', '~의')
    s.g('ourselves', 'ourselves', '우리 자신', referent_ko='사람들')
    s.g('than', 'than', '~보다')
    s.g('our', 'our', '우리의', referent_ko='사람들', at=s.text.index('our material'))
    s.g('material', 'material', '물질적인')
    s.g('goods', 'goods', '재화들, 물건들')
    s.g('says', 'say', '말하다', verb_form=v3(s, 'says', 'say', 'Gilovich'))
    s.brk('of', 'postnominal-preposition', 'of ourselves는 앞 명사 a bigger part를 뒤에서 꾸미는 전치사구')
    s.hint('[says Gilovich]', '[길로비치는 말한다]', span='says Gilovich', label='인용 뒤 동사·주어 도치',
           links=[(['says'], ['말한다'])], meaning='길로비치는 말한다',
           explanation='직접 인용 뒤에서 동사 says가 주어 Gilovich 앞에 온 도치. 앞으로 나간 요소 says ↔ 말한다를 강조(s49 보어 도치 선례와 같은 기준). 해석은 ‘길로비치는 말한다’.')
    s.review = ('인용된 절 Our experiences are a bigger part of ourselves than our material goods(비교급 bigger … than) + 인용 뒤 도치 says Gilovich. '
                'Gilovich는 1번 문장에서 제공한 고유명사 반복. 힌트 1개(도치). 관계사·수동 없음.')
    out.append(s)

    # ---------------- s17 ----------------
    s = S('s17', T['s17'])
    s.ch('“You can really like your material stuff.', '“여러분은 여러분의 물질적인 물건들을 정말 좋아할 수 있다.')
    s.natural('“여러분은 물질적인 물건을 정말 좋아할 수 있다.')
    s.cl('main', 'You', subj='You', verbs=['can', 'like'])
    f = s.g('can', 'can V', '~할 수 있다', kind='function', combines_with=[])
    s.g('really', 'really', '정말')
    lk = s.g('like', 'like', '좋아하다')
    link(f, lk)
    s.g('your', 'your', '여러분의', referent_ko='사람들')
    s.g('material', 'material', '물질적인')
    s.g('stuff', 'stuff', '물건, 것', star=W['stuff'])
    s.review = '단일 절 You can really like your material stuff(인용 계속). 연결·관계사·수동 없음 → 힌트 없음.'
    out.append(s)

    # ---------------- s18 ----------------
    s = S('s18', T['s18'])
    s.ch('You can even think', '여러분은 심지어 생각할 수도 있다')
    s.ch('that part', '일부가')
    s.ch('of your identity', '여러분의 정체성의')
    s.ch('is connected to those things,', '그 물건들에 연결되어 있다고,')
    s.ch('but nonetheless they remain separate from you.', '하지만 그럼에도 불구하고 그것들은 여러분으로부터 분리된 채로 남아 있다.')
    s.natural('여러분은 심지어 자신의 정체성 일부가 그 물건들과 연결되어 있다고 생각할 수도 있지만, 그럼에도 그것들은 여러분과 분리된 채로 남아 있다.')
    s.cl('main', 'You', subj='You', verbs=['can', 'think'])
    s.cl('subordinate', 'that', subj='part of your identity', verbs=['is', 'connected'], marker='that', disp='part',
         disp_review='중심명사 part까지 표시하고 뒤에서 꾸미는 of your identity는 제외')
    s.cl('main', 'they', subj='they', verbs=['remain'], marker='but')
    f = s.g('can', 'can V', '~할 수 있다', kind='function', combines_with=[])
    s.g('even', 'even', '심지어')
    tk = s.g('think', 'think', '생각하다')
    link(f, tk)
    s.g('that', 'that S′ V′', 'S′(이/가) V′라고')
    s.g('part', 'part', '일부')
    s.g('of', 'of', '~의')
    s.g('your', 'your', '여러분의', referent_ko='사람들')
    s.g('identity', 'identity', '정체성, 나다움', star=W['identity'])
    fb = s.g('is', 'be p.p.', '~되다', kind='function', combines_with=[])
    cn = s.g('connected', 'connected', '연결된', verb_form=pp('passive-participle', s, 'connected', 'connect', fb['id']))
    link(fb, cn)
    s.g('to', 'to', '~에')
    s.g('those', 'those', '그')
    s.g('things', 'things', '물건들')
    s.g('nonetheless', 'nonetheless', '그럼에도 불구하고', star=W['nonetheless'])
    s.g('they', 'they', '그것들은', referent_ko='물질적인 물건들')
    s.g('remain', 'remain', '(여전히) ~인 채로 남아 있다', star=W['remain'])
    s.g('separate', 'separate', '분리된, 별개의')
    s.g('from', 'from', '~로부터')
    s.brk('of', 'postnominal-preposition', 'of your identity는 앞 명사 part를 뒤에서 꾸미는 전치사구')
    s.hint('[that part of your identity is connected]', '[여러분[사람들]의 정체성의 일부가 연결되어 있다고]',
           span='that part of your identity is connected', label='명사절 접속사 that',
           links=[(['that'], ['가', '다고'])], refs=[('your', '여러분', '[사람들]')],
           meaning='여러분의 정체성의 일부가 (그 물건들에) 연결되어 있다고',
           explanation='think의 목적어 that절. S′ part of your identity, V′ is connected까지 표시하고 to those things는 제외.')
    s.review = ('주절 You can even think + 목적어 that 명사절(S′ part of your identity, V′ is connected — 수동) + but nonetheless 뒤 둘째 절 they remain separate from you(remain + 형용사 보어). '
                '힌트 1개(명사절 that). 수동 is connected는 힌트가 있는 문장이라 분석 보충 u2-gp5로 연결.')
    out.append(s)

    # ---------------- s19 ----------------
    s = S('s19', T['s19'])
    s.ch('On the other hand,', '반면에,')
    s.ch('your experiences really are part', '여러분의 경험들은 정말로 일부이다')
    s.ch('of you.', '여러분의.')
    s.natural('반면에 여러분의 경험은 정말로 여러분의 일부이다.')
    s.cl('main', 'your', subj='your experiences', verbs=['are'])
    s.g('On|the|other|hand', 'on the other hand', '반면에, 다른 한편으로', star=W['other_hand'])
    s.g('your', 'your', '여러분의', referent_ko='사람들')
    s.g('experiences', 'experiences', '경험들')
    s.g('really', 'really', '정말로')
    s.g('are', 'are', '~이다')
    s.g('part', 'part', '일부')
    s.g('of', 'of', '~의')
    s.brk('of', 'postnominal-preposition', 'of you는 앞 명사 part를 뒤에서 꾸미는 전치사구')
    s.review = '단일 절 your experiences really are part of you(18번의 물건과 대조). 연결·관계사·수동 없음 → 힌트 없음.'
    out.append(s)

    # ---------------- s20 ----------------
    s = S('s20', T['s20'])
    s.ch('We are the sum total', '우리는 총합이다')
    s.ch('of our experiences.”', '우리의 경험들의.”')
    s.natural('우리는 우리 경험의 총합이다.”')
    s.cl('main', 'We', subj='We', verbs=['are'])
    s.g('We', 'we', '우리는', referent_ko='사람들')
    s.g('are', 'are', '~이다')
    s.g('sum total', 'sum total', '총합, 전부', star=W['sum_total'])
    s.g('of', 'of', '~의')
    s.g('our', 'our', '우리의', referent_ko='사람들')
    s.g('experiences', 'experiences', '경험들')
    s.brk('of', 'postnominal-preposition', 'of our experiences는 앞 명사 the sum total을 뒤에서 꾸미는 전치사구')
    s.review = '단일 절 We are the sum total of our experiences(인용 끝). 연결·관계사·수동 없음 → 힌트 없음.'
    out.append(s)
    return out


UNIT = {
    'id': 'u2', 'source_id': 'src', 'paragraph_ids': ['p03', 'p04'],
    'sentence_ids': [f's{n:02d}' for n in range(13, 21)],
    'today_words': [
        {'id': W['deliver'], 'text': 'deliver', 'meaning_ko': '가져다주다, 전하다'},
        {'id': W['identity'], 'text': 'identity', 'meaning_ko': '정체성, 나다움'},
        {'id': W['accumulation'], 'text': 'accumulation', 'meaning_ko': '축적, 쌓인 것'},
        {'id': W['stuff'], 'text': 'stuff', 'meaning_ko': '물건, 것'},
        {'id': W['nonetheless'], 'text': 'nonetheless', 'meaning_ko': '그럼에도 불구하고'},
        {'id': W['remain'], 'text': 'remain', 'meaning_ko': '(여전히) ~인 채로 남아 있다'},
        {'id': W['other_hand'], 'text': 'on the other hand', 'meaning_ko': '반면에, 다른 한편으로'},
        {'id': W['sum_total'], 'text': 'sum total', 'meaning_ko': '총합, 전부'},
    ],
}


def analysis(_):
    return {
        'heading_kind': '제목',
        'title_or_topic_en': 'Why Experiences Bring Longer Lasting Happiness',
        'title_or_topic_ko': '경험이 더 오래가는 행복을 주는 이유',
        'intent_ko': '경험이 물건보다 더 오래가는 행복을 주는 이유를 경험이 우리 정체성의 일부가 된다는 점으로 설명하고, 길로비치의 말을 인용해 우리는 경험의 총합이라고 강조하는 글이다.',
        'flow': [
            {'sentence_ids': ['s13', 's14', 's15'], 'label': '경험이 오래가는 이유',
             'text_ko': '길로비치와 다른 연구자들은 경험이 물건보다 더 오래 지속되는 행복을 가져다준다는 것을 발견했다. 경험은 우리 정체성의 일부가 되기 때문이다. 우리는 가진 물건이 아니라 보고, 하고, 가 본 모든 것이 쌓인 존재다.'},
            {'sentence_ids': ['s16', 's17', 's18', 's19', 's20'], 'label': '길로비치의 말',
             'text_ko': '길로비치는 경험이 물질적인 재화보다 우리 자신의 더 큰 부분이라고 말한다. 물건을 좋아하고 그것이 정체성과 연결되어 있다고 생각할 수는 있어도 물건은 여전히 우리와 분리되어 있다. 반면 경험은 정말로 우리의 일부이며, 우리는 경험의 총합이다.'},
        ],
        'easy_explanations': [
            {'sentence_id': 's14', 'explanatory_sentences': [
                '14번 문장은 13번에서 말한 연구 결과의 이유를 설명한다.',
                'That은 경험이 물건보다 더 오래가는 행복을 준다는 13번의 내용을 가리킨다.',
                '우리가 한 경험은 우리가 어떤 사람인지를 이루는 한 부분이 된다.',
                '글쓴이는 이것이 경험의 행복이 더 오래가는 이유라고 말한다.']},
            {'sentence_id': 's16', 'explanatory_sentences': [
                '16번 문장부터는 길로비치 교수가 직접 한 말을 옮긴다.',
                '그는 경험이 물질적인 물건보다 우리 자신에서 더 큰 부분을 차지한다고 말한다.',
                '문장 끝의 says Gilovich는 이 말을 한 사람이 길로비치라는 것을 알려 준다.']},
            {'sentence_id': 's18', 'explanatory_sentences': [
                '17번에서 길로비치는 우리가 물건을 정말 좋아할 수 있다고 먼저 인정한다.',
                '18번은 한 걸음 더 나아간다.',
                '우리는 내 정체성의 일부가 어떤 물건과 이어져 있다고 생각할 수도 있다.',
                '그래도 그 물건은 여전히 나와 떨어져 있는 따로 된 것이다.',
                '19번 문장은 이와 달리 경험은 정말로 나의 일부라고 말한다.']},
        ],
        'grammar_points': [
            {'id': 'u2-gp1', 'sentence_id': 's14', 'span': 'That’s because experiences become a part of our identity',
             'title': 'That’s because S′ V′: 그것은 S′가 V′하기 때문이다', 'formula_key': 'That’s because S′ V′',
             'explanation': '공식: That’s because S′ V′ — 그것은 S′(이/가) V′하기 때문이다. That = 앞 문장 내용(경험이 물건보다 더 오래 지속되는 행복을 가져다주는 것), '
                            'S′ = experiences(경험들), V′ = become(~이 되다), 보어 = a part of our identity(우리 정체성의 일부). '
                            '→ 그것은 경험들이 우리 정체성의 일부가 되기 때문이다. That’s because 뒤에는 앞 내용의 이유가 온다.',
             'practice': {'span': 'That’s because experiences become a part of our identity',
                          'formula_support': {'en': 'That’s because S′ V′', 'ko': '그것은 S′(이/가) V′하기 때문이다'},
                          'support': [('s14', 'experiences'), ('s14', 'become'), ('s14', 'part'), ('s14', 'of'),
                                      ('s14', 'our'), ('s14', 'identity')],
                          'answer_ko': '그것은 경험들이 우리 정체성의 일부가 되기 때문이다'}},
            {'id': 'u2-gp2', 'sentence_id': 's15', 'span': 'We are not our possessions, but we are the accumulation of everything we’ve seen',
             'title': 'not A, but B: A가 아니라 B', 'formula_key': 'not A, but B',
             'explanation': '공식: S are not A, but S are B — S는 A가 아니라 B이다. S = we(우리), A = our possessions(우리의 소유물들), '
                            'B = the accumulation of everything we’ve seen(우리가 본 모든 것의 축적). '
                            '→ 우리는 우리의 소유물들이 아니라, 우리가 본 모든 것의 축적이다. not과 but이 짝을 이루어 A를 부정하고 B를 강조한다. 원문의 B는 뒤의 the things we’ve done(우리가 한 일들), the places we’ve been to(우리가 가 본 장소들)까지 이어진다.',
             'practice': {'span': 'We are not our possessions, but we are the accumulation of everything we’ve seen',
                          'formula_support': {'en': 'not A, but B', 'ko': 'A가 아니라 B'},
                          'support': [('s15', 'our'), ('s15', 'possessions'), ('s15', 'accumulation'), ('s15', 'of'),
                                      ('s15', 'everything'), ('s15', 'have p.p.'), ('s15', 'see')],
                          'answer_ko': '우리는 우리의 소유물들이 아니라, 우리가 본 모든 것의 축적이다'}},
            {'id': 'u2-gp3', 'sentence_id': 's18', 'span': 'You can even think that part of your identity is connected to those things',
             'title': 'think that S′ V′: S′가 V′라고 생각하다', 'formula_key': 'think that S′ V′',
             'explanation': '공식: think that S′ V′ — S′(이/가) V′라고 생각하다. can = ~할 수 있다, even = 심지어, that = 명사절 접속사(~라고), '
                            'S′ = part of your identity(여러분 정체성의 일부), V′ = is connected(연결되어 있다), to those things = 그 물건들에. '
                            '→ 여러분은 심지어 여러분 정체성의 일부가 그 물건들에 연결되어 있다고 생각할 수도 있다.',
             'practice': {'span': 'think that part of your identity is connected to those things',
                          'formula_support': {'en': 'think that S′ V′', 'ko': 'S′(이/가) V′라고 생각하다'},
                          'support': [('s18', 'think'), ('s18', 'part'), ('s18', 'of'), ('s18', 'your'), ('s18', 'identity'),
                                      ('s18', 'be p.p.'), ('s18', 'connected'), ('s18', 'to'), ('s18', 'those'), ('s18', 'things')],
                          'answer_ko': '여러분 정체성의 일부가 그 물건들에 연결되어 있다고 생각하다'}},
            {'id': 'u2-gp4', 'sentence_id': 's13', 'span': 'Gilovich and other researchers have found',
             'title': 'have p.p.: ~했다 (have found: 발견했다)', 'formula_key': 'have p.p.',
             'explanation': '공식: have p.p. — ~했다. p.p. = found(find의 p.p.형, find = 발견하다), 주어 = Gilovich and other researchers(길로비치와 다른 연구자들). '
                            '→ 길로비치와 다른 연구자들은 발견했다. 무엇을 발견했는지는 뒤의 that절이 알려 준다. 15번의 we’ve seen·done·been(’ve = have)도 같은 have p.p.이며, have been to는 ‘~에 가 본 적이 있다’(경험)이다.',
             'supplemental': {'function': ('s13', 'have p.p.', 0),
                              'reason': 's13의 능동 완료 have found와 s15의 we’ve seen·done·been은 각각 명사절 힌트와 생략 관계사 힌트를 선정한 문장이라 결합 힌트로 두지 않았고, 기본 분석 3개에 have p.p. 설명이 없어 이 단위 대표 사례로 1회 보충'},
             'practice': {'span': 'Gilovich and other researchers have found',
                          'formula_support': {'en': 'have p.p.', 'ko': '~했다'},
                          'support': [('s13', 'other'), ('s13', 'researchers'), ('s13', 'find')],
                          'answer_ko': '길로비치와 다른 연구자들은 발견했다'}},
            {'id': 'u2-gp5', 'sentence_id': 's18', 'span': 'part of your identity is connected to those things',
             'title': 'be p.p.: ~되다 (is connected: 연결되어 있다)', 'formula_key': 'be p.p.',
             'explanation': '공식: be p.p. — ~되다. p.p. = connected(연결된, connect의 p.p.형), 주어 = part of your identity(여러분 정체성의 일부), to those things = 그 물건들에. '
                            '→ 여러분 정체성의 일부가 그 물건들에 연결되어 있다. 정체성의 일부는 스스로 연결하는 것이 아니라 ‘연결되는’ 쪽이라 수동을 쓴다.',
             'supplemental': {'function': ('s18', 'be p.p.', 0),
                              'reason': 's18의 수동 is connected는 명사절 that 힌트 표시 범위 안이라 결합 힌트로 두지 않았고, 기본 분석 3개에 be p.p. 설명이 없어 이 단위 대표 사례로 1회 보충'},
             'practice': {'span': 'part of your identity is connected to those things',
                          'formula_support': {'en': 'be p.p.', 'ko': '~되다'},
                          'support': [('s18', 'part'), ('s18', 'of'), ('s18', 'your'), ('s18', 'identity'), ('s18', 'connected'),
                                      ('s18', 'to'), ('s18', 'those'), ('s18', 'things')],
                          'answer_ko': '여러분 정체성의 일부가 그 물건들에 연결되어 있다'}},
        ],
        'formula_routes': [
            {'function': ('s13', 'have p.p.', 0), 'route': 'analysis', 'grammar_point_id': 'u2-gp4',
             'review_record': 'have found: 명사절 that 힌트가 있는 문장이라 분석 보충 u2-gp4로 연결'},
            {'function': ('s15', 'have p.p.', 0), 'route': 'analysis', 'grammar_point_id': 'u2-gp4',
             'review_record': 'we’ve seen: 생략 관계사 힌트가 있는 문장이라 분석 보충 u2-gp4로 연결'},
            {'function': ('s15', 'have p.p.', 1), 'route': 'analysis', 'grammar_point_id': 'u2-gp4',
             'review_record': 'we’ve done: 같은 이유로 u2-gp4로 연결'},
            {'function': ('s15', 'have p.p.', 2), 'route': 'analysis', 'grammar_point_id': 'u2-gp4',
             'review_record': 'we’ve been to: 같은 이유로 u2-gp4로 연결'},
            {'function': ('s18', 'be p.p.', 0), 'route': 'analysis', 'grammar_point_id': 'u2-gp5',
             'review_record': 'is connected: 명사절 that 힌트 표시 범위 안이라 분석 보충 u2-gp5로 연결'},
        ],
        'relations': [
            {'head': {'id': 'u2-r1h', 'text': 'lasting', 'meaning_ko': '지속되는, 오래가는'},
             'synonym': {'id': 'u2-r1s', 'text': 'enduring', 'meaning_ko': '오래가는, 지속적인'},
             'antonym': {'id': 'u2-r1a', 'text': 'temporary', 'meaning_ko': '일시적인'}},
            {'head': {'id': 'u2-r2h', 'text': 'material', 'meaning_ko': '물질적인'},
             'synonym': {'id': 'u2-r2s', 'text': 'physical', 'meaning_ko': '물리적인, 물질의'},
             'antonym': {'id': 'u2-r2a', 'text': 'spiritual', 'meaning_ko': '정신적인'}},
            {'head': {'id': 'u2-r3h', 'text': 'separate', 'meaning_ko': '분리된, 별개의'},
             'synonym': {'id': 'u2-r3s', 'text': 'distinct', 'meaning_ko': '별개의, 뚜렷이 다른'},
             'antonym': {'id': 'u2-r3a', 'text': 'united', 'meaning_ko': '결합된, 하나가 된'}},
        ],
    }


def workbook():
    return {
        'relation_order': ['u2-r3s', 'u2-r1a', 'u2-r2h', 'u2-r3a', 'u2-r1h', 'u2-r2s', 'u2-r3h', 'u2-r2a', 'u2-r1s'],
        'key_sentence_ids': ['s13', 's15'],
        'question_id': 'Q02',
        'syntax_point_ids': ['u2-gp1', 'u2-gp2', 'u2-gp3', 'u2-gp4', 'u2-gp5'],
    }
