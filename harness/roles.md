# 역할

> 파이프라인: harness/pipeline.md · 게이트: harness/gates.md

## 에이전트와 편집 폴더
| 에이전트 | 스테이지 | 편집 가능 폴더 (1개) | Figma |
|---|---|---|---|
| ref-researcher | S1 | runs/{flow}/s1/ | 접근 안 함 (uibowl은 MCP로) |
| screen-planner | S2 | runs/{flow}/s2/ | 접근 안 함 |
| keyscreen-designer | S3 | runs/{flow}/s3/ | `{flow} · keyscreens` 페이지만 씀 |
| ui-designer | S4 | runs/{flow}/s4/ | `{flow}` 페이지만 씀. keyscreens 페이지는 읽기만 |
| judge | S5 | runs/{flow}/s5/ (리포트만) | 접근 안 함 |
| 사람 | H | runs/{flow}/human/approval.md | — |
| 오케스트레이터 (메인 세션) | 전체 | runs/{flow}/state.json, retro.md | 접근 안 함 |

- 에이전트 정의: .claude/agents/{이름}.md (도구 목록이 frontmatter의 tools로 제한됨)
- 모든 에이전트에게 harness/와 docs/는 읽기 전용이다.
- 00 Foundations · 01 Components · 02 Screens 페이지는 어떤 에이전트도 수정하지 않는다.
- 앞 스테이지의 폴더는 읽을 수 있지만 쓸 수 없다.

## 판정자 (judge) — 읽기 전용
- 허용 도구: Read, Bash
- Bash로는 `python3 harness/gates/gate_*.py`만 실행할 수 있다.
- Edit 0개, Figma 쓰기 도구 0개
- 쓸 수 있는 것은 스크립트 출력을 s5/report.json으로 저장하는 것 하나뿐
- 위반을 고치지 않고 보고만 한다. 수정은 ui-designer가 한다.

## 강제 방식 (.claude/settings.json → harness/hooks/guard.py)
훅 입력의 `agent_type`으로 누가 쓰는지 구분한다.
- 에이전트가 자기 폴더(runs/{flow}/sN/) 밖에 Write/Edit하면 차단 (harness/, docs/, 프로젝트 밖 포함)
- human/approval.md에는 누구도(오케스트레이터 포함) 쓸 수 없음
- judge: Write/Edit 차단, Bash는 `python3 harness/gates/gate_*.py`만, --out은 s5/report.json만
- ref-researcher: Bash는 s1/refs 안으로 받는 `curl -o`만
- 나머지 에이전트: Bash 차단. 명령 연결(; && | 리다이렉트)은 모두 차단
- 오케스트레이터(메인 세션): s1~s5 산출물 직접 작성 차단. state.json·retro.md·하네스 유지보수는 허용
- 프로젝트 훅은 이 폴더의 workspace trust를 수락해야 실행된다

## 자연어 트리거
| 말 | 동작 |
|---|---|
| "하네스 돌려줘 {flow}" | S1부터 전체 실행 |
| "하네스 이어서" | state.json을 보고 다음 스테이지부터 |
| "하네스 판정 {flow}" | S5만 실행 |
| "승인" / "반려: 사유" | 오케스트레이터가 human/approval.md를 확인한다. 파일이 없거나 형식이 틀리면 사람에게 직접 작성해 달라고 요청하고 멈춘다. 있으면 S4(승인) 또는 S2(반려)로 진행 |

- "토큰 검사해줘", "DS 점검해줘"는 design-system-validator 스킬의 트리거라 쓰지 않는다.
