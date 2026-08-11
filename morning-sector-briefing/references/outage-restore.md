# 소스 장애·복구 전환 절차

소스 상태가 바뀐 것으로 의심될 때만 읽는다. 전환 후엔 SKILL.md "소스 상태" 섹션을 반드시 함께 갱신.

## UsStockInfo — 정상 상태 경로 (복구 시 되돌릴 내용)

**복구 확인 방법**: ToolSearch로 `UsStockInfo-get_stock_info` 스키마 로드 시도 — 성공하면 정상화. 아래 항목을 정상 경로로 되돌리고 **예산 63/64/66 → 64/65/67 원복**.

| 항목 | 정상 상태 경로 |
|---|---|
| MCP-2.5(VIX)·MCP-3(SPY)·MCP-4(QQQ) | `UsStockInfo-get_stock_info(ticker="^VIX"/"SPY"/"QQQ")` 개별 3회 (통합 1회 → 3회, +2). SPY·QQQ는 `postMarketChangePercent` 사용 |
| MCP-5 | `UsStockInfo-get_finance_news(ticker="SPY")` [1회] → 신호: ±5%+=강 · ±2~4%=중 · ±2%-=약. 강/중 신호 종목 1~2개→MCP-9·강화-B·G 대상(없으면 MCP-9 생략). 후보 섹터 최대 1개→MCP-7 후보. 목표주가·투자의견 변경→⑤기관의견 |
| MCP-9 | `UsStockInfo-get_finance_news(ticker="[MCP-5 핵심 US티커]")` [조건부 1회, MCP-5 강/중신호 시만] → 목표주가상향·투자의견변경 우선 포착 |
| 강화-B | **원복 대상 아님** — SEC 공식 소스인 OpenInsider-MCP로 영구 이관(SKILL.md 강화-B 참고). UsStockInfo 경로(`get_holder_info` insider_transactions)로 되돌리지 않는다 |
| 강화-G | `UsStockInfo-get_recommendations(ticker="...", recommendation_type="recommendations")` [1회] → `period "0m"` 기준 매수비율=(strongBuy+buy)/전체. -1m/-2m 추세를 근거서술 병기(점수기준은 0m 스냅샷) |
| 강화-B·G 대상 티커 | MCP-5 결과 그대로 사용(검색2c-B 폴백 해제) |

**재단절 시**: 위 표의 역방향 — SKILL.md "소스 상태"의 현재 경로(Bigdata 통합·폴백 티커·B/9 생략)로 전환, 예산 64/65/67 → 63/64/66.

## NaverSearch — 재단절 시 전환

NaverSearch가 다시 끊기면: 검색1·MCP-7·조건부-C·조건부-D2·MCP-SEASON·정책1~2를 전부 `web_search_exa`로 전환(`numResults`=기존 `display` 값 그대로). 복구 확인되면 현재 배치(SKILL.md "소스 상태")로 원상복구.

## 데이터 항목별 소스 우선순위 (폴백 체인)

새 장애 발생 시 이 표의 다음 순위로 전환하고 SKILL.md "소스 상태"를 갱신. "(현재)"는 2026-08-11 기준 적용 중인 경로.

| 데이터 | 1순위 | 2순위 | 폴백 소진 시 |
|---|---|---|---|
| 미국 시세(VIX·SPY·QQQ) | UsStockInfo 개별 3회 | Bigdata tearsheet 통합 1회 (현재) | 생략, VIX 등급조정 조건 판정 제외 |
| 미국 종목뉴스(MCP-5·9) | UsStockInfo | 없음 (현재 생략, 티커 소싱만 검색2c-B 폴백) | 생략 |
| 미국 내부자매수(강화-B) | OpenInsider-MCP `search_by_ticker` (커넥터 연결 시) | 없음 (미연결이면 생략) | 0점 처리, 서술 없음 |
| 미국 매수비율(강화-G) | UsStockInfo 1회 | Bigdata 2회 (현재) | 생략 |
| 국내 뉴스검색 | NaverSearch (현재) | web_search_exa (numResults=display) | 해당 항목 생략 |
| 국내 공시 | opendart-* + easyGongsi (현재) | — | 해당 강화신호 생략 |
| 국내 수급(외국인/기관) | pykrx-mcp 확정치 (커넥터+KRX 계정 시 — 검색1.5·조건부-D2⓪) | 뉴스 텍스트 추정 (현재) | 갭③ 미확인 처리 |

※ pykrx-mcp·OpenInsider-MCP 경로는 "커넥터 연결 시" 게이트로 SKILL.md에 반영돼 있음 — 미연결 상태에선 각 항목의 다음 순위가 그대로 작동. 커넥터 등록 절차는 프로젝트 UPGRADE-PLAN 문서 참고.

## 상태 이력

- UsStockInfo: 2026-08-07 마지막 정상 실행 확인 → 2026-08-11 단절 확인, Bigdata 폴백 적용 중.
- NaverSearch: 2026-07-28 장애로 전면 Exa 전환 → 2026-08-11 복구 확인, 항목별 재배치 적용 중.
