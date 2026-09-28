"""공통 단위 3: The Reasons for the Viral Spread of Fake News (s20~s30, 단락 p05~p07; 짧은 단락이 있어 소제목 전체 묶음)."""
from author import S, link
from u1 import pp, v3

W = {'viral': 'u3-w1', 'phenomenon': 'u3-w2', 'effortlessly': 'u3-w3', 'proof': 'u3-w4',
     'inclined': 'u3-w5', 'prejudices': 'u3-w6', 'bias': 'u3-w7', 'selectively': 'u3-w8'}


def sentences(T):
    out = []

    # ---------------- s20 ----------------
    s = S('s20', T['s20'])
    s.ch('Fake news', '가짜 뉴스는')
    s.ch('on social media', '소셜 미디어상의')
    s.ch('spreads significantly farther and faster', '훨씬 더 멀리 그리고 더 빠르게 퍼진다')
    s.ch('than true stories.', '진짜 이야기들보다.')
    s.natural('소셜 미디어상의 가짜 뉴스는 진짜 이야기보다 훨씬 더 멀리, 더 빠르게 퍼진다.')
    s.cl('main', 'Fake', subj='Fake news on social media', verbs=['spreads'], disp='Fake news',
         disp_review='중심명사 news까지 표시하고 뒤수식 on social media는 제외')
    s.g('Fake|news', 'fake news', '가짜 뉴스')
    s.g('on', 'on', '~상의 (흔한 뜻: ~위에)')
    s.g('social|media', 'social media', '소셜 미디어')
    s.g('spreads', 'spread', '퍼지다', verb_form=v3(s, 'spreads', 'spread', 'Fake news'))
    s.g('significantly', 'significantly', '훨씬, 상당히')
    s.g('farther', 'farther', '더 멀리 (far의 비교급)')
    s.g('faster', 'faster', '더 빠르게 (fast의 비교급)')
    s.g('than', 'than', '~보다')
    s.g('true', 'true', '진짜의, 사실인')
    s.g('stories', 'stories', '이야기들')
    s.brk('on', 'postnominal-preposition', 'on social media는 앞 명사 Fake news를 뒤에서 꾸미는 전치사구')
    s.hint('farther and faster [than true stories]', '[진짜 이야기들보다] 더 멀리 그리고 더 빠르게', span='farther and faster than true stories',
           label='비교급 + than', links=[(['er', ('er', 1), 'than'], ['더', ('더', 1), '보다'])],
           meaning='진짜 이야기들보다 더 멀리 그리고 더 빠르게',
           explanation='비교급 farther·faster가 than과 짝을 이뤄 가짜 뉴스와 진짜 이야기를 비교한다(~보다 더 …하게). significantly는 비교급을 강조(훨씬).')
    s.review = '단일 주절 spreads(주어 Fake news on social media) + 비교급 farther and faster than …. on 앞 후치수식 경계. 힌트 1개(비교급 than). 관계사·접속사절·수동 없음.'
    out.append(s)

    # ---------------- s21 ----------------
    s = S('s21', T['s21'])
    s.ch('A study', '한 연구는')
    s.ch('by the Massachusetts Institute of Technology', '매사추세츠 공과대학에 의한')
    s.ch('in the US', '미국에 있는')
    s.ch('has shown', '보여 주었다')
    s.ch('that fake news spreads online', '가짜 뉴스가 온라인에서 퍼진다는 것을')
    s.ch('6 times faster', '6배 더 빠르게')
    s.ch('than real news', '진짜 뉴스보다')
    s.ch('on average.', '평균적으로.')
    s.natural('미국 매사추세츠 공과대학의 한 연구는 가짜 뉴스가 평균적으로 진짜 뉴스보다 6배 더 빠르게 온라인에서 퍼진다는 것을 보여 주었다.')
    s.cl('main', 'A', subj='A study by the Massachusetts Institute of Technology in the US', verbs=['has', 'shown'], disp='A study',
         disp_review='중심명사 study까지 표시하고 뒤수식 by the Massachusetts Institute of Technology in the US는 제외')
    s.cl('subordinate', 'that', subj='fake news', verbs=['spreads'], marker='that')
    s.g('study', 'study', '연구')
    s.g('by', 'by', '~에 의한')
    s.g('Massachusetts|Institute|of|Technology', 'Massachusetts Institute of Technology', '매사추세츠 공과대학 (MIT, 미국의 대학)', proper=True)
    s.g('in', 'in', '~에 있는')
    s.g('US', 'the US', '미국', proper=True)
    f = s.g('has', 'have p.p.', '~했다', kind='function', combines_with=[])
    sh = s.g('shown', 'show', '보여 주다 (shown은 show의 p.p.형)', verb_form=pp('perfect-participle', s, 'shown', 'show', f['id']))
    link(f, sh)
    s.g('that', 'that S′ V′', 'S′(이/가) V′한다는 것을 (접속사)')
    s.g('fake|news', 'fake news', '가짜 뉴스')
    s.g('spreads', 'spread', '퍼지다', verb_form=v3(s, 'spreads', 'spread', 'fake news'))
    s.g('online', 'online', '온라인에서')
    s.g('times', 'times', '~배')
    s.g('faster', 'faster', '더 빠르게 (fast의 비교급)')
    s.g('than', 'than', '~보다')
    s.g('real', 'real', '진짜의')
    s.g('news', 'news', '뉴스', at=s.text.index('news on average'))
    s.g('on|average', 'on average', '평균적으로')
    s.brk('by', 'postnominal-preposition', 'by the Massachusetts Institute of Technology는 앞 명사 A study를 뒤에서 꾸미는 전치사구(연구의 주체)')
    s.brk('in', 'postnominal-preposition', 'in the US는 앞 명사 the Massachusetts Institute of Technology를 뒤에서 꾸미는 전치사구')
    s.hint('[that fake news spreads]', '[가짜 뉴스가 퍼진다는 것]', span='that fake news spreads', label='명사절 접속사 that',
           links=[(['that'], [('가', 1), '다는 것'])], meaning='가짜 뉴스가 퍼진다는 것',
           explanation='has shown의 목적어 that 명사절(S′ fake news, V′ spreads). 뒤의 online 6 times faster … 이하와 바깥 동사 has shown은 표시에서 제외.')
    s.vf_hint(fn=f, lex=sh, en='has shown', ko='보여 주었다', formula='have p.p.', step_form='show', step_ko='보여 주다',
              en_mark=['has'], ko_mark=['었다'], span='has shown', meaning='보여 주었다',
              explanation='현재완료 has shown: 연구 결과가 지금까지 보여 준 사실. 주어와 목적어 that절은 표시에서 제외.')
    s.review = ('주절 A study … has shown(주어 뒤수식 by …·in the US 앞에서 끊음; by는 연구의 주체를 나타내는 후치수식, 수동태 행위자 아님) + 목적어 that 명사절 fake news spreads … '
                '6 times faster than real news(배수 비교). 힌트 2개(명사절 that, have p.p. 기능 결합). 관계사·수동 없음.')
    out.append(s)

    # ---------------- s22 ----------------
    s = S('s22', T['s22'])
    s.ch('One explanation', '한 가지 설명은')
    s.ch('for this phenomenon', '이 현상에 대한')
    s.ch('is that people like new and provocative things.', '사람들이 새롭고 자극적인 것들을 좋아한다는 것이다.')
    s.natural('이 현상에 대한 한 가지 설명은 사람들이 새롭고 자극적인 것을 좋아한다는 것이다.')
    s.cl('main', 'One', subj='One explanation for this phenomenon', verbs=['is'], disp='One explanation',
         disp_review='중심명사 explanation까지 표시하고 뒤수식 for this phenomenon은 제외')
    s.cl('subordinate', 'that', subj='people', verbs=['like'], marker='that')
    s.g('One', 'one', '한 가지')
    s.g('explanation', 'explanation', '설명')
    s.g('for', 'for', '~에 대한')
    s.g('this', 'this', '이')
    s.g('phenomenon', 'phenomenon', '현상', star=W['phenomenon'])
    s.g('is', 'is', '~이다')
    s.g('that', 'that S′ V′', 'S′(이/가) V′한다는 것 (접속사)')
    s.g('people', 'people', '사람들')
    s.g('like', 'like', '좋아하다')
    s.g('new', 'new', '새로운')
    s.g('provocative', 'provocative', '자극적인')
    s.g('things', 'things', '것들')
    s.brk('for', 'postnominal-preposition', 'for this phenomenon은 앞 명사 One explanation을 뒤에서 꾸미는 전치사구')
    s.hint('[that people like]', '[사람들이 좋아한다는 것]', span='that people like', label='명사절 접속사 that',
           links=[(['that'], ['이', '다는 것'])], meaning='사람들이 (새롭고 자극적인 것들을) 좋아한다는 것',
           explanation='is의 보어인 that 명사절(S′ people, V′ like). 목적어 new and provocative things와 바깥 동사 is는 표시에서 제외.')
    s.review = ('주절 One explanation … is + 보어 that 명사절 people like new and provocative things. this phenomenon은 앞 문장의 가짜 뉴스가 더 빨리 퍼지는 현상. '
                'for 앞 후치수식 경계. 힌트 1개(명사절 that). 관계사·수동 없음.')
    out.append(s)

    # ---------------- s23 ----------------
    s = S('s23', T['s23'], key=True)
    s.ch('When information is astonishing,', '정보가 놀라울 때,')
    s.ch('people not only feel', '사람들은 느낄 뿐만 아니라')
    s.ch('that it is surprising,', '그것이 놀랍다고,')
    s.ch('but they also want to share the stimulating news', '그들은 또한 그 자극적인 뉴스를 공유하고 싶어 한다')
    s.ch('with others.', '다른 사람들과.')
    s.natural('정보가 놀라우면 사람들은 그것이 놀랍다고 느낄 뿐만 아니라 그 자극적인 뉴스를 다른 사람들과 공유하고 싶어 한다.')
    s.cl('subordinate', 'When', subj='information', verbs=['is'], marker='When')
    s.cl('main', 'people', subj='people', verbs=['feel'])
    s.cl('subordinate', 'that', subj='it', verbs=['is'], marker='that')
    s.cl('main', 'they', subj='they', verbs=['want'], marker='but')
    s.g('When', 'when S′ V′', 'S′(이/가) V′할 때')
    s.g('information', 'information', '정보')
    s.g('is', 'is', '~이다')
    s.g('astonishing', 'astonishing', '깜짝 놀라게 하는, 놀라운')
    s.g('people', 'people', '사람들')
    s.g('not|only|but|also', 'not only A but also B', 'A뿐만 아니라 B도')
    s.glosses.sort(key=lambda g: g['spans'][0][0])
    s.g('feel', 'feel', '느끼다', at=s.text.index('feel'))
    s.g('that', 'that S′ V′', 'S′(이/가) V′하다고 (접속사)')
    s.g('it', 'it', '그것이', referent_ko='그 정보')
    s.g('is', 'is', '~이다', at=s.text.index('is surprising'))
    s.g('surprising', 'surprising', '놀라운')
    s.g('they', 'they', '그들은', referent_ko='사람들')
    s.g('want|to', 'want to V', '~하고 싶다',
        verb_construction={'kind': 'to-complement', 'verb_span': s.span_of('want'), 'lemma': 'want',
                           'link_spans': [s.span_of('to', s.text.index('want'))],
                           'review_record': 'they also want to share …: want to V, V=share.'})
    s.glosses.sort(key=lambda g: g['spans'][0][0])
    s.g('share', 'share', '공유하다', at=s.text.index('share'))
    s.g('stimulating', 'stimulating', '자극적인, 흥미를 돋우는')
    s.g('news', 'news', '뉴스')
    s.g('with', 'with', '~와')
    s.g('others', 'others', '다른 사람들')
    s.hint('[When information is astonishing]', '[정보가 놀라울 때]', span='When information is astonishing',
           label='시간 접속사 when', links=[(['When'], ['가', '울 때'])], meaning='정보가 놀라울 때',
           explanation='when이 이끄는 부사절(S′ information, V′ is + 최소 보어 astonishing). ~할 때(조건에 가까운 때).')
    s.hint('not only feel … but … also want to share', '느낄 뿐만 아니라 … 또한 공유하고 싶어 한다',
           span='not only feel that it is surprising, but they also want to share', category='paired-structure',
           display_spans=[s.span_of('not only feel'), s.span_of('but', s.text.index('surprising')), s.span_of('also want to share')],
           links=[(['not only', 'but', 'also'], ['뿐만 아니라', '또한'])],
           meaning='느낄 뿐만 아니라 또한 공유하고 싶어 한다',
           explanation='not only A but (they) also B(A뿐만 아니라 B도): A=feel that it is surprising, B=want to share …. but 뒤에 주어 they가 다시 나와 두 번째 절이 된다.')
    s.review = ('시간 부사절 When information is astonishing + 주절 people not only feel that it is surprising(목적어 that 명사절) + [but] they also want to share …: '
                'not only A but also B가 두 절을 잇는다(but 뒤 주어 they 반복). 힌트 2개(접속사 when, not only … but also 짝 구조). that절은 각주로 지원. 관계사·수동 없음.')
    out.append(s)

    # ---------------- s24 ----------------
    s = S('s24', T['s24'])
    s.ch('By passing it to others', '그것을 다른 사람들에게 전달함으로써')
    s.ch('on social media,', '소셜 미디어에서,')
    s.ch('they can gain attention', '그들은 관심을 얻을 수 있다')
    s.ch('because they are the first', '그들이 첫 번째 사람이기 때문에')
    s.ch('to post previously unknown, but possibly false, information.', '이전에 알려지지 않았지만 어쩌면 거짓일 수도 있는 정보를 게시하는.')
    s.natural('소셜 미디어에서 그것을 다른 사람들에게 전달하면, 그들은 이전에 알려지지 않았지만 어쩌면 거짓일 수도 있는 정보를 처음으로 게시한 사람이 되기 때문에 관심을 얻을 수 있다.')
    s.cl('main', 'they', subj='they', verbs=['can', 'gain'])
    s.cl('subordinate', 'because', subj='they', verbs=['are'], marker='because')
    fb = s.g('By', 'by V-ing', '~함으로써', kind='function', combines_with=[])
    ps = s.g('passing', 'pass', '전달하다', verb_form=pp('ing', s, 'passing', 'pass'))
    link(fb, ps)
    s.g('it', 'it', '그것을', referent_ko='그 자극적인 뉴스')
    s.g('to', 'to', '~에게')
    s.g('others', 'others', '다른 사람들')
    s.g('on', 'on', '~에서 (흔한 뜻: ~위에)')
    s.g('social|media', 'social media', '소셜 미디어')
    s.g('they', 'they', '그들은', referent_ko='자극적인 뉴스를 공유하는 사람들')
    fc = s.g('can', 'can V', '~할 수 있다', kind='function', combines_with=[])
    gn = s.g('gain', 'gain', '얻다')
    link(fc, gn)
    s.g('attention', 'attention', '관심, 주목')
    s.g('because', 'because S′ V′', 'S′(이/가) V′이기 때문에')
    s.g('they', 'they', '그들이', referent_ko='자극적인 뉴스를 공유하는 사람들', at=s.text.index('they are'))
    s.g('are', 'are', '~이다')
    s.g('first|to', 'the first to V', '처음으로 ~하는 사람')
    s.g('post', 'post', '게시하다, 올리다')
    s.g('previously', 'previously', '이전에')
    s.g('unknown', 'unknown', '알려지지 않은')
    s.g('possibly', 'possibly', '어쩌면, 아마')
    s.g('false', 'false', '거짓의')
    s.g('information', 'information', '정보')
    s.hint('[By passing]', '[전달함으로써]', span='By passing', label='전치사 by + 동명사',
           links=[(['By', 'ing'], ['함으로써'])], meaning='(그것을 다른 사람들에게) 전달함으로써',
           explanation='전치사 by + 동명사 passing: ~함으로써(수단). 관심을 얻는 방법. 목적어 it과 to others는 표시에서 제외.')
    s.hint('the first [to post]', '[게시하는] 첫 번째 사람', span='the first to post', label='to부정사 후치수식',
           links=[(['to'], ['는'])], meaning='(정보를) 게시하는 첫 번째 사람',
           explanation='to post …가 앞의 the first(첫 번째 사람)를 뒤에서 꾸민다(처음으로 게시하는 사람). 목적어 previously unknown … information은 표시에서 제외.')
    s.review = ('문두 수단 By passing it to others on social media(pass와 to는 대표 뜻 ~에게로 분리, L 검수 Lu3-02) + 주절 they can gain attention + 이유 부사절 because they are the first to post …(the first to V: 처음으로 ~하는 사람). '
                '목적어 information 앞에 삽입된 previously unknown, but possibly false(두 형용사구가 but으로 이어져 information을 꾸밈). 힌트 2개(by + 동명사, to부정사 후치수식). 관계사·수동 없음.')
    out.append(s)

    # ---------------- s25 ----------------
    s = S('s25', T['s25'])
    s.ch('Also,', '또한,')
    s.ch('fake news goes viral', '가짜 뉴스는 빠르게 퍼진다')
    s.ch('because people', '사람들이')
    s.ch('in their daily lives', '그들의 일상생활에서')
    s.ch('tend to think simply and effortlessly.', '단순하고 쉽게 생각하는 경향이 있기 때문에.')
    s.natural('또한 사람들은 일상생활에서 단순하고 쉽게 생각하는 경향이 있기 때문에 가짜 뉴스는 빠르게 퍼진다.')
    s.cl('main', 'fake', subj='fake news', verbs=['goes'])
    s.cl('subordinate', 'because', subj='people', verbs=['tend'], marker='because')
    s.g('Also', 'also', '또한')
    s.g('fake|news', 'fake news', '가짜 뉴스')
    s.g('goes|viral', 'go viral', '(인터넷에서) 급속히 퍼지다', star=W['viral'], verb_form=v3(s, 'goes', 'go', 'fake news'))
    s.g('because', 'because S′ V′', 'S′(이/가) V′하기 때문에')
    s.g('people', 'people', '사람들')
    s.g('in', 'in', '~에서')
    s.g('their', 'their', '그들의', referent_ko='사람들')
    s.g('daily', 'daily', '일상의, 매일의')
    s.g('lives', 'lives', '생활, 삶들 (life의 복수)')
    s.g('tend|to', 'tend to V', '~하는 경향이 있다',
        verb_construction={'kind': 'to-complement', 'verb_span': s.span_of('tend'), 'lemma': 'tend',
                           'link_spans': [s.span_of('to', s.text.index('tend'))],
                           'review_record': 'people … tend to think: tend to V, V=think.'})
    s.g('think', 'think', '생각하다')
    s.g('simply', 'simply', '단순하게')
    s.g('effortlessly', 'effortlessly', '힘들이지 않고, 쉽게', star=W['effortlessly'])
    s.hint('[because people in their daily lives tend to think]', '[사람들이 그들[사람들]의 일상생활에서 생각하는 경향이 있기 때문에]',
           span='because people in their daily lives tend to think', label='이유 접속사 because',
           links=[(['because'], ['이', '기 때문에'])], refs=[('their', '그들', '[사람들]')],
           meaning='사람들이 일상생활에서 (단순하고 쉽게) 생각하는 경향이 있기 때문에',
           explanation='because가 이끄는 이유 부사절(S′ people, V′ tend). tend to V는 뜻을 이루는 동사 구문이라 to think까지 표시하고 부사 simply and effortlessly는 제외. in their daily lives는 절 안의 부사구.')
    s.review = ('주절 fake news goes viral(go viral) + 이유 부사절 because people in their daily lives tend to think simply and effortlessly(tend to V). '
                'in their daily lives는 tend를 꾸미는 절 안 부사구로 보아 S′는 people. 힌트 1개(because). 관계사·수동 없음.')
    out.append(s)

    # ---------------- s26 ----------------
    s = S('s26', T['s26'])
    s.ch('It is more likely', '가능성이 더 높다')
    s.ch('for them to believe new information', '그들이 새로운 정보를 믿을')
    s.ch('without any proof,', '어떤 증거도 없이,')
    s.ch('instead of critically examining it.', '그것을 비판적으로 검토하는 대신에.')
    s.natural('사람들은 새로운 정보를 비판적으로 검토하는 대신 아무 증거 없이 믿을 가능성이 더 크다.')
    s.cl('main', 'It', subj='It', verbs=['is'])
    s.g('It|is|likely|for|to', 'It is likely for A to V', 'A(이/가) ~할 가능성이 높다 (It은 뒤의 for A to V를 대신함)')
    s.g('more', 'more', '더', at=s.text.index('more'))
    s.glosses.sort(key=lambda g: g['spans'][0][0])
    s.g('them', 'them', '그들이', referent_ko='일상생활에서 단순하게 생각하는 사람들', at=s.text.index('them'))
    s.g('believe', 'believe', '믿다', at=s.text.index('believe'))
    s.g('new', 'new', '새로운')
    s.g('information', 'information', '정보')
    s.g('without', 'without', '~ 없이')
    s.g('any', 'any', '어떤 ~도')
    s.g('proof', 'proof', '증거', star=W['proof'])
    fi = s.g('instead|of', 'instead of V-ing', '~하는 대신에', kind='function', combines_with=[])
    s.g('critically', 'critically', '비판적으로')
    ex = s.g('examining', 'examine', '검토하다, 조사하다', verb_form=pp('ing', s, 'examining', 'examine'))
    link(fi, ex)
    s.g('it', 'it', '그것을', referent_ko='새로운 정보')
    s.hint('It is more likely [for them to believe]', '[그들[사람들]이 믿을] 가능성이 더 높다',
           span='It is more likely for them to believe', label='가주어 It과 진주어 to부정사',
           links=[(['for', 'to'], ['이', '을'])], refs=[('them', '그들', '[사람들]')],
           meaning='그들이 (새로운 정보를) 믿을 가능성이 더 높다',
           explanation='It은 뒤의 for them to believe …를 대신하는 가주어. for 뒤 them은 to believe의 의미상 주어. 목적어 new information 이하는 제외.')
    s.hint('[instead of critically examining]', '[비판적으로 검토하는 대신에]', span='instead of critically examining',
           label='전치사 instead of + 동명사', links=[(['instead of', 'ing'], ['는 대신에'])],
           meaning='(그것을) 비판적으로 검토하는 대신에',
           explanation='전치사구 instead of 뒤에 동명사 examining(부사 critically가 앞에서 꾸밈)이 와서 ‘~하는 대신에’. 목적어 it은 표시에서 제외.')
    s.review = ('가주어 It + 진주어 for them to believe new information(A=them) + without any proof + instead of critically examining it(동명사). '
                'them은 앞 문장의 people. 진주어 앞(for 앞)에서 끊음. 힌트 2개(가주어–진주어, instead of + 동명사). 관계사·수동 없음.')
    out.append(s)

    # ---------------- s27 ----------------
    s = S('s27', T['s27'])
    s.ch('Moreover,', '게다가,')
    s.ch('people are inclined to believe information', '사람들은 정보를 믿는 경향이 있다')
    s.ch('that fits their prejudices or experiences', '그들의 편견이나 경험에 맞는')
    s.ch('even when not true.', '사실이 아닐 때조차.')
    s.natural('게다가 사람들은 사실이 아닐 때조차 자신의 편견이나 경험에 맞는 정보를 믿는 경향이 있다.')
    s.cl('main', 'people', subj='people', verbs=['are'])
    s.cl('subject_relative', 'that', verbs=['fits'], marker='that')
    s.g('Moreover', 'moreover', '게다가')
    s.g('people', 'people', '사람들')
    s.g('are|inclined|to', 'be inclined to V', '~하는 경향이 있다', star=W['inclined'])
    s.g('believe', 'believe', '믿다')
    s.g('information', 'information', '정보')
    rel = s.g('that', 'that V′', 'V′하는 (관계대명사)')
    s.g('fits', 'fit', '~에 맞다', verb_form=v3(s, 'fits', 'fit', '관계절 선행사 information'))
    s.g('their', 'their', '그들의', referent_ko='사람들')
    s.g('prejudices', 'prejudices', '편견들', star=W['prejudices'])
    s.g('or', 'or', '또는')
    s.g('experiences', 'experiences', '경험들')
    s.g('even', 'even', '~조차')
    s.g('when', 'when', '~일 때 (뒤에 it is가 생략됨)')
    s.g('not', 'not', '~이 아닌')
    s.g('true', 'true', '사실인')
    s.hint('information [that fits]', '[맞는] 정보', span='information that fits', label='주격 관계대명사 that',
           links=[(['that'], ['는'])], meaning='(그들의 편견이나 경험에) 맞는 정보',
           explanation='선행사 information을 주격 관계대명사 that이 받아 fits their prejudices or experiences가 꾸민다. V′ fits까지만 표시.')
    s.hint('[even when not true]', '[사실이 아닐 때조차]', span='even when not true', label='축약된 when 부사절',
           links=[(['even when'], ['때조차'])], meaning='사실이 아닐 때조차',
           explanation='even when (it is) not true: when 뒤에 주어 it(그 정보)과 be동사 is가 생략되었다. 생략된 말은 표시에 보충하지 않음.')
    s.relative_ids = [rel['id']]
    s.review = ('주절 people are inclined to believe information(be inclined to V, 숙어 각주) + 주격 관계절 that fits …(선행사 information) + 생략 부사절 even when (it is) not true. '
                '힌트 2개(필수 관계사, 생략된 when절). 수동 기능 공식 없음(be inclined to V는 숙어로 제공).')
    out.append(s)

    # ---------------- s28 ----------------
    s = S('s28', T['s28'])
    s.ch('In this process,', '이 과정에서,')
    s.ch('people easily fall into the trap', '사람들은 쉽게 함정에 빠진다')
    s.ch('of “confirmation bias.”', '‘확증 편향’이라는.')
    s.natural('이 과정에서 사람들은 ‘확증 편향’이라는 함정에 쉽게 빠진다.')
    s.cl('main', 'people', subj='people', verbs=['fall'])
    s.g('In', 'in', '~에서')
    s.g('this', 'this', '이')
    s.g('process', 'process', '과정')
    s.g('people', 'people', '사람들')
    s.g('easily', 'easily', '쉽게')
    s.g('fall|into', 'fall into', '~에 빠지다')
    s.g('trap', 'trap', '함정')
    s.g('of', 'of', '~이라는 (흔한 뜻: ~의)')
    s.g('confirmation|bias', 'confirmation bias', '확증 편향 (자기 생각에 맞는 정보만 받아들이는 경향)', star=W['bias'])
    s.brk('of', 'postnominal-preposition', 'of “confirmation bias”는 앞 명사 the trap의 내용을 나타내는 전치사구')
    s.hint('the trap [of “confirmation bias.”]', '[‘확증 편향’이라는] 함정', span='the trap of “confirmation bias', label='동격의 of',
           links=[(['of'], ['이라는'])], meaning='‘확증 편향’이라는 함정',
           explanation='of “confirmation bias”가 앞 명사 the trap이 무엇인지 설명한다(A라는 B). 원문 인용 부호와 마침표를 그대로 보존.')
    s.review = '단일 주절 fall into the trap + 동격의 of(‘확증 편향’이라는 함정). of 앞 후치수식 경계. 힌트 1개(동격 of). 관계사·수동 없음.'
    out.append(s)

    # ---------------- s29 ----------------
    s = S('s29', T['s29'], key=True)
    s.ch('That is,', '즉,')
    s.ch('they selectively accept news', '그들은 선택적으로 뉴스를 받아들인다')
    s.ch('in a way', '방식으로')
    s.ch('that only confirms their beliefs', '오직 그들의 믿음을 확인해 주는')
    s.ch('and ignore news', '그리고 뉴스는 무시한다')
    s.ch('that doesn’t support them.', '그것들을 뒷받침하지 않는.')
    s.natural('즉, 그들은 자신의 믿음을 확인해 주는 뉴스만 골라서 받아들이고, 믿음을 뒷받침하지 않는 뉴스는 무시한다.')
    s.cl('main', 'they', subj='they', verbs=['accept', 'and', 'ignore'])
    s.cl('subject_relative', 'that', verbs=['confirms'], marker='that')
    s.cl('subject_relative', 'that', verbs=['doesn’t', 'support'], marker='that', occ=1)
    s.g('That|is', 'that is', '즉, 다시 말해')
    s.g('they', 'they', '그들은', referent_ko='사람들')
    s.g('selectively', 'selectively', '선택적으로, 골라서', star=W['selectively'])
    s.g('accept', 'accept', '받아들이다')
    s.g('news', 'news', '뉴스')
    s.g('in', 'in', '~으로')
    s.g('way', 'way', '방식')
    r1 = s.g('that', 'that V′', 'V′하는 (관계대명사)')
    s.g('only', 'only', '오직, ~만')
    s.g('confirms', 'confirm', '확인해 주다, 사실임을 보여 주다', verb_form=v3(s, 'confirms', 'confirm', '관계절 선행사 a way'))
    s.g('their', 'their', '그들의', referent_ko='사람들')
    s.g('beliefs', 'beliefs', '믿음들, 신념들')
    s.g('ignore', 'ignore', '무시하다')
    s.g('news', 'news', '뉴스', at=s.text.index('news that doesn'))
    r2 = s.g('that', 'that V′', 'V′하는 (관계대명사)')
    fd = s.g('doesn’t', 'does not V', '~하지 않다', kind='function', combines_with=[])
    su = s.g('support', 'support', '뒷받침하다, 지지하다')
    link(fd, su)
    s.g('them', 'them', '그것들을', referent_ko='그들의 믿음들')
    s.hint('a way [that only confirms]', '[오직 확인해 주는] 방식', span='a way that only confirms', label='주격 관계대명사 that',
           links=[(['that'], ['는'])], meaning='오직 (그들의 믿음을) 확인해 주는 방식',
           explanation='선행사 a way를 주격 관계대명사 that이 받아 only confirms their beliefs가 꾸민다. 사이 부사 only는 보존하고 목적어는 제외.')
    s.hint('news [that doesn’t support]', '[뒷받침하지 않는] 뉴스', span='news that doesn’t support', label='주격 관계대명사 that',
           links=[(['that'], ['는'])], meaning='(그것들을) 뒷받침하지 않는 뉴스',
           explanation='선행사 news를 주격 관계대명사 that이 받아 doesn’t support them이 꾸민다. 부정 doesn’t를 보존하고 목적어 them은 제외.')
    s.relative_ids = [r1['id'], r2['id']]
    s.review = ('주절 they accept … and ignore …(병렬 동사) + 주격 관계절 두 개: that only confirms their beliefs(선행사 a way), that doesn’t support them(선행사 news, them=그들의 믿음들). '
                '힌트 2개(필수 관계사 둘). 수동 없음.')
    out.append(s)

    # ---------------- s30 ----------------
    s = S('s30', T['s30'])
    s.ch('During election season,', '선거철 동안,')
    s.ch('for example,', '예를 들어,')
    s.ch('people tend to blindly believe any news', '사람들은 어떤 뉴스든 맹목적으로 믿는 경향이 있다')
    s.ch('describing their favored candidates', '그들이 선호하는 후보들을 묘사하는')
    s.ch('in a positive way,', '긍정적인 방식으로,')
    s.ch('while unconsciously believing news', '그러면서 무의식적으로 뉴스를 믿는다')
    s.ch('that reports something negative', '부정적인 무언가를 보도하는')
    s.ch('about other candidates.', '다른 후보들에 대해.')
    s.natural('예를 들어 선거철에 사람들은 자신이 지지하는 후보를 긍정적으로 묘사하는 뉴스라면 무엇이든 맹목적으로 믿는 경향이 있고, 동시에 다른 후보에 대해 부정적인 내용을 보도하는 뉴스도 무의식적으로 믿는다.')
    s.cl('main', 'people', subj='people', verbs=['tend'])
    s.cl('subject_relative', 'that', verbs=['reports'], marker='that')
    s.g('During', 'during', '~ 동안')
    s.g('election|season', 'election season', '선거철')
    s.g('for|example', 'for example', '예를 들어')
    s.g('people', 'people', '사람들')
    s.g('tend|to', 'tend to V', '~하는 경향이 있다',
        verb_construction={'kind': 'to-complement', 'verb_span': s.span_of('tend'), 'lemma': 'tend',
                           'link_spans': [s.span_of('to', s.text.index('tend'))],
                           'review_record': 'people tend to blindly believe …: tend to V, V=believe(사이 부사 blindly).'})
    s.g('blindly', 'blindly', '맹목적으로')
    s.g('believe', 'believe', '믿다')
    s.g('any', 'any', '어떤 ~든')
    s.g('news', 'news', '뉴스')
    fd = s.g('describing', 'V-ing', '~하는', kind='function', combines_with=[])
    ds = s.g('describing', 'describe', '묘사하다', same=True, verb_form=pp('ing', s, 'describing', 'describe'))
    link(fd, ds)
    s.g('their', 'their', '그들의', referent_ko='사람들')
    s.g('favored', 'favored', '선호하는, 지지하는', verb_form=pp('past-participle', s, 'favored', 'favor'))
    s.g('candidates', 'candidates', '후보들')
    s.g('in', 'in', '~으로')
    s.g('positive', 'positive', '긍정적인')
    s.g('way', 'way', '방식')
    fw = s.g('while', 'while V-ing', '~하면서', kind='function', combines_with=[])
    s.g('unconsciously', 'unconsciously', '무의식적으로')
    bl = s.g('believing', 'believe', '믿다', verb_form=pp('ing', s, 'believing', 'believe'))
    link(fw, bl)
    s.g('news', 'news', '뉴스', at=s.text.index('news that'))
    rel = s.g('that', 'that V′', 'V′하는 (관계대명사)')
    s.g('reports', 'report', '보도하다', verb_form=v3(s, 'reports', 'report', '관계절 선행사 news'))
    s.g('something', 'something', '무언가')
    s.g('negative', 'negative', '부정적인')
    s.g('about', 'about', '~에 대해')
    s.g('other', 'other', '다른')
    s.g('candidates', 'candidates', '후보들', at=s.text.index('candidates.'))
    s.hint('any news [describing their favored candidates]', '[그들[사람들]이 선호하는 후보들을 묘사하는] 어떤 뉴스든',
           span='any news describing their favored candidates', label='현재분사 후치수식',
           links=[(['ing'], [('는', 1)])], refs=[('their', '그들', '[사람들]')],
           meaning='그들이 선호하는 후보들을 묘사하는 어떤 뉴스든',
           explanation='현재분사 describing이 이끄는 describing their favored candidates (in a positive way)가 앞 명사 any news를 뒤에서 꾸민다.')
    s.hint('news [that reports]', '[보도하는] 뉴스', span='news that reports', label='주격 관계대명사 that',
           links=[(['that'], ['는'])], meaning='(다른 후보들에 대해 부정적인 무언가를) 보도하는 뉴스',
           explanation='선행사 news를 주격 관계대명사 that이 받아 reports something negative about other candidates가 꾸민다. V′ reports까지만 표시.')
    s.brk('about', 'postnominal-preposition', 'about other candidates는 앞 명사구 something negative를 뒤에서 꾸미는 전치사구')
    s.relative_ids = [rel['id']]
    s.review = ('주절 people tend to blindly believe any news + 현재분사 후치수식 describing their favored candidates in a positive way(any news를 꾸밈) '
                '+ while unconsciously believing news(while + V-ing: 동시에 ~하면서, 주어 people 공유) + 주격 관계절 that reports something negative about other candidates. '
                'something negative는 -thing+단일 형용사의 최소 명사구로 비분할(L 검수 확인). about other candidates는 앞 명사구를 꾸미는 후치수식 전치사구. 힌트 2개(현재분사 후치수식, 필수 관계사). 수동 없음.')
    out.append(s)
    return out


