"""권위 원문 PDF에서 전사한 공통영어2 YBM(박준언) 2과 본문(1~3쪽).

PDF 텍스트층의 왼쪽 단 영어 줄을 공백으로 이어 단락을 만들고, 문장은 아래 목록으로 확정한다.
단락 32개는 원본 쪽 이미지의 들여쓰기로 확인했다. 제목 Dry는 본문 문장에 넣지 않는다.
원문에 소제목이 없다(무소제목 소설 본문 + 별표 작품 소개 단락).
4쪽 Further Reading은 사용자 결정(2026-09-28 “나중에 별도 교재로”)으로 이번 범위에서 뺀다.

직접 인용 안에 마침표·물음표가 있으면 그 기호에서 문장을 나누고, 여는 따옴표는 첫 조각에,
닫는 따옴표와 전달절(… says 등)은 마지막 조각에 둔다. 인용문 안의 쉼표(“Mom,” …)는 나누지 않는다.
p32 첫 글자 *(작품 소개 표시)와 곡선 따옴표·아포스트로피·줄표(—)는 원문 그대로 둔다.
"""

TITLE = 'Dry'

PARAGRAPHS = [
    # (paragraph id, subheading id or None, [sentences])
    ('p01', None, [
        'The kitchen tap makes strange sounds.',
        'It coughs.',
        'It spits once, and then goes silent.',
    ]),
    ('p02', None, [
        '“Mom,” I shout out into the living room, “water is not coming out.”',
    ]),
    ('p03', None, [
        '“Alyssa, shush!” Mom says.',
    ]),
    ('p04', None, [
        'She is watching the TV, where a news anchor is talking about the “flow crisis.”',
        'This is what the media has been calling the drought ever since people got tired of hearing the word “drought.”',
        'Now the crisis is entering a new stage.',
        'We have no running water out of the tap.',
    ]),
    ('p05', None, [
        '“To the mall!” says Uncle Basil.',
        'My little brother Garrett and I jump in our uncle’s truck.',
    ]),
    ('p06', None, [
        'As we pull into the parking lot, we can see the crowd.',
    ]),
    ('p07', None, [
        '“You two go in.',
        'I’ll meet you inside,” Uncle Basil says.',
    ]),
    ('p08', None, [
        'Inside it’s like Black Friday at its worst — but today it’s not televisions and video games people are after.',
        'What I see in the carts in the checkout line are mostly water bottles.',
        'The essentials of life.',
    ]),
    ('p09', None, [
        'There is a look of impatience on the faces of the people in line.',
        'There is even hostility, hidden by a thin layer of politeness.',
        'Even that politeness is stretched thin.',
    ]),
    ('p10', None, [
        'As I approach the back of the store for water bottles, I realize I am too late.',
        'The shelves are already empty.',
    ]),
    ('p11', None, [
        'I manage my way to the side aisle, trying my luck.',
        'Sometimes people place unwanted items in the wrong shelves.',
        'Lucky!',
        'I find a single case of water that someone abandoned there maybe yesterday, when it wasn’t such a precious commodity.',
    ]),
    ('p12', None, [
        'I reach for it, only to find it pulled away at the last second by a woman.',
        'She stacks it on top of her cart like a crown on top of her canned goods.',
    ]),
    ('p13', None, [
        '“I’m sorry, but we were here first,” she says.',
        'And then her daughter steps forward — a girl I recognize from soccer — Hali Hartling.',
        'As her mother pulls their cart away, Hali leans closer to me.',
        '“I’m sorry about that, Alyssa.”',
    ]),
    ('p14', None, [
        '“Didn’t I share my water with you at the practice last week?” I point out to her.',
        '“Maybe you could return the favor and share a few bottles with me.”',
    ]),
    ('p15', None, [
        'She looks back to her mother, who’s already moving down the aisle, then turns back to me shaking her head.',
        'And then she gets a little bit red in the face, and turns to leave before it becomes a deep flush.',
    ]),
    ('p16', None, [
        'I look for Garrett, whom I find in the frozen aisle.',
        'Then I see something.',
        'Just past the frozen vegetables and ice cream, there is a case packed with ice.',
        'I open the door and reach for a bag.',
    ]),
    ('p17', None, [
        '“What are you doing?',
        'We need water, not ice,” he reminds me.',
    ]),
    ('p18', None, [
        '“Ice is water.',
        'Just help me,” I tell him.',
    ]),
    ('p19', None, [
        'Garrett and I put one bag of ice after another into our cart, until it is piled as high as it can get.',
        'By now other people have taken notice and begin to empty the ice case.',
    ]),
    ('p20', None, [
        'The cart is ridiculously heavy now, and almost impossible to push.',
        'Then, a man in a business suit comes up behind us.',
        'He smiles.',
    ]),
    ('p21', None, [
        '“Looks like you could use some help.”',
        'He doesn’t wait for us to answer before grabbing the cart’s handle.',
    ]),
    ('p22', None, [
        '“Thank you for helping us,” I tell him.',
    ]),
    ('p23', None, [
        '“Not a problem.',
        'We all need to help one another.”',
        'He smiles again, and I return the smile.',
        'It is good to know that difficult times can bring out the best in people.',
        'I decide that one favor deserves another.',
    ]),
    ('p24', None, [
        '“Why don’t you take a bag of ice for yourself,” I suggest.',
    ]),
    ('p25', None, [
        'His smile does not fade.',
        '“I have a better idea,” he says.',
        '“Why don’t you take a bag of ice for yourselves, and I’ll keep the rest.”',
    ]),
    ('p26', None, [
        'For a moment I think he is joking, but then realize he is serious.',
        '“Excuse me?”',
    ]),
    ('p27', None, [
        'He is still smiling, but his eyes scare me.',
        'As long as his hands are firmly locked on the handle of our cart, there is nothing to prove that it’s ours and not his.',
    ]),
    ('p28', None, [
        '“Is there a problem here?”',
    ]),
    ('p29', None, [
        'It is Uncle Basil.',
        'He has arrived just in time.',
    ]),
    ('p30', None, [
        '“Not at all.”',
    ]),
    ('p31', None, [
        'The man looks at the ice with a bitter face, then leaves.',
    ]),
    ('p32', None, [
        '*The above is a shortened version of the opening of the novel Dry (2018).',
        'It tells the story of a girl who has to make tough choices for her family during a disastrous California drought.',
        'Her unwanted adventure ends when the water supply resumes and life is back to normal.',
        'Provided that the factors contributing to water shortages worldwide are not addressed, including climate change, population growth, and using too much water for agriculture, it is possible that this story can become a reality.',
    ]),
]

