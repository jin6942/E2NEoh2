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
