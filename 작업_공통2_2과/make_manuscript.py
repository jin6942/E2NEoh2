"""작성 모듈(u1~u5)을 모아 공통 원고 JSON을 만들고 검사기를 실행한다(공통영어2 YBM(박준언) 2과)."""
import hashlib
import importlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
# 사용자 선택(2026-09-28 “최신 스킬 + 9/26 승인 4건”) + 동사 없는 문장 종류 추가(“S/V 줄 빼기 + 스킬 사본 보완”).
SKILL = HERE / '스킬수정본' / 'gyogwaseo-unified'
sys.path.insert(0, str(SKILL / 'scripts'))
sys.path.insert(0, str(HERE))

from source_text import build, UNIT_PARAGRAPHS  # noqa: E402
from author import find_word  # noqa: E402

PDF = ROOT / '(2022개정)2025년_공통영어2_YBM(박준언)_2과_본문_(20251205수정).pdf'
OUT = HERE / '공통영어2_YBM(박)_UNIT02_원고.json'
UNIT_MODULES = ['u1', 'u2', 'u3', 'u4', 'u5']
GROUPING_NOTE = ('2026-09-28 사용자 선택 “5단위, 작품 소개 합침”: 소제목 없는 소설 본문(1~3문장짜리 짧은 단락뿐)을 '
                 '장면 기준 17·19·10·15·13문장 5단위로 묶고, 마지막 장면(p26~p31)과 별표 작품 소개 단락 p32를 한 단위로 합침')


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
    source = {
        'id': 'src', 'label': '교과서 본문', 'text': text, 'sentences': bounds,
        'subheadings': [],
        'provenance': {
            'filename': PDF.name, 'sha256': pdf_hash,
            'location': '원본 PDF 1~3쪽 왼쪽 단 영어 본문 전체(제목 Dry, 오른쪽 단 한국어 해석, 4쪽 Further Reading 제외)',
            'verification_record': ('2026-09-28 pypdfium2 텍스트 추출(1~3쪽 영어 줄, 제목 제외 4,143자)과 문자 단위 완전 일치. '
                                    '줄바꿈은 공백으로 연결. 곡선 따옴표·아포스트로피·줄표(—)·p32 첫 글자 *는 원문 유지. '
                                    '단락 32개는 1~3쪽 페이지 이미지의 들여쓰기로 확인. 직접 인용 안의 마침표·물음표에서 문장을 나눔.'),
        },
    }
    T = {b['id']: text[b['start']:b['end']] for b in bounds}
    units, sentences, first_names = [], [], {}
    for name in UNIT_MODULES:
        try:
            mod = importlib.import_module(name)
        except ModuleNotFoundError:
            continue
        built = mod.sentences(T)
        rows = []
        for s in built:
            rows.append(s.build('src', first_names))
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
        'metadata': {'book_name': '공통영어2 YBM(박준언) 2과', 'course': '공통영어2',
                     'publisher_author': 'YBM(박준언)', 'lesson': '2과', 'lesson_id': 'UNIT02',
                     'syntax_training_version': 1},
        'cover': {'lesson_label': 'LESSON', 'lesson_number': '02',
                  'topic_first': 'Dry',
                  'topic_ko': '드라이 (소설 『Dry』의 도입부)'},
        'sources': [source],
        'paragraphs': [p for p in paragraphs if set(p['sentence_ids']) <= done],
        'grouping_resolutions': [
            {'source_id': 'src', 'paragraph_ids': pids,
             'instruction': f'{GROUPING_NOTE} — {uid}: {pids[0]}~{pids[-1]}'}
            for uid, pids in UNIT_PARAGRAPHS.items()],
        'units': units, 'sentences': sentences,
    }
    keep = {p['id'] for p in data['paragraphs']}
    if len(keep) < len(paragraphs):
        data['grouping_resolutions'] = [g for g in data['grouping_resolutions'] if set(g['paragraph_ids']) <= keep]
        src = data['sources'][0]
        ids = [s for p in data['paragraphs'] for s in p['sentence_ids']]
        src['sentences'] = [b for b in src['sentences'] if b['id'] in ids]
        src['text'] = src['text'][:src['sentences'][-1]['end']]
    if scope == 'full':
        import assessment_data
        assessment_data.attach(data)
        data['set_labels'] = {f'mock{n}': f'미니 모의고사 {n}회' for n in (1, 2, 3)}
        # 2026-09-28 사용자 결정 “간격 줄이기 조판 쓰기 — LibreOffice 기준으로 적용”:
        # Word가 없는 환경이라 LibreOffice 예비 렌더(66쪽)에서 넘친 두 분석 설명부에만
        # 첫 단계 spacing 프로필을 적용한다(글자 크기 유지).
        sys.path.insert(0, str(SKILL / 'scripts'))
        from book_plan import content_hash
        rev = content_hash(data)
        evidence = '432edb359b4de74bf77fa8059fd8ffcc2cf8e37949e79a0cac2422744658f9ff'
        approval = '2026-09-28 사용자 결정: 간격 줄이기 조판 적용(LibreOffice 기준으로 적용)'
        data['layout_adjustments'] = [
            {'kind': 'compact_block', 'block_id': uid, 'profile': 'spacing', 'content_sha256': rev,
             'renderer': 'LibreOffice', 'renderer_exception_approval': approval,
             'observed_page': page, 'evidence_pdf_sha256': evidence, 'reason': reason,
             'approval_reference': approval}
            for uid, page, reason in [
                ('u1/analysis', 9, '문단 1 분석 설명부의 필수 유의어/반의어 마지막 1줄(essentials)만 9쪽으로 넘어가 9쪽이 거의 빈 쪽(J-W01)'),
                ('u3/analysis', 27, '문단 3 분석 설명부의 필수 유의어/반의어 제목과 3줄이 27쪽으로 넘어가 27쪽 대부분이 빈 쪽(J-W02)')]]
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
