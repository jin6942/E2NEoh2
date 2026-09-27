# 공통 원고 데이터 v1

Claude·ChatGPT·Codex가 같은 구조의 JSON을 작성하고 같은 검사기를 실행한다. 모델이 본문을 읽고 판단할 부분과 기계가 확인할 부분을 구별한다. JSON은 언어 검수 결과를 대신하지 않으며 구조 검사만으로 FINAL을 확정하지 않는다.

`check_learning_content.py`는 해석·분석·워크북 연결을, `check_book.py`는 여기에 문항 원문 복원·편성·빠른 정답·해설의 연결을 추가로 검사한다. `book_plan.py`는 MASTER 역할 계획을, `export_handoff.py`는 같은 데이터의 QC TXT를 만든다. 생성 뒤에도 언어 검수·저장본 대조·Word 페이지 검수가 필요하다. 기존 자유 형식 TXT는 내용을 대조하여 공통 데이터로 이관하며, 자동 왕복 변환이 구현됐다고 안내하지 않는다.

## 최상위

| 필드 | 내용 |
|---|---|
| schema_version | 정수 1 |
| metadata | book_name, course, publisher_author, lesson. 실제 교재 식별 정보. lesson_id·lesson_number를 추가하면 같은 과를 가리켜야 함 |
| sources | 독립 본문 배열. id, text, sentences, provenance. 실제 소제목은 subheadings, 특수 문장 경계 확인은 boundary_reviews에 기록 |
| paragraphs | 원문 순서의 id, source_id, subheading_id 또는 null, sentence_ids |
| grouping_resolutions | 소제목 없는 짧은 단락의 실제 확인 결정 배열. source_id, paragraph_ids, instruction |
| units | 확정 공통 단위 배열. 아래 필드 참조 |
| sentences | 원문 순서의 문장별 해석·분석 주석 배열 |
| assessment | 전체 교재 검사 시 필수. check_answer_links.py의 scope/plan/questions/quick_key/explanations |
| question_sources | 전체 교재 검사 시 필수. 각 문항의 id와 question_source.py의 원문 변형 입력 |
| layout_adjustments | 실제 Word 관찰에 근거한 쪽 배치 또는 아래 승인된 소폭 조판 조정 기록 |

sources의 sentences는 `{id,start,end}` 배열이며 위치는 독립 본문의 text 내부다. provenance에는 실제 원본의 filename, sha256, location(쪽·영역), verification_record(전사 대조 기록)를 둔다. 기록된 해시를 실제 파일과 비교하는 작업도 수행한다. 이 검사기는 기록 형식과 전사 범위를 확인할 뿐 외부 원본 파일을 자동 열어 진위를 확인하지 않는다.

### 과 식별과 학생용 표시

`metadata.lesson`은 확인한 과를 나타낸다. `UNIT03`, `LESSON 3`, `제3과`, `3과`, `03`처럼 같은 숫자를 가진 기존 입력을 지원한다. `source_contract.lesson_identity(metadata, cover)`는 `{number:3, kind:"lesson", internal_id:"UNIT03", display:"3과"}`를 돌려주고 입력값은 바꾸지 않는다. `display_lesson`은 학생용 `3과`를 반환한다. `metadata.lesson_id`, `metadata.lesson_number`, `cover.lesson_number`를 제공했다면 모두 같은 과여야 하며 상충하면 실패한다. 과목명·출판사·저자명은 실제 확인한 공식 표기를 그대로 기록하고, 과 번호를 맞추기 위해 제목 문자열에서 추측하지 않는다. 인계 TXT는 내부 `[UNIT] UNIT03`과 `[학생용 과 표시] 3과`를 구분한다.

교과서의 Special Lesson은 정규 과와 다른 종류다. 원본에서 확인한 `metadata.lesson: "Special Lesson 1"`(대소문자·`01` 허용)은 `{number:1, kind:"special", internal_id:"SL01", display:"Special Lesson 1"}`로 반환한다. 내부 형식 `SL01`도 입력으로 지원하므로 `metadata.lesson_id: "SL01"`로 같은 특별 과를 명시할 수 있다. 학생용 제목·인계 TXT에 `Special Lesson 1`을 유지하고 `1과`로 바꾸지 않는다. 특별 과에 `UNIT01`·`1과`를 함께 기록하거나 정규 과에 `SL01`을 함께 기록하면 종류 충돌로 실패한다. 숫자만 있는 `lesson_number: "01"`은 종류를 바꾸지 않는 번호 확인값이다.

Special Lesson 표지는 `cover.lesson_label: "SPECIAL LESSON"`, `cover.lesson_number: "01"`처럼 실제 원본에 맞춘 값을 사용한다. 알려진 표지 라벨 `LESSON`·`UNIT`·`SPECIAL LESSON`이 metadata의 과 종류와 다르면 실패한다. 표지 라벨이 없는 부분 검사에서도 종류를 추측하거나 원고를 고치지 않으며, 전체 생성에서는 기존 표지 필수 필드 검사를 계속 적용한다. 썸네일 입력 변환기의 원본 제목 형식은 `N과`만 표현하므로 Special Lesson은 그 변환 대상이 아니다. 이 지원을 이유로 보호된 썸네일 코드·로고·MASTER·역할 계약을 수정하지 않는다.

선택 필드 `cover.lesson_suffix`(예: `"Further Reading"`)가 있으면 표지의 `출판사 · 과` 줄만 `2과 (Further Reading)`처럼 과 표시 뒤에 괄호로 덧붙인다. 한 줄 문자열이어야 하며 괄호를 직접 넣지 않는다. 과 식별·쪽 머리·해석지 헤더·파일명에는 쓰지 않는다. (2026-09-27 영어2 YBM(박) 2과 Further Reading 사용자 요청으로 이 스킬 사본에만 추가)

### 해석지 헤더의 표시 정규화

해석지의 학생용 교재명은 자유 `metadata.book_name`을 그대로 출력하지 않고 정규화한 `metadata.course` + 공백 + `metadata.publisher_author`에서 파생한다. `능률(민병천)`·`NE능률(민병천)`의 알려진 별칭(중간 공백 포함)은 `NE능률(민병천)`로 표시하며 그 밖의 출판사·저자는 보존한다. 원고의 식별값과 전달용 파일명을 다시 쓰는 규칙이 아니다. 과 표시는 위 `lesson_identity`를 계속 사용한다.

