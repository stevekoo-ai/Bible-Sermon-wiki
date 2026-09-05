# 🧠 성경 연구 및 설교 지식베이스 LLM Wiki 운영 원칙 (v3.2 Kid-Adult Hybrid + Group Sharing)

## 1. 저장소 정체성 및 격리 (Repository Architecture)
- 이 리포지토리는 **학술적 성경 주해(Bible Exegesis)**, **3대지 구조의 설교 아웃라인(Sermon Outlines)**, **신학 자산(Assets)**, 그리고 **목장 나눔(Group Sharing)** 관리를 위한 전용 LLM Wiki입니다.
- 개발 관련 불필요한 파일이나 스크립트를 섞지 마십시오. (단, `scripts/` 내 자동화 스크립트는 허용)

## 2. 어린이 설교 작성의 핵심 철학 (Pedagogical & Homiletical Principles)
- **수준의 깊이 (Adult-Level Depth):** 신학적 내용, 원어 주해, 본문의 핵심 메시지를 아이들이라고 해서 얕게 희석하지 마십시오. 어른 설교와 동일한 엄밀성을 유지합니다.
- **3대지 구조 필수 (Strict 3-Point Structure):** 설교 대지는 반드시 3개의 대지(대지 1, 대지 2, 대지 3)로 명확히 나누어 논리적 완결성을 갖춥니다.
- **시선 집중 도입부 (Focus Hook):** 도입부는 아이들의 주의를 순식간에 사로잡을 수 있는 실물 교안, 시각 자료, 질문, 흥미로운 상황극으로 설계하십시오.
- **생생한 맞춤 예화 (Concrete Illustrations):** 각 대지마다 어린이들의 일상 및 삶과 밀접하면서도 신학적 진리를 정확히 시각화하는 예화(`3_Shared_Assets/Illustrations/`)를 필수 연결(`[[WikiLink]]`)하십시오.

## 3. 정보 검증 및 Fact / Opinion 구분
- `1_Bible_Exegesis` 작성 시 사본학/원어 문법/역사적 배경 등 **객관적 데이터(Fact)**와 신학파별 **해석(Opinion)**을 엄격히 구분하십시오.
- 단론이나 대립하는 주석이 존재할 경우 양측 견해와 대표 출처를 병기하십시오.

## 4. 토큰 활용 및 서브에이전트(Subagent) 활용
- 난이도 높은 본문 주해나 예화 발굴 시, 적극적으로 **Subagent Loop**를 가동하여 독립적 조사를 마친 후 본문으로 합치십시오.

## 4.1 성경공부 묵상 노트 (`1_Bible_Exegesis/0_Study_Notes/`)

> [!IMPORTANT] 자동 저장 원칙 (2026-08-25, 사용자 명시적 지시)
> **대화 중 신학적 질문·답변으로 도출된 의미 있는 결론은, 사용자가 "저장해줘"라고
> 요청하지 않아도 항상 적절한 형태로 위키에 저장한다.** 저장 여부를 되묻지 않는다.
> 판단 기준: 단순 사실 확인 답변이 아니라, 본문 해석·신학적 종합·설교 활용 가능성이
> 있는 대화라면 저장 대상이다. 저장 형식은 아래 규칙(묵상 노트 템플릿)을 따르되,
> 대화의 질문-답변 흐름 자체를 보존하여 나중에 문맥을 다시 이해할 수 있게 한다.
> 저장한 뒤에는 무엇을, 어디에 저장했는지 결과만 간단히 보고한다(저장할지 묻지 않는다).

- 정식 주해(Fact/Opinion 구분, 원어 분석)로 다듬기 전 단계의 개인적 깨달음/묵상은
  `1_Bible_Exegesis/0_Study_Notes/`에 `YYYY-MM-DD_제목.md` 형식으로 저장합니다.
  템플릿: `.claude/templates/study-note-template.md`.
