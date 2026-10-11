# 산출물

> 파이프라인: harness/pipeline.md · 규칙 SSOT: harness/rules.json

## 실행 폴더
실행할 때마다 runs/{플로우}/ 폴더를 하나 만든다.
플로우 이름은 7개로 고정한다:
free-browse / paid-library / skill-card / mission-submit /
asset-register / sale-request / admin-review

```
runs/{플로우}/
├─ state.json                # 오케스트레이터만 씀. 현재 스테이지, 반복 횟수
├─ s1/refs/*.png
├─ s1/refs/index.md          # 출처 URL, 앱 이름, 화면 유형 (이미지마다 1행)
├─ s1/points.md              # 반영 포인트 3~7개
├─ s2/screens.md             # 화면 설계
├─ s3/keyscreens.json        # Figma 노드 ID 2~3개
├─ human/approval.md         # 사람만 씀. 승인/반려 + 사유
├─ s4/export.json            # Figma 노드별 색, radius, 간격, effect 값
└─ s5/report.json            # 위반 목록, 위반 건수
```

## 스테이지별 산출물
| 스테이지 | 남기는 파일 |
|---|---|
| S1 | s1/refs/*.png, s1/refs/index.md, s1/points.md |
| S2 | s2/screens.md |
| S3 | s3/keyscreens.json (승인 기록 human/approval.md는 사람이 씀) |
| S4 | s4/export.json (Figma에도 실제 화면이 그려짐) |
| S5 | s5/report.json |

## Figma 결과물 판정 방식
- S4 에이전트가 작업을 마칠 때 Figma에서 노드별 값을 뽑아 s4/export.json으로 저장한다.
- 판정 스크립트는 s4/export.json만 읽는다. Figma에는 접근하지 않는다.

## 규칙 SSOT
- harness/rules.json 1개. 숫자 값은 R5에서 확정한다.
  - design.md(ChriFit)에서 뽑은 값: color 변수, radius 변수, space 변수, 텍스트 스타일, shadow 0개, Primary 버튼 개수
  - 프레임 너비 390, 최소 높이 844, 헤더 높이 56
  - 플로우 7개, Phase 2 금지 화면 목록
  - 레퍼런스 개수 제한 (유형별 3~5장, 전체 15장 이하)
  - Figma fileKey
- docs/design.md는 사람이 읽는 원본이다. rules.json과 다르면 design.md가 이기고, rules.json을 고친다.
- docs/design2.md는 읽지 않는다.

## 재개
- state.json에 마지막으로 통과한 스테이지와 S5→S4 반복 횟수를 기록한다.
- 다시 시작하면 마지막으로 통과한 스테이지의 다음부터 진행한다.
- 이미 통과한 스테이지의 파일은 덮어쓰지 않는다. 단, 되돌아간 경우(S3 반려 → S2, S5 위반 → S4)는 예외로, 해당 스테이지 파일을 새로 쓴다.
