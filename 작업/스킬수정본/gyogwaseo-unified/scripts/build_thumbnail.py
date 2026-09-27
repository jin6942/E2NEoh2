#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_thumbnail.py — 끊어읽기 해석지 블로그/카페 게시용 썸네일 PNG (1200x1200)

사용법:
    python3 build_thumbnail.py <data.json> <출력.png>

data.json 은 해석지 빌더가 쓰는 파일과 같은 것을 그대로 넣는다.
본문 문장 하나를 골라 끊어읽기(/) 표시와 각주(※)를 실제로 보여 준다.
외부 프로그램 없이 Pillow(PIL)로 직접 그린다.
"""
import json, re, sys, pathlib

from PIL import Image, ImageDraw, ImageFont

W = H = 1200
CREAM = (253, 251, 244)
RULE = (241, 234, 218)
RED = (232, 73, 47)
INK = (23, 23, 26)
GRAY = (122, 115, 106)
GLOSS_C = (107, 100, 89)
BLANK_C = (201, 191, 168)
HAND_C = (167, 156, 134)
PAD = 84

FONT_DIR = pathlib.Path('/usr/share/fonts/opentype/noto')
KR = 1

MAX_GLOSS = 7          # 각주 최대 개수

# 썸네일에 쓸 문장의 최소 조건 — "앞에서부터, 이 조건을 넘는 첫 문장"
MIN_CHUNKS = 2         # 끊어읽기 / 가 최소 한 번은 보여야 자료 성격이 드러난다
MIN_GLOSS = 3          # 각주가 너무 적으면 썸네일이 헐거워진다
SENT_MIN, SENT_MAX = 34, 150   # 글자 수 범위(3줄 안에 들어가는 상한)


def font(weight, size):
    return ImageFont.truetype(str(FONT_DIR / f'NotoSansCJK-{weight}.ttc'), size, index=KR)


def w_of(d, text, f):
    return d.textbbox((0, 0), text, font=f)[2]


def fit(d, text, weight, size, max_w, min_size=22):
    while size > min_size:
        f = font(weight, size)
        if w_of(d, text, f) <= max_w:
            return f
        size -= 2
    return font(weight, min_size)


def draw_runs(d, x, y, runs, max_w, line_h, max_lines=None):
    """runs = [(글자, 폰트, 색), ...] 를 max_w 안에서 줄바꿈하며 그린다. 그린 줄 수를 돌려준다."""
    cx, cy, lines = x, y, 1
    for text, f, color in runs:
        for i, word in enumerate(re.split(r'(\s+)', text)):
            if not word:
                continue
            ww = w_of(d, word, f)
            if cx + ww > x + max_w and word.strip():
                if max_lines and lines >= max_lines:
                    return lines
                cx, cy, lines = x, cy + line_h, lines + 1
            if not word.strip() and cx == x:
                continue
            d.text((cx, cy), word, font=f, fill=color)
            cx += ww
    return lines


def badge(d, x, y, text, f, bg, fg, padx=24, pady=12):
    """알약 모양 라벨을 그리고 (너비, 높이) 를 돌려준다."""
    tw = w_of(d, text, f)
    h = f.size + pady * 2
    d.rounded_rectangle([x, y, x + tw + padx * 2, y + h], radius=9, fill=bg)
    d.text((x + padx, y + pady - 2), text, font=f, fill=fg)
    return tw + padx * 2, h


def parse_meta(data):
    """'공통영어2 YBM(박준언) 1과 · 끊어읽기 혼공 해석지' → 교과서 / 출판사 / 과"""
    t = (data.get('title') or '').split('·')[0].strip()
    m = re.match(r'^(\S+)\s+(.+?)\s+(\S*\d+\s*과)\b', t)
    if m:
        return m.group(1), m.group(2).strip(), m.group(3).replace(' ', '')
    return t, '', ''


def clean(s):
    return re.sub(r'\s*★핵심\s*$', '', str(s)).strip()


def pick_sentence(data):
    """**본문 앞에서부터** 보아, 최소 조건을 넘는 **첫 문장**을 쓴다 (사용자 확정).

    점수를 매겨 '제일 좋은 문장'을 고르지 않는다 — 지문 앞쪽이 도입부라 썸네일에서
    자연스럽게 이어 읽히고, 어느 자료든 같은 방식으로 뽑혀 결과를 미리 알 수 있다.
    다만 맨 첫 문장이 `My name is Lee Saem.` 처럼 **끊어읽기 조각도 각주도 거의 없는**
    문장이면 썸네일이 헐거워져 자료의 성격이 드러나지 않는다. 그래서 조각·각주·길이의
    최소선을 넘는 첫 문장까지만 내려가서 고른다(보통 1~3번째 문장에서 걸린다).

    순서대로 완화하며 찾는다:
      1) 조각 MIN_CHUNKS+ · 각주 MIN_GLOSS+ · 길이 SENT_MIN~SENT_MAX
      2) 조각 MIN_CHUNKS+ (길이·각주 조건 없이)
      3) chunks가 있는 아무 문장
    """
    sents = [se for sec in data.get('sections', []) for se in sec.get('sentences', [])
             if [clean(c) for c in se.get('chunks', []) if clean(c)]]

    def ok(se, strict):
        chunks = [clean(c) for c in se.get('chunks', []) if clean(c)]
        if len(chunks) < MIN_CHUNKS:
            return False
        if not strict:
            return True
        n = len(' / '.join(chunks))
        return len(se.get('gloss', []) or []) >= MIN_GLOSS and SENT_MIN <= n <= SENT_MAX

    for strict in (True, False):
        for se in sents:
            if ok(se, strict):
                return se
    return sents[0] if sents else None


def stats(data):
    secs = data.get('sections', [])
    n = sum(len(s.get('sentences', [])) for s in secs)
    g = sum(len(se.get('gloss', []) or []) for s in secs for se in s.get('sentences', []))
    return n, g


def main():
    if len(sys.argv) < 3:
        sys.exit('사용법: python3 build_thumbnail.py <data.json> <출력.png>')
    data = json.load(open(sys.argv[1], encoding='utf-8'))
    out = pathlib.Path(sys.argv[2])

    book, pub, lesson = parse_meta(data)
    n_sent, n_gloss = stats(data)
    sent = pick_sentence(data)

    im = Image.new('RGB', (W, H), CREAM)
    d = ImageDraw.Draw(im)

    # 노트 줄 + 상단 빨간 띠
    for y in range(44, H, 76):
        d.rectangle([0, y, W, y + 1], fill=RULE)
    d.rectangle([0, 0, W, 21], fill=RED)

    y = 66
    _, bh = badge(d, PAD, y, '내신 3등급용', font('Bold', 28), INK, CREAM)
    y += bh + 26

    fk = font('Black', 64)
    d.text((PAD, y), '끊어읽기 혼공 해석지', font=fk, fill=RED)
    y += fk.size + 30

    head = f'{book} {lesson}'.strip()
    fh = fit(d, head, 'Black', 52, W - PAD * 2)
    d.text((PAD, y), head, font=fh, fill=INK)
    y += fh.size + 28

    if pub:
        d.text((PAD, y), pub, font=fit(d, pub, 'Regular', 38, W - PAD * 2), fill=GRAY)
    y += 84

    # 문장 (끊어읽기 / 는 빨강)
    if sent:
        chunks = [clean(c) for c in sent.get('chunks', []) if clean(c)]
        fs = font('Bold', 44)
        runs = []
        for i, c in enumerate(chunks):
            if i:
                runs.append(('/ ', font('Black', 44), RED))
            runs.append((c + ' ', fs, INK))
        used = draw_runs(d, PAD, y, runs, W - PAD * 2, 66, max_lines=3)
        y += used * 66 + 18

        # 각주 — **문장에 나온 순서 그대로** 싣는다 (사용자 확정).
        #   ★를 앞으로 끌어와 정렬하면 썸네일의 각주 순서와 문장의 단어 순서가 어긋나
        #   학생이 "그 단어가 어디 있는지" 짚어 가며 읽을 수 없다. 그래서 순서를 바꾸지 않는다.
        #   MAX_GLOSS 개를 넘어 잘라낼 때만 ★ 항목을 우선 남기고, 남긴 것들은 다시 원래 순서로 배열한다.
        gl = list(sent.get('gloss', []) or [])
        if len(gl) > MAX_GLOSS:
            keep = [i for i, g in enumerate(gl) if len(g) > 2 and g[2]][:MAX_GLOSS]
            for i in range(len(gl)):                       # ★로 다 못 채우면 앞에서부터 보충
                if len(keep) >= MAX_GLOSS:
                    break
                if i not in keep:
                    keep.append(i)
            gl = [gl[i] for i in sorted(keep)]              # 원문 등장 순서 복원
        if gl:
            fg, fgb, fgs = font('Regular', 30), font('Bold', 30), font('Black', 30)
            runs = [('※ ', fg, GLOSS_C)]
            for i, g in enumerate(gl):
                if i:
                    runs.append((' · ', fg, BLANK_C))
                if len(g) > 2 and g[2]:
                    runs.append(('★', fgs, RED))
                    runs.append((str(g[0]), fgb, INK))
                else:
                    runs.append((str(g[0]), fg, GLOSS_C))
                runs.append((f' — {g[1]}', fg, GLOSS_C))
            used = draw_runs(d, PAD, y, runs, W - PAD * 2, 50, max_lines=3)
            y += used * 50 + 26

    # 해석 쓰는 빈 줄 2개
    for wfrac in (1.0, 0.66):
        y += 70
        d.rectangle([PAD, y, PAD + int((W - PAD * 2) * wfrac), y + 3], fill=BLANK_C)
    y += 44
    d.text((PAD, y), '↑ 사전 없이 바로 해석해 보기', font=font('Medium', 32), fill=HAND_C)

    # 로고 + 수치
    logo_p = pathlib.Path(__file__).resolve().parent.parent / 'assets' / 'logo-horizontal.png'
    if logo_p.is_file():
        lg = Image.open(logo_p).convert('RGBA')
        lh = 64
        lg = lg.resize((int(lg.width * lh / lg.height), lh), Image.LANCZOS)
        im.paste(lg, (PAD, H - 74 - lh), lg)

    fc = font('Black', 52)
    txt = f'{n_sent}문장'
    d.text((W - PAD - w_of(d, txt, fc), H - 74 - 62), txt, font=fc, fill=RED)
    fsub = font('Regular', 28)
    sub = f'단어 풀이 {n_gloss}개 · 분석지 해석 수록'
    d.text((W - PAD - w_of(d, sub, fsub), H - 74 - 4), sub, font=fsub, fill=(140, 133, 120))

    out.parent.mkdir(parents=True, exist_ok=True)
    im.save(out, optimize=True)
    print(f'thumbnail: {out}  ({book} {lesson} / {n_sent}문장 · 각주 {n_gloss})')


if __name__ == '__main__':
    main()
