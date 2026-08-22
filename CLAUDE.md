# 🧠 성경 연구 및 설교 지식베이스 LLM Wiki 운영 원칙 (v3.1 Kid-Adult Hybrid)

## 1. 저장소 정체성 및 격리 (Repository Architecture)
- 이 리포지토리는 **학술적 성경 주해(Bible Exegesis)**, **3대지 구조의 설교 아웃라인(Sermon Outlines)**, **신학 자산(Assets)** 관리를 위한 전용 LLM Wiki입니다.
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

## 5. 지식 그래프 자동 갱신 및 Git 자동화 (Git Automation)
- 작업 완료 후 다음 명령을 순차 실행하십시오:
  1. `python3 scripts/rebuild_index.py` (Master Index 갱신)
  2. `git status` 확인 후 커밋 & 푸시:
     - 주해 작성: `feat(exe): [성경구절] 학술 주해 작성`
     - 설교 작성: `feat(sermon): [날짜] [제목] 3대지 어린이 설교 작성`
     - 예화 추가: `feat(asset): [예화명] 예화 자산 추가`
