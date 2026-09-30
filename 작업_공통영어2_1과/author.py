"""원고 작성 보조 도구.

사람이 판단해 적은 청크·절·각주·힌트의 '문자열'을 원문에서 찾아 위치(start/end)를
계산해 공통 원고 JSON 형식으로 바꾼다. 문법·뜻은 추측하지 않는다.
찾지 못하거나 모호하면 즉시 오류를 낸다.
"""
import re

WORDS = re.compile(r"[A-Za-z]+(?:['’][A-Za-z]+)*")
ARTICLES = {'a', 'an', 'the'}


def find_word(text, needle, start=0):
    """needle을 낱말 경계에서 찾는다(부분 낱말 일치 금지)."""
    pat = r'(?<![A-Za-z0-9’\'])' + re.escape(needle) + r'(?![A-Za-z0-9])'
    m = re.compile(pat).search(text, start)
    if not m:
        raise ValueError(f'찾을 수 없음: {needle!r} (from {start}) in {text!r}')
    return m.start(), m.end()


def find_in(value, needle):
    """표시 문자열 안의 위치. needle 은 문자열 또는 (문자열, n번째) ."""
    if isinstance(needle, tuple):
        needle, occ = needle
    else:
        occ = 0
    start = -1
    for _ in range(occ + 1):
        start = value.find(needle, start + 1)
        if start < 0:
            raise ValueError(f'표시 문자열에서 찾을 수 없음: {needle!r} in {value!r}')
    return [start, start + len(needle)]


