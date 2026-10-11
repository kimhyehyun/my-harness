# my-harness — ChriFit 디자인 하네스

ChriFit 운동 앱 화면을 Claude Code가 **규칙(게이트)을 지키며** 만들도록 짠 하네스입니다.

- 서비스 정의: [docs/prd.md](docs/prd.md) · 판정 기준: [docs/story-service.md](docs/story-service.md)
- 디자인 규칙: [docs/design.md](docs/design.md) (Figma `ChriFit Design System`)
- 하네스: [CLAUDE.md](CLAUDE.md)에서 시작 → [harness/](harness/)
- 실행 기록: [runs/chrifit/](runs/chrifit/README.md) — 키스크린 Today 1장으로 화면 4개 생성

## 흐름
S1 레퍼런스(uibowl MCP) → S2 화면 설계 → S3 키스크린 → **사람 컨펌** → S4 디자인(Figma) → S5 검토(읽기 전용 판정)

## 어기면 안 되는 것
1. 운동 기록은 사용자가 직접 체크한 것만 남긴다 (자동 완료 금지)
2. 운동 이름·설명·이미지는 출처를 표시하고 허락된 자료만 쓴다

## 아직 만들지 않은 것
- 판정 스크립트(harness/gates/*.py), 서브에이전트 정의(.claude/agents/), PreToolUse 훅
