"""워크북 실전문제(Q01~Q04)와 미니 모의고사 3회(Q05~Q25) 원고.

지문·정답 위치는 원문에서 계산하고 question_source.build_view로 복원을 검증한다.
"""
import glob
import sys

sys.path.insert(0, glob.glob('/root/.claude/skills/synced/*/gyogwaseo-unified')[0] + '/scripts')
from question_source import build_view, recommended_benchmarks, word_count, LENGTH_PROFILE_ID  # noqa: E402

CIRCLED = '①②③④⑤'
ORDER = [['A', 'C', 'B'], ['B', 'A', 'C'], ['B', 'C', 'A'], ['C', 'A', 'B'], ['C', 'B', 'A']]
BENCH_SHORT_NOTE = '동일 유형 공식 표본보다 짧아 독립 검수에서 분량·정보 전개를 확인해야 함. '

Q = []  # 작성 순서 = 출력 순서


def q(**kw):
    Q.append(kw)


# ---------------------------------------------------------------- 워크북
q(id='Q01', set_id='workbook', number=1, unit_id='u1', type='요지', first='s50', last='s60',
  question='다음 글의 요지로 가장 적절한 것은?',
  choices=['Only a few experts are able to make real progress in understanding the night sky.',
           'Numerous unproven theories show that citizen science is in decline.',
           'Ordinary people can make remarkable contributions to the advancement of science.',
           'Extraordinary discoveries are possible only for those with science degrees.',
           'Citizen science projects are too ordinary to lead to new knowledge.'],
  answer=3,
  uses=[('u1-r2a', 1, 'few', '소수의 전문가만 진전을 이룬다는 뜻이 되어 본문(시민이 발견·기여)과 반대임을 판단해야 함'),
        ('u1-r3s', 1, 'progress', '진보(progress)가 누구에 의해 이루어지는지를 판단하는 핵심어'),
        ('u1-r2h', 2, 'Numerous', '이론이 많다는 사실과 쇠퇴를 잇는 잘못된 추론을 알아보아야 함'),
        ('u1-r3a', 2, 'decline', '쇠퇴(decline)는 과학자와 시민이 계속 협력한다는 본문과 반대'),
        ('u1-r1a', 3, 'Ordinary', '평범한 사람들이 주체라는 요지의 핵심어'),
        ('u1-r1h', 3, 'remarkable', '기여가 놀랍다(가치 있다)는 평가를 담은 핵심어'),
        ('u1-r3h', 3, 'advancement', '과학의 발전에 기여한다는 요지의 핵심어'),
        ('u1-r1s', 4, 'Extraordinary', '비범한 발견이 학위 소지자에게만 가능하다는 주장은 본문과 반대'),
        ('u1-r1a', 5, 'ordinary', '평범하다는 이유로 가치가 없다는 판단은 본문과 반대')],
  evidence='If it had not been for them, it might have remained unnoticed forever. / they are still capable of making valuable contributions to science. / The next great scientific achievement could be made by citizen scientists …',
  explanation='오로라 추적자들이 STEVE를 처음 발견해 공로를 인정받았고, 학위가 없는 시민 과학자도 과학에 귀중한 기여를 할 수 있으며 다음 위대한 업적도 그들이 이룰 수 있다고 말한다. 따라서 평범한 사람들이 과학의 발전에 놀라운 기여를 할 수 있다는 ③이 요지다.',
  choices_ko=['소수의 전문가만이 밤하늘을 이해하는 데 실제로 진전을 이룰 수 있다.',
              '증명되지 않은 수많은 이론은 시민 과학이 쇠퇴하고 있음을 보여 준다.',
              '평범한 사람들도 과학의 발전에 놀라운 기여를 할 수 있다.',
              '비범한 발견은 과학 학위가 있는 사람들에게만 가능하다.',
              '시민 과학 프로젝트는 너무 평범해서 새로운 지식으로 이어질 수 없다.'],
  wrong={1: 'STEVE는 전문가가 아닌 오로라 추적자들이 발견했고 전문가들도 그 공로를 인정했으므로 반대 내용이다.',
         2: '이론이 증명되지 않았다는 사실만 있을 뿐, 과학자와 시민이 계속 협력해 점점 더 많이 알아 가고 있다고 했으므로 쇠퇴와 무관하다.',
         4: '시민 과학자는 과학 학위가 없어도 귀중한 기여를 할 수 있다고 했으므로 반대 내용이다.',
         5: '다음 위대한 과학적 업적은 시민 과학자들이 이룰 수도 있다고 했으므로 반대 내용이다.'})

q(id='Q02', set_id='workbook', number=2, unit_id='u2', type='내용', first='s07', last='s19',
  question='다음 글의 내용과 일치하지 않는 것은?',
  choices=['Schawinski’s work of classifying galaxy images at Oxford was boring.',
           'Sorting the images one by one would require an enormous amount of time.',
           'Lintott suggested using the Internet to get help from other people.',
           'New visitors to the website were given a short tutorial about the project.',
           'Schawinski found his task exciting because it took only a tiny amount of time.'],
  answer=5,
  uses=[('u2-r2s', 1, 'boring', 'dull(따분한)과 같은 뜻인지 판단해야 일치 여부를 알 수 있음'),
        ('u2-r1s', 2, 'enormous', 'tremendous(엄청난)와 같은 뜻인지 판단해야 함'),
        ('u2-r3s', 4, 'short', 'brief(간단한)와 같은 뜻인지 판단해야 함'),
        ('u2-r2a', 5, 'exciting', 'dull과 반대되는 exciting이 본문과 어긋남을 알아야 함'),
        ('u2-r1a', 5, 'tiny', 'tremendous amount와 반대되는 tiny amount가 본문과 어긋남을 알아야 함')],
  evidence='his job there was dull and time-consuming. / this would require a tremendous amount of time. / It took Schawinski a whole week to classify just 50,000 galaxies.',
  explanation='본문은 Schawinski의 일이 흥미롭게 들릴 수 있지만 실제로는 따분하고 시간이 많이 걸렸으며, 5만 개를 분류하는 데만 꼬박 일주일이 걸렸다고 한다. 따라서 일이 신났고 아주 적은 시간이 걸렸다는 ⑤는 본문과 일치하지 않는다.',
  choices_ko=['옥스퍼드에서 은하 이미지를 분류하는 Schawinski의 일은 지루했다.',
              '이미지를 하나하나 분류하는 것은 엄청난 양의 시간이 필요할 것이었다.',
              'Lintott은 다른 사람들의 도움을 얻기 위해 인터넷을 이용할 것을 제안했다.',
              '웹사이트의 새 방문자들은 프로젝트에 관한 짧은 사용 지침을 받았다.',
              'Schawinski는 일이 아주 적은 시간밖에 걸리지 않아서 신난다고 생각했다.'],
  wrong={1: '“his job there was dull and time-consuming”과 일치한다(dull = boring).',
         2: '“this would require a tremendous amount of time”과 일치한다(tremendous = enormous).',
         3: '“Lintott suggested that he turn to the Internet to ask other people for help.”와 일치한다.',
         4: '“New visitors were greeted with a brief tutorial that explained the project.”와 일치한다(brief = short).'})

