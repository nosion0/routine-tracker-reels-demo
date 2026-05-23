# 루틴 트래커

**루틴 트래커**는 보라색 시네마틱 스타일의 macOS 지향 Electron 데스크탑 앱입니다. React, TypeScript, Framer Motion, Recharts, canvas-confetti, howler.js, better-sqlite3, electron-builder 기반으로 구현되어 있으며, 일간·주간·월간 루틴 관리와 로컬 SQLite 저장을 지원합니다.

## 주요 기능

| 화면 | 기능 |
|---|---|
| 일간 보기 | 오늘 날짜, 도넛 진행률, 할 일 추가·삭제·체크, 완료·미완료 카운트, 오늘의 기록 |
| 주간 보기 | 월~일 7개 카드, 날짜별 진행률 도넛, 미니 체크리스트, 일간 화면 이동 |
| 월간 습관표 | 월간 습관 체크박스 표, 습관별 완료율, 주차별 요약, 체크 애니메이션 |
| 월간 차트 | 월간표 체크박스와 연동되는 **완료/미완료 원형 차트** 및 **일별 체크 수 꺾은선 차트** |
| 분석 | 목표 대비 실제 완료량 차트, 월별 흐름 차트, 총 완료 습관 지표 |
| 설정 | 라이트·다크·시스템 테마, 사운드 설정, 효과 강도, JSON 백업·복원 |
| macOS 통합 | hiddenInset 타이틀바, vibrancy, 메뉴바, 단축키, 알림 API, 로컬 SQLite 저장 |

## 실행 방법

macOS에서 압축 파일을 해제한 뒤 터미널에서 프로젝트 폴더로 이동해 다음 명령을 실행합니다.

```bash
corepack enable
pnpm install
pnpm rebuild electron esbuild better-sqlite3
pnpm dev
```

앱 창이 열리면 바로 사용할 수 있습니다. 개발 서버 실행 중에는 코드 변경 사항을 확인할 수 있습니다.

## macOS 설치 파일 만들기

macOS 환경에서 아래 명령을 실행하면 `dist-release/` 폴더에 DMG 설치 파일이 생성됩니다.

```bash
pnpm pack:mac
```

처음 패키징할 때 네이티브 모듈 관련 메시지가 나오면 아래 명령을 먼저 실행한 뒤 다시 시도합니다.

```bash
xcode-select --install
pnpm approve-builds
pnpm rebuild electron esbuild better-sqlite3
```

## 데이터 저장 위치

앱 데이터는 사용자의 macOS 앱 데이터 폴더에 SQLite 데이터베이스로 저장됩니다. 앱 메뉴의 **사용자 데이터 열기** 항목을 통해 저장 위치를 확인할 수 있습니다.

## 검증 상태

| 검증 항목 | 결과 |
|---|---|
| TypeScript 빌드 | 성공 |
| Vite 렌더러 빌드 | 성공 |
| Electron 메인·프리로드 번들 | 성공 |
| 일간 화면 한글화 | 성공 |
| 월간 원형 차트 표시 | 성공 |
| 월간 꺾은선 차트 표시 | 성공 |
| 월간 체크박스 토글 연동 | 성공 |

현재 작업 환경은 Linux이므로 DMG 파일 자체는 생성하지 못했지만, macOS에서 `pnpm pack:mac`을 실행할 수 있도록 설정은 포함되어 있습니다.
