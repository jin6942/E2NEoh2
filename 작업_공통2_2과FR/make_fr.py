"""FR 작성 모듈(fr1)을 모아 공통 원고 JSON을 만들고 검사기를 실행한다(공통영어2 YBM(박준언) 2과 Further Reading)."""
import hashlib
import importlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
# 사용자 선택(2026-09-28 “최신 스킬 + 9/26 승인 4건”) + 동사 없는 문장 종류 추가(“S/V 줄 빼기 + 스킬 사본 보완”).
# 2과 본문과 같은 스킬 사본을 쓴다(2026-09-28, 본문 교재에서 기록한 사용자 결정·예외 포함).
SKILL = ROOT / '작업_공통2_2과' / '스킬수정본' / 'gyogwaseo-unified'
sys.path.insert(0, str(SKILL / 'scripts'))
sys.path.insert(0, str(ROOT / '작업_공통2_2과'))
sys.path.insert(0, str(HERE))

from source_text_fr import build, UNIT_PARAGRAPHS  # noqa: E402
from author import find_word  # noqa: E402

PDF = ROOT / '(2022개정)2025년_공통영어2_YBM(박준언)_2과_본문_(20251205수정).pdf'
OUT = HERE / '공통영어2_YBM(박)_2과FurtherReading_원고.json'
UNIT_MODULES = ['fr1']
GROUPING_NOTE = ('2026-09-28 사용자 선택 “1단위 (추천)”: 소제목 없는 짧은 단락 p01(2문장)·p02(5문장)·p03(2문장)을 '
                 '기아석과 가뭄 경고라는 한 흐름으로 9문장 1단위로 묶음')


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
        'id': 'src', 'label': 'Further Reading', 'text': text, 'sentences': bounds,
        'subheadings': [],
        'provenance': {
            'filename': PDF.name, 'sha256': pdf_hash,
            'location': '원본 PDF 4쪽 Further Reading 왼쪽 단 영어 본문 전체(섹션 표시 Further Reading·제목 Hunger Stones 제외, 오른쪽 단 한국어 해석 제외)',
            'verification_record': ('2026-09-28 pypdfium2 텍스트 추출(4쪽 영어 줄, 제목 제외 1,043자)과 문자 단위 완전 일치. '
                                    '줄바꿈은 공백으로 연결. 곡선 따옴표(“hunger stone”·“If you see me, then cry.”) 원문 유지. '
                                    '단락 3개는 줄 첫 글자 위치(들여쓰기 약 64pt, 기본 약 57pt)로 확인.'),
        },
    }
    T = {b['id']: text[b['start']:b['end']] for b in bounds}
    units, sentences, first_names = [], [], {}
    for name in UNIT_MODULES:
        mod = importlib.import_module(name)
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
        units.append(unit)
    data = {
        'schema_version': 1, 'rule_revision': 'R2026-09-23',
        'metadata': {'book_name': '공통영어2 YBM(박준언) 2과 Further Reading', 'course': '공통영어2',
                     'publisher_author': 'YBM(박준언)', 'lesson': '2과', 'lesson_id': 'UNIT02',
                     'syntax_training_version': 1},
        'cover': {'lesson_label': 'LESSON', 'lesson_number': '02',
                  'lesson_note': 'Further Reading',  # 이전 FR 교재의 사용자 요청과 같은 표지 괄호 표시
                  'topic_first': 'Hunger Stones',
                  'topic_ko': '기아석(헝거 스톤)'},
        'sources': [source],
        'paragraphs': paragraphs,
        'grouping_resolutions': [
            {'source_id': 'src', 'paragraph_ids': pids, 'instruction': f'{GROUPING_NOTE} — {uid}: {pids[0]}~{pids[-1]}'}
            for uid, pids in UNIT_PARAGRAPHS.items()],
        'units': units, 'sentences': sentences,
    }
    if scope == 'full':
        import assessment_fr
        assessment_fr.attach(data)
        data['set_labels'] = {'mock1': '미니 모의고사 1회'}
        # 2026-09-30 사용자 결정(7단계 FABLE F-S01): Word 실제 렌더에서 워크북 정답 ‘5. 핵심 문장 해석’(제목+2줄)만
        # 15쪽으로 넘어가 거의 빈 쪽이 생김 → u1/answers에 첫 단계 spacing 프로필만 적용(spacing_and_type 금지).
        # 근거: Word PDF는 사용자 컴퓨터에만 있어, 사용자 결정 “FABLE 검수 파일로 대신”에 따라
        # 7단계_FABLE_검수.json(Word 렌더 18쪽 기록)의 SHA-256을 evidence_pdf_sha256 자리에 기록한다.
        sys.path.insert(0, str(SKILL / 'scripts'))
        from book_plan import content_hash
        approval = '2026-09-30 사용자 결정: 7단계 FABLE F-S01 워크북 정답에 spacing 프로필 적용(spacing 단계만)'
        data['layout_adjustments'] = [
            {'kind': 'compact_block', 'block_id': 'u1/answers', 'profile': 'spacing',
             'content_sha256': content_hash(data), 'renderer': 'Microsoft Word', 'observed_page': 15,
             'evidence_pdf_sha256': sha(HERE / '검수기록' / '7단계_FABLE_검수.json'),
             'reason': ('Microsoft Word(Microsoft 365) 렌더 18쪽 중 14쪽이 워크북 정답 4번까지 차고 ‘5. 핵심 문장 해석’ 제목+해석 2줄만 '
                        '15쪽으로 넘어가 거의 빈 쪽(7단계 FABLE F-S01·W-NEW-01). 근거 해시는 Word PDF가 아니라 그 렌더를 기록한 '
                        '검수기록/7단계_FABLE_검수.json의 SHA-256(Word PDF는 사용자 컴퓨터 FR_Word확인_임시 폴더에만 있음, 사용자 결정)'),
             'approval_reference': approval}]
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