q(id='Q03', set_id='workbook', number=3, unit_id='u3', type='제목', first='s34', last='s46',
  question='다음 글의 제목으로 가장 적절한 것은?',
  choices=['How Aurora Chasers Competed with NASA for the Best Photos',
           'A Strange New Light Spotted by Ordinary Sky Watchers',
           'Why Experts Found the Lights Too Familiar to Study',
           'An Average Aurora That Everyone Can See at Night',
           'Outstanding Photos That Proved What Steve Really Was'],
  answer=2,
  uses=[('u3-r3a', 1, 'Competed', 'collaborate와 반대되는 compete가 본문(전문가에게 도움을 구함)과 어긋남을 판단해야 함'),
        ('u3-r2s', 2, 'Strange', 'unfamiliar(낯선)와 같은 뜻으로 새 현상의 성격을 나타냄'),
        ('u3-r2a', 3, 'Familiar', '전문가도 무엇인지 몰랐다는 본문과 반대되는 familiar를 알아보아야 함'),
        ('u3-r1a', 4, 'Average', 'exceptional과 반대인 average(평범한)가 새로운 유형의 현상이라는 본문과 어긋남'),
        ('u3-r1s', 5, 'Outstanding', 'outstanding(뛰어난) 사진이라도 정체를 증명하지는 못했다는 점을 판단해야 함')],
  evidence='the group members began to notice something strange appearing in the night sky. / Surprisingly, neither of them had any idea what Steve was. / They realized that the group had discovered a new type of phenomenon that had never been properly studied.',
  explanation='오로라 추적자라는 평범한 사람들이 밤하늘에서 이상한 빛을 발견했고, 전문가들도 그것이 제대로 연구된 적 없는 새로운 현상임을 깨달았다는 내용이다. 따라서 ②가 제목으로 가장 적절하다.',
  choices_ko=['오로라 추적자들은 최고의 사진을 위해 어떻게 NASA와 경쟁했는가',
              '평범한 하늘 관찰자들이 발견한 이상한 새 빛',
              '전문가들은 왜 그 빛을 연구하기에 너무 익숙하다고 여겼는가',
              '누구나 밤에 볼 수 있는 평범한 오로라',
              'Steve의 정체를 증명한 뛰어난 사진들'],
  wrong={1: '단체는 NASA와 경쟁한 것이 아니라 전문가들에게 도움을 구했다.',
         3: '전문가들은 Steve가 무엇인지 전혀 몰랐으므로 익숙하다는 말은 본문과 반대다.',
         4: '그것은 오로라가 아니었고 이전에 본 어떤 것과도 닮지 않은 새로운 유형의 현상이었다.',
         5: '사진을 보여 주었지만 전문가도 정체를 알지 못했으므로 무엇인지 증명했다는 말은 틀리다.'})

q(id='Q04', set_id='workbook', number=4, unit_id='u4', type='주장', first='s01', last='s06',
  question='다음 글에서 필자가 주장하는 바로 가장 적절한 것은?',
  choices=['Only professional scientists should be trusted to advance science.',
           'The ideas of amateurs are worthless unless experts check them first.',
           'Scientists in lab coats should promote their work to ordinary people.',
           'Anyone, not only experts, can play a valuable role in advancing science.',
           'Citizen science projects tend to hinder real scientific progress.'],
  answer=4,
  uses=[('u4-r2h', 1, 'professional', '전문 과학자만 신뢰해야 한다는 주장이 필자의 생각과 반대임을 알아야 함'),
        ('u4-r3h', 1, 'advance', '과학을 발전시키는 주체가 누구인지 판단하는 핵심어'),
        ('u4-r1a', 2, 'worthless', 'valuable과 반대되는 worthless가 필자의 생각과 어긋남'),
        ('u4-r3s', 3, 'promote', '홍보·촉진(promote)이 필자의 주장과 무관함을 판단해야 함'),
        ('u4-r2s', 4, 'experts', '전문가만이 아니라 누구나라는 대비의 핵심어'),
        ('u4-r1h', 4, 'valuable', '누구나 귀중한 역할을 할 수 있다는 주장의 핵심어'),
        ('u4-r3a', 5, 'hinder', 'advance와 반대되는 hinder가 필자의 주장과 어긋남')],
  evidence='However, this perception is far from the truth. In reality, science belongs to everyone, and we all have the ability to play a role in the advancement of science.',
  explanation='과학이 흰 가운을 입은 과학자만의 영역이라는 생각은 사실과 거리가 멀고, 과학은 모두의 것이며 누구나 과학 발전에 한몫할 수 있다고 주장한다. 따라서 ④가 필자의 주장이다.',
  choices_ko=['전문 과학자들만이 과학을 발전시킬 것으로 신뢰받아야 한다.',
              '아마추어의 생각은 전문가가 먼저 확인하지 않으면 가치가 없다.',
              '실험실 가운을 입은 과학자들은 평범한 사람들에게 자신들의 연구를 홍보해야 한다.',
              '전문가뿐만 아니라 누구나 과학을 발전시키는 데 귀중한 역할을 할 수 있다.',
              '시민 과학 프로젝트는 실제 과학의 진보를 방해하는 경향이 있다.'],
  wrong={1: '과학은 모두의 것이라는 필자의 주장과 정반대다.',
         2: '아마추어의 생각을 전문가가 확인해야 한다는 내용은 본문에 없고, 필자는 누구나 기여할 수 있다고 본다.',
         3: '과학자의 홍보에 관한 내용은 본문에 없다.',
         5: '필자는 평범한 사람들이 놀라운 과학적 업적에 기여한 시민 과학 프로젝트가 많았다고 했으므로 반대 내용이다.'})

