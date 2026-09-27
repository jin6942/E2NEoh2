# 현재 파일과 검수 기록을 연결하는 출고 기록

`scripts/verify_release.py`는 전체 제작 결과를 읽기 전용으로 검증한다. 원고를 제작하거나 번역·문항을 대신 검수하거나 FINAL을 승인하는 도구가 아니다. 실제 원문·원고·계획·DOCX/PDF·FINAL·수행한 검수 기록을 연결하여, 같은 이름의 옛 파일과 부분 검사를 전체 출고로 오인하지 않게 한다.

현재 기본 ‘최종 출고’는 [전체통합본+분권 5개](split-delivery.md)이며 `scripts/verify_split_release.py`를 사용한다. 아래 통합본 검수 기준은 그대로 유지하고 다음 분권 증거를 추가한다. PDF는 검사용 파일이며 기본 전달 목록에는 DOCX 6개가 든 ZIP 1개만 들어간다.

## 전체통합본과 분권의 현재 출고 기록

`delivery_mode:"integrated_plus_five_docx"`를 명시한다. 아래 기존 원문·공통 원고·계획·통합 DOCX/내부 PDF·FINAL·structure·saved_docx·word_render·S/L/M/N·사용자 요청 검수의 요건을 유지한다. 기존 기록의 mode를 바꾸거나 PDF를 빼는 것만으로 새 출고가 완료되지 않는다.

- `artifacts.split_manifest`: `split_book.py`가 실제 출력한 분권 목록의 `{path,sha256}`. 목록에 연결된 전체통합본은 입력 DOCX와 바이트가 같아야 하고, 다섯 분권은 각 관리 블록이 원래 순서·서식·내용대로 배정되어 모든 블록을 정확히 한 번씩 포함해야 한다. 검사기는 실제 파일을 다시 읽어 확인한다.
- `reports.split_word_renders`: 다섯 권 순서의 배열. 각 항목은 `{kind,pdf:{path,sha256},receipt:{path,sha256}}`이고 kind는 `reading`, `analysis`, `workbook`, `mock`, `answers`다. 실제 Word 렌더 receipt는 아래 `word_render`와 같은 현재 권의 DOCX/PDF 바이트·Word 버전·실제 실행·페이지 수·원본 보존을 기록한다. 다른 권이나 옛 버전의 PDF/receipt는 사용할 수 없다.
- J/K는 전체통합본 PDF 다음 01~05권 PDF 순으로 평탄화한 현재 `word_page_map`의 페이지를 소유·확인한다. 예를 들어 통합본이 50쪽이면 01권 1쪽은 전역 51번이며, 원래 권과 권 안의 쪽 번호도 함께 기록한다. 권 안의 실제 인접 경계는 모두 확인하되 서로 다른 권 사이에 가상의 연결 검수를 만들지 않는다. 묶음 기록은 `word_pages`에 여섯 문서 페이지 수 합계를 적는다.
- 현재 분권 조판 bindings에는 `package_sha256`, `plan_sha256`, `contract_sha256`, `split_manifest_sha256`, `volume_set_sha256`, `pdf_set_sha256`, `word_renders_sha256`, `word_page_map_sha256`을 연결한다. 실제 파일에서 계산한 도구 결과를 사용하며 임의 지문을 만들지 않는다. 독립 J/K의 범위·실행·상세 확인·해결되지 않은 발견 사항은 기존처럼 검사한다.
- R과 사용자 추가 요청 확인은 기존 실제 산출물 해시와 분권 목록·세트 해시를 함께 연결한다. R은 전체 내용의 대응뿐 아니라 여섯 DOCX 실제 저장본과 마지막 수정 요청·다운로드 대상까지 확인한다. 내보내기 성공이나 자동 해시 집계를 독립 R 확인으로 취급하지 않는다.

`verify_split_release.py`의 `docx_files`는 실제 검수 대상 DOCX 6개이며 `delivery_files`는 그 여섯 파일을 담은 ZIP 1개만을 반환한다. `delivery_zip_sha256`을 R·사용자 요청 확인에 연결하고 ZIP을 다시 열어 정확한 파일 집합·이름·바이트와 압축 무결성을 대조한다. PDF·내부 자료 혼입이나 누락·중복·다른 버전의 엔트리는 거부한다. 새 mode가 빠진 통합본 단독 READY, 분권 파일만 생성한 상태, 일부 권의 Word/시각 검수가 빠진 상태는 현재 여섯 파일 최종 출고 통과가 아니다. 미완료는 REVIEW_PENDING, 변조·누락·서로 다른 버전의 연결 오류는 FAIL로 보고한다. 상세 CLI 인자는 각 도구의 `--help`로 확인한다.