- 원문(사용자가 말한 그대로의 묵상)은 반드시 전문을 보존하고, 그 위에 `related_passages`,
  `theological_themes`, 한 줄 요약, 확장 가능성(Follow-up)을 함께 기록합니다.
- 이후 내용이 충분히 무르익으면 `1_Bible_Exegesis/1_Old_Testament` 또는
  `2_New_Testament`로 정식 주해 승격이 가능하며, 이때 frontmatter의
  `promoted_to_exegesis: true`로 갱신합니다.

### 4.1.1 핫/콜드 2계층 구조 (긴 대화 저장 시)
> [!IMPORTANT] 로그 비대화 방지 원칙 (2026-08-25, 사용자 명시적 지시)
> "로그"(Master Index, 묵상 노트 목록 등 평소 훑어보는 장소)에는 너무 많은
> 내용을 담지 않는다. 대화가 길어지면(핵심 인용 5개 이상, 또는 다시 읽기에
> 부담스러운 분량) 다음 2계층으로 분리한다:
> - **Hot** (`1_Bible_Exegesis/0_Study_Notes/파일명.md`): 한 줄 요약, 재사용할
>   핵심 인용(짧게), Follow-up 체크리스트, 관련 문서 링크만 남긴다. 이 파일이
>   평소 스캔·인덱싱되는 대상이다.
> - **Cold** (`9_Archive/Study_Conversations/파일명_전문.md`): 질문-응답 대화
>   전문을 가공 없이 보존한다. `type: raw_conversation`, `status: cold_archive`.
>   `9_Archive/`는 `scripts/rebuild_index.py`가 스캔하지 않는 폴더이므로
>   (`Raw_Sermon_Scripts`와 동일한 원리) 자동으로 "무겁게 로딩되지 않는" 데이터가
>   된다.
> - 서로 frontmatter로 연결한다: Hot 쪽에 `full_conversation: "[[콜드 파일명]]"`,
>   Cold 쪽에 `hot_summary: "[[핫 파일명]]"`. **연관성 정보(WikiLink)를 타고
>   가야만 전문을 볼 수 있게** 하는 것이 핵심 — 평소에는 요약만 보이고, 필요할
>   때만 링크를 눌러 전문으로 들어간다.
> - 짧은 대화(핵심 인용 3-4개 이내)는 굳이 분리하지 않고 Hot 파일 하나로 충분하다.
> - 커밋 메시지: 콜드 아카이브 추가는 `feat(note)` 커밋에 함께 포함(별도 커밋 불필요).

- 커밋 메시지: `feat(note): [제목] 묵상 노트 추가`

## 4.2 외부 자료 조사 (`4_Reference_Research/`)

- 웹 검색·논문·타 설교 등 **외부에서 가져온 자료**는 `4_Reference_Research/`에
  별도 보관합니다. 내가 직접 쓴 주해(`1_Bible_Exegesis`)·설교(`2_Sermon_Outlines`)와
  **반드시 분리**하여, 나중에 "내 결론"과 "남의 결론"이 섞이지 않게 합니다.
- frontmatter 필수 필드: `type: research_note`, `topic`, `date_researched`,
  `researched_by`, `status`, 그리고 검증 한계가 있으면 `verification_caveat`.
- **신뢰도 등급을 반드시 표기**합니다:
  - `★★★` 학술 (단행본 · 피어리뷰 저널 · 학위논문) — 주해에 인용 가능
  - `★★` 유대교 1차·전통 자료 및 주요 기관 — 인용 가능, 원문 확인 권장
  - `★` 대중 설교 · 블로그 — 아이디어 참고용, 직접 인용은 지양
  - `⚠️` 근거가 얇은 대중 문헌 — 인용하지 말 것 (이유를 함께 명시)
- 조사 문서에는 **"다음 설교 준비 시 할 일" 체크리스트**를 넣어, 다음 작업 때
  무엇을 반영해야 하는지 바로 보이게 합니다.
