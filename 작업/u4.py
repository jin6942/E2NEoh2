"""공통 단위 4: 결론 단락 s56~s60 (사용자 결정: 무소제목 짧은 단락을 단독 단위로 유지)."""
from author import S, link
from u2 import pp

W = {'involved': 'u4-w1', 'degrees': 'u4-w2', 'desire': 'u4-w3', 'capable': 'u4-w4',
     'individuals': 'u4-w5', 'curiosity': 'u4-w6', 'achievement': 'u4-w7', 'volunteer': 'u4-w8'}


def sentences(T):
    out = []

    # ---------------- s56 ----------------
    s = S('s56', T['s56'])
    s.ch('Most of the individuals', '개인들 중 대부분은')
    s.ch('involved in these two projects', '이 두 프로젝트에 참여한')
    s.ch('are not professional scientists.', '전문 과학자가 아니다.')
    s.natural('이 두 프로젝트에 참여한 사람들 대부분은 전문 과학자가 아니다.')
    s.cl('main', 'Most', subj='Most of the individuals involved in these two projects', verbs=['are'])
    s.g('Most|of', 'most of', '~ 중 대부분')
    s.g('individuals', 'individuals', '개인들, 사람들', star=W['individuals'])
    iv = s.g('involved|in', 'involved in', '(~에) 참여한', star=W['involved'],
             verb_form=pp('past-participle', s, 'involved', 'involve'))
    s.g('these', 'these', '이')
    s.g('two', 'two', '두')
    s.g('projects', 'projects', '프로젝트들')
    s.g('are', 'are', '~이다')
    s.g('not', 'not', '~이 아닌')
    s.g('professional', 'professional', '전문적인, 직업적인')
    s.g('scientists', 'scientists', '과학자들')
    s.hint('the individuals [involved in these two projects]', '[이 두 프로젝트에 참여한] 개인들',
           span='the individuals involved in these two projects', label='과거분사 후치수식',
           links=[(['involved'], ['참여한'])], participle_focus_gloss_id=iv['id'],
           meaning='이 두 프로젝트에 참여한 개인들',
           explanation='과거분사 involved가 이끄는 involved in these two projects가 앞 명사 the individuals를 뒤에서 꾸민다.')
    s.review = ('주어 Most of the individuals involved in these two projects는 부분 표현이라 S 표시에서 줄이지 않고 전체 유지. '
                'involved in … 과거분사 후치수식 → 힌트. 수동 없음.')
    out.append(s)

    # ---------------- s57 ----------------
    s = S('s57', T['s57'])
    s.ch('Instead,', '대신,')
    s.ch('they are citizen scientists —', '그들은 시민 과학자들이다 —')
    s.ch('ordinary people', '평범한 사람들')
    s.ch('who desire to help advance science', '과학을 발전시키는 것을 돕기를 바라는')
    s.ch('in areas', '분야들에서')
    s.ch('that they are interested in.', '그들이 관심 있는.')
    s.natural('대신, 그들은 시민 과학자들인데, 그들은 자신이 관심 있는 분야에서 과학의 발전을 돕고자 하는 평범한 사람들이다.')
    s.cl('main', 'they', subj='they', verbs=['are'])
    s.cl('subject_relative', 'who', verbs=['desire'], marker='who')
    s.cl('subordinate', 'that', subj='they', verbs=['are'], marker='that')
    s.g('Instead', 'instead', '대신')
    s.g('they', 'they', '그들은', referent_ko='이 두 프로젝트에 참여한 대부분의 사람들')
    s.g('are', 'are', '~이다')
    s.g('citizen|scientists', 'citizen scientists', '시민 과학자들')
    s.g('ordinary', 'ordinary', '평범한')
    s.g('people', 'people', '사람들')
    rel1 = s.g('who', 'who V′', 'V′하는 (관계대명사)')
    s.g('desire|to', 'desire to V', '~하기를 바라다', star=W['desire'],
        verb_construction={'kind': 'to-complement', 'verb_span': s.span_of('desire'), 'lemma': 'desire',
                           'link_spans': [s.span_of('to')], 'review_record': 'desire to help: desire의 목적어 to V.'})
    s.g('help', 'help V', '~하는 것을 돕다',
        verb_construction={'kind': 'verb-frame', 'verb_span': s.span_of('help'), 'lemma': 'help', 'link_spans': [],
                           'review_record': 'help advance science: help 뒤 원형부정사 advance.'})
    s.g('advance', 'advance', '발전시키다')
    s.g('science', 'science', '과학')
    s.g('in', 'in', '~에서')
    s.g('areas', 'areas', '분야들')
    rel2 = s.g('that', 'that S′ V′', 'S′(이/가) V′하는 (관계대명사)')
    s.g('they', 'they', '그들이', referent_ko='시민 과학자들', at=s.text.index('they are interested'))
    s.g('are|interested|in', 'be interested in', '~에 관심이 있다', at=s.text.index('are interested'))
    s.hint('ordinary people [who desire]', '[바라는] 평범한 사람들', span='ordinary people who desire',
           label='주격 관계대명사 who', links=[(['who'], ['는'])], meaning='(과학의 발전을 돕기를) 바라는 평범한 사람들',
           explanation='ordinary people을 주격 관계대명사 who가 받아 desire to help advance science …가 꾸민다. V′ desire까지만 표시.')
    s.hint('areas [that they are interested in]', '[그들[시민 과학자들]이 관심 있는] 분야들',
           span='areas that they are interested in', label='목적격 관계대명사 that',
           links=[(['that'], ['이', '는'])], refs=[('they', '그들', '[시민 과학자들]')],
           meaning='그들이 관심 있는 분야들',
           explanation='areas를 목적격 관계대명사 that이 받고, be interested in의 전치사 in이 관계절 끝에 남는다(in areas → interested in areas). S′ they, V′ are interested in까지 표시.')
    s.relative_ids = [rel1['id'], rel2['id']]
    s.review = ('주절 they are citizen scientists + 대시 뒤 동격 명사구 ordinary people + 주격 관계절 who + 목적격 관계절 that(전치사 in이 절 끝에 남음). '
                '필수 관계사 힌트 2개. help V(원형부정사). 수동 없음.')
    out.append(s)

    # ---------------- s58 ----------------
    s = S('s58', T['s58'], key=True)
    s.ch('Even though citizen scientists may not have science degrees', '비록 시민 과학자들이 과학 학위를 가지고 있지 않을 수도 있지만')
    s.ch('or long, white lab coats,', '또는 길고 흰 실험실 가운을,')
    s.ch('they are still capable of making valuable contributions', '그들은 여전히 귀중한 기여를 할 수 있다')
    s.ch('to science.', '과학에.')
    s.natural('시민 과학자들에게 과학 학위나 길고 흰 실험실 가운은 없을 수도 있지만, 그들은 여전히 과학에 귀중한 기여를 할 수 있다.')
    s.cl('subordinate', 'Even', subj='citizen scientists', verbs=['may not have'], marker='Even though')
    s.cl('main', 'they', subj='they', verbs=['are'])
    s.g('Even|though', 'even though S′ V′', '비록 S′(이/가) V′하지만')
    s.g('citizen|scientists', 'citizen scientists', '시민 과학자들')
    f = s.g('may|not', 'may not V', '~하지 않을 수도 있다', kind='function', combines_with=[])
    hv = s.g('have', 'have', '가지고 있다')
    link(f, hv)
    s.g('science|degrees', 'science degrees', '과학 학위', star=W['degrees'])
    s.g('or', 'or', '또는')
    s.g('long', 'long', '긴')
    s.g('white', 'white', '흰')
    s.g('lab|coats', 'lab coats', '실험실 가운')
    s.g('they', 'they', '그들은', referent_ko='시민 과학자들')
    s.g('are|capable|of', 'be capable of V-ing', '~할 수 있다', star=W['capable'])
    s.g('still', 'still', '여전히')
    s.glosses.sort(key=lambda g: g['spans'][0][0])
    s.g('making', 'make', '하다 (흔한 뜻: 만들다)', verb_form=pp('ing', s, 'making', 'make'), at=s.text.index('making'))
    s.g('valuable', 'valuable', '귀중한, 가치 있는')
    s.g('contributions', 'contributions', '기여, 공헌')
    s.g('to', 'to', '~에')
    s.g('science', 'science', '과학', at=s.text.index('to science') + 3)
    s.hint('[Even though citizen scientists may not have]', '[비록 시민 과학자들이 가지고 있지 않을 수도 있지만]',
           span='Even though citizen scientists may not have', label='양보 접속사 even though',
           links=[(['Even though'], ['비록', '이', '지만'])], meaning='비록 시민 과학자들이 (과학 학위나 가운을) 가지고 있지 않을 수도 있지만',
           explanation='even though S′ V′: 비록 S′가 V′하지만(양보). S′ citizen scientists, V′ may not have까지 표시하고 목적어 science degrees 이하 제외. 부정·양태 may not 보존.')
    s.review = ('양보 부사절 even though + 주절 be capable of V-ing(able과 of 이하는 V 칸에 넣지 않음). '
                '힌트 1개(양보절). be capable of는 각주로 지원. 수동 없음.')
    out.append(s)

    # ---------------- s59 ----------------
    s = S('s59', T['s59'])
    s.ch('You can become one as well', '여러분도 그런 사람이 될 수 있다')
    s.ch('if you have curiosity and an interest', '만약 여러분이 호기심과 관심을 가지고 있다면')
    s.ch('in taking part in scientific research.', '과학 연구에 참여하는 것에 대한.')
    s.natural('호기심과, 과학 연구에 참여하는 것에 대한 관심이 있다면 여러분도 시민 과학자가 될 수 있다.')
    s.cl('main', 'You', subj='You', verbs=['can', 'become'])
    s.cl('subordinate', 'if', subj='you', verbs=['have'], marker='if')
    f = s.g('can', 'can V', '~할 수 있다', kind='function', combines_with=[])
    bc = s.g('become', 'become', '~이 되다')
    link(f, bc)
    s.g('one', 'one', '(그런) 사람 하나', referent_ko='시민 과학자')
    s.g('as|well', 'as well', '~도, 또한')
    s.g('if', 'if S′ V′', 'S′(이/가) V′한다면')
    s.g('have', 'have', '가지고 있다')
    s.g('curiosity', 'curiosity', '호기심', star=W['curiosity'])
    s.g('interest', 'interest', '관심')
    s.g('in', 'in', '~에 대한', at=s.text.index('in taking'))
    f2 = s.g('taking', 'V-ing', '~하는 것', kind='function', combines_with=[])
    tk = s.g('taking|part|in', 'take part in', '~에 참여하다', same=True, verb_form=pp('ing', s, 'taking', 'take'))
    link(f2, tk)
    s.g('scientific', 'scientific', '과학적인')
    s.g('research', 'research', '연구')
    s.brk('in', 'postnominal-preposition', 'in taking part …는 앞 명사 an interest를 꾸미는 전치사구', after=s.text.index('interest'))
    s.hint('an interest [in taking part]', '[참여하는 것에 대한] 관심', span='an interest in taking part',
           label='전치사+동명사 후치수식', links=[([('in', 1)], ['에 대한']), (['ing'], ['는 것'])],
           meaning='(과학 연구에) 참여하는 것에 대한 관심',
           explanation='전치사 in + 동명사 taking part …가 앞 명사 an interest를 뒤에서 꾸민다. 동명사 ing ↔ 는 것, 전치사 in ↔ 에 대한.')
    s.review = ('주절 can become + 조건절 if. one은 앞의 a citizen scientist를 대신함. an interest in taking part in … 전치사구 후치수식(동명사) → 힌트. '
                'if절은 단순해 각주로 지원. 수동 없음.')
    out.append(s)

    # ---------------- s60 ----------------
    s = S('s60', T['s60'], key=True)
    s.ch('The next great scientific achievement could be made', '다음의 위대한 과학적 업적은 이루어질 수도 있다')
    s.ch('by citizen scientists', '시민 과학자들에 의해')
    s.ch('volunteering their time', '자신들의 시간을 자발적으로 내는')
    s.ch('for the purpose of better understanding the world.', '세상을 더 잘 이해하기 위한 목적으로.')
    s.natural('다음의 위대한 과학적 업적은 세상을 더 잘 이해하기 위해 자신의 시간을 자발적으로 내는 시민 과학자들에 의해 이루어질 수도 있다.')
    s.cl('main', 'The', subj='The next great scientific achievement', verbs=['could be made'])
    s.g('next', 'next', '다음의')
    s.g('great', 'great', '위대한')
    s.g('scientific', 'scientific', '과학적인')
    s.g('achievement', 'achievement', '업적, 성취', star=W['achievement'])
    f = s.g('could|be', 'could be p.p.', '~될 수도 있다', kind='function', combines_with=[])
    md = s.g('made', 'made', '이루어진 (흔한 뜻: 만들어진)', verb_form=pp('passive-participle', s, 'made', 'make', f['id']))
    link(f, md)
    s.g('by', 'by', '~에 의해')
    s.g('citizen|scientists', 'citizen scientists', '시민 과학자들')
    f2 = s.g('volunteering', 'V-ing', '~하는', kind='function', combines_with=[])
    vl = s.g('volunteering', 'volunteer', '(시간·노력을) 자발적으로 내다', same=True, star=W['volunteer'],
             verb_form=pp('ing', s, 'volunteering', 'volunteer'))
    link(f2, vl)
    s.g('their', 'their', '그들의', referent_ko='시민 과학자들')
    s.g('time', 'time', '시간')
    s.g('for|purpose|of', 'for the purpose of V-ing', '~하기 위한 목적으로')
    s.g('better', 'better', '더 잘 (well의 비교급)')
    s.g('understanding', 'understand', '이해하다', verb_form=pp('ing', s, 'understanding', 'understand'))
    s.g('world', 'world', '세상')
    s.brk('by', 'passive-agent-by', '수동 could be made의 행위자(누구에 의해)를 나타내는 by 구')
    s.prot('for the purpose of', 'fixed-expression', 'for the purpose of V-ing 숙어를 끊지 않음')
    s.hint('citizen scientists [volunteering]', '[자발적으로 내는] 시민 과학자들', span='citizen scientists volunteering',
           label='현재분사 후치수식', links=[(['ing'], ['는'])], meaning='(자신의 시간을) 자발적으로 내는 시민 과학자들',
           explanation='현재분사 volunteering이 이끄는 구가 앞 명사 citizen scientists를 뒤에서 꾸민다. 목적어 their time 이하는 표시에서 제외.')
    s.vf_hint(fn=f, lex=md, en='could be made', ko='이루어질 수도 있다', formula='could be p.p.', step_form='made', step_ko='이루어진',
              en_mark=['could be'], ko_mark=['질 수도 있다'], span='The next great scientific achievement could be made',
              meaning='이루어질 수도 있다',
              explanation='조동사 수동 could be made: ~될 수도 있다(가능성). 글의 결론의 핵심 동사라 후순위 기능 결합으로 선정. 주어·by 구 제외.')
    s.review = ('주절 조동사 수동 could be made + 행위자 by 구(by 앞에서 끊음) + volunteering 현재분사 후치수식 + for the purpose of V-ing. '
                '힌트 2개(현재분사 후치수식, 조동사 수동 기능 결합).')
    out.append(s)
    return out


