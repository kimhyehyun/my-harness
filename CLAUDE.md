# ChriFit 디자인 하네스

이 저장소는 ChriFit 운동 앱(PRD: docs/prd.md)의 화면을
레퍼런스 수집 → 화면 설계 → 키스크린 → 디자인 → 검토 순서로 만드는 하네스다.
디자인 기준은 Figma `ChriFit Design System`(docs/design.md, rules.json의 figma)이다.
메인 세션은 **오케스트레이터**로만 동작한다. 산출물을 직접 만들지 않는다.

## 먼저 읽을 것
| 문서 | 역할 |
|---|---|
| docs/prd.md | ChriFit 서비스 정의, 화면, 플로우 5개, 범위 |
| docs/story-service.md | 판정 기준. 유저스토리 5개, 어기면 안 되는 것 2개 |
| docs/story-work.md | 원래 손으로 하던 작업 흐름 |
| docs/design.md | 디자인 규칙 원본 = ChriFit Design System |
| harness/purpose.md | 입력, 사용자, 완료 기준 |
| harness/pipeline.md | 스테이지 S1~S5, 되돌아가는 지점 |
| harness/artifacts.md | runs/{flow}/ 파일 구조, 재개 |
| harness/rules.json | 모든 숫자·목록 규칙의 SSOT |
| harness/gates.md | 게이트 ID별 통과 조건 |
| harness/roles.md | 에이전트, 편집 폴더, 트리거 |
| harness/orchestrator.md | 실행 순서, state.json, 보고 형식 |
| harness/verification.md | 스크립트 검증, 규칙 동기화, 회고 |
| harness/gates/*.py | 판정 스크립트 (G1·G2·G5, 규칙 동기화) |
| .claude/agents/*.md | 서브에이전트 5개 정의 |
| harness/hooks/guard.py | 편집 범위 훅 (.claude/settings.json) |

docs/prd-huddling.md, docs/design-huddling.md는 이전 버전 보관용이다. 읽지 않는다.

## 트리거
| 말 | 동작 |
|---|---|
| "하네스 돌려줘 {flow}" | check_rules_sync.py → S1부터 실행 |
| "하네스 이어서" | runs/*/state.json을 보고 다음 스테이지부터 |
| "하네스 판정 {flow}" | judge만 호출 (S5) |
| "승인" / "반려: 사유" | human/approval.md를 확인만 한다. 없으면 사람에게 작성을 요청 |

{flow}는 rules.json의 flows 5개(pick-today, find-exercise, do-session, finish-workout, review-history) 중 하나. 그 외의 이름이면 실행하지 않고 목록을 보여준다.

## 오케스트레이터 규칙
- 하는 일: 서브에이전트 호출, 게이트 결과 읽기, state.json·retro.md 작성
- 하지 않는 일: s1~s5 산출물 작성, Figma 수정, 위반 직접 수정, human/approval.md 작성
- 한 번에 플로우 1개. running·waiting_human 상태의 플로우가 있으면 새로 시작하지 않는다.
- 사람 승인 지점은 S3→S4 한 곳뿐이다.
- 게이트를 지날 때마다 1줄로 보고한다. 멈추면 이유와 사람이 할 일을 1줄로 알린다.

## 어기면 안 되는 것 (story-service.md)
1. 운동 기록은 사용자가 직접 체크한 것만 남긴다. 자동으로 완료 처리하지 않는다 → G2-3 ~ G2-6
2. 운동 이름·설명·이미지는 출처를 표시하고, 허락된 자료만 쓴다 → G5-10, G5-11
이 게이트들은 어떤 이유로도 건너뛰거나 예외로 처리하지 않는다.

## 범위
- PRD §4 MVP 화면만. PRD §10 범위 밖(로그인, 결제, 커뮤니티, 태블릿, 라이트 테마)은 만들지 않는다.
- 프레임 너비 390, 최소 높이 844, 상단 헤더 56.
- 새 화면은 ChriFit 컴포넌트 인스턴스와 변수·텍스트 스타일로만 조립한다.

## 외부 도구
- uibowl: 프로젝트 .mcp.json의 uibowl MCP를 쓴다. 인증이 풀리면 멈추고 `/mcp` 재인증을 요청한다. 우회하지 않는다.
- Figma: fileKey는 rules.json에 둔다. 기준 키스크린은 02 Screens의 Today. 플로우 키스크린은 `{flow} · keyscreens`, 전체 화면은 `{flow}` 페이지에 그린다. 기존 페이지(00·01·02)와 원본 컴포넌트는 수정하지 않는다.
- Figma 판정 입력은 harness/figma/export_s4.js로 만든 s4/export.json이다.

## 규칙이 바뀌면
- design.md·prd.md가 원본이다. rules.json과 다르면 실행을 멈추고 사람에게 갱신을 요청한다.
- 에이전트는 harness/와 docs/에 쓰지 않는다 (PreToolUse 훅으로 차단).
