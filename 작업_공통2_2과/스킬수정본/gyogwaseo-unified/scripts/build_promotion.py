"""Derive optional, unpublished promotional text from the checked manuscript.

Does not fetch links, publish, infer release status, or advertise past products.
Each requested output is explicit; output files are created exclusively.
"""
import argparse
import json
from pathlib import Path
from urllib.parse import urlparse

from check_learning_content import check
from book_plan import gloss_text


def context(data):
    result = check(data)
    if result['status'] != 'STRUCTURE_PASS':
        raise ValueError('Learning manuscript structure must pass')
    by_id = {(s['source_id'], s['id']): s for s in data['sentences']}
    sentences = [by_id[(source['id'], item['id'])]
                 for source in data['sources'] for item in source['sentences']]
    return result, sentences


def chunks(s):
    return [s['text'][c['start']:c['end']] for c in s['chunks']]


def checked_link(promo, key):
    value = promo.get('links', {}).get(key)
    if value is None:
        return '미정 — 실제 주소 확인 후 입력'
    if not isinstance(value, dict) or not value.get('verification_record', '').strip():
        raise ValueError('Each supplied link requires an actual verification record')
    address = value.get('url', '')
    parsed = urlparse(address)
    if parsed.scheme not in {'https', 'http'} or not parsed.netloc or '\n' in address:
        raise ValueError('Expected a verified HTTP(S) link')
    return address


def render(data):
    result, sentences = context(data)
    promo = data.get('promotion', {})
    m = data['metadata']
    title = f'{m["course"]} {m["publisher_author"]} {m["lesson"]}'
    target = promo.get('target_label', '내신 3등급 이하 (5등급제)')
    review = promo.get('review_record')
    if review is not None and (not isinstance(review, str) or not review.strip()):
        raise ValueError('Review record must be a nonempty evidence location')
    status = '검수 기록: ' + review if review else '검수 상태: 독립 내용 검수 완료 여부 확인 필요'
    sample_count = promo.get('preview_count', 3)
    if type(sample_count) is not int or sample_count < 1:
        raise ValueError('preview_count must be a positive integer')
    previews = sentences[:sample_count]
    gloss_count = sum(len(s['glosses']) for s in sentences)
    steps = ['· 영어 끊어읽기 표시대로 의미 덩어리를 확인하기',
             '· 주어(S)·동사(V)를 확인하고 각주를 참고하기',
             '· 나의 해석 칸에 직접 쓰기',
             '· 지문 분석지의 영어·한국어 끊어읽기와 자연 해석 비교하기']
    scope = f'본문 {len(sentences)}문장 · 공통 학습 단위 {len(data["units"])}개 · 각주 {gloss_count}개'
    blog = [f'{title} 본문 해석ㅣ끊어읽기 혼공해석지', '', status, '',
            '안녕하세요. TOM’S EDU 교과서 학습 자료를 소개합니다.',
            f'대상: {target}', scope, '', '▶ 학습 순서', *steps, '', '▶ 앞부분 미리보기']
    for i, s in enumerate(previews, 1):
        glosses = s['glosses'][:5]
        blog += [f'{i}. ' + ' / '.join(chunks(s)),
                 result['sv_lines'][f'{s["source_id"]}/{s["id"]}'],
                 '※ ' + ' / '.join(('★ ' if g['star'] else '') + gloss_text(g) for g in glosses)]
        if len(s['glosses']) > len(glosses):
            blog.append('… 각주는 일부 미리보기이며 전체 내용은 학습지에서 확인하세요.')
        if i == 1:
            blog.append('[분석지 해석 예시] ' + s['natural_ko'])
        blog.append('')
    blog += [f'→ 남은 {max(0,len(sentences)-len(previews))}문장은 전체 자료에서 이어서 학습하세요.',
             '', '▶ 전체 자료', '▷ 학습지: ' + checked_link(promo, 'download'),
             '▷ 관련 자료 모음: ' + checked_link(promo, 'collection')]
    related = promo.get('related_product')
    if related:
        if not all(isinstance(related.get(k), str) and related[k].strip()
                   for k in ('verified_copy', 'verification_record')):
            raise ValueError('Related product copy requires current approved text and evidence')
        blog += ['', '▶ 관련 학습 자료', related['verified_copy']]
    blog += ['', '── TOM’S EDU']
    cafe1 = [f'{title} 본문 해석ㅣ끊어읽기 + 직접 해석 연습지 ({target})',
             '', status, scope, '', '의미 덩어리와 주어·동사를 확인하고 직접 해석해 보는 자료입니다.',
             *steps, '', '▷ 미리보기와 자료 안내: '+checked_link(promo, 'blog'), '', '── TOM’S EDU']
    cafe2 = [f'{title} 혼자 푸는 교과서 해석 연습', '', status,
             f'{target} 학생을 위한 본문 학습 자료입니다.', scope,
             '영어를 읽고 빈칸에 우리말 해석을 쓴 뒤 지문 분석지의 해석과 비교해 보세요.',
             '문장별 각주와 S/V 표시를 확인하며 다시 읽을 수 있습니다.',
             '', '▷ 학습법·앞부분 미리보기·자료 위치: '+checked_link(promo, 'blog'), '', '── TOM’S EDU']
    return {'blog':'\n'.join(blog)+'\n', 'cafe1':'\n'.join(cafe1)+'\n', 'cafe2':'\n'.join(cafe2)+'\n'}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('manuscript',type=Path)
    for name in ('blog','cafe1','cafe2'):
        parser.add_argument('--'+name,type=Path)
    args=parser.parse_args()
    paths={k:getattr(args,k) for k in ('blog','cafe1','cafe2') if getattr(args,k)}
    if not paths:
        parser.error('Choose at least one requested output')
    if len({p.resolve() for p in paths.values()})!=len(paths):
        parser.error('Output paths must be distinct')
    if any(p.exists() for p in paths.values()):
        parser.error('Output exists; read and edit the current promotional file instead')
    data=json.loads(args.manuscript.read_text(encoding='utf-8-sig'))
    texts=render(data)
    for name,path in paths.items():
        path.parent.mkdir(parents=True,exist_ok=True)
        with path.open('x',encoding='utf-8',newline='\n') as stream:
            stream.write(texts[name])
    print(json.dumps({'outputs':{k:str(v) for k,v in paths.items()},'published':False},ensure_ascii=False))


if __name__=='__main__':
    main()
