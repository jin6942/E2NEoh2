"""워크북 실전문제(Q01~Q05)와 미니 모의고사 3회(Q06~Q20) 원고 — 공통영어2 YBM(박준언) 2과.

지문·정답 위치는 원문에서 계산하고 question_source.build_view로 복원을 검증한다.
공통영어2이므로 분량 비교는 고1(grade 1) 동유형 공식 표본을 사용하고, 모의 1회는 일반 3 + 장문 2 = 5문항이다.

회차 편성 원칙: 한 회차 안에서 빈칸·어휘·순서·삽입·무관 문항의 정답 근거가 다른 문항 지문에
원형으로 드러나지 않도록 원문 구간을 나눈다.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / '스킬수정본' / 'gyogwaseo-unified' / 'scripts'))
from question_source import build_view, recommended_benchmarks, LENGTH_PROFILE_ID  # noqa: E402

GRADE = 1
CIRCLED = '①②③④⑤'
ORDER = [['A', 'C', 'B'], ['B', 'A', 'C'], ['B', 'C', 'A'], ['C', 'A', 'B'], ['C', 'B', 'A']]
BENCH_SHORT_NOTE = '동일 유형 공식 표본보다 짧아 독립 검수에서 분량·정보 전개를 확인해야 함. '

Q = []  # 작성 순서 = 출력 순서


def q(**kw):
    Q.append(kw)


# ================================================================ 워크북 실전문제
q(id='Q01', set_id='workbook', number=1, unit_id='u1', type='주제', first='s01', last='s17',
  question='다음 글의 주제로 가장 적절한 것은?',
  choices=['strange sounds that often come from old kitchen taps',
           'people rushing to buy necessities as a water crisis worsens',
           'shoppers’ strong desire for luxuries on Black Friday',
           'the media’s efforts to keep people quiet about the drought',
           'a normal family trip to a crowded shopping mall'],
  answer=2,
  uses=[('u1-r3s', 2, 'necessities', 'necessities가 본문의 essentials(필수품)와 같은 뜻임을 알아야 정답을 고를 수 있음'),
        ('u1-r3a', 3, 'luxuries', 'luxuries(사치품)가 필수품과 반대되는 말임을 알아야 텔레비전·비디오 게임이 아니라는 본문과 어긋남을 판단할 수 있음'),
        ('u1-r2s', 4, 'quiet', '사람들을 조용하게(quiet) 만든다는 내용이 본문에 없음을 판단해야 함'),
        ('u1-r1a', 5, 'normal', '평범한(normal) 나들이가 아니라 물이 끊긴 위기 속 외출임을 판단해야 함')],
  evidence='We have no running water out of the tap. / Inside it’s like Black Friday at its worst — but today it’s not televisions and video games people are after. What I see in the carts in the checkout line are mostly water bottles. The essentials of life.',
  explanation='가뭄 위기로 수도꼭지의 물이 끊기자 앨리사 가족은 쇼핑몰로 가고, 그곳에서 사람들이 텔레비전이나 비디오 게임이 아니라 삶의 필수품인 생수를 사려고 몰려든 모습이 그려진다. 따라서 물 위기가 심해지면서 사람들이 필수품을 사려고 몰려드는 모습이라는 ②가 주제로 가장 적절하다.',
  choices_ko=['오래된 부엌 수도꼭지에서 흔히 나는 이상한 소리',
              '물 위기가 심해지면서 필수품을 사려고 몰려드는 사람들',
              '블랙 프라이데이에 사치품을 사려는 쇼핑객들의 강한 욕구',
              '가뭄에 대해 사람들을 조용하게 만들려는 언론의 노력',
              '붐비는 쇼핑몰로 가는 평범한 가족 나들이'],
  wrong={1: '수도꼭지의 이상한 소리는 물이 끊겼음을 알리는 첫 장면일 뿐 글 전체의 중심 내용이 아니다.',
         3: '오늘 사람들이 원하는 것은 텔레비전과 비디오 게임이 아니라고 했으므로 사치품을 사려는 욕구는 본문과 반대다.',
         4: '언론은 사람들이 ‘가뭄’이라는 말을 듣는 데 지치자 그것을 ‘물 공급 위기’라고 불렀을 뿐, 사람들을 조용하게 만들려 했다는 내용은 없다.',
         5: '물이 끊겨 생수를 사러 가는 위기 상황이므로 평범한 가족 나들이가 아니다.'})

q(id='Q02', set_id='workbook', number=2, unit_id='u2', type='함축 의미', first='s18', last='s32',
  target='Even that politeness is stretched thin',
  question='밑줄 친 Even that politeness is stretched thin이 다음 글에서 의미하는 바로 가장 적절한 것은?',
  choices=['People are treating one another with warm and sincere courtesy.',
           'People are openly showing their rudeness by fighting in line.',
           'People are barely managing to keep up their courtesy.',
           'People feel calm because the shelves are still full of water.',
           'People think bottled water has become worthless.'],
  answer=3,
  uses=[('u2-r3s', 1, 'courtesy', '따뜻하고 진심 어린 예의(courtesy)가 ‘얇게 늘어난’ 예의와 반대임을 판단해야 함'),
        ('u2-r3a', 2, 'rudeness', '무례함(rudeness)을 드러내 놓고 싸운다는 말이 적대감이 예의 아래 숨겨져 있다는 본문과 어긋남을 판단해야 함'),
        ('u2-r3s', 3, 'courtesy', 'courtesy가 politeness(예의)와 같은 뜻임을 알아야 예의가 겨우 유지되는 상태라는 정답을 판단할 수 있음'),
        ('u2-r1a', 4, 'full', '선반이 가득 찬(full) 상태가 아니라 이미 비어 있었음을 판단해야 함'),
        ('u2-r2a', 5, 'worthless', 'worthless(가치 없는)가 precious(귀중한)와 반대임을 알아야 본문과 어긋남을 판단할 수 있음')],
  evidence='There is a look of impatience on the faces of the people in line. There is even hostility, hidden by a thin layer of politeness. Even that politeness is stretched thin.',
  explanation='줄 선 사람들의 얼굴에는 조급함이 있고, 얇은 예의 층 아래 적대감까지 숨어 있다고 했다. 밑줄 친 부분은 ‘그 예의마저 얇게 늘어나 있다’는 뜻으로, 겉으로 지키던 예의조차 곧 무너질 만큼 겨우 유지되고 있음을 나타낸다. 실제로 뒤에서 한 여자가 앨리사가 잡으려던 생수 상자를 마지막 순간에 가로챈다. 따라서 ③이 알맞다.',
  choices_ko=['사람들은 따뜻하고 진심 어린 예의로 서로를 대하고 있다.',
              '사람들은 줄에서 싸우며 드러내 놓고 무례함을 보이고 있다.',
              '사람들은 예의를 겨우 유지하고 있다.',
              '선반이 아직 물로 가득 차 있어서 사람들은 차분하다.',
              '사람들은 생수가 가치 없어졌다고 생각한다.'],
  wrong={1: '예의가 ‘얇게 늘어나’ 있다는 것은 겨우 유지되는 상태이므로 따뜻하고 진심 어린 예의와는 반대다.',
         2: '적대감은 얇은 예의 층에 ‘숨겨져’ 있다고 했으므로, 사람들이 줄에서 드러내 놓고 싸운다는 것은 지나친 해석이다.',
         4: '선반은 이미 비어 있었고 사람들의 얼굴에는 조급함이 있었으므로 맞지 않는다.',
         5: '어제만 해도 생수가 그렇게 귀하지 않았다는 말은 지금은 귀중한 상품이 되었다는 뜻이므로, 가치가 없어졌다는 것은 반대다.'})

q(id='Q03', set_id='workbook', number=3, unit_id='u3', type='내용', first='s37', last='s51',
  question='다음 글의 내용과 일치하지 않는 것은?',
  choices=['Alyssa discovered her brother in the frozen food aisle.',
           'Alyssa saw a case filled with ice near the ice cream.',
           'Garrett reminded Alyssa that they needed water, not ice.',
           'Other shoppers disregarded what the two were doing.',
           'The two filled the cart with ice until it was piled high.'],
  answer=4,
  uses=[('u3-r2s', 1, 'discovered', 'discover가 본문의 find(발견하다)와 같은 뜻임을 알아야 냉동식품 통로에서 동생을 찾았다는 본문과 일치함을 판단할 수 있음'),
        ('u3-r1s', 2, 'filled', 'filled가 packed(가득 찬)와 같은 뜻임을 알아야 얼음이 가득 든 진열장이라는 본문과 일치함을 판단할 수 있음'),
        ('u3-r3a', 4, 'disregarded', 'disregard(무시하다)가 notice(주목, 알아챔)와 반대 뜻임을 알아야 다른 사람들이 알아차렸다는 본문과 어긋남을 판단할 수 있음'),
        ('u3-r1s', 5, 'filled', '카트를 얼음으로 채웠다(filled)는 말이 본문의 put one bag of ice after another … until it is piled와 맞는지 판단해야 함')],
  evidence='By now other people have taken notice and begin to empty the ice case.',
  explanation='앨리사와 개릿이 카트에 얼음 봉지를 가득 쌓자, 이제는 다른 사람들도 알아차리고(have taken notice) 얼음 진열장을 비우기 시작한다고 했다. 따라서 다른 쇼핑객들이 두 사람의 행동을 무시했다는 ④는 본문과 일치하지 않는다.',
  choices_ko=['앨리사는 냉동식품 통로에서 남동생을 발견했다.',
              '앨리사는 아이스크림 근처에서 얼음이 가득 든 진열장을 보았다.',
              '개릿은 자신들에게 필요한 것은 얼음이 아니라 물이라고 앨리사에게 상기시켰다.',
              '다른 쇼핑객들은 두 사람이 하는 일을 무시했다.',
              '두 사람은 카트가 높이 쌓일 때까지 얼음으로 채웠다.'],
  wrong={1: '“I look for Garrett, whom I find in the frozen aisle.”와 일치한다(find = discover).',
         2: '“Just past the frozen vegetables and ice cream, there is a case packed with ice.”와 일치한다(packed = filled).',
         3: '“We need water, not ice,” he reminds me.와 일치한다.',
         5: '“Garrett and I put one bag of ice after another into our cart, until it is piled as high as it can get.”과 일치한다.'})

q(id='Q04', set_id='workbook', number=4, unit_id='u4', type='빈칸', first='s47', last='s62',
  blank='bring out the best in people',
  question='다음 빈칸에 들어갈 말로 가장 적절한 것은?',
  choices=['lead people to show their finest qualities',
           'bring out the worst side of people',
           'make everyday life easy for everyone',
           'make people’s hearts heavy with worry',
           'make people stop trusting strangers'],
  answer=1,
  uses=[('u4-r3s', 1, 'finest', 'finest가 best(가장 좋은)와 같은 뜻임을 알아야 사람들의 가장 좋은 면을 끌어낸다는 원래 뜻과 맞는 정답을 고를 수 있음'),
        ('u4-r3a', 2, 'worst', 'worst(가장 나쁜)가 best와 반대임을 알아야 ‘알게 되어 좋다’는 앞말과 맞지 않음을 판단할 수 있음'),
        ('u4-r2a', 3, 'easy', 'easy(쉬운)가 difficult(어려운)의 반대임을 알고, 어려운 시기가 삶을 쉽게 만든다는 말이 문맥과 맞지 않음을 판단해야 함')],
  evidence='“Not a problem. We all need to help one another.” He smiles again, and I return the smile. It is good to know that difficult times can ________. I decide that one favor deserves another.',
  explanation='정장 차림의 남자가 무거운 카트를 밀어 주며 “우리는 모두 서로 도와야 해요.”라고 말하고, 앨리사는 미소로 답한 뒤 호의에는 호의로 보답하기로 한다. 빈칸 문장은 ‘어려운 시기가 ~할 수 있다는 것을 알게 되어 좋다’이므로, 어려운 시기가 사람들의 가장 좋은 면을 끌어낸다는 긍정적인 내용이 와야 한다. 따라서 ①이 알맞다.',
  choices_ko=['사람들이 자신의 가장 훌륭한 자질을 보여 주게 하다',
              '사람들의 가장 나쁜 면을 끌어내다',
              '모든 사람의 일상을 쉽게 만들다',
              '사람들의 마음을 걱정으로 무겁게 하다',
              '사람들이 낯선 사람을 믿지 않게 만들다'],
  wrong={2: '앨리사는 남자의 도움에 미소로 답하고 ‘알게 되어 좋다’고 했으므로 사람들의 가장 나쁜 면이 드러난다는 말은 문맥과 반대다. 뒤에서 남자의 속셈이 드러나지만, 빈칸 문장은 그 전에 앨리사가 한 생각이다.',
         3: '어려운 시기가 모든 사람의 일상을 쉽게 만든다는 것은 물 부족과 무거운 카트라는 본문 상황과 맞지 않는다.',
         4: '걱정으로 마음이 무거워지는 것은 ‘알게 되어 좋다’와 어울리지 않고, 이 장면은 도움을 받은 고마움을 말한다.',
         5: '낯선 남자의 도움을 받고 호의에 보답하려는 장면이므로 낯선 사람을 믿지 않게 된다는 것은 반대다.'})

q(id='Q05', set_id='workbook', number=5, unit_id='u5', type='내용', first='s62', last='s74',
  question='다음 글의 내용과 일치하지 않는 것은?',
  choices=['Alyssa first thought the man was being playful, but he was earnest.',
           'The man’s eyes scared Alyssa even though he was smiling.',
           'Uncle Basil showed up at just the right moment.',
           'In the novel, the girl’s adventure ends when the water supply restarts.',
           'The writer mentions a decline in population as a cause of water shortages.'],
  answer=5,
  uses=[('u5-r1a', 1, 'playful', 'playful(장난스러운)이 본문의 joking과 통하고 serious의 반대임을 알아야 판단할 수 있음'),
        ('u5-r1s', 1, 'earnest', 'earnest가 serious(진지한)와 같은 뜻임을 알아야 판단할 수 있음'),
        ('u5-r2s', 4, 'restarts', 'restart가 resume(재개되다)와 같은 뜻임을 알아야 일치 여부를 판단할 수 있음'),
        ('u5-r3a', 5, 'decline', 'decline(감소)이 본문의 population growth(인구 증가)와 반대임을 알아야 일치하지 않음을 판단할 수 있음')],
  evidence='Provided that the factors contributing to water shortages worldwide are not addressed, including climate change, population growth, and using too much water for agriculture, …',
  explanation='필자는 전 세계 물 부족의 요인으로 기후 변화, 인구 증가(population growth), 농업에 물을 너무 많이 쓰는 것을 든다. 따라서 인구 감소를 원인으로 언급한다는 ⑤는 본문과 일치하지 않는다.',
  choices_ko=['앨리사는 처음에 남자가 장난친다고 생각했지만 그는 진지했다.',
              '남자는 웃고 있었지만 그의 눈은 앨리사를 겁먹게 했다.',
              '바질 삼촌은 딱 알맞은 때에 나타났다.',
              '소설에서 소녀의 모험은 물 공급이 다시 시작되면서 끝난다.',
              '필자는 인구 감소를 물 부족의 원인으로 언급한다.'],
  wrong={1: '“For a moment I think he is joking, but then realize he is serious.”와 일치한다(joking ≈ playful, serious = earnest).',
         2: '“He is still smiling, but his eyes scare me.”와 일치한다.',
         3: '“He has arrived just in time.”과 일치한다.',
         4: '“Her unwanted adventure ends when the water supply resumes …”와 일치한다(resume = restart).'})


# ================================================================ 미니 모의고사 1회
q(id='Q06', set_id='mock1', number=1, type='순서', first='s23', last='s36',
  blocks=('s23', 's26', {'A': ('s31', 's32'), 'B': ('s33', 's36'), 'C': ('s27', 's30')}),
  question='주어진 글 다음에 이어질 글의 순서로 가장 적절한 것은?',
  answer=4,
  evidence='(C) “I reach for it …”의 it이 주어진 글의 a single case of water를 가리킴 / (A) “As her mother pulls their cart away, Hali leans closer to me.”가 (C)에서 소개된 딸 Hali와 그 엄마를 이어받음 / (B) “Maybe you could return the favor …”가 (A)의 사과에 대한 응답이고, 마지막에 Hali가 떠나려고 돌아섬',
  explanation='주어진 글에서 앨리사는 옆 통로에서 생수 한 상자를 발견한다. (C) 그것을 잡으려는 순간 한 여자가 가로채고, 그 딸 할리가 앞으로 나선다. (A) 엄마가 카트를 끌고 가는 사이 할리가 다가와 사과한다. (B) 앨리사는 지난주 연습 때 물을 나눠 준 일을 말하며 보답을 부탁하지만, 할리는 고개를 저으며 얼굴을 붉히고 떠나려 한다. 따라서 (C)-(A)-(B)이다.',
  wrong={1: '(A)가 주어진 글 바로 뒤에 오면 her mother, their cart, Hali가 누구인지 알 수 없고, 할리가 무엇에 대해 사과하는지도 알 수 없다.',
         2: '(B)가 주어진 글 바로 뒤에 오면 앨리사가 말을 거는 her가 누구인지 알 수 없고, 아직 생수를 빼앗기지도 않았는데 물을 나눠 달라고 부탁하게 된다.',
         3: '(B)–(C)–(A)도 (B)의 her와 물 부탁이 생수를 빼앗기기 전에 나와 맞지 않는다.',
         5: '(C)–(B)–(A)가 가장 헷갈리는 배열이다. 그러나 (B)의 ‘보답해 달라’는 부탁은 (A)의 사과에 대한 응답이고, (B)에서 이미 통로를 따라 가고 있는 엄마는 (A)에서 엄마가 카트를 끌고 가기 시작한 뒤의 모습이다. 또 (B) 끝에서 할리가 떠나려고 돌아선 뒤 (A)에서 다시 다가와 사과하는 것은 어색하다.'})

q(id='Q07', set_id='mock1', number=2, type='삽입', first='s37', last='s51', given='s39',
  slots=['s38', 's39', 's41', 's43', 's45'],
  question='글의 흐름으로 보아, 주어진 문장이 들어가기에 가장 적절한 곳은?',
  answer=2,
  evidence='Then I see something. ( ② ) I open the door and reach for a bag.',
  explanation='주어진 문장은 냉동 채소와 아이스크림 바로 뒤에 얼음이 가득 든 케이스가 있다는 내용이다. ② 앞의 “Then I see something.”에서 앨리사가 무언가를 발견하고, 주어진 문장이 그 ‘무언가’가 얼음 케이스임을 밝힌다. ② 뒤의 “I open the door and reach for a bag.”의 the door와 a bag은 그 케이스의 문과 얼음 봉지이므로 ②에 들어가야 한다.',
  wrong={1: '이 위치에 넣으면 진열장을 먼저 소개한 뒤에 “Then I see something.”이 와서, 이미 소개한 대상을 새로 발견하는 것처럼 되어 발견 → 소개의 순서가 뒤바뀐다.',

         3: '이 위치에 넣으면 앨리사가 문을 열고 봉지에 손을 뻗은 뒤에야 진열장이 처음 소개되어, 발견(Then I see something) → 진열장 소개 → 문을 열고 봉지를 집는 행동의 순서가 거꾸로 된다.',
         4: '이 위치는 개릿과 앨리사가 얼음을 두고 주고받는 대화 사이로, 얼음 케이스를 처음 소개하는 문장이 들어가면 대화가 끊긴다.',
         5: '이 위치는 이미 문을 열고 얼음을 두고 대화까지 나눈 뒤라, 진열장을 처음 소개하는 문장이 오면 발견 → 소개 → 행동의 시간 순서가 뒤집힌다.'})

q(id='Q08', set_id='mock1', number=3, type='빈칸', first='s55', last='s70',
  blank='there is nothing to prove that it’s ours and not his',
  question='다음 빈칸에 들어갈 말로 가장 적절한 것은?',
  choices=['he will surely let go of the handle soon',
           'Uncle Basil will never find us in the crowd',
           'we have no way to show that the cart belongs to us',
           'the ice in our cart will melt before long',
           'everyone in the store will help us get the cart back'],
  answer=3,
  evidence='“Why don’t you take a bag of ice for yourselves, and I’ll keep the rest.” … He is still smiling, but his eyes scare me. As long as his hands are firmly locked on the handle of our cart, ________.',
  explanation='남자는 앨리사 남매에게 얼음 한 봉지만 가져가고 나머지는 자기가 갖겠다고 진지하게 말하며, 웃고 있지만 눈빛이 무섭다. 그의 손이 카트 손잡이를 단단히 붙잡고 있는 한, 카트가 앨리사 남매의 것이라는 걸 보여 줄 방법이 없다는 내용이 와야 한다. 따라서 ③이 알맞다.',
  choices_ko=['그가 곧 틀림없이 손잡이를 놓을 것이다',
              '바질 삼촌은 붐비는 사람들 속에서 결코 우리를 찾지 못할 것이다',
              '우리는 카트가 우리 것임을 보여 줄 방법이 없다',
              '우리 카트의 얼음이 곧 녹을 것이다',
              '가게의 모든 사람이 우리가 카트를 되찾도록 도와줄 것이다'],
  wrong={1: '남자가 손잡이를 ‘단단히’ 잡고 있고 나머지 얼음을 갖겠다고 진지하게 말했으므로, 곧 손을 놓을 것이라는 말은 흐름과 반대다.',
         2: '바질 삼촌은 바로 뒤에서 “Is there a problem here?”라고 말하며 제때 나타나므로 맞지 않는다.',
         4: '얼음이 녹는다는 것은 남자가 손잡이를 붙잡고 있는 한(As long as …)이라는 조건과 연결되지 않는다.',
         5: '가게 사람들이 도와준다는 내용은 없고, 앨리사는 남자의 눈빛에 겁을 먹은 상태다.'})

q(id='Q09', set_id='mock1', number=4, type='제목', first='s01', last='s22', group='G1',
  question='윗글의 제목으로 가장 적절한 것은?',
  choices=['The Day the Water Stopped: A Rush for the Essentials',
           'A Black Friday Sale on Televisions and Games',
           'How Uncle Basil Fixed the Broken Kitchen Tap',
           'A Relaxing Weekend Trip to the Shopping Mall',
           'A New Name for the Drought: The Media’s Choice'],
  answer=1,
  evidence='We have no running water out of the tap. / What I see in the carts in the checkout line are mostly water bottles. The essentials of life. / As I approach the back of the store for water bottles, I realize I am too late.',
  explanation='가뭄 위기로 수도꼭지의 물이 끊긴 날, 앨리사 가족은 쇼핑몰로 가고, 사람들은 삶의 필수품인 생수를 사려고 몰려들어 앨리사가 생수를 사러 갔을 때는 이미 너무 늦었다. 따라서 ‘물이 멈춘 날: 필수품을 향한 쇄도’라는 ①이 제목으로 가장 적절하다.',
  choices_ko=['물이 멈춘 날: 필수품을 향한 쇄도',
              '텔레비전과 게임의 블랙 프라이데이 할인',
              '바질 삼촌이 고장 난 부엌 수도꼭지를 고친 방법',
              '쇼핑몰로 가는 편안한 주말 여행',
              '가뭄의 새 이름: 언론의 선택'],
  wrong={2: '오늘 사람들이 사려는 것은 텔레비전과 비디오 게임이 아니라고 했다.',
         3: '바질 삼촌은 아이들을 쇼핑몰에 데려갈 뿐 수도꼭지를 고치지 않는다.',
         4: '조급함과 적대감이 감도는 위기 속 외출이므로 편안한 주말 여행이 아니다.',
         5: '언론이 가뭄을 ‘물 공급 위기’라고 부른다는 것은 한 문장의 세부 내용일 뿐 글 전체를 포괄하지 못한다.'})

q(id='Q10', set_id='mock1', number=5, type='어휘', first='s01', last='s22', group='G1',
  marks=[('silent', 's03'), ('tired', 's07'), ('crowd', 's12'), ('impatience', 's18'), ('empty', 's22')],
  replace=('empty', 'full'),
  question='윗글의 밑줄 친 부분 중, 문맥상 낱말의 쓰임이 적절하지 않은 것은?',
  answer=5,
  evidence='As I approach the back of the store for water bottles, I realize I am too late.',
  explanation='앨리사는 생수를 사러 매장 뒤쪽으로 가면서 자신이 너무 늦었다는 것을 깨닫는다. 너무 늦었다는 것은 이미 물이 다 팔렸다는 뜻이므로, 선반이 이미 ‘가득 차(full)’ 있다는 ⑤는 문맥에 맞지 않고 empty(비어 있는)가 되어야 한다.',
  wrong={1: '물이 한 번 튀어나온 뒤 수도꼭지가 조용해졌다(silent)는 것은 물이 끊긴 상황과 맞다.',
         2: '사람들이 ‘가뭄’이라는 말을 듣는 데 지쳐서(tired) 언론이 다른 이름을 쓰게 되었다는 흐름에 맞다.',
         3: '주차장에 들어서며 사람들의 무리(crowd)를 보았다는 것은 뒤의 블랙 프라이데이 같은 혼잡과 이어진다.',
         4: '줄 선 사람들의 얼굴에 조급함(impatience)이 있다는 것은 뒤의 적대감·얇은 예의와 이어진다.'})


# ================================================================ 미니 모의고사 2회
q(id='Q11', set_id='mock2', number=1, type='함축 의미', first='s01', last='s17',
  target='Black Friday at its worst',
  question='밑줄 친 Black Friday at its worst가 다음 글에서 의미하는 바로 가장 적절한 것은?',
  choices=['a day when stores give the biggest discounts of the year',
           'a scene of huge crowds rushing wildly to buy things',
           'a quiet store where only a few people are shopping',
           'a time when TVs and video games sell out quickly',
           'a sad day when people remember a past disaster'],
  answer=2,
  evidence='As we pull into the parking lot, we can see the crowd. / … but today it’s not televisions and video games people are after. What I see in the carts in the checkout line are mostly water bottles.',
  explanation='주차장에 들어서자마자 사람들의 무리가 보이고, 매장 안은 ‘최악일 때의 블랙 프라이데이’ 같다고 했다. 블랙 프라이데이는 사람들이 물건을 사려고 몰려드는 날이며, at its worst는 그 혼잡이 가장 심한 상태라는 뜻이다. 오늘은 텔레비전이 아니라 생수를 사려고 몰려든 것이므로, 엄청난 인파가 물건을 사려고 정신없이 몰려드는 장면이라는 ②가 알맞다.',
  choices_ko=['상점들이 연중 가장 큰 할인을 하는 날',
              '엄청난 인파가 물건을 사려고 정신없이 몰려드는 장면',
              '몇 사람만 쇼핑하고 있는 조용한 상점',
              '텔레비전과 비디오 게임이 빨리 매진되는 때',
              '사람들이 과거의 재난을 기억하는 슬픈 날'],
  wrong={1: '할인은 본문에 나오지 않으며, 이 표현은 할인 자체가 아니라 몰려든 사람들의 혼잡을 나타낸다.',
         3: '주차장에서부터 인파가 보였으므로 사람이 적은 조용한 상점은 반대다.',
         4: '오늘 사람들이 원하는 것은 텔레비전과 비디오 게임이 아니라고 했다.',
         5: '슬픈 기념일이라는 내용은 본문에 없다.'})

q(id='Q12', set_id='mock2', number=2, type='심경·분위기', first='s23', last='s36',
  question='다음 글에 드러난 ‘I’의 심경 변화로 가장 적절한 것은?',
  choices=['bored → excited',
           'nervous → relieved',
           'angry → grateful',
           'hopeful → disappointed',
           'jealous → proud'],
  answer=4,
  evidence='I manage my way to the side aisle, trying my luck. … Lucky! I find a single case of water … / I reach for it, only to find it pulled away at the last second by a woman. / … then turns back to me shaking her head.',
  explanation='앨리사는 운을 시험해 보려고 옆 통로로 가서 버려진 생수 한 상자를 발견하고 “Lucky!”라고 외칠 만큼 기대에 찬다. 그러나 손을 뻗는 순간 한 여자가 그것을 가로채 가고, 물을 나눠 달라는 부탁도 할리가 고개를 저어 거절한다. 따라서 ‘희망에 찬 → 실망한’의 ④가 알맞다.',
  choices_ko=['지루한 → 신이 난', '긴장한 → 안도한', '화난 → 고마워하는', '희망에 찬 → 실망한', '질투하는 → 자랑스러운'],
  wrong={1: '처음에 운을 시험하며 물을 찾는 모습은 지루함이 아니고, 뒤는 신이 난 것이 아니라 실망한 것이다.',
         2: '처음에는 긴장보다 기대가 드러나고, 물을 빼앗기고 부탁을 거절당한 뒤 안도할 일은 없다.',
         3: '물을 빼앗기고 부탁을 거절당했으므로 고마워할 일이 없다.',
         5: '질투나 자랑스러움이 드러나는 장면이 없다.'})

q(id='Q13', set_id='mock2', number=3, type='삽입', first='s62', last='s74', given='s73',
  slots=['s68', 's70', 's71', 's72', 's73'],
  question='글의 흐름으로 보아, 주어진 문장이 들어가기에 가장 적절한 곳은?',
  answer=5,
  evidence='It tells the story of a girl who has to make tough choices for her family during a disastrous California drought. ( ⑤ ) Provided that the factors …',
  explanation='주어진 문장은 ‘그녀의 원치 않은 모험은 물 공급이 재개되고 삶이 정상으로 돌아오면서 끝난다’는 내용이다. Her가 가리킬 대상은 ⑤ 앞 문장의 a girl(가뭄 속에서 가족을 위해 힘든 선택을 해야 하는 소녀)이며, 소설 줄거리 소개가 시작에서 끝으로 이어진 뒤 ⑤ 뒤에서 물 부족의 원인과 경고로 넘어간다. 따라서 ⑤에 들어가야 한다.',
  wrong={1: '이 위치 앞은 바질 삼촌이 나타난 1인칭 현재 장면으로, 서술자 자신을 3인칭 Her로 가리키며 물 공급이 재개되는 결말을 요약하는 문장이 장면 한가운데 끼어들 수 없다.',
         2: '이 위치 앞은 남자가 “Not at all.”이라고 답하는 장면으로, 이야기가 아직 진행 중인 1인칭 서술 속에 3인칭 결말 요약이 들어갈 수 없다.',
         3: '이 위치에 넣으면 이야기가 끝난 것처럼 보이지만, 곧이어 ‘위 글은 소설 도입부를 줄인 것’이라는 설명이 나와 모순되고, 소녀(a girl)도 그 뒤에야 소개된다.',
         4: '이 위치는 소설을 처음 언급한 문장 바로 뒤로, 소녀가 소개되기 전에 Her가 나오고 “It tells the story of a girl …”보다 결말이 먼저 오게 된다.'})

q(id='Q14', set_id='mock2', number=4, type='제목', first='s45', last='s70', group='G2',
  question='윗글의 제목으로 가장 적절한 것은?',
  choices=['How to Push a Heavy Cart with Ease',
           'Uncle Basil’s Clever Business Idea',
           'A Helping Hand with a Selfish Plan',
           'A Stranger Who Wanted Nothing in Return',
           'Why Ice Sells Better Than Bottled Water'],
  answer=3,
  evidence='“Why don’t you take a bag of ice for yourselves, and I’ll keep the rest.” / For a moment I think he is joking, but then realize he is serious.',
  explanation='정장 차림의 남자가 무거운 카트를 밀어 주며 서로 도와야 한다고 말하지만, 곧 얼음 한 봉지만 가져가고 나머지는 자기가 갖겠다고 진지하게 말한다. 바질 삼촌이 나타나자 그는 씁쓸한 얼굴로 떠난다. 따라서 ‘이기적인 속셈이 있는 도움의 손길’이라는 ③이 제목으로 가장 적절하다.',
  choices_ko=['무거운 카트를 쉽게 미는 방법',
              '바질 삼촌의 기발한 사업 아이디어',
              '이기적인 속셈이 있는 도움의 손길',
              '대가를 전혀 바라지 않은 낯선 사람',
              '얼음이 생수보다 더 잘 팔리는 이유'],
  wrong={1: '카트가 무거워 밀기 힘들다는 것은 장면의 출발점일 뿐, 카트를 쉽게 미는 방법은 나오지 않는다.',
         2: '바질 삼촌은 마지막에 나타나 남자를 떠나게 할 뿐이며, 사업 아이디어를 낸다는 내용은 없다.',
         4: '남자는 나머지 얼음을 모두 가지려 했으므로 대가를 바라지 않았다는 것은 반대다.',
         5: '얼음과 생수의 판매 비교는 나오지 않는다.'})

q(id='Q15', set_id='mock2', number=5, type='어휘', first='s45', last='s70', group='G2',
  marks=[('high', 's45'), ('heavy', 's47'), ('help', 's54'), ('best', 's56'), ('better', 's60')],
  replace=('high', 'low'),
  question='윗글의 밑줄 친 부분 중, 문맥상 낱말의 쓰임이 적절하지 않은 것은?',
  answer=1,
  evidence='Garrett and I put one bag of ice after another into our cart … / The cart is ridiculously heavy now, and almost impossible to push.',
  explanation='앨리사와 개릿은 얼음 봉지를 하나씩 계속 카트에 넣었고, 그 결과 카트는 터무니없이 무거워져 밀기 거의 불가능해졌다. 따라서 얼음이 ‘가능한 한 낮게(low)’ 쌓였다는 ①은 문맥에 맞지 않고 high(높이)가 되어야 한다.',
  wrong={2: '얼음을 가득 실어 카트가 무거워(heavy) 밀기 거의 불가능하다는 흐름에 맞다.',
         3: '남자가 “우리는 모두 서로 도와야(help) 해요.”라고 말하며 도움을 당연하게 여기는 말로 적절하다.',
         4: '남자의 도움을 받은 앨리사가 어려운 시기가 사람들의 가장 좋은(best) 면을 끌어낸다고 생각하는 흐름에 맞다.',
         5: '앨리사의 제안(얼음 한 봉지)보다 ‘더 나은(better)’ 생각이 있다며 자기 몫을 늘리려는 남자의 속셈을 보여 준다.'})


# ================================================================ 미니 모의고사 3회
q(id='Q16', set_id='mock3', number=1, type='순서', first='s01', last='s17',
  blocks=('s01', 's05', {'A': ('s15', 's17'), 'B': ('s06', 's09'), 'C': ('s10', 's14')}),
  question='주어진 글 다음에 이어질 글의 순서로 가장 적절한 것은?',
  answer=3,
  evidence='(B) “She is watching the TV …”의 She가 주어진 글의 Mom이며, 엄마가 “쉿!”이라고 한 이유(뉴스 시청)를 설명함 / (C) “To the mall!”이 (B)의 ‘수돗물이 나오지 않는다’에 대한 대응 / (A) “Inside …”가 (C)의 “You two go in. I’ll meet you inside”에 이어짐',
  explanation='주어진 글에서 수도꼭지의 물이 끊기자 앨리사가 엄마를 부르지만 엄마는 “쉿!”이라고 한다. (B) 엄마는 ‘물 공급 위기’에 관한 뉴스를 보고 있었고, 위기가 새 단계에 들어서 수돗물이 나오지 않는다. (C) 그러자 바질 삼촌이 “쇼핑몰로!”라고 외치고, 주차장에서 인파를 본 뒤 아이들에게 먼저 들어가라고 한다. (A) 안은 최악일 때의 블랙 프라이데이 같고, 카트에는 대부분 생수가 담겨 있다. 따라서 (B)-(C)-(A)이다.',
  wrong={1: '(A)가 주어진 글 바로 뒤에 오면 Inside가 어디의 안인지 알 수 없다.',
         2: '(B) 다음 (A)가 오면 쇼핑몰에 가기도 전에 매장 안의 장면이 나오고, 그 뒤 (C)에서 다시 쇼핑몰로 출발하게 된다.',
         4: '(C)가 주어진 글 바로 뒤에 오면 엄마가 “쉿!”이라고 한 이유가 설명되지 않은 채 쇼핑몰로 떠나고, 매장 안 장면 (A) 뒤에 다시 집에서 TV를 보는 (B)가 이어진다.',
         5: '(C)–(B)–(A)가 가장 헷갈리는 배열이다. 그러나 (B)의 She is watching the TV는 주어진 글에서 “쉿!”이라고 한 엄마의 모습을 바로 이어 설명하는 것이며, 트럭을 타고 쇼핑몰 주차장에 들어간 (C) 뒤에 집 안의 뉴스 장면이 오면 시간과 장소가 거꾸로 된다.'})

q(id='Q17', set_id='mock3', number=2, type='무관한 문장', first='s37', last='s51',
  addition='Frozen vegetables keep most of their vitamins because they are frozen soon after they are picked.',
  add_before='s46', marks=['s39', 's40', 's45', '@added', 's46'],
  question='다음 글에서 전체 흐름과 관계 없는 문장은?',
  answer=4,
  evidence='Garrett and I put one bag of ice after another into our cart, until it is piled as high as it can get. By now other people have taken notice and begin to empty the ice case.',
  explanation='글은 물이 떨어진 매장에서 앨리사가 얼음 케이스를 발견하고, 동생과 함께 카트에 얼음을 가득 쌓자 다른 사람들도 따라 하며, 무거운 카트에 한 남자가 다가오는 흐름이다. ④는 냉동 채소가 수확 직후 얼려져 비타민이 대부분 유지된다는 일반 정보로, 얼음을 쌓는 장면과 다른 사람들이 알아차리는 장면 사이를 끊는다.',
  wrong={1: '앨리사가 본 ‘무언가’가 얼음이 가득 든 케이스임을 밝혀 이야기의 전환점이 된다.',
         2: '케이스 문을 열고 얼음 봉지에 손을 뻗는 행동으로, 앞 문장의 발견에 이어진다.',
         3: '개릿과 함께 카트에 얼음을 가득 쌓는 장면으로, 앞의 “Just help me”에 이어진다.',
         5: '두 사람이 얼음을 쌓자 다른 사람들도 알아차리고 얼음 케이스를 비우기 시작한다는 내용으로 ③에 이어진다.'})

q(id='Q18', set_id='mock3', number=3, type='심경·분위기', first='s52', last='s65',
  question='다음 글에 드러난 ‘I’의 심경 변화로 가장 적절한 것은?',
  choices=['grateful → frightened',
           'jealous → satisfied',
           'bored → curious',
           'nervous → relieved',
           'angry → calm'],
  answer=1,
  evidence='“Thank you for helping us,” I tell him. / It is good to know that difficult times can bring out the best in people. / He is still smiling, but his eyes scare me.',
  explanation='처음에 앨리사는 자신들을 도와준 남자(him)에게 고마워하며(Thank you for helping us) 미소로 답하고, 호의에 보답하려고 얼음 한 봉지를 권한다. 그러나 남자가 나머지 얼음을 자기가 갖겠다고 진지하게 말하고, 웃는 얼굴과 달리 그의 눈이 무섭게 느껴진다. 따라서 ‘고마워하는 → 겁먹은’의 ①이 알맞다.',
  choices_ko=['고마워하는 → 겁먹은', '질투하는 → 만족한', '지루한 → 호기심 있는', '긴장한 → 안도한', '화난 → 차분한'],
  wrong={2: '질투하거나 만족하는 모습은 없고, 마지막에는 겁을 먹는다.',
         3: '지루함은 드러나지 않으며, 남자의 속셈을 알게 된 뒤의 감정은 호기심이 아니라 두려움이다.',
         4: '처음에는 긴장이 아니라 고마움을 느끼고, 뒤로 갈수록 안도가 아니라 두려움이 커진다.',
         5: '처음부터 화를 내지 않았고, 마지막에도 차분하기보다 겁을 먹는다.'})

q(id='Q19', set_id='mock3', number=4, type='제목', first='s18', last='s36', group='G3',
  question='윗글의 제목으로 가장 적절한 것은?',
  choices=['A Crown Made of Canned Goods',
           'When Water Is Precious, Kindness Runs Dry',
           'How Soccer Practice Made Two Girls Best Friends',
           'Full Shelves and Friendly Shoppers',
           'Why Stores Put Items on the Wrong Shelves'],
  answer=2,
  evidence='There is even hostility, hidden by a thin layer of politeness. / I reach for it, only to find it pulled away at the last second by a woman. / … then turns back to me shaking her head.',
  explanation='물이 귀해진 상황에서 줄 선 사람들은 얇은 예의 아래 적대감을 숨기고 있고, 앨리사가 겨우 찾은 생수 한 상자는 한 여자에게 빼앗기며, 예전에 물을 나눠 준 할리에게 보답을 부탁하지만 거절당한다. 따라서 ‘물이 귀해지면 친절이 바닥난다’는 ②가 제목으로 가장 적절하다.',
  choices_ko=['통조림으로 만든 왕관',
              '물이 귀해지면 친절이 바닥난다',
              '축구 연습이 두 소녀를 가장 친한 친구로 만든 방법',
              '가득 찬 선반과 친절한 쇼핑객들',
              '가게가 물건을 엉뚱한 선반에 두는 이유'],
  wrong={1: '여자가 생수 상자를 통조림 위에 왕관처럼 올려놓는다는 한 장면의 비유일 뿐 글 전체를 포괄하지 못한다.',
         3: '앨리사가 축구 연습 때 할리에게 물을 나눠 준 적은 있지만, 할리는 보답을 거절하므로 두 사람이 가장 친한 친구가 되었다는 것은 맞지 않는다.',
         4: '선반은 이미 비어 있었고 사람들에게는 조급함과 적대감이 있었으므로 반대다.',
         5: '사람들이 원치 않는 물건을 엉뚱한 선반에 두기도 한다는 것은 앨리사가 옆 통로를 찾아본 이유일 뿐이며, 가게가 그렇게 한다는 내용도 아니다.'})

q(id='Q20', set_id='mock3', number=5, type='어휘', first='s18', last='s36', group='G3',
  marks=[('impatience', 's18'), ('thin', 's20'), ('precious', 's26'), ('closer', 's31'), ('share', 's34')],
  replace=('share', 'hide'),
  question='윗글의 밑줄 친 부분 중, 문맥상 낱말의 쓰임이 적절하지 않은 것은?',
  answer=5,
  evidence='“Didn’t I share my water with you at the practice last week?” I point out to her. “Maybe you could return the favor …”',
  explanation='앨리사는 지난주 연습 때 할리에게 자기 물을 나눠 주었던 일을 말하며 그 호의에 보답해 달라고 부탁한다. 보답(return the favor)은 물을 ‘나눠 주는(share)’ 것이어야 하므로, 몇 병을 함께 ‘숨기자(hide)’는 ⑤는 문맥에 맞지 않고 share가 되어야 한다.',
  wrong={1: '줄 선 사람들의 얼굴에 조급함(impatience)이 보인다는 것은 뒤의 적대감과 이어진다.',
         2: '적대감을 숨긴 예의마저 ‘얇게(thin)’ 늘어나 있다는 것은 사람들의 긴장이 커지는 흐름에 맞다.',
         3: '어제만 해도 생수가 그렇게 귀한(precious) 상품이 아니었다는 것은 물이 부족해진 지금과 대비된다.',
         4: '엄마가 카트를 끌고 가는 사이 할리가 앨리사에게 더 가까이(closer) 다가와 사과한다는 흐름에 맞다.'})




# ================================================================ 조립
def _bounds(source):
    return {s['id']: s for s in source['sentences']}


def attach(data):
    src = data['sources'][0]
    B = _bounds(src)
    text = src['text']
    questions, quick, exps, plan, requests, groups = [], [], [], [], [], {}
    for row in Q:
        a, z = B[row['first']]['start'], B[row['last']]['end']
        original = text[a:z]
        kind = row['type']
        req = {'id': row['id'], 'type': kind, 'source_id': 'src',
               'first_sentence': row['first'], 'last_sentence': row['last']}
        rel = lambda sid: B[sid]['start'] - a  # noqa: E731
        if kind == '빈칸':
            s = original.index(row['blank'])
            req['replacement_span'] = [s, s + len(row['blank'])]
        elif kind == '함축 의미':
            s = original.index(row['target'])
            req['target_span'] = [s, s + len(row['target'])]
        elif kind == '어휘':
            marks = []
            for word, sid in row['marks']:
                base = rel(sid)
                m = re.compile(r'(?<![A-Za-z])' + re.escape(word) + r'(?![A-Za-z])').search(original, base)
                marks.append([m.start(), m.end()])
            req['vocabulary_marks'] = marks
            old, new = row['replace']
            idx = [w for w, _ in row['marks']].index(old)
            req['replacement_span'] = marks[idx]
            req['replacement'] = new
        elif kind == '삽입':
            req['given_sentence'] = row['given']
            req['insertion_slots'] = [rel(s) for s in row['slots']]
        elif kind == '순서':
            req['block_spans'] = _order_spans(row, B, a, len(original))
        elif kind == '무관한 문장':
            req['addition_offset'] = rel(row['add_before'])
            req['addition'] = row['addition']
            req['sentence_marks'] = row['marks']
        grouped = 'group' in row
        bench_type = 'long41_42' if grouped else kind
        probe = dict(req, length_review={'profile_id': LENGTH_PROFILE_ID, 'grade': GRADE,
                                         'benchmark_ids': recommended_benchmarks(GRADE, bench_type),
                                         'rationale': 'probe', 'independent_review_required': True})
        view = build_view(src, probe, expected_grade=GRADE, benchmark_type=bench_type)
        lc = view['length_comparison']
        refs = lc['reference_words']
        short = lc['shorter_than_all_references']
        rationale = (f"{'공유 장문 41~42' if grouped else kind} 고1 표본 {refs}단어와 비교해 현재 {lc['assessment_word_count']}단어. "
                     + (BENCH_SHORT_NOTE if short else '표본 범위 이상으로 너무 짧지 않음. ')
                     + '연속 원문 범위 안에서 정답과 네 오답의 근거가 자족적임.')
        req['length_review'] = {'profile_id': LENGTH_PROFILE_ID, 'grade': GRADE,
                                'benchmark_ids': recommended_benchmarks(GRADE, bench_type), 'rationale': rationale}
        if short:
            req['length_review']['independent_review_required'] = True
        view = build_view(src, req, expected_grade=GRADE, benchmark_type=bench_type)
        requests.append(req)
        identity = {'id': row['id'], 'set_id': row['set_id'], 'number': row['number']}
        p = dict(identity)
        if row['set_id'] == 'workbook':
            p['unit_id'] = row['unit_id']
        plan.append(p)
        qrow = dict(identity, type=kind, question=row['question'], answer=row['answer'])
        if kind in {'삽입', '무관한 문장', '어휘'}:
            qrow['choice_mode'] = 'in_passage'
            choices = [{'number': n, 'text': CIRCLED[n - 1]} for n in range(1, 6)]
        elif kind == '순서':
            qrow['choice_mode'] = 'order'
            qrow['permutations'] = ORDER
            choices = [{'number': n + 1, 'text': ' → '.join(p_)} for n, p_ in enumerate(ORDER)]
        else:
            qrow['choice_mode'] = 'text'
            choices = [{'number': n + 1, 'text': t} for n, t in enumerate(row['choices'])]
        qrow['choices'] = choices
        for field in ['passage', 'given', 'blocks', 'target']:
            if field in view and view[field] is not None:
                qrow[field] = view[field]
        if kind == '순서':
            qrow.pop('passage', None)
        if kind == '요약':
            qrow['summary'] = row['summary']
        if kind == '함축 의미':
            s = row['question'].index(row['target'])
            qrow['prompt_underlines'] = [[s, s + len(row['target'])]]
        if 'answer' in view:
            assert view['answer'] == row['answer'], (row['id'], view['answer'], row['answer'])
        if kind == '순서':
            assert ORDER[row['answer'] - 1] == view['correct_order'], (row['id'], view['correct_order'])
        if grouped:
            gid = 'long-' + row['set_id']
            qrow['passage_group_id'] = gid
            groups.setdefault(gid, {'id': gid, 'kind': 'long_reading', 'set_id': row['set_id'], 'question_ids': []})
            groups[gid]['question_ids'].append(row['id'])
            if kind == '어휘':
                groups[gid]['passage_question_id'] = row['id']
        if row['set_id'] == 'workbook':
            uses = []
            for term, num, surface, reason in row['uses']:
                ctext = row['choices'][num - 1]
                s = ctext.index(surface)
                uses.append({'term_id': term, 'choice_number': num, 'choice_span': [s, s + len(surface)],
                             'surface': surface, 'reason_ko': reason})
            qrow['learned_relation_uses'] = uses
        questions.append(qrow)
        quick.append(dict(identity, answer=row['answer']))
        exp = dict(identity, choices=[dict(c) for c in choices], answer=row['answer'],
                   evidence=row['evidence'], explanation=row['explanation'],
                   wrong_reasons=[{'number': n, 'text': t} for n, t in sorted(row['wrong'].items())])
        if qrow['choice_mode'] == 'text':
            exp['choices_ko'] = [{'number': n + 1, 'text': t} for n, t in enumerate(row['choices_ko'])]
        else:
            exp['choices_ko'] = []
        exps.append(exp)
    data['assessment'] = {
        'scope': {'kind': 'full', 'course': data['metadata']['course'], 'unit_ids': [u['id'] for u in data['units']]},
        'plan': plan, 'questions': questions, 'quick_key': quick, 'explanations': exps,
        'passage_groups': list(groups.values()),
    }
    data['question_sources'] = requests
    return data


def _order_spans(row, B, a, total):
    g0, g1, blocks = row['blocks']
    starts = {k: B[v[0]]['start'] - a for k, v in blocks.items()}
    ordered = sorted(starts.items(), key=lambda kv: kv[1])
    spans = {'given': [0, ordered[0][1]]}
    for i, (k, s) in enumerate(ordered):
        e = ordered[i + 1][1] if i + 1 < len(ordered) else total
        spans[k] = [s, e]
    return spans
