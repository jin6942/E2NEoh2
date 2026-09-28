"""공통 단위 2: The Impact of Fake News on Society (s11~s19, 단락 p03~p04; 짧은 단락이 있어 소제목 전체 묶음)."""
from author import S, link, find_word
from u1 import pp

W = {'distributor': 'u2-w1', 'deliberate': 'u2-w2', 'manipulate': 'u2-w3', 'intention': 'u2-w4',
     'disturb': 'u2-w5', 'shelters': 'u2-w6', 'displaced': 'u2-w7', 'anxious': 'u2-w8'}


def sentences(T):
    out = []

    # ---------------- s11 ----------------
    s = S('s11', T['s11'])
    s.ch('Unfortunately,', '안타깝게도,')
    s.ch('becoming an accidental distributor', '우발적인 유포자가 되는 것은')
    s.ch('of fake news', '가짜 뉴스의')
    s.ch('like Gina', '지나처럼')
    s.ch('is not unusual.', '드물지 않다.')
    s.natural('안타깝게도 지나처럼 뜻하지 않게 가짜 뉴스를 퍼뜨리는 사람이 되는 것은 드문 일이 아니다.')
    s.cl('main', 'becoming', subj='becoming an accidental distributor of fake news like Gina', verbs=['is'])
    s.g('Unfortunately', 'unfortunately', '안타깝게도, 불행하게도')
    f = s.g('becoming', 'V-ing', '~하는 것', kind='function', combines_with=[])
    bc = s.g('becoming', 'become', '~이 되다', same=True, verb_form=pp('ing', s, 'becoming', 'become'))
    link(f, bc)
    s.g('accidental', 'accidental', '우발적인, 뜻하지 않은')
    s.g('distributor', 'distributor', '유포자, 퍼뜨리는 사람 (흔한 뜻: 유통업자)', star=W['distributor'])
    s.g('of', 'of', '~의')
    s.g('fake|news', 'fake news', '가짜 뉴스')
    s.g('like', 'like', '~처럼')
    s.g('is', 'is', '~이다')
    s.g('not', 'not', '~지 않다')
    s.g('unusual', 'unusual', '드문, 흔치 않은')
    s.brk('of', 'postnominal-preposition', 'of fake news는 앞 명사 an accidental distributor를 뒤에서 꾸미는 전치사구')
    s.brk('like', 'postnominal-preposition', 'like Gina는 앞 명사구 an accidental distributor of fake news를 뒤에서 꾸미는 전치사구')
    s.hint('[becoming an accidental distributor]', '[우발적인 유포자가 되는 것은]', span='becoming an accidental distributor',
           label='동명사 주어', links=[(['ing'], ['는 것은'])], meaning='우발적인 유포자가 되는 것은',
           explanation='동명사 becoming이 이끄는 becoming an accidental distributor of fake news like Gina 전체가 문장의 주어이고 동사는 is. 보어 an accidental distributor까지 표시하고 뒤수식은 제외.')
    s.review = ('동명사구 주어 becoming … like Gina(전체 유지) + is not unusual(이중 부정: 드물지 않다 = 흔하다). of·like 앞 후치수식 경계. '
                '힌트 1개(동명사 주어). 관계사·접속사절·수동 없음.')
    out.append(s)

    # ---------------- s12 ----------------
    s = S('s12', T['s12'], key=True)
    s.ch('Fake news is a deliberate attempt', '가짜 뉴스는 의도적인 시도이다')
    s.ch('to manipulate people', '사람들을 조종하려는')
    s.ch('by spreading inaccurate information.', '부정확한 정보를 퍼뜨림으로써.')
    s.natural('가짜 뉴스는 부정확한 정보를 퍼뜨려 사람들을 조종하려는 의도적인 시도이다.')
    s.cl('main', 'Fake', subj='Fake news', verbs=['is'])
    s.g('Fake|news', 'fake news', '가짜 뉴스')
    s.g('is', 'is', '~이다')
    s.g('deliberate', 'deliberate', '의도적인, 고의적인', star=W['deliberate'])
    ft = s.g('attempt|to', 'attempt to V', '~하려는 시도')
    mn = s.g('manipulate', 'manipulate', '조종하다, 조작하다', star=W['manipulate'])
    s.g('people', 'people', '사람들')
    fb = s.g('by', 'by V-ing', '~함으로써', kind='function', combines_with=[])
    sp = s.g('spreading', 'spread', '퍼뜨리다', verb_form=pp('ing', s, 'spreading', 'spread'))
    link(fb, sp)
    s.g('inaccurate', 'inaccurate', '부정확한')
    s.g('information', 'information', '정보')
    s.hint('a deliberate attempt [to manipulate]', '[조종하려는] 의도적인 시도', span='a deliberate attempt to manipulate',
           label='to부정사 후치수식', links=[(['to'], ['려는'])], meaning='(사람들을) 조종하려는 의도적인 시도',
           explanation='to manipulate people가 앞 명사 a deliberate attempt의 내용을 꾸민다(~하려는 시도). 목적어 people은 표시에서 제외.')
    s.hint('[by spreading]', '[퍼뜨림으로써]', span='by spreading', label='전치사 by + 동명사',
           links=[(['by', 'ing'], ['림으로써'])], meaning='(부정확한 정보를) 퍼뜨림으로써',
           explanation='전치사 by + 동명사 spreading: ~함으로써(수단). 사람들을 조종하는 방법. 목적어 inaccurate information은 표시에서 제외.')
    s.review = ('단일 주절 Fake news is a deliberate attempt + to부정사 후치수식 to manipulate people(attempt to V: ~하려는 시도) + 수단 by spreading …. '
                '힌트 2개(to부정사 후치수식, by + 동명사). 관계사·수동 없음.')
    out.append(s)

    # ---------------- s13 ----------------
    s = S('s13', T['s13'])
    s.ch('It is made', '그것은 만들어진다')
    s.ch('by certain groups', '특정 집단들에 의해')
    s.ch('with the intention of attracting people’s attention,', '사람들의 관심을 끌려는 의도를 가지고,')
    s.ch('making profits,', '이익을 얻으려는,')
    s.ch('or gaining political benefits.', '또는 정치적 이득을 얻으려는.')
    s.natural('가짜 뉴스는 사람들의 관심을 끌거나, 이익을 얻거나, 정치적 이득을 얻으려는 의도를 가진 특정 집단들에 의해 만들어진다.')
    s.cl('main', 'It', subj='It', verbs=['is', 'made'])
    s.g('It', 'it', '그것은', referent_ko='가짜 뉴스')
    f = s.g('is', 'be p.p.', '~되다', kind='function', combines_with=[])
    md = s.g('made', 'made', '만들어진', verb_form=pp('passive-participle', s, 'made', 'make', f['id']))
    link(f, md)
    s.g('by', 'by', '~에 의해')
    s.g('certain', 'certain', '특정한 (흔한 뜻: 확실한)')
    s.g('groups', 'groups', '집단들')
    wi = s.g('with|the|intention|of', 'with the intention of V-ing', '~하려는 의도를 가지고', star=W['intention'])
    s.g('attracting', 'attract', '끌다, 끌어들이다', verb_form=pp('ing', s, 'attracting', 'attract'))
    s.g('people’s', 'people’s', '사람들의')
    s.g('attention', 'attention', '관심, 주목')
    s.g('making|profits', 'make profits', '이익을 얻다, 수익을 내다', verb_form=pp('ing', s, 'making', 'make'))
    s.g('or', 'or', '또는')
    s.g('gaining', 'gain', '얻다', verb_form=pp('ing', s, 'gaining', 'gain'))
    s.g('political', 'political', '정치적인')
    s.g('benefits', 'benefits', '이득들, 혜택들')
    s.brk('by', 'passive-agent-by', '수동 is made의 행위자(누구에 의해)를 나타내는 by 구')
    s.prot('with the intention of', 'fixed-expression', 'with the intention of V-ing(~하려는 의도를 가지고)를 가르지 않음', gloss=wi)
    s.vf_hint(fn=f, lex=md, en='is made', ko='만들어진다', formula='be p.p.', step_form='made', step_ko='만들어진',
              en_mark=['is'], ko_mark=['어진다'], span='It is made', meaning='만들어진다',
              explanation='빈 힌트 문장의 수동태 후보: is made(현재 수동). 주어 It과 by 구 이하는 표시에서 제외.')
    s.review = ('단일 주절 수동 is made + 행위자 by certain groups(by 앞에서 끊음) + with the intention of + 병렬 동명사 3개(attracting …, making …, or gaining …). '
                'with the intention of V-ing는 숙어 각주로 제공(힌트 후보 아님), V-ing 연결 뜻을 숙어가 제공해 별도 기능 각주 없음. 관계사·접속사절 없음 → 수동태 기능 결합 힌트.')
    out.append(s)

    # ---------------- s14 ----------------
    s = S('s14', T['s14'])
    s.ch('It can confuse people,', '그것은 사람들을 혼란스럽게 할 수 있다,')
    s.ch('disturb society,', '사회를 어지럽힐 수 있다,')
    s.ch('and even seriously harm the public', '그리고 심지어 대중에게 심각하게 해를 끼칠 수 있다')
    s.ch('as well as all individuals', '모든 개인들뿐만 아니라')
    s.ch('involved.', '관련된.')
    s.natural('가짜 뉴스는 사람들을 혼란스럽게 하고, 사회를 어지럽히며, 심지어 관련된 모든 개인뿐만 아니라 대중에게도 심각한 해를 끼칠 수 있다.')
    s.cl('main', 'It', subj='It', verbs=['can', 'confuse', 'disturb', 'and', 'harm'])
    s.g('It', 'it', '그것은', referent_ko='가짜 뉴스')
    f = s.g('can', 'can V', '~할 수 있다', kind='function', combines_with=[])
    c1 = s.g('confuse', 'confuse', '혼란스럽게 하다')
    s.g('people', 'people', '사람들')
    c2 = s.g('disturb', 'disturb', '어지럽히다, 방해하다', star=W['disturb'])
    s.g('society', 'society', '사회')
    s.g('even', 'even', '심지어')
    s.g('seriously', 'seriously', '심각하게')
    c3 = s.g('harm', 'harm', '해를 끼치다')
    link(f, c1, c2, c3)
    s.g('public', 'the public', '대중')
    s.g('as|well|as', 'B as well as A', 'A뿐만 아니라 B도')
    s.g('all', 'all', '모든')
    s.g('individuals', 'individuals', '개인들')
    iv = s.g('involved', 'involved', '관련된', verb_form=pp('past-participle', s, 'involved', 'involve'))
    s.brk('involved', 'postpositive-adjective', 'involved는 앞 명사 all individuals를 뒤에서 꾸미는 과거분사')
    s.hint('all individuals [involved]', '[관련된] 모든 개인들', span='all individuals involved', label='과거분사 후치수식',
           links=[(['involved'], ['관련된'])], participle_focus_gloss_id=iv['id'], meaning='관련된 모든 개인들',
           explanation='과거분사 involved가 명사 all individuals 뒤에서 꾸민다(관련된 모든 개인들).')
    s.review = ('단일 주절: 조동사 can이 병렬 동사 confuse, disturb, and harm을 모두 이끈다. the public as well as all individuals involved: B as well as A(A뿐만 아니라 B도), '
                'A=all individuals involved, B=the public. involved는 명사 뒤 과거분사 후치수식 → 앞에서 끊음. 힌트 1개(과거분사 후치수식). 관계사·수동 없음.')
    out.append(s)

    # ---------------- s15 ----------------
    s = S('s15', T['s15'])
    s.ch('It is very common', '매우 흔하다')
    s.ch('for fake news to spread', '가짜 뉴스가 퍼지는 것은')
    s.ch('during states of emergency.', '비상사태 동안.')
    s.natural('비상사태 때 가짜 뉴스가 퍼지는 것은 매우 흔한 일이다.')
    s.cl('main', 'It', subj='It', verbs=['is'])
    s.g('It|for|to', 'It … for A to V', 'A가 ~하는 것은 (It은 뒤의 for A to V를 대신함)')
    s.g('is', 'is', '~이다')
    s.glosses.sort(key=lambda g: g['spans'][0][0])
    s.g('very', 'very', '매우', at=s.text.index('very'))
    s.g('common', 'common', '흔한')
    s.g('fake|news', 'fake news', '가짜 뉴스')
    s.g('spread', 'spread', '퍼지다', at=s.text.index('spread'))
    s.g('during', 'during', '~ 동안')
    s.g('states|of|emergency', 'states of emergency', '비상사태들')
    s.prot('states of emergency', 'fixed-expression', 'state of emergency(비상사태)는 한 덩어리 명사 표현이라 of 앞에서 끊지 않음')
    s.hint('It is very common [for fake news to spread]', '[가짜 뉴스가 퍼지는 것은] 매우 흔하다',
           span='It is very common for fake news to spread', label='가주어 It과 진주어 to부정사',
           links=[(['for', 'to'], ['가', '는 것은'])], meaning='가짜 뉴스가 퍼지는 것은 매우 흔하다',
           explanation='It은 뒤의 for fake news to spread를 대신하는 가주어. for 뒤 fake news는 to spread의 의미상 주어(가짜 뉴스가 퍼지는 것). 진주어 앞(for 앞)에서 끊음.')
    s.review = ('가주어 It + 진주어 for A to V(for fake news to spread, A=fake news). 진주어 앞에서 끊음. '
                'states of emergency는 한 명사 표현. 힌트 1개(가주어–진주어). 관계사·수동 없음.')
    out.append(s)

    # ---------------- s16 ----------------
    s = S('s16', T['s16'])
    s.ch('For example,', '예를 들어,')
    s.ch('after an earthquake measuring 6.5', '규모 6.5의 지진이')
    s.ch('struck Ambon, Indonesia,', '인도네시아 암본을 강타한 후에,')
    s.ch('in September 2019,', '2019년 9월에,')
    s.ch('thousands of residents did not return', '수천 명의 주민들이 돌아가지 않았다')
    s.ch('to their homes', '그들의 집으로')
    s.ch('and were still in shelters', '그리고 여전히 대피소에 있었다')
    s.ch('for two weeks.', '2주 동안.')
    s.natural('예를 들어, 2019년 9월 인도네시아 암본에 규모 6.5의 지진이 발생한 후 수천 명의 주민들이 집으로 돌아가지 않고 2주 동안 대피소에 머물렀다.')
    s.cl('subordinate', 'after', subj='an earthquake measuring 6.5', verbs=['struck'], marker='after',
         disp='an earthquake', disp_review='중심명사 earthquake까지 표시하고 뒤수식 현재분사구 measuring 6.5는 제외')
    s.cl('main', 'thousands', subj='thousands of residents', verbs=['did', 'not', 'return', 'and', 'were'])
    s.g('For|example', 'for example', '예를 들어')
    s.g('after', 'after S′ V′', 'S′(이/가) V′한 후에')
    s.g('earthquake', 'earthquake', '지진')
    fm = s.g('measuring', 'V-ing', '~인', kind='function', combines_with=[])
    ms = s.g('measuring', 'measure', '(크기·규모가) ~이다 (흔한 뜻: 측정하다)', same=True, verb_form=pp('ing', s, 'measuring', 'measure'))
    link(fm, ms)
    s.g('struck', 'struck', '강타했다 (strike의 과거)', verb_form=pp('irregular-past', s, 'struck', 'strike'))
    s.g('Ambon', 'Ambon', '암본 (인도네시아의 도시)', proper=True)
    s.g('Indonesia', 'Indonesia', '인도네시아', proper=True)
    s.g('in', 'in', '~에')
    s.g('September', 'September', '9월')
    q = s.g('thousands of', 'thousands of', '수천 (명)의')
    s.g('residents', 'residents', '주민들')
    fd = s.g('did|not', 'did not V', '~하지 않았다', kind='function', combines_with=[])
    rt = s.g('return', 'return', '돌아가다')
    link(fd, rt)
    s.g('to', 'to', '~로')
    s.g('their', 'their', '그들의', referent_ko='암본 주민들')
    s.g('homes', 'homes', '집들')
    s.g('were', 'were', '(~에) 있었다')
    s.g('still', 'still', '여전히')
    s.g('in', 'in', '~에', at=s.text.index('in shelters'))
    s.g('shelters', 'shelters', '대피소들', star=W['shelters'])
    s.g('for', 'for', '~ 동안', at=s.text.index('for two'))
    s.g('two', 'two', '두, 2')
    s.g('weeks', 'weeks', '주들')
    s.prot('thousands of', 'quantity-kind-of', '수량 표현 thousands of가 뒤 명사 residents 앞에서 ‘수천 명의’로 같은 어순 대응', gloss=q)
    s.hint('[after an earthquake measuring 6.5 struck]', '[규모 6.5의 지진이 강타한 후에]', span='after an earthquake measuring 6.5 struck',
           label='시간 접속사 after', links=[(['after'], ['이', '한 후에'])], meaning='규모 6.5의 지진이 (암본을) 강타한 후에',
           explanation='after가 이끄는 시간 부사절(S′ an earthquake measuring 6.5, V′ struck). 주어 뒤 현재분사 measuring 6.5가 earthquake를 꾸며 S′에 포함. 목적어 Ambon, Indonesia 이하는 제외.')
    s.review = ('문두 시간 부사절 after an earthquake measuring 6.5 struck Ambon, Indonesia, in September 2019 + 주절 thousands of residents did not return … and were still in shelters(병렬 동사, 부정은 did not return에만 걸림). '
                'measuring 6.5는 현재분사 후치수식(규모가 6.5인). thousands of는 수량+of 같은 어순 예외. 힌트 1개(접속사 after). 관계사·수동 없음.')
    out.append(s)

    # ---------------- s17 ----------------
    s = S('s17', T['s17'])
    s.ch('This was because of fake news stories', '이것은 가짜 뉴스 이야기들 때문이었다')
    s.ch('on social media', '소셜 미디어에 올라온')
    s.ch('that another earthquake', '또 다른 지진이')
    s.ch('followed', '(뒤에) 이어지는')
    s.ch('by a tsunami', '쓰나미로')
    s.ch('was about to strike.', '곧 닥칠 것이라는.')
    s.natural('이는 쓰나미를 동반한 또 다른 지진이 곧 닥칠 것이라는 소셜 미디어상의 가짜 뉴스 때문이었다.')
    s.cl('main', 'This', subj='This', verbs=['was'])
    s.cl('subordinate', 'that', subj='another earthquake followed by a tsunami', verbs=['was'], marker='that',
         disp='another earthquake', disp_review='중심명사 earthquake까지 표시하고 뒤수식 과거분사구 followed by a tsunami는 제외(common-errors 1의 후치수식 주어 오인 방지)')
    s.g('This', 'this', '이것은', referent_ko='주민들이 집에 돌아가지 않고 2주 동안 대피소에 있었던 일')
    s.g('was', 'was', '~였다')
    s.g('because|of', 'because of', '~ 때문에')
    s.g('fake|news', 'fake news', '가짜 뉴스')
    s.g('stories', 'stories', '이야기들')
    s.g('on', 'on', '~에 올라온 (흔한 뜻: ~위에)')
    s.g('social|media', 'social media', '소셜 미디어')
    s.g('that', 'that S′ V′', 'S′(이/가) V′라는 (앞 명사의 내용을 설명)')
    s.g('another', 'another', '또 다른')
    s.g('earthquake', 'earthquake', '지진')
    fl = s.g('followed', 'followed', '(뒤에) 이어지는, 뒤따라진', verb_form=pp('past-participle', s, 'followed', 'follow'))
    s.g('by', 'by', '~로, ~에 의해')
    s.g('tsunami', 'tsunami', '쓰나미, 지진 해일')
    s.g('was|about|to', 'be about to V', '막 ~하려 하다, 곧 ~할 것이다')
    s.g('strike', 'strike', '(재난이) 닥치다, 발생하다')
    s.brk('on', 'postnominal-preposition', 'on social media는 앞 명사 fake news stories를 뒤에서 꾸미는 전치사구')
    s.brk('by', 'passive-agent-by', '과거분사 followed의 수동 관계에서 행위자(무엇에 의해)를 나타내는 by 구')
    s.hint('[that another earthquake followed by a tsunami was about to strike]',
           '[쓰나미로 이어지는 또 다른 지진이 곧 닥칠 것이라는]',
           span='that another earthquake followed by a tsunami was about to strike', label='동격 접속사 that',
           links=[(['that'], [('이', 1), '라는'])],
           meaning='쓰나미로 이어지는 또 다른 지진이 곧 닥칠 것이라는',
           explanation='that절이 앞 명사 fake news stories의 내용을 설명하는 동격절. S′는 another earthquake(과거분사구 followed by a tsunami가 뒤에서 꾸밈), V′는 was(be about to V: 곧 ~할 것이다). followed를 동사로 오인하지 않도록 S′ 전체와 V′ was까지 표시.')
    s.review = ('주절 This was because of fake news stories on social media + 동격 that절(stories의 내용). that절 주어 another earthquake를 과거분사구 followed by a tsunami가 꾸미고 '
                '동사는 was(be about to strike). followed는 동사가 아니라 후치수식(common-errors 1). on 앞 후치수식, 수동 관계 by 앞에서 끊음. '
                '힌트 1개(동격 that, 후치수식을 포함한 S′·V′ 표시). 유한 수동태 없음.')
    out.append(s)

    # ---------------- s18 ----------------
    s = S('s18', T['s18'])
    s.ch('One of those messages said,', '그 메시지들 중 하나는 말했다,')
    s.ch('“It’s up to you', '“당신에게 달려 있다')
    s.ch('if you want to believe me or not,', '당신이 나를 믿고 싶은지 아닌지는,')
    s.ch('but apparently Ambon is going to sink', '하지만 듣자 하니 암본은 가라앉을 것이다')
    s.ch('in the next few days.”', '앞으로 며칠 안에.”')
    s.natural('그 메시지 중 하나는 “나를 믿든 말든 당신 마음이지만, 듣자 하니 앞으로 며칠 안에 암본이 가라앉을 거래요.”라고 했다.')
    s.cl('main', 'One', subj='One of those messages', verbs=['said'])
    a = s.text.index('It’s')
    s.clauses.append({'kind': 'main', 'start': a, 'subject_spans': [[a, a + 2]], 'verb_spans': [[a + 2, a + 4]],
                      'contraction_readings': [{'span': [a + 2, a + 4], 'expanded': 'is'}]})
    s.cl('subordinate', 'if', subj='you', verbs=['want'], marker='if', occ=0)
    s.cl('main', 'Ambon', subj='Ambon', verbs=['is', 'going'], marker='but')
    s.g('One|of', 'one of', '~ 중 하나')
    s.g('those', 'those', '그')
    s.g('messages', 'messages', '메시지들')
    s.g('said', 'said', '말했다 (say의 과거)', verb_form=pp('irregular-past', s, 'said', 'say'))
    s.g('It’s', 'it’s', '(뒤의 if절을 대신하는) 그것은 ~이다 (It is의 줄임)')
    s.g('up|to', 'up to A', 'A에게 달려 있는')
    s.g('if|or|not', 'if S′ V′ or not', 'S′(이/가) V′하는지 아닌지')
    s.g('want|to', 'want to V', '~하고 싶다',
        verb_construction={'kind': 'to-complement', 'verb_span': s.span_of('want'), 'lemma': 'want',
                           'link_spans': [s.span_of('to', s.text.index('want'))],
                           'review_record': 'you want to believe me: want to V, V=believe.'})
    s.glosses.sort(key=lambda g: g['spans'][0][0])
    s.g('believe', 'believe', '믿다', at=s.text.index('believe'))
    s.g('me', 'me', '나를')
    s.glosses.sort(key=lambda g: g['spans'][0][0])
    s.g('apparently', 'apparently', '듣자 하니, 보아하니', at=s.text.index('apparently'))
    s.g('is|going|to', 'be going to V', '~할 것이다')
    s.g('sink', 'sink', '가라앉다')
    s.g('in|the|next|few|days', 'in the next few days', '앞으로 며칠 안에')
    s.hint('It’s up to you [if you want to believe]', '[당신[메시지를 읽는 사람]이 믿고 싶은지는] 당신[메시지를 읽는 사람]에게 달려 있다',
           span='It’s up to you if you want to believe', label='가주어 It과 진주어 if절',
           links=[(['if'], ['이', '은지는'])],
           refs=[(('you', 0), ('당신', 1), '[메시지를 읽는 사람]'), (('you', 1), '당신', '[메시지를 읽는 사람]')],
           meaning='당신이 (나를) 믿고 싶은지는 당신에게 달려 있다',
           explanation='It은 뒤의 if절(if you want to believe me or not: 믿고 싶은지 아닌지)을 대신하는 가주어. if는 ‘~인지’. 목적어 me와 or not은 표시에서 제외.')
    s.review = ('주절 One of those messages said(One of 부분 표현 주어 전체 유지) + 직접 인용: 가주어 It(’s = is) + 진주어 if절(if you want to believe me or not: ~인지 아닌지) '
                '+ [but] 등위절 apparently Ambon is going to sink …(be going to V). 인용 속 you는 메시지를 읽는 사람들. 힌트 1개(가주어–if절). 관계사·수동 없음.')
    out.append(s)

    # ---------------- s19 ----------------
    s = S('s19', T['s19'], key=True)
    s.ch('Many displaced people were so anxious', '많은 이재민들이 너무 불안해했다')
    s.ch('about aftershocks', '여진에 대해')
    s.ch('that the government had to announce', '그래서 정부는 발표해야 했다')
    s.ch('that the information was fake.', '그 정보가 가짜라고.')
    s.natural('많은 이재민들이 여진을 너무 불안해해서 정부는 그 정보가 가짜라고 발표해야 했다.')
    s.cl('main', 'Many', subj='Many displaced people', verbs=['were'])
    s.cl('subordinate', 'that', subj='the government', verbs=['had', 'to', 'announce'], marker='that')
    s.cl('subordinate', 'that', subj='the information', verbs=['was'], marker='that', occ=1)
    s.g('Many', 'many', '많은')
    s.g('displaced', 'displaced', '살던 곳을 잃은, 이재민이 된', star=W['displaced'],
        verb_form=pp('past-participle', s, 'displaced', 'displace'))
    s.g('people', 'people', '사람들')
    s.g('were', 'were', '~였다')
    s.g('so|that', 'so A that S′ V′', '너무 A해서 S′(이/가) V′하다')
    s.glosses.sort(key=lambda g: g['spans'][0][0])
    s.g('anxious', 'anxious', '불안해하는, 걱정하는', star=W['anxious'], at=s.text.index('anxious'))
    s.g('about', 'about', '~에 대해')
    s.g('aftershocks', 'aftershocks', '여진들 (큰 지진 뒤에 이어지는 작은 지진)')
    s.g('government', 'government', '정부')
    fh = s.g('had|to', 'had to V', '~해야 했다', kind='function', combines_with=[])
    an = s.g('announce', 'announce', '발표하다, 알리다')
    link(fh, an)
    s.g('that', 'that S′ V′', 'S′(이/가) V′라고 (접속사)', at=s.text.index('that the information'))
    s.g('information', 'information', '정보')
    s.g('was', 'was', '~였다', at=s.text.index('was fake'))
    s.g('fake', 'fake', '가짜의')
    s.hint('so anxious … that the government had to announce', '너무 불안해해서 … 정부는 발표해야 했다',
           span='so anxious about aftershocks that the government had to announce', category='paired-structure',
           display_spans=[s.span_of('so anxious'), s.span_of('that the government had to announce')],
           links=[(['so', 'that'], ['너무', '해서'])],
           meaning='너무 불안해해서 정부는 발표해야 했다',
           explanation='so A that S′ V′(너무 A해서 S′가 V′하다): A=anxious, 결과 that절 S′ the government, V′ had to announce. 사이의 about aftershocks와 뒤 목적어 that절은 표시에서 제외.')
    s.hint('[that the information was fake]', '[그 정보가 가짜라고]', span='that the information was fake',
           label='명사절 접속사 that', links=[(['that'], ['가', '라고'])], meaning='그 정보가 가짜라고',
           explanation='announce의 목적어인 that 명사절(S′ the information, V′ was + 최소 보어 fake). ~라고.')
    s.review = ('주절 Many displaced people were so anxious about aftershocks + 결과의 that절(so A that: the government had to announce) + announce의 목적어 명사절 that the information was fake. '
                '앞 that은 so와 짝을 이루는 결과 접속사, 뒤 that은 명사절 접속사. displaced는 명사 앞 독립 과거분사. 힌트 2개(so … that 짝 구조, 명사절 that). 관계사·수동 없음.')
    out.append(s)
    return out


