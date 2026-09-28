"""공통 단위 1: 제목 아래 무소제목 도입 단락 p01~p02(s01~s10).

사용자 결정(2026-09-28 “한 단위 10문장 (추천)”): 지나의 가짜 뉴스 경험 두 단락을 한 공통 단위로 묶음.
"""
from author import S, link

W = {'astonished': 'u1-w1', 'headline': 'u1-w2', 'undamaged': 'u1-w3', 'embarrassed': 'u1-w4',
     'incident': 'u1-w5', 'turn_out': 'u1-w6', 'creators': 'u1-w7', 'provocative': 'u1-w8'}


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
    s.ch('While scrolling through her social media', '그녀의 소셜 미디어를 스크롤하던 중에')
    s.ch('one day,', '어느 날,')
    s.ch('Gina was astonished', '지나는 깜짝 놀랐다')
    s.ch('when she saw the news headline,', '그녀가 뉴스 헤드라인을 보았을 때,')
    s.ch('“The Heundeulbawi', '“흔들바위가')
    s.ch('in Seoraksan National Park', '설악산 국립공원에 있는')
    s.ch('Has Fallen.”', '떨어졌다.”')
    s.natural('어느 날 소셜 미디어를 스크롤하던 중, 지나는 “설악산 국립공원의 흔들바위가 떨어졌다”라는 뉴스 헤드라인을 보고 깜짝 놀랐다.')
    s.cl('main', 'Gina', subj='Gina', verbs=['was'])
    s.cl('subordinate', 'when', subj='she', verbs=['saw'], marker='when')
    s.cl('main', 'The', subj='The Heundeulbawi in Seoraksan National Park', verbs=['Has', 'Fallen'],
         disp='The Heundeulbawi', disp_review='중심명사 Heundeulbawi까지 표시하고 뒤수식 in Seoraksan National Park는 제외')
    s.g('While', 'while V-ing', '~하던 중에', kind='function', combines_with=[])
    f0 = s.glosses[-1]
    sc = s.g('scrolling|through', 'scroll through', '~을 스크롤하며 훑어보다', verb_form=pp('ing', s, 'scrolling', 'scroll'))
    link(f0, sc)
    s.g('her', 'her', '그녀의', referent_ko='지나')
    s.g('social|media', 'social media', '소셜 미디어 (SNS)')
    s.g('one|day', 'one day', '어느 날')
    s.g('Gina', 'Gina', '지나 (사람 이름)', proper=True)
    s.g('was', 'was', '~였다')
    s.g('astonished', 'astonished', '깜짝 놀란', star=W['astonished'], verb_form=pp('past-participle', s, 'astonished', 'astonish'))
    s.g('when', 'when S′ V′', 'S′(이/가) V′했을 때')
    s.g('she', 'she', '그녀가', referent_ko='지나')
    s.g('saw', 'saw', '보았다 (see의 과거)', verb_form=pp('irregular-past', s, 'saw', 'see'))
    s.g('news|headline', 'news headline', '뉴스 헤드라인, 뉴스 제목', star=W['headline'])
    s.g('Heundeulbawi', 'Heundeulbawi', '흔들바위 (설악산 국립공원의 큰 바위)', proper=True)
    s.g('in', 'in', '~에 있는')
    s.g('Seoraksan|National|Park', 'Seoraksan National Park', '설악산 국립공원', proper=True)
    f = s.g('Has', 'have p.p.', '~했다', kind='function', combines_with=[])
    fl = s.g('Fallen', 'fall', '떨어지다, 무너지다 (Fallen은 fall의 p.p.형)',
             verb_form=pp('perfect-participle', s, 'Fallen', 'fall', f['id']))
    link(f, fl)
    s.brk('in', 'postnominal-preposition', 'in Seoraksan National Park는 앞 명사 The Heundeulbawi를 뒤에서 꾸미는 전치사구',
          after=s.text.index('Heundeulbawi'))
    s.hint('[While scrolling]', '[스크롤하던 중에]', span='While scrolling', label='접속사 while + V-ing',
           links=[(['While', 'ing'], ['던 중에'])], meaning='(소셜 미디어를) 스크롤하던 중에',
           explanation='접속사 while 뒤에 주어·be동사가 생략되고 V-ing가 이어진 형태(While she was scrolling). ~하던 중에(동시). 대상 through her social media는 표시에서 제외.')
    s.hint('[when she saw]', '[그녀[지나]가 보았을 때]', span='when she saw', label='시간 접속사 when',
           links=[(['when'], ['가', '을 때'])], refs=[('she', '그녀', '[지나]')],
           meaning='그녀가 (뉴스 헤드라인을) 보았을 때',
           explanation='when이 이끄는 시간 부사절(S′ she, V′ saw). 목적어 the news headline 이하는 표시에서 제외.')
    s.review = ('주절 Gina was astonished(보어 astonished는 독립 과거분사, 감정 형용사) + 시간 부사절 when she saw … + 헤드라인 직접 인용절 '
                'The Heundeulbawi … Has Fallen(독립된 인용 문장이라 S/V로 표시, 현재완료 Has Fallen). 문두 While scrolling은 접속사 while + V-ing(주어·be 생략). '
                'in Seoraksan National Park는 후치수식 전치사구 → in 앞에서 끊음. 힌트 2개(while + V-ing, 접속사 when). '
                '현재완료 Has Fallen은 힌트 자리가 없어 분석 보충 u1-gp4로 연결. 관계사 없음.')
    out.append(s)

    # ---------------- s02 ----------------
    s = S('s02', T['s02'])
    s.ch('Gina immediately shared the shocking story', '지나는 즉시 그 충격적인 이야기를 공유했다')
    s.ch('with her close friends.', '그녀의 친한 친구들과.')
    s.natural('지나는 곧바로 그 충격적인 소식을 친한 친구들에게 공유했다.')
    s.cl('main', 'Gina', subj='Gina', verbs=['shared'])
    s.g('immediately', 'immediately', '즉시, 곧바로')
    s.g('shared', 'share', '공유하다, 함께 나누다', verb_form=pp('regular-past', s, 'shared', 'share'))
    s.g('shocking', 'shocking', '충격적인')
    s.g('story', 'story', '이야기, 소식')
    s.g('with', 'with', '~와')
    s.g('her', 'her', '그녀의', referent_ko='지나')
    s.g('close', 'close', '친한 (흔한 뜻: 가까운)')
    s.g('friends', 'friends', '친구들')
    s.review = '단일 주절 shared(일반 정규과거) + with 전치사구(대표 뜻 ~와로 분리). 관계사·접속사절·수동 없음 → 힌트 없음.'
    out.append(s)

    # ---------------- s03 ----------------
    s = S('s03', T['s03'])
    s.ch('Later,', '이후에,')
    s.ch('during the morning news', '아침 뉴스 동안')
    s.ch('on TV,', 'TV에서 하는,')
    s.ch('a reporter', '한 기자가')
    s.ch('standing next to the undamaged Heundeulbawi', '손상되지 않은 흔들바위 옆에 서 있는')
    s.ch('said,', '말했다,')
    s.ch('“Today’s Internet stories', '“오늘의 인터넷 기사들은')
    s.ch('of the Heundeulbawi being damaged', '흔들바위가 손상되는 것에 관한')
    s.ch('were fake.”', '가짜였습니다.”')
    s.natural('이후 TV 아침 뉴스에서, 멀쩡한 흔들바위 옆에 서 있던 기자가 “흔들바위가 손상되었다는 오늘 인터넷 기사들은 가짜였습니다.”라고 말했다.')
    s.cl('main', 'a', subj='a reporter standing next to the undamaged Heundeulbawi', verbs=['said'],
         disp='a reporter', disp_review='중심명사 reporter까지 표시하고 뒤수식 현재분사구 standing next to the undamaged Heundeulbawi는 제외')
    s.cl('main', 'Today’s', subj='Today’s Internet stories of the Heundeulbawi being damaged', verbs=['were'],
         disp='Today’s Internet stories', disp_review='중심명사 stories까지 표시하고 뒤수식 of the Heundeulbawi being damaged는 제외')
    s.g('Later', 'later', '이후에, 나중에')
    s.g('during', 'during', '~ 동안')
    s.g('morning', 'morning', '아침')
    s.g('news', 'news', '뉴스')
    s.g('on', 'on', '~에서 (흔한 뜻: ~위에)')
    s.g('TV', 'TV', 'TV, 텔레비전')
    s.g('reporter', 'reporter', '기자')
    fs = s.g('standing', 'V-ing', '~하고 있는', kind='function', combines_with=[])
    st = s.g('standing', 'stand', '서다', same=True, verb_form=pp('ing', s, 'standing', 'stand'))
    link(fs, st)
    s.g('next|to', 'next to', '~ 옆에')
    s.g('undamaged', 'undamaged', '손상되지 않은, 멀쩡한', star=W['undamaged'])
    s.g('said', 'said', '말했다 (say의 과거)', verb_form=pp('irregular-past', s, 'said', 'say'))
    s.g('Today’s', 'today’s', '오늘의')
    s.g('Internet', 'Internet', '인터넷')
    s.g('stories', 'stories', '기사들 (흔한 뜻: 이야기들)')
    s.g('of', 'of', '~에 관한 (흔한 뜻: ~의)')
    fb = s.g('being', 'being p.p.', '~되는 것', kind='function', combines_with=[])
    dm = s.g('damaged', 'damaged', '손상된', verb_form=pp('passive-participle', s, 'damaged', 'damage', fb['id']))
    link(fb, dm)
    s.g('were', 'were', '~였다')
    s.g('fake', 'fake', '가짜의')
    s.brk('on', 'postnominal-preposition', 'on TV는 앞 명사 the morning news를 뒤에서 꾸미는 전치사구')
    s.brk('of', 'postnominal-preposition', 'of the Heundeulbawi being damaged는 앞 명사 Internet stories를 뒤에서 꾸미는 전치사구')
    s.hint('a reporter [standing next to the undamaged Heundeulbawi]', '[손상되지 않은 흔들바위 옆에 서 있는] 한 기자',
           span='a reporter standing next to the undamaged Heundeulbawi', label='현재분사 후치수식',
           links=[(['ing'], ['있는'])], meaning='손상되지 않은 흔들바위 옆에 서 있는 한 기자',
           explanation='현재분사 standing이 이끄는 standing next to the undamaged Heundeulbawi가 앞 명사 a reporter를 뒤에서 꾸민다. ing ↔ 있는(~하고 있는).')
    s.hint('stories [of the Heundeulbawi being damaged]', '[흔들바위가 손상되는 것에 관한] 기사들',
           span='stories of the Heundeulbawi being damaged', label='전치사 of + 의미상 주어 + 동명사',
           links=[(['of'], ['에 관한']), (['being'], ['가', '되는 것'])], meaning='흔들바위가 손상되는 것에 관한 기사들',
           explanation='전치사 of의 목적어는 동명사 being damaged(수동)이고 앞의 the Heundeulbawi가 그 의미상 주어다. 흔들바위가 손상되었다는 내용의 기사.')
    s.review = ('주절 a reporter … said(주어는 현재분사 후치수식 standing … 포함, 표시는 a reporter) + 인용절 Today’s Internet stories … were fake(독립 인용 문장). '
                'on TV·of the Heundeulbawi … 후치수식 전치사구 앞에서 끊음. 힌트 2개(현재분사 후치수식, of + 의미상 주어 + 동명사 수동). '
                '동명사 수동 being damaged(being p.p.)는 힌트가 일반형이라 분석 보충 u1-gp5로 연결. 관계사 없음.')
    out.append(s)

    # ---------------- s04 ----------------
    s = S('s04', T['s04'], key=True)
    s.ch('Gina was embarrassed', '지나는 당황했다')
    s.ch('by the fact', '사실에')
    s.ch('that she had spread the fake news.', '그녀가 가짜 뉴스를 퍼뜨렸다는.')
    s.natural('지나는 자신이 가짜 뉴스를 퍼뜨렸다는 사실에 당황했다.')
    s.cl('main', 'Gina', subj='Gina', verbs=['was'])
    s.cl('subordinate', 'that', subj='she', verbs=['had', 'spread'], marker='that')
    s.g('was', 'was', '~였다')
    s.g('embarrassed', 'embarrassed', '당황한, 창피한', star=W['embarrassed'],
        verb_form=pp('past-participle', s, 'embarrassed', 'embarrass'))
    s.g('by', 'by', '~에 (흔한 뜻: ~에 의해)')
    s.g('fact', 'fact', '사실')
    rel = s.g('that', 'that S′ V′', 'S′(이/가) V′했다는 (앞 명사의 내용을 설명)')
    s.g('she', 'she', '그녀가', referent_ko='지나')
    f = s.g('had', 'had p.p.', '~했다', kind='function', combines_with=[])
    sp = s.g('spread', 'spread', '퍼뜨리다 (spread는 spread의 p.p.형)', verb_form=pp('perfect-participle', s, 'spread', 'spread', f['id']))
    link(f, sp)
    s.g('fake|news', 'fake news', '가짜 뉴스')
    s.hint('the fact [that she had spread]', '[그녀[지나]가 퍼뜨렸다는] 사실', span='the fact that she had spread',
           label='동격 접속사 that', links=[(['that'], ['가', '다는'])], refs=[('she', '그녀', '[지나]')],
           meaning='그녀가 (가짜 뉴스를) 퍼뜨렸다는 사실',
           explanation='that절이 앞 명사 the fact의 내용을 설명하는 동격절(S′ she, V′ had spread). 목적어 the fake news는 표시에서 제외. 과거완료 had spread: 당황한 시점보다 먼저 퍼뜨린 일.')
    s.review = ('주절 Gina was embarrassed(보어 embarrassed는 독립 과거분사, 감정 형용사) + by the fact(감정의 원인, 수동태 행위자 by 아님) + 동격 that절(the fact의 내용). '
                'that절 과거완료 had spread(퍼뜨린 일이 당황한 과거 시점보다 앞섬). 힌트 1개(동격 that). had p.p.는 이 문장의 기본 분석 u1-gp1에서 설명. 관계사·수동 없음.')
    out.append(s)

    # ---------------- s05 ----------------
    s = S('s05', T['s05'])
    s.ch('It reminded her of another incident', '그것은 그녀에게 또 다른 사건을 떠올리게 했다')
    s.ch('of fake news', '가짜 뉴스의')
    s.ch('that had happened a while ago.', '얼마 전에 일어났던.')
    s.natural('이 일은 지나에게 얼마 전에 있었던 또 다른 가짜 뉴스 사건을 떠올리게 했다.')
    s.cl('main', 'It', subj='It', verbs=['reminded'])
    s.cl('subject_relative', 'that', verbs=['had', 'happened'], marker='that')
    s.g('It', 'it', '그것은', referent_ko='지나가 흔들바위 가짜 뉴스를 퍼뜨린 일')
    s.g('reminded|of', 'remind A of B', 'A에게 B를 떠올리게 하다', verb_form=pp('regular-past', s, 'reminded', 'remind'),
        verb_construction={'kind': 'verb-frame', 'verb_span': s.span_of('reminded'), 'lemma': 'remind',
                           'link_spans': [s.span_of('of')],
                           'review_record': 'reminded her of another incident …: A=her, B=another incident of fake news.'})
    s.g('her', 'her', '그녀에게', referent_ko='지나')
    s.g('another', 'another', '또 다른')
    s.g('incident', 'incident', '사건', star=W['incident'])
    s.g('of', 'of', '~의', at=s.text.index('of fake'))
    s.g('fake|news', 'fake news', '가짜 뉴스')
    rel = s.g('that', 'that V′', 'V′했던 (관계대명사)')
    f = s.g('had', 'had p.p.', '~했다', kind='function', combines_with=[])
    hp = s.g('happened', 'happen', '일어나다 (happened는 happen의 p.p.형)',
             verb_form=pp('perfect-participle', s, 'happened', 'happen', f['id']))
    link(f, hp)
    s.g('a|while|ago', 'a while ago', '얼마 전에')
    s.brk('of', 'postnominal-preposition', 'of fake news는 앞 명사 another incident를 뒤에서 꾸미는 전치사구', after=s.text.index('incident'))
    s.prot('reminded her of', 'fixed-expression', 'remind A of B(A에게 B를 떠올리게 하다)의 A와 of를 가르지 않음')
    s.hint('another incident of fake news [that had happened]', '[일어났던] 또 다른 가짜 뉴스 사건',
           span='another incident of fake news that had happened', label='주격 관계대명사 that',
           links=[(['that'], ['던'])], meaning='(얼마 전에) 일어났던 또 다른 가짜 뉴스 사건',
           explanation='선행사 another incident (of fake news)를 주격 관계대명사 that이 받아 had happened a while ago가 꾸민다. 주격이라 V′ had happened까지만 표시. 과거완료의 관형 연결 ‘일어났던’.')
    s.relative_ids = [rel['id']]
    s.review = ('단일 주절 remind A of B(A=her, B=another incident of fake news) + 주격 관계절 that had happened a while ago(선행사 another incident of fake news). '
                'It은 앞 문장까지의 상황(지나가 가짜 뉴스를 퍼뜨린 일). of fake news 앞 후치수식 경계, reminded her of는 가르지 않음. '
                '힌트 1개(필수 관계사). had happened는 기본 분석 u1-gp1(had p.p.)에 연결. 수동 없음.')
    out.append(s)

    # ---------------- s06 ----------------
    s = S('s06', T['s06'])
    s.ch('The news', '뉴스가')
    s.ch('that a famous athlete had died', '한 유명한 운동선수가 죽었다는')
    s.ch('became the number one issue online,', '온라인에서 가장 큰 이슈가 되었다,')
    s.ch('but it turned out to be fake.', '하지만 그것은 가짜인 것으로 드러났다.')
    s.natural('한 유명한 운동선수가 사망했다는 뉴스가 온라인에서 가장 큰 이슈가 되었지만, 그것은 가짜로 밝혀졌다.')
    s.cl('main', 'The', subj='The news that a famous athlete had died', verbs=['became'], disp='The news',
         disp_review='중심명사 news까지 표시하고 동격 that절 that a famous athlete had died는 제외(그 절의 S′·V′는 따로 표시)')
    s.cl('subordinate', 'that', subj='a famous athlete', verbs=['had', 'died'], marker='that')
    s.cl('main', 'it', subj='it', verbs=['turned', 'out'], marker='but')
    s.g('news', 'news', '뉴스')
    s.g('that', 'that S′ V′', 'S′(이/가) V′했다는 (앞 명사의 내용을 설명)')
    s.g('famous', 'famous', '유명한')
    s.g('athlete', 'athlete', '운동선수')
    f = s.g('had', 'had p.p.', '~했다', kind='function', combines_with=[])
    dd = s.g('died', 'die', '죽다, 사망하다 (died는 die의 p.p.형)', verb_form=pp('perfect-participle', s, 'died', 'die', f['id']))
    link(f, dd)
    s.g('became', 'became', '~이 되었다 (become의 과거)', verb_form=pp('irregular-past', s, 'became', 'become'))
    s.g('number|one', 'number one', '1위의, 가장 큰')
    s.g('issue', 'issue', '이슈, 화제')
    s.g('online', 'online', '온라인에서')
    s.g('it', 'it', '그것은', referent_ko='유명한 운동선수가 사망했다는 뉴스')
    s.g('turned|out|to', 'turn out to V', '~인 것으로 드러나다, 밝혀지다', star=W['turn_out'],
        verb_form=pp('regular-past', s, 'turned', 'turn'),
        verb_construction={'kind': 'verb-frame', 'verb_span': s.span_of('turned'), 'lemma': 'turn',
                           'link_spans': [s.span_of('out'), s.span_of('to')],
                           'review_record': 'turned out to be fake: turn out to V(~인 것으로 드러나다), V=be.'})
    s.g('be', 'be', '~이다')
    s.g('fake', 'fake', '가짜의')
    s.hint('The news [that a famous athlete had died]', '[한 유명한 운동선수가 죽었다는] 뉴스',
           span='The news that a famous athlete had died', label='동격 접속사 that',
           links=[(['that'], ['가', '다는'])], meaning='한 유명한 운동선수가 죽었다는 뉴스',
           explanation='that절이 앞 명사 The news의 내용을 설명하는 동격절(S′ a famous athlete, V′ had died). 동사 died 뒤에 목적어가 없어 절 전체가 표시됨.')
    s.review = ('주절 The news … became …(주어 뒤 동격 that절) + [but] 등위절 it turned out to be fake(turn out to V). '
                '동격 that절 과거완료 had died(이슈가 되기 전에 죽었다는 내용). 힌트 1개(동격 that). had died는 기본 분석 u1-gp1(had p.p.)에 연결. '
                'turn out to V는 각주로 제공(구조 힌트 후보는 상위 동격 that 우선). 관계사·수동 없음.')
    out.append(s)

    # ---------------- s07 ----------------
    s = S('s07', T['s07'])
    s.ch('It had been made', '그것은 만들어졌다')
    s.ch('by content creators', '콘텐츠 제작자들에 의해')
    s.ch('who sought people’s attention.', '사람들의 관심을 추구했던.')
    s.natural('그 뉴스는 사람들의 관심을 끌려던 콘텐츠 제작자들이 만든 것이었다.')
    s.cl('main', 'It', subj='It', verbs=['had', 'been', 'made'])
    s.cl('subject_relative', 'who', verbs=['sought'], marker='who')
    s.g('It', 'it', '그것은', referent_ko='유명한 운동선수가 사망했다는 가짜 뉴스')
    f = s.g('had|been', 'had been p.p.', '~되었다', kind='function', combines_with=[])
    md = s.g('made', 'made', '만들어진', verb_form=pp('passive-participle', s, 'made', 'make', f['id']))
    link(f, md)
    s.g('by', 'by', '~에 의해')
    s.g('content|creators', 'content creators', '콘텐츠 제작자들', star=W['creators'])
    rel = s.g('who', 'who V′', 'V′했던 (관계대명사)')
    s.g('sought', 'sought', '추구했다, 얻으려 했다 (seek의 과거)', verb_form=pp('irregular-past', s, 'sought', 'seek'))
    s.g('people’s', 'people’s', '사람들의')
    s.g('attention', 'attention', '관심, 주목')
    s.brk('by', 'passive-agent-by', '과거완료 수동 had been made의 행위자(누구에 의해)를 나타내는 by 구')
    s.hint('content creators [who sought]', '[추구했던] 콘텐츠 제작자들', span='content creators who sought',
           label='주격 관계대명사 who', links=[(['who'], ['던'])], meaning='(사람들의 관심을) 추구했던 콘텐츠 제작자들',
           explanation="선행사 content creators를 주격 관계대명사 who가 받아 sought people’s attention이 꾸민다. 주격이라 V′ sought까지만 표시.")
    s.vf_hint(fn=f, lex=md, en='had been made', ko='만들어졌다', formula='had been p.p.', step_form='made', step_ko='만들어진',
              en_mark=['had been'], ko_mark=['어졌다'], span='It had been made', meaning='만들어졌다',
              explanation='과거완료 수동 had been made: 뉴스가 퍼지기 전에 이미 만들어졌다. 주어 It과 by 구는 표시에서 제외.')
    s.relative_ids = [rel['id']]
    s.review = ('주절 과거완료 수동 had been made + 행위자 by content creators(by 앞에서 끊음) + 주격 관계절 who sought(선행사 content creators). '
                'It은 앞 문장의 유명 운동선수 사망 가짜 뉴스. 힌트 2개(필수 관계사, had been p.p. 기능 결합).')
    out.append(s)

    # ---------------- s08 ----------------
    s = S('s08', T['s08'])
    s.ch('They produced provocative false stories', '그들은 자극적인 거짓 이야기들을 만들어 냈다')
    s.ch('to make money', '돈을 벌기 위해')
    s.ch('by raising the number', '수를 높임으로써')
    s.ch('of views', '조회의')
    s.ch('of their posts.', '그들의 게시물들의.')
    s.natural('그들은 자신들의 게시물 조회수를 높여 돈을 벌기 위해 자극적인 거짓 이야기를 만들어 냈다.')
    s.cl('main', 'They', subj='They', verbs=['produced'])
    s.g('They', 'they', '그들은', referent_ko='콘텐츠 제작자들')
    s.g('produced', 'produce', '만들어 내다, 생산하다', verb_form=pp('regular-past', s, 'produced', 'produce'))
    s.g('provocative', 'provocative', '자극적인, 도발적인', star=W['provocative'])
    s.g('false', 'false', '거짓의, 사실이 아닌')
    s.g('stories', 'stories', '이야기들')
    ft = s.g('to', 'to V', '~하기 위해', kind='function', combines_with=[])
    mm = s.g('make|money', 'make money', '돈을 벌다')
    link(ft, mm)
    fb = s.g('by', 'by V-ing', '~함으로써', kind='function', combines_with=[])
    rs = s.g('raising', 'raise', '높이다, 올리다', verb_form=pp('ing', s, 'raising', 'raise'))
    link(fb, rs)
    s.g('number', 'number', '수')
    s.g('of', 'of', '~의')
    s.g('views', 'views', '조회 (흔한 뜻: 견해들)')
    s.g('of', 'of', '~의', at=s.text.index('of their'))
    s.g('their', 'their', '그들의', referent_ko='콘텐츠 제작자들')
    s.g('posts', 'posts', '게시물들')
    s.brk('of', 'postnominal-preposition', 'of views는 앞 명사 the number를 뒤에서 꾸미는 전치사구')
    s.brk('of', 'postnominal-preposition', 'of their posts는 앞 명사 views를 뒤에서 꾸미는 전치사구', after=s.text.index('views'))
    s.hint('[to make money]', '[돈을 벌기 위해]', span='to make money', label='목적의 to부정사',
           links=[(['to'], ['기 위해'])], meaning='돈을 벌기 위해',
           explanation='to make money는 자극적인 거짓 이야기를 만들어 낸 목적을 나타낸다.')
    s.hint('[by raising]', '[높임으로써]', span='by raising', label='전치사 by + 동명사',
           links=[(['by', 'ing'], ['임으로써'])], meaning='(조회수를) 높임으로써',
           explanation='전치사 by + 동명사 raising: ~함으로써(수단). 돈을 버는 방법. 목적어 the number of views of their posts는 표시에서 제외.')
    s.review = ('단일 주절 produced + 목적 to부정사 to make money + 수단 by raising …. the number of views of their posts는 어순이 뒤집히는 일반 명사구라 '
                '수량+of 예외가 아니며 두 of 앞에서 끊음. 힌트 2개(목적 to V, by + 동명사). 관계사·수동 없음.')
    out.append(s)

    # ---------------- s09 ----------------
    s = S('s09', T['s09'], key=True)
    s.ch('At that time,', '그 당시에,')
    s.ch('Gina criticized those', '지나는 사람들을 비판했다')
    s.ch('who had made and spread fake news', '가짜 뉴스를 만들고 퍼뜨렸던')
    s.ch('because it had hurt the athlete', '그것이 그 운동선수에게 상처를 주었고')
    s.ch('and confused people.', '사람들을 혼란스럽게 했기 때문에.')
    s.natural('그 당시 지나는 가짜 뉴스를 만들고 퍼뜨린 사람들을 비판했는데, 그 뉴스가 그 운동선수에게 상처를 주고 사람들을 혼란스럽게 했기 때문이었다.')
    s.cl('main', 'Gina', subj='Gina', verbs=['criticized'])
    s.cl('subject_relative', 'who', verbs=['had', 'made', 'and', 'spread'], marker='who')
    s.cl('subordinate', 'because', subj='it', verbs=['had', 'hurt', 'and', 'confused'], marker='because')
    s.g('At|that|time', 'at that time', '그 당시에')
    s.g('criticized', 'criticize', '비판하다', verb_form=pp('regular-past', s, 'criticized', 'criticize'))
    s.g('those', 'those', '(~한) 사람들')
    rel = s.g('who', 'who V′', 'V′했던 (관계대명사)')
    f1 = s.g('had', 'had p.p.', '~했다', kind='function', combines_with=[])
    mk = s.g('made', 'make', '만들다 (made는 make의 p.p.형)', verb_form=pp('perfect-participle', s, 'made', 'make', f1['id']))
    sp = s.g('spread', 'spread', '퍼뜨리다 (spread는 spread의 p.p.형)', verb_form=pp('perfect-participle', s, 'spread', 'spread', f1['id']))
    link(f1, mk, sp)
    s.g('fake|news', 'fake news', '가짜 뉴스')
    s.g('because', 'because S′ V′', 'S′(이/가) V′했기 때문에')
    s.g('it', 'it', '그것이', referent_ko='그 가짜 뉴스')
    f2 = s.g('had', 'had p.p.', '~했다', kind='function', combines_with=[], at=s.text.index('had hurt'))
    ht = s.g('hurt', 'hurt', '상처를 주다 (hurt는 hurt의 p.p.형)', verb_form=pp('perfect-participle', s, 'hurt', 'hurt', f2['id']))
    s.g('athlete', 'athlete', '운동선수')
    cf = s.g('confused', 'confuse', '혼란스럽게 하다 (confused는 confuse의 p.p.형)',
             verb_form=pp('perfect-participle', s, 'confused', 'confuse', f2['id']))
    link(f2, ht, cf)
    s.g('people', 'people', '사람들')
    s.hint('those [who had made and spread]', '[만들고 퍼뜨렸던] 사람들', span='those who had made and spread',
           label='주격 관계대명사 who', links=[(['who'], ['던'])], meaning='(가짜 뉴스를) 만들고 퍼뜨렸던 사람들',
           explanation='those(사람들)를 주격 관계대명사 who가 받아 had made and spread fake news가 꾸민다. 병렬 동사 made and spread가 had를 공유. 목적어 fake news는 표시에서 제외.')
    s.hint('[because it had hurt]', '[그것[그 가짜 뉴스]이 상처를 주었기 때문에]', span='because it had hurt',
           label='이유 접속사 because', links=[(['because'], ['이', '기 때문에'])], refs=[('it', '그것', '[그 가짜 뉴스]')],
           meaning='그것이 (그 운동선수에게) 상처를 주었기 때문에',
           explanation='because가 이끄는 이유 부사절(S′ it, V′ had hurt … and confused). 병렬 둘째 동사 confused와 목적어는 표시에서 제외.')
    s.relative_ids = [rel['id']]
    s.review = ('주절 criticized those + 주격 관계절 who had made and spread fake news(병렬 과거분사가 had 공유) + 이유 부사절 because it had hurt … and confused …(병렬). '
                'it은 앞 문장의 가짜 뉴스. 힌트 2개(필수 관계사, because). 과거완료 두 곳은 기본 분석 u1-gp1(had p.p.)에 연결. 수동 없음.')
    out.append(s)

    # ---------------- s10 ----------------
    s = S('s10', T['s10'])
    s.ch('This time,', '이번에는,')
    s.ch('however,', '하지만,')
    s.ch('Gina herself had accidentally contributed', '지나 자신이 뜻하지 않게 기여했다')
    s.ch('to the spread', '확산에')
    s.ch('of fake news.', '가짜 뉴스의.')
    s.natural('하지만 이번에는 지나 자신이 뜻하지 않게 가짜 뉴스의 확산에 한몫한 것이었다.')
    s.cl('main', 'Gina', subj='Gina herself', verbs=['had', 'contributed'])
    s.g('This|time', 'this time', '이번에는')
    s.g('however', 'however', '하지만')
    s.g('herself', 'herself', '(그녀) 자신이, 직접', referent_ko='지나')
    f = s.g('had', 'had p.p.', '~했다', kind='function', combines_with=[])
    s.g('accidentally', 'accidentally', '뜻하지 않게, 실수로')
    ct = s.g('contributed', 'contribute', '기여하다, 한몫하다 (contributed는 contribute의 p.p.형)',
             verb_form=pp('perfect-participle', s, 'contributed', 'contribute', f['id']))
    link(f, ct)
    s.g('to', 'to', '~에')
    s.g('spread', 'spread', '확산, 퍼짐')
    s.g('of', 'of', '~의')
    s.g('fake|news', 'fake news', '가짜 뉴스')
    s.brk('of', 'postnominal-preposition', 'of fake news는 앞 명사 the spread를 뒤에서 꾸미는 전치사구')
    s.vf_hint(fn=f, lex=ct, en='had accidentally contributed', ko='뜻하지 않게 기여했다', formula='had p.p.',
              step_form='contribute', step_ko='기여하다', en_mark=['had'], ko_mark=['했다'],
              span='Gina herself had accidentally contributed', meaning='뜻하지 않게 기여했다',
              explanation='빈 힌트 문장의 과거완료 후보: had accidentally contributed(흔들바위 뉴스 공유 당시 이미 한 일). 부사 accidentally는 표시 범위 안이라 보존. 주어와 to 이하 제외.')
    s.review = ('단일 주절 과거완료 had accidentally contributed(사이 부사 accidentally) + to the spread of fake news(contribute와 to는 대표 뜻 ~에로 분리). '
                'herself는 주어 Gina를 강조하는 재귀대명사. of fake news 앞 후치수식 경계. 관계사·접속사절 없음 → 과거완료 기능 결합 힌트.')
    out.append(s)
    return out


