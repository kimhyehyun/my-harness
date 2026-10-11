# ChriFit Design System

> 출처: Figma `ChriFit Design System` (fileKey `EDcJ9a4nsLkEYJDmZPGi80`)
> - 00 Foundations (`0:1`) · 01 Components (`6:2`) · 02 Screens (`6:3`) · 03 Harness (`35:2`)
> - 값은 Figma 변수(Variables)와 텍스트 스타일에서 그대로 옮겼다. 숫자 규칙의 기계 판정용 사본은 `harness/rules.json`이다.
> - 이전 허들링 모노크롬 규칙은 `docs/design-huddling.md`에 보관한다.

## Overview

ChriFit은 운동 기록 앱이다. 단일 다크 테마로, 거의 검은 배경(`bg` #1E2024) 위에 한 단계씩 밝아지는 surface 사다리로 깊이를 만든다. 색은 민트 액센트(`accent` #1AE7C2) 하나가 "선택·완료·주동작"을 맡고, 보라(`pt` #A78BFA)는 "PT 받은 날" 한 가지 의미에만 쓴다.

**핵심 특징**
- 다크 단일 테마: `bg` → `surface` → `surface-2` → `surface-3` 사다리
- 민트 액센트 = 주동작(Primary 버튼), 선택, 완료. 액센트 위 글자는 `accent-ink`
- 그림자 없음. 깊이는 surface 단계와 1px `line` 테두리로만 표현
- Pretendard 단일 서체(브랜드 워드마크만 Jost)
- 모든 색·radius는 변수에 바인딩, 모든 글자는 텍스트 스타일에 연결

## Colors

컬렉션 `color`. 화면의 모든 fill/stroke는 아래 변수 중 하나에 바인딩한다. hex 직접 입력 금지.

### Surface
| 변수 | 값 | 용도 |
|---|---|---|
| `bg` | #1E2024 | 페이지 배경 |
| `surface` | #26292F | 카드, 검색창, 시트 |
| `surface-2` | #353940 | 시트·입력칸·칩, 보조 버튼 |
| `surface-3` | #434852 | 한 단계 더 밝은 면, 체크박스 테두리 |
| `line` | #2F333A | 카드 테두리, 하단 바 상단선 |
| `divider` | #141719 | 섹션 밴드, 시트 뒤 딤 영역 |

### Text
| 변수 | 값 | 용도 |
|---|---|---|
| `ink` | #FFFFFF | 본문·제목 |
| `ink-2` | #D3D7DE | 낮은 본문 |
| `muted` | #8B909A | 보조 설명, 라벨 |

### Accent
| 변수 | 값 | 용도 |
|---|---|---|
| `accent` | #1AE7C2 | 주동작 버튼, 선택, 완료, 활성 탭 |
| `accent-ink` | #04241C | 민트 위 글자·아이콘 |
| `pt` | #A78BFA | PT 받은 날 (이 의미에만 사용) |

### Alpha
| 변수 | 값 | 용도 |
|---|---|---|
| `alpha/accent-08` | #1AE7C2 8% | 선택된 카드 배경 |
| `alpha/accent-12` | #1AE7C2 12% | 숫자 배지, 활성 탭 배경 |
| `alpha/accent-15` | #1AE7C2 15% | 예비 |
| `alpha/accent-40` | #1AE7C2 40% | 선택된 카드 테두리 |
| `alpha/pt-12` · `pt-40` · `pt-60` | #A78BFA 12/40/60% | PT 표시 |
| `alpha/ink-80` | #FFFFFF 80% | 반투명 글자 |

## Typography

서체: **Pretendard** (Regular 400 · Medium 500 · SemiBold 600 · Bold 700). 브랜드 워드마크만 Jost(앱에서는 Futura). 0.5px 단위 크기는 한글 가독성 때문이므로 반올림하지 않는다.

| 스타일 | 크기 | 굵기 | 자간 | 용도 |
|---|---|---|---|---|
| `brand/wordmark` | 36 | Medium | -2% | 스플래시 로고 |
| `brand/date` | 20 | Bold | 1% | 홈 날짜 |
| `title/screen` | 24 | Bold | -4% | 화면 제목, 카드 헤드라인 |
| `title/sheet` | 23 | Bold | -4% | 시트 제목 |
| `title/group` | 19 | Bold | -3.5% | 그룹 제목, **상단 헤더 제목**, 큰 숫자 |
| `title/card` | 17 | Bold | -3% | 카드 제목 |
| `title/card-sm` | 16.5 | Bold | -3% | 작은 카드 제목 |
| `body/name` | 17 | SemiBold | -3% | 항목 이름 |
| `body/name-sm` | 16.5 | SemiBold | -3% | 작은 항목 이름 |
| `body/base` | 17 | Regular | 0 | 기본 본문 |
| `body/md` | 16 | Regular | 0 | 본문 |
| `body/sm` | 15.5 | Regular | 0 | 본문 |
| `body/15` | 15 | Regular | 0 | 설명 문단 |
| `caption/lg` | 14.5 | Regular | 0 | 보조 설명, 메타 |
| `caption/md` | 14 | Regular | 0 | 라벨 |
| `caption/sm` | 13.5 | Regular | 0 | 작은 안내 |
| `caption/xs` | 13 | Regular | 0 | 요일 등 |
| `label/badge` | 12 | Bold | 0 | 배지, 번호 |
| `label/tab` | 11 | Medium | -2% | 탭 라벨 |

## Layout

### Spacing
컬렉션 `space`.
| 변수 | 값 | 용도 |
|---|---|---|
| `page-x` | 20 | 화면 좌우 여백 |
| `card-p` | 16 | 카드 안쪽 여백 |
| `inside` | 12 | 요소 사이 기본 간격 |
| `group` | 24 | 그룹 사이 |
| `section` | 28 | 섹션 사이 |

보조 간격: 4 · 6 · 8 · 10 · 14 · 18 · 20 · 32 · 48 (짝수 단위, 2px 스텝).

### Screen
| 항목 | 값 |
|---|---|
| 프레임 너비 | 390 (고정) |
| 최소 높이 | 844. 내용이 길면 세로로 늘린다 |
| 상단 헤더 | 높이 56 고정, 세로 가운데 정렬 |
| 하단 탭 바 | `Tab Bar` 인스턴스, 높이 58, 화면 맨 아래 |
| 하단 액션 바 | `bg` 배경 + 상단 1px `line`, 탭 바 바로 위 |

### Header 규칙
- Today: 왼쪽에 날짜·요일과 날씨 칩, 오른쪽에 메뉴 아이콘을 배치한다 ([오늘 화면](screens/main.png))
- Library, History: 왼쪽 `title/screen` 제목
- 그 밖의 화면: ← `Icon/chevron-left` 22 + 가운데 `title/group` 제목 + 오른쪽 22 여백
- 시트: `Sheet Header` + 오른쪽 `Icon/x` 22 닫기

### Splash 화면 구성

[스플래시 화면 캡처](screens/Splash.png)를 기준으로 `bg` 배경 중앙에 `accent` 마스코트(`Mark/Mascot`)를 두고, 그 아래에 흰색(`ink`) ChriFit 워드마크를 배치한다. 다른 장식이나 조작 요소는 넣지 않는다.

### Today 화면 구성

[오늘 화면 캡처](screens/main.png)를 홈 화면의 시각적 기준으로 삼는다.
- 상단: 날짜·요일, 날씨 칩, 메뉴 아이콘
- 선택 방식: `직접 고르기`와 `스마트 랜덤` 카드를 나란히 배치한다. 선택한 카드는 `accent` 테두리와 `alpha/accent-08` 배경으로 구분한다
- 탐색: 검색 필드 아래에 즐겨찾기·부위·기구 필터를 하나의 `surface` 영역으로 묶는다
- 목록: 운동 개수와 `내 운동` 제목 다음에 사진·이름·부위/기구·선택 표시·즐겨찾기 아이콘이 있는 행을 배치한다
- 하단: `Tab Bar`의 `오늘`을 활성 상태로 표시한다

## Shapes

컬렉션 `radius` (Tailwind 기본값의 0.75배로 재정의).
| 변수 | 값 | 용도 |
|---|---|---|
| `xs` | 1.5 | |
| `sm` | 3 | |
| `md` | 4.5 | 배지 |
| `lg` | 6 | 칩, 체크박스 |
| `xl` | 9 | Md 버튼, 아이콘 타일 |
| `2xl` | 12 | Lg 버튼, 입력칸, 리스트 카드 |
| `3xl` | 18 | 큰 카드, 시트 상단, 썸네일 |
| `4xl` | 24 | |
| (pill) | 999 | 알약형 버튼(전체 선택 등), 점 |

중첩 규칙: 바깥 radius = 안쪽 radius + 여백.

## Elevation
그림자는 쓰지 않는다. 깊이는 아래 두 가지로만 표현한다.
1. surface 단계 차이 (`bg` < `surface` < `surface-2` < `surface-3`)
2. 1px `line` 테두리, 선택 상태는 1.5px `alpha/accent-40` 테두리 + `alpha/accent-08` 배경

## Components (01 Components)

| 컴포넌트 | 변형 | 비고 |
|---|---|---|
| `Button` | Size: Lg(56) · Md(48) / Style: Primary · Secondary · Ghost | Primary = accent 채움. 한 화면 Primary 1개 |
| `Chip` | State: Default · Done · Remove | 운동 태그 |
| `Badge` | Type: Today · PT | |
| `Field` | 아이콘 · 값 · 단위 | 숫자 입력 |
| `Exercise Row` | Selected: False · True | 운동 목록 행, 썸네일 52 |
| `Tab Bar` | Active: Today · Library · History | |
| `PT Toggle` | State: Off · On | |
| `Record Card` | — | 기록 카드 |
| `Sheet Header` | — | 시트 손잡이 + 제목 |
| `Icon/*` | 21종 (24 기준) | 크기는 rescale로 조절 |
| `Mark/Mascot` · `Mark/Bloom` | — | 브랜드 마크 |

새 화면은 위 컴포넌트의 인스턴스로 조립한다. 같은 역할의 요소를 새로 그리지 않는다.

## Do's and Don'ts

### Do
- 모든 fill/stroke를 `color` 변수에 바인딩한다
- 모든 텍스트에 텍스트 스타일을 연결한다
- radius는 `radius` 변수(또는 pill 999)만 쓴다
- 주동작은 `Button / Primary` 1개, 보조는 Secondary, 취소·해제는 Ghost
- 선택 상태는 `alpha/accent-08` 배경 + `alpha/accent-40` 테두리
- 운동 이미지는 썸네일 radius `3xl`·`2xl` 안에 FILL로 넣는다

### Don't
- hex 직접 입력, 변수 없는 색
- 그림자(drop shadow)
- `pt` 보라를 PT 외의 의미로 사용
- radius 20처럼 스케일에 없는 값 (알려진 예외: `Sheet Header` 컴포넌트 원본이 20 → 인스턴스에서 `3xl`로 덮어씀, 원본 수정 필요)
- 텍스트 스타일 없는 글자

## 하네스 적용 기록 (03 Harness)
키스크린 `Today`(22:145) 1장을 기준으로 4개 화면을 만들었다.
| 화면 | 노드 | 진입 |
|---|---|---|
| History | 37:22 | 탭 바 "기록" |
| Add Exercise Sheet | 37:23 | "운동 추가" |
| Exercise Detail | 37:24 | "설명 보기" |
| Workout Done | 37:25 | "오늘 운동 마치기" |

운동 이름·이미지 출처: fitnessprogramer.com (Chest). 이미지 사용은 허락받았다.
