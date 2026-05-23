# 테스트 기록

## 빌드 검증

`pnpm build`를 실행하여 TypeScript 프로젝트 빌드, Vite 렌더러 빌드, Electron 메인·프리로드 번들을 검증했습니다. 빌드는 성공했습니다.

| 검증 항목 | 결과 |
|---|---|
| TypeScript 컴파일 | 성공 |
| Vite 프로덕션 빌드 | 성공 |
| Electron 메인 프로세스 번들 | 성공 |
| Electron 프리로드 번들 | 성공 |

## 화면 검증

빌드 후 정적 미리보기 서버에서 앱 화면을 확인했습니다. 앱의 주요 화면은 한국어 UI로 표시되며, 일간·주간·월간·분석·설정 화면 전환이 정상 동작합니다.

| 화면 | 결과 | 스크린샷 |
|---|---|---|
| 일간 보기 | 사이드바, 제목, 날짜, 진행률, 할 일 목록, 입력창, 버튼, 오늘의 기록이 한글로 표시됨 | `deliverables/screenshots/ko_daily_overview.webp` |
| 월간 습관표 | 월간표 제목, 설명, 습관명, 날짜 체크박스, 주차 요약이 한글로 표시됨 | `deliverables/screenshots/ko_monthly_charts.webp` |
| 월간 차트 | 완료·미완료 원형 차트와 일별 체크 수 꺾은선 차트가 월간 화면 상단에 표시됨 | `deliverables/screenshots/ko_monthly_charts.webp` |
| 월간 체크박스 연동 | 체크박스 토글 후 차트 및 주차 요약이 같은 데이터 상태를 기준으로 갱신됨 | `deliverables/screenshots/ko_monthly_chart_interaction.webp` |

## 인터랙션 검증

| 기능 | 결과 |
|---|---|
| 화면 이동 | 일간, 주간, 월간, 분석, 설정 버튼 전환 정상 |
| 할 일 추가 | 입력창에 새 루틴을 입력하고 추가 가능 |
| 할 일 체크 | 체크 상태 변경 시 완료율과 완료·미완료 카운트 갱신 |
| 월간 체크박스 | 날짜별 습관 체크 상태 토글 가능 |
| 월간 원형 차트 | 전체 완료·미완료 집계와 완료율 표시 |
| 월간 꺾은선 차트 | 날짜별 체크 완료 수 표시 |

## macOS 패키징 참고

현재 작업 환경은 Linux이므로 macOS 전용 DMG 생성은 완료하지 않았습니다. 프로젝트에는 macOS 환경에서 실행 가능한 `pnpm pack:mac` 스크립트와 electron-builder DMG 설정이 포함되어 있습니다.