UNIT = {
    'id': 'u2', 'source_id': 'src', 'paragraph_ids': ['p03', 'p04'],
    'sentence_ids': [f's{n:02d}' for n in range(11, 20)],
    'today_words': [
        {'id': W['distributor'], 'text': 'distributor', 'meaning_ko': '유포자, 퍼뜨리는 사람'},
        {'id': W['deliberate'], 'text': 'deliberate', 'meaning_ko': '의도적인, 고의적인'},
        {'id': W['manipulate'], 'text': 'manipulate', 'meaning_ko': '조종하다, 조작하다'},
        {'id': W['intention'], 'text': 'with the intention of V-ing', 'meaning_ko': '~하려는 의도를 가지고'},
        {'id': W['disturb'], 'text': 'disturb', 'meaning_ko': '어지럽히다, 방해하다'},
        {'id': W['shelters'], 'text': 'shelters', 'meaning_ko': '대피소들'},
        {'id': W['displaced'], 'text': 'displaced', 'meaning_ko': '살던 곳을 잃은, 이재민이 된'},
        {'id': W['anxious'], 'text': 'anxious', 'meaning_ko': '불안해하는, 걱정하는'},
    ],
}


def analysis(_):
    return {
        'heading_kind': '주제',
        'title_or_topic_en': 'What Fake News Is and How It Harms Society',
        'title_or_topic_ko': '가짜 뉴스의 정체와 사회에 끼치는 해',
        'intent_ko': '가짜 뉴스는 사람들을 조종하려고 부정확한 정보를 퍼뜨리는 의도적인 시도이며, 특히 비상사태 때 퍼져 사회에 큰 혼란과 해를 끼친다는 점을 인도네시아 암본의 사례로 보여 주는 글이다.',
        'flow': [
            {'sentence_ids': ['s11', 's12', 's13', 's14'], 'label': '정의와 해악',
             'text_ko': '지나처럼 뜻하지 않게 가짜 뉴스를 퍼뜨리는 일은 흔하다. 가짜 뉴스는 관심·이익·정치적 이득을 노리는 집단이 사람들을 조종하려고 만든 의도적인 시도이며, 사람들과 사회에 심각한 해를 끼칠 수 있다.'},
            {'sentence_ids': ['s15', 's16', 's17', 's18', 's19'], 'label': '비상사태 사례',
             'text_ko': '가짜 뉴스는 비상사태 때 특히 잘 퍼진다. 2019년 암본 지진 뒤 또 다른 지진과 쓰나미가 온다는 가짜 뉴스 때문에 주민들은 2주 동안 집에 돌아가지 못했고, 결국 정부가 그 정보가 가짜라고 발표해야 했다.'},
        ],
        'easy_explanations': [
            {'sentence_id': 's11', 'explanatory_sentences': [
                '11번 문장은 앞 도입부의 지나 이야기를 이 부분의 주제와 이어 준다.',
                '지나는 일부러 가짜 뉴스를 퍼뜨린 것이 아니다.',
                '글쓴이는 이런 일이 지나에게만 일어나는 드문 일이 아니라고 말한다.',
                '누구든 지나처럼 모르는 사이에 가짜 뉴스를 퍼뜨릴 수 있다는 뜻이다.']},
            {'sentence_id': 's13', 'explanatory_sentences': [
                '13번 문장은 12번에서 정의한 가짜 뉴스를 누가, 왜 만드는지 설명한다.',
                '가짜 뉴스를 만드는 쪽은 특정한 목적을 가진 집단이다.',
                '목적은 세 가지다.',
                '사람들의 관심 끌기, 돈 벌기, 정치적으로 유리해지기다.',
                '7~8번에서 조회수로 돈을 벌려던 콘텐츠 제작자들이 그 예다.']},
            {'sentence_id': 's17', 'explanatory_sentences': [
                '17번 문장은 16번에서 주민들이 집에 돌아가지 않은 이유를 밝힌다.',
                '소셜 미디어에 또 다른 지진이 곧 온다는 가짜 이야기가 돌았다.',
                '그 지진 뒤에는 쓰나미까지 이어진다고 했다.',
                '쓰나미는 지진 때문에 생기는 아주 큰 바닷물 파도다.',
                '주민들은 이 말을 믿고 무서워서 대피소에 계속 머물렀다.']},
        ],
        'grammar_points': [
            {'id': 'u2-gp1', 'sentence_id': 's12', 'span': 'a deliberate attempt to manipulate people',
             'title': '명사 + to V: ~하려는 명사', 'formula_key': 'N + to V',
             'explanation': '공식: 명사(N) + to V — ~하려는 N. N = a deliberate attempt(의도적인 시도), to V = to manipulate(조종하다), 목적어 = people(사람들). '
                            '→ 사람들을 조종하려는 의도적인 시도. to manipulate people가 앞 명사 attempt가 어떤 시도인지 뒤에서 설명한다.',
             'practice': {'span': 'a deliberate attempt to manipulate people',
                          'formula_support': {'en': 'N + to V', 'ko': '~하려는 N'},
                          'support': [('s12', 'deliberate'), ('s12', 'manipulate'), ('s12', 'people')],
                          'answer_ko': '사람들을 조종하려는 의도적인 시도'}},
            {'id': 'u2-gp2', 'sentence_id': 's15', 'span': 'It is very common for fake news to spread',
             'title': 'It … for A to V: A가 ~하는 것은 …', 'formula_key': 'It … for A to V',
             'explanation': '공식: It is 형용사 for A to V — A가 ~하는 것은 (형용사)하다. It = 가주어(뒤의 for A to V를 대신함), 형용사 = very common(매우 흔한), '
                            'A = fake news(가짜 뉴스), to V = to spread(퍼지다). → 가짜 뉴스가 퍼지는 것은 매우 흔하다. for 뒤의 A가 to V의 주체다.',
             'practice': {'span': 'It is very common for fake news to spread',
                          'formula_support': {'en': 'It … for A to V', 'ko': 'A가 ~하는 것은'},
                          'support': [('s15', 'very'), ('s15', 'common'), ('s15', 'fake news'), ('s15', 'spread')],
                          'answer_ko': '가짜 뉴스가 퍼지는 것은 매우 흔하다'}},
            {'id': 'u2-gp3', 'sentence_id': 's19', 'span': 'were so anxious about aftershocks that the government had to announce',
             'title': 'so A that S′ V′: 너무 A해서 S′가 V′하다', 'formula_key': 'so A that S′ V′',
             'explanation': '공식: so A that S′ V′ — 너무 A해서 S′(이/가) V′하다. A = anxious(불안해하는), about aftershocks = 여진에 대해, '
                            'S′ = the government(정부), V′ = had to announce(발표해야 했다). → 여진에 대해 너무 불안해해서 정부가 발표해야 했다. '
                            'that 앞은 원인(몹시 불안함), that 뒤는 그 결과다.',
             'practice': {'span': 'so anxious about aftershocks that the government had to announce',
                          'formula_support': {'en': 'so A that S′ V′', 'ko': '너무 A해서 S′(이/가) V′하다'},
                          'support': [('s19', 'anxious'), ('s19', 'about'), ('s19', 'aftershocks'), ('s19', 'government'),
                                      ('s19', 'had to V'), ('s19', 'announce')],
                          'answer_ko': '여진에 대해 너무 불안해해서 정부가 발표해야 했다'}},
        ],
        'formula_routes': [
            {'function': ('s13', 'be p.p.', 0), 'route': 'hint', 'hint_index': 0,
             'review_record': 'is made: 빈 힌트 문장의 수동태 기능 결합 힌트'},
        ],
        'relations': [
            {'head': {'id': 'u2-r1h', 'text': 'deliberate', 'meaning_ko': '의도적인, 고의적인'},
             'synonym': {'id': 'u2-r1s', 'text': 'intentional', 'meaning_ko': '의도적인, 고의의'},
             'antonym': {'id': 'u2-r1a', 'text': 'accidental', 'meaning_ko': '우연한, 뜻하지 않은'}},
            {'head': {'id': 'u2-r2h', 'text': 'inaccurate', 'meaning_ko': '부정확한'},
             'synonym': {'id': 'u2-r2s', 'text': 'incorrect', 'meaning_ko': '틀린, 부정확한'},
             'antonym': {'id': 'u2-r2a', 'text': 'accurate', 'meaning_ko': '정확한'}},
            {'head': {'id': 'u2-r3h', 'text': 'common', 'meaning_ko': '흔한'},
             'synonym': {'id': 'u2-r3s', 'text': 'usual', 'meaning_ko': '흔히 있는, 보통의'},
             'antonym': {'id': 'u2-r3a', 'text': 'rare', 'meaning_ko': '드문'}},
        ],
    }


def workbook():
    return {
        'relation_order': ['u2-r3s', 'u2-r1a', 'u2-r2h', 'u2-r3a', 'u2-r1s', 'u2-r2a', 'u2-r3h', 'u2-r1h', 'u2-r2s'],
        'key_sentence_ids': ['s12', 's19'],
        'question_id': 'Q02',
        'syntax_point_ids': ['u2-gp1', 'u2-gp2', 'u2-gp3'],
    }