class S:
    def __init__(self, sid, text, key=False):
        self.id, self.text, self.key = sid, text, key
        self.chunks, self.clauses, self.glosses, self.hints = [], [], [], []
        self.nat = None
        self._cursor = 0          # 다음 청크 시작
        self._gpos = -1           # 직전 각주 시작
        self._gid = 0
        self.breaks, self.protected, self.review = [], [], None
        self.relative_ids = []
        self.extra_cov = {}

    # ---------- 청크 ----------
    def ch(self, en, ko):
        t = self.text
        while self._cursor < len(t) and t[self._cursor] == ' ':
            self._cursor += 1
        if not t.startswith(en, self._cursor):
            raise ValueError(f'{self.id}: 청크 불일치 {en!r} at {t[self._cursor:self._cursor+40]!r}')
        self.chunks.append({'start': self._cursor, 'end': self._cursor + len(en), 'ko': ko})
        self._cursor += len(en)
        return self

    def natural(self, ko):
        self.nat = ko
        return self

    # ---------- 절(S/V) ----------
    def cl(self, kind, at, subj=None, verbs=(), marker='', omitted=False, disp=None, disp_review=None,
           occ=0, vfirst=None, readings=None):
        """at: 절 시작 낱말(문자열, occ번째). subj/verbs 는 시작 위치 이후에서 순서대로 찾는다."""
        pos = 0
        for _ in range(occ + 1):
            s0, e0 = find_word(self.text, at, pos)
            pos = s0 + 1
        start = s0
        cur = start
        row = {'kind': kind, 'start': start}
        if marker:
            row['marker'] = marker
        if omitted:
            row['omitted_marker'] = True
        if subj is not None:
            a, b = find_word(self.text, subj, cur)
            row['subject_spans'] = [[a, b]]
            cur = b
            if disp:
                da, db = find_word(self.text, disp, a)
                assert da == a
                row['subject_display_spans'] = [[a, db]]
                row['subject_display_review'] = disp_review
        else:
            row['subject_spans'] = []
            if kind == 'subject_relative':
                cur = find_word(self.text, marker, start)[1] if marker else start
        vs = []
        if vfirst:
            vcur = start
            for v in vfirst:
                a, b = find_word(self.text, v, vcur)
                vs.append([a, b])
                vcur = b
        for v in verbs:
            a, b = find_word(self.text, v, cur)
            vs.append([a, b])
            cur = b
        row['verb_spans'] = vs
        if readings:
            row['contraction_readings'] = readings
        self.clauses.append(row)
        return self

    # ---------- 각주 ----------
    def g(self, surface, headword, meaning, *, same=False, at=None, star=None, gid=None, **extra):
        """surface: 원문 조각. 불연속이면 '|'로 구분. same=True 면 직전 각주와 같은 시작 위치."""
        pieces = surface.split('|')
        if at is not None:
            base = at
        elif same:
            base = self._gpos
        else:
            base = self._gpos + 1
        spans = []
        cur = base
        for i, piece in enumerate(pieces):
            a, b = find_word(self.text, piece, cur)
            if i == 0 and same and a != self._gpos:
                raise ValueError(f'{self.id}: same 위치 불일치 {surface}')
            spans.append([a, b])
            cur = b
        self._gid += 1
        row = {'id': gid or f'{self.id}-g{self._gid:02d}', 'spans': spans, 'headword': headword,
               'meaning_ko': meaning, 'star': False}
        if star:
            row['star'] = True
            row['today_word_id'] = star
        if 'verb_construction' in extra and 'kind' not in extra:
            row['kind'] = 'lexical'
        row.update(extra)
        self._gpos = spans[0][0]
        self.glosses.append(row)
        return row

    def span_of(self, piece, after=0):
        return list(find_word(self.text, piece, after))

    # ---------- 힌트 ----------
    def hint(self, en, ko, *, span, label=None, links=(), refs=(), explanation, meaning, **extra):
        """span: 원문 조각 문자열 또는 (문자열, 시작검색위치). links: [(en_needles, ko_needles)]"""
        if isinstance(span, tuple):
            a, b = find_word(self.text, span[0], span[1])
        else:
            a, b = find_word(self.text, span, 0)
        pair = {'en': en, 'ko': ko}
        if refs:
            pr = []
            for en_p, ko_p, ko_ref in refs:
                ea = find_in(en, en_p)
                ka = find_in(ko, ko_p + ko_ref if isinstance(ko_p, str) else (ko_p[0] + ko_ref, ko_p[1]))
                kp = [ka[0], ka[0] + len(ko_p if isinstance(ko_p, str) else ko_p[0])]
                pr.append({'en_span': ea, 'ko_pronoun_span': kp, 'ko_reference_span': [kp[1], ka[1]]})
            pair['pronoun_refs'] = pr
        pair['emphasis_links'] = [{'en_spans': sorted(find_in(en, x) for x in e),
                                   'ko_spans': sorted(find_in(ko, x) for x in k)} for e, k in links]
        if 'emphasis_note' in extra:
            pair['emphasis_note'] = extra.pop('emphasis_note')
        row = {'span': [a, b], 'meaning_ko': meaning, 'explanation': explanation, 'display_pairs': [pair]}
        if label:
            row['structure_label'] = label
        row.update(extra)
        self.hints.append(row)
        return row

    def vf_hint(self, *, fn, lex, en, ko, formula, step_form, step_ko, en_mark, ko_mark, span, explanation, meaning):
        """수동·능동 완료 기능 결합 한 줄 힌트."""
        a, b = find_word(self.text, span, 0)
        da, db = find_word(self.text, en, 0)
        pair = {'en': en, 'ko': ko, 'emphasis_links': [{'en_spans': sorted(find_in(en, x) for x in en_mark),
                                                         'ko_spans': sorted(find_in(ko, x) for x in ko_mark)}]}
        row = {'category': 'function-combination', 'span': [a, b], 'gloss_ids': [fn['id'], lex['id']],
               'meaning_ko': meaning, 'explanation': explanation, 'display_mode': 'verb-function',
               'display_span': [da, db], 'formula_label': formula,
               'lexical_step': {'gloss_id': lex['id'], 'form': step_form, 'meaning_ko': step_ko},
               'display_pairs': [pair]}
        self.hints.append(row)
        return row

    # ---------- 읽기 검토 ----------
    def brk(self, piece, kind, reason, after=0):
        a, _ = find_word(self.text, piece, after)
        self.breaks.append({'at': a, 'kind': kind, 'reason': reason})

    def prot(self, piece, kind, reason, gloss=None, after=0):
        pieces = piece
        a, b = find_word(self.text, pieces, after)
        row = {'span': [a, b], 'kind': kind, 'reason': reason}
        if gloss is not None:
            row['gloss_id'] = gloss['id']
        self.protected.append(row)

    # ---------- 출력 ----------
    def build(self, source_id, first_names):
        """first_names: 고유명사 첫 각주 {소문자 이름: gloss_id} (지문 공통, 갱신됨)."""
        if self.nat is None:
            raise ValueError(f'{self.id}: 자연 해석 누락')
        joined = ''.join(self.text[c['start']:c['end']] + ' ' for c in self.chunks).strip()
        if joined != self.text:
            raise ValueError(f'{self.id}: 청크가 원문을 모두 덮지 않음')
        coverage = []
        lexical_targets = {}
        for g in self.glosses:
            for t in g.get('combines_with', []):
                lexical_targets[t] = True
        for m in WORDS.finditer(self.text):
            a, b = m.span()
            covering = [g for g in self.glosses if any(x <= a and b <= y for x, y in g['spans'])]
            linked = [g for g in covering if g['id'] in lexical_targets]
            word = m.group()
            if linked:
                coverage.append({'span': [a, b], 'gloss_id': linked[0]['id']})
            elif covering:
                coverage.append({'span': [a, b], 'gloss_id': covering[0]['id']})
            elif word.lower() in ARTICLES:
                coverage.append({'span': [a, b], 'exemption': 'below-middle1-unneeded', 'level': 'below-middle1',
                                 'reason': '관사: 초등 기초어로 문맥상 별도 뜻 지원 불필요'})
            elif word.lower() in {'and', 'but'}:
                coverage.append({'span': [a, b], 'exemption': 'standalone-and-but',
                                 'reason': '일반 연결 and/but 단독 각주 제외'})
            elif word.lower() == 'you':
                coverage.append({'span': [a, b], 'exemption': 'standalone-you',
                                 'reason': '단독 you 각주 제외(사용자 지정)'})
            elif word in first_names:
                coverage.append({'span': [a, b], 'exemption': 'proper-name-repeat',
                                 'first_gloss_id': first_names[word],
                                 'reason': '같은 지문에서 먼저 제공한 고유명사 반복'})
            elif (a, b) in self.extra_cov:
                coverage.append({'span': [a, b], **self.extra_cov[(a, b)]})
            else:
                raise ValueError(f'{self.id}: 각주 누락 낱말 {word!r} at {a}')
        for g in self.glosses:
            if g.get('proper'):
                for x, y in g['spans']:
                    for w in WORDS.finditer(self.text[x:y]):
                        if w.group()[0].isupper():
                            first_names.setdefault(w.group(), g['id'])
        glosses = []
        for g in self.glosses:
            g = dict(g)
            g.pop('proper', None)
            glosses.append(g)
        return {
            'source_id': source_id, 'id': self.id, 'text': self.text, 'key': self.key,
            'chunks': self.chunks, 'natural_ko': self.nat, 'clauses': self.clauses,
            'glosses': glosses, 'lexical_coverage': coverage, 'hints': self.hints,
            'reading_checks': {
                'review_record': self.review or '검토 기록 누락',
                'required_breaks': self.breaks, 'protected_spans': self.protected,
                'function_gloss_ids': [g['id'] for g in self.glosses if g.get('kind') == 'function'],
                'relative_gloss_ids': self.relative_ids,
            },
        }


def fn(s, surface, headword, meaning, lex_rows, **extra):
    """기능 각주(kind:function) — lex_rows 는 뒤에 만들 낱말 각주를 나중에 연결하기 위해 list 로 받음."""
    row = s.g(surface, headword, meaning, kind='function', combines_with=[], **extra)
    return row


def link(function_row, *lexical_rows):
    for r in lexical_rows:
        r['kind'] = 'lexical'
        function_row['combines_with'].append(r['id'])