# ---------------------------------------------------------------- 미니 모의고사 1회
q(id='Q05', set_id='mock1', number=1, type='주제', first='s24', last='s33',
  question='다음 글의 주제로 가장 적절한 것은?',
  choices=['the role of ordinary participants in the success and growth of Galaxy Zoo',
           'the reasons online media reduced the popularity of Galaxy Zoo',
           'the difficulty of classifying galaxies without professional training',
           'the time Schawinski spent training new astronomy researchers',
           'the dangers of sharing personal information on science websites'],
  answer=1,
  evidence='It was online media that helped spread the word about Galaxy Zoo, bringing more and more participants to the website. / If it had not been for those participants, Schawinski couldn’t have classified that many images. / Galaxy Zoo has now grown into Zooniverse …',
  explanation='많은 참여자가 몰려 엄청난 수의 분류가 이루어졌고, 그들이 없었다면 불가능했으며, Galaxy Zoo가 지금은 인기 있는 시민 과학 플랫폼 Zooniverse로 성장했다는 내용이다. 따라서 ①이 주제다.',
  choices_ko=['Galaxy Zoo의 성공과 성장에서 평범한 참여자들이 한 역할',
              '온라인 미디어가 Galaxy Zoo의 인기를 떨어뜨린 이유',
              '전문적인 훈련 없이 은하를 분류하는 것의 어려움',
              'Schawinski가 새로운 천문학 연구원을 교육하는 데 들인 시간',
              '과학 웹사이트에서 개인 정보를 공유하는 것의 위험'],
  wrong={2: '온라인 미디어는 소문을 퍼뜨려 참여자를 늘렸으므로 인기를 떨어뜨렸다는 것은 반대 내용이다.',
         3: '참여자들은 사용 지침과 약간의 연습만으로 분류할 수 있었고, 이 글은 분류의 어려움이 아니라 참여의 성과를 다룬다.',
         4: '연구원 교육은 본문에 나오지 않으며 Schawinski 혼자서는 수십 년이 걸렸을 것이라는 내용만 있다.',
         5: '개인 정보의 위험은 본문에 전혀 나오지 않는다.'})

q(id='Q06', set_id='mock1', number=2, type='내용', first='s34', last='s41',
  question='다음 글의 내용과 일치하는 것은?',
  choices=['The aurora chasers met in person every week to share their photos.',
           'Some of the ribbons of light seemed to stretch for thousands of kilometers.',
           'The ribbons of light always stayed in the sky for exactly one hour.',
           'The lights looked completely different from auroras.',
           'A NASA scientist gave the phenomenon the name “Steve.”'],
  answer=2,
  evidence='There were unusual ribbons of green and purple light, some of which seemed to stretch for thousands of kilometers.',
  explanation='녹색과 보라색 빛의 띠 가운데 일부가 수천 킬로미터에 걸쳐 뻗어 있는 것처럼 보였다고 했으므로 ②가 본문과 일치한다.',
  choices_ko=['오로라 추적자들은 사진을 공유하기 위해 매주 직접 만났다.',
              '빛의 띠 중 일부는 수천 킬로미터에 걸쳐 뻗어 있는 것처럼 보였다.',
              '빛의 띠는 항상 정확히 한 시간 동안 하늘에 머물렀다.',
              '그 빛은 오로라와 완전히 다르게 생겼다.',
              'NASA의 한 과학자가 그 현상에 ‘Steve’라는 이름을 붙였다.'],
  wrong={1: '그들은 온라인에서 비공식 단체를 결성해 사진을 공유했을 뿐, 매주 직접 만났다는 내용은 없다.',
         3: '어떤 때는 단 몇 분만 지속되었고 다른 때는 한 시간 내내 머물렀으므로 ‘항상 한 시간’은 틀리다.',
         4: '생김새는 오로라와 비슷했지만 몇 가지 다른 특징이 있었다고 했다.',
         5: '이름을 붙인 것은 오로라 추적자 단체다.'})

q(id='Q07', set_id='mock1', number=3, type='빈칸', first='s42', last='s49',
  blank='a new type of phenomenon that had never been properly studied',
  question='다음 빈칸에 들어갈 말로 가장 적절한 것은?',
  choices=['an old kind of aurora that experts had studied for years',
           'a photograph that NASA had already published',
           'a common light that anyone could easily identify',
           'something that science had not yet properly explained',
           'a mistake in the way the group had taken photos'],
  answer=4,
  evidence='Surprisingly, neither of them had any idea what Steve was. They confirmed that it was not an aurora, but it did not resemble anything they had seen before. / In order to learn more about it, NASA funded a citizen science project …',
  explanation='전문가들도 Steve의 정체를 몰랐고, 오로라가 아니며 이전에 본 어떤 것과도 닮지 않았다고 확인했다. 이어서 NASA가 더 알아보기 위해 프로젝트를 지원했으므로, 빈칸에는 ‘과학이 아직 제대로 설명하지 못한 것’을 발견했다는 ④가 알맞다.',
  choices_ko=['전문가들이 수년 동안 연구해 온 오래된 종류의 오로라',
              'NASA가 이미 발표한 사진',
              '누구나 쉽게 알아볼 수 있는 흔한 빛',
              '과학이 아직 제대로 설명하지 못한 것',
              '단체가 사진을 찍은 방식의 실수'],
  wrong={1: '그것은 오로라가 아니라고 확인했으므로 틀리다.',
         2: 'NASA가 사진을 발표했다는 내용은 없고, 오히려 NASA도 그것이 무엇인지 몰랐다.',
         3: '교수와 NASA 과학자조차 무엇인지 알지 못했으므로 누구나 쉽게 알아볼 수 있다는 것은 반대다.',
         5: '사진 촬영의 실수라는 근거는 없고, NASA는 그 현상을 더 알기 위해 프로젝트를 지원했다.'})