## 판정과 범위

- `READY_FOR_RELEASE`, 종료 코드 0: 현재 파일·내용·서식·필수 검수 증거의 범위와 연결을 확인했다. 실제 독립 검수나 언어 판단의 진위를 기계가 증명했다는 뜻은 아니다.
- `REVIEW_PENDING`, 종료 코드 2: Word 미실시, 필수 검수자/파일 부재, 미해결 발견 사항 등 필수 완료 증거가 남아 있다.
- `FAIL`, 종료 코드 1: 현재 원고/계획/계약/결과물 해시·내용·서식이 다르거나 보고서와 재검사 결과가 맞지 않는 등 연결 오류가 있다.

현재 승인된 구문 분석→워크북 연습을 포함한 출고는 원고의 `metadata.syntax_training_version=1`과 현재 실행한 구조검사의 `learning.syntax_training.status=DECLARED_LINKS_CHECKED`를 모두 필요로 한다. 둘 중 하나라도 없으면 `SYNTAX_TRAINING_REVIEW_REQUIRED`로 `REVIEW_PENDING`이며, 구형 원고가 호환 `STRUCTURE_PASS`를 받았다는 이유만으로 최신 규칙을 적용한 `READY_FOR_RELEASE`라고 보고하지 않는다. 구형 원고를 읽는 호환성은 유지하되 활동이나 검수 증거를 자동 작성하여 완료 처리하지 않는다. 연결 검사 통과는 원문·분석·연습·정답의 선언된 연결만 증명하며 구문 뜻·학생 이해도·독립 검수 완료를 대신하지 않는다.

이 판정은 `scope="full"`인 전체 교재 출고만 다룬다. 사용자가 일부 단계만 요청하거나 Word 검수를 제외했다면 그 요청 범위의 실제 완료 상태를 보고한다. 부분 범위를 full로 바꾸거나 미실시를 PASS로 채워 표준 출고 판정을 얻지 않는다.

## 경로·해시·패키지

출고 기록과 작업 파일은 스킬 설치 폴더 밖의 해당 교재 작업 폴더에 둔다. 모든 상대 경로는 출고 기록 JSON의 폴더 기준이다. 파일 참조의 형식은 `{ "path": "실제 경로", "sha256": "실제 바이트 SHA-256" }`다. 스킬 원본, 원문, DOCX/PDF 또는 검수 기록을 검사 보고서 출력 경로로 지정하지 않는다.

`package.root`는 실제로 실행한 스킬 폴더다. `package.files`는 그 아래 배포 파일의 상대 경로→실제 SHA-256 전체 매핑이며 `package.sha256`은 이 매핑의 canonical JSON SHA-256이다. canonical JSON은 Python `json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')`이다. 원문 바이트의 SHA-256과 JSON 정규 표현의 SHA-256을 혼용하지 않는다.

패키지 지문은 `SKILL.md`, 모든 references, scripts, tests, requirements, assets 및 나머지 배포 파일을 포함한다. 실행 후 생기는 `__pycache__`, `.pytest_cache`, `tests/common-test-results.json`, 시험기의 `tests/{master,saved-docx,saved-format,book-plan,build-book,handoff,release}-test-<32자리 hex>` 및 `tests/thumbnail-input-test/<32자리 hex>` 산출물만 고정 제외한다. 이 제외 경로에 배포 코드·규칙을 넣지 않는다. 추가/누락 파일도 탐지하며 심볼릭 링크 패키지는 거부한다. 스킬을 수정하거나 재등록했으면 패키지 지문을 다시 계산하고 영향을 받는 검수 연결을 갱신한다.

