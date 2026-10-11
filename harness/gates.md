# 게이트

> 숫자는 모두 harness/rules.json에서 읽는다. 이 문서는 "무엇을 어디서 세는지"만 정한다.
> 실패하면 harness/pipeline.md의 "되돌아가는 지점" 표를 따른다.

## 공통 형식
- 게이트마다 스크립트 1개: harness/gates/gate_s1.py, gate_s2.py, gate_s5.py
- 통과하면 exit 0, 실패하면 exit 1
- 실패 내용은 {rule, target, actual, allowed} 목록으로 출력
- 판정 스크립트는 읽기만 한다. 파일을 고치지 않는다.

## G1 — S1→S2 (대상: s1/refs/, s1/points.md)
| ID | 조건 |
|---|---|
| G1-1 | PNG 개수 = index.md 행 수 |
| G1-2 | index.md에서 출처 URL이 빠진 행 0개 |
| G1-3 | 화면 유형마다 3~5장, 전체 15장 이하 |
| G1-4 | 반영 포인트 3~7개 |
| G1-5 | 포인트마다 근거 레퍼런스 파일명 1개 이상, 그 파일이 실제로 있음 |
| G1-6 | 포인트마다 유저스토리 번호(1~5) 1개 이상 |

## G2 — S2→S3 (대상: s2/screens.md)
| ID | 조건 |
|---|---|
| G2-1 | Phase 2 이후 금지어 0개 (rules.json의 phase2_forbidden). 판매 기준 체크리스트 8개 문장은 세지 않는다 |
| G2-2 | 모든 화면에 유저스토리 번호 1개 이상 |
| ★G2-3 | 자산 상태값은 asset_status.allowed 5개만 허용. forbidden 상태값 0개 |
| ★G2-4 | admin-review 플로우일 때 판매 기준 체크리스트 8개 항목이 모두 있음 |
| ★G2-5 | 승인 버튼에 "체크리스트를 모두 체크하기 전에는 비활성"이라고 명시됨 |
| ★G2-6 | `판매 신청 → 승인됨` 직접 전이 0개 (반드시 검수 대기를 거침) |

## H — S3→S4 사람 승인 (대상: human/approval.md)
- 첫 줄이 `승인` 또는 `반려: {사유}` 중 하나
- 사유 없는 반려는 무효
- 이 파일은 사람만 작성한다. 에이전트는 쓰지 않는다.
- 반려되면 S2로 돌아간다.

## G5 — S5 완료 (대상: s4/export.json)
| ID | 조건 |
|---|---|
| G5-1 | 색: fill과 stroke 값이 colors.allowed에 있음 |
| G5-2 | radius: radius.allowed에 있음. app-icon 노드는 한 변의 30% |
| G5-3 | 간격: padding과 gap 값이 spacing.allowed에 있음 |
| G5-4 | 그림자: shadow.allowed_nodes 외 drop shadow 0개 |
| G5-5 | accent: 화면당 2개 이하, button 노드에는 0개 |
| G5-6 | 타이포: 폰트, 크기, 굵기, 자간이 허용 목록에 있음 |
| G5-7 | 프레임: 최상위 화면 크기 390×844 |
| G5-8 | 터치: button 노드의 높이 44 이상 |
| G5-9 | textCase UPPER 0개 |
| ★G5-10 | 더미 텍스트에 개인정보 패턴(pii_patterns) 0건 |
| ★G5-11 | s1/refs 이미지를 화면 안에 그대로 쓴 경우 0건 |

★ = story-service.md의 "어기면 안 되는 것"을 지키는 게이트
- 규칙 1 (판매 자산은 운영자 검수를 반드시 통과, 체크리스트 필수) → G2-3, G2-4, G2-5, G2-6
- 규칙 2 (개인정보, 고객정보, 회사기밀, 타인 저작물 금지) → G5-10, G5-11