q(id='Q08', set_id='mock1', number=4, type='순서', first='s01', last='s13',
  blocks=('s01', 's03', {'A': ('s10', 's13'), 'B': ('s04', 's06'), 'C': ('s07', 's09')}),
  question='주어진 글 다음에 이어질 글의 순서로 가장 적절한 것은?',
  answer=3,
  evidence='(B) However 뒤 “In reality, science belongs to everyone …” → “Let’s take a look at two of them.” / (C) 첫 사례 Kevin Schawinski 소개와 백만 장의 분류 작업 / (A) “Since they all looked similar …”의 they가 (C)의 images of galaxies를 가리킴.',
  explanation='주어진 글은 과학이 과학자만의 영역이라는 인식이 사실과 거리가 멀다고 한다. (B)는 과학이 모두의 것이며 두 가지 시민 과학 프로젝트를 살펴보자고 이어 간다. (C)는 첫 사례로 백만 장의 은하 이미지를 분류해야 했던 Schawinski를 소개하고, (A)는 그 이미지들(they)을 하나씩 보며 분류하느라 엄청난 시간이 걸렸다는 내용이다. 따라서 (B)-(C)-(A)이다.',
  wrong={1: '(A)의 they가 가리킬 은하 이미지가 앞에 나오지 않아 연결되지 않는다.',
         2: '(B) 다음 (A)가 오면 (A)의 they·this가 가리킬 대상이 없다.',
         4: '주어진 글 바로 뒤에 (C)의 구체적 인물이 나오면 (B)의 ‘두 가지를 살펴보자’라는 예고가 사례 뒤에 놓여 흐름이 어긋난다.',
         5: '(C) 다음 (B)가 오면 사례 도중에 ‘두 가지를 살펴보자’는 도입이 끼어들어 어색하다.'})

q(id='Q09', set_id='mock1', number=5, type='삽입', first='s50', last='s60', given='s53',
  slots=['s52', 's53', 's55', 's56', 's57'],
  question='글의 흐름으로 보아, 주어진 문장이 들어가기에 가장 적절한 곳은?',
  answer=2,
  evidence='Experts have acknowledged that it is the dedicated members of the aurora chasers group that deserve the credit for discovering STEVE. + If it had not been for them(= the dedicated members) …',
  explanation='주어진 문장의 them은 STEVE 발견의 공로를 인정받는 오로라 추적자 단체의 헌신적인 구성원들을 가리킨다. 그들이 없었다면 STEVE가 영원히 알려지지 않았을 것이라는 내용은 공로를 인정했다는 문장 바로 뒤인 ②에 들어가야 한다.',
  wrong={1: '①의 앞 문장은 STEVE라는 이름이 무엇을 뜻하는지 설명하므로 them(구성원들)과 연결되지 않는다.',
         3: '③의 앞 문장은 STEVE에 관한 이론이 증명되지 않았다는 내용이라 공로를 강조하는 주어진 문장이 이어지기 어색하다.',
         4: '④ 앞에서는 과학자와 시민의 협력을 말하고 뒤에서는 두 프로젝트 참여자 전체로 넘어가므로 주어진 문장이 끼어들 자리가 아니다.',
         5: '⑤ 앞뒤는 시민 과학자가 누구인지 설명하는 흐름이라 STEVE 발견자를 가리키는 them이 들어갈 수 없다.'})

q(id='Q10', set_id='mock1', number=6, type='제목', first='s07', last='s23', group='G1',
  question='윗글의 제목으로 가장 적절한 것은?',
  choices=['How Computers Replaced Human Researchers in Astronomy',
           'The Dangers of Asking Strangers Online for Help',
           'Why All Galaxies Look Exactly the Same',
           'A Researcher Who Gave Up on Classifying Galaxies',
           'Turning an Overwhelming Task into a Simple Online Project'],
  answer=5,
  evidence='He had to classify around one million images … / Lintott suggested that he turn to the Internet … / the two men ended up launching a crowdsourced online project known as Galaxy Zoo. The website was kept as simple as possible …',
  explanation='혼자 하기엔 엄청난 은하 분류 작업을 인터넷에서 대중의 도움을 받는 단순한 온라인 프로젝트(Galaxy Zoo)로 바꾸어 해결해 간 과정을 다루므로 ⑤가 제목으로 적절하다.',
  choices_ko=['컴퓨터는 어떻게 천문학에서 인간 연구자를 대신했는가',
              '온라인에서 낯선 사람들에게 도움을 청하는 것의 위험',
              '왜 모든 은하는 똑같아 보이는가',
              '은하 분류를 포기한 한 연구원',
              '엄청난 과업을 단순한 온라인 프로젝트로 바꾸기'],
  wrong={1: '컴퓨터가 사람을 대신했다는 내용은 없고, 오히려 많은 사람이 직접 분류에 참여했다.',
         2: '온라인 도움 요청의 위험은 다루지 않으며 그 방법으로 문제를 해결했다.',
         3: '은하들은 비슷해 보이지만 실제로는 모양이 조금씩 달랐다고 했다.',
         4: 'Schawinski는 포기하지 않고 Galaxy Zoo를 시작해 해결책을 찾았다.'})

q(id='Q11', set_id='mock1', number=7, type='어휘', first='s07', last='s23', group='G1',
  marks=[('dull', 's08'), ('similar', 's10'), ('tremendous', 's11'), ('simple', 's17'), ('quickly', 's18')],
  replace=('simple', 'complicated'),
  question='윗글의 밑줄 친 부분 중, 문맥상 낱말의 쓰임이 적절하지 않은 것은?',
  answer=4,
  evidence='with a very basic design and an easy-to-use interface. This allowed those who wanted to participate to get started quickly.',
  explanation='웹사이트는 매우 기본적인 디자인과 사용하기 쉬운 인터페이스를 갖추어 참여자들이 빨리 시작할 수 있었다. 따라서 ④의 complicated(복잡한)는 문맥에 맞지 않고 simple(단순한)이 되어야 한다.',
  wrong={1: '흥미롭게 들릴 수 있지만(But) 실제로는 시간이 많이 걸리는 일이었으므로 dull(따분한)은 적절하다.',
         2: '모두 비슷해 보이지만 실제로는 모양이 조금씩 달랐다는 대조이므로 similar는 적절하다.',
         3: '5만 개에 일주일이 걸렸으므로 엄청난(tremendous) 시간이 필요하다는 말은 적절하다.',
         5: '단순한 웹사이트 덕분에 빨리(quickly) 시작할 수 있었다는 흐름에 맞다.'})