검사기는 실제 실행 중인 스킬 전체 정적 파일도 기록된 패키지와 대조한다. 경로가 다른 사본을 지정할 수는 있지만 코드뿐 아니라 MASTER·계약·규칙·시험·의존성까지 파일 집합과 바이트가 같아야 한다. 원고 계획은 실행 모듈의 기본 자산을 쓰고 저장본 검사는 지정된 자산을 쓰기 때문에, 두 패키지의 코드만 같고 자산이 다른 경우는 거부한다. 패키지 이름이나 U 번호만 같다는 것으로 동일 버전이라고 판단하지 않는다. 배포 ZIP 파일 자체의 해시는 별도 배포 기록에 남길 수 있으며, 압축 시각이 달라도 동일한 파일 내용 집합인지 판단하는 실행 기준은 이 전체 파일 지문이다.

## 최상위 기록 schema_version 1

| 필드 | 필수 내용 |
|---|---|
| `schema_version` | 정수 1 |
| `scope` | 문자열 `full` |
| `producer` | 실제 제작자 `reviewer_id`, 실제 실행 `execution_id` |
| `package` | `root`, 전체 `files` 매핑, `sha256` |
| `sources` | 원고의 모든 source에 대해 `{id,path,sha256}`. 같은 권위 파일이 여러 독립 본문의 근거이면 같은 파일을 여러 source ID로 연결할 수 있음 |
| `artifacts` | 아래 7개 역할의 실제 파일 참조 |
| `reports` | 아래 구조/저장본/Word 렌더 3개 보고서 참조 |
| `reviews` | 실제 검수 JSON 파일 참조 배열 |
| `user_feedback` | 사용자 추가 요청 접수 시 필수: 현재 원장 ledger와 요청별 독립 확인서 review의 파일 참조. 확인 전에는 review 생략·대기 |

artifacts의 7개 역할은 `manuscript`, `plan`, `contract`, `docx`, `pdf`, `learning_final`, `assessment_final`이다. contract 경로는 해당 package.root의 `assets/layout-contract.json`과 같아야 한다. 각 역할은 서로 다른 파일을 가리킨다. 두 FINAL TXT는 독립 검수의 수정이 현재 공통 원고로 반영된 다음 `export_handoff.py`가 내보낸 전체 내용과 같아야 한다. 파일명만 FINAL로 바꾸거나 해시만 새로 써 넣어도 내용 불일치는 통과하지 않는다.

원고의 source.provenance.sha256과 실제 source 파일을 대조한다. 기계 검사는 source.text가 그 PDF/이미지의 정확한 전사인지 판단하지 않으므로 별도 source 검수 증거가 필요하다.

## 기계 검사 보고서

눈검수 후 추가 요청은 [후속 검수](user-feedback.md)의 원장·확인서로 검사한다. 출고 기록 폴더에 `사용자수정요청.json`이 있으면 user_feedback 누락이나 옛 보관 원장 연결을 차단한다. 미반영·미확인 요청, 조건 누락, 자기확인, 현재 원장/산출물과 다른 확인서는 새 출고를 통과하지 못한다. 기존 S/L/M/N/J/K/R은 그대로 요구하며 분할 검수 자식 JSON에 임의 요청 필드를 추가하지 않는다.

추가 요청이 없는 기존/최초 기록은 계속 지원하지만 출력 user_feedback.status=NOT_RECORDED를 사용자 승인으로 읽지 않는다. 기계는 기록하지 않은 채팅을 알 수 없으므로 접수 즉시 기록해야 한다. 원장·확인서는 실제 의미 검수의 대체가 아니며 과거 PASS를 자동 승계하지 않는다.

- `reports.structure`: 현재 `check_book.py`의 실제 JSON 보고서. `input_sha256`이 현재 manuscript의 바이트 SHA와 같고, 상태·수량·원문 복원 결과 등 보고 내용이 재실행 결과와 같아야 한다.
- `reports.saved_docx`: 현재 `check_saved_docx.py`로 **full** 검사한 보고서. 현재 plan/DOCX/contract/reference SHA, 내용 대응, `format_validation=PASS`, 전체 블록 및 서식 결과를 재실행 결과와 대조한다. `targeted` 검사는 출고용 full을 대신하지 못한다.
- `reports.word_render`: 실제 Word 렌더 실행을 보존한 JSON. `status="PASS"`, `renderer="Microsoft Word"`, 실제 `version`, 실제 `execution_id`, DOCX 바이트 `source_sha256`, PDF 바이트 `pdf_sha256`, `source_unchanged=true`, 정수 `pages`를 기록한다. `render_word.ps1` 출력의 renderer/version/pages/source_sha256/source_unchanged를 실제 실행 로그에서 가져오고 생성 직후 PDF 해시와 실행 식별자를 연결한다. 이 파일은 단순히 원하는 값을 적는 확인서가 아니다. PDF의 실제 페이지 수는 pypdfium2로 다시 센다.

