# 승인된 학습 단위 병합과 명사구 답변

사용자의 명시적 결정에 한정한 입력·출력 지원이다. 원문·단락 경계·문장 ID·순서·offset은 보존한다. 승인 기록을 데이터에 적었다는 사실만으로 사용자 승인이나 독립 검수가 자동 증명되는 것은 아니다.

## 영어2 YBM(박준언) 1과의 현재 승인

2022개정·2026년 자료의 PDF 1~4쪽 본문 13단락·70문장에 적용한다. Further Reading은 제외한다.

- `UNIT01-본문`의 H03(The Messages of Hip-Hop), P10·P11 각 8문장을 16문장인 `UNIT01-P04`로 묶는다.
- 전체 학습 단위는 `18·19·11·16·6`이다. P12·P13은 `UNIT01-P05`, P01~P03 도입부 묶음은 유지한다.
- 사용자 결정 `USER-20260928-H03-SIXTEEN-SENTENCE-SINGLE-UNIT`은 종전 6단위 결정을 대체한다. 옛 S-v1 정정과 S-v2의 당시 판정은 지우거나 현재 PASS로 바꾸지 않는다.
- P04S04는 앞 질문 P04S03에 대한 명사구 답변이다. `called`, `based`를 유한동사로 표시하지 않으며 원문에 주어·동사를 보충하지 않는다. S/V 줄과 ‘명사구 답변’ 같은 대체 안내문을 모두 생략한다.

## 병합 예외 입력

공통 원고의 `grouping_resolutions`에 다음 레코드를 기존 도입부 확인 기록과 함께 둔다. 별도 근거 파일만 두고 이 입력을 생략하면 일반 규칙의 6단위 결과가 나온다.

```json
{
  "kind": "approved-merge",
  "source_id": "UNIT01-본문",
  "subheading_id": "H03",
  "paragraph_ids": ["P10", "P11"],
  "sentence_ids": [
    "P10S01", "P10S02", "P10S03", "P10S04", "P10S05", "P10S06", "P10S07", "P10S08",
    "P11S01", "P11S02", "P11S03", "P11S04", "P11S05", "P11S06", "P11S07", "P11S08"
  ],
  "paragraph_sentence_counts": {"P10": 8, "P11": 8},
  "approved_by": "user",
  "approval_id": "USER-20260928-H03-SIXTEEN-SENTENCE-SINGLE-UNIT",
  "instruction": "이거 그냥 원래대로 16문장을 한단위로 만들어"
}
```

단락은 같은 독립 본문·같은 실제 소제목에 속하고 원문 순서대로 연속해야 한다. 정확한 문장 목록과 단락별 수량을 현재 입력과 대조한다. 중복·겹침·다른 소제목이나 본문 횡단·일부 문장 누락은 허용하지 않는다. 짧은 단락 때문에 소제목 전체가 자동으로 묶이는 경우 그 전체를 부분 예외로 쪼개지 않는다. 예외 없는 다른 소제목과 다른 교재의 기본 규칙은 그대로다.

소제목 없는 짧은 단락의 기존 `source_id`, `paragraph_ids`, `instruction` 기록은 유지한다. 일반 원문 확인 기록을 `approved-merge`로 자동 변환하지 않는다. CLI 입력은 `grouping_resolutions`를 사용하며 구형 `resolutions`와 상충하는 값을 동시에 주지 않는다.

## 명사구 답변 입력과 출력

해당 `sentences[]` 항목의 `clauses`는 명시적으로 빈 배열이며 다음 `sv_review`를 함께 기록한다. SHA-256은 각 문장 원문 문자열 자체를 UTF-8로 인코딩한 바이트의 값이며 파일 전체 해시가 아니다.

```json
{
  "clauses": [],
  "sv_review": {
    "kind": "noun-phrase-answer",
    "reviewed": true,
    "reason": "P04S03의 질문에 대한 명사구 답변이다. called와 based는 수식 분사이며 이 답변에는 유한동사가 없다.",
    "source_text_sha256": "6a631334479fd209a3b9c2f4489bfd7b86adfd9d0c92ef6a834a312aa24ba827",
    "context_sentence_id": "P04S03",
    "context_text_sha256": "6a2fce9265bc5517b1dd616db2978eddc22189a25fe57d77113738f1e3325c2f"
  }
}
```

질문: `What eventually emerged from these parties?`

답변: `A vibrant youth movement called hip-hop culture, based on DJing, breakdancing, MCing, and graffiti.`