UNIT = {
    'id': 'u1', 'source_id': 'src', 'paragraph_ids': ['p01', 'p02'],
    'sentence_ids': [f's{n:02d}' for n in range(1, 11)],
    'today_words': [
        {'id': W['astonished'], 'text': 'astonished', 'meaning_ko': '깜짝 놀란'},
        {'id': W['headline'], 'text': 'news headline', 'meaning_ko': '뉴스 헤드라인, 뉴스 제목'},
        {'id': W['undamaged'], 'text': 'undamaged', 'meaning_ko': '손상되지 않은, 멀쩡한'},
        {'id': W['embarrassed'], 'text': 'embarrassed', 'meaning_ko': '당황한, 창피한'},
        {'id': W['incident'], 'text': 'incident', 'meaning_ko': '사건'},
        {'id': W['turn_out'], 'text': 'turn out to V', 'meaning_ko': '~인 것으로 드러나다, 밝혀지다'},
        {'id': W['creators'], 'text': 'content creators', 'meaning_ko': '콘텐츠 제작자들'},
        {'id': W['provocative'], 'text': 'provocative', 'meaning_ko': '자극적인, 도발적인'},
    ],
}


def analysis(_):
    return {
        'heading_kind': '제목',
        'title_or_topic_en': 'Gina Spreads Fake News by Mistake',
        'title_or_topic_ko': '실수로 가짜 뉴스를 퍼뜨린 지나',
        'intent_ko': '지나가 흔들바위 가짜 뉴스를 믿고 친구들에게 퍼뜨린 경험을 통해, 가짜 뉴스를 비판하던 사람도 뜻하지 않게 가짜 뉴스를 퍼뜨리는 사람이 될 수 있음을 보여 주며 글을 시작한다.',
        'flow': [
            {'sentence_ids': ['s01', 's02', 's03', 's04'], 'label': '사건',
             'text_ko': '지나는 소셜 미디어에서 흔들바위가 떨어졌다는 헤드라인을 보고 놀라 친구들에게 곧바로 공유했다. 그런데 아침 뉴스에서 그 기사가 가짜였다고 밝혀졌고, 지나는 자신이 가짜 뉴스를 퍼뜨렸다는 사실에 당황했다.'},
            {'sentence_ids': ['s05', 's06', 's07', 's08', 's09'], 'label': '떠오른 과거',
             'text_ko': '이 일로 지나는 예전의 유명 운동선수 사망 가짜 뉴스를 떠올린다. 그 뉴스는 조회수로 돈을 벌려는 콘텐츠 제작자들이 만든 것이었고, 지나는 그때 가짜 뉴스를 만들고 퍼뜨린 사람들을 비판했다.'},
            {'sentence_ids': ['s10'], 'label': '깨달음',
             'text_ko': '하지만 이번에는 지나 자신이 뜻하지 않게 가짜 뉴스를 퍼뜨리는 데 한몫했다.'},
        ],
        'easy_explanations': [
            {'sentence_id': 's03', 'explanatory_sentences': [
                '3번 문장은 1~2번에서 지나가 믿고 퍼뜨린 소식이 사실인지 밝혀지는 장면이다.',
                '기자는 흔들바위 바로 옆에서 방송을 하고 있었다.',
                '흔들바위는 떨어지지 않고 멀쩡하게 제자리에 있었다.',
                '그래서 기자는 흔들바위가 망가졌다는 인터넷 기사들이 가짜라고 알린다.']},
            {'sentence_id': 's07', 'explanatory_sentences': [
                '7번 문장은 6번의 운동선수 사망 뉴스를 누가 만들었는지 알려 준다.',
                '콘텐츠 제작자는 인터넷에 글이나 영상을 만들어 올리는 사람이다.',
                '이 사람들은 많은 사람의 관심을 끌고 싶어서 그 가짜 뉴스를 만들었다.',
                '8번 문장에서 그 관심이 곧 돈벌이와 이어진다는 것이 드러난다.']},
            {'sentence_id': 's10', 'explanatory_sentences': [
                '10번 문장은 9번과 반대되는 지나의 모습을 보여 준다.',
                '예전의 지나는 가짜 뉴스를 퍼뜨린 사람들을 비판하는 쪽이었다.',
                '그런데 이번에는 지나 자신이 흔들바위 가짜 뉴스를 친구들에게 퍼뜨렸다.',
                '일부러 한 일은 아니지만 결과적으로 가짜 뉴스가 퍼지는 데 한몫한 것이다.',
                '가짜 뉴스를 비판하던 사람도 뜻하지 않게 가짜 뉴스를 퍼뜨릴 수 있다는 점이 이 글의 출발점이다.']},
        ],
        'grammar_points': [
            {'id': 'u1-gp1', 'sentence_id': 's04', 'span': 'that she had spread the fake news',
             'title': 'had p.p.: (그 전에) ~했다', 'formula_key': 'had p.p.',
             'explanation': '공식: had p.p. — ~했다(과거의 어느 때보다 먼저 일어난 일). had p.p. = had spread(퍼뜨렸다; spread는 spread의 p.p.형), '
                            'S′ = she(지나), 목적어 = the fake news(가짜 뉴스). → 그녀가 가짜 뉴스를 퍼뜨렸다. '
                            '지나가 당황한 것(was embarrassed)은 과거이고, 가짜 뉴스를 퍼뜨린 일은 그보다 먼저라서 had spread를 쓴다.',
             'practice': {'span': 'she had spread the fake news',
                          'formula_support': {'en': 'had p.p.', 'ko': '~했다'},
                          'support': [('s04', 'she'), ('s04', 'spread'), ('s04', 'fake news')],
                          'answer_ko': '그녀가 가짜 뉴스를 퍼뜨렸다'}},
            {'id': 'u1-gp2', 'sentence_id': 's06', 'span': 'The news that a famous athlete had died',
             'title': '명사 + that S′ V′(동격): S′(이/가) V′했다는 명사', 'formula_key': 'N + that S′ V′',
             'explanation': '공식: 명사(N) + that S′ V′ — S′(이/가) V′했다는 N. N = The news(뉴스), that = 앞 명사의 내용을 알려 주는 접속사, '
                            'S′ = a famous athlete(한 유명한 운동선수), V′ = had died(죽었다). → 한 유명한 운동선수가 죽었다는 뉴스. '
                            'that 뒤에 주어와 동사가 모두 있는 완전한 절이 와서 뉴스의 ‘내용’을 설명한다.',
             'practice': {'span': 'The news that a famous athlete had died',
                          'formula_support': {'en': 'N + that S′ V′', 'ko': 'S′(이/가) V′했다는 N'},
                          'support': [('s06', 'news'), ('s06', 'famous'), ('s06', 'athlete'), ('s06', 'had p.p.'), ('s06', 'die')],
                          'answer_ko': '한 유명한 운동선수가 죽었다는 뉴스'}},
            {'id': 'u1-gp3', 'sentence_id': 's09', 'span': 'those who had made and spread fake news',
             'title': 'those who V′: V′한 사람들', 'formula_key': 'those who V′',
             'explanation': '공식: those who V′ — V′한 사람들. those = 사람들, who = 주격 관계대명사(그 사람들이), '
                            'V′ = had made and spread(만들고 퍼뜨렸다), 목적어 = fake news(가짜 뉴스). → 가짜 뉴스를 만들고 퍼뜨렸던 사람들. '
                            'those는 여기서 ‘그것들’이 아니라 뒤의 who절이 꾸미는 ‘사람들’이다.',
             'practice': {'span': 'those who had made and spread fake news',
                          'formula_support': {'en': 'those who V′', 'ko': 'V′한 사람들'},
                          'support': [('s09', 'had p.p.'), ('s09', 'make'), ('s09', 'spread'), ('s09', 'fake news')],
                          'answer_ko': '가짜 뉴스를 만들고 퍼뜨렸던 사람들'}},
            {'id': 'u1-gp4', 'sentence_id': 's01', 'span': 'The Heundeulbawi in Seoraksan National Park Has Fallen',
             'title': 'have p.p.: ~했다', 'formula_key': 'have p.p.',
             'explanation': '공식: have(has) p.p. — ~했다(지금의 결과까지 이어짐). S = The Heundeulbawi(흔들바위), in Seoraksan National Park = 설악산 국립공원에 있는, '
                            'p.p. = Fallen(fall의 p.p.형, 떨어지다). → 설악산 국립공원의 흔들바위가 떨어졌다. '
                            '떨어져서 지금은 제자리에 없다는 결과를 알리는 헤드라인이라 현재완료를 쓴다.',
             'supplemental': {'function': ('s01', 'have p.p.', 0),
                              'reason': 's01의 현재완료 Has Fallen은 while·when 힌트가 있어 결합 힌트로 선정하지 않았고, 기본 분석 3개에 have p.p. 설명이 없어 이 단위 대표 사례로 1회 보충'},
             'practice': {'span': 'The Heundeulbawi in Seoraksan National Park Has Fallen',
                          'formula_support': {'en': 'have p.p.', 'ko': '~했다'},
                          'support': [('s01', 'Heundeulbawi'), ('s01', 'in'), ('s01', 'Seoraksan National Park'), ('s01', 'fall')],
                          'answer_ko': '설악산 국립공원에 있는 흔들바위가 떨어졌다'}},
            {'id': 'u1-gp5', 'sentence_id': 's03', 'span': 'stories of the Heundeulbawi being damaged',
             'title': 'being p.p.: ~되는 것 (동명사의 수동)', 'formula_key': 'being p.p.',
             'explanation': '공식: being p.p. — ~되는 것. 앞의 of = ~에 관한, 의미상 주어 = the Heundeulbawi(흔들바위), p.p. = damaged(손상된). '
                            '→ 흔들바위가 손상되는 것에 관한 기사들(자연스럽게는 ‘흔들바위가 손상되었다는 기사들’). '
                            '흔들바위는 스스로 손상시키는 쪽이 아니라 ‘손상되는’ 대상이라 수동 being damaged를 쓴다.',
             'supplemental': {'function': ('s03', 'being p.p.', 0),
                              'reason': 's03의 동명사 수동 being damaged는 일반형 힌트 2개(현재분사 후치수식, of + 동명사)가 있어 결합 힌트로 선정하지 않았고, 기본 분석 3개에 being p.p. 설명이 없어 이 단위 대표 사례로 1회 보충'},
             'practice': {'span': 'stories of the Heundeulbawi being damaged',
                          'formula_support': {'en': 'being p.p.', 'ko': '~되는 것'},
                          'support': [('s03', 'stories'), ('s03', 'of'), ('s03', 'damaged')],
                          'answer_ko': '흔들바위가 손상되는 것에 관한 기사들'}},
        ],
        'formula_routes': [
            {'function': ('s01', 'have p.p.', 0), 'route': 'analysis', 'grammar_point_id': 'u1-gp4',
             'review_record': 'Has Fallen: while·when 힌트가 있어 분석 보충 u1-gp4로 연결'},
            {'function': ('s03', 'being p.p.', 0), 'route': 'analysis', 'grammar_point_id': 'u1-gp5',
             'review_record': 'being damaged: 일반형 힌트 2개가 있어 분석 보충 u1-gp5로 연결'},
            {'function': ('s04', 'had p.p.', 0), 'route': 'analysis', 'grammar_point_id': 'u1-gp1',
             'review_record': 'had spread: 이 문장의 기본 분석 u1-gp1이 had p.p.를 설명'},
            {'function': ('s05', 'had p.p.', 0), 'route': 'analysis', 'grammar_point_id': 'u1-gp1',
             'review_record': 'had happened: 관계사 힌트가 있어 같은 공식의 기본 분석 u1-gp1로 연결'},
            {'function': ('s06', 'had p.p.', 0), 'route': 'analysis', 'grammar_point_id': 'u1-gp1',
             'review_record': 'had died: 동격 that 힌트가 있어 같은 공식의 기본 분석 u1-gp1로 연결'},
            {'function': ('s07', 'had been p.p.', 0), 'route': 'hint', 'hint_index': 1,
             'review_record': 'had been made: 관계사 힌트 뒤 두 번째 힌트로 과거완료 수동 기능 결합 제공'},
            {'function': ('s09', 'had p.p.', 0), 'route': 'analysis', 'grammar_point_id': 'u1-gp1',
             'review_record': 'had made and spread: 관계사·because 힌트가 있어 같은 공식의 기본 분석 u1-gp1로 연결'},
            {'function': ('s09', 'had p.p.', 1), 'route': 'analysis', 'grammar_point_id': 'u1-gp1',
             'review_record': 'had hurt and confused: 관계사·because 힌트가 있어 같은 공식의 기본 분석 u1-gp1로 연결'},
            {'function': ('s10', 'had p.p.', 0), 'route': 'hint', 'hint_index': 0,
             'review_record': 'had accidentally contributed: 빈 힌트 문장의 과거완료 기능 결합 힌트'},
        ],
        'relations': [
            {'head': {'id': 'u1-r1h', 'text': 'famous', 'meaning_ko': '유명한'},
             'synonym': {'id': 'u1-r1s', 'text': 'well-known', 'meaning_ko': '잘 알려진, 유명한'},
             'antonym': {'id': 'u1-r1a', 'text': 'unknown', 'meaning_ko': '알려지지 않은, 무명의'}},
            {'head': {'id': 'u1-r2h', 'text': 'criticize', 'meaning_ko': '비판하다'},
             'synonym': {'id': 'u1-r2s', 'text': 'condemn', 'meaning_ko': '비난하다'},
             'antonym': {'id': 'u1-r2a', 'text': 'praise', 'meaning_ko': '칭찬하다'}},
            {'head': {'id': 'u1-r3h', 'text': 'accidentally', 'meaning_ko': '뜻하지 않게, 실수로'},
             'synonym': {'id': 'u1-r3s', 'text': 'unintentionally', 'meaning_ko': '의도하지 않게, 무심코'},
             'antonym': {'id': 'u1-r3a', 'text': 'intentionally', 'meaning_ko': '의도적으로, 일부러'}},
        ],
    }


def workbook():
    return {
        'relation_order': ['u1-r2s', 'u1-r3a', 'u1-r1h', 'u1-r2a', 'u1-r3s', 'u1-r1s', 'u1-r2h', 'u1-r1a', 'u1-r3h'],
        'key_sentence_ids': ['s04', 's09'],
        'question_id': 'Q01',
        'syntax_point_ids': ['u1-gp1', 'u1-gp2', 'u1-gp3', 'u1-gp4', 'u1-gp5'],
    }