현재 원고를 같은 `book_plan.compile_plan(...,'full')`로 다시 계산해 저장 계획과 일치하는지도 검사한다. CLI가 기록한 `input_sha256`이 있으면 현재 원고 바이트와 같아야 한다. 모델이 수정한 임의 계획을 기준으로 DOCX만 일치시킨 것을 정상 생성으로 보지 않는다.

## 실제 검수 기록

각 reviews 참조가 가리키는 JSON에는 다음 필드가 필요하다.

| 필드 | 내용 |
|---|---|
| `id`, `kind` | 중복 없는 기록 ID, `source`/`learning`/`questions`/`word_layout`/`release` |
| `reviewer_id`, `execution_id` | 실제 담당자·에이전트의 안정 ID와 실제 세션·실행·검수 기록 ID. 단순 표시 이름/역할명으로 대신하지 않음 |
| `performed_at`, `method`, `summary` | 실제 검수 시각, 방법, 확인 범위와 결론 |
| `status` | 실제 완료이면 `PASS`, 미실시/실패는 그 상태 그대로 |
| `scope` | 아래 종류별 실제 전체 source/unit/question ID 목록 |
| `bindings` | 아래 종류별 현재 파일/내용 해시 |
| `findings` | 오류가 없으면 빈 배열 `[]`. S/source 전체 기록에 한해 누락 시 아래 `no_findings:true`로 대체 가능. 발견 항목마다 중복 없는 `id`와 `description,status,resolution,recheck`; 출고 전 status는 `resolved`이고 수정·재검증 근거를 적음 |
| `no_findings` | S/source 전체 검수에서만 선택적인 명시 선언 `true`. findings와 함께 쓰면 findings는 빈 배열이어야 하며, 다른 검수 종류의 findings를 대체하지 못함 |

S가 실제 원문 전체를 검수하고 발견 사항이 없으면 `"findings": []`와 `"no_findings": true`는 각각 유효한 기록 방식이다. findings를 생략한 경우에는 반드시 후자를 명시한다. 둘 다 없는 기록, `no_findings:false/1/"true"/null`, findings가 배열이 아닌 기록은 거부한다. findings가 비어 있지 않으면 resolved 항목이라도 `no_findings:true`와 충돌하므로 발견·해결 이력을 보존하고 그 선언을 쓰지 않는다. 중복 JSON 키로 앞의 findings나 status를 덮어쓰는 기록도 거부한다. 검증기는 원본 JSON을 고쳐 빈 배열이나 PASS를 채우지 않는다. S의 실제 담당·실행·시각·방법·요약·현재 해시·전체 범위·완료 상태는 그대로 필요하다.

다음은 발견 사항이 없는 S 기록의 **형식 설명용 합성 예시**다. 예시 ID·해시·근거를 실제 검수 증거로 사용하지 않는다. 기존 방식으로 쓰려면 `no_findings` 대신 `"findings": []`를 둔다.

```json
{
  "id": "example-source-review",
  "kind": "source",
  "status": "PASS",
  "reviewer_id": "example-actual-reviewer",
  "execution_id": "example-actual-review-execution",
  "performed_at": "2026-09-25T00:00:00Z",
  "method": "실제 수행한 원문 대조 방법을 기록",
  "summary": "실제 확인한 원문 범위와 발견 사항이 없다는 결론을 기록",
  "scope": {"kind": "full", "source_ids": ["example-source-id"]},
  "bindings": {
    "package_sha256": "REPLACE_WITH_ACTUAL_PACKAGE_HASH",
    "source_content_sha256": "REPLACE_WITH_ACTUAL_SOURCE_CONTENT_HASH"
  },
  "no_findings": true
}
```

최소 source 1건, learning 1건, questions 2건, word_layout 1건, release 1건이 필요하다. 추가 기록이 있어도 미완료·옛 버전을 그대로 현재 PASS 기록과 혼합하지 않는다. 역사 기록은 별도 보존하고 reviews에는 현재 유효 기록만 연결한다.

