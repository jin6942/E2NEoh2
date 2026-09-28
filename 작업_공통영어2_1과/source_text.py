"""권위 원문 PDF에서 전사한 공통영어2 YBM(박준언) 1과 본문(1~3쪽).

PDF 왼쪽 단 영어 추출 줄을 공백으로 이어 단락을 만들고, 문장은 아래 목록으로 확정한다.
단락은 원본의 들여쓰기로 확인했다. 제목(Warning: Fake News Alert!)·소제목은 본문 문장에 넣지 않는다.
4쪽 Further Reading(Breaking Out of the Echo Chamber)은 사용자 결정(2026-09-28 “본문 먼저, FR은 따로”)으로 범위에서 뺀다.
"""

PARAGRAPHS = [
    # (paragraph id, subheading id or None, [sentences])
    ('p01', None, [
        'While scrolling through her social media one day, Gina was astonished when she saw the news headline, “The Heundeulbawi in Seoraksan National Park Has Fallen.”',
        'Gina immediately shared the shocking story with her close friends.',
        'Later, during the morning news on TV, a reporter standing next to the undamaged Heundeulbawi said, “Today’s Internet stories of the Heundeulbawi being damaged were fake.”',
        'Gina was embarrassed by the fact that she had spread the fake news.',
    ]),
    ('p02', None, [
        'It reminded her of another incident of fake news that had happened a while ago.',
        'The news that a famous athlete had died became the number one issue online, but it turned out to be fake.',
        'It had been made by content creators who sought people’s attention.',
        'They produced provocative false stories to make money by raising the number of views of their posts.',
        'At that time, Gina criticized those who had made and spread fake news because it had hurt the athlete and confused people.',
        'This time, however, Gina herself had accidentally contributed to the spread of fake news.',
    ]),
    ('p03', 'h-impact', [
        'Unfortunately, becoming an accidental distributor of fake news like Gina is not unusual.',
        'Fake news is a deliberate attempt to manipulate people by spreading inaccurate information.',
        'It is made by certain groups with the intention of attracting people’s attention, making profits, or gaining political benefits.',
        'It can confuse people, disturb society, and even seriously harm the public as well as all individuals involved.',
    ]),
    ('p04', 'h-impact', [
        'It is very common for fake news to spread during states of emergency.',
        'For example, after an earthquake measuring 6.5 struck Ambon, Indonesia, in September 2019, thousands of residents did not return to their homes and were still in shelters for two weeks.',
        'This was because of fake news stories on social media that another earthquake followed by a tsunami was about to strike.',
        'One of those messages said, “It’s up to you if you want to believe me or not, but apparently Ambon is going to sink in the next few days.”',
        'Many displaced people were so anxious about aftershocks that the government had to announce that the information was fake.',
    ]),
    ('p05', 'h-reasons', [
        'Fake news on social media spreads significantly farther and faster than true stories.',
        'A study by the Massachusetts Institute of Technology in the US has shown that fake news spreads online 6 times faster than real news on average.',
    ]),
    ('p06', 'h-reasons', [
        'One explanation for this phenomenon is that people like new and provocative things.',
        'When information is astonishing, people not only feel that it is surprising, but they also want to share the stimulating news with others.',
        'By passing it to others on social media, they can gain attention because they are the first to post previously unknown, but possibly false, information.',
        'Also, fake news goes viral because people in their daily lives tend to think simply and effortlessly.',
        'It is more likely for them to believe new information without any proof, instead of critically examining it.',
    ]),
    ('p07', 'h-reasons', [
        'Moreover, people are inclined to believe information that fits their prejudices or experiences even when not true.',
        'In this process, people easily fall into the trap of “confirmation bias.”',
        'That is, they selectively accept news in a way that only confirms their beliefs and ignore news that doesn’t support them.',
        'During election season, for example, people tend to blindly believe any news describing their favored candidates in a positive way, while unconsciously believing news that reports something negative about other candidates.',
    ]),
    ('p08', 'h-ways', [
        'With so much information on the Internet, how can you make sure that fake news does not mislead you?',
        'First, read beyond the provocative headlines.',
        'They can be so stimulating to get more clicks that you may click on them accidentally.',
        'So don’t just read the headlines, but read the text carefully.',
        'Second, don’t read the news at face value.',
        'Exercise critical thinking skills to judge the news.',
    ]),
    ('p09', 'h-ways', [
        'You should question, analyze, and evaluate what you read.',
        'Third, examine your biases.',
        'Consider if your own beliefs could affect your judgment.',
        'Ask yourself if you are only reading articles that suit your opinion, and look for articles that oppose your opinion as well.',
        'Finally, check the credibility of the source.',
        'You should examine who wrote the news story and what the intent was behind writing the news story.',
        'You also need to check whether the news story is from a reliable media source and the evidence is valid.',
    ]),
    ('p10', 'h-ways', [
        'In the digital age, it might be impossible to avoid or eliminate all false information that spreads online.',
        'However, if you have the ability to view information critically and objectively, you will be able to reduce the damage that fake news can cause.',
        'Don’t forget!',
        'Anyone can be the next person producing or spreading fake news!',
    ]),
]

SUBHEADINGS = [
    {'id': 'h-impact', 'text': 'The Impact of Fake News on Society',
     'location': '원본 PDF 1쪽 왼쪽 단 아래(‘Unfortunately, becoming’ 단락 위)', 'before': 'p03'},
    {'id': 'h-reasons', 'text': 'The Reasons for the Viral Spread of Fake News',
     'location': '원본 PDF 2쪽 왼쪽 단 중간(‘Fake news on social media’ 단락 위)', 'before': 'p05'},
    {'id': 'h-ways', 'text': 'Ways to Spot and Avoid Fake News',
     'location': '원본 PDF 3쪽 왼쪽 단 맨 위(‘With so much information’ 단락 위)', 'before': 'p08'},
]


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
