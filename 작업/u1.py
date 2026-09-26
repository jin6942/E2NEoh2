"""공통 단위 1: 도입 단락 s01~s06 (사용자 결정: 무소제목 짧은 단락을 단독 단위로 유지)."""
from author import S, link


def sentences(T):
    out = []

    # ---------------- s01 ----------------
    s = S('s01', T['s01'], key=True)
    s.ch('When we think about science,', '우리가 과학에 대해 생각할 때,')
    s.ch('we might consider it as a domain', '우리는 그것을 영역으로 여길 수도 있다')
    s.ch('reserved exclusively for scientists', '오로지 과학자들을 위해 지정된')
    s.ch('in long, white lab coats', '길고 흰 실험실 가운을 입은')
    s.ch('who spend their days', '자신들의 나날을 보내는')
    s.ch('conducting experiments and analyzing data.', '실험을 하고 데이터를 분석하면서.')
    s.natural('과학에 대해 생각할 때, 우리는 그것을 실험을 하고 데이터를 분석하며 나날을 보내는, 길고 흰 실험실 가운을 입은 과학자들만을 위한 영역이라고 여길지도 모른다.')
    s.cl('subordinate', 'When', subj='we', verbs=['think'], marker='When')
    s.cl('main', 'we', subj='we', verbs=['might', 'consider'], occ=1)
    s.cl('subject_relative', 'who', verbs=['spend'], marker='who')
    s.g('When', 'when S′ V′', 'S′(이/가) V′할 때')
    s.g('we', 'we', '우리가')
    s.g('think', 'think', '생각하다')
    s.g('about', 'about', '~에 관해')
    s.g('science', 'science', '과학')
    s.g('we', 'we', '우리는')
    f = s.g('might', 'might V', '~할 수도 있다', kind='function', combines_with=[])
    c = s.g('consider|as', 'consider A as B', 'A를 B로 여기다',
            verb_construction={'kind': 'verb-frame', 'verb_span': s.span_of('consider'), 'lemma': 'consider',
                               'link_spans': [s.span_of('as')],
                               'review_record': 'consider it as a domain: A=it(과학), B=a domain. as는 B를 이끄는 고정 연결어.'})
    link(f, c)
    s.g('it', 'it', '그것을', referent_ko='과학')
    s.g('domain', 'domain', '영역, 분야', star='u1-w2')
    s.g('reserved', 'reserved', '지정된', star='u1-w3',
        verb_form={'usage': 'past-participle', 'source_span': s.span_of('reserved'), 'lemma': 'reserve'})
    s.g('exclusively', 'exclusively', '오로지, 독점적으로', star='u1-w7')
    s.g('for', 'for', '~을 위해')
    s.g('scientists', 'scientists', '과학자들')
    s.g('in', 'in', '~을 입은 (흔한 뜻: ~안에)')
    s.g('long', 'long', '긴')
    s.g('white', 'white', '흰')
    s.g('lab|coats', 'lab coats', '실험실 가운')
    who = s.g('who', 'who V′', 'V′하는 (관계대명사)')
    s.g('spend', 'spend A V-ing', 'V-ing하면서 A(시간)를 보내다',
        verb_construction={'kind': 'verb-frame', 'verb_span': s.span_of('spend'), 'lemma': 'spend',
                           'link_spans': [], 'review_record': 'spend their days conducting…and analyzing…: A=their days, V-ing=conducting/analyzing. V-ing 연결 뜻은 이 구문이 제공하므로 V-ing 기능 각주를 따로 두지 않음.'})
    s.g('their', 'their', '그들의', referent_ko='과학자들')
    s.g('days', 'days', '나날, 하루하루')
    s.g('conducting', 'conduct', '(실험 등을) 하다, 수행하다',
        verb_form={'usage': 'ing', 'source_span': s.span_of('conducting'), 'lemma': 'conduct'})
    s.g('experiments', 'experiments', '실험들')
    s.g('analyzing', 'analyze', '분석하다',
        verb_form={'usage': 'ing', 'source_span': s.span_of('analyzing'), 'lemma': 'analyze'})
    s.g('data', 'data', '데이터, 자료')
    reserved_id = s.glosses[10]['id']
    s.hint('a domain [reserved exclusively for scientists]', '[오로지 과학자들을 위해 지정된] 영역',
           span='a domain reserved exclusively for scientists', label='과거분사 후치수식',
           links=[(['reserved'], ['지정된'])], participle_focus_gloss_id=reserved_id,
           meaning='오로지 과학자들을 위해 지정된 영역',
           explanation='과거분사 reserved가 이끄는 구가 앞 명사 a domain을 뒤에서 꾸민다. 표시는 앞 명사와 분사구까지.')
    s.hint('scientists in long, white lab coats [who spend]', '[보내는] 길고 흰 실험실 가운을 입은 과학자들',
           span='scientists in long, white lab coats who spend', label='주격 관계대명사 who',
           links=[(['who'], ['는'])],
           meaning='나날을 보내는, 길고 흰 실험실 가운을 입은 과학자들',
           explanation='선행사 scientists(사람)를 주격 관계대명사 who가 받아 뒤 절 spend their days …가 꾸민다. 주격이므로 V′ spend까지만 표시하고 목적어·V-ing는 제외.')
    s.relative_ids = [who['id']]
    s.brk('in', 'postnominal-preposition', 'in long, white lab coats는 앞 명사 scientists를 뒤에서 꾸미는 전치사구', after=s.text.index('scientists'))
    s.review = ('When 부사절·주절·주격 관계절 who를 확인. reserved는 a domain을 꾸미는 독립 과거분사. '
                'in long, white lab coats는 scientists 후치수식이라 in 앞에서 끊음. consider A as B는 목적어 it을 사이에 두므로 한 청크 유지. '
                '힌트: 과거분사 후치수식(reserved)과 필수 관계사 who 두 개. When 절은 단순해 힌트 미선정. 수동·완료 기능 없음.')
    out.append(s)

    # ---------------- s02 ----------------
    s = S('s02', T['s02'])
    s.ch('They seem to have very little in common', '그들은 공통점이 거의 없는 것 같다')
    s.ch('with ordinary people', '평범한 사람들과')
    s.ch('like us.', '우리 같은.')
    s.natural('그들은 우리 같은 평범한 사람들과는 공통점이 거의 없어 보인다.')
    s.cl('main', 'They', subj='They', verbs=['seem'])
    s.g('They', 'they', '그들은', referent_ko='실험실 가운을 입은 과학자들')
    s.g('seem|to', 'seem to V', '~하는 것 같다',
        verb_construction={'kind': 'to-complement', 'verb_span': s.span_of('seem'), 'lemma': 'seem',
                           'link_spans': [s.span_of('to')], 'review_record': 'seem to have: 동사 seem의 뜻을 완성하는 to V 보충.'})
    s.g('have|little|in|common', 'have little in common', '공통점이 거의 없다')
    s.g('very', 'very', '매우')
    s.g('with', 'with', '~와')
    s.g('ordinary', 'ordinary', '평범한')
    s.g('people', 'people', '사람들')
    s.g('like', 'like', '~ 같은')
    s.g('us', 'us', '우리', referent_ko='글쓴이와 독자를 포함한 평범한 사람들')
    s.brk('like', 'postnominal-preposition', 'like us는 앞 명사 ordinary people을 뒤에서 꾸미는 전치사구')
    s.review = ('단일 주절. seem to V 보충 부정사, have little in common 숙어와 with 분리. like us는 ordinary people을 꾸미는 전치사구이나 뜻이 쉬워 청크로만 구분. '
                '관계사·접속사절·수동 없음 → 힌트 없음. very는 little을 꾸며 숙어 사이에 끼어 있음.')
    out.append(s)

    # ---------------- s03 ----------------
    s = S('s03', T['s03'])
    s.ch('However,', '그러나,')
    s.ch('this perception is far from the truth.', '이러한 인식은 사실과 거리가 멀다.')
    s.natural('그러나 이러한 인식은 사실과 거리가 멀다.')
    s.cl('main', 'this', subj='this perception', verbs=['is'])
    s.g('However', 'however', '그러나')
    s.g('this', 'this', '이러한')
    s.g('perception', 'perception', '인식', star='u1-w1')
    s.g('is|far|from', 'be far from', '~와 거리가 멀다, 결코 ~이 아니다')
    s.g('truth', 'truth', '사실, 진실')
    s.review = '단일 주절, be far from 숙어(실제 be 있음). this는 perception을 꾸미는 한정사. 구조 힌트 불필요, 수동 없음.'
    out.append(s)

    # ---------------- s04 ----------------
    s = S('s04', T['s04'])
    s.ch('In reality,', '사실은,')
    s.ch('science belongs to everyone,', '과학은 모든 사람의 것이다,')
    s.ch('and we all have the ability', '그리고 우리 모두는 능력을 가지고 있다')
    s.ch('to play a role in the advancement', '발전에서 역할을 할')
    s.ch('of science.', '과학의.')
    s.natural('사실은 과학은 모든 사람의 것이며, 우리 모두는 과학의 발전에 한몫할 수 있는 능력을 가지고 있다.')
    s.cl('main', 'science', subj='science', verbs=['belongs'])
    s.cl('main', 'we', subj='we all', verbs=['have'], marker='and')
    s.g('In|reality', 'in reality', '사실은, 실제로는')
    s.g('science', 'science', '과학')
    s.g('belongs|to', 'belong to', '~의 것이다, ~에 속하다', star='u1-w5',
        verb_form={'usage': 'third-person-singular', 'source_span': s.span_of('belongs'), 'lemma': 'belong',
                   'review_record': '주어 science(3인칭 단수)의 일반동사 belongs → 원형 belong.'})
    s.g('everyone', 'everyone', '모든 사람')
    s.g('we', 'we', '우리')
    s.g('all', 'all', '모두')
    s.g('have', 'have', '가지고 있다')
    s.g('ability', 'ability', '능력')
    f = s.g('to', 'to V', '~할', kind='function', combines_with=[])
    p = s.g('play|role|in', 'play a role in', '~에서 역할을 하다, ~에 한몫하다', star='u1-w8')
    link(f, p)
    s.g('advancement', 'advancement', '발전, 진보')
    s.g('of', 'of', '~의')
    s.g('science', 'science', '과학', at=s.text.index('of science') + 3)
    s.hint('the ability [to play]', '[할] 능력', span='the ability to play a role in the advancement',
           label='to부정사 후치수식', links=[(['to'], ['할'])],
           meaning='과학의 발전에서 역할을 할 능력',
           explanation='to play a role in …이 앞 명사 the ability를 뒤에서 꾸며 ‘~할 능력’. 표시는 명사와 to V까지로 한 초점만 보임.')
    s.brk('of', 'postnominal-preposition', 'of science는 앞 명사 the advancement를 뒤에서 꾸미는 전치사구', after=s.text.index('advancement'))
    s.prot('play a role in', 'fixed-expression', 'play a role in 숙어를 끊지 않음')
    s.review = ('두 독립 주절(and). we all의 all은 주어 we와 함께 표시. to play a role in은 ability를 꾸미는 to부정사(형용사적 용법) → 힌트. '
                'play a role in 숙어라서 in the advancement까지 한 청크, of science는 후치수식이라 of 앞에서 끊음. 수동·완료 없음.')
    out.append(s)

    # ---------------- s05 ----------------
    s = S('s05', T['s05'], key=True)
    s.ch('There have been numerous citizen science projects', '수많은 시민 과학 프로젝트들이 있어 왔다')
    s.ch('in which ordinary people have made contributions', '평범한 사람들이 기여를 해 온')
    s.ch('to remarkable scientific accomplishments.', '놀라운 과학적 업적들에.')
    s.natural('평범한 사람들이 놀라운 과학적 업적에 기여해 온 수많은 시민 과학 프로젝트들이 있었다.')
    s.cl('main', 'There', subj='numerous citizen science projects in which ordinary people have made contributions to remarkable scientific accomplishments',
         disp='numerous citizen science projects', disp_review='관계절 in which … 은 뒤수식이라 S 표시는 한정어+중심명사까지(전체 주어는 subject_spans에 보존)',
         verbs=[], vfirst=['have', 'been'])
    s.cl('subordinate', 'in', subj='ordinary people', verbs=['have', 'made'], marker='in which')
    f1 = s.g('have', 'have p.p.', '~해 왔다', kind='function', combines_with=[])
    b = s.g('been', 'be', '있다 (been은 be의 p.p.형)',
            verb_form={'usage': 'perfect-participle', 'source_span': s.span_of('been'), 'lemma': 'be',
                       'function_gloss_id': f1['id']})
    link(f1, b)
    s.g('numerous', 'numerous', '수많은')
    s.g('citizen|science', 'citizen science', '시민 과학 (일반 시민이 참여하는 과학 연구)')
    s.g('projects', 'projects', '프로젝트들, 연구 과제들')
    rel = s.g('in|which', 'in which S′ V′', 'S′(이/가) V′하는 (관계대명사)')
    s.g('ordinary', 'ordinary', '평범한')
    s.g('people', 'people', '사람들')
    f2 = s.g('have', 'have p.p.', '~해 왔다', kind='function', combines_with=[])
    m = s.g('made', 'make', '하다 (흔한 뜻: 만들다) (made는 make의 p.p.형)',
            verb_form={'usage': 'perfect-participle', 'source_span': s.span_of('made'), 'lemma': 'make',
                       'function_gloss_id': f2['id']})
    link(f2, m)
    s.g('contributions', 'contributions', '기여, 공헌', star='u1-w4')
    s.g('to', 'to', '~에')
    s.g('remarkable', 'remarkable', '놀라운, 주목할 만한')
    s.g('scientific', 'scientific', '과학적인')
    s.g('accomplishments', 'accomplishments', '업적들, 성과들', star='u1-w6')
    s.extra_cov[tuple(s.span_of('There'))] = {'exemption': 'below-middle1-unneeded', 'level': 'below-middle1',
        'reason': '유도부사 there(초등 기초어)는 따로 해석하지 않으며 뒤 be 각주의 ‘있다’로 뜻을 지원'}
    s.hint('projects [in which ordinary people have made]', '[평범한 사람들이 해 온] 프로젝트들',
           span='projects in which ordinary people have made', label='전치사+관계대명사 in which',
           links=[(['in which'], ['이', '온'])],
           meaning='평범한 사람들이 (기여를) 해 온 프로젝트들',
           explanation='선행사 projects를 in which가 받는다(그 프로젝트들 안에서). 뒤 절 S′ ordinary people, V′ have made까지만 표시하고 목적어 contributions 이하는 제외.')
    s.relative_ids = [rel['id']]
    s.review = ('유도부사 There + have been: 주어는 numerous citizen science projects(There는 S 아님). in which 관계절은 필수 관계사 힌트. '
                '능동 완료 have been / have made 두 개: 이미 관계사 힌트가 있어 기능 결합 힌트는 추가하지 않고 같은 단위 분석(have p.p. 보충)에 연결. '
                'in which 각주는 통일 틀 S′(이/가) V′하는 적용 가능(평범한 사람들이 기여해 온 프로젝트).')
    out.append(s)

    # ---------------- s06 ----------------
    s = S('s06', T['s06'])
    s.ch('Let’s take a look at two of them.', '그것들 중 두 개를 살펴보자.')
    s.natural('그중 두 가지를 살펴보자.')
    s.cl('imperative', 'Let', verbs=['Let'])
    s.g('Let’s', 'Let’s V', '~하자')
    s.g('take|look|at', 'take a look at', '~을 살펴보다')
    s.g('two|of', 'two of', '~ 중 두 개')
    s.g('them', 'them', '그것들', referent_ko='시민 과학 프로젝트들')
    s.review = 'Let’s V 권유 명령문(주어 없음). ’s는 us의 축약이며 동사 칸은 Let만. 숙어 take a look at을 가르지 않도록 한 청크. two of them은 ~중 두 개. 힌트 불필요.'
    out.append(s)
    return out


