"""공통 단위 1: 도입 단락 s01~s06 (사용자 결정: 무소제목 도입 단락을 단독 단위로 유지)."""
from author import S, link

W = {'subscription': 'u1-w1', 'delivery': 'u1-w2', 'utilize': 'u1-w3', 'login': 'u1-w4',
     'academic': 'u1-w5', 'updated': 'u1-w6', 'field': 'u1-w7', 'quality': 'u1-w8'}


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
    s.ch('Jiyun,', '지윤이는,')
    s.ch('a high school student,', '고등학생인,')
    s.ch('starts her day', '그녀의 하루를 시작한다')
    s.ch('by logging in to a music streaming service', '음악 스트리밍 서비스에 로그인함으로써')
    s.ch('on her smartphone.', '그녀의 스마트폰으로.')
    s.natural('고등학생인 지윤이는 스마트폰으로 음악 스트리밍 서비스에 로그인하며 하루를 시작한다.')
    s.cl('main', 'Jiyun', subj='Jiyun', verbs=['starts'])
    s.g('Jiyun', 'Jiyun', '지윤 (고등학생)', proper=True)
    s.g('high|school|student', 'high school student', '고등학생')
    s.g('starts', 'start', '시작하다', verb_form=v3(s, 'starts', 'start', 'Jiyun'))
    s.g('her', 'her', '그녀의', referent_ko='지윤')
    s.g('day', 'day', '하루')
    f = s.g('by', 'by V-ing', '~함으로써', kind='function', combines_with=[])
    lg = s.g('logging|in|to', 'log in to', '~에 로그인하다', star=W['login'], verb_form=pp('ing', s, 'logging', 'log'))
    link(f, lg)
    s.g('music', 'music', '음악')
    s.g('streaming', 'streaming', '스트리밍 (인터넷으로 실시간 재생하는 방식)')
    s.g('service', 'service', '서비스')
    s.g('on', 'on', '~으로 (흔한 뜻: ~위에)')
    s.g('her', 'her', '그녀의', referent_ko='지윤', at=s.text.index('her smartphone'))
    s.g('smartphone', 'smartphone', '스마트폰')
    s.hint('[by logging in]', '[로그인함으로써]', span='by logging in', label='전치사 by + 동명사',
           links=[(['by', 'ing'], ['함으로써'])],
           meaning='로그인함으로써', explanation='전치사 by + 동명사 logging in: ~함으로써(수단). 하루를 무엇으로 시작하는지 보여 준다. 대상 to a music streaming service는 표시에서 제외.')
    s.review = ('주어 Jiyun 뒤 콤마 사이 a high school student는 동격 명사구. 단일 주절(starts). by + 동명사 logging in(수단) → 힌트. '
                'log in to는 한 각주. on her smartphone은 도구(~으로). 관계사·접속사절·수동 없음.')
    out.append(s)

    # ---------------- s02 ----------------
    s = S('s02', T['s02'])
    s.ch('She enjoys listening to her favorite music,', '그녀는 그녀가 가장 좋아하는 음악을 듣는 것을 즐긴다,')
    s.ch('discovering new songs,', '새로운 노래들을 발견하는 것을,')
    s.ch('and exploring new artists', '그리고 새로운 아티스트들을 탐색하는 것을')
    s.ch('every day.', '매일.')
    s.natural('그녀는 매일 좋아하는 음악을 듣고, 새로운 노래를 발견하고, 새로운 아티스트를 찾아보는 것을 즐긴다.')
    s.cl('main', 'She', subj='She', verbs=['enjoys'])
    s.g('She', 'she', '그녀는', referent_ko='지윤')
    s.g('enjoys', 'enjoy V-ing', 'V-ing하는 것을 즐기다',
        verb_form=v3(s, 'enjoys', 'enjoy', 'She'),
        verb_construction={'kind': 'verb-frame', 'verb_span': s.span_of('enjoys'), 'lemma': 'enjoy', 'link_spans': [],
                           'review_record': 'enjoys listening …, discovering …, and exploring …: 동명사 목적어 세 개. V-ing 연결 뜻은 이 구문이 제공.'})
    s.g('listening|to', 'listen to', '~을 듣다', verb_form=pp('ing', s, 'listening', 'listen'))
    s.g('her', 'her', '그녀의', referent_ko='지윤')
    s.g('favorite', 'favorite', '가장 좋아하는')
    s.g('music', 'music', '음악')
    s.g('discovering', 'discover', '발견하다', verb_form=pp('ing', s, 'discovering', 'discover'))
    s.g('new', 'new', '새로운')
    s.g('songs', 'songs', '노래들')
    s.g('exploring', 'explore', '탐색하다, 찾아보다', verb_form=pp('ing', s, 'exploring', 'explore'))
    s.g('new', 'new', '새로운', at=s.text.index('new artists'))
    s.g('artists', 'artists', '아티스트들, 예술가들')
    s.g('every|day', 'every day', '매일')
    s.review = ('단일 주절. enjoy의 동명사 목적어 listening·discovering·exploring이 콤마와 and로 병렬(각주 enjoy V-ing로 지원). '
                '절 연결·관계사·수동 없음, 단순 병렬이라 힌트 없음.')
    out.append(s)

    # ---------------- s03 ----------------
    s = S('s03', T['s03'], key=True)
    s.ch('For a healthy breakfast,', '건강한 아침 식사를 위해,')
    s.ch('Jiyun receives a delivery', '지윤이는 배송을 받는다')
    s.ch('from a subscription service', '구독 서비스로부터')
    s.ch('that provides fresh vegetables and fruits.', '신선한 채소와 과일을 제공하는.')
    s.natural('건강한 아침 식사를 위해 지윤이는 신선한 채소와 과일을 제공하는 구독 서비스로부터 배송을 받는다.')
    s.cl('main', 'Jiyun', subj='Jiyun', verbs=['receives'])
    s.cl('subject_relative', 'that', verbs=['provides'], marker='that')
    s.g('For', 'for', '~을 위해')
    s.g('healthy', 'healthy', '건강한')
    s.g('breakfast', 'breakfast', '아침 식사')
    s.g('receives', 'receive', '받다', verb_form=v3(s, 'receives', 'receive', 'Jiyun'))
    s.g('delivery', 'delivery', '배송, 배달', star=W['delivery'])
    s.g('from', 'from', '~로부터')
    s.g('subscription', 'subscription', '구독 (정기적으로 돈을 내고 이용하는 것)', star=W['subscription'])
    s.g('service', 'service', '서비스')
    rel = s.g('that', 'that V′', 'V′하는 (관계대명사)')
    s.g('provides', 'provide', '제공하다', verb_form=v3(s, 'provides', 'provide', '관계절 선행사 a subscription service'))
    s.g('fresh', 'fresh', '신선한')
    s.g('vegetables', 'vegetables', '채소들')
    s.g('fruits', 'fruits', '과일들')
    s.hint('a subscription service [that provides]', '[제공하는] 구독 서비스', span='a subscription service that provides',
           label='주격 관계대명사 that', links=[(['that'], ['는'])],
           meaning='(신선한 채소와 과일을) 제공하는 구독 서비스',
           explanation='선행사 a subscription service를 주격 관계대명사 that이 받아 provides fresh vegetables and fruits가 꾸민다. 주격이라 V′ provides까지만 표시.')
    s.relative_ids = [rel['id']]
    s.review = ('단일 주절 + 주격 관계절 that(선행사 a subscription service) → 필수 관계사 힌트. from a subscription service는 받는 출처(receive와 연결). '
                '수동 없음.')
    out.append(s)

    # ---------------- s04 ----------------
    s = S('s04', T['s04'])
    s.ch('After school,', '방과 후에,')
    s.ch('Jiyun utilizes a video lecture service', '지윤이는 비디오 강의 서비스를 활용한다')
    s.ch('to expand her knowledge', '그녀의 지식을 넓히기 위해')
    s.ch('in whatever she finds interesting.', '그녀가 흥미롭다고 여기는 어떤 것에서든.')
    s.natural('방과 후에 지윤이는 흥미를 느끼는 것이라면 무엇이든 그에 관한 지식을 넓히기 위해 비디오 강의 서비스를 활용한다.')
    s.cl('main', 'Jiyun', subj='Jiyun', verbs=['utilizes'])
    s.cl('subordinate', 'whatever', subj='she', verbs=['finds'], marker='whatever')
    s.g('After|school', 'after school', '방과 후에')
    s.g('utilizes', 'utilize', '활용하다, 이용하다', star=W['utilize'], verb_form=v3(s, 'utilizes', 'utilize', 'Jiyun'))
    s.g('video', 'video', '비디오, 동영상')
    s.g('lecture', 'lecture', '강의')
    s.g('service', 'service', '서비스')
    f = s.g('to', 'to V', '~하기 위해', kind='function', combines_with=[])
    ex = s.g('expand', 'expand', '넓히다, 확장하다')
    link(f, ex)
    s.g('her', 'her', '그녀의', referent_ko='지윤')
    s.g('knowledge', 'knowledge', '지식')
    s.g('in', 'in', '~에서')
    s.g('whatever', 'whatever S′ V′', 'S′(이/가) V′하는 것은 무엇이든')
    s.g('she', 'she', '그녀가', referent_ko='지윤')
    s.g('finds', 'find A B', 'A를 B하다고 여기다', verb_form=v3(s, 'finds', 'find', 'she'),
        verb_construction={'kind': 'verb-frame', 'verb_span': s.span_of('finds'), 'lemma': 'find', 'link_spans': [],
                           'review_record': 'whatever she finds interesting: A=whatever(앞으로 나간 목적어), B=interesting(목적격 보어).'})
    s.g('interesting', 'interesting', '흥미로운')
    s.hint('[to expand]', '[넓히기 위해]', span='to expand', label='목적의 to부정사',
           links=[(['to'], ['기 위해'])], meaning='(그녀의 지식을) 넓히기 위해',
           explanation='to expand her knowledge …는 강의 서비스를 활용하는 목적을 나타낸다. 목적어 her knowledge는 표시에서 제외.')
    s.hint('[whatever she finds]', '[그녀[지윤]가 여기는 것은 무엇이든]', span='whatever she finds',
           label='복합관계대명사 whatever', links=[(['whatever'], ['가', '는 것은 무엇이든'])],
           refs=[('she', '그녀', '[지윤]')],
           meaning='그녀가 (흥미롭다고) 여기는 것은 무엇이든',
           explanation='전치사 in의 목적어 자리에 whatever절이 온다. whatever는 find A B의 A(목적어)이며 B는 interesting. 절 연결 표시는 S′ she, V′ finds까지로 하고 보어 interesting은 제외.')
    s.review = ('주절 utilizes + 목적 to부정사 to expand + 전치사 in의 목적어인 복합관계대명사절 whatever she finds interesting(find A B, A=whatever). '
                'whatever는 관계사 각주 목록에 넣지 않음(선행사가 없는 복합관계사, 힌트로 연결 제공). 힌트 2개(목적 to V, whatever). 수동 없음.')
    out.append(s)

    # ---------------- s05 ----------------
    s = S('s05', T['s05'], key=True)
    s.ch('For example,', '예를 들어,')
    s.ch('she watches various academic lectures', '그녀는 다양한 학술 강의들을 시청한다')
    s.ch('to review her schoolwork', '그녀의 학교 공부를 복습하기 위해')
    s.ch('and stay updated about the latest knowledge', '그리고 최신 지식에 대해 계속 새로 알기 위해')
    s.ch('in her chosen field of study.', '그녀가 선택한 학문 분야에서의.')
    s.natural('예를 들어, 그녀는 학교 공부를 복습하고 자신이 선택한 학문 분야의 최신 지식을 계속 새로 알기 위해 다양한 학술 강의를 시청한다.')
    s.cl('main', 'she', subj='she', verbs=['watches'])
    s.g('For|example', 'for example', '예를 들어')
    s.g('she', 'she', '그녀는', referent_ko='지윤')
    s.g('watches', 'watch', '시청하다, 보다', verb_form=v3(s, 'watches', 'watch', 'she'))
    s.g('various', 'various', '다양한')
    s.g('academic', 'academic', '학술적인, 학문의', star=W['academic'])
    s.g('lectures', 'lectures', '강의들')
    f = s.g('to', 'to V', '~하기 위해', kind='function', combines_with=[])
    rv = s.g('review', 'review', '복습하다 (흔한 뜻: 검토하다)')
    s.g('her', 'her', '그녀의', referent_ko='지윤')
    s.g('schoolwork', 'schoolwork', '학교 공부, 학업')
    st = s.g('stay|updated|about', 'stay updated about', '~에 대해 계속 최신 정보를 알고 있다', star=W['updated'])
    link(f, rv, st)
    s.g('latest', 'latest', '최신의')
    s.g('knowledge', 'knowledge', '지식')
    s.g('in', 'in', '~에서의')
    s.g('her', 'her', '그녀의', referent_ko='지윤', at=s.text.index('her chosen'))
    s.g('chosen', 'chosen', '선택된', verb_form=pp('past-participle', s, 'chosen', 'choose'))
    s.g('field|of|study', 'field of study', '학문 분야, 연구 분야', star=W['field'])
    s.brk('in', 'postnominal-preposition', 'in her chosen field of study는 앞 명사 the latest knowledge를 뒤에서 꾸미는 전치사구',
          after=s.text.index('knowledge'))
    s.prot('field of study', 'fixed-expression', 'field of study(학문 분야)는 한 덩어리 명사 표현이라 of 앞에서 끊지 않음')
    s.prot('stay updated about', 'fixed-expression', 'stay updated about 숙어를 끊지 않음')
    s.hint('[to review her schoolwork and stay updated]', '[그녀[지윤]의 학교 공부를 복습하고 계속 새로 알기 위해]',
           span='to review her schoolwork and stay updated', label='목적의 to부정사',
           links=[(['to'], ['기 위해'])], refs=[('her', '그녀', '[지윤]')],
           meaning='학교 공부를 복습하고 (최신 지식에 대해) 계속 새로 알기 위해',
           explanation='목적의 to 뒤에 동사원형 review와 stay가 and로 병렬되어 둘 다 to에 걸린다. stay가 to 없이 이어져 학생이 놓치기 쉬워 병렬 두 동사까지 표시하고 about 이하 대상은 제외.')
    s.review = ('단일 주절 watches + 목적 to부정사(to review … and stay updated …: 두 동사원형이 to를 공유). the latest knowledge를 in her chosen field of study가 꾸며 in 앞에서 끊음. '
                'chosen은 명사 앞 독립 과거분사, field of study는 한 덩어리 표현. 힌트 1개(목적 to V의 병렬). 수동 없음.')
    out.append(s)

    # ---------------- s06 ----------------
    s = S('s06', T['s06'])
    s.ch('During weekends,', '주말 동안,')
    s.ch('Jiyun and her family spend quality time together', '지윤이와 그녀의 가족은 함께 좋은 시간을 보낸다')
    s.ch('watching movies or dramas', '영화나 드라마를 보면서')
    s.ch('using a streaming service.', '스트리밍 서비스를 이용하여.')
    s.natural('주말에 지윤이와 가족은 스트리밍 서비스를 이용해 영화나 드라마를 보며 함께 좋은 시간을 보낸다.')
    s.cl('main', 'Jiyun', subj='Jiyun and her family', verbs=['spend'])
    s.g('During', 'during', '~ 동안')
    s.g('weekends', 'weekends', '주말들')
    s.g('her', 'her', '그녀의', referent_ko='지윤')
    s.g('family', 'family', '가족')
    s.g('spend', 'spend A V-ing', 'V-ing하면서 A(시간)를 보내다',
        verb_construction={'kind': 'verb-frame', 'verb_span': s.span_of('spend'), 'lemma': 'spend', 'link_spans': [],
                           'review_record': 'spend quality time together watching …: A=quality time, V-ing=watching. V-ing 연결 뜻은 이 구문이 제공.'})
    s.g('quality|time', 'quality time', '(함께 보내는) 좋은 시간, 소중한 시간', star=W['quality'])
    s.g('together', 'together', '함께')
    s.g('watching', 'watch', '보다', verb_form=pp('ing', s, 'watching', 'watch'))
    s.g('movies', 'movies', '영화들')
    s.g('or', 'or', '또는')
    s.g('dramas', 'dramas', '드라마들')
    f = s.g('using', 'V-ing', '~하여', kind='function', combines_with=[])
    us = s.g('using', 'use', '이용하다, 사용하다', same=True, verb_form=pp('ing', s, 'using', 'use'))
    link(f, us)
    s.g('streaming', 'streaming', '스트리밍')
    s.g('service', 'service', '서비스')
    s.hint('spend quality time together [watching]', '[보면서] 함께 좋은 시간을 보낸다', span='spend quality time together watching',
           label='spend A V-ing 구문', links=[(['spend', 'ing'], ['면서', ('을', 0)])], emphasis_policy='ko-only-verb-construction',
           meaning='(영화나 드라마를) 보면서 함께 좋은 시간을 보낸다',
           explanation='spend A V-ing: V-ing하면서 A(시간)를 보내다. A=quality time, V-ing=watching. 목적어 movies or dramas는 표시에서 제외.')
    s.hint('[using a streaming service]', '[스트리밍 서비스를 이용하여]', span='using a streaming service', label='분사구문',
           links=[(['ing'], ['하여'])], meaning='스트리밍 서비스를 이용하여',
           explanation='using a streaming service는 영화·드라마를 보는 방법(수단)을 덧붙이는 분사구. ing ↔ 하여.')
    s.review = ('등위 주어 Jiyun and her family(전체 유지) + spend A V-ing(A=quality time) + 수단의 분사구 using a streaming service. '
                '힌트 2개(spend A V-ing 동사 구문, 분사구). 관계사·수동 없음.')
    out.append(s)
    return out