# ---------------------------------------------------------------- 미니 모의고사 2회
q(id='Q12', set_id='mock2', number=1, type='요지', first='s14', last='s28',
  question='다음 글의 요지로 가장 적절한 것은?',
  choices=['A simple website and many ordinary helpers made a huge classification task possible.',
           'Online media made it harder for scientists to find volunteers.',
           'Classifying galaxies requires years of professional training.',
           'Schawinski finished most of the classifications by himself.',
           'Tutorials make citizen science projects too complicated for beginners.'],
  answer=1,
  evidence='The website was kept as simple as possible … / more than 80,000 individuals participated, and they made more than 75 million classifications. If it had not been for those participants, Schawinski couldn’t have classified that many images.',
  explanation='단순한 웹사이트와 짧은 사용 지침 덕분에 누구나 참여할 수 있었고, 많은 참여자 덕분에 혼자서는 수십 년이 걸렸을 분류 작업을 해냈다는 내용이므로 ①이 요지다.',
  choices_ko=['단순한 웹사이트와 많은 평범한 조력자들이 거대한 분류 작업을 가능하게 했다.',
              '온라인 미디어는 과학자들이 자원봉사자를 찾기 더 어렵게 만들었다.',
              '은하를 분류하는 데에는 수년간의 전문적인 훈련이 필요하다.',
              'Schawinski는 분류의 대부분을 혼자서 끝냈다.',
              '사용 지침은 시민 과학 프로젝트를 초보자에게 너무 복잡하게 만든다.'],
  wrong={2: '온라인 미디어는 소문을 퍼뜨려 참여자를 늘렸으므로 반대 내용이다.',
         3: '사용 지침과 약간의 연습 후 참가자들은 효과적으로 분류할 수 있었다.',
         4: '참여자들이 없었다면 그렇게 많이 분류할 수 없었고 혼자서는 수십 년이 걸렸을 것이라고 했다.',
         5: '간단한 사용 지침과 약간의 연습 후 효과적으로 분류할 수 있었다고 했으므로 반대다.'})

q(id='Q13', set_id='mock2', number=2, type='함축 의미', first='s07', last='s16',
  target='what about the remaining 950,000',
  question='밑줄 친 what about the remaining 950,000가 다음 글에서 의미하는 바로 가장 적절한 것은?',
  choices=['He wanted to know where the other images had been stored.',
           'He worried that classifying all the other images alone would take far too long.',
           'He was excited that there were many more galaxies to study.',
           'He thought the remaining images were too similar to classify.',
           'He hoped his friend would pay someone to finish the work.'],
  answer=2,
  evidence='It took Schawinski a whole week to classify just 50,000 galaxies. / One evening after work, Schawinski met a friend … and complained about the situation.',
  explanation='5만 개를 분류하는 데 꼬박 일주일이 걸렸으므로 나머지 95만 개를 혼자 분류하려면 너무 오래 걸린다는 걱정이다. 이어서 친구에게 그 상황을 불평한 것도 이 걱정을 뒷받침한다. 따라서 ②가 알맞다.',
  choices_ko=['그는 나머지 이미지들이 어디에 저장되어 있는지 알고 싶었다.',
              '그는 나머지 이미지를 혼자 모두 분류하려면 너무 오래 걸릴 것을 걱정했다.',
              '그는 연구할 은하가 훨씬 더 많다는 것에 신이 났다.',
              '그는 남은 이미지들이 너무 비슷해서 분류할 수 없다고 생각했다.',
              '그는 친구가 누군가에게 돈을 주고 일을 끝내게 해 주기를 바랐다.'],
  wrong={1: '이미지의 저장 위치는 본문에서 다루지 않는다.',
         3: '그의 일은 따분하고 시간이 많이 걸렸으며, 그는 친구에게 상황을 불평했으므로 신이 났다는 것은 반대다.',
         4: '비슷해 보여도 하나씩 보면 분류할 수 있었다. 문제는 분류할 수 없다는 것이 아니라 시간이었다.',
         5: '친구 Lintott은 인터넷으로 다른 사람들에게 도움을 요청하라고 제안했을 뿐, 돈을 주는 내용은 없다.'})

q(id='Q14', set_id='mock2', number=3, type='무관한 문장', first='s24', last='s33',
  addition='Some astronomers still prefer to observe galaxies through huge telescopes built on high mountains.',
  add_before='s28', marks=['s25', 's26', 's27', '@added', 's28'],
  question='다음 글에서 전체 흐름과 관계 없는 문장은?',
  answer=4,
  evidence='If it had not been for those participants, Schawinski couldn’t have classified that many images. In fact, it would have taken him decades on his own.',
  explanation='글은 참여자들 덕분에 엄청난 분류가 가능했다는 흐름이다. ④는 높은 산의 거대한 망원경으로 은하를 관측하는 천문학자들에 관한 내용으로, 참여자의 기여와 혼자서는 수십 년이 걸렸을 것이라는 앞뒤 문장 사이를 끊는다.',
  wrong={1: '웹사이트 개설 직후의 분류 속도로 참여자가 많았음을 보여 준다.',
         2: '1년 반 동안의 참여자 수와 분류 건수를 제시해 흐름을 잇는다.',
         3: '참여자들이 없었다면 불가능했다는 핵심 주장이다.',
         5: '③의 가정에 이어 혼자서는 수십 년이 걸렸을 것이라고 덧붙인다.'})

q(id='Q15', set_id='mock2', number=4, type='요약', first='s34', last='s49',
  summary='When aurora chasers noticed a(n) (A) light in the night sky that even experts could not explain, NASA started a project that depends on the (B) of ordinary people.',
  question='다음 글의 내용을 한 문장으로 요약하고자 한다. 빈칸 (A), (B)에 들어갈 말로 가장 적절한 것은?',
  choices=['familiar …… participation',
           'unfamiliar …… criticism',
           'unfamiliar …… participation',
           'familiar …… donations',
           'dangerous …… participation'],
  answer=3,
  evidence='something strange appearing in the night sky / neither of them had any idea what Steve was / NASA funded a citizen science project involving the public. The project asked ordinary people to gather photos of Steve …',
  explanation='추적자들이 전문가도 설명하지 못하는 낯선(unfamiliar) 빛을 발견했고, NASA는 일반인의 참여(participation)로 사진을 모으는 프로젝트를 지원했다. 따라서 ③이다.',
  choices_ko=['익숙한 …… 참여', '낯선 …… 비판', '낯선 …… 참여', '익숙한 …… 기부', '위험한 …… 참여'],
  wrong={1: '(A) 전문가도 무엇인지 몰랐으므로 familiar(익숙한)는 틀리다.',
         2: '(B) 프로젝트는 일반인에게 사진을 모아 보내 달라고 요청했으므로 criticism(비판)은 틀리다.',
         4: '(A) familiar가 틀리고, (B) 기부(donations)가 아니라 사진을 모으는 참여를 요청했다.',
         5: '(A) 그 빛이 위험하다는 내용은 본문에 없다.'})