scope는 ID를 원고 순서 그대로 나열한다.

- source: `{kind:"full",source_ids:[...]}`.
- learning: `{kind:"full",source_ids:[...],unit_ids:[...]}`.
- questions/word_layout/release: `{kind:"full",source_ids:[...],unit_ids:[...],question_ids:[...]}`.

learning/questions/release는 `independent=true`를 기록해야 하며 제작자와 reviewer_id/execution_id가 달라야 한다. questions의 두 기록은 서로도 두 ID가 각각 달라야 한다. **같은 제작자/한 실행을 두 이름으로 바꾸는 것은 독립 검수가 아니다.** 실제 실행 기록을 바탕으로 기입하고 허위 ID를 만들어 통과시키지 않는다. 기계는 식별자 중복과 증거 연결은 확인하지만 허위로 서로 다른 ID를 적었는지 또는 독립 사고가 실제로 이루어졌는지 알아낼 수 없다.

questions에는 각각 `solved_before_answer_key=true`와 해당 검수자가 실제로 푼 전체 `{문항ID: 최종 확인한 정답 번호}`인 `answers`를 둔다. 먼저 정답을 보기 전 풀이를 수행하고, 대조에서 발견한 오류 및 수정 후 재풀이 결과를 findings에 남긴다. 제작자의 answers를 복사해 독립 풀이로 표시하지 않는다.

현재 구조 검사에서 `independent_length_review_required`에 포함된 문항은 두 questions 기록 각각에 `length_reviews:{문항ID:{status:"PASS",benchmark_ids:[실제비교표본ID,…],rationale:"분량·정보 전개를 실제 비교한 근거"}}`를 둔다. 같은 공유 지문을 쓰는 두 문항도 각 ID를 연결한다. 검토하지 않았거나 너무 짧으면 PASS로 쓰지 말고 범위를 재선정·문항을 재설계한다. 출고 게이트는 누락·미완료 및 다른 표본 연결을 차단하지만 비교 근거의 교육적 타당성 자체를 자동 증명하지 않는다. 제작자의 분량 메모를 복사하여 독립 검수라고 표시하지 않는다.

word_layout에는 `renderer="Microsoft Word"`, `pages_reviewed=[1,2,...마지막쪽]`, 수정·밀집 페이지 등 실제 상세 확인한 `detail_pages`를 기록한다. 렌더 성공은 시각 검수의 대체가 아니다. pages_reviewed는 전 페이지 축소본 확인이며 detail_pages는 원본 크기 상세 확인을 뜻한다.

## 검수와 변경 범위의 해시 연결

현재 버전에서 담당 범위를 나눈 기록은 아래 분할 형식으로 검증할 수 있다. 과거 기록의 해시만 새 값으로 바꾸는 자동 승계 기능은 제공하지 않는다. 필수 단계 해시가 바뀌면 해당 현재 버전의 실제 검수 근거를 확보한다.

`verify_release.content_digests(원고객체)`는 source/learning/assessment의 정규 JSON 지문을 계산한다. source는 metadata/sources/paragraphs/grouping_resolutions, learning은 source+sentences+워크북 필드를 제외한 units, assessment는 learning+전체 units+assessment+question_sources다. 후속 문제나 조판이 추가되어도 이미 검수한 학습 내용이 그대로이면 learning 지문은 유지된다. 해당 내용이 바뀌면 그 검수를 재수행·수정부 재검증해야 한다. 단순히 새 지문으로 덮어쓰지 않는다.

| 검수 종류 | bindings의 필수 키 |
|---|---|
| source | `package_sha256`, `source_content_sha256` |
| learning | `package_sha256`, `learning_content_sha256`, `learning_final_sha256` |
| questions | `package_sha256`, `assessment_content_sha256`, `learning_final_sha256`, `assessment_final_sha256` |
| word_layout | `package_sha256`, `plan_sha256`, `contract_sha256`, `docx_sha256`, `pdf_sha256` |
| release | `package_sha256` 및 artifacts 7개 역할의 `역할명_sha256` 모두 |