`sources[].label`의 `교과서 본문`·`본문`만 학생 표시 `본문`으로 정규화하고 다른 실제 출처명·원문 소제목·ID는 유지한다. DOCX와 FINAL 인계가 같은 표시 계산을 사용한다. 전체 헤더 순서·공통 안내는 [조판 기준](layout-rules.md#2026-09-26-해석지-헤더-통일과-도입-질문-제외)을 따른다.

### 원문 소제목의 별도 보존

`paragraphs[].subheading_id`가 있으면 해당 `sources[].subheadings`에 원문 소제목 발생마다 아래 레코드를 둔다.

```json
{
  "id": "heading-occurrence-1",
  "text": "실제 원문에 인쇄된 소제목 그대로",
  "location": "원본 42쪽 본문 상단",
  "before_sentence_id": "s1",
  "artifact_sha256": "해당 sources.provenance.sha256과 같은 원본 파일 해시"
}
```

`sources.text`는 본문 전사이므로 소제목을 본문 문장 사이에 끼워 넣지 않는다. 위치는 원본 쪽·영역인 `location`과 그 소제목 바로 뒤 첫 문장인 `before_sentence_id`로 연결한다. 같은 제목이 다시 나타나도 각각 다른 발생 ID를 사용한다. ID는 첫 번째 소속 원문 단락의 첫 문장에 연결되어야 한다. 원문 소제목은 작성한 분석 제목/주제로 대체하지 않는다. `unit_subheadings(data, unit)`는 확정 단위에 해당하는 원문 소제목을 원문 순서로 반환하며 DOCX와 인계 TXT가 같은 레코드를 사용한다.

기존 원고에 `subheading_id`만 있으면 검사 결과는 `NEEDS_SOURCE_REVIEW`와 `MISSING_SOURCE_SUBHEADING`이다. 원본을 읽어 원문 문자열·위치·해시를 기록한 뒤 다시 검사한다. 분석 제목을 복사하거나 소제목을 새로 지어 마이그레이션하지 않는다. 원문에 소제목이 없는 단락은 `subheading_id:null`을 사용하며 기존 무소제목 묶음 확인 규칙을 따른다. 등록한 소제목의 대응 단락이 없거나 출처 해시가 다르면 오류다.

### 문장 경계의 공백 확인

`Earle.Sylvia`, `tools.We`처럼 인접한 두 원문 문장 경계에서 종결부호와 다음 영문이 공백 없이 붙으면 `JOINED_SENTENCE_BOUNDARY`와 `NEEDS_SOURCE_REVIEW`를 반환한다. 원본의 줄바꿈·공백을 잘못 전사했는지 대조하고, 잘못됐다면 권위 전사와 문장 위치·연결된 문제 원고를 함께 정정한다. 생성기는 공백을 자동 삽입하지 않는다. 공백 또는 줄바꿈이 있는 정상 경계에는 예외 기록이 필요 없다.

원문이 실제로 붙여 인쇄되어 있거나 약어 등의 경계를 원본으로 확인했다면 `sources[].boundary_reviews`에 다음 값을 기록한다.

```json
{
  "left_sentence_id": "s5",
  "right_sentence_id": "s6",
  "resolution": "source-confirmed-no-space",
  "reason": "원본에서 확인한 구체적인 이유",
  "verification_record": "실제 원본 쪽·영역과 대조 기록",
  "artifact_sha256": "해당 sources.provenance.sha256과 같은 원본 파일 해시",
  "transcription_sha256": "현재 sources.text의 UTF-8 바이트 SHA-256"
}
```

`resolution`은 `source-confirmed-no-space` 또는 원본 대조로 확인한 `abbreviation-boundary`다. 예외는 해당 인접 문장 쌍에만 적용하며 다른 경계로 확장하지 않는다. 전사나 원본 해시가 바뀌면 옛 검토 기록을 재사용할 수 없다. `source_contract.transcription_sha256(source)`로 전사 해시를 계산할 수 있다. 이 확인도 기록의 대응 검사이며, 검사기가 외부 원본을 직접 열어 확인했다는 뜻은 아니다. 의미상 문장 분할의 정확성은 원문 검수 대상이다.

문장·각주 내부 위치는 각 문장의 text 기준이다. 문항 변형 위치는 question_source.py가 정의한 발췌 원문 기준이다. 전부 Unicode 코드 포인트, 0부터 시작하고 끝 위치를 포함하지 않는다. 원문 기호·대소문자·구두점을 정규화하지 않는다.

## 묶음 결정

단락에 6문장 이하가 있으면 같은 소제목 전체를 묶는다. 소제목 ID는 문자열 제목 자체가 아니라 해당 소제목이 등장한 위치를 식별한다. 소제목 없는 짧은 단락은 grouping_resolutions가 없으면 NEEDS_SOURCE_REVIEW이며 확정 단위를 내보내지 않는다.

확인 결정의 paragraph_ids는 같은 독립 본문의 연속된 무소제목 단락을 실제 순서대로 적는다. 짧은 단락과 인접한 긴 무소제목 단락을 함께 묶거나 짧은 단락 하나를 유지할 수 있으나 실제 사용자 확인 내용이 instruction에 있어야 한다. 자동 처리를 위해 확인 내용을 만들어 넣지 않는다. 이 예외 입력으로 소제목 규칙을 덮어쓰거나 다른 본문을 합칠 수 없다.

## 문장 주석

각 sentences 항목에는 source_id, id, text, key(참/거짓), chunks, natural_ko, clauses, glosses, lexical_coverage를 둔다. hints는 필요한 문장에 두며, 실제 관계대명사·관계부사절은 생략 여부와 무관하게 연결 힌트를 포함한다. 각주·S/V 기재만으로 관계사 힌트를 대신하지 않는다.

- text는 sources에서 해당 문장의 start/end로 잘라 얻은 원문과 정확히 일치한다.
- chunks는 `{start,end,ko}` 배열이다. 영어는 원문에서 파생하며 한국어 청크와 별도 자연 해석을 모두 작성한다.
- clauses는 sv_line.py 계약이다. 절 종류·주어/동사 위치·축약형 해석은 원문에서 검토하여 기록한다. `be able to`의 V에 able을 포함하지 않는다.
- 같은 절의 병렬 동사를 잇는 실제 `and`·`or`·`but`는 기존 `verb_spans`에 원문 순서로 포함한다. 접속사만 별도 span으로 두거나 이미 접속사를 포함한 동사 조각을 유지하며, 중복해서 넣지 않는다. 예: `She reads and writes.`의 `verb_spans:[[4,9],[10,13],[14,20]]`은 `V: reads and writes`를 표시한다. 부사·목적어를 생략한 간격에서 접속사를 자동 추정하거나 모든 span 사이에 `and`를 넣지 않는다. 조동사·완료·진행·수동의 분리된 동사 조각은 기존 공백 결합을 유지한다. 새 필드 없이 검토된 원문 위치만 사용하며, 위치 검사 통과가 실제 병렬 관계의 확인을 대신하지 않는다.
- S/V 주어 표시를 줄일 때는 `clauses[].subject_display_spans:[[start,end]]`와 비어 있지 않은 `subject_display_review` 문자열을 함께 둔다. `subject_spans`는 실제 전체 주어를 보존한다. 두 필드는 선택 사항이며 없으면 구형 전체 주어 출력으로 호환한다. 표시 범위는 정확히 하나의 연속 구간이고 전체 주어 역시 하나의 연속 구간이어야 한다. 표시 시작은 전체 주어 시작과 같고 끝은 전체 주어 끝 이하이며, 낱말·하이픈·아포스트로피 중간을 자르거나 양끝 공백을 포함하지 않는다. 검토된 전체 범위를 그대로 표시하는 것도 허용한다. 한 필드만 사용·빈 표시·범위 밖 표시·중간 명사만 발췌·여러 조각으로 분리·다중 전체 주어 범위 축약은 허용하지 않는다. `subject_relative` 절과 주어 없는 명령문에는 이 표시 필드를 넣지 않는다. 긴 명사구 주어의 S/V 표시에서는 한정사·앞수식어·중심명사를 남기고 뒤수식어를 제외한다. 내부 `subject_spans`의 실제 전체 주어는 보존하며, 문법 검토 후 `subject_display_spans`와 `subject_display_review`로 표시 범위와 이유를 따로 기록한다. 명사절·동명사 주어, 부분/수량 표현, 등위 주어는 이 명사구 축약으로 의미·수·구조를 잃지 않게 전체를 유지한다. 검토 기록에는 남긴 중심명사와 제외한 뒤수식어 또는 전체 유지 이유를 적는다. 범위 검사는 문법 축약의 타당성을 증명하지 않으며 L 독립 검수에서 실제 원문을 확인한다.
- glosses는 원문 등장 순서로 `{id,spans,headword,meaning_ko,star,today_word_id?,verb_form?,verb_phrase?,verb_construction?}`를 둔다. spans는 실제 원문의 `[[start,end],…]`이며 표제어와 별도로 보존한다. 수동·능동 완료는 기능 공식과 낱말을 나눈다. 수동의 낱말은 실제 p.p.형·수동 뜻(`be p.p. — ~되다 / produced — 생산된`), 능동 완료는 원형·기본 뜻과 실제 p.p. 관계(`have p.p. — ~했다 / find — 발견하다 (found는 find의 p.p.형)`)로 제공한다. 완료수동 `have been p.p.`는 수동이므로 실제 p.p.형을 유지한다. 전치사의 흔한 뜻으로 이해하기 어려운 `be provided with`·`be satisfied with` 등의 숙어는 한 각주로 유지한다. 독립 p.p.는 실제 형태·문맥 뜻(`held — 개최된`, `trained — 훈련받은`), 일반 정규과거 -ed는 원형·기본 뜻, 불규칙 과거는 현행 표기, 일반 -ing는 기존 기능/원형 분리를 유지한다. 이번 p.p. 구별 밖인 완료진행 `have been V-ing`와 오늘의 낱말 선정·표기는 별도 현행 규칙을 유지한다. 원문 text·spans·lexical_coverage는 표제어 정규화로 바꾸지 않는다. 실제 be 고정 숙어의 정규 패턴과 용법별 구문 예외는 `gloss-rules.md`를 따른다.
- `verb_phrase`는 고정 숙어와 기존 완료진행 결합에만 사용한다. 고정 숙어는 `{usage:"idiom",dictionary_headword:"be provided with",review_record,reason,formula_label:"be p.p.",source_spans:[[start,end],…],verb_span:[start,end]}`로 실제 판정 근거를 기록한다. source_spans는 해당 각주 spans 안의 실제 표현이며 앞의 be 활용형만 사전형 be로 정규화한다. 나머지 고정 낱말·전치사는 원문과 순서까지 일치해야 한다. `be born`·`be called A`도 실제 해당 구문이면 사전형을 유지하고 A의 낱말 뜻은 따로 둔다. `have been V-ing`의 기존 결합 계약은 이번 p.p. 변경 밖이라 유지한다. 구형 일반 수동·능동 완료 verb_phrase는 최신 검사에서 기능/낱말 분리로 이관해야 하며 읽기 호환을 현재 규칙 적용 완료로 보지 않는다.
- `verb_form`은 실제 용법을 검토한 낱말의 `{usage,source_span:[start,end],lemma,function_gloss_id?}`다. source_span은 각주 spans 안의 실제 영어 한 단어 토큰이다. `usage:"passive-participle"`은 수동/진행수동/완료수동의 실제 p.p.형 표제어·수동 뜻, `usage:"perfect-participle"`은 능동 완료의 원형 표제어·기본 뜻과 의미 뒤 실제 p.p. 관계 병기다. 두 용법은 `function_gloss_id`로 같은 문장의 기능 각주를 연결하며 그 각주 `combines_with`에도 낱말 ID가 있어야 한다. 능동 완료의 `meaning_ko`에는 `(found는 find의 p.p.형)`처럼 실제형과 lemma의 관계를 적는다. 기존 `past-participle`은 독립 수식/보어의 실제형, `regular-past`는 원형, `irregular-past`는 실제형, `ing`는 기존 원형 분리다. 독립 p.p.에 없는 be나 별도 p.p. 기능을 보충하지 않는다. be 사전형 숙어에는 낱말용 필드를 억지 적용하지 않는다.
  - `usage:"third-person-singular"`는 사람이 3인칭 단수 일반동사로 판정한 각주의 원형 표제어다. 실제 한 단어 `source_span`, 정확한 `lemma`, 판정 근거 `review_record`가 필수다. 예: 본문 `helps`의 범위에 lemma `help`, 표제어 `help`; 실제 구문 `provides … with …`에는 기존 `verb_construction` 범위를 유지하며 `provide A with B`를 쓴다. `has`·`does`는 어휘적 동사 용법만 이 선언을 쓰며 기능 공식은 제외한다. 별도 새로운 의미나 공식은 추가하지 않는다. 검사기는 선언한 실제형과 원형의 철자 관계 및 표제어를 대조할 뿐, 명사/동사·조동사 구분과 정확한 사전 원형을 자동 판정하지 않는다. 복수 명사의 실제 표제어는 보존하며 이 동사 필드를 붙이지 않는다. 원문·청크·S/V·힌트·인용·실제 연습 영어·오늘의 낱말은 바꾸지 않으며 해당 각주 ID를 재사용하는 도움말만 같은 표제어를 출력한다.
- 원형 동사 구문에는 `verb_construction:{kind:"verb-frame"|"to-complement",verb_span:[start,end],lemma,link_spans:[[start,end],…],review_record}`를 기록한다. `provide A with B`는 verb-frame, `struggle to V`는 to-complement이며, verb_span은 실제 provided/struggled, link_spans는 실제 with/to 위치다. 각주 spans는 verb_span과 link_spans만 정확히 덮고 A/B/V의 실제 낱말 뜻은 따로 지원한다. to-complement는 단순 동사+to V에 사용하고 persuade A to V 같은 목적어 틀은 verb-frame으로 기록한다. 능동 완료와 결합하면 같은 lexical 각주에 perfect-participle·function_gloss_id도 둔다. 목적 to V는 이 결합 필드를 만들어 묶지 않는다.
  - 실제 수동 구동사 `dug up`처럼 낱말 뜻에 필요한 particle은 삭제하거나 별도 전치사 뜻으로 바꾸지 않는다. `verb_form.source_span`은 dug 토큰, `particle_spans:[[start,end],…]`는 실제 up 토큰이며 `review_record`에 구동사 판정을 기록한다. 각주 spans는 동사 토큰과 particle 토큰만 각각 원문 순서로 담고 표제어는 `dug up`, 뜻은 `파내어진`처럼 전체 낱말 뜻이다. 목적어를 이 범위에 넣지 않는다. 이 선택 필드는 수동 각주의 원문 연결을 지원하며 그 사실만으로 구조 힌트를 추가하거나 선정 우선순위를 바꾸지 않는다.
  - `give A B`처럼 실제 고정 연결어 없이 목적어 자리만 있는 verb-frame의 `link_spans`는 빈 배열이다. 이 경우 각주 spans는 실제 given 토큰만 연결하고 A/B에 해당하는 낱말은 각자 지원한다. 없는 to/with를 보충하거나 대상 낱말을 각주 범위에 흡수하지 않는다. `to-complement`는 여전히 실제 to 연결 위치가 필요하다.
  - 이 선택 필드는 제작자와 독립 검토자의 실제 용법 판정을 기록하는 계약이며 검사기가 철자만으로 품사를 추정하는 기능이 아니다. 새 제작·해당 낱말 수정에서는 확인한 적용 대상을 선언한다. 옛 자료의 필드 부재는 구조 호환일 뿐 최신 검토 완료가 아니다. 검사 보고의 `verb_form_declarations`에 미선언과 실제 선언 수를 구별하고 의미 검토의 누락을 PASS로 숨기지 않는다.
- 단독 you/You의 lexical_coverage는 gloss_id:null, exemption:standalone-you, reason으로 원문 위치를 보존한다. you 단독 각주는 만들지 않고 다른 대명사나 숙어 속 you로 제외를 확대하지 않는다.
- 국가명 US에 검사 통과용 referent_ko를 만들지 않는다. 기존 필드에서 원문이 정확히 `US`이고 headword가 `US`/`the US`/`The US`, meaning_ko가 `미국`/`미합중국`인 검수된 각주만 국가명으로 구분한다. 대문자라는 이유로 실제 대명사를 제외하지 않는다. 같은 지문의 반복 국가명은 검증된 첫 각주에 `proper-name-repeat`로 연결할 수 있으며 앞선 등장·출처·원문 위치 검사는 유지한다.
- 지정 대명사 they/their/them/themselves/our/us/his/hers/its의 각주는 뜻뿐 아니라 referent_ko도 기록한다. meaning_ko의 조사는 실제 문장·구문 틀에 맞춘다. 예: `we — 우리는`, `they — 그들은/그것들은`, 목적어 us는 ‘우리를’, 수여 대상은 ‘우리에게’, A가 틀에 들어가면 ‘우리가’. 소유격은 소유 관계를 유지한다. 출력에서는 각주 상세 규칙에 따라 뜻·지시 대상을 결합한다. S/V에는 지시 대상을 추가하지 않는다.
- hints는 `{span:[start,end],meaning_ko,explanation,display_pairs:[{en,ko,emphasis_links,emphasis_note?,pronoun_refs?}],structure_label?,category?,display_spans?,display_mode?,display_span?,formula_label?,lexical_step?,omitted_relative?,omitted_conjunction?,emphasis_policy?,participle_focus_gloss_id?}` 배열이며 문장당 최대 2개다. span은 실제 원문 근거, meaning_ko와 explanation은 내부 검수 근거다. 학생용 DOCX와 FINAL은 display_pairs와 일반형의 structure_label을 출력하며 내부 뜻·설명 필드를 자동 덧붙이지 않는다. 일반형은 대응 대괄호를 유지한 `영어 → 한국어 (structure_label)` 한 줄로 표시한다. 절 연결의 display_pairs에는 연결어와 실제 S′·V′까지만 넣는다. 주격 관계사는 V′만, be동사는 최소 보어만 예외로 허용한다. 관계사 앞 명사와 가주어 It~that 틀은 남기되 일반 명사절 바깥의 means·have found 및 동사 뒤 목적어·전치사 대상은 넣지 않는다. 동명사·분사·부정사 등의 자체 연결도 한 문법 초점의 최소 범위만 기록한다. 문법 연결을 동사 구문·기능 결합보다 먼저 고르고, 상위 문법의 display_pairs에 안쪽 동사 구문 A/B 풀이까지 합치지 않는다. 자세한 선정 기준은 analysis-content.md를 따른다. 일반형의 표시 대괄호는 선택한 대응 범위이며 전체 절의 문법적 경계를 뜻하지 않는다. span은 실제 연결 근거에 맞게 기록하고, 표시를 짧게 했다는 이유로 내부 explanation의 실제 전체 절 판정을 축소하거나 바꾸지 않는다. 절 연결과 구문 자체를 구별하는 표시 범위, 부정·양태의 보존은 `analysis-content.md`를 따른다. 일반형은 1쌍이 기본이며 최대 3쌍을 허용한다. 복수 쌍은 ` / `로 같은 줄에 연결하고 마지막 한국어 뒤에 이름표를 한 번만 붙인다. structure_label은 일반형에서 필수인 짧은 한국어 구조 이름표다. 특정 문법명 목록으로 판정하지 않으며 빈 값·제어문자·괄호를 포함한 값·60자 초과를 허용하지 않는다. 입력·출력 모두 수동 줄바꿈을 넣지 않으며 Word의 자연스러운 줄 감김은 허용한다.
- 생략 관계사 표시에는 일반형 `display_mode:"omitted-relative"`, `omitted_relative:"that"`를 둔다. `omitted_relative`는 실제 선행사·격·문맥에 맞는 `that/which/who/whom/when/where/why` 중 하나이며 생략 접속사에 쓰지 않는다. `display_pairs`는 정확히 1개다. 영어 관계절의 대괄호 시작에 `(that)`처럼 해당 표지를 한 번만 넣는다. 예: `{en:"a few solutions [(that) we can find]",ko:"[우리[인간들]가 찾을 수 있는] 몇 가지 해결책",pronoun_refs:[{en_span:[24,26],ko_pronoun_span:[1,3],ko_reference_span:[3,8]}],emphasis_links:[{en_spans:[[18,22]],ko_spans:[[8,9],[16,17]]}]}`. 위치는 삽입 괄호를 포함한 표시 문자열 기준이며 실제 강조는 괄호를 제외한 관계사 글자와 한국어의 최소 대응 부분에만 적용한다. `structure_label`에는 ‘관계’와 ‘생략’을 포함한 실제 용법의 짧은 이름표를 둔다. 이 모드의 `emphasis_links`는 정확히 1개이고 영어 범위는 보충 관계사 글자 하나, 한국어 범위는 대괄호 안의 최소 문법 대응 범위다. 별도 S′를 가진 목적격 관계절은 해당 S′ 주어의 실제 조사 `이/가`와 관형 연결 어미를 각각 비중첩 구간으로 둘 수 있다. 주격 관계사에 없는 별도 S′·조사를 만들지 않는다. 대괄호 안 전체를 선택하지 않으며 한 음절로 강제하지 않는다. 원문 위치 `span`은 보충 전의 실제 원문을 가리키고, 승인된 괄호 표지만 제거한 영어는 실제 연속 원문 발췌와 같아야 한다. 원문·청크·S/V·각주·정식 해석에는 이 표지를 추가하지 않는다. 이 모드에서는 빈 `emphasis_links`와 `emphasis_note` 예외를 사용하지 않으며, 접속사 that은 아래 별도 모드로 구분하고 주어·to를 보충하는 모드로 확대하지 않는다.
- 생략 명사절 접속사 that은 `display_mode:"omitted-conjunction"`, `omitted_conjunction:"that"`, `structure_label:"명사절 접속사 that 생략"`을 사용한다. display_pairs는 1개이며 영어 대괄호 시작에 `(that)`을 정확히 한 번 넣는다. 예: `{en:"[(that) she knew]",ko:"[그녀가 알았다는 것]",emphasis_links:[{en_spans:[[2,6]],ko_spans:[[3,4],[7,11]]}]}`. 표지를 제거한 표시 영어는 실제 연속 원문과 같아야 하며 괄호는 보통, that 글자와 실제 주어 이/가·해당 ~하는 것/~라는 것/~라고/~다고 연결만 강조한다. 빈 링크나 ko-only 정책으로 대체하지 않는다. 원문·청크·S/V·각주·자연 해석은 보존하며 관계사는 omitted-relative로 따로 판정한다.
- 분리 구동사 목적어만 생략하는 일반형 예외는 `display_mode:"split-phrasal-verb"`, `display_spans:[[start,end],[start,end]]`를 사용한다. `display_pairs`는 정확히 1개다. 조각은 정확히 2개이며 같은 원문의 `span` 안에서 앞에서 뒤로 겹치지 않게 선택하고 두 조각 사이에 실제로 생략한 원문 글자가 있어야 한다. 영어의 편집용 `[ ]`를 벗긴 값은 두 실제 원문 조각을 공백 포함 ` … `로 연결한 값과 같아야 한다. 예: `[after you throw … away] → [여러분[독자들]이 버린 후에]`. 생략되는 것은 throw와 away 사이 목적어 them뿐이고 그 뜻은 한국어에도 넣지 않는다. 일반형의 짧은 `structure_label`과 대응 대괄호를 유지하며 `category:paired-structure`를 사용하지 않는다. 분리 구동사의 실제 의미·생략 대상은 원문에서 사람이 확인하며 위치 검사가 문법 판정을 대신하지 않는다. 동사 내부 부사를 일반적으로 지우는 기능으로 확대하지 않는다.

- 짝 구조(`category:paired-structure`)의 display_pairs는 정확히 1개이며 `{en,ko}`를 모두 작성한다. `display_spans:[[start,end],…]`는 해당 문장 text 기준으로 고른 실제 원문 조각의 위치다. 각 위치는 0부터 시작하고 끝을 포함하지 않으며 기존 span 안에서 원문 순서대로 겹치지 않아야 한다. en은 각 조각을 철자·어순·구두점 그대로 ` … `로 연결한 문자열이며 필요하면 끝에 ` …`를 붙일 수 있다. 예: `{en:"both to hide … and to secretly crawl up to …",ko:"숨기 위해서도 … 몰래 기어서 다가가기 위해서도 …"}`. ko는 선택한 대응 부분만 옮기며 생략한 내용이나 문장 전체의 완성 해석을 덧붙이지 않는다. structure_label·설명문·수동 줄바꿈은 표시 필드에 넣지 않는다. span/meaning_ko/explanation은 내부 근거로 그대로 보존한다. 영어만 내보내는 별도 표시 필드는 사용하지 않는다.
- 기능 결합(`category:function-combination`)의 display_pairs는 정확히 1개다. 시제·태가 아닌 기존 `what to V + do → 무엇을 해야 할지`는 기본형을 유지한다. 기본형 각 항목은 비어 있지 않고 연결 기호는 ` + `다. 시제·태를 공식+낱말의 더하기식으로 쪼개지 않고 아래 verb-function과 승인된 lexical_step 한 줄을 사용한다. 별도 단계별 display_pairs·수동 줄바꿈·대괄호·structure_label을 넣지 않는다.
- 시제·태 힌트는 `category:"function-combination"`, `display_mode:"verb-function"`, `display_span:[start,end]`, `formula_label:"be p.p."` 등을 사용한다. display_pairs는 `{en:"is produced",ko:"생산된다",emphasis_links:[…]}`처럼 실제 동사구 en과 문맥 뜻 ko의 정확히 한 쌍이다. 이번 수동·능동 완료의 한 줄 결합 표시에는 `lexical_step:{gloss_id,form,meaning_ko}`를 추가한다. 예: `{gloss_id:"g-produced",form:"produced",meaning_ko:"생산된"}` → `produced(생산된) → is produced(생산된다) (be p.p.)`. 능동 완료는 `form:"find",meaning_ko:"발견하다"`처럼 연결 원형 낱말 뜻만 쓰고 그 각주의 p.p. 관계 괄호를 힌트에서 반복하지 않는다. 단순 낱말은 괄호 부가 안내를 뺀 주된 문맥 뜻 중 하나 전체를 선택한다. 예를 들어 `발견하다, 알아내다 (흔한 뜻: 찾다)`에서는 발견하다 또는 알아내다이며 흔한 다른 뜻만 택하지 않는다. A/B 틀을 포함한 구문 각주와 연결했어도 lexical_step에는 기본 동사와 그 뜻만 둔다. `form`은 연결 lexical 각주의 실제형/lemma와 일치하며 원문에 없는 다른 동사를 만들지 않는다. display_span은 내부 span 안의 실제 연속 동사구이며 시제·부정·양태·내부 부사를 보존하고 주어·목적어·by/for 구는 제외한다. 강조 위치는 변하지 않은 display_pairs en/ko 기준이고 lexical_step·뜻 괄호·formula_label은 자동 강조하지 않는다. formula_label은 60자 이내의 실제 공식으로 끝에 보통 괄호로 한 번 출력한다. 이번 범위 밖의 일반 진행·완료진행과 구형 표시의 호환을 새로운 p.p. 한 줄 형식 적용 완료로 보고하지 않는다.
- 모든 유형의 display_pairs에는 `emphasis_links`를 명시한다. 각 항목은 `{en_spans:[[start,end],...],ko_spans:[[start,end],...]}`이며 **같은 한 문법 기능**의 실제 영한 대응을 연결한다. 위치는 각각 해당 쌍의 `en`·`ko` 표시 문자열을 기준으로 0부터 세고 끝을 포함하지 않는다. 대괄호·공백도 위치 계산에는 포함하지만 강조 대상 범위에는 대괄호·문장부호·앞뒤 공백을 넣지 않는다. 각 언어 안에서 모든 범위는 겹치거나 중복되지 않아야 한다. 각 배열의 범위는 원문 순서로 기록하며 영한 어순 차이 때문에 링크끼리의 한국어 위치 순서가 영어와 달라지는 것은 허용한다. `With … ing`처럼 하나의 문법 기능이 불연속 표지로 이루어진 경우 한 링크의 `en_spans`에 실제 표지 위치들을, `ko_spans`에 그 기능의 실제 한국어 위치를 기록할 수 있다. 서로 다른 문법 초점을 하나의 링크나 힌트로 합치지 않는다.
- 예: `{en:"a career [of more than thirty years]",ko:"[30년 이상의] 경력",emphasis_links:[{en_spans:[[10,12]],ko_spans:[[7,8]]}]}`는 `of ↔ 의`만 강조한다. `{en:"[using her miniature crime scenes]",ko:"[그녀의 범죄 현장 미니어처를 사용하여]",emphasis_links:[{en_spans:[[3,6]],ko_spans:[[19,21]]}]}`는 `ing ↔ 하여`만 강조한다. 해당 영어 범위에는 기존 영어 색의 굵게+한 줄 밑줄, 한국어 범위에는 검정 굵게+한 줄 밑줄을 적용하며 나머지는 각 언어의 기본색·보통 글씨다. 대괄호 전체 굵게나 무관한 한국어 조사 자동 강조를 적용하지 않는다. 선정 공식의 S′/A 자리에 실제 대응하는 주어 조사 이/가는 그 공식의 연결 어미와 같은 링크에 별도 한국어 범위로 기록할 수 있다. 위의 간략 en/ko 예시를 실제 원고에 쓸 때에도 직접 검토한 링크를 추가해야 한다.
- 독립 p.p. 낱말을 초점으로 삼는 일반 힌트는 `participle_focus_gloss_id`에 해당 lexical 각주 ID를 기록한다. 그 각주는 `verb_form.usage:"past-participle"`이며, 같은 `emphasis_links` 항목이 실제 영어 p.p. 전체와 `meaning_ko`의 선택된 문맥 뜻 전체를 연결해야 한다. 예: held↔개최된. 괄호 안내를 제외한 주된 문맥 뜻에서 하나를 고르며 `(행사가) 열린, 개최된 (흔한 뜻: 손에 쥔)`이면 열린 또는 개최된 전체다. 어미 된만이나 흔한 다른 뜻을 고르지 않는다. 이 필드는 function-combination·paired-structure·생략 모드나 by/without V-ing에 적용하지 않는다. 위치 검사는 실제 문맥 뜻의 타당성을 대신하지 않는다.
- 일반형 동사 결합 구문에는 힌트 최상위 `emphasis_policy:"ko-only-verb-construction"`을 명시한다. `emphasis_links`는 양쪽 모두 비어 있지 않은 실제 대응 범위를 유지하며 렌더러만 영어 강조를 끈다. 한국어는 해당 공식의 조사·연결 어미와 명시된 S′/A 주어 조사만 표시한다. 돕다·제공하다 같은 동사 낱말 뜻과 A/B의 내용어 전체는 선택하지 않는다. 정책 없는 일반형은 양쪽 표시를 유지하며 빈 영어 범위로 예외를 구현하지 않는다. 기능 결합형·짝 구조·조동사 완료형 및 `omitted-relative`·`omitted-conjunction` 표시에는 이 정책을 넣지 않는다. 관계사·가주어·It is not until·by/without+V-ing를 동사 결합으로 오분류하지 않는다. 의미·분류는 원문과 각주로 독립 검수하며 표시 문자열만으로 자동 추정하지 않는다.
- 생략 관계사·접속사는 각각 `omitted-relative`·`omitted-conjunction` 표시와 비어 있지 않은 대응 링크를 사용하며 옛 빈 링크 예외를 적용하지 않는다. 생략된 주어처럼 이번 보충 범위 밖의 요소에 실제 강조 짝이 없으면 `emphasis_links:[]`, `emphasis_note:"생략된 등위절 주어는 표시 영어에 실제 글자가 없어 대응 강조를 만들지 않음"`처럼 실제 이유를 명시한다. 이런 경우 기존 대괄호·짧은 이름표를 유지하며 영어를 지어내거나 한국어만 억지 강조하지 않는다. `emphasis_note`는 내부 근거로만 남기고 단순 누락을 빈 배열로 숨기지 않는다.
- 현재 `rule_revision:R2026-09-23` 원고의 힌트는 이 명시적 링크를 필수로 검사한다. `ko_emphasis_spans`만 있는 입력은 새 대응 강조를 충족하지 못하므로 실제 원문·각주·선정 문법을 읽고 `emphasis_links`로 교정한다. 문구·어미만 보고 자동 이관하거나 과거 한국어 강조를 그대로 짝짓지 않는다. rule_revision이 없는 옛 입력의 무표식 읽기 호환은 최신 규칙 적용 완료를 뜻하지 않는다. 문구를 고치면 영한 위치와 의미 대응을 모두 다시 검토한다. 의미 대응의 정확성은 위치 검사의 통과만으로 증명하지 않는다.
- 포함 힌트는 합친다. 신규 생성·내보내기는 display_pairs 누락을 오류로 처리한다. 과거 원고의 구조 검사 호환 통과는 새 힌트 형식 적용 완료가 아니다. 의미 대응·원문 범위·선정 우선순위는 분석 참조로 검수한다.

현재 생성기는 최상위 `rule_revision:"R2026-09-23"`를 요구한다. 새 제작과 기존 원고의 이번 규칙 이관에서 모든 문장에 `reading_checks`를 기록한다. `review_record`는 실제 문법 판정 기록, `function_gloss_ids`는 해당 문장의 기능 각주 ID 전체를 등장 순서대로 담은 배열이다. 아래 두 경계 배열도 필수이며 검토 후 해당 구조가 없으면 빈 배열을 둔다. 검사 목적의 하위 호환 입력에 필드가 없다는 것은 해당 문법이 존재하지 않는다는 뜻이나 새 규칙 검수 완료를 뜻하지 않는다.

- 수동·능동 완료와 기존 일반 진행·to·-ing의 분리 대상 기능은 `kind:function, combines_with:[낱말각주ID,…]`, 낱말은 `kind:lexical`이다. 명시적으로 연결한 같은 위치 한 쌍의 범위 공유를 허용한다. 숙어와 기존 완료진행의 결합 항목은 같은 정보를 기능·낱말로 다시 중복하지 않는다.
- `reading_checks.required_breaks`는 `{at,kind,reason}` 배열이다. 명사 후치수식에는 `postpositive-adjective` 또는 `postnominal-preposition`으로 실제 구의 시작 위치를 적는다. 수동태의 ‘누가·무엇에 의해’를 나타내는 by 구는 `kind:passive-agent-by`로 by의 시작 위치를 적는다. 실제 수동 관계와 부분 부정 등 의미 범위는 검토자가 확인해 reason과 review_record에 남긴다. 검사기는 해당 위치가 실제 by이고 청크 경계가 유지되는지 확인하며, 빠뜨린 문법 판정까지 자동 발견하지는 않는다.
- 전치사+관계대명사 각주의 기본 뜻은 `S′(이/가) V′하는`이다. 실제 적용 불가 예는 같은 문장의 `reading_checks.review_record`에 문장/각주 ID·원문·표준 적용 시 손실·문맥 뜻을 기록하고 1차 L 검수의 사용자 보고와 연결한다. 별도 임의 데이터 필드나 예외 통과 판정을 만들지 않는다. 실제 힌트의 `explanation`에는 선행사·전치사의 연결 근거를 보존한다.
- `reading_checks.protected_spans`는 `{span,kind,reason,gloss_id?}` 배열이다. kind는 `dummy-it-prefix`, `fixed-expression`, `adjective-complement`, `quantity-kind-of`이다. `quantity-kind-of`는 실제 수량·종류 표현이 같은 어순의 한국어 `~의`로 대응한다고 사람이 확인한 of까지의 연속 원문 범위다. `gloss_id`가 필수이며 그 각주는 단일 `spans:[span]`과 실제 표현 표제어로 같은 전체 범위를 제공한다. 마지막 영어 단어는 of이고, 같은 범위의 구성 낱말·단독 of 각주를 중복하지 않는다. 기계는 선언한 경계·각주 연결만 검사하며 모든 of를 자동 분류하지 않는다. 가주어는 It~that 구간과 통합 구문 각주 ID를 연결한다. that절 내용 전체를 보호 구간으로 만들어 필요한 경계를 없애지 않는다.
- 동사 구문 각주의 선택 필드 `pattern`에는 정규 구문형을 기록할 수 있다. 실제 출력은 `headword`와 `meaning_ko`이며 `spans`와 `lexical_coverage`로 실제 활용형 및 구문의 고정 성분을 연결한다. 구문 안의 중복 기능 각주를 제거하면 `function_gloss_ids`·`combines_with`·힌트 연결도 함께 검수한다.
- 기능 결합 힌트에는 `category:function-combination, gloss_ids:[연결할각주ID,…]`를 두고 기존 높은 우선순위 힌트 뒤에 둔다. 이번 수동·능동 완료는 function+lexical 각주를 연결하고 `lexical_step.gloss_id`는 그 lexical 각주 ID다. 기존 완료진행은 결합 lexical ID 연결을 유지한다. 표시 범위·낱말 뜻→결합 뜻·실제 문맥을 독립 검토하며, 힌트의 한 줄 예시를 이유로 분석 항목 수나 워크북 활동을 늘리지 않는다.
- 새 제작·관계사 힌트 보완에서는 모든 문장의 `reading_checks.relative_gloss_ids`에 실제 관계대명사·관계부사로 확인한 각주 ID를 중복 없이 기록한다. 해당하지 않으면 `[]`다. `three areas where ...`는 해당 where 각주 ID를 넣고, `think about where ... go`의 간접의문 where는 넣지 않는다. 명시한 각주의 원문 위치와 기존 `subject_relative` 절의 관계사 위치가 일반 구조 힌트의 **실제 표시 영어**에도 들어가는지 검사한다. 내부 span만 넓게 잡거나 기능 결합 힌트로 대신하지 않는다. 관계사가 생략되어 실제 각주 위치가 없으면 목록에 가짜 ID를 만들지 않는다. 실제 관계절을 확인해 `omitted-relative` 힌트에만 괄호 표지와 대응 강조를 넣고, 표시용 보충을 원문의 각주 위치로 만들지 않는다. 필드가 없는 구형 입력의 호환 검사는 관계사 힌트 반영 완료가 아니다.

위 위치·연결 검사는 실제로 선언한 문법 판정의 일관성만 확인한다. 원고 작성·검수자는 누락된 후치수식이나 잘못된 용법도 원문에서 찾아야 한다. 기계 검사가 모든 문법 구조를 발견했다고 보고하지 않는다.

각주 ID는 교재 전체에서 유일하다. 일반 단어의 제공 범위는 U56이며, lexical_coverage에는 문장 안의 영어 낱말 **등장 위치마다** 한 행을 둔다. 같은 단어가 되풀이되어도 행을 생략하지 않는다. 검사기의 위치 목록은 영문자와 낱말 내부 아포스트로피를 기준으로 하며 숫자·한글·장식 기호를 영어 어휘로 세지 않는다. 하이픈 표현은 구성 낱말들이 같은 구문 각주를 가리킬 수 있다.

제공한 낱말은 `{span:[start,end],gloss_id}`로 연결한다. 숙어 안 낱말도 그 숙어 각주가 실제로 덮는 위치에 연결한다. 같은 위치에 별도 뜻풀이가 불필요하면 이 연결로 중복을 피하며, 다른 등장 위치까지 제거하지 않는다.

제외 행은 gloss_id 대신 exemption과 구체적 reason을 둔다. 허용 범위는 아래 네 가지이며 새 예외를 조용히 추가하지 않는다.

| exemption | 추가 조건 |
|---|---|
| below-middle1-unneeded | level이 below-middle1이고 문맥상 지원이 불필요하다는 실제 판단. 지정 필수 대명사는 제외 불가 |
| standalone-and-but | 실제 낱말이 and 또는 but인 일반 연결 용법. 상관어구를 누락하는 데 쓰지 않음 |
| standalone-you | 대소문자와 무관한 단독 you. 원문·S/V는 보존하며 다른 대명사나 숙어 속 you로 제외를 확대하지 않음 |
| proper-name-repeat | 같은 독립 본문에서 먼저 제공한 first_gloss_id에 연결. 현재와 실제 같은 이름의 앞선 위치여야 함 |

중1 이상 여부·고유명사 판정·다의어 필요성·관용 표현·전치사 의미는 기계가 판정하지 않는다. 분류가 잘못되어도 형식 검사를 통과할 수 있으므로 내용 검수자가 예외 사유까지 확인한다. ★ 반복 표시는 의미가 같은 오늘의 낱말의 모든 등장과 대조한다. 기계는 제공된 연결의 일관성을 검사하며 누락된 의미 관계를 자동 발견했다고 주장하지 않는다.

### 구조 힌트의 대명사 참조

앞의 `[(that) she knew]`·`using her …` 예시는 생략·강조 위치만 설명하는 단편이다. 실제 원고에서는 앞뒤 문맥에서 she/her의 지칭 대상을 확인하고 아래 `pronoun_refs`를 추가하며, 원고 전체에서도 불명확하면 기록·보고한다.

`hints[].display_pairs[]`의 선택 필드 `pronoun_refs`는 표시 영어의 대명사와 한국어 `대명사[지칭 대상]`을 연결한다. 정확한 키는 `en_span`, `ko_pronoun_span`, **`ko_reference_span`**이며 `ko_referent_span`을 사용하지 않는다. 필드를 사용하면 비어 있지 않은 배열이어야 하며 각 항목에는 이 세 위치 필드만 둔다.

```json
{
  "en": "the fact [that they can recognize]",
  "ko": "[그것들[문어들]이 알아볼 수 있다는] 사실",
  "pronoun_refs": [
    {"en_span": [15, 19], "ko_pronoun_span": [1, 4], "ko_reference_span": [4, 9]}
  ],
  "emphasis_links": [
    {"en_spans": [[10, 14]], "ko_spans": [[9, 10], [18, 20]]}
  ]
}
```

- 모든 위치는 해당 쌍의 **전체 표시 문자열**에서 0부터 세고 끝은 포함하지 않는다. 편집용 괄호도 위치 계산에 포함한다. `en_span`은 실제 대명사 하나를, `ko_pronoun_span`은 조사·괄호 없는 한국어 대명사만 선택한다. `ko_reference_span`은 그 바로 뒤의 `[지칭 대상]` 전체를 양쪽 괄호까지 포함한다. 즉 `ko_pronoun_span[1] == ko_reference_span[0]`이다.
- 항목은 영어 위치 순서로 기록하고 각 언어의 선택 범위는 겹치거나 중복되지 않게 한다. 영어 `one … it`과 한국어 `그것[문어] … 것[팔]`처럼 한국어 위치 순서가 영어와 교차하는 것은 허용한다. `That’s`의 That처럼 실제 축약형 속 대명사도 그 부분만 선택하며 축약형이나 영어를 고쳐 쓰지 않는다.
- 참조어는 비어 있지 않고 내부 대괄호·줄바꿈을 포함하지 않는다. 선언된 `ko_reference_span`만 문법 괄호 검사에서 제외하고 나머지 한국어 문법 괄호와 영어 괄호의 대응·균형·범위를 검사한다. 단지 괄호가 중첩되었다는 이유로 참조어로 추정하지 않는다. 기능 결합(`category:function-combination`)에는 이 필드를 넣지 않는다.
- `emphasis_links`는 한국어 대명사부터 참조 괄호 끝까지를 선택하지 않는다. 기존 문법 초점의 조사·어미는 참조 괄호 뒤의 새 위치로 다시 연결한다. 위 예의 `이`·`다는`은 that에 대응하며 `[문어들]`은 보통 글씨다. 새로운 내용어 강조를 만들지 않는다.
- 실제 지시 용법·단복수·격·참조 내용은 [내용 기준](analysis-content.md#대명사와-지칭-대상)에 따라 사람이 검수한다. 철자·위치 검사나 허용 대명사 목록은 가주어/관계사/한정사 구별과 지칭 대상의 정확성을 보증하지 않는다. 같은 문장의 각주 및 문맥 근거·확인 불가 사유는 기존 `reading_checks.review_record`·힌트 `explanation`에 기록한다. 필드가 없는 구형 원고의 호환 통과는 최신 대명사 참조 검토 완료를 뜻하지 않는다. 본문·S/V·각주·정식 해석과 단독 you의 각주 제외는 유지한다.

## 공통 단위

각 units 항목은 id, source_id, paragraph_ids, sentence_ids, today_words, analysis를 갖고 전체 교재 단계에서는 workbook도 갖는다. 앞 네 필드는 원문과 묶음 결정에 일치해야 한다.

이전 원고의 `hook`은 보존 가능한 과거 입력이다. 2026-09-26 결정으로 노란 도입 질문을 폐지하여 DOCX·FINAL 인계에 출력하지 않고 필수 필드로 검사하지 않는다. 새 질문을 작성하거나 다른 단위에서 복사해 채우지 않는다.

today_words는 최대 8개이며 `{id,text,meaning_ko,source_gloss_id}`로 관리한다. 학생용 text와 답안은 `workbook.md`의 기존 오늘의 낱말 기준을 따른다. 이번 각주의 능동 완료 원형화를 오늘의 낱말에 자동 전파하지 않는다. 선정된 낱말의 각주에는 star=true와 today_word_id를 함께 연결한다.

analysis 필드:

- heading_kind: 제목 또는 주제 중 하나. title_or_topic_en, title_or_topic_ko에 해당 내용을 기록한다.
- intent_ko: 해당 단위의 의도/요지.
- flow: `{sentence_ids,text_ko,label?}` 배열. 단위의 모든 문장을 순서대로 한 번씩 포함한다. 선택 필드 `label`에는 원문의 흐름에 맞게 작성한 단계명(예: `도입`, `전개`, `결론`)을 빈 문자열이 아닌 문자열로 넣는다. A13에 따라 DOCX는 `(단계명)`을 강조하고 QC/FINAL TXT도 같은 단계명을 보존한다. `label`이 없는 기존 원고는 양쪽 모두 `(흐름)`을 사용하며, 검수·변환 과정에서 단계명을 임의로 창작하지 않는다.
- easy_explanations: 기본 서로 다른 원문 3문장을 선정하고 원문 순서로 배치한다. `{sentence_id,explanatory_sentences:[한국어 설명문,…]}`이며 explanatory_sentences는 비어 있지 않은 문자열의 목록이다. 설명문 수의 2~3문장 제한은 폐지하여 1문장이나 4문장 이상도 허용한다. 각 배열 원소에는 한 내용의 짧은 설명문 하나를 담는다. 선정 원문 수 3개와 짧은 단위의 수량 예외는 유지한다. 앞 문맥·역할, 중학생 수준 문체·예시와 L 검수는 [쉬운 풀이 기준](analysis-content.md#각-문장-쉬운-풀이)을 따른다.
- grammar_points: 기본 3개에 승인된 결합 공식 대표 사례 보충을 별도로 허용한다. `{sentence_id,span:[start,end],title,explanation}`의 기존 내용에 아래 syntax_training_version 1 연결 필드를 추가한다. 각 항목은 원문에 근거한 학습 초점 하나이며 title·span·explanation도 그 초점에만 맞춘다. explanation에는 구문 공식·문맥 뜻, 필요한 S/V/A/B 등의 실제 원문과 각 뜻, 핵심 결합 해석을 담는다. 실제 대응 없이 원문 전체와 번역 또는 추상적 읽기 조언만 반복하지 않는다. 낱말과 구의 범위는 구별하며 관계사는 실제 선행사·역할·뒤 S/V 또는 생략 자리를 짚는다. 모든 구조에 A/B를 강제하지 않으며 아래 승인된 연결 필드 외의 임의 필드를 만들지 않는다. 양보절과 조동사 수동태처럼 독립 초점을 합치지 않되 가주어–진주어 같은 하나의 통합 구문은 나누지 않는다. 별도 hints의 짧은 표시 계약은 유지한다.
- relations: 기본 3세트. 각 세트의 head/synonym/antonym은 `{id,text,meaning_ko}`. 실제 품사·뜻·유반 관계는 내용 검수 대상이다.

workbook에는 relation_order(확정 관계 어휘 ID를 개별로 섞은 순서), key_sentence_ids(해당 단위 key=true 문장과 일치), question_id(그 단위 실전문제), syntax_point_ids(해당 단위 grammar_points의 모든 ID를 분석 순서대로)를 둔다. 관계별 묶음으로 출력하지 않는다. 낱말 정답의 표시 번호는 각 활동에서 1부터, 핵심 문장은 1부터 실제 수까지 별도로 파생한다.

### 분석·워크북 구문 결합 연습 계약

새 제작과 이 승인 규칙을 적용하는 수정 원고는 `metadata.syntax_training_version:1`을 기록한다. 표식 없는 구형 원고의 읽기 호환을 새 활동 적용 완료로 보고하지 않는다.

- 모든 `analysis.grammar_points`에 `id`, `formula_key`, `practice`를 둔다. id는 같은 단위 안에서 고유하며 기본 항목과 보충 항목을 모두 포함한다. `formula_key`는 비어 있지 않은 공식 식별 문자열이다.
- `practice`는 `{span:[start,end],formula_support:{en,ko},support_gloss_ids:[...],answer_ko,support_overrides?}`다. span은 같은 문장의 실제 연속 원문이며 해당 분석 항목 span 안에 있다. formula_support는 분석에서 가르친 공식과 그 문맥 뜻을 직접 검토해 적으며 en은 정규화한 formula_key와 일치시킨다. 연결 기능 각주가 있으면 같은 공식·뜻과 일치시키며 독립 p.p. 수식처럼 각주에 별도 공식이 없는 경우에도 분석에서 설명한 공식을 사용할 수 있다. 생성기가 영어 형태만 보고 공식이나 한국어 뜻을 추측하지 않는다.
- support_gloss_ids에는 같은 문장의 연습 범위 안에 실제 근거를 가진 각주 ID를 중복 없이 연결하고 낱말 각주를 최소 1개 포함한다. 문항 아래 도움말 안에서는 주초점 공식을 formula_support에서 먼저 제공하고, 그 뒤의 지원에는 실제 구절의 해석에 필요한 기존 보조 기능 각주(kind:function)와 낱말 뜻을 허용한다. can/can be·완료·전치사 등의 뜻을 빠뜨려 시제·태·양태·경로 관계를 학생이 추측하게 만들지 않는다. 주초점 공식과 같은 항목은 중복하지 않으며 기존 각주의 최종 문맥 뜻을 유지한다. 정규화 표제어와 실제형의 관계 안내 등 각주에서 승인한 정보를 자의적으로 바꾸지 않는다. answer_ko는 표시된 실제 영어 구절의 결합 해석이며 정답지에만 출력한다.
- 선택 `support_overrides`는 `[{gloss_id,form,meaning_ko,review_record,source_span?}]`다. support_gloss_ids에 이미 연결된 각주를 한 번씩만 지정하며 두 가지 검토된 축소만 허용한다. ① 원 각주에 `verb_construction`이 있고 불필요한 A/B 틀이 노출되면 `provide A with B`를 `provide — 제공하다`처럼 원 구문의 검토된 기본 동사와 뜻으로 좁힌다. ② `contributor to`처럼 묶은 원 각주에서 연습 범위에 contributor만 있으면 원 각주 범위와 practice 범위 안의 완전한 낱말 `source_span`을 지정하고 form을 그 실제 원문과 정확히 일치시켜 해당 낱말 뜻만 지원한다. 후자의 경로에서는 실제 p.p.를 임의로 원형화하지 않는다. 두 경로 모두 원 각주를 고치지 않고 ID·경로별 기본형/실제형 일치·review_record와 L의 뜻 검토를 보존한다. 능동 완료 원형 지원으로 좁힐 때도 `(given은 give의 p.p.형)`·`(provided는 provide의 p.p.형)` 같은 원 각주의 실제 p.p. 관계 안내를 삭제하지 않는다. 일반 낱말 뜻을 임의 교체하거나 범위·근거 없이 새로운 도움말을 만드는 예외가 아니다.
- 기본 분석은 기존 3개와 근거 부족 예외를 유지한다. 보충 항목에는 `supplemental:{function_gloss_id,reason}`를 두어 같은 문장의 실제 수동/능동 완료 기능 각주와 보충 이유를 밝힌다. 아직 설명하지 않은 같은 공식의 대표 사례만 단위당 한 번 보충한다. 기존 기본 분석을 보충으로 바꿔 수량 검사를 우회하거나 기본 항목 부족을 보충 수로 채우지 않는다.
- `analysis.formula_routes`는 대상이 없는 단위에도 빈 목록으로 명시하며, 모든 대상 기능 각주를 `{sentence_id,function_gloss_id,formula_key,route,review_record,hint_index? 또는 grammar_point_id?}`로 연결한다. 일반 route는 `hint` 또는 `analysis`이며 hint이면 같은 문장의 실제 선정 힌트 번호(hint_index, 0부터), analysis이면 같은 단위·같은 공식의 분석 ID를 사용한다. 둘을 함께 쓰거나 검토 기록만으로 연결을 대신하지 않는다. 다른 문장에 같은 공식 힌트가 있어도 해당 문장에 결합 힌트가 없으면 분석 대표에 연결한다. 기존 기본 분석이 해당 공식을 설명하면 그 항목을 재사용한다.
- 사용자 승인 부분 부정 예외에는 `route:"approved-exception"`, `exception_kind:"partial-negation"`, `partial_negation_span:[start,end]`, `grammar_point_id`, `replacement_grammar_point_id`, `approval_reference`, `review_record`를 사용한다. 기존 occurrence의 sentence_id/function_gloss_id/formula_key를 보존하고 원래 부분 부정 분석·연습을 grammar_point_id로 연결한다. partial_negation_span은 실제 원문에서 not~solely 등의 범위를 가리키며 원래 분석의 practice 범위 안에 전부 들어가야 한다. 대체 분석 ID는 같은 단위의 다른 문장에서 실제 수동 기능 각주를 근거로 한 보충 항목과 연습을 가리킨다. 그 문장의 기존 hint route는 유지한다. 대체 항목의 supplemental.function_gloss_id·reason은 실제 원문과 사용자 승인 이유를 기록한다. 이 예외의 대체 보충은 자신의 기존 hint route가 있어도 명시적 replacement 연결로 사용되며 일반 보충 허용으로 확대하지 않는다.
- 승인 사례: SL1 s08 `[42,78]`의 `isn’t controlled solely by its brain`은 부분 부정 gp01을 유지하고, 같은 단위 s09 `are located`의 `be p.p. — ~해 있다`를 gp04의 수동 연습으로 제공한다. 원래 기능 키 `be not p.p.`와 대체 기능 키 `be p.p.`를 같은 공식으로 바꾸지 않는다. 승인 근거는 `2026-09-25 사용자 선택: 부분부정 유지·수동태는 다른 문장에서 연습`처럼 실제 결정을 기록한다. 이 예외로 원래 각주·원문·정답 의미를 바꾸거나 다른 생략 사유를 임의 통과시키지 않는다.
- 기능 공식과 formula_key를 비교할 때 소문자·공백·p.p. 표기만 정규화한다. be/have/has/had·부정·조동사·시제·태를 자의적으로 동일 공식으로 합치지 않는다. 일반 완료진행 등 이번 수동/능동 완료 분리 대상 밖으로 자동 확대하지 않는다.
- `workbook.syntax_point_ids`는 해당 단위의 모든 grammar_points.id를 분석 순서 그대로 한 번씩 담는다. 기본·보충 각각 1항목↔1연습↔1정답이다. 실전문제 question_id·모의고사 문항 수에는 이 연습을 합산하지 않는다. 학생용은 4번 연습, 기존 핵심 문장은 5번, 정답도 같은 번호로 내보낸다.
- 기계는 ID·범위·공식 연결·수량과 지원 필드의 일관성을 검사한다. 공식이 실제 구문에 맞는지, 한국어 뜻·답·주체·부정·태가 맞는지는 L 검수에서 대조하고 학생용 정답 누출과 실제 페이지 흐름은 저장본·Word 검수에서 확인한다.

해석지·분석지 제작 단계에서는 `check_learning_content.check(data, scope="learning")` 또는 CLI `--scope learning`을 사용한다. 이 단계는 아직 만들지 않은 `workbook`, 문제 ID, 워크북 낱말 순서를 요구하지 않는다. 각주 별표에 연결된 `today_words`, 원문·해석·분석·핵심 문장 선정과 부족 수량 기록은 계속 검사한다. 전체 교재 단계는 `scope="full"`(기본값)로 워크북 연결까지 검사하며 `check_book.py`가 이를 명시적으로 호출한다. 학습 단계 성공을 전체 교재 검증 완료로 보고하지 않는다.

quantity_exceptions는 부족한 항목마다 `{field,expected,actual,reason,reported_to_user}`를 둔다. field는 key_sentences, easy_explanations, grammar_points, relations 중 하나다. 보고하지 않은 것을 보고했다고 채우지 않는다. 기존 문장이 있으면 핵심 2개·쉬운 풀이 3문장은 각각 확보 가능한 문장 수까지 제공한다. 구문으로 해석하기의 수량 예외는 보충을 제외한 기본 항목 수를 expected/actual로 기록한다. 유반의 적합한 근거 부족도 설명과 실제 제공 수로 기록한다. 수량 예외로 모의고사 수준의 지문 분량이나 정해진 문항 수를 줄이지 않는다.

## 문항 연결

assessment의 세 목록(학생용 문제·빠른 정답·해설)을 각각 확인한다. 같은 데이터를 복사해 세 목록을 만들면 내부 대응만 검사할 수 있으며 독립 검수를 대신하지 않는다. plan의 workbook 문항은 unit_id를 함께 갖는다.

question_sources에는 각 문항 ID마다 실제 독립 원문·첫/마지막 문장·허용 변형 범위를 둔다. 복원한 passage/given/blocks/target은 학생용 원고와 일치해야 한다. 삽입·무관한 문장의 기계적으로 정해지는 답과 순서의 원문 복원 순서는 답안과 추가 대조한다. 다른 유형의 의미적 유일정답은 독립 풀이로 검증한다.

워크북 문제는 과 안의 적절한 독립 본문에서 연속 범위를 고르며, 해당 학습 단위의 문장과 겹쳐야 한다는 제한은 없다. 해당 단위에서 확정한 유반의 의미 학습을 평가하는 연결은 유지한다. 문항의 `learned_relation_uses`에는 `{term_id,choice_number,choice_span:[start,end],surface,reason_ko}`를 실제 사용만큼 기록한다. term_id는 해당 단위의 분석 유반 어휘 ID이고 surface는 선택지의 해당 조각과 같다. 형태 변화·의미상 기여는 독립 검수 대상이다. 세 세트나 아홉 단어 전부 사용을 강제하지 않는다. 실제 원문 부족으로 보고된 유반 0세트는 이 연결 목록을 생략하거나 비우고 일반 실전문제로 출제한다. 오늘의 낱말로의 대체 연결도 강제하지 않는다. 유반이 한 세트라도 있으면 이 예외를 쓰지 않는다. 원문 범위 선정은 문제의 전체 논지·정답·오답 근거와 동학년 모의고사 분량을 함께 충족해야 한다. 발췌 때문에 학습 단위는 바꾸지 않는다.

문항 길이는 `question_sources[].length_review`에 `profile_id`, `grade:1|2`, `benchmark_ids`, `rationale`를 기록한다. 공식 표본 ID는 `question_source.recommended_benchmarks(grade,type)`에서 얻되 비교 근거를 자동 작성하지 않는다. 같은 학년·유형 표본 전체를 대조한다. 표본보다 짧으면 `independent_review_required:true`를 추가하고 실제 독립 검수에서 짧음·정보 전개를 확인한다. 이 필드는 짧은 지문을 충분하다고 승인하는 예외가 아니다. 공통영어는 1, 영어2는 2이며 그 밖의 과목은 `assessment.scope.reference_grade`를 명시한다. 원고보다 긴 표본에 맞추려고 무관한 내용을 붙이지 않는다.

`assessment.passage_groups`는 `{id,kind:"long_reading",set_id,question_ids:[제목문항ID,어휘문항ID],passage_question_id:어휘문항ID}`다. 각 자식 `questions`에도 `passage_group_id`를 적는다. 매회 마지막 두 문항을 하나의 그룹으로 연결하며 총수에 포함한다. 두 문항의 원본·범위·복원 원문은 같아야 한다. 각 `q.passage`는 자신의 source view를 보존하고, 실제 학생용 공유 지문은 어휘 표적·치환을 갖춘 owner view를 **한 번** 출력한다. 두 문항의 길이 비교 유형은 `long41_42`다. 제목의 정답은 치환된 오답 어휘 하나에 의해 흔들리지 않는지 독립 검수한다.

함축 의미의 `questions[].prompt_underlines`는 발문 문자열 기준 `[[start,end]]` 한 구간이며 해당 조각은 `target`과 정확히 같다. 일반 지문의 원문 줄바꿈은 데이터에 보존하고 조판할 때만 공백으로 연결한다. 원문 위치 계산 전에 줄바꿈을 지우지 않는다. 공유 장문은 문단을 유지하고, 순서 문제는 주어진 글·A/B/C의 필수 구획을 유지한다.

표준 전체 편성은 scope.kind=full이며 과목·unit_ids가 metadata·units와 같아야 한다. 사용자 지정 전체 편성은 근거가 있는 custom이다. partial은 일부 검사 전용이며 전체 교재 검사로 승격하지 않는다.

## 승인된 소폭 조판 조정

`layout_adjustments`의 소폭 조정 항목은 `{kind:"compact_block",block_id,profile,content_sha256,renderer:"Microsoft Word",observed_page,evidence_pdf_sha256,reason,approval_reference}`다. `block_id`는 실제 공통 단위의 `<unit_id>/analysis` 또는 `<unit_id>/answers`이고, `profile`은 계약의 `compact_profiles`에 있는 `spacing` 또는 `spacing_and_type`이다. 임의 수치를 원고에 넣지 않고 선택한 프로필의 `role_map`으로 연결한다.

`content_sha256`은 `book_plan.content_hash(data)`의 현재 내용 해시다. `observed_page`는 넘침을 실제로 확인한 Word PDF의 쪽 번호이며 `evidence_pdf_sha256`은 그 PDF의 SHA-256이다. `reason`에는 실제 넘침과 선택 사유를, `approval_reference`에는 이번 사용자 승인을 기록한다. 관찰하지 않은 쪽·이전 내용 해시·가공한 승인 기록으로 대체하지 않는다.

분석은 마지막 `analysis_header` 뒤 설명부에만 적용하며 앞의 끊어읽기·자연 해석은 보존한다. 정답은 해당 단위 정답의 허용 본문 역할만 조정하고 표 및 제목 글자 크기는 유지한다. `spacing`을 먼저 적용하며, 부족할 때만 `spacing_and_type`으로 본문을 0.5pt 줄이되 8.5pt 아래로 내리지 않는다. 제목·유반 글자 크기와 보호 영역은 [최신 조판 규칙](layout-rules.md)의 범위를 따른다. 이 데이터는 별도 강제 새 쪽이나 내용 축약을 허용하지 않는다. 저장본 대조 뒤 실제 Word 재렌더로 넘침·가독성·인접 페이지 흐름을 다시 확인한다.

## 실행

```text
python scripts/check_learning_content.py 원고.json 학습연결검사.json
python scripts/check_learning_content.py 학습단계원고.json 학습단계검사.json --scope learning
python scripts/check_book.py 원고.json 전체연결검사.json
```

검사 보고서는 실제 입력 SHA-256과 범위를 포함한다. 원문 파일 대조, 문법·번역·수준 분류, 문항 독립 검수, DOCX 저장본 대조, Word 조판 검수를 각각 기록한다. 수정 뒤 기존 보고서를 그대로 재사용하지 않는다.