q(id='Q16', set_id='mock2', number=5, type='빈칸', first='s50', last='s60',
  blank='capable of making valuable contributions to science',
  question='다음 빈칸에 들어갈 말로 가장 적절한 것은?',
  choices=['unable to understand real scientific research',
           'required to become professional scientists first',
           'less important than the experts at NASA',
           'interested only in taking beautiful photographs',
           'able to do something truly useful for science'],
  answer=5,
  evidence='Experts have acknowledged that it is the dedicated members of the aurora chasers group that deserve the credit … / The next great scientific achievement could be made by citizen scientists …',
  explanation='Even though로 시작하는 양보절(학위나 흰 가운이 없을 수 있다) 뒤에는 그래도 과학에 도움이 되는 일을 할 수 있다는 내용이 와야 한다. 앞의 STEVE 사례와 뒤의 ‘다음 위대한 업적도 시민 과학자가 이룰 수 있다’는 문장도 이를 뒷받침하므로 ⑤가 알맞다.',
  choices_ko=['실제 과학 연구를 이해할 수 없는', '먼저 전문 과학자가 되어야 하는',
              'NASA의 전문가들보다 덜 중요한', '아름다운 사진을 찍는 데에만 관심이 있는',
              '과학에 정말 유용한 일을 할 수 있는'],
  wrong={1: '양보절 뒤 still(여전히)과 이어지려면 긍정적인 내용이어야 하며, 시민 과학자의 기여를 강조하는 글의 흐름과 반대다.',
         2: '학위가 없어도 기여할 수 있다는 흐름과 반대다.',
         3: '전문가들도 오로라 추적자들의 공로를 인정했으므로 덜 중요하다는 말은 흐름에 맞지 않는다.',
         4: '시민 과학자는 관심 분야에서 과학의 발전을 돕고자 하는 사람들이라고 했으므로 사진에만 관심이 있다는 것은 틀리다.'})

q(id='Q17', set_id='mock2', number=6, type='제목', first='s42', last='s55', group='G2',
  question='윗글의 제목으로 가장 적절한 것은?',
  choices=['How NASA Solved the Mystery of STEVE Alone',
           'STEVE: A Discovery Credited to Dedicated Amateurs',
           'Why Experts Refused to Study Strange Lights',
           'The Science Behind Ordinary Auroras',
           'Tips for Taking Better Photos of the Night Sky'],
  answer=2,
  evidence='Experts have acknowledged that it is the dedicated members of the aurora chasers group that deserve the credit for discovering STEVE.',
  explanation='전문가들도 정체를 몰랐던 새로운 현상을 오로라 추적자들이 발견했고, 이름을 유지하고 공로를 인정했으며 지금도 과학자와 시민이 함께 연구한다는 내용이므로 ②가 적절하다.',
  choices_ko=['NASA는 어떻게 혼자서 STEVE의 수수께끼를 풀었는가', 'STEVE: 헌신적인 아마추어들의 공로로 인정된 발견',
              '전문가들은 왜 이상한 빛의 연구를 거부했는가', '평범한 오로라 뒤에 숨은 과학', '밤하늘 사진을 더 잘 찍는 요령'],
  wrong={1: 'NASA는 대중이 참여하는 프로젝트를 지원했고, 수수께끼는 아직 풀리지 않았다.',
         3: '전문가들은 연구를 거부하지 않았고 NASA는 프로젝트에 자금을 지원했다.',
         4: '그것은 오로라가 아니었다.',
         5: '사진 촬영 요령은 다루지 않는다.'})

q(id='Q18', set_id='mock2', number=7, type='어휘', first='s42', last='s55', group='G2',
  marks=[('confirmed', 's45'), ('properly', 's46'), ('gather', 's48'), ('honor', 's50'), ('unnoticed', 's53')],
  replace=('unnoticed', 'famous'),
  question='윗글의 밑줄 친 부분 중, 문맥상 낱말의 쓰임이 적절하지 않은 것은?',
  answer=5,
  evidence='If it had not been for them, it might have remained unnoticed forever.',
  explanation='오로라 추적자들이 없었다면 STEVE는 영원히 알려지지 않은 채로 남았을 것이라는 흐름이므로 ⑤의 famous(유명한)는 맞지 않고 unnoticed(알려지지 않은)가 되어야 한다.',
  wrong={1: '오로라가 아니라는 것은 확인했다(confirmed)는 흐름에 맞다.',
         2: '제대로(properly) 연구된 적이 없는 새로운 현상이라는 뜻으로 적절하다.',
         3: '프로젝트가 일반인에게 사진을 모아(gather) 보내 달라고 요청했다는 흐름에 맞다.',
         4: '처음 발견한 추적자들에게 경의를 표하여(in honor of) 이름을 유지했다는 흐름에 맞다.'})