`sv_line.render_sv(original, clauses, sv_review)`는 검토 기록·답변 지문을 확인하고 빈 문자열을 반환한다. 단독 렌더러는 외부 질문 원문을 갖고 있지 않으므로 공통 `check_learning_content.py`가 같은 본문의 바로 앞 질문 ID와 원문 지문까지 대조한다. 질문 관계와 유한동사 부재의 문법 판정은 실제 검토 근거로 남긴다.

검토 기록 없는 빈 clauses, 불명확한 검토 상태, 비어 있는 이유, 다른 원문 지문, 잘못된 질문 연결, 비어 있지 않은 clauses와의 모순은 계속 오류다. 일반 문장의 S/V 표시는 유지한다. `book_plan.py`는 해당 S/V 문단 자체를 만들지 않고 `export_handoff.py`는 `[S/V]` 행을 내보내지 않는다. 영어 본문·해석·각주·필요한 구조 힌트는 보존한다.

## 적용과 검수 기록

기존 동결 패킷을 덮어쓰지 않고 최신 5단위 원고의 새 버전에 위 입력을 추가한다. 별도 예외 근거 파일·사용자 결정·새 패키지 지문·원고 파일 해시를 함께 연결한다. 배포 자료의 실제 대상 입력 예제를 사용하되 다른 교재로 해당 ID·지문·승인을 복사하지 않는다.

`4fcd6a2f…`판은 이 승인 예외와 명사구 계약을 지원하지 않는다. 그 버전의 일반 검사 결과를 현재 계약의 통과로 취급하지 않는다. 새 버전으로 필요한 구조·출력 연결을 확인하고, 실제 교재의 독립 검수와 DOCX 조판·출고는 해당 현재 파일의 증거로 따로 기록한다. 과거 PASS의 패키지 지문만 새 값으로 치환하지 않는다.

## 공통영어2 YBM(박준언) 2과의 동사 없는 짧은 문장 (이 스킬 사본에만 추가)

2026-09-28 사용자 결정 “S/V 줄 빼기 + 스킬 사본 보완”, “50번 V만, 52번 전달절만”. 대상은 이 교재의 원문 s17 `The essentials of life.`, s25 `Lucky!`, s53 `“Not a problem.`, s69 `“Not at all.”`이다.

- 유한동사가 없는 이 네 문장은 위 명사구 답변과 같은 방식으로 S/V 줄과 대체 안내문을 모두 생략한다. `clauses:[]`와 `sv_review`를 두되 `kind:"verbless-fragment"`로 기록하고, 이유에 실제 성격(앞 문장 보충 명사구·감탄·대답)을 적는다. 문맥 연결 필드는 기존 계약대로 바로 앞 같은 본문 문장의 ID·SHA-256을 쓴다. s69처럼 실제 질문이 더 앞(s66)에 있으면 그 사실을 이유에 적는다.
- `sv_line.py`는 `noun-phrase-answer`와 `verbless-fragment` 두 종류만 받는다. 검토 기록 없는 빈 clauses는 계속 오류다. 다른 교재나 다른 문장으로 이 종류를 자동 확대하지 않는다.
- 주어가 생략된 구어 s50 `“Looks like you could use some help.”`는 명령문과 같은 표시 방식(주어 칸 없이 V만)으로 `V: Looks ／ [like] S′: you, V′: could use`를 출력한다. 생략된 It을 보충하지 않으며, 절 종류는 표시 장치상 `imperative`로 기록하되 `reading_checks.review_record`에 ‘주어 It 생략 구어, 명령문 아님’을 적는다. s52의 인사 관용 표현 Thank you는 S/V에서 제외하고 전달절 `S: I, V: tell`만 표시한다.

### 같은 교재의 L 독립 검수 뒤 추가 결정 (2026-09-28, 이 스킬 사본에만 추가)