SUBHEADINGS = []

# 사용자 결정(2026-09-28 “5단위, 작품 소개 합침”): 무소제목 본문을 장면 기준 5단위로 묶는다.
UNIT_PARAGRAPHS = {
    'u1': ['p01', 'p02', 'p03', 'p04', 'p05', 'p06', 'p07', 'p08'],
    'u2': ['p09', 'p10', 'p11', 'p12', 'p13', 'p14', 'p15'],
    'u3': ['p16', 'p17', 'p18', 'p19'],
    'u4': ['p20', 'p21', 'p22', 'p23', 'p24', 'p25'],
    'u5': ['p26', 'p27', 'p28', 'p29', 'p30', 'p31', 'p32'],
}


def build():
    """Return (text, sentence bounds, paragraph rows) with sequential IDs s01…"""
    parts, bounds, rows, offset, n = [], [], [], 0, 0
    for pi, (pid, heading, sentences) in enumerate(PARAGRAPHS):
        if pi:
            parts.append('\n'); offset += 1
        ids = []
        for si, sentence in enumerate(sentences):
            if si:
                parts.append(' '); offset += 1
            n += 1
            sid = f's{n:02d}'
            parts.append(sentence)
            bounds.append({'id': sid, 'start': offset, 'end': offset + len(sentence)})
            offset += len(sentence)
            ids.append(sid)
        rows.append({'id': pid, 'source_id': 'src', 'subheading_id': heading, 'sentence_ids': ids})
    return ''.join(parts), bounds, rows


if __name__ == '__main__':
    text, bounds, rows = build()
    counts = {u: sum(len(r['sentence_ids']) for r in rows if r['id'] in ps) for u, ps in UNIT_PARAGRAPHS.items()}
    print(len(rows), '단락', len(bounds), '문장', counts)
