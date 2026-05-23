# 루틴 트래커 빌드 및 전달 보고서

## 개요

첨부 프롬프트를 기준으로 제작한 **보라색 시네마틱 스타일의 macOS 지향 루틴 트래커 데스크탑 앱**을 추가 개선했습니다. 이번 수정에서는 앱 내 표시 문구를 한글 중심으로 정리하고, **월간 습관표의 체크박스 상태와 직접 연동되는 차트 2개**를 월간 화면에 추가했습니다. 앱은 Electron, React, TypeScript 기반이며 로컬 SQLite 저장 구조를 유지합니다.

| 구분 | 내용 |
|---|---|
| 앱 이름 | 루틴 트래커 |
| 대상 플랫폼 | macOS 우선, Electron 기반 데스크탑 앱 |
| 프론트엔드 | React, TypeScript, Framer Motion, Recharts |
| 데스크탑 런타임 | Electron |
| 로컬 저장소 | better-sqlite3 기반 SQLite |
| 패키징 | electron-builder, macOS DMG 설정 포함 |

## 반영된 변경사항

| 요청 항목 | 반영 내용 |
|---|---|
| 전체 한글화 | 사이드바, 화면 제목, 버튼, 상태값, 메뉴, 설정, 샘플 데이터, 앱 표시 이름을 한글로 수정 |
| 월간 원형 차트 | 월간 습관표 체크박스의 완료·미완료 수를 집계해 완료율 원형 차트로 표시 |
| 월간 꺾은선 차트 | 날짜별 체크 완료 수를 계산해 일별 흐름 꺾은선 차트로 표시 |
| 체크박스 연동 | 월간표 체크박스를 클릭하면 원형 차트, 꺾은선 차트, 주차 요약이 같은 데이터 상태를 기준으로 즉시 갱신 |
| 문서 갱신 | README, 빌드 보고서, 테스트 기록을 수정된 한글 UI와 차트 기능 기준으로 업데이트 |

## 구현된 주요 기능

| 화면 | 구현 내용 |
|---|---|
| 일간 보기 | 오늘 날짜 표시, 할 일 추가·삭제·체크, 완료율 도넛, 완료·미완료 카운트, 오늘의 기록 저장 영역 |
| 주간 보기 | 월~일 7일 카드, 날짜별 진행률 도넛, 현재 날짜의 할 일 요약, 날짜 선택 시 일간 보기 이동 |
| 월간 습관표 | 월간 습관 체크 그리드, 습관별 완료율, 주차별 요약, 클릭 시 시각 효과 |
| 월간 차트 | 완료·미완료 원형 차트, 일별 체크 수 꺾은선 차트, 월간 체크박스와 실시간 연동 |
| 분석 | 목표 대비 실제 완료량 차트, 월간 흐름 라인 차트, 완료 습관 총계 표시 |
| 설정 | 라이트·다크·시스템 테마, 사운드 설정, 효과 강도, JSON 백업·복원 |
| macOS 통합 | hiddenInset 타이틀바, vibrancy, 메뉴바, 단축키, 로컬 알림 구조 |

## 검증 결과

`pnpm build`를 실행하여 TypeScript 빌드, Vite 렌더러 빌드, Electron 메인·프리로드 번들을 검증했습니다. 빌드는 성공했으며, 정적 미리보기 서버에서 한글 UI, 월간 차트 표시, 월간 체크박스 토글 연동을 확인했습니다.

| 검증 항목 | 결과 |
|---|---|
| TypeScript 빌드 | 성공 |
| Vite 프로덕션 빌드 | 성공 |
| Electron 메인·프리로드 번들 | 성공 |
| 일간 보기 한글 UI 렌더링 | 성공 |
| 월간 습관표 한글 UI 렌더링 | 성공 |
| 완료·미완료 원형 차트 표시 | 성공 |
| 일별 체크 수 꺾은선 차트 표시 | 성공 |
| 월간 체크박스 토글 후 차트 갱신 | 성공 |

## macOS DMG 패키징 상태

프로젝트에는 다음 명령으로 macOS에서 DMG를 만들 수 있는 설정을 포함했습니다.

```bash
corepack enable
pnpm install
pnpm rebuild electron esbuild better-sqlite3
pnpm pack:mac
```

현재 작업 환경은 Linux이므로 macOS 전용 DMG 생성은 완료할 수 없었습니다. Electron 네이티브 모듈인 `better-sqlite3`는 macOS용 Electron ABI로 재빌드되어야 하므로 실제 `.dmg` 생성은 macOS 로컬 또는 macOS CI 환경에서 실행해야 합니다.

> macOS에서 빌드하면 `dist-release/` 폴더에 DMG 산출물이 생성됩니다. Apple Developer ID 서명이 필요한 배포용 빌드라면 별도의 코드 서명 인증서와 notarization 설정을 추가해야 합니다.

## 실행 방법

개발 실행은 다음과 같습니다.

```bash
corepack enable
pnpm install
pnpm rebuild electron esbuild better-sqlite3
pnpm dev
```

프로덕션 빌드는 다음과 같습니다.

```bash
pnpm build
```

macOS DMG 패키징은 macOS 환경에서 다음과 같이 실행합니다.

```bash
pnpm pack:mac
```

## 포함 산출물

| 파일 | 설명 |
|---|---|
| `routine-tracker-source.zip` | 전체 앱 소스 코드와 문서, 테스트 스크린샷을 포함한 압축 파일 |
| `BUILD_REPORT.md` | 구현·빌드·테스트 결과 보고서 |
| `TEST_NOTES.md` | 화면별 검증 기록과 스크린샷 경로 |
| `deliverables/screenshots/` | 한글 UI 및 월간 차트 검증 화면 캡처 |
