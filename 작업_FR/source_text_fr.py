"""권위 원문 PDF 5쪽 Further Reading ‘Happiness Comes From Experiences’ 전사.

PDF 텍스트층의 영어 줄을 공백으로 이어 단락을 만들고 문장은 아래 목록으로 확정한다.
단락 4개는 들여쓰기로 확인했다. 섹션 표시 Further Reading과 제목은 본문 문장에 넣지 않는다.
인용문(Gilovich의 말)은 인용 안의 마침표 기준으로 문장을 나누고 여는·닫는 따옴표는 첫·끝 문장에 둔다.
"""

PARAGRAPHS = [
    ('p01', None, [
        'A long-term study conducted by Thomas Gilovich, a psychology professor at Cornell University, reached a powerful and clear conclusion: Don’t spend your money on things.',
        'We assume that the happiness we get from buying something will last as long as the thing itself.',
        'But it’s wrong.',
        'The trouble with things is that the happiness they provide fades quickly.',
        'There are three critical reasons for this.',
    ]),
    ('p02', None, [
        'First, we get used to new possessions.',
        'What once seemed novel and exciting quickly becomes the norm.',
        'Second, we keep raising the bar.',
        'New purchases lead to new expectations.',
        'As soon as we get used to a new possession, we look for an even better one.',
        'Third, possessions stimulate humans to compare themselves with others.',
        'We buy a new car and are thrilled with it until a friend buys a better one, and there’s always someone with a better one.',
    ]),
    ('p03', None, [
        'Gilovich and other researchers have found that experiences deliver longer lasting happiness than things.',
        'That’s because experiences become a part of our identity.',
        'We are not our possessions, but we are the accumulation of everything we’ve seen, the things we’ve done, and the places we’ve been to.',
    ]),
    ('p04', None, [
        '“Our experiences are a bigger part of ourselves than our material goods,” says Gilovich.',
        '“You can really like your material stuff.',
        'You can even think that part of your identity is connected to those things, but nonetheless they remain separate from you.',
        'On the other hand, your experiences really are part of you.',
        'We are the sum total of our experiences.”',
    ]),
]

SUBHEADINGS = []
TITLE = 'Happiness Comes From Experiences'


def build():
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