UNIT = {
    'id': 'u1', 'source_id': 'src', 'paragraph_ids': ['p01'],
    'sentence_ids': ['s01', 's02', 's03', 's04', 's05', 's06'],
    'today_words': [
        {'id': 'u1-w1', 'text': 'perception', 'meaning_ko': '인식', 'source_gloss_id': None},
        {'id': 'u1-w2', 'text': 'domain', 'meaning_ko': '영역, 분야', 'source_gloss_id': None},
        {'id': 'u1-w3', 'text': 'reserved', 'meaning_ko': '지정된', 'source_gloss_id': None},
        {'id': 'u1-w4', 'text': 'contributions', 'meaning_ko': '기여, 공헌', 'source_gloss_id': None},
        {'id': 'u1-w5', 'text': 'belong to', 'meaning_ko': '~의 것이다, ~에 속하다', 'source_gloss_id': None},
        {'id': 'u1-w6', 'text': 'accomplishments', 'meaning_ko': '업적들, 성과들', 'source_gloss_id': None},
        {'id': 'u1-w7', 'text': 'exclusively', 'meaning_ko': '오로지, 독점적으로', 'source_gloss_id': None},
        {'id': 'u1-w8', 'text': 'play a role in', 'meaning_ko': '~에서 역할을 하다, ~에 한몫하다', 'source_gloss_id': None},
    ],
}


