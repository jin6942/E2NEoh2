# 공통 실행과 검증 계약

[공통 원고 데이터](manuscript-data.md)로 원문·학습 단위·각주·워크북·문항을 연결하는 상위 JSON 검사기, MASTER 역할 조립기, QC TXT 내보내기를 구현했다. 기존 자유 형식 TXT의 자동 역변환은 구현하지 않았으며 실제 내용을 대조해 공통 데이터에 이관한다. 표시용 빗금·기호를 파싱해 검수된 원문 위치를 추정하지 않는다.

## 플랫폼 공통

S-7 후속 승인 글꼴 예외는 `assets/layout-contract.json`의 `circled_number_typography`다. `master_docx.RoleBank.paragraph`가 관리 문단의 ①~⑤만 맑은 고딕으로 지정한다. 나머지 글자·서식·MASTER 자산은 보존한다. 지정 글꼴이 없으면 환경 미충족으로 기록하고 임의 대체 글꼴을 동일 출력으로 보고하지 않는다. 글꼴 파일은 패키지에 넣지 않는다.

내용은 `editorial-core.md`와 각 참조, 디자인은 `assets/latest-approved-reference.docx`와 `assets/layout-contract.json` 한 벌을 사용한다. Claude·ChatGPT·Codex용 별도 규칙 사본을 만들지 않는다. 실행 환경에서 작업 폴더·Python 실행기·파일 저장 방법을 확인하고, `/mnt/data`·특정 사용자 Windows 경로·특정 Node 설치 위치가 있다고 가정하지 않는다.

공통 생성·구조 검사기는 Python이다. 표준 라이브러리 외 DOCX 역할 생성 및 저장본 검사는 lxml을 사용한다. 현 검증 환경은 Python 3.12.14, lxml 6.1.1, Word 16.0, 이미지 확인은 pypdfium2 5.13.0이다. 이 목록은 실제 시험 환경이며 다른 버전에서도 이미 동등하게 검증했다는 뜻이 아니다. 내장 Microsoft 글꼴을 임의로 재배포하지 않는다. 맑은 고딕·Times New Roman의 실제 가용성을 확인하고, 대체 글꼴로 만든 결과는 승인 MASTER의 동일 조판으로 확정하지 않는다.

공통 DOCX가 생성되어도 조판 검수는 별도다. Word에서 내보낸 PDF를 마지막 페이지 경계 확인에 사용한다. 다른 엔진의 렌더는 예비 확인으로 기록한다. Word에 접근하지 못한 환경에서는 내용·DOCX 구조 검사까지 진행할 수 있지만 Word 최종 조판 검수는 미실시로 남긴다. 실제로 실행하지 않은 플랫폼 비교·독립 검수를 통과로 표시하지 않는다.

## 데이터의 권위와 위치

권위 원문 파일과 전사 텍스트를 구별한다. 전사에는 원본 파일 해시·쪽·본문 영역·판본과 확인 기록을 연결한다. 원문의 제목·소제목·단락·문장 경계를 확인한 뒤 안정적인 ID를 부여한다. 도구가 ID를 부여했다고 원문 OCR 정확성이나 문장 경계가 검증된 것은 아니다.

모든 `start`/`end`는 0부터 시작하는 Unicode 코드 포인트 인덱스이며 끝 위치는 제외한다. Python 문자열 슬라이스와 같다. UTF-8 바이트 위치 및 JavaScript의 UTF-16 인덱스를 그대로 쓰지 않는다. 위치가 독립 본문 전체 기준인지 문장 내부 기준인지 아래 계약으로 구별한다. 원문을 정규화한 뒤 옛 위치를 재사용하지 않는다.

각주·청크·문항 정보를 출력 문자열의 `/`·`—`·원숫자로 분해해서 되찾지 않는다. 구조화 데이터에서 표시 문자열을 만들고, 원문에 실제로 포함된 같은 기호는 보존한다.

## 현재 도구별 입력과 한계

