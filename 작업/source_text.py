"""권위 원문 PDF에서 전사한 영어II YBM(박준언) 2과 본문(1~4쪽).

PDF 추출 줄을 공백으로 이어 단락을 만들고, 문장은 아래 목록으로 확정한다.
단락은 원본의 들여쓰기로 확인했다. 제목·소제목은 본문 문장에 넣지 않는다.
5쪽 Further Reading은 사용자 결정(2026-09-27 “제외”)으로 범위에서 뺀다.
"""

PARAGRAPHS = [
    # (paragraph id, subheading id or None, [sentences])
    ('p01', None, [
        'Jiyun, a high school student, starts her day by logging in to a music streaming service on her smartphone.',
        'She enjoys listening to her favorite music, discovering new songs, and exploring new artists every day.',
        'For a healthy breakfast, Jiyun receives a delivery from a subscription service that provides fresh vegetables and fruits.',
        'After school, Jiyun utilizes a video lecture service to expand her knowledge in whatever she finds interesting.',
        'For example, she watches various academic lectures to review her schoolwork and stay updated about the latest knowledge in her chosen field of study.',
        'During weekends, Jiyun and her family spend quality time together watching movies or dramas using a streaming service.',
    ]),
    ('p02', 'h-everywhere', [
        'To be sure, the subscription economy is a popular economic model nowadays, and Jiyun is actively taking part in it.',
        'The concept of business models based on subscriptions is not new.',
        'Initially it was limited to products such as milk and newspapers.',
        'However, these business models have expanded to all industries, including entertainment, technology, fashion, education, and much more.',
        'Instead of creating a hit product that will be sold once, companies now prioritize providing continuing value, such as new content, more personalization, or access to updates.',
        'Customers pay for these benefits via a regular subscription.',
    ]),
    ('p03', 'h-everywhere', [
        'The subscription economy brings advantages for both companies and consumers.',
        'Companies can have a stable revenue and build customer loyalty by using the subscription model.',
        'From the consumers’ perspective, they can enjoy a wider range of choices and personalized experiences.',
        'They can also save money by having flexible subscription contracts.',
    ]),
    ('p04', 'h-everywhere', [
        'The rise of the subscription economy is closely connected to two major drivers: changes in consumption trends and the rapid growth of online platforms.',
    ]),
    ('p05', 'h-love', [
        'The subscription economy is highly relevant to how people consume goods and services nowadays.',
        'More and more people prioritize experiences over owning things.',
        'This makes the subscription economy attractive to them because it offers access to services or content without the requirement of ownership.',
        'For example, by subscribing to a music streaming service, consumers can enjoy limitless music without the need for having disc albums.',
        'Another example is subscribing to clothing services, where consumers can explore a variety of clothing styles without filling up their drawers.',
    ]),
    ('p06', 'h-love', [
        'Moreover, consumers value diversity and customization.',
        'The subscription economy offers a diverse range of subscription options, enabling individuals to personalize their experiences based on their own preferences and interests.',
        'This aspect of the subscription economy is more popular among younger generations, as they enjoy expressing their uniqueness and discovering valuable content and services that fit with their individual tastes.',
        'A popular example that has gained attention is the cosmetics subscription service.',
        'It stands out by thoroughly analyzing customers’ current skin conditions and providing specialized recommendations, including manufacturing cosmetics created to address each individual’s unique skin concerns.',
        'To come to the point, consumers receive a personalized experience that prioritizes their individual skin conditions, rather than a uniform purchasing process.',
    ]),
    ('p07', 'h-love', [
        'Furthermore, consumers appreciate flexibility and convenience.',
        'In some subscription models, consumers can experience a variety of products or services for a fixed cost.',
        'In other models, they can flexibly adjust subscription fees by choosing only the necessary services or products when needed.',
        'This means they can either enjoy a range of offerings for a set price or save money by selecting only what they really need.',
        'Moreover, subscription services are made easily accessible by online platforms, enhancing consumers’ convenience.',
        'With just a few clicks, consumers can receive services or products.',
        'If they wish to change their device model, they can do so.',
        'Whoever desires an upgrade can get it and experience the latest models.',
    ]),
    ('p08', 'h-online', [
        'With the development of various digital devices centered on smartphones, consumers have been able to do numerous things with great ease.',
        'In the past, people had no choice but to go to the theater or purchase the videos they wanted to watch.',
        'Today, whoever wants to watch a movie can access online media subscription platforms and enjoy a vast selection of movies on their smartphones or other digital devices.',
    ]),
    ('p09', 'h-online', [
        'At the same time, these platforms make it easy for companies to offer customized products and services to customers.',
        'By applying AI and big data algorithm technology, companies identify consumers’ needs, tastes, and consumption patterns.',
        'People appreciate having diverse choices and customization, which in turn enhances their satisfaction.',
        'Services, such as suggesting personalized clothing styles based on customers’ purchase history or recommending videos that match their movie and video viewing history, bring them great satisfaction.',
    ]),
    ('p10', 'h-limits', [
        'Although the subscription economy offers many advantages, there are also some disadvantages to consider.',
        'One concern is the potential for overconsumption.',
        'The convenience and accessibility of the subscription model make it easy for consumers to sign up for multiple services and use a lot of content or products.',
        'This can result in excessive consumption and using more subscription services than actually needed.',
        'It is crucial to subscribe only to services that are truly necessary and avoid subscribing to similar services.',
    ]),
    ('p11', 'h-limits', [
        'Related to the concern of overconsumption is the financial burden that subscriptions can create.',
        'While the cost of individual subscriptions may seem affordable, subscribing to multiple services can add up quickly.',
        'It is important to carefully consider the costs of these subscriptions to avoid financial strain.',
        'Regularly reviewing and canceling unnecessary subscriptions can be beneficial.',
    ]),
    ('p12', 'h-limits', [
        'Additionally, the subscription economy can contribute to environmental pollution.',
        'The regular delivery of products in packaging materials can increase the use of disposable packaging, which harms the environment.',
        'Using environmentally friendly packaging materials and opting for reusable packaging can help reduce this problem.',
    ]),
    ('p13', 'h-limits', [
        'Despite the potential limitations of subscription services, they have become deeply embedded in our lives and more and more businesses are jumping onto the subscription economy model.',
        'It is expected that new subscription services will be continuously provided to consumers in new areas in the future.',
        'We need to have a deeper understanding of the subscription economy and become wise consumers who receive the services that are really needed.',
    ]),
]

SUBHEADINGS = [
    {'id': 'h-everywhere', 'text': 'Subscriptions are everywhere',
     'location': '원본 PDF 1쪽 왼쪽 단 중간(‘To be sure’ 단락 위)', 'before': 'p02'},
    {'id': 'h-love', 'text': 'People love the subscriptions',
     'location': '원본 PDF 2쪽 왼쪽 단 맨 위(‘The subscription economy is highly relevant’ 단락 위)', 'before': 'p05'},
    {'id': 'h-online', 'text': 'Online platforms drive the subscription economy',
     'location': '원본 PDF 3쪽 왼쪽 단 맨 위(‘With the development’ 단락 위)', 'before': 'p08'},
    {'id': 'h-limits', 'text': 'Limitations of the subscription economy',
     'location': '원본 PDF 3쪽 왼쪽 단 중간(‘Although the subscription economy’ 단락 위)', 'before': 'p10'},
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
