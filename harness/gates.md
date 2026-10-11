# 게이트

> 숫자와 목록은 모두 harness/rules.json에서 읽는다. 이 문서는 "무엇을 어디서 세는지"만 정한다.
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
| G1-3 | refs.types 유형마다 3~5장, 전체 15장 이하 |
| G1-4 | 반영 포인트 3~7개 |
| G1-5 | 포인트마다 근거 레퍼런스 파일명 1개 이상, 그 파일이 실제로 있음 |
| G1-6 | 포인트마다 유저스토리 번호(1~5) 1개 이상 |

## G2 — S2→S3 (대상: s2/screens.md)
| ID | 조건 |
|---|---|
| G2-1 | 범위 밖 금지어(out_of_scope) 0개 |
| G2-2 | 모든 화면에 유저스토리 번호 1개 이상, 그중 하나는 flow_stories[flow]에 포함 |
| ★G2-3 | 운동 상태값은 exercise_status.allowed(`미완료`/`완료`) 2개만 등장 |
| ★G2-4 | `완료`로 바뀌는 트리거는 `사용자 체크`만. auto_complete_forbidden 문구 0개 |
| ★G2-5 | 체크를 되돌리는 수단(undo_required_any 중 1개 이상)이 화면 설계에 있음 |
| ★G2-6 | `운동 완료` 화면으로 가는 전이는 `오늘 운동 마치기`(finish_trigger) 하나뿐. 다른 진입 0개 |

## H — S3→S4 사람 승인 (대상: human/approval.md)
- 첫 줄이 `승인` 또는 `반려: {사유}` 중 하나
- 사유 없는 반려는 무효
- 이 파일은 사람만 작성한다. 에이전트는 쓰지 않는다.
- 반려되면 S2로 돌아간다.

## G5 — S5 완료 (대상: s4/export.json)
| ID | 조건 |
|---|---|
| G5-1 | 색: 모든 fill·stroke가 colors.variables 중 하나에 바인딩됨 (binding_required) |
| G5-2 | radius: radius.allowed에 있음 (known_exceptions 제외) |
| G5-3 | 간격: padding과 gap 값이 spacing.allowed에 있음 |
| G5-4 | 그림자: drop shadow 0개 |
| G5-5 | Primary 버튼: 화면당 primary_button_max_per_screen 이하 |
| G5-6 | 타이포: 모든 TEXT에 typography.styles 중 하나가 연결됨 |
| G5-7 | 프레임: 너비 390, 높이 844 이상, 헤더 높이 56 |
| G5-8 | 터치: Button 인스턴스 높이 44 이상 |
| G5-9 | 컴포넌트: rules.json components에 있는 요소는 인스턴스로만 사용 |
| ★G5-10 | 운동 이미지 fill 노드마다 source가 exercise_sources.allowed의 id 중 하나 (출처 없는 이미지 0개) |
| ★G5-11 | s1/refs 레퍼런스 이미지를 화면 안에 그대로 쓴 경우 0건 (타인 저작물) |
| G5-12 | 더미 텍스트에 개인정보 패턴(pii_patterns) 0건 |

★ = story-service.md의 "어기면 안 되는 것"을 지키는 게이트
- 규칙 1 (운동 기록은 사용자가 직접 체크한 것만, 자동 완료 금지) → G2-3, G2-4, G2-5, G2-6
- 규칙 2 (운동 이름·설명·이미지는 출처 표시, 허락된 자료만) → G5-10, G5-11