여기의 파일 역할 SHA는 **그 파일 바이트의 SHA**다. check_saved_docx 보고서의 `plan_sha256`은 해당 검사기의 canonical plan SHA이며 파일 바이트 SHA와 형식이 다를 수 있다. 출고 기록은 artifact.plan의 바이트 SHA를 사용하고 saved_docx 보고서는 새 검사와 별도로 비교하므로 두 값을 바꿔 적지 않는다.

## 실행 순서와 예시

추가 준비 도구와 분할 검수 운영은 [입력 절약](review-efficiency.md)을 따른다. 기본 전체 FINAL 생성·독립 검수·출고 절차는 유지한다.

아래 경로·ID·0으로 된 해시는 **형식 설명용 합성 예시**다. 실제 교재 검수 완료 기록이 아니며 이대로는 출고 검증을 통과하지 않는다. PASS/independent/검수자 값을 채우기 전에 실제 작업을 수행해야 한다.

```json
{
  "schema_version": 1,
  "scope": "full",
  "producer": {"reviewer_id": "example-producer", "execution_id": "example-production-run"},
  "package": {"root": "../gyogwaseo-unified", "files": {}, "sha256": "REPLACE_WITH_ACTUAL_PACKAGE_HASH"},
  "sources": [{"id": "src1", "path": "원문.pdf", "sha256": "REPLACE_WITH_ACTUAL_SHA256"}],
  "artifacts": {
    "manuscript": {"path": "원고.json", "sha256": "REPLACE_WITH_ACTUAL_SHA256"},
    "plan": {"path": "역할계획.json", "sha256": "REPLACE_WITH_ACTUAL_SHA256"},
    "contract": {"path": "../gyogwaseo-unified/assets/layout-contract.json", "sha256": "REPLACE_WITH_ACTUAL_SHA256"},
    "docx": {"path": "교재_통합교재.docx", "sha256": "REPLACE_WITH_ACTUAL_SHA256"},
    "pdf": {"path": "교재_통합교재.pdf", "sha256": "REPLACE_WITH_ACTUAL_SHA256"},
    "learning_final": {"path": "교재_FINAL.txt", "sha256": "REPLACE_WITH_ACTUAL_SHA256"},
    "assessment_final": {"path": "교재_문제_FINAL.txt", "sha256": "REPLACE_WITH_ACTUAL_SHA256"}
  },
  "reports": {
    "structure": {"path": "전체연결검사.json", "sha256": "REPLACE_WITH_ACTUAL_SHA256"},
    "saved_docx": {"path": "저장본검사.json", "sha256": "REPLACE_WITH_ACTUAL_SHA256"},
    "word_render": {"path": "Word렌더실행.json", "sha256": "REPLACE_WITH_ACTUAL_SHA256"}
  },
  "reviews": []
}
```

패키지 지문은 다음 명령으로 읽어 package.files/sha256에 넣는다. 표준 출력 저장 파일은 스킬 밖에 둔다.

```text
python scripts/verify_release.py --fingerprint 스킬폴더
python scripts/check_book.py 원고.json 전체연결검사.json
python scripts/book_plan.py 원고.json 역할계획.json --scope full
python scripts/check_saved_docx.py 역할계획.json 교재_통합교재.docx 저장본검사.json --scope full
python -m pip install -r requirements-visual.txt
python scripts/verify_release.py 교재_출고기록.json 교재_출고검증.json
```

이 명령 사이의 실제 DOCX 생성/부분 수정, FINAL 반영, 독립 검수와 Word 렌더·시각 확인은 workflow에 따라 실행한다. 위 명령만 실행하여 미수행 검수를 완료로 만들 수 없다. 실패·대기 항목을 실제로 해결한 뒤 현재 기록으로 재검사하며, 원고·계획·DOCX/PDF가 바뀌면 옛 검사 보고서를 재사용하지 않는다.


## 2026-09-24 맞춤 편성 완료 보고

사용자가 요청한 맞춤 편성(custom)도 실제 요청 범위 전체와 필요한 검수를 완료하면 기존 READY_FOR_RELEASE 판정을 사용할 수 있다. 다만 검사 결과와 완료 보고에 ‘맞춤 편성’, 실제 워크북 문항 수·모의고사 회차별 문항 수, 원고에 기록된 사용자 요청 근거를 함께 표시한다. 표준 편성(full)과 구별하며 기본 3회 편성을 통과한 것으로 보고하지 않는다. 여기서 전체 출고 scope full은 요청한 교재 전체의 완료 범위이고 assessment.scope.kind의 표준/custom 편성과 별개다. partial은 계속 전체 출고를 허용하지 않는다. 이 보고 구분으로 내용·Word·독립검수 조건을 줄이지 않는다.

