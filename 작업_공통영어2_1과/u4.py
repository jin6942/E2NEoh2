"""공통 단위 4: Ways to Spot and Avoid Fake News (s31~s47, 단락 p08~p10; 짧은 단락이 있어 소제목 전체 묶음)."""
from author import S, link
from u1 import pp, v3

W = {'mislead': 'u4-w1', 'face_value': 'u4-w2', 'critical': 'u4-w3', 'evaluate': 'u4-w4',
     'biases': 'u4-w5', 'credibility': 'u4-w6', 'intent': 'u4-w7', 'eliminate': 'u4-w8'}
READER = '[독자]'


def sentences(T):
    out = []

    # ---------------- s31 ----------------
    s = S('s31', T['s31'])
    s.ch('With so much information', '그렇게 많은 정보가 있는 상황에서')
    s.ch('on the Internet,', '인터넷에,')
    s.ch('how can you make sure', '어떻게 당신은 확실히 할 수 있을까')
    s.ch('that fake news does not mislead you?', '가짜 뉴스가 당신을 속이지 않는다는 것을?')
    s.natural('인터넷에 그렇게 많은 정보가 있는데, 어떻게 가짜 뉴스에 속지 않을 수 있을까?')
    s.cl('main', 'how', subj='you', vfirst=['can'], verbs=['make'])
    s.cl('subordinate', 'that', subj='fake news', verbs=['does', 'not', 'mislead'], marker='that')
    s.g('With', 'with', '~이 있는 상황에서 (흔한 뜻: ~와 함께)')
    s.g('so|much', 'so much', '그렇게 많은')
    s.g('information', 'information', '정보')
    s.g('on', 'on', '~에')
    s.g('Internet', 'Internet', '인터넷')
    s.g('how', 'how', '어떻게')
    fc = s.g('can', 'can V', '~할 수 있다', kind='function', combines_with=[])
    ms = s.g('make|sure', 'make sure', '확실히 하다')
    link(fc, ms)
    s.g('that', 'that S′ V′', 'S′(이/가) V′한다는 것을 (접속사)')
    s.g('fake|news', 'fake news', '가짜 뉴스')
    fd = s.g('does|not', 'does not V', '~하지 않다', kind='function', combines_with=[])
    ml = s.g('mislead', 'mislead', '속이다, 오도하다', star=W['mislead'])
    link(fd, ml)
    s.hint('[With so much information on the Internet]', '[인터넷에 그렇게 많은 정보가 있는 상황에서]',
           span='With so much information on the Internet', label='with 구문',
           links=[(['With'], ['가', '있는 상황에서'])], meaning='인터넷에 그렇게 많은 정보가 있는 상황에서',
           explanation='with + A + 전치사구(A가 ~에 있는 상황에서): A=so much information, 전치사구=on the Internet. 질문의 배경 상황.')
    s.hint('[that fake news does not mislead]', '[가짜 뉴스가 속이지 않는다는 것]', span='that fake news does not mislead',
           label='명사절 접속사 that', links=[(['that'], [('가', 1), '다는 것'])], meaning='가짜 뉴스가 (당신을) 속이지 않는다는 것',
           explanation='make sure의 목적어 that 명사절(S′ fake news, V′ does not mislead). 부정 does not을 보존하고 목적어 you는 표시에서 제외.')
    s.review = ('직접의문문: 의문사 how + 조동사 can + 주어 you + make sure(확실히 하다) + 목적어 that 명사절 fake news does not mislead you. '
                '문두 With so much information on the Internet는 with + A + 전치사구(A가 ~에 있는 상황에서). on 앞 경계는 with 구문 안 A와 전치사구 사이. 힌트 2개(with 구문, 명사절 that). 관계사·수동 없음.')
    out.append(s)

    # ---------------- s32 ----------------
    s = S('s32', T['s32'])
    s.ch('First,', '첫째,')
    s.ch('read beyond the provocative headlines.', '자극적인 헤드라인들을 넘어서 읽어라.')
    s.natural('첫째, 자극적인 헤드라인에서 멈추지 말고 그 너머까지 읽어라.')
    s.cl('imperative', 'read', verbs=['read'])
    s.g('First', 'first', '첫째')
    s.g('read', 'read', '읽다')
    s.g('beyond', 'beyond', '~을 넘어서')
    s.g('provocative', 'provocative', '자극적인')
    s.g('headlines', 'headlines', '헤드라인들, 제목들')
    s.review = '주어 없는 명령문 read beyond …(V만 표시). 관계사·접속사절·수동 없음 → 힌트 없음.'
    out.append(s)

    # ---------------- s33 ----------------
    s = S('s33', T['s33'], key=True)
    s.ch('They can be so stimulating', '그것들은 너무 자극적일 수 있다')
    s.ch('to get more clicks', '더 많은 클릭 수를 얻기 위해')
    s.ch('that you may click on them accidentally.', '그래서 당신은 뜻하지 않게 그것들을 클릭할 수도 있다.')
    s.natural('헤드라인은 클릭 수를 늘리려고 너무 자극적으로 만들어져서 당신이 무심코 클릭하게 될 수도 있다.')
    s.cl('main', 'They', subj='They', verbs=['can', 'be'])
    s.cl('subordinate', 'that', subj='you', verbs=['may', 'click'], marker='that')
    s.g('They', 'they', '그것들은', referent_ko='자극적인 헤드라인들')
    fc = s.g('can', 'can V', '~할 수 있다', kind='function', combines_with=[])
    be = s.g('be', 'be', '~이다')
    link(fc, be)
    s.g('so|that', 'so A that S′ V′', '너무 A해서 S′(이/가) V′하다')
    s.glosses.sort(key=lambda g: g['spans'][0][0])
    s.g('stimulating', 'stimulating', '자극적인', at=s.text.index('stimulating'))
    ft = s.g('to', 'to V', '~하기 위해', kind='function', combines_with=[])
    gt = s.g('get', 'get', '얻다')
    link(ft, gt)
    s.g('more', 'more', '더 많은')
    s.g('clicks', 'clicks', '클릭 수, 클릭들')
    fm = s.g('may', 'may V', '~할 수도 있다', kind='function', combines_with=[])
    ck = s.g('click|on', 'click on', '~을 클릭하다')
    link(fm, ck)
    s.g('them', 'them', '그것들을', referent_ko='자극적인 헤드라인들')
    s.g('accidentally', 'accidentally', '뜻하지 않게, 무심코')
    s.hint('so stimulating … that you may click', '너무 자극적이어서 … 당신[독자]이 클릭할 수도 있다',
           span='so stimulating to get more clicks that you may click', category='paired-structure',
           display_spans=[s.span_of('so stimulating'), s.span_of('that you may click')],
           links=[(['so', 'that'], ['너무', '어서', ('이', 1)])], refs=[('you', '당신', READER)],
           meaning='너무 자극적이어서 당신이 클릭할 수도 있다',
           explanation='so A that S′ V′(너무 A해서 S′(이/가) V′하다): A=stimulating, 결과 that절 S′ you, V′ may click. 사이의 to get more clicks와 뒤 on them accidentally는 제외.')
    s.review = ('주절 They can be so stimulating(They=앞 문장의 자극적인 헤드라인들) + 목적 to get more clicks + 결과 that절 you may click on them accidentally(so A that). '
                '힌트 1개(so … that 짝 구조; 목적 to get은 짝 구조 표시 범위 안이라 포함 힌트 합치기 원칙으로 별도 힌트 없이 각주로 지원). 관계사·수동 없음.')
    out.append(s)

    # ---------------- s34 ----------------
    s = S('s34', T['s34'])
    s.ch('So don’t just read the headlines,', '그러므로 그저 헤드라인만 읽지 말고,')
    s.ch('but read the text carefully.', '본문을 주의 깊게 읽어라.')
    s.natural('그러므로 헤드라인만 읽지 말고 본문을 주의 깊게 읽어라.')
    s.cl('imperative', 'don’t', verbs=['don’t', 'read'])
    s.cl('imperative', 'read', verbs=['read'], marker='but', occ=1)
    s.g('So', 'so', '그러므로')
    s.g('don’t|just|but', 'don’t just A but B', '그저 A하지 말고 B하라')
    s.g('read', 'read', '읽다')
    s.g('headlines', 'headlines', '헤드라인들, 제목들')
    s.glosses.sort(key=lambda g: g['spans'][0][0])
    s.g('read', 'read', '읽다', at=s.text.index('read the text'))
    s.g('text', 'text', '본문 (흔한 뜻: 글, 문자)')
    s.g('carefully', 'carefully', '주의 깊게')
    s.hint('don’t just read … but read', '그저 읽지 말고 … 읽어라', span='don’t just read the headlines, but read',
           category='paired-structure', display_spans=[s.span_of('don’t just read'), s.span_of('but read')],
           links=[(['don’t just', 'but'], ['그저', '지 말고'])],
           meaning='그저 (헤드라인만) 읽지 말고 (본문을) 읽어라',
           explanation='not just A but B(그저 A만 하지 말고 B하라): 부정 명령문 don’t just read the headlines와 명령문 read the text carefully가 but으로 짝을 이룬다. 목적어는 표시에서 제외.')
    s.review = ('주어 없는 명령문 두 개(don’t just read …, but read …)가 but으로 이어짐: not just A but B. 힌트 1개(짝 구조). 관계사·접속사절·수동 없음.')
    out.append(s)

    # ---------------- s35 ----------------
    s = S('s35', T['s35'])
    s.ch('Second,', '둘째,')
    s.ch('don’t read the news at face value.', '뉴스를 액면 그대로 읽지 마라.')
    s.natural('둘째, 뉴스를 곧이곧대로 받아들이지 마라.')
    s.cl('imperative', 'don’t', verbs=['don’t', 'read'])
    s.g('Second', 'second', '둘째')
    fd = s.g('don’t', 'do not V', '~하지 마라', kind='function', combines_with=[])
    rd = s.g('read', 'read', '읽다')
    link(fd, rd)
    s.g('news', 'news', '뉴스')
    s.g('at|face|value', 'at face value', '액면 그대로, 곧이곧대로', star=W['face_value'])
    s.review = '주어 없는 부정 명령문 don’t read … at face value(숙어 각주). 관계사·접속사절·수동 없음 → 힌트 없음.'
    out.append(s)

    # ---------------- s36 ----------------
    s = S('s36', T['s36'])
    s.ch('Exercise critical thinking skills', '비판적 사고 기술을 발휘하라')
    s.ch('to judge the news.', '뉴스를 판단하기 위해.')
    s.natural('뉴스를 판단하기 위해 비판적 사고 능력을 발휘하라.')
    s.cl('imperative', 'Exercise', verbs=['Exercise'])
    s.g('Exercise', 'exercise', '발휘하다, 활용하다 (흔한 뜻: 운동하다)')
    s.g('critical|thinking', 'critical thinking', '비판적 사고', star=W['critical'])
    s.g('skills', 'skills', '기술들, 능력들')
    ft = s.g('to', 'to V', '~하기 위해', kind='function', combines_with=[])
    jd = s.g('judge', 'judge', '판단하다')
    link(ft, jd)
    s.g('news', 'news', '뉴스')
    s.hint('[to judge]', '[판단하기 위해]', span='to judge', label='목적의 to부정사', links=[(['to'], ['기 위해'])],
           meaning='(뉴스를) 판단하기 위해', explanation='to judge the news는 비판적 사고 기술을 발휘하는 목적. 목적어 the news는 표시에서 제외.')
    s.review = '주어 없는 명령문 Exercise … + 목적 to judge the news. 힌트 1개(목적 to V). 관계사·수동 없음.'
    out.append(s)

    # ---------------- s37 ----------------
    s = S('s37', T['s37'], key=False)
    s.ch('You should question, analyze, and evaluate', '당신은 의문을 제기하고, 분석하고, 평가해야 한다')
    s.ch('what you read.', '당신이 읽는 것을.')
    s.natural('당신은 자신이 읽는 것에 대해 질문하고, 분석하고, 평가해야 한다.')
    s.cl('main', 'You', subj='You', verbs=['should', 'question', 'analyze', 'and', 'evaluate'])
    s.cl('subordinate', 'what', subj='you', verbs=['read'], marker='what')
    fs = s.g('should', 'should V', '~해야 한다', kind='function', combines_with=[])
    q1 = s.g('question', 'question', '의문을 제기하다 (흔한 뜻: 질문)')
    q2 = s.g('analyze', 'analyze', '분석하다')
    q3 = s.g('evaluate', 'evaluate', '평가하다', star=W['evaluate'])
    link(fs, q1, q2, q3)
    rel = s.g('what', 'what S′ V′', 'S′(이/가) V′하는 것 (관계대명사)')
    s.g('read', 'read', '읽다')
    s.hint('[what you read]', '[당신[독자]이 읽는 것]', span='what you read', label='관계대명사 what',
           links=[(['what'], ['이', '는 것'])], refs=[('you', '당신', READER)], meaning='당신이 읽는 것',
           explanation='what은 선행사를 포함한 관계대명사(~하는 것). 절 what you read 전체가 question, analyze, evaluate의 공통 목적어.')
    s.relative_ids = [rel['id']]
    s.review = ('주절 You should question, analyze, and evaluate(조동사 should가 병렬 동사 셋을 이끎) + 공통 목적어인 관계대명사 what절 what you read. '
                '힌트 1개(필수 관계사 what). 수동 없음.')
    out.append(s)

    # ---------------- s38 ----------------
    s = S('s38', T['s38'])
    s.ch('Third,', '셋째,')
    s.ch('examine your biases.', '당신의 편견들을 점검하라.')
    s.natural('셋째, 자신의 편견을 점검하라.')
    s.cl('imperative', 'examine', verbs=['examine'])
    s.g('Third', 'third', '셋째')
    s.g('examine', 'examine', '점검하다, 살펴보다')
    s.g('your', 'your', '당신의')
    s.g('biases', 'biases', '편견들', star=W['biases'])
    s.review = '주어 없는 명령문 examine your biases. 관계사·접속사절·수동 없음 → 힌트 없음.'
    out.append(s)

    # ---------------- s39 ----------------
    s = S('s39', T['s39'])
    s.ch('Consider', '고려하라')
    s.ch('if your own beliefs could affect your judgment.', '당신 자신의 믿음이 당신의 판단에 영향을 미칠 수 있는지.')
    s.natural('자신의 믿음이 판단에 영향을 줄 수 있는지 생각해 보라.')
    s.cl('imperative', 'Consider', verbs=['Consider'])
    s.cl('subordinate', 'if', subj='your own beliefs', verbs=['could', 'affect'], marker='if')
    s.g('Consider', 'consider', '고려하다, 생각해 보다')
    s.g('if', 'if S′ V′', 'S′(이/가) V′하는지 (접속사)')
    s.g('your', 'your', '당신의')
    s.g('own', 'own', '자신의')
    s.g('beliefs', 'beliefs', '믿음들, 신념들')
    fc = s.g('could', 'could V', '~할 수 있다', kind='function', combines_with=[])
    af = s.g('affect', 'affect', '~에 영향을 미치다')
    link(fc, af)
    s.g('your', 'your', '당신의', at=s.text.index('your judgment'))
    s.g('judgment', 'judgment', '판단')
    s.hint('[if your own beliefs could affect]', '[당신[독자] 자신의 믿음이 영향을 미칠 수 있는지]',
           span='if your own beliefs could affect', label='명사절 접속사 if',
           links=[(['if'], ['이', '는지'])], refs=[('your', '당신', READER)],
           meaning='당신 자신의 믿음이 (당신의 판단에) 영향을 미칠 수 있는지',
           explanation='Consider의 목적어인 if 명사절(~인지; S′ your own beliefs, V′ could affect). 목적어 your judgment는 표시에서 제외.')
    s.review = '주어 없는 명령문 Consider + 목적어 if 명사절(~인지) your own beliefs could affect your judgment. 힌트 1개(명사절 if). 관계사·수동 없음.'
    out.append(s)

    # ---------------- s40 ----------------
    s = S('s40', T['s40'])
    s.ch('Ask yourself', '당신 자신에게 물어보라')
    s.ch('if you are only reading articles', '당신이 오직 기사들만 읽고 있는지')
    s.ch('that suit your opinion,', '당신의 의견에 맞는,')
    s.ch('and look for articles', '그리고 기사들을 찾아라')
    s.ch('that oppose your opinion', '당신의 의견에 반대되는')
    s.ch('as well.', '또한.')
    s.natural('자신의 의견에 맞는 기사만 읽고 있는 것은 아닌지 스스로에게 물어보고, 자신의 의견에 반대되는 기사도 찾아보라.')
    s.cl('imperative', 'Ask', verbs=['Ask'])
    s.cl('subordinate', 'if', subj='you', verbs=['are', 'reading'], marker='if')
    s.cl('subject_relative', 'that', verbs=['suit'], marker='that')
    s.cl('imperative', 'look', verbs=['look'], marker='and')
    s.cl('subject_relative', 'that', verbs=['oppose'], marker='that', occ=1)
    s.g('Ask', 'ask', '묻다')
    s.g('yourself', 'yourself', '당신 자신에게')
    s.g('if', 'if S′ V′', 'S′(이/가) V′하는지 (접속사)')
    fb = s.g('are', 'be V-ing', '~하고 있다', kind='function', combines_with=[])
    s.g('only', 'only', '오직, ~만')
    rd = s.g('reading', 'read', '읽다', verb_form=pp('ing', s, 'reading', 'read'))
    link(fb, rd)
    s.g('articles', 'articles', '기사들')
    r1 = s.g('that', 'that V′', 'V′하는 (관계대명사)')
    s.g('suit', 'suit', '~에 맞다, 어울리다')
    s.g('your', 'your', '당신의')
    s.g('opinion', 'opinion', '의견')
    s.g('look|for', 'look for', '~을 찾다')
    s.g('articles', 'articles', '기사들', at=s.text.index('articles that oppose'))
    r2 = s.g('that', 'that V′', 'V′하는 (관계대명사)')
    s.g('oppose', 'oppose', '~에 반대되다, 반대하다')
    s.g('your', 'your', '당신의', at=s.text.index('your opinion as'))
    s.g('opinion', 'opinion', '의견', at=s.text.index('opinion as'))
    s.g('as|well', 'as well', '또한, ~도')
    s.hint('articles [that suit]', '[맞는] 기사들', span='articles that suit', label='주격 관계대명사 that',
           links=[(['that'], ['는'])], meaning='(당신의 의견에) 맞는 기사들',
           explanation='선행사 articles를 주격 관계대명사 that이 받아 suit your opinion이 꾸민다. V′ suit까지만 표시.')
    s.hint('articles [that oppose]', '[반대되는] 기사들', span='articles that oppose', label='주격 관계대명사 that',
           links=[(['that'], ['는'])], meaning='(당신의 의견에) 반대되는 기사들',
           explanation='선행사 articles를 주격 관계대명사 that이 받아 oppose your opinion이 꾸민다. V′ oppose까지만 표시.')
    s.relative_ids = [r1['id'], r2['id']]
    s.review = ('명령문 Ask yourself + 목적어 if 명사절 you are only reading articles(현재진행) + 주격 관계절 that suit your opinion, [and] 명령문 look for articles + 주격 관계절 that oppose your opinion as well. '
                '힌트 2개(필수 관계사 둘). if 명사절은 각주로 지원(문장당 최대 2개). 수동 없음.')
    out.append(s)

    # ---------------- s41 ----------------
    s = S('s41', T['s41'])
    s.ch('Finally,', '마지막으로,')
    s.ch('check the credibility', '신뢰성을 확인하라')
    s.ch('of the source.', '출처의.')
    s.natural('마지막으로, 출처가 믿을 만한지 확인하라.')
    s.cl('imperative', 'check', verbs=['check'])
    s.g('Finally', 'finally', '마지막으로')
    s.g('check', 'check', '확인하다')
    s.g('credibility', 'credibility', '신뢰성', star=W['credibility'])
    s.g('of', 'of', '~의')
    s.g('source', 'source', '출처 (흔한 뜻: 원천)')
    s.brk('of', 'postnominal-preposition', 'of the source는 앞 명사 the credibility를 뒤에서 꾸미는 전치사구')
    s.review = '주어 없는 명령문 check the credibility of the source. of 앞 후치수식 경계. 관계사·접속사절·수동 없음 → 힌트 없음.'
    out.append(s)

    # ---------------- s42 ----------------
    s = S('s42', T['s42'])
    s.ch('You should examine', '당신은 살펴보아야 한다')
    s.ch('who wrote the news story', '누가 그 뉴스 기사를 썼는지')
    s.ch('and what the intent was', '그리고 의도가 무엇이었는지')
    s.ch('behind writing the news story.', '그 뉴스 기사를 쓴 것 뒤에 있는.')
    s.natural('당신은 누가 그 뉴스 기사를 썼는지, 그리고 그 기사를 쓴 이면의 의도가 무엇이었는지 살펴보아야 한다.')
    s.cl('main', 'You', subj='You', verbs=['should', 'examine'])
    s.cl('subject_relative', 'who', verbs=['wrote'], marker='who')
    s.cl('subordinate', 'what', subj='the intent', verbs=['was'], marker='what')
    fs = s.g('should', 'should V', '~해야 한다', kind='function', combines_with=[])
    ex = s.g('examine', 'examine', '살펴보다, 조사하다')
    link(fs, ex)
    s.g('who', 'who V′', '누가 V′했는지')
    s.g('wrote', 'wrote', '썼다 (write의 과거)', verb_form=pp('irregular-past', s, 'wrote', 'write'))
    s.g('news|story', 'news story', '뉴스 기사')
    s.g('what', 'what S′ V′', 'S′(이/가) 무엇이었는지')
    s.g('intent', 'intent', '의도', star=W['intent'])
    s.g('was', 'was', '~였다')
    s.g('behind', 'behind', '~ 뒤에 있는')
    fw = s.g('writing', 'V-ing', '~하는 것', kind='function', combines_with=[])
    wr = s.g('writing', 'write', '쓰다', same=True, verb_form=pp('ing', s, 'writing', 'write'))
    link(fw, wr)
    s.g('news|story', 'news story', '뉴스 기사', at=s.text.index('news story.'))
    s.hint('[who wrote]', '[누가 썼는지]', span='who wrote', label='간접의문문 who',
           links=[(['who'], ['누가', '는지'])], meaning='누가 (그 뉴스 기사를) 썼는지',
           explanation='examine의 첫째 목적어인 간접의문문. 의문사 who 자체가 주어이고 V′는 wrote. 목적어 the news story는 제외.')
    s.hint('[what the intent was]', '[의도가 무엇이었는지]', span='what the intent was', label='간접의문문 what',
           links=[(['what'], ['가', '무엇', '는지'])], meaning='(그 기사를 쓴 이면의) 의도가 무엇이었는지',
           explanation='examine의 둘째 목적어인 간접의문문(S′ the intent, V′ was, what은 보어). 뒤의 behind writing the news story는 intent를 꾸미는 말로 표시에서 제외.')
    s.review = ('주절 You should examine + 목적어 간접의문문 둘(and로 병렬): who wrote the news story(who가 주어라 S/V는 V′만 표시, 관계절 아님), '
                'what the intent was behind writing the news story(what은 보어, behind + 동명사 writing). 힌트 2개(간접의문문 who·what). 관계사·수동 없음.')
    out.append(s)

    # ---------------- s43 ----------------
    s = S('s43', T['s43'])
    s.ch('You also need to check', '당신은 또한 확인할 필요가 있다')
    s.ch('whether the news story is from a reliable media source', '그 뉴스 기사가 믿을 만한 미디어 출처에서 나온 것인지')
    s.ch('and the evidence is valid.', '그리고 증거가 타당한지.')
    s.natural('또한 그 뉴스 기사가 믿을 만한 언론 출처에서 나온 것인지, 그리고 증거가 타당한지 확인해야 한다.')
    s.cl('main', 'You', subj='You', verbs=['need'])
    s.cl('subordinate', 'whether', subj='the news story', verbs=['is'], marker='whether')
    s.cl('subordinate', 'and', subj='the evidence', verbs=['is'], marker='and')
    s.g('also', 'also', '또한')
    s.g('need|to', 'need to V', '~할 필요가 있다',
        verb_construction={'kind': 'to-complement', 'verb_span': s.span_of('need'), 'lemma': 'need',
                           'link_spans': [s.span_of('to')],
                           'review_record': 'You also need to check …: need to V, V=check.'})
    s.g('check', 'check', '확인하다')
    s.g('whether', 'whether S′ V′', 'S′(이/가) V′하는지')
    s.g('news|story', 'news story', '뉴스 기사')
    s.g('is', 'is', '~이다')
    s.g('from', 'from', '~에서 나온')
    s.g('reliable', 'reliable', '믿을 만한, 신뢰할 수 있는')
    s.g('media', 'media', '미디어, 언론')
    s.g('source', 'source', '출처 (흔한 뜻: 원천)')
    s.g('evidence', 'evidence', '증거')
    s.g('is', 'is', '~이다', at=s.text.index('is valid'))
    s.g('valid', 'valid', '타당한, 근거가 확실한')
    s.hint('[whether the news story is from a reliable media source]', '[그 뉴스 기사가 믿을 만한 미디어 출처에서 나온 것인지]',
           span='whether the news story is from a reliable media source', label='명사절 접속사 whether',
           links=[(['whether'], ['가', '인지'])], meaning='그 뉴스 기사가 믿을 만한 미디어 출처에서 나온 것인지',
           explanation='check의 목적어인 whether 명사절(~인지). S′ the news story, V′ is + 뜻을 잇는 최소 보어 from a reliable media source. and 뒤 the evidence is valid도 whether에 이어지는 둘째 절이라 표시에서 제외.')
    s.review = ('주절 You also need to check(need to V) + 목적어 whether 명사절 두 절(the news story is from …, and the evidence is valid; and 뒤 절도 whether에 걸림). '
                '힌트 1개(명사절 whether). 관계사·수동 없음.')
    out.append(s)

    # ---------------- s44 ----------------
    s = S('s44', T['s44'])
    s.ch('In the digital age,', '디지털 시대에는,')
    s.ch('it might be impossible', '불가능할지도 모른다')
    s.ch('to avoid or eliminate all false information', '모든 거짓 정보를 피하거나 없애는 것은')
    s.ch('that spreads online.', '온라인에서 퍼지는.')
    s.natural('디지털 시대에는 온라인에서 퍼지는 모든 거짓 정보를 피하거나 없애는 것이 불가능할지도 모른다.')
    s.cl('main', 'it', subj='it', verbs=['might', 'be'])
    s.cl('subject_relative', 'that', verbs=['spreads'], marker='that')
    s.g('In', 'in', '~에')
    s.g('digital', 'digital', '디지털의')
    s.g('age', 'age', '시대 (흔한 뜻: 나이)')
    s.g('it|to', 'It … to V', '~하는 것은 (It은 뒤의 to V를 대신함)')
    s.glosses.sort(key=lambda g: g['spans'][0][0])
    fm = s.g('might', 'might V', '~할지도 모른다', kind='function', combines_with=[], at=s.text.index('might'))
    be = s.g('be', 'be', '~이다')
    link(fm, be)
    s.g('impossible', 'impossible', '불가능한')
    s.g('avoid', 'avoid', '피하다')
    s.g('or', 'or', '또는')
    s.g('eliminate', 'eliminate', '없애다, 제거하다', star=W['eliminate'])
    s.g('all', 'all', '모든')
    s.g('false', 'false', '거짓의')
    s.g('information', 'information', '정보')
    rel = s.g('that', 'that V′', 'V′하는 (관계대명사)')
    s.g('spreads', 'spread', '퍼지다', verb_form=v3(s, 'spreads', 'spread', '관계절 선행사 all false information'))
    s.g('online', 'online', '온라인에서')
    s.hint('it might be impossible [to avoid or eliminate]', '[피하거나 없애는 것은] 불가능할지도 모른다',
           span='it might be impossible to avoid or eliminate', label='가주어 It과 진주어 to부정사',
           links=[(['to'], ['는 것은'])], meaning='(모든 거짓 정보를) 피하거나 없애는 것은 불가능할지도 모른다',
           explanation='it은 뒤의 to avoid or eliminate …를 대신하는 가주어. to 뒤 avoid와 eliminate가 or로 병렬. 목적어 all false information 이하는 제외.')
    s.hint('all false information [that spreads]', '[퍼지는] 모든 거짓 정보', span='all false information that spreads',
           label='주격 관계대명사 that', links=[(['that'], ['는'])], meaning='(온라인에서) 퍼지는 모든 거짓 정보',
           explanation='선행사 all false information을 주격 관계대명사 that이 받아 spreads online이 꾸민다. V′ spreads까지만 표시.')
    s.relative_ids = [rel['id']]
    s.review = ('가주어 it + 진주어 to avoid or eliminate all false information(병렬 동사원형) + 주격 관계절 that spreads online. 진주어 앞에서 끊음. '
                '힌트 2개(가주어–진주어, 필수 관계사). 수동 없음.')
    out.append(s)

    # ---------------- s45 ----------------
    s = S('s45', T['s45'], key=True)
    s.ch('However,', '하지만,')
    s.ch('if you have the ability', '만약 당신이 능력을 가지고 있다면')
    s.ch('to view information critically and objectively,', '정보를 비판적이고 객관적으로 볼 수 있는,')
    s.ch('you will be able to reduce the damage', '당신은 피해를 줄일 수 있을 것이다')
    s.ch('that fake news can cause.', '가짜 뉴스가 일으킬 수 있는.')
    s.natural('하지만 정보를 비판적이고 객관적으로 볼 수 있는 능력이 있다면, 가짜 뉴스가 일으킬 수 있는 피해를 줄일 수 있을 것이다.')
    s.cl('subordinate', 'if', subj='you', verbs=['have'], marker='if')
    s.cl('main', 'you', subj='you', verbs=['will', 'be'], occ=1)
    s.cl('subordinate', 'that', subj='fake news', verbs=['can', 'cause'], marker='that')
    s.g('However', 'however', '하지만')
    s.g('if', 'if S′ V′', 'S′(이/가) V′한다면')
    s.g('have', 'have', '가지고 있다')
    s.g('ability|to', 'ability to V', '~할 수 있는 능력')
    s.g('view', 'view', '보다, 바라보다')
    s.g('information', 'information', '정보')
    s.g('critically', 'critically', '비판적으로')
    s.g('objectively', 'objectively', '객관적으로')
    fw = s.g('will', 'will V', '~할 것이다', kind='function', combines_with=[])
    ba = s.g('be|able|to', 'be able to V', '~할 수 있다')
    link(fw, ba)
    s.g('reduce', 'reduce', '줄이다')
    s.g('damage', 'damage', '피해')
    rel = s.g('that', 'that S′ V′', 'S′(이/가) V′하는 (관계대명사)')
    s.g('fake|news', 'fake news', '가짜 뉴스')
    fc = s.g('can', 'can V', '~할 수 있다', kind='function', combines_with=[])
    ca = s.g('cause', 'cause', '일으키다, 야기하다')
    link(fc, ca)
    s.hint('[if you have]', '[당신[독자]이 가지고 있다면]', span='if you have', label='조건 접속사 if',
           links=[(['if'], ['이', '다면'])], refs=[('you', '당신', READER)], meaning='(만약) 당신이 (능력을) 가지고 있다면',
           explanation='if가 이끄는 조건 부사절(S′ you, V′ have). 목적어 the ability to view … 이하는 제외.')
    s.hint('the damage [that fake news can cause]', '[가짜 뉴스가 일으킬 수 있는] 피해', span='the damage that fake news can cause',
           label='목적격 관계대명사 that', links=[(['that'], [('가', 1), '는'])], meaning='가짜 뉴스가 일으킬 수 있는 피해',
           explanation='선행사 the damage를 목적격 관계대명사 that이 받는다(cause의 목적어 자리가 비어 있음). S′ fake news, V′ can cause.')
    s.relative_ids = [rel['id']]
    s.review = ('조건 부사절 if you have the ability to view …(the ability to V: ~할 수 있는 능력) + 주절 you will be able to reduce the damage(be able to V: V는 will be) '
                '+ 목적격 관계절 that fake news can cause(선행사 the damage). 힌트 2개(조건 if, 필수 관계사). 수동 없음.')
    out.append(s)

    # ---------------- s46 ----------------
    s = S('s46', T['s46'])
    s.ch('Don’t forget!', '잊지 마라!')
    s.natural('잊지 마라!')
    s.cl('imperative', 'Don’t', verbs=['Don’t', 'forget'])
    fd = s.g('Don’t', 'do not V', '~하지 마라', kind='function', combines_with=[])
    fg = s.g('forget', 'forget', '잊다')
    link(fd, fg)
    s.review = '주어 없는 부정 명령문 Don’t forget(V만 표시). 힌트 없음.'
    out.append(s)

    # ---------------- s47 ----------------
    s = S('s47', T['s47'])
    s.ch('Anyone can be the next person', '누구든지 다음 사람이 될 수 있다')
    s.ch('producing or spreading fake news!', '가짜 뉴스를 만들어 내거나 퍼뜨리는!')
    s.natural('누구든지 가짜 뉴스를 만들어 내거나 퍼뜨리는 다음 사람이 될 수 있다!')
    s.cl('main', 'Anyone', subj='Anyone', verbs=['can', 'be'])
    s.g('Anyone', 'anyone', '누구든지')
    fc = s.g('can', 'can V', '~할 수 있다', kind='function', combines_with=[])
    be = s.g('be', 'be', '~이 되다 (흔한 뜻: ~이다)')
    link(fc, be)
    s.g('next', 'next', '다음의')
    s.g('person', 'person', '사람')
    f1 = s.g('producing', 'V-ing', '~하는', kind='function', combines_with=[])
    pr = s.g('producing', 'produce', '만들어 내다', same=True, verb_form=pp('ing', s, 'producing', 'produce'))
    link(f1, pr)
    s.g('or', 'or', '또는')
    f2 = s.g('spreading', 'V-ing', '~하는', kind='function', combines_with=[])
    sp = s.g('spreading', 'spread', '퍼뜨리다', same=True, verb_form=pp('ing', s, 'spreading', 'spread'))
    link(f2, sp)
    s.g('fake|news', 'fake news', '가짜 뉴스')
    s.hint('the next person [producing or spreading fake news]', '[가짜 뉴스를 만들어 내거나 퍼뜨리는] 다음 사람',
           span='the next person producing or spreading fake news', label='현재분사 후치수식',
           links=[(['ing', ('ing', 1)], ['는'])], meaning='가짜 뉴스를 만들어 내거나 퍼뜨리는 다음 사람',
           explanation='현재분사 producing과 spreading이 or로 이어져 fake news를 공통 목적어로 받고, 앞 명사 the next person을 뒤에서 꾸민다.')
    s.review = '주절 Anyone can be the next person + 현재분사 후치수식 producing or spreading fake news(병렬 분사, 공통 목적어). 힌트 1개(현재분사 후치수식). 관계사·수동 없음.'
    out.append(s)
    return out