- 관련 주해 문서에는 frontmatter `reference_research` 필드로 역참조를 겁니다.
- 커밋 메시지: `feat(research): [주제] 외부 자료 조사`

## 4.3 주해 문서의 검토 노트 (`## N. 검토 노트`)

- 기존 주해·설교를 재검토해 문제를 발견하면, 주해 문서 말미에
  `## N. 검토 노트 (YYYY-MM-DD 재검토)` 섹션을 추가해 기록합니다.
  원문 스크립트(`9_Archive/`)는 콜드 아카이브 원칙상 **수정하지 않고**,
  수정 대기 항목만 주해 쪽에 남깁니다.
- 심각도 표기: `🔴` 논리·신학 골격 / `🟠` 사실 오류 / `🟡` 근거 취약 /
  `✅` 확인 완료 / `🟢` 보강 기회
- 각 항목에 **수정 방향**을 함께 적어, 다음 작업자가 판단을 반복하지 않게 합니다.
- 주해 frontmatter에 `review_status`를 갱신합니다.
- 커밋 메시지: `docs(review): [본문] 검토 노트 추가`

## 4.4 메타데이터 기반 검색 인덱스 (`0_Index_MOC/Index_by_*.md`)

> [!IMPORTANT] 저장에서 끝나지 않고 "찾을 수 있어야" 한다 (2026-08-25, 사용자 명시적 지시)
> 문서를 아무리 잘 저장해도, frontmatter에만 적혀 있으면 파일명을 이미 아는
> 사람만 찾을 수 있다. `scripts/rebuild_index.py`는 Master Index 갱신과 함께
> **모든 문서(콜드 아카이브 제외)의 frontmatter를 스캔해 두 개의 교차 인덱스를
> 자동 생성**한다:
> - **`Index_by_Theme.md`**: `tags`·`theological_themes` 필드를 전부 모아
>   주제별로 역색인. "은혜로 태그된 문서 다 보여줘"가 즉시 가능해진다.
> - **`Index_by_Book.md`**: 66권 성경책 이름을 문서 전체(frontmatter + 본문)에서
>   스캔해 등장하는 책마다 역색인. 예화 설명이나 "교차 참조" 목록 안에서만
>   언급된 책도 잡아낸다 — 그래서 본문 전체를 스캔하는 것이 핵심이다.
> - 두 인덱스 모두 **수동 유지 금지** — `python3 scripts/rebuild_index.py` 한
>   번으로 항상 재생성된다. 새 문서를 추가할 때 직접 `Index_by_*.md`를 편집하지
>   말 것.
> - **알려진 한계**: (1) 동의어 통합 없음 — "은혜"·"구원"·"값없이"가 각각 다른
>   항목으로 분리된다. 문서를 못 찾으면 관련어로 한 번 더 찾아볼 것.
>   (2) 짧은 책 이름(`아가` 등)은 일반 단어(`돌아가다`)와 겹쳐 오탐이 나므로
>   `AMBIGUOUS_SHORT_BOOKS`에 등록해 frontmatter만 스캔하도록 예외 처리했다 —
>   새로운 오탐이 발견되면 그 목록에 추가할 것.
> - 새로운 문서 유형을 추가할 때는 `TYPE_ICON` 딕셔너리에 아이콘을 등록해야
>   인덱스에 올바르게 표시된다.

## 4.5 콜드 아카이브 (`9_Archive/`)
`9_Archive/`는 **의도적으로 `scripts/rebuild_index.py`의 자동 스캔 대상에서
제외**되어 있습니다 — 평소 위키 운영/로딩 시 매번 불러오지 않는 콜드 데이터이기
때문입니다. 하위 두 폴더 모두 이 원리를 공유하며, 항상 "요약본 → 링크 → 전문"
방향으로만 열람합니다.

