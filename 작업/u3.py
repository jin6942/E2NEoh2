"""공통 단위 3: Chasing Steve (s34~s55, 단락 p06~p09; 짧은 단락이 있어 소제목 전체 묶음)."""
from author import S, link
from u2 import pp

W = {'informal': 'u3-w1', 'phenomenon': 'u3-w2', 'possess': 'u3-w3', 'resemble': 'u3-w4',
     'acknowledged': 'u3-w5', 'dedicated': 'u3-w6', 'deserve': 'u3-w7', 'confirm': 'u3-w8'}


def sentences(T):
    out = []

    # ---------------- s34 ----------------
    s = S('s34', T['s34'])
    s.ch('In Alberta, Canada,', '캐나다 앨버타주에는,')
    s.ch('there were some “aurora chasers”', '몇몇 ‘오로라 추적자들’이 있었다')
    s.ch('who formed an informal group online.', '온라인에서 비공식 단체를 결성한.')
    s.natural('캐나다 앨버타주에는 온라인상에서 비공식 단체를 결성한 ‘오로라 추적자들’이 있었다.')
    s.cl('main', 'there', subj='some “aurora chasers”', verbs=[], vfirst=['were'])
    s.cl('subject_relative', 'who', verbs=['formed'], marker='who')
    s.g('In', 'in', '~에')
    s.g('Alberta', 'Alberta', '앨버타주 (캐나다의 주)', proper=True)
    s.g('Canada', 'Canada', '캐나다', proper=True)
    s.g('were', 'were', '있었다 (be의 과거)', verb_form=pp('irregular-past', s, 'were', 'be'))
    s.g('some', 'some', '몇몇의')
    s.g('aurora|chasers', 'aurora chasers', '오로라 추적자들 (오로라를 쫓아다니며 관찰하는 사람들)')
    rel = s.g('who', 'who V′', 'V′한 (관계대명사)')
    s.g('formed', 'form', '결성하다, 만들다', verb_form=pp('regular-past', s, 'formed', 'form'))
    s.g('informal', 'informal', '비공식적인', star=W['informal'])
    s.g('group', 'group', '단체, 모임')
    s.g('online', 'online', '온라인에서')
    s.extra_cov[tuple(s.span_of('there'))] = {'exemption': 'below-middle1-unneeded', 'level': 'below-middle1',
        'reason': '유도부사 there(초등 기초어)는 따로 해석하지 않으며 뒤 were 각주의 ‘있었다’로 뜻을 지원'}
    s.hint('some “aurora chasers” [who formed]', '[결성한] 몇몇 ‘오로라 추적자들’', span='some “aurora chasers” who formed',
           label='주격 관계대명사 who', links=[(['who'], ['한'])], meaning='(온라인에서 비공식 단체를) 결성한 몇몇 오로라 추적자들',
           explanation='“aurora chasers”(사람)를 주격 관계대명사 who가 받아 formed an informal group online이 꾸민다. V′ formed까지만 표시.')
    s.relative_ids = [rel['id']]
    s.review = '유도부사 there + were, 주어 some “aurora chasers”. 필수 관계사 who 힌트. 수동 없음.'
    out.append(s)

    # ---------------- s35 ----------------
    s = S('s35', T['s35'])
    s.ch('They would leave their homes at night', '그들은 밤에 자신들의 집을 나서곤 했다')
    s.ch('and try to get exceptional photographs', '그리고 특별한 사진들을 얻으려고 애쓰곤 했다')
    s.ch('of auroras.', '오로라의.')
    s.natural('그들은 밤에 집을 나서서 특별한 오로라 사진을 찍으려고 하곤 했다.')
    s.cl('main', 'They', subj='They', verbs=['would', 'leave', 'and', 'try'])
    s.g('They', 'they', '그들은', referent_ko='오로라 추적자들')
    f = s.g('would', 'would V', '~하곤 했다', kind='function', combines_with=[])
    lv = s.g('leave', 'leave', '떠나다, 나서다')
    s.g('their', 'their', '그들의', referent_ko='오로라 추적자들')
    s.g('homes', 'homes', '집들')
    s.g('at|night', 'at night', '밤에')
    tr = s.g('try|to', 'try to V', '~하려고 애쓰다',
             verb_construction={'kind': 'to-complement', 'verb_span': s.span_of('try'), 'lemma': 'try',
                                'link_spans': [s.span_of('to')], 'review_record': 'try to get: try의 목적어 to V.'})
    link(f, lv, tr)
    s.g('get', 'get', '얻다, (사진을) 찍다')
    s.g('exceptional', 'exceptional', '특별한, 뛰어난')
    s.g('photographs', 'photographs', '사진들')
    s.g('of', 'of', '~의')
    s.g('auroras', 'auroras', '오로라들')
    s.brk('of', 'postnominal-preposition', 'of auroras는 앞 명사 photographs를 꾸미는 전치사구')
    s.review = '주어 They의 병렬 동사 would leave and (would) try: would는 과거의 반복 습관. 접속사절·관계사·수동 없음 → 힌트 없음.'
    out.append(s)

    # ---------------- s36 ----------------
    s = S('s36', T['s36'])
    s.ch('Then they would share them', '그런 다음 그들은 그것들을 공유하곤 했다')
    s.ch('with the rest', '나머지 사람들과')
    s.ch('of the group.', '그 단체의.')
    s.natural('그런 다음 그들은 그 사진들을 단체의 나머지 사람들과 공유하곤 했다.')
    s.cl('main', 'they', subj='they', verbs=['would', 'share'])
    s.g('Then', 'then', '그런 다음')
    s.g('they', 'they', '그들은', referent_ko='오로라 추적자들')
    f = s.g('would', 'would V', '~하곤 했다', kind='function', combines_with=[])
    sh = s.g('share|with', 'share A with B', 'A를 B와 공유하다',
             verb_construction={'kind': 'verb-frame', 'verb_span': s.span_of('share'), 'lemma': 'share',
                                'link_spans': [s.span_of('with')], 'review_record': 'share them with the rest of the group: A=them, B=the rest of the group.'})
    link(f, sh)
    s.g('them', 'them', '그것들을', referent_ko='그들이 찍은 오로라 사진들')
    s.g('rest', 'rest', '나머지 (사람들)')
    s.g('of', 'of', '~의')
    s.g('group', 'group', '단체')
    s.brk('of', 'postnominal-preposition', 'of the group은 앞 명사 the rest를 꾸미는 전치사구')
    s.review = '단일 주절 would V(습관), share A with B. the rest of the group은 어순이 뒤집히는 일반 명사구라 of 앞에서 끊음. 힌트 없음.'
    out.append(s)

    # ---------------- s37 ----------------
    s = S('s37', T['s37'])
    s.ch('In the summer', '여름에')
    s.ch('of 2014,', '2014년의,')
    s.ch('the group members began to notice', '그 단체 구성원들은 알아채기 시작했다')
    s.ch('something', '무언가가')
    s.ch('strange', '이상한')
    s.ch('appearing in the night sky.', '밤하늘에 나타나는 것을.')
    s.natural('2014년 여름, 그 단체 구성원들은 밤하늘에 이상한 무언가가 나타나는 것을 알아채기 시작했다.')
    s.cl('main', 'the', subj='the group members', verbs=['began'], occ=1)
    s.g('In', 'in', '~에')
    s.g('summer', 'summer', '여름')
    s.g('of', 'of', '~의')
    s.g('group|members', 'group members', '단체 구성원들')
    s.g('began|to', 'begin to V', '~하기 시작하다 (began은 begin의 과거)',
        verb_construction={'kind': 'to-complement', 'verb_span': s.span_of('began'), 'lemma': 'begin',
                           'link_spans': [s.span_of('to')], 'review_record': 'began to notice: begin의 목적어 to V.'})
    nt = s.g('notice', 'notice A V-ing', 'A(이/가) ~하는 것을 알아채다',
             verb_construction={'kind': 'verb-frame', 'verb_span': s.span_of('notice'), 'lemma': 'notice', 'link_spans': [],
                                'review_record': 'notice something strange appearing: A=something strange, V-ing=appearing(목적격 보어). V-ing 연결은 이 구문이 제공.'})
    s.g('something', 'something', '무언가')
    s.g('strange', 'strange', '이상한')
    s.g('appearing', 'appear', '나타나다', verb_form=pp('ing', s, 'appearing', 'appear'))
    s.g('in', 'in', '~에', at=s.text.index('in the night'))
    s.g('night|sky', 'night sky', '밤하늘')
    s.brk('of', 'postnominal-preposition', 'of 2014는 앞 명사 the summer를 꾸미는 전치사구')
    s.brk('strange', 'postpositive-adjective', 'strange는 something 뒤에서 꾸미는 형용사')
    s.hint('notice [something strange appearing]', '[이상한 무언가가 나타나는 것을] 알아채다', span='notice something strange appearing',
           label='notice A V-ing 구문', links=[(['notice', 'ing'], ['가', '는 것을'])],
           emphasis_policy='ko-only-verb-construction', meaning='이상한 무언가가 나타나는 것을 알아채다',
           explanation='지각동사 notice + A(something strange) + V-ing(appearing): A가 ~하는 것을 알아채다. 동사 구문이라 한국어의 주어 조사 가와 연결 어미 는 것을만 강조.')
    s.review = ('단일 주절 began to notice. notice A V-ing(지각동사+목적어+현재분사). something strange는 형용사 후치라 strange 앞에서 끊고, '
                'the summer of 2014의 of 앞에서 끊음. 힌트: notice A V-ing 동사 구문(더 우선하는 관계사·접속사 없음). 수동 없음.')
    out.append(s)

    # ---------------- s38 ----------------
    s = S('s38', T['s38'])
    s.ch('There were unusual ribbons', '특이한 띠들이 있었다')
    s.ch('of green and purple light,', '녹색과 보라색 빛의,')
    s.ch('some of which seemed to stretch', '그리고 그중 일부는 뻗어 있는 것처럼 보였다')
    s.ch('for thousands of kilometers.', '수천 킬로미터에 걸쳐.')
    s.natural('녹색과 보라색의 특이한 빛의 띠가 있었는데, 그중 일부는 수천 킬로미터에 걸쳐 뻗어 있는 것처럼 보였다.')
    s.cl('main', 'There', subj='unusual ribbons of green and purple light', verbs=[], vfirst=['were'],
         disp='unusual ribbons', disp_review='중심명사 ribbons까지 표시하고 뒤에서 꾸미는 of green and purple light는 제외')
    s.cl('subject_relative', 'some', verbs=['seemed'], marker='some of which')
    s.g('were', 'were', '있었다 (be의 과거)', verb_form=pp('irregular-past', s, 'were', 'be'))
    s.g('unusual', 'unusual', '특이한, 흔치 않은')
    s.g('ribbons', 'ribbons', '(리본 모양의) 띠들')
    s.g('of', 'of', '~의')
    s.g('green', 'green', '녹색의')
    s.g('purple', 'purple', '보라색의')
    s.g('light', 'light', '빛')
    rel = s.g('some|of|which', 'some of which V′', '그리고 그중 일부는 V′하다 (관계대명사)')
    s.g('seemed|to', 'seem to V', '~하는 것 같다, ~처럼 보이다', verb_form=pp('regular-past', s, 'seemed', 'seem'),
        verb_construction={'kind': 'to-complement', 'verb_span': s.span_of('seemed'), 'lemma': 'seem',
                           'link_spans': [s.span_of('to')], 'review_record': 'seemed to stretch: seem의 보충 to V.'})
    s.g('stretch', 'stretch', '뻗다, 뻗어 있다')
    s.g('for', 'for', '~에 걸쳐')
    q = s.g('thousands of', 'thousands of', '수천의')
    s.g('kilometers', 'kilometers', '킬로미터')
    s.extra_cov[tuple(s.span_of('There'))] = {'exemption': 'below-middle1-unneeded', 'level': 'below-middle1',
        'reason': '유도부사 there(초등 기초어)는 따로 해석하지 않으며 뒤 were 각주의 ‘있었다’로 뜻을 지원'}
    s.brk('of', 'postnominal-preposition', 'of green and purple light는 앞 명사 ribbons를 꾸미는 전치사구')
    s.prot('thousands of', 'quantity-kind-of', '수량 표현 thousands of가 kilometers 앞에서 ‘수천의’로 같은 어순 대응', gloss=q)
    s.hint('ribbons of green and purple light, [some of which seemed to stretch]', '녹색과 보라색 빛의 띠들, [그리고 그중 일부는 뻗어 있는 것처럼 보였다]',
           span='ribbons of green and purple light, some of which seemed to stretch', label='관계대명사 some of which',
           links=[(['some of which'], ['그리고 그중 일부는'])], meaning='그리고 그 띠들 중 일부는 뻗어 있는 것처럼 보였다',
           explanation='some of which: which는 앞의 unusual ribbons(빛의 띠들)를 받고 some of가 붙어 ‘그중 일부’가 주어 역할. seem to V는 보충 to V까지 함께 보여야 뜻이 잡혀 포함(be 동사의 최소 보어 예외를 준용).')
    s.relative_ids = [rel['id']]
    s.review = ('유도부사 There + were, 주어 unusual ribbons of green and purple light(표시는 중심명사까지). '
                'some of which 관계절(which=ribbons) 필수 힌트. thousands of 수량 표현 보호. 수동 없음.')
    out.append(s)

    # ---------------- s39 ----------------
    s = S('s39', T['s39'])
    s.ch('Sometimes they lasted for just a few minutes,', '때때로 그것들은 단 몇 분 동안 지속되었다,')
    s.ch('while other times they remained in the sky', '반면 다른 때에는 그것들은 하늘에 머물렀다')
    s.ch('for a whole hour.', '한 시간 내내.')
    s.natural('그것들은 어떤 때에는 단 몇 분간 지속되었지만, 다른 때에는 한 시간 내내 하늘에 머무르기도 했다.')
    s.cl('main', 'they', subj='they', verbs=['lasted'])
    s.cl('subordinate', 'while', subj='they', verbs=['remained'], marker='while')
    s.g('Sometimes', 'sometimes', '때때로, 어떤 때는')
    s.g('they', 'they', '그것들은', referent_ko='녹색과 보라색 빛의 띠들')
    s.g('lasted', 'last', '지속되다', verb_form=pp('regular-past', s, 'lasted', 'last'))
    s.g('for', 'for', '~동안')
    s.g('just', 'just', '단, 겨우')
    s.g('a few', 'a few', '몇몇의, 몇')
    s.g('minutes', 'minutes', '분')
    s.g('while', 'while S′ V′', 'S′(이/가) V′하는 반면')
    s.g('other|times', 'other times', '다른 때에는')
    s.g('they', 'they', '그것들이', referent_ko='녹색과 보라색 빛의 띠들')
    s.g('remained', 'remain', '머무르다, 남아 있다', verb_form=pp('regular-past', s, 'remained', 'remain'))
    s.g('in', 'in', '~에')
    s.g('sky', 'sky', '하늘')
    s.g('for', 'for', '~동안')
    s.g('whole', 'whole', '꼬박, 전체의')
    s.g('hour', 'hour', '시간')
    s.hint('[while other times they remained]', '[다른 때에는 그것들[빛의 띠들]이 머무른 반면]',
           span='while other times they remained', label='대조 접속사 while',
           links=[(['while'], ['이', '반면'])], refs=[('they', '그것들', '[빛의 띠들]')],
           meaning='다른 때에는 그것들이 (하늘에 한 시간 내내) 머무른 반면',
           explanation='while S′ V′가 앞 절(몇 분만 지속)과 대조를 이룬다. S′ they, V′ remained까지 표시하고 in the sky 이하는 제외.')
    s.review = '주절 + 대조의 while 부사절(시간 아님). 힌트 1개. 수동 없음.'
    out.append(s)

    # ---------------- s40 ----------------
    s = S('s40', T['s40'])
    s.ch('They were similar in appearance to auroras,', '그것들은 생김새가 오로라와 비슷했다,')
    s.ch('yet they possessed some notably different features.', '하지만 그것들은 몇 가지 현저하게 다른 특징들을 지니고 있었다.')
    s.natural('그것들은 생김새가 오로라와 비슷했지만, 몇 가지 눈에 띄게 다른 특징들을 지니고 있었다.')
    s.cl('main', 'They', subj='They', verbs=['were'])
    s.cl('main', 'they', subj='they', verbs=['possessed'], marker='yet')
    s.g('They', 'they', '그것들은', referent_ko='녹색과 보라색 빛의 띠들')
    s.g('were|similar|to', 'be similar to', '~와 비슷하다')
    s.g('in|appearance', 'in appearance', '생김새가, 겉모습이')
    s.g('auroras', 'auroras', '오로라들')
    s.g('yet', 'yet', '하지만, 그렇지만')
    s.g('they', 'they', '그것들은', referent_ko='녹색과 보라색 빛의 띠들')
    s.g('possessed', 'possess', '지니다, 가지다', star=W['possess'], verb_form=pp('regular-past', s, 'possessed', 'possess'))
    s.g('some', 'some', '몇몇의, 몇 가지')
    s.g('notably', 'notably', '현저하게, 눈에 띄게')
    s.g('different', 'different', '다른')
    s.g('features', 'features', '특징들')
    s.review = '두 독립절(yet=but). be similar to 사이에 in appearance가 끼어 있음. 힌트 불필요, 수동 없음.'
    out.append(s)

    # ---------------- s41 ----------------
    s = S('s41', T['s41'])
    s.ch('Unsure of what they were,', '그것들이 무엇인지 확신하지 못해서,')
    s.ch('the group decided to name the phenomenon “Steve,”', '그 단체는 그 현상을 ‘Steve’라고 이름 짓기로 결정했다,')
    s.ch('based on a scene', '한 장면을 바탕으로')
    s.ch('from an animated movie', '한 애니메이션 영화에 나오는')
    s.ch('where some characters give that name', '몇몇 등장인물들이 그 이름을 붙이는')
    s.ch('to an unfamiliar object.', '낯선 물체에.')
    s.natural('그것들이 무엇인지 확신하지 못한 그 단체는, 등장인물들이 낯선 물체에 Steve라는 이름을 붙이는 한 애니메이션 영화의 장면을 바탕으로 이 현상을 ‘Steve’라고 이름 짓기로 결정했다.')
    s.cl('subordinate', 'what', subj='they', verbs=['were'], marker='what')
    s.cl('main', 'the', subj='the group', verbs=['decided'])
    s.cl('subordinate', 'where', subj='some characters', verbs=['give'], marker='where')
    s.g('Unsure|of', 'unsure of', '~을 확신하지 못하는')
    s.g('what', 'what S′ V′', 'S′(이/가) 무엇인지')
    s.g('they', 'they', '그것들이', referent_ko='녹색과 보라색 빛의 띠들')
    s.g('were', 'were', '~이었다 (be의 과거)', verb_form=pp('irregular-past', s, 'were', 'be'))
    s.g('group', 'group', '단체')
    s.g('decided|to', 'decide to V', '~하기로 결정하다', verb_form=pp('regular-past', s, 'decided', 'decide'),
        verb_construction={'kind': 'to-complement', 'verb_span': s.span_of('decided'), 'lemma': 'decide',
                           'link_spans': [s.span_of('to')], 'review_record': 'decided to name: decide의 목적어 to V.'})
    s.g('name', 'name A B', 'A를 B라고 이름 짓다',
        verb_construction={'kind': 'verb-frame', 'verb_span': s.span_of('name'), 'lemma': 'name', 'link_spans': [],
                           'review_record': 'name the phenomenon “Steve”: A=the phenomenon, B=“Steve”.'})
    s.g('phenomenon', 'phenomenon', '현상', star=W['phenomenon'])
    s.g('Steve', 'Steve', '스티브 (단체가 이 현상에 붙인 이름)', proper=True)
    bs = s.g('based|on', 'based on', '~을 바탕으로', verb_form=pp('past-participle', s, 'based', 'base'))
    s.g('scene', 'scene', '장면')
    s.g('from', 'from', '~에 나오는')
    s.g('animated', 'animated', '애니메이션으로 된')
    s.g('movie', 'movie', '영화')
    rel = s.g('where', 'where S′ V′', 'S′(이/가) V′하는 (앞말을 꾸미는 관계부사)')
    s.g('some', 'some', '몇몇의')
    s.g('characters', 'characters', '등장인물들')
    s.g('give|to', 'give A to B', 'A를 B에게 붙이다 (흔한 뜻: 주다)',
        verb_construction={'kind': 'verb-frame', 'verb_span': s.span_of('give'), 'lemma': 'give',
                           'link_spans': [s.span_of('to', s.text.index('name to'))],
                           'review_record': 'give that name to an unfamiliar object: A=that name, B=an unfamiliar object.'})
    s.glosses[-1]['spans'] = [s.span_of('give'), s.span_of('to', s.text.index('name to'))]
    s.g('that', 'that', '그', at=s.text.index('that name'))
    s.g('name', 'name', '이름', at=s.text.index('that name') + 5)
    s.g('unfamiliar', 'unfamiliar', '낯선, 익숙하지 않은')
    s.g('object', 'object', '물체')
    s.hint('[what they were]', '[그것들[빛의 띠들]이 무엇인지]', span='what they were',
           label='간접의문문 what', links=[(['what'], ['이', '무엇인지'])], refs=[('they', '그것들', '[빛의 띠들]')],
           meaning='그것들이 무엇인지',
           explanation='unsure of의 목적어 자리의 간접의문문 what S′ V′(그것들이 무엇인지). 바깥 형용사 Unsure of는 표시에서 제외.')
    s.hint('an animated movie [where some characters give]', '[몇몇 등장인물들이 붙이는] 한 애니메이션 영화',
           span='an animated movie where some characters give', label='관계부사 where',
           links=[(['where'], ['이', '는'])], meaning='몇몇 등장인물들이 (낯선 물체에 그 이름을) 붙이는 한 애니메이션 영화',
           explanation='관계부사 where가 an animated movie(그 영화 속 장면·상황)를 받아 뒤 절이 꾸민다. S′ some characters, V′ give까지 표시하고 목적어 that name 이하 제외.')
    s.relative_ids = [rel['id']]
    s.brk('from', 'postnominal-preposition', 'from an animated movie는 앞 명사 a scene을 꾸미는 전치사구')
    s.review = ('형용사구 Unsure of + 간접의문 what(관계사 아님), 주절 decided to name A B, based on 분사구, 관계부사 where(선행사 movie). '
                '힌트 2개: 간접의문 what, 필수 관계부사 where. name A B·based on은 각주로 지원. 수동 없음.')
    out.append(s)

    # ---------------- s42 ----------------
    s = S('s42', T['s42'])
    s.ch('After photographing Steve for several years', '몇 년 동안 Steve의 사진을 찍은 후에')
    s.ch('and discussing what it might be,', '그리고 그것이 무엇일지 논의한 후에,')
    s.ch('the group members decided to get help from experts.', '그 단체 구성원들은 전문가들로부터 도움을 받기로 결정했다.')
    s.natural('몇 년 동안 Steve의 사진을 찍고 그것이 무엇일지에 대해 논의한 후에, 그 단체 구성원들은 전문가들로부터 도움을 받기로 결정했다.')
    s.cl('subordinate', 'what', subj='it', verbs=['might', 'be'], marker='what')
    s.cl('main', 'the', subj='the group members', verbs=['decided'])
    f = s.g('After', 'after V-ing', '~한 후에', kind='function', combines_with=[])
    ph = s.g('photographing', 'photograph', '사진을 찍다', verb_form=pp('ing', s, 'photographing', 'photograph'))
    s.g('for', 'for', '~동안')
    s.g('several', 'several', '몇몇의, 여러')
    s.g('years', 'years', '해, 년')
    ds = s.g('discussing', 'discuss', '논의하다', verb_form=pp('ing', s, 'discussing', 'discuss'))
    link(f, ph, ds)
    s.g('what', 'what S′ V′', 'S′(이/가) 무엇인지')
    s.g('it', 'it', '그것이', referent_ko='Steve')
    f2 = s.g('might', 'might V', '~일지도 모른다', kind='function', combines_with=[])
    b = s.g('be', 'be', '~이다')
    link(f2, b)
    s.g('group|members', 'group members', '단체 구성원들')
    s.g('decided|to', 'decide to V', '~하기로 결정하다', verb_form=pp('regular-past', s, 'decided', 'decide'),
        verb_construction={'kind': 'to-complement', 'verb_span': s.span_of('decided'), 'lemma': 'decide',
                           'link_spans': [s.span_of('to')], 'review_record': 'decided to get: decide의 목적어 to V.'})
    s.g('get|help|from', 'get help from', '~로부터 도움을 받다')
    s.g('experts', 'experts', '전문가들')
    s.hint('[After photographing Steve for several years and discussing]', '[몇 년 동안 Steve의 사진을 찍고 논의한 후에]',
           span='After photographing Steve for several years and discussing', label='전치사 after + 동명사',
           links=[(['After', 'ing', ('ing', 1)], ['한 후에'])], meaning='몇 년 동안 Steve의 사진을 찍고 논의한 후에',
           explanation='전치사 After 뒤 동명사 photographing과 discussing이 and로 병렬되어 ‘~하고 ~한 후에’. 두 ing를 모두 after 기능에 연결하고 목적어 what절은 제외.')
    s.hint('[what it might be]', '[그것[Steve]이 무엇일지]', span='what it might be', label='간접의문문 what',
           links=[(['what'], ['이', '무엇일지'])], refs=[('it', '그것', '[Steve]')], meaning='그것이 무엇일지',
           explanation='discussing의 목적어 간접의문문 what S′ V′. S′ it, V′ might be(추측).')
    s.review = '전치사 After + 병렬 동명사(photographing … and discussing), 간접의문 what it might be, 주절 decided to V. 힌트 2개. 수동 없음.'
    out.append(s)

    # ---------------- s43 ----------------
    s = S('s43', T['s43'])
    s.ch('They showed their photos', '그들은 자신들의 사진들을 보여 주었다')
    s.ch('of Steve', 'Steve의')
    s.ch('to a professor', '한 교수에게')
    s.ch('of astronomy', '천문학의')
    s.ch('at a local university', '지역 대학에 있는')
    s.ch('and a scientist', '그리고 한 과학자에게')
    s.ch('at NASA.', 'NASA에 있는.')
    s.natural('그들은 Steve의 사진들을 지역 대학의 천문학 교수와 NASA의 과학자에게 보여 주었다.')
    s.cl('main', 'They', subj='They', verbs=['showed'])
    s.g('They', 'they', '그들은', referent_ko='오로라 추적자 단체 구성원들')
    s.g('showed|to', 'show A to B', 'A를 B에게 보여 주다', verb_form=pp('regular-past', s, 'showed', 'show'),
        verb_construction={'kind': 'verb-frame', 'verb_span': s.span_of('showed'), 'lemma': 'show',
                           'link_spans': [s.span_of('to')], 'review_record': 'showed their photos of Steve to a professor … and a scientist …: A=their photos of Steve, B=두 사람.'})
    s.g('their', 'their', '그들의', referent_ko='오로라 추적자 단체 구성원들')
    s.g('photos', 'photos', '사진들')
    s.g('of', 'of', '~의')
    s.g('professor', 'professor', '교수')
    s.g('of', 'of', '~의', at=s.text.index('of astronomy'))
    s.g('astronomy', 'astronomy', '천문학')
    s.g('at', 'at', '~에 있는')
    s.g('local', 'local', '지역의')
    s.g('university', 'university', '대학')
    s.g('scientist', 'scientist', '과학자')
    s.g('at', 'at', '~에 있는')
    s.g('NASA', 'NASA', '나사 (미국 항공 우주국)', proper=True)
    s.glosses.sort(key=lambda g: g['spans'][0][0])
    for piece, at in [('of', 'of Steve'), ('of', 'of astronomy'), ('at', 'at a local'), ('at', 'at NASA')]:
        s.brk(piece, 'postnominal-preposition', f'{at} …는 앞 명사를 뒤에서 꾸미는 전치사구', after=s.text.index(at))
    s.review = '단일 주절 show A to B. 명사 후치수식 전치사구 4곳(of Steve, of astronomy, at a local university, at NASA) 앞에서 끊음. 힌트 불필요, 수동 없음.'
    out.append(s)

    # ---------------- s44 ----------------
    s = S('s44', T['s44'])
    s.ch('Surprisingly,', '놀랍게도,')
    s.ch('neither of them had any idea', '그들 중 누구도 전혀 알지 못했다')
    s.ch('what Steve was.', 'Steve가 무엇인지.')
    s.natural('놀랍게도, 둘 중 누구도 Steve가 무엇인지 전혀 알지 못했다.')
    s.cl('main', 'neither', subj='neither of them', verbs=['had'])
    s.cl('subordinate', 'what', subj='Steve', verbs=['was'], marker='what')
    s.g('Surprisingly', 'surprisingly', '놀랍게도')
    s.g('neither|of', 'neither of', '~ 중 누구도 …않다')
    s.g('them', 'them', '그들', referent_ko='지역 대학의 천문학 교수와 NASA의 과학자')
    s.g('had|any|idea', 'have any idea', '조금이라도 알다 (had는 have의 과거)')
    s.g('what', 'what S′ V′', 'S′(이/가) 무엇인지')
    s.g('was', 'was', '~이었다 (be의 과거)', verb_form=pp('irregular-past', s, 'was', 'be'))
    s.hint('[what Steve was]', '[Steve가 무엇인지]', span='what Steve was', label='간접의문문 what',
           links=[(['what'], ['가', '무엇인지'])], meaning='Steve가 무엇인지',
           explanation='any idea 뒤에 이어지는 간접의문문 what S′ V′(Steve가 무엇인지). neither가 부정을 담아 ‘누구도 전혀 몰랐다’.')
    s.review = 'neither of them(둘 중 누구도 ~않다) 부정 주어, have any idea + 간접의문 what. 힌트 1개. 수동 없음.'
    out.append(s)

    # ---------------- s45 ----------------
    s = S('s45', T['s45'])
    s.ch('They confirmed', '그들은 확인했다')
    s.ch('that it was not an aurora,', '그것이 오로라가 아니라는 것을,')
    s.ch('but it did not resemble anything', '하지만 그것은 어떤 것과도 닮지 않았다')
    s.ch('they had seen before.', '그들이 이전에 보았던.')
    s.natural('그들은 그것이 오로라가 아니라는 것은 확인했지만, 그것은 그들이 이전에 보았던 어떤 것과도 닮지 않았다.')
    s.cl('main', 'They', subj='They', verbs=['confirmed'])
    s.cl('subordinate', 'that', subj='it', verbs=['was'], marker='that')
    s.cl('main', 'it', subj='it', verbs=['did not resemble'], marker='but', occ=1)
    s.cl('subordinate', 'they', subj='they', verbs=['had', 'seen'], marker='that', omitted=True, occ=0)
    s.clauses[-1]['start'] = s.text.index('they had')
    s.clauses[-1]['subject_spans'] = [[s.text.index('they had'), s.text.index('they had') + 4]]
    s.clauses[-1]['verb_spans'] = [[s.text.index('had seen'), s.text.index('had seen') + 3],
                                  [s.text.index('seen'), s.text.index('seen') + 4]]
    s.g('They', 'they', '그들은', referent_ko='지역 대학의 천문학 교수와 NASA의 과학자')
    s.g('confirmed', 'confirm', '확인하다', star=W['confirm'], verb_form=pp('regular-past', s, 'confirmed', 'confirm'))
    s.g('that', 'that S′ V′', 'S′(이/가) V′라는 것을 (접속사)')
    s.g('it', 'it', '그것이', referent_ko='Steve')
    s.g('was', 'was', '~이었다 (be의 과거)', verb_form=pp('irregular-past', s, 'was', 'be'))
    s.g('not', 'not', '~이 아닌')
    s.g('aurora', 'aurora', '오로라')
    s.g('it', 'it', '그것은', referent_ko='Steve')
    f = s.g('did|not', 'did not V', '~하지 않았다', kind='function', combines_with=[])
    rs = s.g('resemble', 'resemble', '닮다, 비슷하다', star=W['resemble'])
    link(f, rs)
    s.g('anything', 'anything', '(부정문에서) 어떤 것(도)')
    s.g('they', 'they', '그들이', referent_ko='지역 대학의 천문학 교수와 NASA의 과학자', at=s.text.index('they had'))
    f2 = s.g('had', 'had p.p.', '~했다', kind='function', combines_with=[])
    sn = s.g('seen', 'see', '보다 (seen은 see의 p.p.형)', verb_form=pp('perfect-participle', s, 'seen', 'see', f2['id']))
    link(f2, sn)
    s.g('before', 'before', '이전에')
    s.hint('[that it was not an aurora]', '[그것[Steve]이 오로라가 아니라는 것]', span='that it was not an aurora',
           label='명사절 접속사 that', links=[(['that'], ['이', '라는 것'])], refs=[('it', '그것', '[Steve]')],
           meaning='그것이 오로라가 아니라는 것',
           explanation='confirmed의 목적어 that절. be동사라 최소 보어 an aurora까지 표시하며 부정 not을 보존.')
    s.hint('anything [(that) they had seen]', '[그들[교수와 과학자]이 보았던] 어떤 것',
           span='anything they had seen', label='목적격 관계대명사 that 생략', display_mode='omitted-relative',
           omitted_relative='that', links=[(['that'], ['이', '던'])], refs=[('they', '그들', '[교수와 과학자]')],
           meaning='그들이 (이전에) 보았던 어떤 것',
           explanation='anything 뒤에 목적격 관계대명사 that이 생략되고 they had seen이 꾸민다. S′ they, V′ had seen까지 표시하고 before는 제외.')
    s.relative_ids = []
    s.review = ('주절 confirmed + 명사절 that, [but] 독립절 did not resemble + 생략 목적격 관계절 (that) they had seen. '
                '힌트 2개(명사절 that, 필수 생략 관계사). 과거완료 had seen은 힌트 한도로 단위 분석 had p.p.(u3-gp3)에 연결.')
    out.append(s)

    # ---------------- s46 ----------------
    s = S('s46', T['s46'], key=True)
    s.ch('They realized', '그들은 깨달았다')
    s.ch('that the group had discovered a new type of phenomenon', '그 단체가 새로운 유형의 현상을 발견했다는 것을')
    s.ch('that had never been properly studied.', '한 번도 제대로 연구된 적이 없는.')
    s.natural('그들은 그 단체가 제대로 연구된 적이 없는 새로운 유형의 현상을 발견했다는 것을 깨달았다.')
    s.cl('main', 'They', subj='They', verbs=['realized'])
    s.cl('subordinate', 'that', subj='the group', verbs=['had', 'discovered'], marker='that')
    s.cl('subject_relative', 'that', verbs=['had', 'been', 'studied'], marker='that', occ=1)
    s.g('They', 'they', '그들은', referent_ko='지역 대학의 천문학 교수와 NASA의 과학자')
    s.g('realized', 'realize', '깨닫다', verb_form=pp('regular-past', s, 'realized', 'realize'))
    s.g('that', 'that S′ V′', 'S′(이/가) V′라는 것을 (접속사)')
    s.g('group', 'group', '단체')
    f = s.g('had', 'had p.p.', '~했다', kind='function', combines_with=[])
    dc = s.g('discovered', 'discover', '발견하다 (discovered는 discover의 p.p.형)',
             verb_form=pp('perfect-participle', s, 'discovered', 'discover', f['id']))
    link(f, dc)
    q = s.g('a new type of', 'a new type of', '새로운 유형의')
    s.g('phenomenon', 'phenomenon', '현상', star=W['phenomenon'], at=s.text.index('phenomenon'))
    rel = s.g('that', 'that V′', 'V′하는 (관계대명사)', at=s.text.index('that had never'))
    f2 = s.g('had|been', 'had been p.p.', '~되었다', kind='function', combines_with=[], at=s.text.index('had never'))
    s.g('never', 'never', '한 번도 ~않다')
    s.g('properly', 'properly', '제대로')
    sd = s.g('studied', 'studied', '연구된', verb_form=pp('passive-participle', s, 'studied', 'study', f2['id']))
    link(f2, sd)
    s.glosses.sort(key=lambda g: g['spans'][0][0])
    s.prot('a new type of', 'quantity-kind-of', '종류 표현 a new type of가 phenomenon 앞에서 ‘새로운 유형의’로 같은 어순 대응', gloss=q)
    s.hint('[that the group had discovered]', '[그 단체가 발견했다는 것]', span='that the group had discovered',
           label='명사절 접속사 that', links=[(['that'], ['가', '다는 것'])], meaning='그 단체가 발견했다는 것',
           explanation='realized의 목적어 that절. S′ the group, V′ had discovered(깨달은 시점보다 앞선 일)까지 표시.')
    s.hint('phenomenon [that had never been properly studied]', '[한 번도 제대로 연구된 적이 없는] 현상',
           span='phenomenon that had never been properly studied', label='주격 관계대명사 that',
           links=[(['that'], ['는'])], meaning='한 번도 제대로 연구된 적이 없는 현상',
           explanation='phenomenon을 주격 관계대명사 that이 받는다. V′ had never been properly studied(과거완료 수동+부정)를 그대로 표시.')
    s.relative_ids = [rel['id']]
    s.review = ('주절 realized + 명사절 that(과거완료 had discovered) + 주격 관계절 that(과거완료 수동 had never been studied). '
                '힌트 2개(명사절 that, 필수 관계사). had p.p.는 분석 u3-gp3(바로 이 문장), had been p.p.는 보충 u3-gp4로 연결. a new type of 보호.')
    out.append(s)

    # ---------------- s47 ----------------
    s = S('s47', T['s47'])
    s.ch('In order to learn more about it,', '그것에 대해 더 알기 위해,')
    s.ch('NASA funded a citizen science project', 'NASA는 시민 과학 프로젝트에 자금을 지원했다')
    s.ch('involving the public.', '대중을 참여시키는.')
    s.natural('이에 대해 더 자세히 알아보기 위해, NASA는 대중이 참여하는 시민 과학 프로젝트에 자금을 지원했다.')
    s.cl('main', 'NASA', subj='NASA', verbs=['funded'])
    f = s.g('In|order|to', 'in order to V', '~하기 위해', kind='function', combines_with=[])
    ln = s.g('learn', 'learn', '알게 되다, 배우다')
    link(f, ln)
    s.g('more', 'more', '더 많이')
    s.g('about', 'about', '~에 대해')
    s.g('it', 'it', '그것', referent_ko='Steve')
    s.g('funded', 'fund', '자금을 지원하다', verb_form=pp('regular-past', s, 'funded', 'fund'))
    s.g('citizen|science', 'citizen science', '시민 과학')
    s.g('project', 'project', '프로젝트')
    f2 = s.g('involving', 'V-ing', '~하는', kind='function', combines_with=[])
    iv = s.g('involving', 'involve', '참여시키다, 포함하다', same=True, verb_form=pp('ing', s, 'involving', 'involve'))
    link(f2, iv)
    s.g('public', 'public', '대중')
    s.hint('a citizen science project [involving the public]', '[대중을 참여시키는] 시민 과학 프로젝트',
           span='a citizen science project involving the public', label='현재분사 후치수식', links=[(['ing'], ['는'])],
           meaning='대중을 참여시키는 시민 과학 프로젝트',
           explanation='현재분사 involving이 목적어 the public을 거느리고 앞 명사 a citizen science project를 뒤에서 꾸민다.')
    s.review = 'in order to V 목적, 주절 funded, involving the public 현재분사 후치수식 → 힌트. NASA는 앞 문장 첫 등장 고유명사 반복. 수동 없음.'
    out.append(s)

    # ---------------- s48 ----------------
    s = S('s48', T['s48'])
    s.ch('The project asked ordinary people', '그 프로젝트는 일반인들에게 요청했다')
    s.ch('to gather photos', '사진들을 모으도록')
    s.ch('of Steve', 'Steve의')
    s.ch('and send them to NASA.', '그리고 그것들을 NASA에 보내도록.')
    s.natural('그 프로젝트는 일반인들에게 Steve의 사진을 모아 NASA에 보내 달라고 요청했다.')
    s.cl('main', 'The', subj='The project', verbs=['asked'])
    s.g('project', 'project', '프로젝트')
    s.g('asked|to', 'ask A to V', 'A에게 ~하도록 요청하다', verb_form=pp('regular-past', s, 'asked', 'ask'),
        verb_construction={'kind': 'verb-frame', 'verb_span': s.span_of('asked'), 'lemma': 'ask',
                           'link_spans': [s.span_of('to')], 'review_record': 'asked ordinary people to gather … and send …: A=ordinary people, to V=to gather/send(병렬).'})
    s.g('ordinary', 'ordinary', '평범한, 일반의')
    s.g('people', 'people', '사람들')
    s.g('gather', 'gather', '모으다')
    s.g('photos', 'photos', '사진들')
    s.g('of', 'of', '~의')
    s.g('send|to', 'send A to B', 'A를 B에게 보내다',
        verb_construction={'kind': 'verb-frame', 'verb_span': s.span_of('send'), 'lemma': 'send',
                           'link_spans': [s.span_of('to', s.text.index('send'))], 'review_record': 'send them to NASA: A=them, B=NASA.'})
    s.g('them', 'them', '그것들을', referent_ko='Steve의 사진들')
    s.brk('of', 'postnominal-preposition', 'of Steve는 앞 명사 photos를 꾸미는 전치사구')
    s.hint('asked ordinary people [to gather]', '일반인들에게 [모으도록] 요청했다', span='asked ordinary people to gather',
           label='ask A to V 구문', links=[(['asked', 'to'], ['에게', '도록'])], emphasis_policy='ko-only-verb-construction',
           meaning='일반인들에게 (사진을) 모으도록 요청했다',
           explanation='ask A to V: A(ordinary people)에게 ~하도록 요청하다. to gather와 (to) send가 and로 병렬. 동사 구문이라 한국어 조사 에게·어미 도록만 강조.')
    s.review = '단일 주절 ask A to V(병렬 to gather … and send …). 더 우선하는 절 연결이 없어 동사 구문 힌트. 수동 없음.'
    out.append(s)

    # ---------------- s49 ----------------
    s = S('s49', T['s49'])
    s.ch('It is still in progress today.', '그것은 오늘날에도 여전히 진행 중이다.')
    s.natural('그 프로젝트는 오늘날에도 여전히 진행 중이다.')
    s.cl('main', 'It', subj='It', verbs=['is'])
    s.g('It', 'it', '그것은', referent_ko='NASA가 지원한 시민 과학 프로젝트')
    s.g('is', 'is', '~이다')
    s.g('still', 'still', '여전히')
    s.g('in|progress', 'in progress', '진행 중인')
    s.g('today', 'today', '오늘날')
    s.review = '단일 주절. 힌트 불필요.'
    out.append(s)

    # ---------------- s50 ----------------
    s = S('s50', T['s50'])
    s.ch('In honor of the aurora chasers', '오로라 추적자들에게 경의를 표하여')
    s.ch('who first discovered the phenomenon,', '그 현상을 처음 발견했던,')
    s.ch('the name “Steve” has been kept.', '‘Steve’라는 이름은 유지되어 왔다.')
    s.natural('이 현상을 처음 발견한 오로라 추적자들에게 경의를 표하여 ‘Steve’라는 이름은 유지되었다.')
    s.cl('subject_relative', 'who', verbs=['discovered'], marker='who')
    s.cl('main', 'the', subj='the name “Steve”', verbs=['has been kept'], occ=2)
    s.g('In|honor|of', 'in honor of', '~에게 경의를 표하여, ~을 기리어')
    s.g('aurora|chasers', 'aurora chasers', '오로라 추적자들')
    rel = s.g('who', 'who V′', 'V′했던 (관계대명사)')
    s.g('first', 'first', '처음')
    s.g('discovered', 'discover', '발견하다', verb_form=pp('regular-past', s, 'discovered', 'discover'))
    s.g('phenomenon', 'phenomenon', '현상', star=W['phenomenon'])
    s.g('name', 'name', '이름')
    f = s.g('has|been', 'have been p.p.', '~되어 왔다', kind='function', combines_with=[])
    kp = s.g('kept', 'kept', '유지된', verb_form=pp('passive-participle', s, 'kept', 'keep', f['id']))
    link(f, kp)
    s.hint('the aurora chasers [who first discovered]', '[처음 발견했던] 오로라 추적자들', span='the aurora chasers who first discovered',
           label='주격 관계대명사 who', links=[(['who'], ['던'])], meaning='(그 현상을) 처음 발견했던 오로라 추적자들',
           explanation='the aurora chasers를 주격 관계대명사 who가 받아 first discovered the phenomenon이 꾸민다. 과거 관형 연결 ~했던.')
    s.vf_hint(fn=f, lex=kp, en='has been kept', ko='유지되어 왔다', formula='have been p.p.', step_form='kept', step_ko='유지된',
              en_mark=['has been'], ko_mark=['되어 왔다'], span='the name “Steve” has been kept', meaning='유지되어 왔다',
              explanation='완료 수동 has been kept: (처음 붙인 뒤 지금까지) 유지되어 왔다. 주어 the name “Steve” 제외.')
    s.relative_ids = [rel['id']]
    s.review = '부사구 In honor of + 주격 관계절 who, 주절 완료 수동 has been kept. 힌트 2개(필수 관계사, 완료 수동 기능 결합).'
    out.append(s)

    # ---------------- s51 ----------------
    s = S('s51', T['s51'])
    s.ch('However,', '그러나,')
    s.ch('it is now written in all capital letters', '그것은 이제 모두 대문자로 쓰인다')
    s.ch('and stands for “Strong Thermal Emission Velocity Enhancement.”', '그리고 ‘Strong Thermal Emission Velocity Enhancement’를 의미한다.')
    s.natural('그러나 그것은 이제 모두 대문자로 쓰이며, ‘속도 증가에 따른 강한 열 방출(Strong Thermal Emission Velocity Enhancement)’을 의미한다.')
    s.cl('main', 'it', subj='it', verbs=['is', 'written', 'and', 'stands'])
    s.g('However', 'however', '그러나')
    s.g('it', 'it', '그것은', referent_ko='Steve라는 이름')
    f = s.g('is', 'be p.p.', '~되다', kind='function', combines_with=[])
    s.g('now', 'now', '이제')
    wr = s.g('written', 'written', '쓰인', verb_form=pp('passive-participle', s, 'written', 'write', f['id']))
    link(f, wr)
    s.g('in', 'in', '~로 (흔한 뜻: ~안에)')
    s.g('all', 'all', '모두, 모든')
    s.g('capital|letters', 'capital letters', '대문자')
    s.g('stands|for', 'stand for', '~을 의미하다, ~을 나타내다', verb_form={'usage': 'third-person-singular',
        'source_span': s.span_of('stands'), 'lemma': 'stand', 'review_record': '주어 it(3인칭 단수)의 일반동사 stands → 원형 stand.'})
    s.g('Strong Thermal Emission Velocity Enhancement', 'Strong Thermal Emission Velocity Enhancement',
        '속도 증가에 따른 강한 열 방출 (STEVE의 각 글자가 나타내는 말, 교과서 해석)', proper=True)
    s.vf_hint(fn=f, lex=wr, en='is now written', ko='이제 쓰인다', formula='be p.p.', step_form='written', step_ko='쓰인',
              en_mark=['is'], ko_mark=['인다'], span='it is now written', meaning='이제 (모두 대문자로) 쓰인다',
              explanation='빈 힌트 문장의 수동태 후보: is now written(현재 수동). 표시 범위 안 부사 now 보존, 주어와 in all capital letters 제외.')
    s.review = ('주어 it의 병렬 동사 is written and stands for. 관계사·접속사절 없음 → 빈 힌트 문장의 수동태 후보로 be p.p. 기능 결합 힌트. '
                '인용된 긴 이름은 고유명사 한 각주.')
    out.append(s)

    # ---------------- s52 ----------------
    s = S('s52', T['s52'], key=True)
    s.ch('Experts have acknowledged', '전문가들은 인정했다')
    s.ch('that it is the dedicated members', '바로 헌신적인 구성원들이라는 것을')
    s.ch('of the aurora chasers group', '오로라 추적자 단체의')
    s.ch('that deserve the credit', '공로를 받을 만한 것은')
    s.ch('for discovering STEVE.', 'STEVE를 발견한 것에 대한.')
    s.natural('전문가들은 STEVE를 발견한 공로를 받을 만한 사람들은 바로 오로라 추적자 단체의 헌신적인 구성원들임을 인정했다.')
    s.cl('main', 'Experts', subj='Experts', verbs=['have', 'acknowledged'])
    s.cl('subordinate', 'that', subj='it', verbs=['is'], marker='that')
    s.cl('subject_relative', 'that', verbs=['deserve'], marker='that', occ=1)
    s.g('Experts', 'experts', '전문가들')
    f = s.g('have', 'have p.p.', '~했다', kind='function', combines_with=[])
    ac = s.g('acknowledged', 'acknowledge', '인정하다 (acknowledged는 acknowledge의 p.p.형)', star=W['acknowledged'],
             verb_form=pp('perfect-participle', s, 'acknowledged', 'acknowledge', f['id']))
    link(f, ac)
    s.g('that', 'that S′ V′', 'S′(이/가) V′라는 것을 (접속사)')
    s.g('it|is|that', 'It is A that V′', 'V′하는 것은 바로 A이다', at=s.text.index('it is'))
    s.glosses[-1]['spans'] = [s.span_of('it', s.text.index('it is')), s.span_of('is', s.text.index('it is')),
                              s.span_of('that', s.text.index('that deserve'))]
    s.g('dedicated', 'dedicated', '헌신적인', star=W['dedicated'])
    s.g('members', 'members', '구성원들')
    s.g('of', 'of', '~의')
    s.g('aurora|chasers|group', 'aurora chasers group', '오로라 추적자 단체')
    s.g('deserve', 'deserve', '~을 받을 만하다', star=W['deserve'])
    s.g('credit', 'credit', '공로, 인정')
    s.g('for', 'for', '~에 대한')
    f2 = s.g('discovering', 'V-ing', '~하는 것', kind='function', combines_with=[])
    dv = s.g('discovering', 'discover', '발견하다', same=True, verb_form=pp('ing', s, 'discovering', 'discover'))
    link(f2, dv)
    s.g('STEVE', 'STEVE', '스티브 (Strong Thermal Emission Velocity Enhancement의 머리글자)', proper=True)
    s.brk('of', 'postnominal-preposition', 'of the aurora chasers group은 앞 명사 members를 꾸미는 전치사구')
    s.brk('for', 'postnominal-preposition', 'for discovering STEVE는 앞 명사 the credit을 꾸미는 전치사구')
    s.hint('it is the dedicated members of the aurora chasers group [that deserve]',
           '[받을 만한] 것은 바로 오로라 추적자 단체의 헌신적인 구성원들이다',
           span='it is the dedicated members of the aurora chasers group that deserve', label='It ~ that 강조 구문',
           links=[(['it is', ('that', 0)], ['것은 바로', '이다'])],
           meaning='(공로를) 받을 만한 것은 바로 오로라 추적자 단체의 헌신적인 구성원들이다',
           explanation='It is A that V′: A(the dedicated members of the aurora chasers group)를 강조한다.')
    s.review = ('주절 have acknowledged + 명사절 that + 그 안의 It is A that 강조 구문(두 번째 that은 강조의 that이라 관계사 목록에 넣지 않음). '
                '힌트 1개(강조 구문). 명사절 that 힌트는 강조 구문 힌트와 범위가 겹치고 초점이 섞여 삭제(재검수 LB 판단 3, 사용자 결정 B). 현재완료 have acknowledged는 분석 보충 have p.p.(u3-gp5)에 연결. of/for 후치수식 경계.')
    s.relative_ids = []
    out.append(s)

    # ---------------- s53 ----------------
    s = S('s53', T['s53'])
    s.ch('If it had not been for them,', '그들이 없었다면,')
    s.ch('it might have remained unnoticed forever.', '그것은 영원히 알려지지 않은 채로 남았을지도 모른다.')
    s.natural('만약 그들이 없었다면, 그것은 영원히 알려지지 못한 채 남았을지도 모른다.')
    s.cl('subordinate', 'If', subj='it', verbs=['had not been'], marker='If')
    s.cl('main', 'it', subj='it', verbs=['might have remained'], occ=1)
    s.g('If|it|had|not|been|for', 'If it had not been for A', 'A(이/가) 없었다면')
    s.g('them', 'them', '그들이', referent_ko='오로라 추적자 단체의 헌신적인 구성원들')
    s.g('it', 'it', '그것은', referent_ko='STEVE', at=s.text.index('it might'))
    f = s.g('might|have', 'might have p.p.', '~했을지도 모른다', kind='function', combines_with=[])
    rm = s.g('remained', 'remain', '(~인 채로) 남다 (remained는 remain의 p.p.형)',
             verb_form=pp('perfect-participle', s, 'remained', 'remain', f['id']))
    link(f, rm)
    s.g('unnoticed', 'unnoticed', '알려지지 않은, 눈에 띄지 않은')
    s.g('forever', 'forever', '영원히')
    s.hint('[If it had not been for] them', '그들[오로라 추적자들]이 [없었다면]', span='If it had not been for them',
           label='가정법 과거완료 If it had not been for', links=[(['If it had not been for'], [('이', 0), '없었다면'])],
           refs=[('them', '그들', '[오로라 추적자들]')], meaning='그들이 없었다면',
           explanation='If it had not been for A: A가 없었다면. A=them(오로라 추적자 단체 구성원들). 주절 might have p.p.와 짝.')
    s.vf_hint(fn=f, lex=rm, en='might have remained', ko='남았을지도 모른다', formula='might have p.p.', step_form='remain',
              step_ko='남다', en_mark=['might have'], ko_mark=['았을지도 모른다'], span='it might have remained unnoticed forever',
              meaning='(알려지지 않은 채로) 남았을지도 모른다',
              explanation='조동사 완료 might have p.p.: 과거에 ~했을지도 모른다(가정법 과거완료 주절). 보어 unnoticed·forever 제외.')
    s.review = '가정법 과거완료 If it had not been for A + 주절 might have p.p. 힌트 2개(if 구문, 조동사 완료 기능 결합).'
    out.append(s)

    # ---------------- s54 ----------------
    s = S('s54', T['s54'])
    s.ch('There are many interesting theories', '많은 흥미로운 이론들이 있다')
    s.ch('about STEVE,', 'STEVE에 대한,')
    s.ch('but none of them have been proven for certain.', '하지만 그것들 중 어느 것도 확실하게 증명되지 않았다.')
    s.natural('STEVE에 대한 흥미로운 이론들은 많지만, 그중 어느 것도 확실하게 증명되지는 않았다.')
    s.cl('main', 'There', subj='many interesting theories about STEVE', verbs=[], vfirst=['are'],
         disp='many interesting theories', disp_review='중심명사 theories까지 표시하고 뒤에서 꾸미는 about STEVE는 제외')
    s.cl('main', 'none', subj='none of them', verbs=['have been proven'], marker='but')
    s.g('are', 'are', '있다')
    s.g('many', 'many', '많은')
    s.g('interesting', 'interesting', '흥미로운')
    s.g('theories', 'theories', '이론들')
    s.g('about', 'about', '~에 대한')
    s.g('none|of', 'none of', '~ 중 어느 것도 …않다')
    s.g('them', 'them', '그것들', referent_ko='STEVE에 대한 흥미로운 이론들')
    f = s.g('have|been', 'have been p.p.', '~되었다', kind='function', combines_with=[])
    pv = s.g('proven', 'proven', '증명된', verb_form=pp('passive-participle', s, 'proven', 'prove', f['id']))
    link(f, pv)
    s.g('for|certain', 'for certain', '확실하게')
    s.extra_cov[tuple(s.span_of('There'))] = {'exemption': 'below-middle1-unneeded', 'level': 'below-middle1',
        'reason': '유도부사 there(초등 기초어)는 따로 해석하지 않으며 뒤 are 각주의 ‘있다’로 뜻을 지원'}
    s.brk('about', 'postnominal-preposition', 'about STEVE는 앞 명사 theories를 꾸미는 전치사구')
    s.vf_hint(fn=f, lex=pv, en='have been proven', ko='증명되었다', formula='have been p.p.', step_form='proven', step_ko='증명된',
              en_mark=['have been'], ko_mark=['되었다'], span='none of them have been proven for certain',
              meaning='증명되었다 (none과 함께: 어느 것도 증명되지 않았다)',
              explanation='빈 힌트 문장의 수동태 후보: 완료 수동 have been proven. 부정은 주어 none이 담당하므로 동사구 자체는 ‘증명되었다’. 주어·for certain 제외.')
    s.review = ('유도부사 There + are, [but] none of them have been proven(부정은 none이 담당). 관계사·접속사절 없음 → 빈 힌트 문장의 완료 수동 기능 결합 힌트. '
                'STEVE는 앞 문장 첫 등장 고유명사 반복.')
    out.append(s)

    # ---------------- s55 ----------------
    s = S('s55', T['s55'])
    s.ch('Scientists and citizens continue to collaborate', '과학자들과 시민들은 계속 협력한다')
    s.ch('to solve this mystery,', '이 수수께끼를 풀기 위해,')
    s.ch('and they are learning more and more about STEVE', '그리고 그들은 STEVE에 대해 점점 더 많은 것을 알아 가고 있다')
    s.ch('every day.', '매일.')
    s.natural('과학자들과 시민들은 이 수수께끼를 풀기 위해 계속 협력하고 있으며, 매일 STEVE에 대해 점점 더 많은 것을 알아 가고 있다.')
    s.cl('main', 'Scientists', subj='Scientists and citizens', verbs=['continue'])
    s.cl('main', 'they', subj='they', verbs=['are learning'], marker='and')
    s.g('Scientists', 'scientists', '과학자들')
    s.g('citizens', 'citizens', '시민들')
    s.g('continue|to', 'continue to V', '계속 ~하다',
        verb_construction={'kind': 'to-complement', 'verb_span': s.span_of('continue'), 'lemma': 'continue',
                           'link_spans': [s.span_of('to')], 'review_record': 'continue to collaborate: continue의 목적어 to V.'})
    s.g('collaborate', 'collaborate', '협력하다')
    f = s.g('to', 'to V', '~하기 위해', kind='function', combines_with=[], at=s.text.index('to solve'))
    sv = s.g('solve', 'solve', '풀다, 해결하다')
    link(f, sv)
    s.g('this', 'this', '이')
    s.g('mystery', 'mystery', '수수께끼, 미스터리')
    s.g('they', 'they', '그들은', referent_ko='과학자들과 시민들')
    f2 = s.g('are', 'be V-ing', '~하고 있다', kind='function', combines_with=[])
    lr = s.g('learning', 'learn', '알게 되다, 배우다', verb_form=pp('ing', s, 'learning', 'learn'))
    link(f2, lr)
    s.g('more|and|more', 'more and more', '점점 더 많은 것')
    s.g('about', 'about', '~에 대해')
    s.g('every|day', 'every day', '매일')
    s.review = '두 독립 주절(and): continue to V + 목적 to V, 현재진행 are learning. 관계사·접속사절·수동 없음 → 힌트 없음.'
    out.append(s)
    return out