def analysis(ids):
    """ids: 각주 ID 조회 함수 (문장ID, 표제어, n번째) → id"""
    return {
        'heading_kind': '주제',
        'title_or_topic_en': 'Science Is Not Only for Scientists',
        'title_or_topic_ko': '과학은 과학자만의 것이 아니다',
        'intent_ko': '과학이 흰 가운을 입은 과학자들만의 영역이라는 생각은 틀렸고, 누구나 과학 발전에 한몫할 수 있다는 점을 밝히며 시민 과학 프로젝트 두 가지를 소개하려는 글이다.',
        'flow': [
            {'sentence_ids': ['s01', 's02'], 'label': '도입',
             'text_ko': '과학은 실험실 가운을 입은 과학자들만의 영역이고, 그런 과학자들은 우리 같은 보통 사람과 공통점이 거의 없다는 흔한 생각을 먼저 보여 준다.'},
            {'sentence_ids': ['s03', 's04'], 'label': '반박',
             'text_ko': 'However로 방향을 바꿔 그 생각이 틀렸다고 말하고, 과학은 모두의 것이며 누구나 과학 발전에 한몫할 수 있다는 중심 생각을 밝힌다.'},
            {'sentence_ids': ['s05', 's06'], 'label': '예고',
             'text_ko': '보통 사람들이 큰 업적에 힘을 보탠 시민 과학 프로젝트가 많았다는 근거를 들고, 그중 두 가지를 살펴보자고 한다.'},
        ],
        'easy_explanations': [
            {'sentence_id': 's01', 'explanatory_sentences': [
                '1번 문장은 많은 사람이 과학을 어떻게 떠올리는지 보여 주며 글을 시작한다.',
                '흔히 과학은 흰 가운을 입고 하루 종일 실험하고 자료를 분석하는 사람들이 하는 일이라고 생각한다.',
                '그래서 과학은 그런 전문가들만 들어갈 수 있는 곳처럼 느껴진다.',
                '글쓴이는 이 흔한 생각을 먼저 꺼내 놓고, 뒤에서 그 생각을 뒤집는다.']},
            {'sentence_id': 's04', 'explanatory_sentences': [
                '3번 문장의 However(그러나)에 이어, 4번 문장은 글쓴이의 진짜 생각을 밝힌다.',
                '과학은 과학자만의 것이 아니라 모든 사람의 것이다.',
                '‘과학의 발전에 한몫한다’는 말은 새로운 사실을 알아내는 일에 보통 사람도 힘을 보탤 수 있다는 뜻이다.',
                '이 문장이 글 전체의 중심 생각이다.']},
            {'sentence_id': 's05', 'explanatory_sentences': [
                '5번 문장은 4번의 주장이 실제로 가능하다는 근거를 든다.',
                '시민 과학은 과학자가 아닌 일반 시민이 참여하는 과학 연구를 말한다.',
                '이런 프로젝트에서 보통 사람들이 놀라운 과학 성과에 힘을 보탠 일이 이미 많았다.',
                '그래서 6번 문장에서 그 가운데 두 가지를 살펴보자고 한다.']},
        ],
        'grammar_points': [
            {'id': 'u1-gp1', 'sentence_id': 's01', 'span': 'spend their days conducting experiments and analyzing data',
             'title': 'spend + A + V-ing: V-ing하면서 A(시간)를 보내다', 'formula_key': 'spend A V-ing',
             'explanation': '공식: spend + A + V-ing — V-ing하면서 A(시간)를 보내다. '
                            'A = their days(그들의 나날), V-ing = conducting(하다)·analyzing(분석하다), 각 V-ing의 목적어 = experiments(실험을)·data(데이터를). '
                            '→ 실험을 하고 데이터를 분석하면서 그들의 나날을 보내다.',
             'practice': {'span': 'spend their days conducting experiments',
                          'formula_support': {'en': 'spend A V-ing', 'ko': 'V-ing하면서 A(시간)를 보내다'},
                          'support': [('s01', 'their'), ('s01', 'days'), ('s01', 'conduct'), ('s01', 'experiments')],
                          'answer_ko': '실험을 하면서 그들의 나날을 보내다'}},
            {'id': 'u1-gp2', 'sentence_id': 's04', 'span': 'the ability to play a role in the advancement of science',
             'title': '명사 + to V: ~할 명사', 'formula_key': 'N + to V',
             'explanation': '공식: 명사(N) + to V — ~할 N. N = the ability(능력), to V = to play a role in(~에서 역할을 하다), in의 대상 = the advancement of science(과학의 발전). '
                            '→ 과학의 발전에서 역할을 할 능력. to부정사가 앞 명사 ability를 뒤에서 꾸며 어떤 능력인지 알려 준다.',
             'practice': {'span': 'the ability to play a role in the advancement',
                          'formula_support': {'en': 'N + to V', 'ko': '~할 N'},
                          'support': [('s04', 'ability'), ('s04', 'play a role in'), ('s04', 'advancement')],
                          'answer_ko': '발전에서 역할을 할 능력'}},
            {'id': 'u1-gp3', 'sentence_id': 's05', 'span': 'projects in which ordinary people have made contributions to remarkable scientific accomplishments',
             'title': '명사 + in which S′ V′: S′가 V′하는 명사', 'formula_key': 'in which S′ V′',
             'explanation': '공식: 명사 + in which S′ V′ — S′(이/가) V′하는 명사. 선행사 = projects(프로젝트들), in which = 그 프로젝트들 안에서, '
                            'S′ = ordinary people(평범한 사람들), V′ = have made(해 왔다), 목적어 = contributions(기여). '
                            '→ 평범한 사람들이 기여를 해 온 프로젝트들. 전치사 in이 관계대명사 which 앞에 붙어 ‘그 프로젝트 안에서’라는 관계를 나타낸다.',
             'practice': {'span': 'projects in which ordinary people have made contributions',
                          'formula_support': {'en': 'in which S′ V′', 'ko': 'S′(이/가) V′하는'},
                          'support': [('s05', 'projects'), ('s05', 'ordinary'), ('s05', 'people'), ('s05', 'have p.p.', 1),
                                      ('s05', 'make'), ('s05', 'contributions')],
                          'answer_ko': '평범한 사람들이 기여를 해 온 프로젝트들'}},
            {'id': 'u1-gp4', 'sentence_id': 's05', 'span': 'There have been numerous citizen science projects',
             'title': 'have p.p.: ~해 왔다 (There have been ~: ~이 있어 왔다)', 'formula_key': 'have p.p.',
             'explanation': '공식: have p.p. — ~해 왔다. p.p. = been(be의 p.p.형, 있다), 주어 = numerous citizen science projects(수많은 시민 과학 프로젝트들). '
                            'There는 따로 해석하지 않는다. → 수많은 시민 과학 프로젝트들이 있어 왔다. 과거부터 지금까지 이어진 일임을 나타낸다.',
             'supplemental': {'function': ('s05', 'have p.p.', 0),
                              'reason': 's05의 능동 완료 have been·have made는 관계사 힌트가 이미 있어 결합 힌트로 선정하지 않았고, 기본 분석 3개에 have p.p. 설명이 없어 이 단위 대표 사례로 1회 보충'},
             'practice': {'span': 'There have been numerous citizen science projects',
                          'formula_support': {'en': 'have p.p.', 'ko': '~해 왔다'},
                          'support': [('s05', 'be'), ('s05', 'numerous'), ('s05', 'citizen science'), ('s05', 'projects')],
                          'answer_ko': '수많은 시민 과학 프로젝트들이 있어 왔다'}},
        ],
        'formula_routes': [
            {'function': ('s05', 'have p.p.', 0), 'route': 'analysis', 'grammar_point_id': 'u1-gp4',
             'review_record': 'There have been: 관계사 힌트가 있는 문장이라 분석 보충 u1-gp4로 연결'},
            {'function': ('s05', 'have p.p.', 1), 'route': 'analysis', 'grammar_point_id': 'u1-gp4',
             'review_record': 'have made: 같은 공식 have p.p.의 단위 대표 u1-gp4로 연결'},
        ],
        'relations': [
            {'head': {'id': 'u1-r1h', 'text': 'remarkable', 'meaning_ko': '놀라운, 주목할 만한'},
             'synonym': {'id': 'u1-r1s', 'text': 'extraordinary', 'meaning_ko': '비범한, 놀라운'},
             'antonym': {'id': 'u1-r1a', 'text': 'ordinary', 'meaning_ko': '평범한'}},
            {'head': {'id': 'u1-r2h', 'text': 'numerous', 'meaning_ko': '수많은'},
             'synonym': {'id': 'u1-r2s', 'text': 'countless', 'meaning_ko': '셀 수 없이 많은'},
             'antonym': {'id': 'u1-r2a', 'text': 'few', 'meaning_ko': '거의 없는, 소수의'}},
            {'head': {'id': 'u1-r3h', 'text': 'advancement', 'meaning_ko': '발전, 진보'},
             'synonym': {'id': 'u1-r3s', 'text': 'progress', 'meaning_ko': '진보, 발전'},
             'antonym': {'id': 'u1-r3a', 'text': 'decline', 'meaning_ko': '쇠퇴, 감소'}},
        ],
    }


def workbook():
    return {
        'relation_order': ['u1-r2s', 'u1-r1a', 'u1-r3h', 'u1-r2a', 'u1-r1h', 'u1-r3s', 'u1-r2h', 'u1-r3a', 'u1-r1s'],
        'key_sentence_ids': ['s01', 's05'],
        'question_id': 'Q01',
        'syntax_point_ids': ['u1-gp1', 'u1-gp2', 'u1-gp3', 'u1-gp4'],
    }