- **`Raw_Sermon_Scripts/`**: 사용자가 기존에 작성했던 설교 스크립트 원문(슬라이드
  형식 등 가공되지 않은 원본)을 `type: raw_script`, `status: cold_archive`로
  그대로 보존합니다. 원문이 필요할 때만 정제된 설교 문서의 frontmatter
  (`raw_script_archive` 필드)를 통해 링크를 따라가서 열람합니다. 원문을 정제하여
  `1_Bible_Exegesis`·`2_Sermon_Outlines`로 옮길 때는, 정제 문서 쪽에
  `raw_script_archive: "[[원문 파일명]]"`을 반드시 추가해 역참조를 유지합니다.
- **`Study_Conversations/`**: 묵상 노트의 대화 전문을 보존합니다. 4.1.1(핫/콜드
  2계층 구조)을 참고하십시오.

## 4.6 설교 준비 산출물 — PPT / 구연 스크립트
- 설교 준비 시 `2_Sermon_Outlines`의 3대지 아웃라인 작성 후, 필요하면 다음 두 산출물을
  추가로 만듭니다 (기존 설교/예화를 참고하여 작성):
  - **구연 스크립트**: 아웃라인과 같은 폴더에 `[날짜]_[제목]_script.md`로 저장 —
    실제 강단에서 말할 문장 단위의 대본.
  - **PPT**: 동일 폴더 또는 `3_Shared_Assets/Slides/`에 `.pptx` 파일로 생성.
- 아웃라인 frontmatter에 `script_file`, `slides_file` 필드로 상호 참조를 남깁니다.

## 5. 지식 그래프 자동 갱신 및 Git 자동화 (Git Automation)
- 작업 완료 후 다음 명령을 순차 실행하십시오:
  1. `python3 scripts/rebuild_index.py` (Master Index 갱신)
  2. `git status` 확인 후 커밋 & 푸시:
     - 주해 작성: `feat(exe): [성경구절] 학술 주해 작성`
     - 설교 작성: `feat(sermon): [날짜] [제목] 3대지 어린이 설교 작성`
     - 예화 추가: `feat(asset): [예화명] 예화 자산 추가`
     - 묵상 노트: `feat(note): [제목] 묵상 노트 추가`
     - PPT/스크립트: `feat(media): [날짜] [제목] PPT/스크립트 추가`
     - 외부 자료 조사: `feat(research): [주제] 외부 자료 조사`
     - 검토 노트: `docs(review): [본문] 검토 노트 추가`
     - 나눔 작성: `feat(nanum): [날짜] [목장명] 나눔 등록`

## 6. 목장 나눔(Group Sharing) 운영 원칙 (`4_Group_Sharing/`)
- 성인 목장에서 나누는 개인 간증/묵상 나눔은 어린이 설교(2_Sermon_Outlines)나 학술 주해(1_Bible_Exegesis)와 **완전히 다른 장르**입니다 — `.claude/templates/nanum-template.md`를 사용하고, 목장별 하위 폴더(`4_Group_Sharing/[목장명]/`)에 날짜별로 저장하십시오.
- **구조를 강제하지 마십시오:** 3대지 구조나 Fact/Opinion 구분 같은 다른 카테고리의 엄격한 형식을 나눔에 적용하지 않습니다. 나눔은 나눈 사람의 목소리와 표현을 최대한 그대로 살리는 자유 서술체이며, 편집은 사용자가 명시적으로 요청할 때(오타 교정, 논리 보완 제안 등)만 수행합니다.
- **문체는 사용자 지정을 따릅니다:** 존댓말/반말 등 문체 선택은 목장·나눈 사람의 스타일을 존중하여 사용자가 지정한 대로 유지하십시오.
- 관련 설교나 주해가 있으면 `related_passage`/`Linked Sermon/Exegesis` 필드로 상호 연결하되, 나눔이 반드시 특정 설교 문서와 1:1로 연결되어야 하는 것은 아닙니다.
- `scripts/rebuild_index.py`는 `4_Group_Sharing/` 하위의 각 목장 폴더를 동적으로 스캔하여 Master Index에 반영합니다 (연도별 설교 폴더 스캔과 동일한 방식).
