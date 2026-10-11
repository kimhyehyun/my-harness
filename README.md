# my-harness — ChriFit 디자인 하네스

ChriFit 운동 앱 화면을 Claude Code가 **규칙(게이트)을 지키며** 만들도록 짠 하네스입니다.

- 서비스 정의: [docs/prd.md](docs/prd.md) · 판정 기준: [docs/story-service.md](docs/story-service.md)
- 디자인 규칙: [docs/design.md](docs/design.md) (Figma `ChriFit Design System`)
- 하네스: [CLAUDE.md](CLAUDE.md)에서 시작 → [harness/](harness/)
- 실행 기록: [runs/chrifit/](runs/chrifit/README.md) — Today 키스크린 1장으로 화면 4개 생성, 제출용 메인 기준으로 하단 바 보정
- 화면 이미지: [docs/screens/](docs/screens/) — [Today (main.png)](docs/screens/main.png), [Splash](docs/screens/Splash.png), History, Add Exercise Sheet, Exercise Detail, Workout Done

## 제출 기준
- [Figma 메인 `58:1070`](https://www.figma.com/design/EDcJ9a4nsLkEYJDmZPGi80/ChriFit-Design-System?node-id=58-1070)이 현재 시각 기준이다. [main.png](docs/screens/main.png)의 `전체 83개`와 하단 얼굴형 마스코트를 따른다.
- Figma `22:145`는 시범 실행 때 사용한 네이티브 Today 화면이다. 당시 `전체 77개`가 표시되어 현재 메인과 구분한다.
- [History](docs/screens/History.png)와 [Workout Done](docs/screens/Workout%20Done.png)의 하단 바 및 안전 영역을 현재 메인에 맞춰 수정했다. S5 자동 검사는 구조·토큰 규칙을 판정하며, 시각 비교는 캡처로 확인한다.

## 흐름
S1 레퍼런스(uibowl MCP) → S2 화면 설계 → S3 키스크린 → **사람 컨펌** → S4 디자인(Figma) → S5 검토(읽기 전용 판정)

## 어기면 안 되는 것
1. 운동 기록은 사용자가 직접 체크한 것만 남긴다 (자동 완료 금지)
2. 운동 이름·설명·이미지는 출처를 표시하고 허락된 자료만 쓴다

## 구성
| 구성 | 위치 |
|---|---|
| 판정 스크립트 | `harness/gates/` — gate_s1.py(G1), gate_s2.py(G2·★), gate_s5.py(G5·★), check_rules_sync.py |
| Figma 값 추출 | `harness/figma/export_s4.js` → `runs/{flow}/s4/export.json` |
| 서브에이전트 5개 | `.claude/agents/` — ref-researcher, screen-planner, keyscreen-designer, ui-designer, judge(읽기 전용) |
| 편집 범위 훅 | `.claude/settings.json` → `harness/hooks/guard.py` |
| 산출물 템플릿 | `harness/templates/` |
| 검증 | `harness/tests/` |

## 직접 확인하기
```bash
python3 harness/gates/check_rules_sync.py      # design.md ↔ rules.json
python3 harness/tests/run_fixtures.py          # 게이트 24개가 각자 자기 규칙만 잡는지
python3 harness/tests/test_guard.py            # 훅 허용·차단 19건
python3 harness/gates/gate_s5.py runs/chrifit  # 시범 실행 화면 판정 (위반 0건)
```
