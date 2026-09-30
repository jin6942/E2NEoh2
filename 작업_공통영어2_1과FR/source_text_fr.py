"""권위 원문 PDF 4쪽 Further Reading ‘Breaking Out of the Echo Chamber’ 전사.

PDF 텍스트층의 왼쪽 단 영어 줄을 공백으로 이어 단락을 만들고 문장은 아래 목록으로 확정한다.
단락은 1개(들여쓰기 1곳). 섹션 표시 Further Reading과 제목은 본문 문장에 넣지 않는다.
"""

PARAGRAPHS = [
    ('p01', None, [
        'These days, everyone accesses the news through the Internet or social media, and often selectively takes the information that suits their tastes or beliefs.',
        'However, consistently encountering similar perspectives without considering alternative views can lead you to be trapped in an “echo chamber.”',
        'An echo chamber refers to an enclosed space where sound doesn’t leak out and returns as an echo.',
        'The term “echo chamber” is also used to describe any situation in which you only hear opinions you already agree with.',
        'This can distort your understanding of reality, and limit your ability to think critically and engage in meaningful debates.',
        'Worse still, an echo chamber may foster social division, making collaboration on common issues challenging.',
        'To avoid falling into this trap, you must actively seek diverse sources of information and engage with people who have different views.',
        'Always remember to check the information you receive, and keep an open mind when discussing new ideas.',
        'Even if you really want something to be true, it doesn’t always mean that it is true.',
    ]),
]

SUBHEADINGS = []
TITLE = 'Breaking Out of the Echo Chamber'


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