UNIT = {
    'id': 'u4', 'source_id': 'src', 'paragraph_ids': ['p08', 'p09', 'p10'],
    'sentence_ids': [f's{n:02d}' for n in range(31, 48)],
    'today_words': [
        {'id': W['mislead'], 'text': 'mislead', 'meaning_ko': '속이다, 오도하다'},
        {'id': W['face_value'], 'text': 'at face value', 'meaning_ko': '액면 그대로, 곧이곧대로'},
        {'id': W['critical'], 'text': 'critical thinking', 'meaning_ko': '비판적 사고'},
        {'id': W['evaluate'], 'text': 'evaluate', 'meaning_ko': '평가하다'},
        {'id': W['biases'], 'text': 'biases', 'meaning_ko': '편견들'},
        {'id': W['credibility'], 'text': 'credibility', 'meaning_ko': '신뢰성'},
        {'id': W['intent'], 'text': 'intent', 'meaning_ko': '의도'},
        {'id': W['eliminate'], 'text': 'eliminate', 'meaning_ko': '없애다, 제거하다'},
    ],
}


def analysis(_):
    return {
        'heading_kind': '주제',
        'title_or_topic_en': 'Four Ways to Spot and Avoid Fake News',
        'title_or_topic_ko': '가짜 뉴스를 가려내고 피하는 네 가지 방법',
        'intent_ko': '가짜 뉴스에 속지 않으려면 헤드라인 너머까지 읽고, 뉴스를 비판적으로 판단하고, 자신의 편견을 점검하고, 출처의 신뢰성을 확인해야 하며, 이런 비판적·객관적인 태도가 가짜 뉴스의 피해를 줄일 수 있다는 점을 강조하는 글이다.',
        'flow': [
            {'sentence_ids': ['s31'], 'label': '질문',
             'text_ko': '정보가 넘쳐나는 인터넷에서 어떻게 가짜 뉴스에 속지 않을 수 있을지 묻는다.'},
            {'sentence_ids': ['s32', 's33', 's34', 's35', 's36', 's37'], 'label': '방법 1·2',
             'text_ko': '첫째, 클릭을 노린 자극적인 헤드라인만 읽지 말고 본문을 주의 깊게 읽는다. 둘째, 뉴스를 곧이곧대로 믿지 말고 비판적 사고로 질문하고 분석하고 평가한다.'},
            {'sentence_ids': ['s38', 's39', 's40', 's41', 's42', 's43'], 'label': '방법 3·4',
             'text_ko': '셋째, 자신의 편견이 판단에 영향을 주는지 살피고 반대 의견의 기사도 찾아 읽는다. 넷째, 누가 어떤 의도로 썼는지, 믿을 만한 출처인지, 증거가 타당한지 확인한다.'},
            {'sentence_ids': ['s44', 's45', 's46', 's47'], 'label': '결론',
             'text_ko': '온라인에 퍼지는 거짓 정보를 모두 피하거나 없애기는 불가능할지도 모르지만, 정보를 비판적이고 객관적으로 보는 능력이 있으면 가짜 뉴스의 피해를 줄일 수 있다. 누구나 가짜 뉴스를 만들거나 퍼뜨리는 사람이 될 수 있음을 잊지 말자.'},
        ],
        'easy_explanations': [
            {'sentence_id': 's35', 'explanatory_sentences': [
                '35번 문장은 가짜 뉴스를 피하는 두 번째 방법이다.',
                '액면 그대로 읽는다는 것은 뉴스에 쓰인 말을 따져 보지 않고 그대로 믿는 것이다.',
                '글쓴이는 그렇게 하지 말라고 한다.',
                '36~37번에서 그 대신 비판적으로 생각하며 질문하고 분석하라고 이어서 설명한다.']},
            {'sentence_id': 's40', 'explanatory_sentences': [
                '40번 문장은 38번의 ‘편견 점검하기’를 실제로 어떻게 하는지 알려 준다.',
                '먼저 내 생각과 같은 기사만 골라 읽고 있지는 않은지 스스로 물어본다.',
                '이것은 27~29번에서 말한 확증 편향에 빠지지 않기 위한 방법이다.',
                '그다음 내 생각과 반대되는 기사도 일부러 찾아 읽는다.']},
            {'sentence_id': 's47', 'explanatory_sentences': [
                '47번 문장은 글 전체의 마지막 당부다.',
                '도입부의 지나는 가짜 뉴스를 만들고 퍼뜨린 사람들을 비판했었다.',
                '그런데 결국 지나 자신도 실수로 가짜 뉴스를 퍼뜨리게 되었다.',
                '46번의 ‘잊지 마라!’는 바로 이 점을 기억하라는 말이다.',
                '누구든 가짜 뉴스를 만들거나 퍼뜨리는 사람이 될 수 있다는 것이다.']},
        ],
        'grammar_points': [
            {'id': 'u4-gp1', 'sentence_id': 's37', 'span': 'You should question, analyze, and evaluate what you read',
             'title': 'what S′ V′: S′(이/가) V′하는 것', 'formula_key': 'what S′ V′',
             'explanation': '공식: what S′ V′ — S′(이/가) V′하는 것. what = 선행사를 품은 관계대명사(~하는 것), S′ = you(당신), V′ = read(읽다). '
                            '→ 당신이 읽는 것. 이 what절 전체가 question, analyze, evaluate(의문을 제기하다, 분석하다, 평가하다)의 공통 목적어라 ‘당신이 읽는 것에 의문을 제기하고, 분석하고, 평가해야 한다’가 된다.',
             'practice': {'span': 'question, analyze, and evaluate what you read',
                          'formula_support': {'en': 'what S′ V′', 'ko': 'S′(이/가) V′하는 것'},
                          'support': [('s37', 'question'), ('s37', 'analyze'), ('s37', 'evaluate'), ('s37', 'read')],
                          'answer_ko': '당신이 읽는 것에 의문을 제기하고, 분석하고, 평가하다'}},
            {'id': 'u4-gp2', 'sentence_id': 's43', 'span': 'check whether the news story is from a reliable media source and the evidence is valid',
             'title': 'whether S′ V′: S′(이/가) V′하는지', 'formula_key': 'whether S′ V′',
             'explanation': '공식: whether S′ V′ — S′(이/가) V′하는지. S′ = the news story(그 뉴스 기사), V′ = is(~이다), 보어 = from a reliable media source(믿을 만한 미디어 출처에서 나온). '
                            'and 뒤에도 같은 whether에 걸리는 절 the evidence(증거) is(~이다) valid(타당한)가 이어진다. → 그 뉴스 기사가 믿을 만한 미디어 출처에서 나온 것인지, 그리고 증거가 타당한지. '
                            '앞의 check(확인하다)와 합치면 ‘~인지 확인하다’다.',
             'practice': {'span': 'whether the news story is from a reliable media source and the evidence is valid',
                          'formula_support': {'en': 'whether S′ V′', 'ko': 'S′(이/가) V′하는지'},
                          'support': [('s43', 'news story'), ('s43', 'from'), ('s43', 'reliable'), ('s43', 'media'),
                                      ('s43', 'source'), ('s43', 'evidence'), ('s43', 'valid')],
                          'answer_ko': '그 뉴스 기사가 믿을 만한 미디어 출처에서 나온 것인지, 그리고 증거가 타당한지'}},
            {'id': 'u4-gp3', 'sentence_id': 's42', 'span': 'examine who wrote the news story',
             'title': 'who V′(간접의문): 누가 V′했는지', 'formula_key': 'who V′',
             'explanation': '공식: who V′ — 누가 V′했는지. who = 의문사이면서 이 절의 주어(누가), V′ = wrote(썼다), 목적어 = the news story(그 뉴스 기사). '
                            '→ 누가 그 뉴스 기사를 썼는지. 이 절 전체가 앞 동사 examine(살펴보다)의 목적어라 ‘누가 그 뉴스 기사를 썼는지 살펴보다’가 된다. '
                            'who 뒤에 주어가 따로 없고 바로 동사가 온다.',
             'practice': {'span': 'who wrote the news story',
                          'formula_support': {'en': 'who V′', 'ko': '누가 V′했는지'},
                          'support': [('s42', 'wrote'), ('s42', 'news story')],
                          'answer_ko': '누가 그 뉴스 기사를 썼는지'}},
        ],
        'formula_routes': [],
        'relations': [
            {'head': {'id': 'u4-r1h', 'text': 'reliable', 'meaning_ko': '믿을 만한, 신뢰할 수 있는'},
             'synonym': {'id': 'u4-r1s', 'text': 'trustworthy', 'meaning_ko': '신뢰할 수 있는'},
             'antonym': {'id': 'u4-r1a', 'text': 'unreliable', 'meaning_ko': '믿을 수 없는'}},
            {'head': {'id': 'u4-r2h', 'text': 'valid', 'meaning_ko': '타당한, 근거가 확실한'},
             'synonym': {'id': 'u4-r2s', 'text': 'sound', 'meaning_ko': '타당한, 믿을 만한'},
             'antonym': {'id': 'u4-r2a', 'text': 'invalid', 'meaning_ko': '근거 없는, 타당하지 않은'}},
            {'head': {'id': 'u4-r3h', 'text': 'objectively', 'meaning_ko': '객관적으로'},
             'synonym': {'id': 'u4-r3s', 'text': 'impartially', 'meaning_ko': '공정하게, 치우치지 않게'},
             'antonym': {'id': 'u4-r3a', 'text': 'subjectively', 'meaning_ko': '주관적으로'}},
        ],
    }


def workbook():
    return {
        'relation_order': ['u4-r2s', 'u4-r3a', 'u4-r1h', 'u4-r2a', 'u4-r3s', 'u4-r1s', 'u4-r2h', 'u4-r1a', 'u4-r3h'],
        'key_sentence_ids': ['s33', 's45'],
        'question_id': 'Q04',
        'syntax_point_ids': ['u4-gp1', 'u4-gp2', 'u4-gp3'],
    }
