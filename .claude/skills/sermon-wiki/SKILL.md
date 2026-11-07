---
name: sermon-wiki
description: Steve의 성경·설교 위키(stevekoo-ai/Bible-Sermon-wiki, PC E:\Claude_Local) 한방 온보딩. 새 세션에서 설교 저장 구조·진행 중 작업·지켜야 할 규칙을 한 번에 파악하고 바로 작업을 시작할 때 쓴다. "설교 위키", "저장 구조", "어디에 저장돼 있어", "이어가자", "인계 문서", "새 세션", "온보딩", 또는 어린이 설교·구연 스크립트·QT·묵상·목장 나눔·주해·예화 작업을 맥락 없이 받았을 때 먼저 불러온다.
---

# 성경·설교 위키 길잡이

이 스킬은 지도를 **가리키기만** 한다. 규칙의 단일 출처는 루트 `CLAUDE.md`, 진행 상황의 단일 출처는 `0_Index_MOC/진행중_작업_인계.md`다. 내용이 겹치면 그 두 문서가 이긴다.

## 1. 한방 스냅샷 (먼저 실행)

```bash
python scripts/wiki_snapshot.py        # PC (python3 없음, python 사용)
python3 scripts/wiki_snapshot.py       # 클라우드
```

읽기 전용이다. git 동기화(뒤처졌는지) · 폴더별 문서 수 · 인계 문서 · 다가오는/미정 설교와 그 파일들(아웃라인·script R번호·html·pptx) · 최근 묵상 5개 · 목장별 최신 나눔 · PC 바깥 저장 위치를 한 화면에 보여준다. 결과가 `behind`이면 `git pull --rebase origin main` 후 시작한다.

## 2. 저장소 세 곳

| 위치 | 무엇 | 비고 |
|---|---|---|
| `E:\Claude_Local` = GitHub `stevekoo-ai/Bible-Sermon-wiki` | 설교·주해·묵상·나눔 위키 (여기서 작업) | **공개 저장소** — 실명은 ○○○ 또는 Steve |
| `D:\설교\어린이지구설교\YYYYMMDD_본문\` | 실제 강단용 원본 docx/pptx, 소품 사진 | 위키 밖. 읽기만. 위키 원문 보존본은 `9_Archive/Raw_Sermon_Scripts/` |
| `E:\GitHub\Repo_name` = `stevekoo-ai/Repo_name` | 경제·PEOS 위키 | 설교 자료 없음. **오드리 브리핑/영어 오드리 정의만** `wiki/concepts/audrey-briefing-style.md`, `english-meeting-script-style.md`. 그 저장소 규칙(push_with_retry 등)을 여기 섞지 말 것 |

클라우드 세션이면 D:·E:\GitHub는 없다 — 정상이다. 드라이브 전체 검색은 하지 말고 경로를 Steve에게 묻는다.

## 3. 읽는 순서 (3분)

1. `CLAUDE.md` — 특히 §4.1 Steve 묵상 문체, §4.7 HTML 변환, §5 커밋 메시지, §6 나눔
2. `0_Index_MOC/진행중_작업_인계.md` — 지금 무엇을 하다 멈췄는지, 다음 단계
3. 설교·QT·나눔을 **쓰기 전에** `0_Index_MOC/Steve_스타일_가이드.md` (원문에서 뽑은 실제 패턴 + §7 체크리스트)
4. 찾을 때: `Master_Index.md` · `Index_by_Theme.md`(주제) · `Index_by_Book.md`(성경책). 못 찾으면 관련어로 한 번 더

## 4. 작업별 바로가기

| 할 일 | 저장 위치 · 파일명 | 템플릿 / 먼저 볼 것 | 커밋 |
|---|---|---|---|
| 어린이 설교 아웃라인 | `2_Sermon_Outlines/YYYY_Preaching/YYYY-MM-DD_제목.md` (날짜 미정은 `TBD_Steve_설교_제목.md`) | `.claude/templates/sermon-template.md`, 같은 본문의 `9_Archive/Raw_Sermon_Scripts/` 이전 설교, 시리즈 허브 `2_Sermon_Outlines/0_Series/` | `feat(sermon): [날짜] [제목] 3대지 어린이 설교 작성` |
| 구연 스크립트 · PPT | 아웃라인 옆 `…_script.md` → 개정은 `_script_R2.md`, `_R3`… (이전 판은 지우지 않음). PPT는 같은 폴더나 `3_Shared_Assets/Slides/` | 아웃라인 frontmatter `script_file`·`slides_file` 갱신, 스크립트에 `previous_version` | `feat(media): [날짜] [제목] PPT/스크립트 추가` |
| QT · 묵상 정리 | `1_Bible_Exegesis/0_Study_Notes/YYYY-MM-DD_제목.md` | `study-note-template.md`, CLAUDE.md §4.1 문체. 원문 전문 보존. 긴 대화는 핫/콜드 분리(§4.1.1 → `9_Archive/Study_Conversations/…_전문.md`) | `feat(note): [제목] 묵상 노트 추가` |
| 목장 나눔 | `4_Group_Sharing/[목장명]/YYYY-MM-DD_제목.md` (현재: `히엘_1-4목장`, `심화반_6기`) | `nanum-template.md`, §6 (구조 강제 금지). Keep 저장은 Chrome → 라벨 '나눔', 제목 `[목장나눔YYYYMMDD] 제목` | `feat(nanum): [날짜] [목장명] 나눔 등록` |
| 정식 주해 | `1_Bible_Exegesis/1_Old_Testament/` · `2_New_Testament/` | `exegesis-template.md`, Fact/Opinion 분리(§3) | `feat(exe): [성경구절] 학술 주해 작성` |
| 예화 | `3_Shared_Assets/Illustrations/제목.md` (지도 `Maps/`, 연표 `Timelines/`, 용어 `Theology_Terms/`) | 설교에서 `[[WikiLink]]`로 연결 | `feat(asset): [예화명] 예화 자산 추가` |
| 외부 자료 조사 | `4_Reference_Research/주제.md` | 신뢰도 ★★★/★★/★/⚠️, "다음 설교 준비 시 할 일" 체크리스트(§4.2) | `feat(research): [주제] 외부 자료 조사` |
| 기존 설교 재검토 | 주해 말미 `## N. 검토 노트 (YYYY-MM-DD 재검토)` | §4.3 심각도 🔴🟠🟡✅🟢. `9_Archive/`는 고치지 않음 | `docs(review): [본문] 검토 노트 추가` |
| 읽기용 HTML | md 옆 같은 이름 `.html` | `python scripts/note_to_html.py <파일.md>` — **파일 하나만** 넘긴다. HTML 손으로 쓰지 않음 | 해당 작업 커밋에 포함 |
| 오드리 브리핑 | 대상 문서 옆 `…_오드리브리핑.md` (예: `4_Reference_Research/고린도후서_숲과나무_오드리브리핑.md`) | Repo_name `wiki/concepts/audrey-briefing-style.md` | 해당 작업 커밋 |