UNIT = {
    'id': 'u4', 'source_id': 'src', 'paragraph_ids': ['p10'],
    'sentence_ids': ['s56', 's57', 's58', 's59', 's60'],
    'today_words': [
        {'id': W['involved'], 'text': 'involved in', 'meaning_ko': '~에 참여한'},
        {'id': W['degrees'], 'text': 'science degrees', 'meaning_ko': '과학 학위'},
        {'id': W['desire'], 'text': 'desire to V', 'meaning_ko': '~하기를 바라다'},
        {'id': W['capable'], 'text': 'be capable of', 'meaning_ko': '~할 수 있다'},
        {'id': W['individuals'], 'text': 'individuals', 'meaning_ko': '개인들, 사람들'},
        {'id': W['curiosity'], 'text': 'curiosity', 'meaning_ko': '호기심'},
        {'id': W['achievement'], 'text': 'achievement', 'meaning_ko': '업적, 성취'},
        {'id': W['volunteer'], 'text': 'volunteer', 'meaning_ko': '(시간·노력을) 자발적으로 내다'},
    ],
}


def analysis(_):
    return {
        'heading_kind': '주제',
        'title_or_topic_en': 'Anyone Can Become a Citizen Scientist',
        'title_or_topic_ko': '누구나 시민 과학자가 될 수 있다',
        'intent_ko': '두 프로젝트의 참여자 대부분이 전문가가 아닌 시민 과학자라는 점을 정리하고, 호기심과 관심만 있으면 누구나 과학에 기여할 수 있다고 독자의 참여를 권하는 글이다.',
        'flow': [
            {'sentence_ids': ['s56', 's57'], 'label': '정리',
             'text_ko': '두 프로젝트에 참여한 사람들 대부분은 전문 과학자가 아니라, 관심 분야에서 과학 발전을 돕고 싶어 하는 평범한 시민 과학자라고 정리한다.'},
            {'sentence_ids': ['s58', 's59', 's60'], 'label': '주장과 권유',
             'text_ko': '과학 학위나 흰 가운이 없어도 시민 과학자는 과학에 귀중한 기여를 할 수 있다며 글 처음의 ‘흰 가운’ 생각을 다시 뒤집는다. 호기심과 관심만 있으면 독자도 시민 과학자가 될 수 있고, 다음 위대한 업적은 시민 과학자들이 이룰 수도 있다며 참여를 권한다.'},
        ],
        'easy_explanations': [
            {'sentence_id': 's57', 'explanatory_sentences': [
                '57번 문장은 56번에서 말한 참여자들이 어떤 사람들인지 알려 준다.',
                '그들은 전문 과학자가 아니라 시민 과학자다.',
                '시민 과학자는 직업은 달라도 자기가 좋아하는 분야에서 과학을 돕고 싶어 하는 보통 사람이다.',
                '은하 사진을 분류한 사람들과 오로라 사진을 찍은 사람들이 바로 그런 예다.']},
            {'sentence_id': 's58', 'explanatory_sentences': [
                '58번 문장은 글 맨 처음에 나온 ‘흰 가운을 입은 과학자’ 모습을 다시 꺼낸다.',
                '시민 과학자에게는 과학 학위도, 흰 가운도 없을 수 있다.',
                '그래도 과학에 도움이 되는 일을 충분히 할 수 있다.',
                '글 처음의 흔한 생각이 틀렸다는 것을 이 문장에서 확실히 정리한다.']},
            {'sentence_id': 's60', 'explanatory_sentences': [
                '60번 문장은 글 전체를 마무리하며 앞으로의 가능성을 말한다.',
                '다음에 나올 위대한 과학적 업적은 시민 과학자들이 이룰 수도 있다.',
                '시민 과학자들은 돈을 받지 않고 자기 시간을 내어 참여한다.',
                '그 이유는 세상을 더 잘 이해하고 싶기 때문이다.',
                '‘할 수도 있다(could)’라고 했으므로 꼭 그렇게 된다는 뜻은 아니다.']},
        ],
        'grammar_points': [
            {'id': 'u4-gp1', 'sentence_id': 's57', 'span': 'areas that they are interested in',
             'title': '명사 + that S′ V′ … 전치사: S′가 V′하는 명사 (전치사가 절 끝에 남음)', 'formula_key': 'N + that S′ V′ + 전치사',
             'explanation': '공식: 명사 + that S′ V′ + 전치사 — S′(이/가) V′하는 명사. 선행사 = areas(분야들), S′ = they(시민 과학자들), '
                            'V′ = are interested in(~에 관심이 있다). 원래 they are interested in areas에서 areas가 앞으로 나가고 전치사 in이 끝에 남았다. '
                            '→ 그들이 관심 있는 분야들.',
             'practice': {'span': 'areas that they are interested in',
                          'formula_support': {'en': 'N + that S′ V′ + 전치사', 'ko': 'S′(이/가) V′하는 N'},
                          'support': [('s57', 'areas'), ('s57', 'they', 1), ('s57', 'be interested in')],
                          'answer_ko': '그들이 관심 있는 분야들'}},
            {'id': 'u4-gp2', 'sentence_id': 's58', 'span': 'Even though citizen scientists may not have science degrees or long, white lab coats',
             'title': 'even though S′ V′: 비록 S′가 V′하지만', 'formula_key': 'even though S′ V′',
             'explanation': '공식: even though S′ V′ — 비록 S′(이/가) V′하지만. S′ = citizen scientists(시민 과학자들), V′ = may not have(가지고 있지 않을 수도 있다), '
                            '목적어 = science degrees or long, white lab coats(과학 학위나 길고 흰 실험실 가운). '
                            '→ 비록 시민 과학자들이 과학 학위나 길고 흰 실험실 가운을 가지고 있지 않을 수도 있지만. 뒤 주절(그래도 기여할 수 있다)과 반대되는 내용이다.',
             'practice': {'span': 'Even though citizen scientists may not have science degrees',
                          'formula_support': {'en': 'even though S′ V′', 'ko': '비록 S′(이/가) V′하지만'},
                          'support': [('s58', 'citizen scientists'), ('s58', 'may not V'), ('s58', 'have'), ('s58', 'science degrees')],
                          'answer_ko': '비록 시민 과학자들이 과학 학위를 가지고 있지 않을 수도 있지만'}},
            {'id': 'u4-gp3', 'sentence_id': 's60', 'span': 'citizen scientists volunteering their time',
             'title': '명사 + V-ing: ~하는 명사 (현재분사 후치수식)', 'formula_key': 'N + V-ing',
             'explanation': '공식: 명사(N) + V-ing — ~하는 N. N = citizen scientists(시민 과학자들), V-ing = volunteering their time(자신들의 시간을 자발적으로 내다). '
                            '→ 자신들의 시간을 자발적으로 내는 시민 과학자들.',
             'practice': {'span': 'citizen scientists volunteering their time',
                          'formula_support': {'en': 'N + V-ing', 'ko': '~하는 N'},
                          'support': [('s60', 'citizen scientists'), ('s60', 'volunteer'), ('s60', 'their'), ('s60', 'time')],
                          'answer_ko': '자신들의 시간을 자발적으로 내는 시민 과학자들'}},
        ],
        'formula_routes': [
            {'function': ('s60', 'could be p.p.', 0), 'route': 'hint', 'hint_index': 1,
             'review_record': 'could be made: 조동사 수동 기능 결합 힌트'},
        ],
        'relations': [
            {'head': {'id': 'u4-r1h', 'text': 'valuable', 'meaning_ko': '귀중한, 가치 있는'},
             'synonym': {'id': 'u4-r1s', 'text': 'precious', 'meaning_ko': '소중한, 귀중한'},
             'antonym': {'id': 'u4-r1a', 'text': 'worthless', 'meaning_ko': '가치 없는'}},
            {'head': {'id': 'u4-r2h', 'text': 'professional', 'meaning_ko': '전문적인, 직업적인'},
             'synonym': {'id': 'u4-r2s', 'text': 'expert', 'meaning_ko': '전문가의, 숙련된'},
             'antonym': {'id': 'u4-r2a', 'text': 'amateur', 'meaning_ko': '아마추어의, 비전문가의'}},
            {'head': {'id': 'u4-r3h', 'text': 'advance', 'meaning_ko': '발전시키다'},
             'synonym': {'id': 'u4-r3s', 'text': 'promote', 'meaning_ko': '촉진하다, 발전시키다'},
             'antonym': {'id': 'u4-r3a', 'text': 'hinder', 'meaning_ko': '방해하다'}},
        ],
    }


def workbook():
    return {
        'relation_order': ['u4-r2s', 'u4-r1a', 'u4-r3h', 'u4-r2a', 'u4-r1h', 'u4-r3s', 'u4-r2h', 'u4-r3a', 'u4-r1s'],
        'key_sentence_ids': ['s58', 's60'],
        'question_id': 'Q04',
        'syntax_point_ids': ['u4-gp1', 'u4-gp2', 'u4-gp3'],
    }