UNIT = {
    'id': 'u1', 'source_id': 'src', 'paragraph_ids': ['p01'],
    'sentence_ids': ['s01', 's02', 's03', 's04', 's05', 's06'],
    'today_words': [
        {'id': W['subscription'], 'text': 'subscription', 'meaning_ko': '구독'},
        {'id': W['delivery'], 'text': 'delivery', 'meaning_ko': '배송, 배달'},
        {'id': W['utilize'], 'text': 'utilize', 'meaning_ko': '활용하다, 이용하다'},
        {'id': W['login'], 'text': 'log in to', 'meaning_ko': '~에 로그인하다'},
        {'id': W['academic'], 'text': 'academic', 'meaning_ko': '학술적인, 학문의'},
        {'id': W['updated'], 'text': 'stay updated about', 'meaning_ko': '~에 대해 계속 최신 정보를 알고 있다'},
        {'id': W['field'], 'text': 'field of study', 'meaning_ko': '학문 분야, 연구 분야'},
        {'id': W['quality'], 'text': 'quality time', 'meaning_ko': '(함께 보내는) 좋은 시간, 소중한 시간'},
    ],
}


def analysis(_):
    return {
        'heading_kind': '제목',
        'title_or_topic_en': 'A Day Full of Subscription Services',
        'title_or_topic_ko': '구독 서비스로 가득한 하루',
        'intent_ko': '고등학생 지윤이의 하루를 따라가며 음악 감상·아침 식사·공부·주말 여가까지 일상의 많은 부분이 구독 서비스로 채워져 있음을 보여 주고, 구독 경제라는 화제를 꺼내는 도입 글이다.',
        'flow': [
            {'sentence_ids': ['s01', 's02', 's03'], 'label': '아침',
             'text_ko': '지윤이는 스마트폰으로 음악 스트리밍 서비스에 로그인하며 하루를 시작하고, 아침 식사 재료도 구독 서비스로 배송받는다.'},
            {'sentence_ids': ['s04', 's05', 's06'], 'label': '방과 후와 주말',
             'text_ko': '방과 후에는 동영상 강의 서비스로 공부를 넓히고, 주말에는 가족과 스트리밍 서비스로 영화나 드라마를 본다. 하루 전체가 구독 서비스와 이어져 있다.'},
        ],
        'easy_explanations': [
            {'sentence_id': 's01', 'explanatory_sentences': [
                '1번 문장은 지윤이라는 고등학생의 하루로 글을 시작한다.',
                '스트리밍 서비스는 음악이나 영상을 내려받지 않고 인터넷으로 바로 틀어 주는 서비스다.',
                '지윤이는 아침에 눈을 뜨자마자 이 서비스에 로그인한다.',
                '글쓴이는 이 평범한 아침 모습으로 구독 서비스가 우리 생활 가까이에 있다는 것을 보여 준다.']},
            {'sentence_id': 's03', 'explanatory_sentences': [
                '3번 문장은 음악에 이어 먹는 일에서도 구독 서비스가 쓰인다는 것을 보여 준다.',
                '구독은 정해진 돈을 정기적으로 내고 물건이나 서비스를 계속 받는 방식이다.',
                '지윤이는 신선한 채소와 과일을 이런 구독 서비스로 배송받는다.',
                '장을 보러 가지 않아도 건강한 아침 식사 재료가 집으로 온다.']},
            {'sentence_id': 's05', 'explanatory_sentences': [
                '5번 문장은 4번에서 말한 강의 서비스를 지윤이가 어떻게 쓰는지 예를 든다.',
                '지윤이는 학교에서 배운 것을 복습하려고 강의를 본다.',
                '또 자기가 관심 있게 고른 분야에서 새로 나온 지식도 계속 따라잡으려고 강의를 본다.',
                '공부에도 구독 서비스가 쓰인다는 뜻이다.']},
        ],
        'grammar_points': [
            {'id': 'u1-gp1', 'sentence_id': 's01', 'span': 'starts her day by logging in to a music streaming service',
             'title': 'by + V-ing: ~함으로써', 'formula_key': 'by V-ing',
             'explanation': '공식: by + V-ing — ~함으로써. V-ing = logging in to(~에 로그인하다), 대상 = a music streaming service(음악 스트리밍 서비스). '
                            '→ 음악 스트리밍 서비스에 로그인함으로써. 앞의 starts her day(그녀의 하루를 시작한다)와 합치면 ‘로그인하는 것으로 하루를 시작한다’가 된다.',
             'practice': {'span': 'by logging in to a music streaming service',
                          'formula_support': {'en': 'by V-ing', 'ko': '~함으로써'},
                          'support': [('s01', 'log in to'), ('s01', 'music'), ('s01', 'streaming'), ('s01', 'service')],
                          'answer_ko': '음악 스트리밍 서비스에 로그인함으로써'}},
            {'id': 'u1-gp2', 'sentence_id': 's03', 'span': 'a subscription service that provides fresh vegetables and fruits',
             'title': '명사 + that V′: V′하는 명사', 'formula_key': 'N + that V′',
             'explanation': '공식: 명사(N) + that V′ — V′하는 N. 선행사 = a subscription service(구독 서비스), that = 주격 관계대명사(그 서비스가), '
                            'V′ = provides(제공하다), 목적어 = fresh vegetables and fruits(신선한 채소와 과일). '
                            '→ 신선한 채소와 과일을 제공하는 구독 서비스. that 뒤에 주어가 따로 없으므로 that이 주어 역할을 한다.',
             'practice': {'span': 'a subscription service that provides fresh vegetables and fruits',
                          'formula_support': {'en': 'N + that V′', 'ko': 'V′하는 N'},
                          'support': [('s03', 'subscription'), ('s03', 'service'), ('s03', 'provide'), ('s03', 'fresh'),
                                      ('s03', 'vegetables'), ('s03', 'fruits')],
                          'answer_ko': '신선한 채소와 과일을 제공하는 구독 서비스'}},
            {'id': 'u1-gp3', 'sentence_id': 's04', 'span': 'whatever she finds interesting',
             'title': 'whatever S′ V′: S′가 V′하는 것은 무엇이든', 'formula_key': 'whatever S′ V′',
             'explanation': '공식: whatever S′ V′ — S′(이/가) V′하는 것은 무엇이든. S′ = she(지윤), V′ = finds(여기다; find A B = A를 B하다고 여기다), '
                            'A = whatever(앞으로 나간 목적어), B = interesting(흥미로운). '
                            '→ 그녀가 흥미롭다고 여기는 것은 무엇이든. 앞의 in과 합치면 ‘그녀가 흥미를 느끼는 어떤 것에서든’이다.',
             'practice': {'span': 'whatever she finds interesting',
                          'formula_support': {'en': 'whatever S′ V′', 'ko': 'S′(이/가) V′하는 것은 무엇이든'},
                          'support': [('s04', 'she'), ('s04', 'find A B'), ('s04', 'interesting')],
                          'answer_ko': '그녀가 흥미롭다고 여기는 것은 무엇이든'}},
        ],
        'formula_routes': [],
        'relations': [
            {'head': {'id': 'u1-r1h', 'text': 'receive', 'meaning_ko': '받다'},
             'synonym': {'id': 'u1-r1s', 'text': 'obtain', 'meaning_ko': '얻다, 획득하다'},
             'antonym': {'id': 'u1-r1a', 'text': 'send', 'meaning_ko': '보내다'}},
            {'head': {'id': 'u1-r2h', 'text': 'expand', 'meaning_ko': '넓히다, 확장하다'},
             'synonym': {'id': 'u1-r2s', 'text': 'broaden', 'meaning_ko': '넓히다'},
             'antonym': {'id': 'u1-r2a', 'text': 'narrow', 'meaning_ko': '좁히다'}},
            {'head': {'id': 'u1-r3h', 'text': 'latest', 'meaning_ko': '최신의'},
             'synonym': {'id': 'u1-r3s', 'text': 'newest', 'meaning_ko': '가장 새로운'},
             'antonym': {'id': 'u1-r3a', 'text': 'outdated', 'meaning_ko': '구식의, 시대에 뒤떨어진'}},
        ],
    }


def workbook():
    return {
        'relation_order': ['u1-r2s', 'u1-r1a', 'u1-r3h', 'u1-r2a', 'u1-r1h', 'u1-r3s', 'u1-r2h', 'u1-r3a', 'u1-r1s'],
        'key_sentence_ids': ['s03', 's05'],
        'question_id': 'Q01',
        'syntax_point_ids': ['u1-gp1', 'u1-gp2', 'u1-gp3'],
    }