연표·지도 PPT는 `scripts/make_*_ppt.py`, `make_*_map*.py`로 다시 만든다(손으로 고치지 말고 스크립트 수정).

## 5. 꼭 지킬 규칙 (요약 — 원문은 CLAUDE.md)

- **Steve 글은 Steve 목소리.** 완성 원고는 오타만 고치고 고친 목록을 따로 알린다. 새 문장·장면을 지어 넣지 않는다. "거친 말투 그대로"면 맞춤법·띄어쓰기만.
- **설교는 실제 Steve 패턴으로.** 일반 "3대지" 틀만 따르지 말고 스타일 가이드의 열쇠 단어 찾기 · "근데.. 찜찜하지 않아?" · 하나님 1인칭 독백 · 시리즈 회상 퀴즈 · 소품 · 고정 기도 마무리를 반영한다.
- **PPT에 없다고 안 쓴 게 아니다.** Steve는 손으로 만든 소품을 쓴다. 위키를 "바로잡기" 전에 묻는다.
- **신학 대화의 결론은 묻지 않고 저장**(§4.1), 저장 후 무엇을 어디에 저장했는지만 보고한다.
- **9_Archive는 수정 금지**, 인덱스 `Index_by_*.md`·`Master_Index.md`는 손으로 편집 금지(스크립트가 만든다).
- 채팅에서는 오드리(스티브라고 부름, 밝고 다정한 존댓말). 단, Steve 원고 안에는 오드리 말투를 넣지 않는다.

## 6. 작업을 마칠 때

1. 진행 상태가 바뀌었으면 `0_Index_MOC/진행중_작업_인계.md`를 갱신한다(끝난 일은 지우고, 새 일은 위에 추가).
2. `python scripts/rebuild_index.py` (클라우드는 `python3`)
3. `git status` 확인 → §5 형식으로 커밋 → `git push origin main`. 다른 세션이 커밋했을 수 있으니 거절되면 `git pull --rebase origin main` 후 다시 push.
4. 저장소 구조가 바뀌었으면(새 폴더·새 목장·새 스크립트) 이 SKILL.md의 2·4절과 `scripts/wiki_snapshot.py`의 `FOLDERS`/`PC_PLACES`도 같은 커밋에서 고친다.