UNIT = {
    'id': 'u3', 'source_id': 'src', 'paragraph_ids': ['p06', 'p07', 'p08', 'p09'],
    'sentence_ids': [f's{n:02d}' for n in range(34, 56)],
    'today_words': [
        {'id': W['informal'], 'text': 'informal', 'meaning_ko': '비공식적인'},
        {'id': W['phenomenon'], 'text': 'phenomenon', 'meaning_ko': '현상'},
        {'id': W['possess'], 'text': 'possess', 'meaning_ko': '지니다, 가지다'},
        {'id': W['resemble'], 'text': 'resemble', 'meaning_ko': '닮다, 비슷하다'},
        {'id': W['acknowledged'], 'text': 'acknowledge', 'meaning_ko': '인정하다'},
        {'id': W['dedicated'], 'text': 'dedicated', 'meaning_ko': '헌신적인'},
        {'id': W['deserve'], 'text': 'deserve', 'meaning_ko': '~을 받을 만하다'},
        {'id': W['confirm'], 'text': 'confirm', 'meaning_ko': '확인하다'},
    ],
}


def analysis(_):
    return {
        'heading_kind': '제목',
        'title_or_topic_en': 'STEVE: A Discovery by Aurora Chasers',
        'title_or_topic_ko': 'STEVE: 오로라 추적자들의 발견',
        'intent_ko': '오로라 사진을 찍던 평범한 사람들이 새로운 하늘 현상 STEVE를 발견하고 과학자들과 함께 연구하게 된 사례를 통해, 시민도 새로운 과학적 발견을 이끌 수 있음을 보여 주는 글이다.',
        'flow': [
            {'sentence_ids': ['s34', 's35', 's36'], 'label': '배경',
             'text_ko': '캐나다 앨버타의 ‘오로라 추적자들’은 온라인 모임을 만들어 밤에 오로라 사진을 찍고 서로 공유했다.'},
            {'sentence_ids': [f's{n}' for n in range(37, 42)], 'label': '발견',
             'text_ko': '2014년 여름, 그들은 오로라와 비슷하지만 다른 특징을 지닌 녹색·보라색 빛의 띠를 보았고, 영화 장면을 따서 ‘Steve’라는 이름을 붙였다.'},
            {'sentence_ids': [f's{n}' for n in range(42, 50)], 'label': '전문가와의 협력',
             'text_ko': '추적자들은 대학 교수와 NASA 과학자에게 사진을 보여 주었지만, 전문가들도 Steve가 무엇인지 몰랐고 제대로 연구된 적 없는 새로운 현상임을 깨달았다. 그래서 NASA는 대중의 사진을 모으는 시민 과학 프로젝트를 지원했고, 이 프로젝트는 지금도 진행 중이다.'},
            {'sentence_ids': [f's{n}' for n in range(50, 56)], 'label': '의의',
             'text_ko': '처음 발견한 사람들을 기려 이름은 STEVE로 유지되었고, 전문가들도 그 공로를 인정했다. 아직 밝혀지지 않은 수수께끼를 과학자와 시민이 함께 풀어 가고 있다.'},
        ],
        'easy_explanations': [
            {'sentence_id': 's37', 'explanatory_sentences': [
                '37번 문장부터 이야기의 중심 사건이 시작된다.',
                '밤에 오로라 사진을 찍으러 다니던 사람들이 하늘에서 평소와 다른 이상한 무언가를 보기 시작했다.',
                '38~40번 문장은 그것이 어떤 모습이었고 얼마나 오래 보였는지 자세히 설명한다.']},
            {'sentence_id': 's41', 'explanatory_sentences': [
                '41번 문장은 이 현상에 왜 ‘Steve’라는 사람 이름이 붙었는지 알려 준다.',
                '추적자들은 그 빛이 정확히 무엇인지 알 수 없었다.',
                '어떤 애니메이션 영화에는 몇몇 등장인물들이 낯선 물체에 ‘Steve’라는 이름을 붙이는 장면이 있다.',
                '추적자들도 그 장면처럼 정체를 모르는 빛에 ‘Steve’라는 이름을 붙였다.']},
            {'sentence_id': 's52', 'explanatory_sentences': [
                '52번 문장은 이 발견의 공로가 누구에게 있는지 밝힌다.',
                '전문 과학자들이 STEVE를 처음 발견한 것이 아니다.',
                '몇 년 동안 꾸준히 사진을 찍고 전문가에게 보여 준 오로라 추적자들 덕분에 STEVE가 알려졌다.',
                '그래서 전문가들도 그 공로가 추적자들에게 있다고 인정했다.',
                '이 점이 ‘시민도 과학에 기여할 수 있다’는 글 전체의 생각을 뒷받침한다.']},
        ],
        'grammar_points': [
            {'id': 'u3-gp1', 'sentence_id': 's41', 'span': 'an animated movie where some characters give that name to an unfamiliar object',
             'title': '명사 + where S′ V′: S′가 V′하는 명사 (관계부사)', 'formula_key': 'where S′ V′',
             'explanation': '공식: 명사 + where S′ V′ — S′(이/가) V′하는 명사. 선행사 = an animated movie(한 애니메이션 영화: 장면이 펼쳐지는 곳), '
                            'S′ = some characters(몇몇 등장인물들), V′ = give(붙이다, give A to B), A = that name(그 이름), to B = to an unfamiliar object(낯선 물체에). '
                            '→ 몇몇 등장인물들이 낯선 물체에 그 이름을 붙이는 한 애니메이션 영화.',
             'practice': {'span': 'an animated movie where some characters give that name',
                          'formula_support': {'en': 'where S′ V′', 'ko': 'S′(이/가) V′하는 (앞말을 꾸미는 관계부사)'},
                          'support': [('s41', 'animated'), ('s41', 'movie'), ('s41', 'some'), ('s41', 'characters'),
                                      ('s41', 'give A to B'), ('s41', 'that'), ('s41', 'name')],
                          'support_overrides': [{'gloss': ('s41', 'give A to B'), 'form': 'give', 'meaning_ko': '붙이다 (흔한 뜻: 주다)',
                                                 'review_record': '연습 범위에 to B가 없어 give A to B의 A/B 틀 대신 기본 동사 give만 지원'}],
                          'answer_ko': '몇몇 등장인물들이 그 이름을 붙이는 한 애니메이션 영화'}},
            {'id': 'u3-gp2', 'sentence_id': 's52', 'span': 'it is the dedicated members of the aurora chasers group that deserve the credit for discovering STEVE',
             'title': 'It is A that V′: V′하는 것은 바로 A이다 (강조 구문)', 'formula_key': 'It is A that V′',
             'explanation': '공식: It is A that V′ — V′하는 것은 바로 A이다. A = the dedicated members of the aurora chasers group(오로라 추적자 단체의 헌신적인 구성원들), '
                            'V′ = deserve(~을 받을 만하다), 목적어 = the credit(공로), 뒤에서 꾸미는 말 = for discovering STEVE(STEVE를 발견한 데 대한). '
                            '→ STEVE를 발견한 공로를 받을 만한 것은 바로 오로라 추적자 단체의 헌신적인 구성원들이다.',
             'practice': {'span': 'it is the dedicated members of the aurora chasers group that deserve the credit',
                          'formula_support': {'en': 'It is A that V′', 'ko': 'V′하는 것은 바로 A이다'},
                          'support': [('s52', 'dedicated'), ('s52', 'members'), ('s52', 'of'), ('s52', 'aurora chasers group'),
                                      ('s52', 'deserve'), ('s52', 'credit')],
                          'answer_ko': '공로를 받을 만한 것은 바로 오로라 추적자 단체의 헌신적인 구성원들이다'}},
            {'id': 'u3-gp3', 'sentence_id': 's46', 'span': 'They realized that the group had discovered a new type of phenomenon',
             'title': 'had p.p.: ~했다 (과거완료, 기준이 되는 과거보다 먼저)', 'formula_key': 'had p.p.',
             'explanation': '공식: had p.p. — ~했다. 과거의 한 시점(realized, 깨달았다)보다 먼저 일어난 일을 나타낸다. '
                            'had = 과거완료 표지, p.p. = discovered(discover의 p.p.형, 발견하다), 주어 = the group(그 단체), 목적어 = a new type of phenomenon(새로운 유형의 현상). '
                            '→ 그 단체가 새로운 유형의 현상을 발견했다. 발견이 깨달음(realized)보다 먼저 일어난 일이다.',
             'practice': {'span': 'the group had discovered a new type of phenomenon',
                          'formula_support': {'en': 'had p.p.', 'ko': '~했다'},
                          'support': [('s46', 'group'), ('s46', 'discover'), ('s46', 'a new type of'), ('s46', 'phenomenon')],
                          'answer_ko': '그 단체가 새로운 유형의 현상을 발견했다'}},
            {'id': 'u3-gp4', 'sentence_id': 's46', 'span': 'phenomenon that had never been properly studied',
             'title': 'had been p.p.: ~되었다 (과거완료 수동)', 'formula_key': 'had been p.p.',
             'explanation': '공식: had been p.p. — ~되었다(그때까지). had been = 과거완료 수동 표지, p.p. = studied(연구된), never = 한 번도 ~않다, properly = 제대로. '
                            '→ 한 번도 제대로 연구된 적이 없는 (현상).',
             'supplemental': {'function': ('s46', 'had been p.p.', 0),
                              'reason': 's46의 had never been studied는 명사절 that·필수 관계사 힌트 2개로 결합 힌트를 둘 수 없고, 기본 분석에 had been p.p. 설명이 없어 대표 사례를 1회 보충'},
             'practice': {'span': 'had never been properly studied',
                          'formula_support': {'en': 'had been p.p.', 'ko': '~되었다'},
                          'support': [('s46', 'never'), ('s46', 'properly'), ('s46', 'studied')],
                          'answer_ko': '한 번도 제대로 연구된 적이 없었다'}},
            {'id': 'u3-gp5', 'sentence_id': 's52', 'span': 'Experts have acknowledged',
             'title': 'have p.p.: ~했다 (현재완료)', 'formula_key': 'have p.p.',
             'explanation': '공식: have p.p. — ~했다(그 결과가 지금까지 이어짐). have = 현재완료 표지, p.p. = acknowledged(acknowledge의 p.p.형, 인정하다), 주어 = Experts(전문가들). '
                            '→ 전문가들은 인정했다. 지금도 그 인정이 유효하다는 뜻을 담는다.',
             'supplemental': {'function': ('s52', 'have p.p.', 0),
                              'reason': 's52의 have acknowledged는 핵심인 강조 구문 힌트가 있어 결합 힌트를 추가하지 않고, 기본 분석에 have p.p. 설명이 없어 대표 사례를 1회 보충'},
             'practice': {'span': 'Experts have acknowledged',
                          'formula_support': {'en': 'have p.p.', 'ko': '~했다'},
                          'support': [('s52', 'experts'), ('s52', 'acknowledge')],
                          'answer_ko': '전문가들은 인정했다'}},
        ],
        'formula_routes': [
            {'function': ('s45', 'had p.p.', 0), 'route': 'analysis', 'grammar_point_id': 'u3-gp3',
             'review_record': 'had seen: 힌트 2개(명사절 that·생략 관계사)로 분석 대표 u3-gp3에 연결'},
            {'function': ('s46', 'had p.p.', 0), 'route': 'analysis', 'grammar_point_id': 'u3-gp3',
             'review_record': 'had discovered: 기본 분석 u3-gp3의 대표 사례'},
            {'function': ('s46', 'had been p.p.', 0), 'route': 'analysis', 'grammar_point_id': 'u3-gp4',
             'review_record': 'had never been studied: 보충 분석 u3-gp4'},
            {'function': ('s50', 'have been p.p.', 0), 'route': 'hint', 'hint_index': 1,
             'review_record': 'has been kept: 완료 수동 기능 결합 힌트'},
            {'function': ('s51', 'be p.p.', 0), 'route': 'hint', 'hint_index': 0,
             'review_record': 'is written: 빈 힌트 문장의 수동태 후보 힌트'},
            {'function': ('s52', 'have p.p.', 0), 'route': 'analysis', 'grammar_point_id': 'u3-gp5',
             'review_record': 'have acknowledged: 보충 분석 u3-gp5'},
            {'function': ('s53', 'might have p.p.', 0), 'route': 'hint', 'hint_index': 1,
             'review_record': 'might have remained: 조동사 완료 기능 결합 힌트'},
            {'function': ('s54', 'have been p.p.', 0), 'route': 'hint', 'hint_index': 0,
             'review_record': 'have been proven: 빈 힌트 문장의 완료 수동 힌트'},
        ],
        'relations': [
            {'head': {'id': 'u3-r1h', 'text': 'exceptional', 'meaning_ko': '특별한, 뛰어난'},
             'synonym': {'id': 'u3-r1s', 'text': 'outstanding', 'meaning_ko': '뛰어난, 두드러진'},
             'antonym': {'id': 'u3-r1a', 'text': 'average', 'meaning_ko': '평범한, 보통의'}},
            {'head': {'id': 'u3-r2h', 'text': 'unfamiliar', 'meaning_ko': '낯선, 익숙하지 않은'},
             'synonym': {'id': 'u3-r2s', 'text': 'strange', 'meaning_ko': '낯선, 이상한'},
             'antonym': {'id': 'u3-r2a', 'text': 'familiar', 'meaning_ko': '익숙한, 친숙한'}},
            {'head': {'id': 'u3-r3h', 'text': 'collaborate', 'meaning_ko': '협력하다'},
             'synonym': {'id': 'u3-r3s', 'text': 'cooperate', 'meaning_ko': '협력하다, 협동하다'},
             'antonym': {'id': 'u3-r3a', 'text': 'compete', 'meaning_ko': '경쟁하다'}},
        ],
    }


def workbook():
    return {
        'relation_order': ['u3-r2s', 'u3-r1a', 'u3-r3h', 'u3-r2a', 'u3-r1h', 'u3-r3s', 'u3-r2h', 'u3-r3a', 'u3-r1s'],
        'key_sentence_ids': ['s46', 's52'],
        'question_id': 'Q03',
        'syntax_point_ids': ['u3-gp1', 'u3-gp2', 'u3-gp3', 'u3-gp4', 'u3-gp5'],
    }