## 현재 버전의 분할 검수 기록

이 형식은 추가 선택지이며 기존 실제 전체 검수 기록도 계속 지원한다. 분할 검수 범위를 `full`로 바꾸거나 가상의 총괄 reviewer_id를 붙이지 않는다. 검증 후 집계에는 실제 자식 기록의 ID·경로·해시·담당자·실행·범위를 `review_contributors`로 남긴다. 과거 PASS의 자동 승계·부분 재검만으로 FINAL 인증은 지원하지 않는다.

`reviews`에서 참조하는 묶음 JSON의 필드는 다음과 같다. 미구현 임의 필드는 허용하지 않는다.

- 공통: `schema_version:1`, `type:"review_bundle"`, 실제 고유 `id`, `kind`, `role`, `summary`, 현재 단계 `bindings`, 원고 순서의 현재 전체 `scope`, `children:[{path,sha256},…]`.
- 학습: `kind:"learning", role:"L"`, 추가 `continuity:{path,sha256}`. 전체 scope는 source_ids·unit_ids.
- 문제: `kind:"questions", role:"M"` 묶음과 `role:"N"` 묶음을 별도로 둔다. 각각 전체 scope는 source_ids·unit_ids·question_ids. 분할 방식을 쓰는 출고 기록에서 기존 전체 문제 기록과 혼용할 때도 기존 기록에 실제 `role:"M"` 또는 `"N"`을 명시한다. 두 그룹 사이 모든 실제 reviewer_id·execution_id 집합이 서로 달라야 한다.
- 조판: `kind:"word_layout", role:"JK"`, 추가 현재 PDF의 정수 `pdf_pages`. 전체 scope는 source_ids·unit_ids·question_ids.
- S/source와 R/release는 묶음으로 대체하지 않고 기존 전체 실제 기록을 유지한다.

자식 JSON은 `schema_version:1`, `type:"review_shard"`와 기존 실제 검수 기록의 `id,kind,role,status,reviewer_id,execution_id,performed_at,independent,method,summary,bindings,findings`를 갖춘다. 실제 검수한 현재 파일만 PASS로 적는다. `independent:true` 및 제작자와 다른 실제 ID·실행을 요구한다. 자식의 모든 필수 단계 해시를 현재 입력과 대조하고 파일 바이트 해시도 확인한다. 중첩 묶음·같은 실행의 중복 사칭은 허용하지 않는다.

| 자식 종류 | 실제 소유 scope 및 추가 필드 |
|---|---|
| L | `scope:{kind:"partial",source_ids:[…],unit_ids:[…],sentence_ids:[…]}`. 단위마다 문장을 모두 포함하고 전 단위를 중복·누락 없이 배정 |
| M/N | `scope:{kind:"partial",question_ids:[…]}`. 소유 범위의 실제 `answers`, `solved_before_answer_key:true`, 기존 형식의 `length_reviews` 필수. 같은 공유 장문 문항은 한 자식이 함께 소유. 각 M/N 묶음이 각각 전 문항 커버 |
| J/K | `scope:{kind:"partial",pages:[…]}`, 같은 목록의 `pages_reviewed`, 실제 `detail_pages`, 문맥만 보는 `context_pages`, `renderer:"Microsoft Word"`, `boundaries:[{pages:[p,p+1],status:"PASS",summary:"실제 연결 확인"},…]`. 현재 전 페이지를 중복·누락 없이 소유하며 각 인접 쪽 연결에 최소 한 건의 유효한 실제 관찰을 기록 |

L/M/N에서 선택적인 `context`에는 해당 scope의 ID 목록을 문맥용으로 둘 수 있다. context는 완료 범위가 아니다. J/K는 context 대신 context_pages만 쓴다. 페이지 경계 담당자는 양쪽 페이지를 실제 소유/문맥 범위에서 보고 적어도 한 쪽을 소유해야 한다. 실제 J와 K의 담당자·실행은 다르며 두 역할을 유지한다.

