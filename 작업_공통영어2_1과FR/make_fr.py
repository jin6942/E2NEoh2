"""Further Reading 작성 모듈(fr1)을 모아 공통 원고 JSON을 만들고 검사기를 실행한다."""
import hashlib
import importlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
# 1과 본문과 같은 스킬 사본(2026-09-28 사용자 선택 “최신+승인 4건 합침”)을 쓴다.
SKILL = ROOT / '작업_공통영어2_1과' / '스킬수정본' / 'gyogwaseo-unified'
sys.path.insert(0, str(SKILL / 'scripts'))
sys.path.insert(0, str(ROOT / '작업_공통영어2_1과'))  # author.py 공용
sys.path.insert(0, str(HERE))

from source_text_fr import build, SUBHEADINGS  # noqa: E402
from author import find_word  # noqa: E402

PDF = ROOT / '(2022개정)2025년_공통영어2_YBM(박준언)_1과_본문_(20250723수정).pdf'
OUT = HERE / '공통영어2_YBM(박)_1과FurtherReading_원고.json'
UNIT_MODULES = ['fr1']


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def resolve_gloss(sentences, sid, head, n=0):
    rows = [g for g in sentences[sid]['glosses'] if g['headword'] == head]
    if len(rows) <= n:
        raise ValueError(f'각주 없음 {sid} {head} #{n}')
    return rows[n]['id']


def source_span(text, piece):
    a, b = find_word(text, piece, 0)
    return [a, b]


def resolve_analysis(a, sentences):
    for gp in a['grammar_points']:
        text = sentences[gp['sentence_id']]['text']
        if isinstance(gp['span'], str):
            gp['span'] = source_span(text, gp['span'])
        pr = gp['practice']
        if isinstance(pr['span'], str):
            pr['span'] = source_span(text, pr['span'])
        if 'support' in pr:
            pr['support_gloss_ids'] = [resolve_gloss(sentences, *x) for x in pr.pop('support')]
        for ov in pr.get('support_overrides', []):
            if isinstance(ov.get('gloss'), tuple):
                ov['gloss_id'] = resolve_gloss(sentences, *ov.pop('gloss'))
            if isinstance(ov.get('source_span'), str):
                ov['source_span'] = source_span(text, ov['source_span'])
        if 'supplemental' in gp and 'function' in gp['supplemental']:
            sid, head, n = gp['supplemental'].pop('function')
            gp['supplemental']['function_gloss_id'] = resolve_gloss(sentences, sid, head, n)
    for r in a['formula_routes']:
        if 'function' in r:
            sid, head, n = r.pop('function')
            fid = resolve_gloss(sentences, sid, head, n)
            key = sentences[sid]['glosses']
            head_row = next(g for g in key if g['id'] == fid)
            r.update(sentence_id=sid, function_gloss_id=fid, formula_key=head_row['headword'])
    order = ['sentence_id', 'function_gloss_id', 'formula_key', 'route']
    a['formula_routes'] = [dict(sorted(r.items(), key=lambda kv: order.index(kv[0]) if kv[0] in order else 9))
                           for r in a['formula_routes']]
    return a


def main(scope='learning'):
    text, bounds, paragraphs = build()
    pdf_hash = sha(PDF)
    first_sentence = {p['id']: p['sentence_ids'][0] for p in paragraphs}
    source = {
        'id': 'src', 'label': 'Further Reading', 'text': text, 'sentences': bounds,
        'subheadings': [{'id': h['id'], 'text': h['text'], 'location': h['location'],
                         'before_sentence_id': first_sentence[h['before']], 'artifact_sha256': pdf_hash}
                        for h in SUBHEADINGS],
        'provenance': {
            'filename': PDF.name, 'sha256': pdf_hash,
            'location': '원본 PDF 4쪽 Further Reading 왼쪽 단 영어 본문 전체(섹션 표시 Further Reading·제목 Breaking Out of the Echo Chamber 제외, 오른쪽 단 한국어 해석·쪽 표시 제외)',
            'verification_record': ('2026-09-29 pypdfium2 텍스트 추출(4쪽 왼쪽 62% 영역, 공백 정규화 1,073자)을 원고와 문자 단위 대조해 완전 일치. '
                                    '줄바꿈은 공백으로 연결. 곡선 따옴표(“ ”)·아포스트로피(’) 원문 유지. 단락 1개(들여쓰기 1곳).'),
        },
    }
    T = {b['id']: text[b['start']:b['end']] for b in bounds}
    units, sentences, first_names = [], [], {}
    for name in UNIT_MODULES:
        try:
            mod = importlib.import_module(name)
        except ModuleNotFoundError:
            continue
        rows = [s.build('src', first_names) for s in mod.sentences(T)]
        sentences.extend(rows)
        by_id = {r['id']: r for r in rows}
        unit = json.loads(json.dumps(mod.UNIT))
        for w in unit['today_words']:
            if not w.get('source_gloss_id'):
                w['source_gloss_id'] = next(g['id'] for r in rows for g in r['glosses']
                                            if g.get('today_word_id') == w['id'])
        unit['analysis'] = resolve_analysis(mod.analysis(None), by_id)
        if hasattr(mod, 'workbook') and scope == 'full':
            unit['workbook'] = mod.workbook()
        if hasattr(mod, 'QUANTITY_EXCEPTIONS'):
            unit['quantity_exceptions'] = mod.QUANTITY_EXCEPTIONS
        units.append(unit)
    done = {s for u in units for s in u['sentence_ids']}
    data = {
        'schema_version': 1, 'rule_revision': 'R2026-09-23',
        'metadata': {'book_name': '공통영어2 YBM(박준언) 1과 Further Reading', 'course': '공통영어2',
                     'publisher_author': 'YBM(박준언)', 'lesson': '1과', 'lesson_id': 'UNIT01',
                     'syntax_training_version': 1},
        'cover': {'lesson_label': 'LESSON', 'lesson_number': '01',
                  'lesson_note': 'Further Reading',  # 2026-09-29 사용자 선택 “넣기 (추천)”: 표지 과 표시 옆 괄호
                  'topic_first': 'Breaking Out of the Echo Chamber',
                  'topic_ko': '에코 챔버에서 벗어나기'},
        'sources': [source],
        'paragraphs': [p for p in paragraphs if set(p['sentence_ids']) <= done],
        'grouping_resolutions': [],
        'units': units, 'sentences': sentences,
    }
    keep = {p['id'] for p in data['paragraphs']}
    if len(keep) < len(paragraphs):
        data['grouping_resolutions'] = [g for g in data['grouping_resolutions'] if set(g['paragraph_ids']) <= keep]
        src = data['sources'][0]
        ids = [s for p in data['paragraphs'] for s in p['sentence_ids']]
        src['sentences'] = [b for b in src['sentences'] if b['id'] in ids]
        src['text'] = src['text'][:src['sentences'][-1]['end']]
        src['subheadings'] = [h for h in src['subheadings'] if h['before_sentence_id'] in ids]
    if scope == 'full':
        import assessment_fr
        assessment_fr.attach(data)
        data['set_labels'] = {'mock1': '미니 모의고사 1회'}
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding='utf-8')
    return data


if __name__ == '__main__':
    scope = sys.argv[1] if len(sys.argv) > 1 else 'learning'
    data = main(scope)
    import check_learning_content as c
    result = c.check(data, scope=scope if scope == 'learning' else 'full')
    print(result['status'], result['unit_count'], result['sentence_count'], result['gloss_count'])
    for k, v in result['sv_lines'].items():
        print(k, v)
