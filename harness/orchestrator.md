# 오케스트레이터

> 메인 세션이 이 문서대로 하네스를 지휘한다. CLAUDE.md는 이 문서를 가리키기만 한다.
> 규칙 숫자는 harness/rules.json에만 있다. 여기에 다시 적지 않는다.

## 하는 일 (4가지)
1. 서브에이전트 호출 (harness/roles.md의 에이전트만)
2. 게이트 스크립트 실행 결과 읽기 (실행 시작 시 check_rules_sync.py 먼저)
3. runs/{flow}/state.json 갱신
4. 실행이 끝나면 runs/{flow}/retro.md 작성 (harness/verification.md §4)

## 하지 않는 일 (0회)
- 산출물 작성 (s1~s5 폴더의 파일)
- Figma 수정
- 위반 직접 수정
- human/approval.md 작성

## 실행 순서
| 순서 | 동작 | 통과하면 | 실패하면 |
|---|---|---|---|
| 1 | ref-researcher 호출 → gate_s1.py | S2 | S1 다시 실행, loops.S1 +1 |
| 2 | screen-planner 호출 → gate_s2.py | S3 | S2 다시 실행, loops.S2 +1 |
| 3 | keyscreen-designer 호출 → waiting_human | — | — |
| 4 | human/approval.md 확인 | 승인 → S4 | 반려 → S2 |
| 5 | ui-designer 호출 | S5 | — |
| 6 | judge 호출 (gate_s5.py) | done | S4로 돌아감, loops.S5 +1 |
| 7 | 반복 횟수가 rules.json의 loop 한도에 도달 (S1: s1_max, S2: s2_max, S5→S4: s5_to_s4_max) | — | halted, 사람에게 넘김 |

- uibowl 로그인이 풀렸거나 캡처가 막히면 halted. 사유는 "uibowl 다시 로그인 필요"
- 되돌아간 경우에만 해당 스테이지 폴더를 새로 쓴다. 그 외에는 통과한 스테이지의 파일을 덮어쓰지 않는다.

## state.json
```json
{ "flow": "mission-submit", "stage": "S3",
  "passed": ["S1", "S2"],
  "loops": { "S1": 0, "S2": 0, "S5": 0 },
  "status": "running | waiting_human | halted | done",
  "halted_reason": null }
```

## 실행 단위
- 한 번에 플로우 1개만 실행한다.
- status가 running 또는 waiting_human인 플로우가 있으면 새 플로우를 시작하지 않는다.
- "하네스 이어서"는 이 상태의 플로우를 재개한다.

## 보고 형식
- 게이트를 지날 때마다 1줄. 예: `G2 통과 (6/6) → S3 시작`
- 실패하면 1줄. 예: `G5 실패 (위반 4건) → S4 수정 2/3회차`
- 멈추면 이유와 사람이 할 일을 1줄로. 예: `⏸ 키스크린 3개 완료. runs/mission-submit/human/approval.md에 승인 또는 반려: 사유를 적어 주세요`