| 도구 | 입력·출력 | 확인하는 것 | 확인하지 않는 것 |
|---|---|---|---|
| `check_learning_content.py` | 공통 원고 → 학습 연결 검사·표시 S/V·분석 본문 | 실제 전사와 주석·단위·각주 위치·★·워크북·수량 예외 연결 | 외부 원본 파일의 진위·어휘 수준 분류·번역·유반 의미 |
| `check_book.py` | 공통 원고+assessment+question_sources → 전체 연결 검사 | 학습 연결·편성·문항 원문 복원과 실제 원고·답안 연결 | 문항 의미적 타당성·독립 풀이·실제 DOCX |
| `book_plan.py` | 공통 원고 → 전체/학습 단계 MASTER 역할 계획 | 실제 원고의 섹션·각주·핵심·문항 표시·해설을 해당 역할에 연결 | Word 페이지 경계·계속 제목의 자동 위치 판정·내용 정확성 |
| `build_book.py` | 공통 원고 → 누적 DOCX·정규 계획·저장본 검사 보고서 | 최초 생성 또는 같은 파일의 변경 블록/새 블록만 반영, 저장본 재검사, 이전 해시·비대상 보존 | 독립 내용 검수·Word 시각 검수·최종 출고 승인 |
| `export_handoff.py` | 공통 원고 → 해석분석/문제 QC TXT | 동일 원고에서 모든 내용 파생·저장 후 재열람·기존 파일 해시 | 독립 검수 완료·FINAL 승인·수정된 TXT의 자동 역변환 |
| `learning_units.py` | paragraphs: id/source_id/subheading_id/sentence_ids → 공통 단위 또는 확인 대기 | 6문장 기준·소제목 전체 묶기·중복·순서 | 실제 원문 경계, 소제목 없는 짧은 단락의 사용자 판단 |
| `analysis_body.py` | sentences: source_id/id/text/chunks(start,end,ko)/natural_ko, units: source_id/sentence_ids → 문장별 세 줄 | 영어 문자 범위·영한 청크 수·자연 해석 존재·전체 순서 | 번역 정확성·문법·단어 뜻 |
| `sv_line.py` | original, clauses: kind/start/marker/subject_spans/verb_spans 및 선택 subject_display_spans/subject_display_review → 공통 S/V 문자열 | 전체 주어 보존과 표시 범위 계약·원문 범위·기호·절 순서 | 영어 구문 자동 분석, 표시 축약의 문법 타당성, 누락된 절 탐지 |
| `question_source.py` | source: id/text/sentences(id,start,end), question: type/source_id/first_sentence/last_sentence 및 유형별 변형 → 표시 지문·복원 근거 | 연속 원문·문장 경계·동학년 동유형 공식 분량 비교 기록·허용된 변형 복원 | 유일정답·내용 적합성 |
| `check_answer_links.py` | scope/plan/questions/quick_key/explanations → 대응 검사 | 문항 ID·회차별 번호·수량·답·다섯 선지·번역·네 오답 설명의 존재와 대응 | 정답의 의미적 타당성·독립 풀이·DOCX 실재 |
| `master_docx.py` | blocks(id,elements) 역할 계획 → 신규 DOCX 또는 같은 파일 부분 수정 | MASTER 해시·역할 위치·변경 대상·비대상 보존·저장 직전 해시 | 원고 전체 구성의 완결성·번역·문항 정확성·시각 조판 |
| `check_saved_docx.py` | 역할 계획·실제 저장 DOCX → 내용·서식 대응 보고서 | 블록·글자·줄바꿈, 스타일 상속을 반영한 문자 구간/문단 서식, 표·셀·구역·푸터, 계획/계약/MASTER 해시 | 실제 폰트 설치·Word 좌표/쪽 흐름·문항 정답 의미 |
| `verify_release.py` | 실제 출고 기록 → READY_FOR_RELEASE/REVIEW_PENDING/FAIL | 현재 원고에서 다시 컴파일한 계획, 실제 저장본 재검사, 패키지 전체 파일 지문, 원문·FINAL·독립 검수·Word 검수의 해시/범위 연결 | 검수자의 사고·허위 기록 진위, 원문의 의미·문항 정답을 대신 판단 |

각 실행기의 `--help`와 파일 맨 앞 계약을 먼저 확인한다. 입력 파일을 출력 파일로 덮어쓰지 않는다. 실제 원고에서 입력을 파생하고 해시·범위를 기록한다. 검사기로 넣을 입력을 일부만 만들어서 전체 검수라고 부르지 않는다.