UNIT = {
    'id': 'u3', 'source_id': 'src', 'paragraph_ids': ['p05', 'p06', 'p07'],
    'sentence_ids': [f's{n:02d}' for n in range(20, 31)],
    'today_words': [
        {'id': W['phenomenon'], 'text': 'phenomenon', 'meaning_ko': '현상'},
        {'id': W['viral'], 'text': 'go viral', 'meaning_ko': '(인터넷에서) 급속히 퍼지다'},
        {'id': W['effortlessly'], 'text': 'effortlessly', 'meaning_ko': '힘들이지 않고, 쉽게'},
        {'id': W['proof'], 'text': 'proof', 'meaning_ko': '증거'},
        {'id': W['inclined'], 'text': 'be inclined to V', 'meaning_ko': '~하는 경향이 있다'},
        {'id': W['prejudices'], 'text': 'prejudices', 'meaning_ko': '편견들'},
        {'id': W['bias'], 'text': 'confirmation bias', 'meaning_ko': '확증 편향'},
        {'id': W['selectively'], 'text': 'selectively', 'meaning_ko': '선택적으로, 골라서'},
    ],
}


def analysis(_):
    return {
        'heading_kind': '주제',
        'title_or_topic_en': 'Why Fake News Spreads So Fast',
        'title_or_topic_ko': '가짜 뉴스가 빠르게 퍼지는 이유',
        'intent_ko': '가짜 뉴스가 진짜 뉴스보다 훨씬 빨리 퍼지는 이유를 사람들의 세 가지 특성(새롭고 자극적인 것을 좋아함, 단순하게 생각함, 확증 편향)으로 설명하는 글이다.',
        'flow': [
            {'sentence_ids': ['s20', 's21'], 'label': '현상',
             'text_ko': '소셜 미디어의 가짜 뉴스는 진짜 이야기보다 훨씬 더 멀리, 빨리 퍼진다. MIT 연구에 따르면 평균 6배 빠르다.'},
            {'sentence_ids': ['s22', 's23', 's24'], 'label': '이유 1',
             'text_ko': '사람들은 새롭고 자극적인 것을 좋아한다. 놀라운 정보는 남과 나누고 싶어 하고, 아직 알려지지 않았지만 거짓일 수도 있는 정보를 가장 먼저 올린 사람은 관심을 얻을 수 있다.'},
            {'sentence_ids': ['s25', 's26'], 'label': '이유 2',
             'text_ko': '사람들은 일상에서 단순하고 쉽게 생각하는 경향이 있어서, 새로운 정보를 비판적으로 검토하지 않고 증거 없이 믿기 쉽다.'},
            {'sentence_ids': ['s27', 's28', 's29', 's30'], 'label': '이유 3',
             'text_ko': '사람들은 자신의 편견이나 경험에 맞는 정보를 믿는 확증 편향에 빠진다. 선거철에 지지 후보에게 유리한 뉴스와 다른 후보에게 불리한 뉴스를 쉽게 믿는 것이 그 예다.'},
        ],
        'easy_explanations': [
            {'sentence_id': 's24', 'explanatory_sentences': [
                '24번 문장은 23번에서 말한 ‘나누고 싶은 마음’에 이어, 소식을 나누면 무엇을 얻는지 설명한다.',
                '아직 아무도 모르는 소식을 소셜 미디어에 가장 먼저 올린 사람은 다른 사람들의 관심을 받을 수 있다.',
                '그런데 이렇게 먼저 올린 소식은 새롭기는 하지만 거짓일 수도 있다.']},
            {'sentence_id': 's26', 'explanatory_sentences': [
                '26번 문장은 25번에서 말한 ‘단순하고 쉽게 생각하는 습관’이 어떤 결과를 낳는지 보여 준다.',
                '비판적으로 검토한다는 것은 정보를 그대로 믿지 않고 사실인지 따져 보는 것이다.',
                '따져 보려면 시간과 노력이 든다.',
                '그래서 사람들은 증거가 없어도 새로운 정보를 그냥 믿어 버리기 쉽다.']},
            {'sentence_id': 's28', 'explanatory_sentences': [
                '28번 문장은 27번에서 말한 습관에 ‘확증 편향’이라는 이름을 붙인다.',
                '확증 편향은 내 생각이 맞다고 확인해 주는 정보만 믿고 싶어 하는 마음의 경향이다.',
                '글쓴이는 이것을 사람들이 쉽게 빠지는 함정이라고 부른다.',
                '29~30번 문장에서 이 함정의 뜻과 예가 이어진다.']},
        ],
        'grammar_points': [
            {'id': 'u3-gp1', 'sentence_id': 's21', 'span': 'fake news spreads online 6 times faster than real news',
             'title': 'N times + 비교급 + than A: A보다 N배 더 …하게', 'formula_key': 'N times + 비교급 + than A',
             'explanation': '공식: N times + 비교급 + than A — A보다 N배 더 …하게. N times = 6 times(6배), 비교급 = faster(더 빠르게), '
                            'A = real news(진짜 뉴스), 앞의 fake news spreads online = 가짜 뉴스가 온라인에서 퍼진다. → 가짜 뉴스는 온라인에서 진짜 뉴스보다 6배 더 빠르게 퍼진다.',
             'practice': {'span': 'fake news spreads online 6 times faster than real news',
                          'formula_support': {'en': 'N times + 비교급 + than A', 'ko': 'A보다 N배 더 …하게'},
                          'support': [('s21', 'fake news'), ('s21', 'spread'), ('s21', 'online'), ('s21', 'times'),
                                      ('s21', 'faster'), ('s21', 'than'), ('s21', 'real')],
                          'answer_ko': '가짜 뉴스는 온라인에서 진짜 뉴스보다 6배 더 빠르게 퍼진다'}},
            {'id': 'u3-gp2', 'sentence_id': 's23', 'span': 'people not only feel that it is surprising, but they also want to share the stimulating news',
             'title': 'not only A but also B: A뿐만 아니라 B도', 'formula_key': 'not only A but also B',
             'explanation': '공식: not only A but also B — A뿐만 아니라 B도. A = feel that it is surprising(그것이 놀랍다고 느끼다), '
                            'B = (they) want to share the stimulating news(그 자극적인 뉴스를 공유하고 싶어 하다). → 사람들은 그것이 놀랍다고 느낄 뿐만 아니라 그 자극적인 뉴스를 공유하고 싶어 하기도 한다. '
                            'but 뒤에 주어 they가 다시 나와 also가 동사 want 앞에 놓였다.',
             'practice': {'span': 'not only feel that it is surprising, but they also want to share the stimulating news',
                          'formula_support': {'en': 'not only A but also B', 'ko': 'A뿐만 아니라 B도'},
                          'support': [('s23', 'feel'), ('s23', 'that S′ V′'), ('s23', 'surprising'), ('s23', 'want to V'),
                                      ('s23', 'share'), ('s23', 'stimulating')],
                          'answer_ko': '그것이 놀랍다고 느낄 뿐만 아니라 그 자극적인 뉴스를 공유하고 싶어 하기도 한다'}},
            {'id': 'u3-gp3', 'sentence_id': 's24', 'span': 'they are the first to post previously unknown, but possibly false, information',
             'title': 'the first to V: 처음으로 ~하는 사람', 'formula_key': 'the first to V',
             'explanation': '공식: the first to V — 처음으로 ~하는 사람(첫 번째 사람). to V = to post(게시하다), 목적어 = previously unknown, but possibly false, information'
                            '(이전에 알려지지 않았지만 어쩌면 거짓일 수도 있는 정보). → 이전에 알려지지 않았지만 어쩌면 거짓일 수도 있는 정보를 처음으로 게시하는 사람. '
                            'to post 이하가 앞의 the first를 뒤에서 꾸민다.',
             'practice': {'span': 'the first to post previously unknown, but possibly false, information',
                          'formula_support': {'en': 'the first to V', 'ko': '처음으로 ~하는 사람'},
                          'support': [('s24', 'post'), ('s24', 'previously'), ('s24', 'unknown'), ('s24', 'possibly'),
                                      ('s24', 'false'), ('s24', 'information')],
                          'answer_ko': '이전에 알려지지 않았지만 어쩌면 거짓일 수도 있는 정보를 처음으로 게시하는 사람'}},
        ],
        'formula_routes': [
            {'function': ('s21', 'have p.p.', 0), 'route': 'hint', 'hint_index': 1,
             'review_record': 'has shown: 명사절 that 힌트 뒤 두 번째 힌트로 능동 완료 기능 결합 제공'},
        ],
        'relations': [
            {'head': {'id': 'u3-r1h', 'text': 'significantly', 'meaning_ko': '훨씬, 상당히'},
             'synonym': {'id': 'u3-r1s', 'text': 'considerably', 'meaning_ko': '상당히, 많이'},
             'antonym': {'id': 'u3-r1a', 'text': 'slightly', 'meaning_ko': '약간, 조금'}},
            {'head': {'id': 'u3-r2h', 'text': 'ignore', 'meaning_ko': '무시하다'},
             'synonym': {'id': 'u3-r2s', 'text': 'disregard', 'meaning_ko': '무시하다, 묵살하다'},
             'antonym': {'id': 'u3-r2a', 'text': 'accept', 'meaning_ko': '받아들이다'}},
            {'head': {'id': 'u3-r3h', 'text': 'negative', 'meaning_ko': '부정적인'},
             'synonym': {'id': 'u3-r3s', 'text': 'unfavorable', 'meaning_ko': '호의적이지 않은, 불리한'},
             'antonym': {'id': 'u3-r3a', 'text': 'positive', 'meaning_ko': '긍정적인'}},
        ],
    }


def workbook():
    return {
        'relation_order': ['u3-r2s', 'u3-r3a', 'u3-r1h', 'u3-r2a', 'u3-r3s', 'u3-r1s', 'u3-r2h', 'u3-r1a', 'u3-r3h'],
        'key_sentence_ids': ['s23', 's29'],
        'question_id': 'Q03',
        'syntax_point_ids': ['u3-gp1', 'u3-gp2', 'u3-gp3'],
    }
