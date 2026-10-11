# 실행 기록 — chrifit

> Figma: ChriFit Design System (`EDcJ9a4nsLkEYJDmZPGi80`) · 페이지 `03 Harness` (`35:2`)
> 규칙: docs/design.md · harness/rules.json · 판정 기준: docs/story-service.md (ChriFit)

## S3 키스크린
| 파일 | Figma 노드 |
|---|---|
| ![](s3/keyscreen-today.png) `s3/keyscreen-today.png` | Today `22:145` (02 Screens) |

## S4 화면 (키스크린 1장 → 4장)
| # | 화면 | 진입 | Figma 노드 | 이미지 |
|---|---|---|---|---|
| 1 | History | 탭 바 "기록" | `37:22` | `s4/01-history.png` |
| 2 | Add Exercise Sheet | "운동 추가" | `37:23` | `s4/02-add-exercise-sheet.png` |
| 3 | Exercise Detail (덤벨 풀오버) | "설명 보기" | `37:24` | `s4/03-exercise-detail.png` |
| 4 | Workout Done | "오늘 운동 마치기" | `37:25` | `s4/04-workout-done.png` |

<p>
<img src="s4/01-history.png" width="180"> <img src="s4/02-add-exercise-sheet.png" width="180"> <img src="s4/03-exercise-detail.png" width="180"> <img src="s4/04-workout-done.png" width="180">
</p>

## S5 검토
`s5/report.json` — 1회차 위반 1건(Sheet Header radius 20) → 인스턴스를 `3xl`로 덮어써 0건.

판정 기준을 ChriFit PRD로 바꾼 뒤(★G5-10 이미지 출처) 운동 이미지 노드 6개에 `source=fitnessprogramer`를 레이어 이름으로 달았다.

## 사람 피드백으로 바뀐 것
1. 운동 이름: 임의 예시 → fitnessprogramer.com Chest 목록(덤벨 풀오버 등)
2. 운동 사진 추가 (같은 사이트, 시안용·배포 전 교체 필요)
3. 운동 완료: 마스코트 → 폭죽 (색은 accent·pt·ink-2 변수)
4. 상단 헤더: 없던 화면에 ← / X 추가, 높이 56 통일, 제목 title/group(19 Bold)
5. Exercise Detail 헤더 제목: "운동 설명" → "덤벨 풀오버"
