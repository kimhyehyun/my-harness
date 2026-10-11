# 검증과 리뷰

> 게이트: harness/gates.md · 규칙: harness/rules.json

## 1. 판정 스크립트 검증 (하네스를 실제로 돌리기 전에 1회, 스크립트를 고칠 때마다)
- 위치: harness/tests/fixtures/
  - pass/: 모든 게이트를 통과하는 샘플 1세트
  - fail/{게이트 ID}/: 그 규칙 하나만 어긴 샘플
- 실행: `python3 harness/tests/run_fixtures.py`
- 통과 조건
  | 조건 | 기준 |
  |---|---|
  | pass 샘플 | exit 0, 위반 0건 |
  | fail 샘플 | exit 1, 리포트에 해당 게이트 ID가 정확히 1개 |
  | 커버리지 | 게이트 ID 24개(G1 6, G2 6, G5 12)가 모두 최소 1번 걸림 |
  | ★ 커버리지 | G2-3, G2-4, G2-5, G2-6, G5-10, G5-11 중 빠진 것 0개 |

## 2. 규칙 동기화 검사 (하네스 실행을 시작할 때마다)
- `python3 harness/gates/check_rules_sync.py`
- design.md와 rules.json의 아래 항목을 비교한다
  - color 변수 이름과 hex
  - radius 변수 표 (xs~4xl)
  - space 변수
  - 텍스트 스타일 이름과 크기
- 하나라도 다르면 halted. 사유는 "design.md 변경됨, rules.json 갱신 필요"
- rules.json을 고치는 것은 사람이 한다. 에이전트는 harness/에 쓸 수 없다.

## 3. 첫 실전 실행
- 플로우: finish-workout (오늘의 운동 → 운동 완료)
- 확인할 것: ★ 게이트 G2-3 ~ G2-6(자동 완료 금지)과 G5-10(이미지 출처)이 실제 산출물에서 작동하는지
- 참고: runs/chrifit/은 게이트 스크립트가 없을 때 Figma에서 직접 검사한 시범 실행이다

## 4. 실행 후 리뷰 (runs/{flow}/retro.md, 오케스트레이터가 작성)
1. 스테이지별 반복 횟수 (state.json의 loops)
2. 가장 많이 나온 위반 3개 (게이트 ID 기준)
3. 개선 제안
- 같은 게이트 ID가 2개 이상의 플로우에서 반복되면 에이전트 지침이나 rules.json을 고치자고 제안한다.
- 직접 고치지 않고, 사람이 승인한 뒤에만 반영한다.