# ---------------------------------------------------------------- 미니 모의고사 3회
q(id='Q19', set_id='mock3', number=1, type='주장', first='s56', last='s60',
  question='다음 글에서 필자가 주장하는 바로 가장 적절한 것은?',
  choices=['People who are curious about science should take part in research as citizen scientists.',
           'People should earn a science degree before joining any research project.',
           'Citizen scientists should be paid for the time they spend on research.',
           'Only projects about the night sky really need help from the public.',
           'Professional scientists should stop wearing white lab coats.'],
  answer=1,
  evidence='You can become one as well if you have curiosity and an interest in taking part in scientific research. The next great scientific achievement could be made by citizen scientists …',
  explanation='학위나 흰 가운이 없어도 시민 과학자는 귀중한 기여를 할 수 있고, 호기심과 관심만 있으면 누구나 시민 과학자가 될 수 있다며 참여를 권하므로 ①이 주장이다.',
  choices_ko=['과학에 호기심이 있는 사람들은 시민 과학자로서 연구에 참여해야 한다.',
              '사람들은 어떤 연구 프로젝트에 참여하기 전에 과학 학위를 따야 한다.',
              '시민 과학자는 연구에 쓴 시간에 대해 보수를 받아야 한다.',
              '밤하늘에 관한 프로젝트만 대중의 도움이 정말 필요하다.',
              '전문 과학자들은 흰 실험실 가운을 입는 것을 그만두어야 한다.'],
  wrong={2: '과학 학위가 없어도 기여할 수 있다고 했으므로 반대다.',
         3: '시민 과학자는 자신의 시간을 자발적으로 낸다고 했을 뿐 보수를 주장하지 않는다.',
         4: '두 프로젝트는 은하 분류와 STEVE였고, 필자는 특정 분야로 제한하지 않는다.',
         5: '흰 가운은 학위가 없는 시민 과학자와의 대비로 언급되었을 뿐 이를 그만두라는 주장은 없다.'})

q(id='Q20', set_id='mock3', number=2, type='순서', first='s14', last='s23',
  blocks=('s14', 's15', {'A': ('s18', 's19'), 'B': ('s20', 's23'), 'C': ('s16', 's17')}),
  question='주어진 글 다음에 이어질 글의 순서로 가장 적절한 것은?',
  answer=4,
  evidence='(C) “Eventually, the two men ended up launching … Galaxy Zoo.” / (A) “This allowed …”의 This가 (C)의 단순한 웹사이트를 가리키고 New visitors were greeted … / (B) “Then they were shown …”의 they가 (A)의 New visitors를 가리킴.',
  explanation='친구 Lintott이 인터넷에 도움을 청하라고 제안한 뒤, (C) 두 사람이 Galaxy Zoo를 만들고 웹사이트를 단순하게 유지했다. (A) 이 단순함 덕분에 누구나 빨리 시작할 수 있었고 새 방문자는 사용 지침으로 환영받았다. (B) 그다음(Then) 방문자들은 은하 이미지를 보고 버튼을 눌렀고 연습 후 효과적으로 분류했다. 따라서 (C)-(A)-(B)이다.',
  wrong={1: '(A)의 This가 가리킬 단순한 웹사이트가 앞에 없어 연결되지 않는다.',
         2: '(B)의 they(방문자들)가 먼저 나오면 가리킬 대상이 없다.',
         3: '(B)가 (A)보다 먼저 오면 Then과 they가 가리킬 새 방문자가 아직 소개되지 않는다.',
         5: '(C) 다음 (B)가 오면 they(방문자들)가 소개되기 전에 등장해 어색하다.'})

q(id='Q21', set_id='mock3', number=3, type='삽입', first='s24', last='s33', given='s27',
  slots=['s26', 's27', 's29', 's30', 's31'],
  question='글의 흐름으로 보아, 주어진 문장이 들어가기에 가장 적절한 곳은?',
  answer=2,
  evidence='they made more than 75 million classifications. + If it had not been for those participants … + In fact, it would have taken him decades on his own.',
  explanation='주어진 문장은 참여자들이 없었다면 그렇게 많은 이미지를 분류할 수 없었을 것이라는 가정이다. 7,500만 건의 분류를 해냈다는 문장 뒤, 그리고 ‘사실 혼자서는 수십 년이 걸렸을 것’이라는 문장 앞인 ②에 들어가야 In fact가 자연스럽게 이어진다.',
  wrong={1: '①에 넣으면 참여자 수와 분류 건수를 말하기 전에 ‘그렇게 많은 이미지(that many images)’가 나와 가리킬 대상이 불분명하다.',
         3: '③ 앞은 2007년 이후 15년이 흘렀다는 새로운 화제의 시작이라 가정이 끼어들 수 없다.',
         4: '④ 앞뒤는 Zooniverse의 현재 모습에 관한 내용이라 맞지 않는다.',
         5: '⑤ 앞뒤도 Zooniverse의 활동과 프로젝트 소개라 참여자 가정이 들어갈 자리가 아니다.'})

q(id='Q22', set_id='mock3', number=4, type='내용', first='s42', last='s55',
  question='다음 글의 내용과 일치하지 않는 것은?',
  choices=['The group took photos of Steve for several years before asking experts for help.',
           'Neither the professor nor the NASA scientist knew what Steve was.',
           'NASA supported a project that asked the public to send in photos.',
           'The name “Steve” was kept to honor the aurora chasers.',
           'Scientists have now proven one theory about STEVE for certain.'],
  answer=5,
  evidence='There are many interesting theories about STEVE, but none of them have been proven for certain.',
  explanation='STEVE에 관한 흥미로운 이론은 많지만 그중 어느 것도 확실하게 증명되지 않았다고 했으므로 ⑤는 본문과 일치하지 않는다.',
  choices_ko=['그 단체는 전문가에게 도움을 청하기 전에 몇 년 동안 Steve의 사진을 찍었다.',
              '교수와 NASA 과학자 누구도 Steve가 무엇인지 알지 못했다.',
              'NASA는 대중에게 사진을 보내 달라고 요청하는 프로젝트를 지원했다.',
              '‘Steve’라는 이름은 오로라 추적자들에게 경의를 표하기 위해 유지되었다.',
              '과학자들은 이제 STEVE에 관한 한 가지 이론을 확실히 증명했다.'],
  wrong={1: '“After photographing Steve for several years … decided to get help from experts.”와 일치한다.',
         2: '“neither of them had any idea what Steve was.”와 일치한다.',
         3: '“NASA funded a citizen science project … asked ordinary people to gather photos of Steve and send them to NASA.”와 일치한다.',
         4: '“In honor of the aurora chasers … the name ‘Steve’ has been kept.”와 일치한다.'})

