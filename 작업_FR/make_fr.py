"""Further Reading 작성 모듈(fr1·fr2)을 모아 공통 원고 JSON을 만들고 검사기를 실행한다."""
import hashlib
import importlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
# 사용자 선택(2026-09-27 “적용”): 앞 교재에서 승인한 조판 변경 4건이 든 스킬 사본을 쓴다.
SKILL = ROOT / '작업' / '스킬수정본' / 'gyogwaseo-unified'
sys.path.insert(0, str(SKILL / 'scripts'))
sys.path.insert(0, str(ROOT / '작업'))
sys.path.insert(0, str(HERE))

from source_text_fr import build, SUBHEADINGS  # noqa: E402
from author import find_word  # noqa: E402

PDF = ROOT / '(2022개정)2026년_영어II_YBM(박준언)_2과_본문.pdf'
OUT = HERE / '영어2_YBM(박)_2과FurtherReading_원고.json'
UNIT_MODULES = ['fr1', 'fr2']


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
            'location': '원본 PDF 5쪽 Further Reading 왼쪽 단 영어 본문 전체(섹션 표시 Further Reading·제목 Happiness Comes From Experiences 제외, 오른쪽 단 한국어 해석·세로 저작권 문구 제외)',
            'verification_record': ('2026-09-27 pypdfium2 텍스트 추출로 5쪽 영어 줄(섹션 표시·제목 포함 1,544자)을 원고와 문자 단위 대조해 완전 일치. '
                                    '줄바꿈은 공백으로 연결. 곡선 아포스트로피(Don’t·it’s·there’s·That’s·we’ve)와 곡선 따옴표 원문 유지. '
                                    '단락 4개는 들여쓰기로 확인. 인용문은 인용 안 마침표 기준으로 문장을 나눔.'),
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
        'metadata': {'book_name': '영어II YBM(박준언) 2과 Further Reading', 'course': '영어II',
                     'publisher_author': 'YBM(박준언)', 'lesson': '2과', 'lesson_id': 'UNIT02',
                     'syntax_training_version': 1},
        'cover': {'lesson_label': 'LESSON', 'lesson_number': '02',
                  'topic_first': 'Happiness Comes From Experiences',
                  'topic_ko': '행복은 경험에서 온다'},
        'sources': [source],
        'paragraphs': [p for p in paragraphs if set(p['sentence_ids']) <= done],
        'grouping_resolutions': [
            {'source_id': 'src', 'paragraph_ids': ['p01', 'p02'],
             'instruction': '2026-09-27 사용자 선택 “2단위 (추천)”: 소제목 없는 단락 p01(5문장)·p02(7문장)를 물건의 행복이 빨리 사라지는 이유로 묶음'},
            {'source_id': 'src', 'paragraph_ids': ['p03', 'p04'],
             'instruction': '2026-09-27 사용자 선택 “2단위 (추천)”: 소제목 없는 짧은 단락 p03(3문장)·p04(5문장)를 경험이 오래가는 행복을 주는 이유로 묶음'},
        ],
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