`build_book.py`와 Word 렌더는 호출자가 지정한 출력 경로를 사용하며 전달용 이름을 자동으로 정하지 않는다. 제작 담당이 [파일명 규칙](workflow.md#파일명과-플랫폼별-저장)에 맞는 DOCX/내부 PDF 경로를 지정하고 저장본·출고 기록·제공 링크를 대조한다. 최종 출고는 [분권 절차](split-delivery.md)의 `split_book.py`로 전체통합본 사본과 다섯 분권·ZIP·내부 목록을 만들고 `verify_split_release.py`로 여섯 파일의 실제 출고 연결을 확인한다. PDF는 검수에 사용하되 기본 제공 링크는 DOCX 6개가 들어 있는 ZIP 1개다. 코드의 확장자/해시 통과를 모든 파일명 규칙 준수로 보고하지 않는다. 기존 파일의 patch 경로·임시 시험 파일·내부 인계 파일에 전달용 이름을 일괄 강제하지 않는다.

`check_answer_links.py`의 full은 확인된 정식 과목명으로 편성을 검사한다. 영어II(영어2)는 7문항×3회, 공통영어1·2와 그 밖의 고등 영어 교과서는 기존 기본값 5문항×3회를 적용한다. 과목명이 확인되지 않았으면 먼저 권위 원문으로 식별하며, 이름이 없는 입력을 표준 편성으로 통과시키지 않는다. 사용자 지시나 현재 교재의 승인 편성이 다르면 근거를 기록한 custom을 사용한다. partial/custom은 요청 근거를 남기고 표준 전체 출고 판정과 구별한다.

## 역할 계획과 실제 DOCX

해석지의 교재명·출처 표시는 공통 표시 계산에서 파생하여 `book_plan.py`와 `export_handoff.py`가 같은 정규화 결과를 쓴다. 교재명은 정규화한 과목과 출판사/저자를 공백으로 연결하며 자유 `book_name`을 표시 기준으로 사용하지 않는다. 알려진 민병천 능률 별칭과 `교과서 본문/본문`만 [입력 계약](manuscript-data.md#해석지-헤더의-표시-정규화)에 따라 통일한다. 원고의 식별값·원문·다른 출처명은 유지한다. `units[].hook`이 남아 있어도 노란 질문과 `[흥미 훅]`은 DOCX·FINAL 인계에 출력하지 않으며 hook 누락은 오류가 아니다. 첫 단위의 공통 안내와 기존 MASTER/계약의 서식은 유지한다.

`blocks`는 출력 순서의 배열이다. 각 블록은 안정적인 id와 elements를 갖는다. 문단 요소는 `role`, `runs:[{run:원본run번호,text:새내용}]`로 구성한다. 이는 공통 컴파일러의 내부 출력 형식이며 모델이 임의로 구성하는 두 번째 제작 경로가 아니다. `book_plan.py`로 실제 공통 원고에서 생성한다. 글꼴·크기·색을 임의로 입력하는 필드는 없다. 원고의 핵심 표시·청크 번호·별표는 고정 코드가 맞는 역할에 연결한다. 본문 대신 MASTER 예문을 복제하지 않는다. 첫 공통 안내는 계약의 `guide_runs`로 수동 줄바꿈까지 보존한다.

표 요소는 `kind:table`, `role`, `entries`를 갖는다. 표지 주제 박스는 결합한 영어 제목·한국어 제목 두 문단이며, 워크북 뜻 쓰기 표는 영어 셀+필기 셀 두 쌍을 반복한다. 홀수 낱말의 마지막 남은 칸도 동일 서식의 빈 칸으로 둔다. 단어를 뜻 셀에 미리 채우지 않는다.

최초 create는 기존 출력 파일을 거부한다. 후속 patch는 최신 DOCX의 `--expected-sha256`과 수정할 블록을 요구한다. 새 블록은 기존 블록의 `insert_before` 또는 `insert_after` 하나로 위치를 명시한다. 기존 블록을 이동하거나 내용 삭제를 빈 블록으로 가장하지 않는다. 자동 태그가 없는 기존 사용자 문서는 실제 구조를 대조해 매핑한 후 필요한 최소 수정으로 처리하며 전체 재생성을 우회 방법으로 쓰지 않는다.

저장 뒤 `check_saved_docx.py`를 실행한다. full은 전체 블록 순서·예기치 않은 본문과 역할 서식을 검사한다. targeted는 수정 블록의 범위를 명시하며 전체 검수로 보고하지 않는다. Word의 동일 서식 run 분할·병합은 허용하지만 번호 강조를 본문 전체에 복사한 결과는 실패해야 한다. 내용 일치 상태와 `format_validation=PASS`를 모두 확인한다. 보고서는 실제 DOCX·정규 계획·계약·MASTER SHA-256에 연결한다. 실제 페이지 잘림·고립은 Word 시각 검수로 따로 확인한다.

문항 대응 검사 입력은 원고 또는 저장본에서 각각 확인한다. 한 JSON을 세 번 복제해 문제·정답표·해설 입력을 채웠다면 그 검사는 원고 내부 대응만 입증한다. 저장본 내용 일치 검사와 실제 PDF 확인을 별도로 수행해야 한다.

## 내용에서 파일까지 실행

```text
python scripts/build_book.py 원고.json 교재_통합교재.docx 역할계획.json 제작검사.json --scope full --mode create
python scripts/export_handoff.py 원고.json --learning 교재_QC_HANDOFF.txt --assessment 교재_문제_QC_HANDOFF.txt
```

위 create는 최초 파일에만 사용한다. 이미 진행 중인 파일에는 아래처럼 현재 DOCX 해시와 새 계획/보고서 경로를 사용해 patch한다. build_book은 정규 전체 순서에서 변경한 블록과 새 블록을 찾아 필요한 앵커로 반영한다. 이전 단계의 비대상 내용은 유지한다. 관리되지 않는 기존 내용·삭제·이동·문서 전체 서식 손상은 임의 재생성하지 않고 오류로 남긴다. 전체 요청에서도 독립 검수·최신 FINAL 등 workflow의 단계 조건을 실제로 충족하며 진행한다. 성공 상태 BUILT_NOT_FINAL은 출고 승인이 아니다. 최종 단계는 [출고 기록](release-record.md)을 실제 증거로 구성하고 `python scripts/verify_release.py 교재_출고기록.json 교재_출고검증.json`을 실행한다.

```text
python scripts/build_book.py 최신원고.json 교재_통합교재.docx 전체역할계획.json 전체제작검사.json --scope full --mode patch --expected-sha256 현재DOCX해시
```

해석·분석 단계는 build_book의 `--scope learning`과 export_handoff의 `--learning`만 사용한다. 문제 원고가 아직 없는 단계에서도 해석·분석을 같은 DOCX에 먼저 반영할 수 있다. 후속 전체 계획을 만들었다고 기존 DOCX를 create로 다시 만들지 않는다. 최신 해시를 확인하고 build_book의 patch로 이어가며 표지의 수록 범위·실제 수량도 단계에 맞춰 갱신한다. book_plan/master_docx/check_saved_docx는 이 경로의 내부 도구이며 개별 디버깅도 가능하나, 모델이 별도 역할 계획을 창작해 정규 컴파일러를 우회하지 않는다.

book_plan은 cover의 lesson_label/lesson_number/topic_first/topic_ko와 선택 topic_second, 독립 본문의 label, 모의 회차별 set_labels를 실제 원고에서 입력받는다. 과 식별자는 metadata와 cover가 같아야 하며 본문·정답 제목은 ‘3과’로 파생한다. cover의 과 라벨·번호는 검증 입력으로 유지하되 학생용 표지의 독립 라벨·큰 번호로 출력하지 않는다. 표지에는 기존 로고, `혼공교재 독해편`, 과목명만의 큰 제목, `metadata.publisher_author · 확인된 과 표시` 순서로 배치한다. 예를 들어 `공통영어2` 다음 행은 `NE능률(민병천) · 4과` 또는 `NE능률(민병천) · Special Lesson 1`이다. 과 숫자 앞의 0과 과·교재명 중복을 만들지 않으며 기존 주제 박스·수량·학습 단계는 유지한다. 기존 MASTER 과·제목을 기본값으로 복사하지 않는다. 작성 제목/주제는 해석지·워크북에서 영문과 한국어를 한 문단으로 결합하고 종류는 계획의 heading_kind로 보존한다. 원문 소제목은 source.subheadings의 원문·위치를 사용한다. 소제목 원문이 없는 ID만으로 제목을 창작하지 않는다. 고정 안내문·소제목·기호는 계약에서 가져온다. 밑줄과 번호·영어·해석의 서식은 해당 역할 구간으로 구분한다.

Special Lesson은 `source_contract.lesson_identity`의 `kind:"special"`·`internal_id:"SL01"`·`display:"Special Lesson 1"`을 그대로 사용한다. 일반 과는 `kind:"lesson"`이며 기존 `UNIT03`·`3과` 표시를 유지한다. `metadata.lesson: "Special Lesson 1"` 또는 내부 입력 `SL01`, `cover.lesson_label: "SPECIAL LESSON"`·`cover.lesson_number: "01"`이 같은 종류와 번호를 가리키게 한다. 이 내부 cover 필드를 지우거나 바꾸어 출력 중복을 해결하지 않는다. 학생용 표지는 출판사·저자 행에 `Special Lesson 1`을 한 번만 표시한다. 본문·정답·인계 표시를 숫자만 뽑아 `1과`로 다시 만들지 않는다. 과목 정규화·학년별 문항 수와 분량 기준은 최신 `course_policy`를 계속 따른다. Special Lesson용 썸네일 변환은 지원하지 않으며 기존 썸네일 도구를 이 용도로 임의 수정하지 않는다. 이번에 별도 승인된 공통 표지 역할 갱신은 정규 과와 Special Lesson에 같은 MASTER·계약을 적용하는 좁은 예외다. 다른 MASTER 역할·원본 로고 PNG·썸네일·푸터는 보존한다.

Word 렌더에서 워크북이 넘치는 경우, 현재 원고 해시에 묶인 layout_adjustments에 실제 페이지와 계속 표기 직전 anchor를 기록한다. 현재 어댑터는 워크북 핵심 문장의 `key/문장ID` 앞 계속 제목을 지원한다. `kind:question_page_break`는 `question/문항ID` 또는 `passage_group/그룹ID` 앞 새 쪽을 지원한다. 현재 쪽에서 공유 지문·연결 문항·선지가 갈라지되 새 한 쪽에는 전체가 들어가면 장문 자식 문항만 분리하지 않고 공유 지문 그룹을 이동한다. 새 한 쪽에도 들어가지 않으면 크기·간격을 압축하지 말고 실제 배치와 함께 판단을 요청한다. 이 기록은 content_sha256, renderer:Microsoft Word, observed_page, reason, block_id, before_anchor를 필요로 하며 실제 관찰 없이 만들어 넣지 않는다. 표·문항 중간 등 지원하지 않는 경계가 실제로 필요하면 위치와 영향을 보고하고 공통 컴파일러·검사기의 지원을 함께 보완해야 한다. DOCX만 별도 코드로 고쳐 정규 계획 검사를 우회하지 않는다. 그 문제가 해결되기 전에는 Word 조판을 완료로 판정하지 않는다. 모든 넘침 위치를 자동 판단한다고 보고하지 않는다. 계속 표기 때문에 원고가 바뀌면 재렌더하며 옛 원고의 배치 결정을 무조건 재사용하지 않는다.

해설의 오답 네 항목은 마지막 항목에서만 다음 문단 연결을 끊는다. 긴 실제 해설이 한 페이지를 넘으면 의미 있는 경계와 계속 표기를 추가로 확인한다. 한 문항 전체를 한 페이지에 맞추려고 글자를 줄이지 않는다.

TXT를 검수자가 고쳤으면 현재 수정본과 공통 JSON의 필드·문장 ID·원문 위치를 대조하여 수정 내용을 이관한 뒤 TXT와 해당 DOCX 블록을 갱신한다. 이전 JSON으로 검수자의 최신 TXT를 무단 덮어쓰지 않는다. 기존 TXT 갱신에는 --expected-learning-sha256 또는 --expected-assessment-sha256로 현재 파일 해시를 지정한다. 독립 검수가 끝나기 전 QC를 FINAL로 이름만 바꾸지 않는다.

## 검수 상태

학습부 제작 중에는 `review_preflight.py 원고.json 학습진단.json --scope learning`, 전체 제작 후에는 기본 `--scope full`을 쓴다. 학습 범위 결과를 전체 구조검사·출고 근거로 연결하지 않는다. 문항 분량 근거가 필요한 교사용 QC에는 `export_handoff.py 원고.json --assessment 문제_QC_HANDOFF.txt --qc-diagnostics`를 사용하고, FINAL은 그 옵션 없이 생성한다. 블라인드 패킷에는 이 근거를 넣지 않는다.

제작자용 `review_preflight.py`와 R 준비용 `check_release_text.py`는 `NOT_CERTIFIED` 상태의 진단을 만든다. `review_packets.py`는 별도 부분 검수 JSON을 만들며 전체 FINAL을 대신하지 않는다. `review_coverage.py`는 같은 현재 버전의 실제 분할 증거를 `verify_release.py` 안에서 검증한다. 정확한 사용·한계는 [검수 입력 절약](review-efficiency.md) 및 [출고 기록](release-record.md)을 따른다.

원문 확인, 구조 검사, 번역·문법 검수, 문항 독립 2인 풀이, 저장본 내용 대조, Word 조판 검수, 최종 저장본 재열람은 서로 다른 기록이다. 각 기록에는 입력/결과 해시·검수자·범위·발견 오류·수정·재검증을 연결한다. `NOT_PERFORMED`를 빈 문자열이나 자동 PASS로 바꾸지 않는다. 출력 크기·문항 수가 맞는다는 이유만으로 FINAL을 만들지 않는다.

## S/V 축약형 예외 U53

축약형은 S/V에도 원문 형태를 유지한다. 단, `'s`가 has의 축약형이면 `'s(has)`로 병기한다(U53). 예: `It's clear.` → `S: It, V: 's`, `It's changed.`(has changed) → `S: It, V: 's(has) changed`. 곡선 아포스트로피 `’s`도 원문 모양을 유지해 `’s(has)`로 표시한다. is/has는 문맥에서 확인하며 과거분사가 뒤에 있다는 이유만으로 has로 판정하지 않는다. 원문 영어·청크는 바꾸지 않고 표시용 설명을 분리한다.

기계 입력의 각 절에는 동사 범위 안 `'s`/`’s`마다 `contraction_readings: [{span: [start, end], expanded: is 또는 has}]`를 둔다. 실제 JSON의 expanded 값은 문자열이다. 원문 문장 내부의 코드 포인트 위치를 사용한다. 해석을 자동 추정하지 않으며 미확인 항목은 오류로 남긴다. is는 표시를 추가하지 않고 has만 병기한다.

현재 생성에는 `rule_revision:R2026-09-23`와 문장별 새 읽기 판정 기록이 필요하다. 표지의 두 영어 제목 필드는 한 줄로 결합하며 둘째 필드는 생략할 수 있다. 영어2 계열의 표지 표시만 영어2로 통일하고 권위 원문 메타데이터를 바꾸지 않는다. 문제는 일반 한 문단, 장문 공유 본문 한 번, 순서 필수 구획을 공통 컴파일러가 적용한다. 밑줄은 실제 저장 구간으로 검사한다.

## 구조 힌트 표시 입력

일반형 `display_mode:split-phrasal-verb`는 분리 구동사의 중간 목적어만 생략하는 승인 예외다. `display_pairs`는 정확히 1개이며, `display_spans`의 실제 원문 조각 정확히 2개를 ` … `로 연결하고 일반형 대괄호·이름표를 유지한다. 두 조각 사이에는 실제 생략한 원문 글자가 있어야 한다. 예: `[after you throw … away] → [여러분이 버린 후에] (접속사 after)`. 영어 대괄호를 벗긴 값과 두 원문 조각의 연결이 일치해야 하며 생략 목적어는 한국어에도 출력하지 않는다. 짝 구조로 재분류하거나 일반 부사·수식어 생략을 허용하는 기능으로 확대하지 않는다. 정확한 위치·범위는 `manuscript-data.md`를 따른다.

학생용 생성과 FINAL 내보내기에 `hints[].display_pairs`를 사용한다. 일반형은 필요한 구문과 연결 대상만 `영어 → 한국어 해석 (structure_label)` 한 줄로 출력하며 이름표는 끝에 한 번만 붙인다. 절 연결은 연결어와 S′·V′까지만 출력하고 동사 뒤 목적어·전치사 대상이나 일반 명사절 바깥의 means·have found를 덧붙이지 않는다. 주격 관계사는 V′만, be동사는 최소 보어만 예외로 남긴다. 관계사 앞 명사·가주어 It~that 틀과 준동사 등의 한 초점 표시 범위는 `analysis-content.md`를 따른다. 문법 연결 우선으로 선택된 한 초점만 출력하고 안쪽 동사 구문·기능 결합 풀이를 자동 보충하지 않는다. 표시 대괄호는 원문 전체 절의 경계가 아니고 실제 절 판정은 내부 근거에 유지한다. 필요한 복수 쌍은 ` / `로 같은 줄에 연결한다. 짝 구조(`category:paired-structure`)는 display_pairs가 정확히 1개이며 display_spans에 기록한 원문 조각을 순서대로 ` … `로 연결한 영어와 그 부분만 옮긴 한국어를 출력한다. 영어 끝의 ` …`는 필요할 때 허용한다. 짝 구조에는 structure_label·설명문·문장 전체의 완성 해석을 덧붙이지 않는다. 수동·능동 완료의 기능 결합 힌트는 `category:function-combination`, `display_mode:verb-function`에 `lexical_step`을 연결하여 `produced(생산된) → is produced(생산된다) (be p.p.)`, `find(발견하다) → have found(발견했다) (have p.p.)`처럼 한 줄로 표시한다. 왼쪽 낱말 뜻과 오른쪽 실제 동사구 결합 뜻을 구별하며 수동 뜻을 두 번 더하지 않는다. 실제 시제·태·부정·양태와 표시 범위 안의 부사는 보존하고 주어·목적어·A/B 틀·by/for 구는 덧붙이지 않는다. 공식 `formula_label`과 낱말 뜻 괄호는 보통 글씨다. 일반 진행·완료진행 등 이번 p.p. 구별 밖의 기존 힌트와 `what to V + do → 무엇을 해야 할지`는 현행 형식을 유지한다. 기능 결합 display_pairs는 정확히 한 쌍이며, 승인된 lexical_step은 같은 줄의 접두 낱말 뜻이지 추가 대응 쌍이 아니다. 모든 유형은 수동 줄바꿈 없이 작성하며 Word의 자연스러운 줄 감김은 허용한다. `span/meaning_ko/explanation`은 원문 연결·상세 내부 검수 근거이며 학생용 설명문으로 출력하지 않는다. 이전 원고에 필요한 표시 쌍·일반형 이름표·짝 구조의 원문 위치가 없으면 실제 원문을 보고 추가한 후 생성한다. 구형 구조 검사 통과를 새 표시 형식 적용 완료로 보고하지 않는다. 각 표시 쌍의 `emphasis_links`는 같은 문법 기능의 `en_spans`와 `ko_spans`를 연결한다. 영어는 기존 색·한국어는 검정, 둘 다 보통을 기본으로 하며 일반 문법은 링크에 직접 지정한 범위만 양쪽 굵게+한 줄 밑줄로 렌더링하고 아래 명시적 동사 결합 정책만 영어 보통을 적용한다. 영어·한국어 대괄호 전체를 자동 강조하지 않는다. 한국어는 문법 기능이 보이는 직역을 우선하고, 문구 수정 시 양쪽 위치도 다시 맞춘다. 대괄호·7.5pt·문단 간격은 보존한다. 생략 관계사는 `display_mode:omitted-relative`, `omitted_relative`로 표시한다. 실제 문법에 맞는 that/which/who/whom/when/where/why 하나를 관계절 시작에 `(that)`처럼 보충하고, 관계사 글자와 한국어의 최소 대응 부분을 비어 있지 않은 `emphasis_links`로 연결한다. 괄호는 보통 글씨로 유지하며 승인 표지 하나를 제거한 영어가 실제 원문 발췌와 같은지 검사한다. 원문·청크·S/V·각주·정식 해석은 불변이다. 생략 명사절 접속사 that은 관계사와 구별해 `display_mode:omitted-conjunction`, `omitted_conjunction:that`을 사용한다. 힌트에만 `[(that) laws had to be changed] → [법이 바뀌어야 한다고] (명사절 접속사 that 생략)`처럼 표시하고, 괄호는 보통·that 글자와 실제 S′의 이/가 및 연결 어미는 굵게+밑줄로 대응한다. 생략 관계사는 기존 `omitted-relative`를 유지한다. 두 유형 모두 빈 대응 링크로 대체하지 않고 원문·청크·S/V·각주·자연 해석에 보충 표지를 추가하지 않는다. 생략된 주어·to까지 이 예외를 확대하지 않는다. 생략 주어 등 승인 예외 밖에서 실제 대응 짝을 지정할 수 없으면 빈 링크와 내부 `emphasis_note`를 유지하며 임의 보충하지 않는다. 현재 rule_revision의 힌트에서 링크 누락과 `ko_emphasis_spans` 단독 입력은 거부한다. 구형 무표식 읽기 호환을 최신 대응 강조 완료로 판정하지 않는다. 일반형 동사 결합 힌트의 `emphasis_policy:ko-only-verb-construction`은 양쪽 내부 링크를 보존하고 영어 표시만 보통 글씨로 만든다. 일반 문법·관계사·가주어·without/by+ing·짝 구조·기능 결합에는 이 예외를 적용하지 않는다. 선정 공식의 S′/A 주어 조사 이/가는 해당 연결 뜻과 함께 한국어 범위로 기록한다. 정확한 필드는 `manuscript-data.md`를 따른다.


## 2026-09-24 맞춤 편성 완료 보고

사용자가 요청한 맞춤 편성(custom)도 실제 요청 범위 전체와 필요한 검수를 완료하면 기존 READY_FOR_RELEASE 판정을 사용할 수 있다. 다만 검사 결과와 완료 보고에 ‘맞춤 편성’, 실제 워크북 문항 수·모의고사 회차별 문항 수, 원고에 기록된 사용자 요청 근거를 함께 표시한다. 표준 편성(full)과 구별하며 기본 3회 편성을 통과한 것으로 보고하지 않는다. 여기서 전체 출고 scope full은 요청한 교재 전체의 완료 범위이고 assessment.scope.kind의 표준/custom 편성과 별개다. partial은 계속 전체 출고를 허용하지 않는다. 이 보고 구분으로 내용·Word·독립검수 조건을 줄이지 않는다.

독립 p.p. 낱말 힌트의 최신 좁은 예외는 `held — 개최된`의 held와 개최된 전체를 대응 강조하는 것이다. `participle_focus_gloss_id`와 실제 강조 위치를 연결하며 by/without V-ing나 다른 문법으로 확대하지 않는다. 자세한 기준은 `analysis-content.md`와 `manuscript-data.md`를 따른다.

## 분석·워크북 구문 연습 연결

`metadata.syntax_training_version:1`의 분석 기본·보충 항목은 practice의 명시적 공식 지원·기존 낱말 각주 ID·실제 원문 범위·정답을 사용한다. 대상 수동/능동 완료의 formula_routes와 workbook.syntax_point_ids는 manuscript-data.md의 계약을 따른다. 생성기는 뜻이나 빈 연결을 추측해 채우지 않는다. 원 동사 구문의 불필요한 A/B 풀이 또는 contributor to 중 contributor 같은 실제 연습 낱말만 좁혀 지원할 때는 source-bound support_overrides와 검토 기록으로만 적용하며 원 각주는 보존한다. source_span 경로의 form은 실제 원문 낱말 그대로이며 p.p. 임의 원형화에 쓰지 않는다. 구조 검사·역할 계획·TXT가 같은 원고 연결을 읽어 4번 구문 연습과 5번 핵심 문장을 만든다. 구형 표식 없는 원고의 출력 호환은 새 활동 적용 완료가 아니다.

학생용에는 주초점 공식·문맥 뜻을 먼저, 기존 각주에 연결한 필요한 보조 기능·낱말 뜻을 다음으로 지원하고 결합 답은 정답지에만 둔다. 원형으로 좁힌 능동 완료 낱말의 실제 p.p. 관계는 유지한다. 승인된 부분 부정 예외는 실제 범위·승인 근거·원래 분석과 다른 문장 대체 연습을 명시적 route로 연결하며 자동 예외를 추정하지 않는다. 실전문제 뒤 새 쪽4번에 이어5번을 배치하며, 실제 넘침·계속 표제는 Word 관찰과 기존 layout_adjustments 절차로 검토한다. 새 활동의 내용·의미·페이지 적합성은 자동 연결 검사와 별개로 확인한다.