- **then으로 이어진 병렬 동사:** s35 `She looks back …, then turns back …`, s70 `The man looks at …, then leaves.`는 and 없이 부사 then이 한 주어의 두 동사를 잇는다. 이 두 문장에 한해 V 칸에 then을 남겨 `V: looks then turns`, `V: looks then leaves`로 표시한다. then을 빼면 `looks turns`처럼 한 동사구로 보이기 때문이다. 다른 부사나 다른 교재로 확대하지 않는다.
- **연결동사의 최소 보어:** 절 연결 힌트에서 be동사에만 허용하던 ‘뜻을 잡는 최소 보어’ 예외를 이 교재의 연결동사 get·become에도 적용한다. 대상은 s07 `[ever since people got tired]`, s36 `[before it becomes a deep flush]`, s74 `[this story can become a reality]`이다(사용자 결정은 ‘연결동사의 보어까지 표시’라는 일반 질문에 대한 답이었고 질문 예시가 s07·s36이었다. s74는 L-재검에서 같은 구조로 확인되어 같은 결정을 적용했으며, 사용자에게 적용 사실을 보고함). 보어를 빼면 ‘사람들이 된 이후로’처럼 뜻이 사라진다.
- **그대로 두기로 한 항목:** 인명 각주는 교과서 해석처럼 영어 이름을 유지한다(`Alyssa — Alyssa (…)`). s72 `who has to make`의 S/V는 s54 need to와 같은 방식으로 `V′: has`를 유지하고, 분석 설명만 이에 맞춘다.

### 출고 뒤 조판 결정 (2026-09-28, 이 스킬 사본에만 추가)

- **LibreOffice 근거 간격 줄이기:** 사용자 결정 “간격 줄이기 조판 쓰기 — LibreOffice 기준으로 적용”. Word가 없는 환경이라 LibreOffice 예비 렌더(SHA256 432edb35…)에서 넘친 u1/analysis(9쪽)·u3/analysis(27쪽)에만 첫 단계 `spacing` 프로필을 적용했다. `layout_adjustments`에 `renderer:"LibreOffice"`와 `renderer_exception_approval`을 함께 기록하며, `scripts/compact_layout.py`는 이 승인 기록이 있을 때만 LibreOffice 관찰을 받는다. 승인 기록 없는 LibreOffice·다른 렌더러는 계속 거부한다. Word 렌더에서 원래 넘치지 않았다면 불필요한 축소일 수 있으므로 Word 확인 뒤 되돌릴 수 있다.
- **★핵심 위치:** LibreOffice가 표식 안 U+FEFF를 줄바꿈 방지로 쓰지 않아 ‘★핵 / 심’으로 갈리는 현상(7쪽)이 있었다. U+2060·U+200D·U+202F·NBSP·언어 지정·`w:wordWrap`을 시험했으나 LibreOffice에서는 모두 갈렸다. 사용자 결정 “이전 규칙 유지, Word 확인”에 따라 문장 끝 위치와 기존 표식 문자를 유지하고 Word에서 확인한다.

## 공통영어2 YBM(박준언) 2과 Further Reading의 수동 p.p. + 보충 to V 각주 (2026-09-29, 이 스킬 사본에만 추가)

- **대상:** s07 `The words … are believed to warn of these hardships and to urge people to be prepared.` 독립 L 검수(L-05)에서 보충 to V를 따로 떼어 `to V — ~하는 것으로`라고 적은 것이 ‘동사 보충 to V는 구문으로 묶는다’는 규칙에 어긋난다고 지적했다. 수동 동사 뒤 보충 to V(be believed/said/thought to V)의 표기는 기존 규칙에 없었다.
- **사용자 결정 “p.p.에 to V 결합”:** 수동 분리는 유지하고 보충 to V만 p.p. 쪽 각주에 묶는다. `be p.p. — ~되다 / believed to V — ~하는 것으로 여겨지는`. 각주 spans는 실제 believed와 병렬 to 두 개(to warn, to urge)이며 `verb_form.usage:passive-participle`과 `verb_construction.kind:to-complement`를 함께 둔다. warn of·urge A to V 등 V 자리 낱말은 따로 지원한다.
- **검사기 보완(사용자 결정 “검사기 보완”):** `scripts/check_learning_content.py`는 원래 수동 p.p. 표제어를 실제 p.p. 한 낱말로만 받았다. 이 사본에서는 to-complement가 함께 선언된 경우에만 `실제 p.p. + to V` 표제어를 받고, 연결어는 실제 to만(병렬이면 여러 개) 허용한다. 원형 표제어·A/B 틀(verb-frame)·to 아닌 연결어는 계속 거부한다(`tests/test_passive_to_complement.py`). 다른 교재로 자동 확대하지 않는다.
- **같은 검수의 다른 결정:** s09 `unless significant action is taken`의 significant는 ‘중대한, 상당한’(규모)으로 s05 오늘의 낱말 ‘중요한, 의미 있는’과 뜻이 달라 ★를 붙이지 않는다(사용자 결정 “★ 없이 둠”).