J/K 경계 배정 예: 앞 묶음(1~10쪽)이 11쪽을 context_pages로 보고 10/11을 맡거나, 뒤 묶음(11~20쪽)이 10쪽을 문맥으로 보고 맡을 수 있다. 서로 다른 실제 reviewer_id와 execution_id를 가진 두 담당자가 각각 그 경계를 독립 관찰했다면 양쪽 원본 기록을 유지하고 유효한 중복 관찰로 받는다. 각 관찰은 양쪽 페이지 접근·최소 한 쪽 소유·인접한 현재 정수 페이지·판정·구체적 요약을 갖춰야 한다. 같은 receipt에 동일 경계를 두 번 적거나 같은 실제 검수자 또는 실행의 관찰을 반복하는 것은 거부한다. J와 K의 실제 담당자·실행 독립성 및 페이지 소유의 중복 금지는 그대로다.

예를 들어 J의 `scope.pages:[1,2]`, `context_pages:[3]`와 K의 `scope.pages:[3,4]`, `context_pages:[2]`에 각각 `boundaries`의 `{pages:[2,3],status:"PASS",summary:"각 담당자가 실제 확인한 연결 근거"}`를 둘 수 있다. 각자의 나머지 필수 필드와 1/2·3/4 경계 확인도 필요하다. 집계의 `boundaries_reviewed`는 `[[1,2],[2,3],[3,4]]`이며 2/3을 두 건의 완료 범위로 세지 않는다. 각 `review_contributors`에는 그 담당자의 `boundaries_reviewed`와 원본 ID·경로·바이트 해시·실제 담당자·실행이 남는다. 하나라도 PASS 이외 상태이거나 서로 판정이 다르면 PASS 집계를 만들지 않는다. 원본 기록을 병합·수정하여 불일치나 PENDING을 지우지 않는다.

L의 continuity 파일은 `type:"learning_continuity",kind:"learning",role:"L"`과 실제 자식 공통 검수 필드, 현재 전체 source_ids·unit_ids scope를 갖춘다. 실제 담당자가 전 단위의 용어·지시·흐름·연결을 검수한 근거다. 한 L 담당자가 이 역할도 수행할 수 있지만 같은 execution_id에 다른 reviewer_id를 붙일 수 없다. 기계 집계를 사람의 전체 연결 검수로 보고하지 않는다.

## R 준비 보고서 연결

`check_release_text.py`는 기존 정밀 대조를 재사용하고 PDF 진단 등을 짧게 기록한다. 출력은 항상 `NOT_CERTIFIED`다. 선택적인 `reports.release_text`에 실제 `{path,sha256}`로 연결하면 출고 검사기가 같은 현재 파일로 다시 생성·대조한다. 보고서의 입력/패키지 해시·내용이 다르면 FAIL이며 기계 대조 실패도 유지한다. 기존 필수 structure·saved_docx·word_render와 실제 R은 그대로 필요하다.

경고가 있으면 현재 실제 R 기록에 `release_text_dispositions:{경고ID:{status:"resolved",resolution:"실제 판단/수정 근거",recheck:"현재 파일 재확인 근거"}}`를 남긴다. 미해결·미확인은 REVIEW_PENDING이다. 단지 통과시키려고 resolved를 적지 않는다. PDF 추출 오류가 실제 인쇄 오류인지 화면에서 확인하고, 문구나 폰트를 자동 바꾸지 않는다. 도구가 PDF를 읽지 못해도 Word/J/K/R 미실시를 면제하지 않는다.

```text
python scripts/review_preflight.py 원고.json 제작자진단.json
python scripts/export_handoff.py 원고.json --review-packet L입력.json --review-role learning --unit-id 실제단위ID
python scripts/export_handoff.py 원고.json --review-packet M블라인드입력.json --review-role questions-blind
python scripts/export_handoff.py 원고.json --review-packet 변경부대조.json --review-role questions-compare --baseline 이전원고.json --changed-only
python scripts/check_release_text.py 원고.json 역할계획.json 교재.docx 교재.pdf 교재_FINAL.txt 교재_문제_FINAL.txt R준비.json
```

위 검수 자료 생성은 실제 독립 검수 실행이 아니다. 새 출력 파일명만 사용하고 스킬·입력·기존 FINAL·교재를 덮어쓰지 않는다. 합성 시험 데이터/예시 ID는 실제 출고 증거에 쓰지 않는다.