q(id='Q23', set_id='mock3', number=5, type='빈칸', first='s34', last='s41',
  blank='some notably different features',
  question='다음 빈칸에 들어갈 말로 가장 적절한 것은?',
  choices=['characteristics that set them apart from auroras',
           'exactly the same colors that all auroras have',
           'no connection at all to the night sky',
           'a shape that nobody was able to photograph',
           'a name that scientists had already given them'],
  answer=1,
  evidence='They were similar in appearance to auroras, yet … / Unsure of what they were, the group decided to name the phenomenon “Steve,” …',
  explanation='yet(그렇지만)이 ‘생김새는 오로라와 비슷했다’와 대조를 이루므로 빈칸에는 오로라와 다른 점이 와야 한다. 또 다음 문장에서 무엇인지 확신하지 못했다고 하므로 ①이 알맞다.',
  choices_ko=['그것들을 오로라와 구별해 주는 특징들', '모든 오로라가 가진 것과 똑같은 색깔',
              '밤하늘과는 전혀 관련이 없음', '아무도 사진을 찍을 수 없었던 모양', '과학자들이 이미 붙여 준 이름'],
  wrong={2: 'yet 뒤에는 오로라와 비슷한 점이 아니라 다른 점이 와야 하므로 흐름에 맞지 않는다.',
         3: '그 빛은 밤하늘에 나타났으므로 틀리다.',
         4: '단체 구성원들은 오로라 사진을 찍어 공유했고, 사진을 찍을 수 없었다는 근거는 없다.',
         5: '이름은 과학자가 아니라 단체가 붙였으므로 틀리다.'})

q(id='Q24', set_id='mock3', number=6, type='제목', first='s01', last='s13', group='G3',
  question='윗글의 제목으로 가장 적절한 것은?',
  choices=['Why Scientists Should Work Alone in Their Labs',
           'The Long History of the White Lab Coat',
           'Science for Everyone: A Task Too Big for One Scientist',
           'How to Classify Galaxies by Their Color',
           'Ordinary People Have Nothing to Do with Science'],
  answer=3,
  evidence='In reality, science belongs to everyone … / He had to classify around one million images … It took Schawinski a whole week to classify just 50,000 galaxies.',
  explanation='과학은 모두의 것이라는 주장을 제시한 뒤, 한 연구원이 혼자서 감당하기 어려운 백만 장의 은하 분류 작업을 맡게 된 사례를 소개한다. 따라서 ③이 제목으로 적절하다.',
  choices_ko=['과학자들은 왜 실험실에서 혼자 일해야 하는가', '흰 실험실 가운의 오랜 역사',
              '모두를 위한 과학: 과학자 한 명에게는 너무 큰 과업', '은하를 색깔에 따라 분류하는 방법',
              '평범한 사람들은 과학과 아무 관련이 없다'],
  wrong={1: '과학은 모두의 것이라는 주장과 반대다.',
         2: '흰 가운은 흔한 인식의 예로 잠깐 나올 뿐 역사를 다루지 않는다.',
         4: '은하는 색깔이 아니라 모양에 따라 분류해야 했다.',
         5: '그런 인식은 사실과 거리가 멀다고 했으므로 반대다.'})

q(id='Q25', set_id='mock3', number=7, type='어휘', first='s01', last='s13', group='G3',
  marks=[('exclusively', 's01'), ('little', 's02'), ('remarkable', 's05'), ('dull', 's08'), ('individually', 's10')],
  replace=('little', 'much'),
  question='윗글의 밑줄 친 부분 중, 문맥상 낱말의 쓰임이 적절하지 않은 것은?',
  answer=2,
  evidence='we might consider it as a domain reserved exclusively for scientists … They seem to have very little in common with ordinary people like us. However, this perception is far from the truth.',
  explanation='과학이 과학자들만의 영역이라는 흔한 인식을 설명하는 부분이므로 과학자들은 우리 같은 평범한 사람들과 공통점이 거의 없어 보인다(little)가 되어야 한다. ②의 much(많은)는 뒤의 However로 뒤집히는 인식과 맞지 않는다.',
  wrong={1: '과학이 과학자들만을 위한(exclusively) 영역이라는 흔한 인식을 나타내므로 적절하다.',
         3: '평범한 사람들이 놀라운(remarkable) 과학적 업적에 기여했다는 흐름에 맞다.',
         4: '흥미롭게 들릴 수 있지만(But) 실제로는 따분했다는 대조이므로 적절하다.',
         5: '비슷해 보이지만 모양이 조금씩 달라서 하나씩(individually) 보며 분류해야 했다는 흐름에 맞다.'})


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
                import re
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
            g0, g1, blocks = row['blocks']
            spans = _order_spans(row, B, a, len(original))
            req['block_spans'] = spans
        elif kind == '무관한 문장':
            req['addition_offset'] = rel(row['add_before'])
            req['addition'] = row['addition']
            req['sentence_marks'] = row['marks']
        grouped = 'group' in row
        bench_type = 'long41_42' if grouped else kind
        probe = dict(req, length_review={'profile_id': LENGTH_PROFILE_ID, 'grade': 2,
                                         'benchmark_ids': recommended_benchmarks(2, bench_type),
                                         'rationale': 'probe', 'independent_review_required': True})
        view = build_view(src, probe, expected_grade=2, benchmark_type=bench_type)
        lc = view['length_comparison']
        refs = lc['reference_words']
        short = lc['shorter_than_all_references']
        rationale = (f"{'공유 장문 41~42' if grouped else kind} 고2 표본 {refs}단어와 비교해 현재 {lc['assessment_word_count']}단어. "
                     + (BENCH_SHORT_NOTE if short else '표본 범위 이상으로 너무 짧지 않음. ')
                     + '연속 원문 범위 안에서 정답과 네 오답의 근거가 자족적임.')
        req['length_review'] = {'profile_id': LENGTH_PROFILE_ID, 'grade': 2,
                                'benchmark_ids': recommended_benchmarks(2, bench_type), 'rationale': rationale}
        if short:
            req['length_review']['independent_review_required'] = True
        view = build_view(src, req, expected_grade=2, benchmark_type=bench_type)
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


def blocks_start(blocks, B, g1, row, a):
    return row['blocks'][2]


def _order_spans(row, B, a, total):
    g0, g1, blocks = row['blocks']
    starts = {k: B[v[0]]['start'] - a for k, v in blocks.items()}
    ordered = sorted(starts.items(), key=lambda kv: kv[1])
    spans = {'given': [0, ordered[0][1]]}
    for i, (k, s) in enumerate(ordered):
        e = ordered[i + 1][1] if i + 1 < len(ordered) else total
        spans[k] = [s, e]
    return spans
