# 하네스 목적

> 판정 기준: docs/story-service.md · 작업 흐름: docs/story-work.md · 규칙 원본: docs/design.md

## 매번 달라지는 것 (입력)
- 이번에 만들 플로우 1개. PRD §5의 5개 중에서 고른다.
  pick-today(오늘 운동 고르기) / find-exercise(운동 찾기·추가) / do-session(운동 진행) /
  finish-workout(운동 마치기) / review-history(기록 보기)
- 고정(매번 같음): docs/prd.md, docs/design.md, Figma ChriFit Design System
- 범위: PRD §4 MVP 화면만. PRD §10 범위 밖(로그인, 결제, 커뮤니티 등)은 만들지 않는다.

## 사용자 (결과물을 받는 사람)
- 디자이너(나)
- 4·5단계에서 컨펌하는 내부 관계자
- 앱 사용자(운동하는 사람)는 결과물을 받는 사람이 아니라 판정 기준이다 → story-service.md

## 완료 기준 (한 문장)
선택한 플로우의 화면이 ChriFit Figma 파일에 너비 390(최소 높이 844)으로 그려졌고,
ChriFit 변수·텍스트 스타일·컴포넌트만 써서 design.md 위반 0건과 ★게이트 위반 0건으로 검사를 통과했으며,
사람이 컨펌을 1회 했다.

## "위반 0건"이 세는 것 (기준: docs/design.md, 숫자는 rules.json)
1. 색: 모든 fill/stroke가 ChriFit color 변수에 바인딩됨 (변수 없는 색 0개)
2. radius: 0 / 1.5 / 3 / 4.5 / 6 / 9 / 12 / 18 / 24 / 999만 허용
3. 텍스트: 모든 글자에 ChriFit 텍스트 스타일 연결 (스타일 없는 글자 0개)
4. drop shadow: 0개
5. Primary 버튼: 화면당 1개 이하
6. ★ 운동 완료는 사용자 체크로만, 운동 이미지는 출처가 있는 것만
