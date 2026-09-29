"""권위 원문 PDF 4쪽 Further Reading “Hunger Stones” 전사(공통영어2 YBM(박준언) 2과).

PDF 텍스트층 왼쪽 단 영어 줄을 공백으로 이어 단락을 만들고 문장은 아래 목록으로 확정한다.
단락 3개는 줄 첫 글자 위치(들여쓰기)로 확인했다. 제목 Hunger Stones는 본문 문장에 넣지 않는다.
소제목이 없다. 곡선 따옴표·콜론 뒤 인용은 원문 그대로 둔다(인용 안 마침표는 문장 끝과 같아 나누지 않음).
"""

TITLE = 'Hunger Stones'

PARAGRAPHS = [
    ('p01', None, [
        'In the summer of 2022, during the worst drought in 500 years in Europe, a stone known as a “hunger stone” was found in a Czech town along the Elbe River.',
        'The stone had a sentence written on it that read: “If you see me, then cry.”',
    ]),
    ('p02', None, [
        'The hunger stones, found in rivers across central Europe, typically remain underwater.',
        'However, when droughts occur and water levels retreat, these stones become visible.',
        'The stones are significant because they bear records of the past severe droughts.',
        'Droughts cause reduced harvests, food shortages, and hunger, especially for the poor.',
        'The words on the hunger stones are believed to warn of these hardships and to urge people to be prepared.',
    ]),
    ('p03', None, [
        'Considering the continuation of climate change, experts warn that the situation we face is not just a simple, occasional drought but a severe drought that could persist for decades.',
        'The United Nations has predicted that by 2050, 75 percent of the global population could suffer from the effects of drought unless significant action is taken to address climate change.',
    ]),
]

UNIT_PARAGRAPHS = {'u1': ['p01', 'p02', 'p03']}


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
