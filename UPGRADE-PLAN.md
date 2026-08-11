# morning-sector-briefing 업그레이드 플랜

2026-08-11 오픈소스 조사(GitHub API 실측) + **로컬 실설치 검증**(맥, uvx/npx로 서버 기동해 stdio 핸드셰이크·실데이터 호출) 기반. 스킬 본체(SKILL.md)에는 설치 전 커넥터를 참조하지 않는다(죽은 참조 금지) — 예외적으로 검증 완료된 OpenInsider-MCP는 "연결 시 실행" 게이트와 함께 반영됨.

## 우선순위 로드맵

### ② 미국 내부자매매 부활 — OpenInsider-MCP ✅ 검증 완료·SKILL.md 반영됨
- **실검증 결과 (2026-08-11)**: `npx -y openinsider-mcp` 기동 성공(v0.3.0), 도구 16종 확인, NVDA 실데이터 호출 성공. 응답이 구조화 필드(`transactionType`="P - Purchase"/"S - Sale", `title` 직위, `price`, `value`, `formUrl` SEC Form 4 원문 링크)로 옴 — 야후의 텍스트 접두사 파싱보다 판정 명확, 출처 링크 규칙에도 부합. 키 불필요.
- **SKILL.md 반영됨**: 강화-B가 `search_by_ticker` 기반으로 재정의됨(커넥터 미연결 시 기존대로 생략하는 게이트 포함, 예산 변화 없음). UsStockInfo 복구와 무관하게 이 소스 유지.
- **남은 작업**: 실행 머신(Windows) Claude 환경에 커넥터 등록만 하면 활성화 — `npx -y openinsider-mcp` (Claude Desktop이면 MCP 설정에 command=`npx`, args=`["-y","openinsider-mcp"]`).
- **추가 활용 후보(호출 추가라 예산 검토 후)**: `cluster_buys`(다수 임원 동시매수 — 시장 전체 스캔이라 티커 불요, 미국 직접 기회 발굴 소스로 승격 가능), `dilution_filings`(S-3/424B5 증자 준비 = 강화-CAP의 미국판 역신호).
- **대안**: sec-edgar-mcp(346★) — 더 정식 파싱이나 AGPL-3.0.

### ① 국내 수급을 공식 수치로 교체 — pykrx-mcp ✅ SKILL.md 게이트 반영됨 (수급은 KRX 계정 선결)
- **현황**: 외국인/기관 수급을 네이버 뉴스 기사의 "지속·연속" 문구 판독으로 추정(검색1·조건부-D2·등급조정 1번 조건). 파이프라인에서 가장 약한 고리.
- **실검증 결과 (2026-08-11) — README 주장과 3가지 차이**:
  1. **의존성 버그**: 그냥 실행하면 `mcp` SDK 2.x와 비호환으로 즉사 → **`uvx --with "mcp<2" pykrx-mcp`로 실행해야 함** (v1.29.0 기동 확인).
  2. **도구 8종만 노출** (README의 23종 아님): `get_stock_ohlcv`, `get_market_ticker_list/name`, `get_market_fundamental_by_date`, `get_market_cap_by_date`, **`get_market_trading_value_by_date`**(종목별 투자자 수급 — 핵심 용도는 충족), `get_etf_ohlcv_by_date`, `get_etf_ticker_list`. 외국인 순매수 상위 랭킹(`get_market_net_purchases_of_equities`)·공매도·한도소진률은 MCP에 미노출 → 후보 발굴 소스 용도는 불가, **갭③/조건부-D2/등급조정 1번 판정 용도는 가능**.
  3. **KRX 로그인 필요**: pykrx가 이제 투자자별 수급 조회에 KRX 정보데이터시스템 로그인(`KRX_ID`/`KRX_PW` 환경변수)을 요구함(무료 계정). OHLCV는 로그인 없이 정상(삼성전자 실데이터 수신 확인).
- **선결 조건**: KRX 정보데이터시스템(data.krx.co.kr) 무료 계정 생성 → 커넥터 등록 시 env로 `KRX_ID`/`KRX_PW` 주입.
- **타이밍 주의**: KRX 확정 수급은 당일 18시 이후 제공 → 08:30 브리핑은 전영업일 확정치 사용(현행 뉴스 추정도 전일 기준이라 정합성 동일, 정확도만 상승).
- **KRX Open API(공식 무료)에는 투자자별 매매동향이 없음을 실측 확인** — pykrx 계열이 유일한 실질 경로. 장중 가집계는 KIS API뿐(MCP 부재, 보류).
- **SKILL.md 반영됨 (전부 "연결 시" 게이트 — 미연결이면 기존 경로 그대로)**:
  - 검색1.5 [pykrx-KOSPI] 신설: 최근 5거래일 외국인 순매수 합산으로 등급조정 1번 판정(예산 +1 → 64/65/67). KOSPI 인덱스 티커 지원은 첫 실행에서 확인하도록 가드.
  - 조건부-D2에 ⓪순위 추가: 종목별 수급 확정치로 갭③ 판정(기존 ①을 대체, 호출 수 불변).
  - 강화-TA 대체 경로: `get_stock_ohlcv` 1년치(로그인 불요!)로 koreaStock 호출 대체 — **실제 52주고점** 산출로 60일 근사 문제 해소. 한화시스템 실데이터로 검증 완료(52주고점 184,000원 대비 -58% 정확 산출, 20일선 상회로 등급조정 4번 미발동 판정 정상).
- **활성화 절차**: KRX 정보데이터시스템 무료 계정 생성(수급용 — TA 대체 경로는 계정 없이도 작동) → 커넥터 등록: command=`uvx`, args=`["--with","mcp<2","pykrx-mcp"]`, env=`KRX_ID`/`KRX_PW`.

### ⑤ DART 시그널 강화 — korean-dart-mcp 🟡 기동 검증 완료, 데이터 검증은 실행 머신에서
- [chrisryugj/korean-dart-mcp](https://github.com/chrisryugj/korean-dart-mcp) (90★). 기존 OpenDART 키 재사용.
- **실검증 결과 (2026-08-11)**: `npx -y korean-dart-mcp` 기동 성공(v0.9.2), 도구 18종 확인. 환경변수명은 **`DART_API_KEY`**(OPENDART_API_KEY 아님). 데이터 호출 검증은 실키가 있는 실행 머신에서 필요.
- **추가 발견**: `resolve_corp_code`가 회사명·종목코드를 바로 받고 "상장사·정확일치 우선" 정렬로 반환 — 파라미터 실수로 100% 실패 이력이 있는 강화-F1(`opendart-find_company`)의 대체 후보. `get_corporate_event`(증자·감자 36종 타임라인)는 강화-CAP 보강 후보.
  - `insider_signal`: 임원매매 매수/매도 집계 + `strong_buy_cluster` 라벨 + 한국어 한 줄 요약 → 강화-D1의 원시 테이블 판독을 대체(토큰 절감 + 판정 안정화)
  - `disclosure_anomaly`: 정정공시 비율 기반 회계리스크 0-100점(`clean/watch/warning/red_flag`) → 재무취약 축의 보강 신호 후보
  - `search_disclosures(preset=…)` 22종: "최근 30일 자기주식 취득 전체", "유상증자·CB 발행"을 종목 미지정 시장 전체 스캔 → 후보 발굴 단계 신규 소스
- **주의**: README 주장 수치(실측 예시)는 미검증 — 도입 시 1주 병행 운영으로 기존 opendart-* 결과와 대조 후 교체.

### ③④ 기술지표 스크립트 — ✅ 적용 완료
- `scripts/compute_ta.py` 동봉(표준 라이브러리만, 합성 데이터 테스트 통과). 값+한국어 해석+등급조정 4번 조건 발동 여부까지 반환.
- 근거 패턴: korea-stock-analyzer-mcp "LLM도 서버도 암산하지 않는다", momentum-mcp의 값+평문 해석 동반 반환.
- **활성화 조건**: 실행 환경(Windows 예약작업)에서 Python 실행 가능 여부 확인 필요. 불가하면 SKILL.md의 폴백(직접 계산)이 그대로 작동.

### ⑦ 폴백 체인 명시화 — ✅ 적용 완료
- references/outage-restore.md에 데이터 항목별 소스 우선순위 표 추가(awesome-stock-skills의 3-tier 폴백 패턴).

### ⑥ 거시 축 확장 — korea-finance-mcp (선택)
- [emceeKim/korea-finance-mcp](https://github.com/emceeKim/korea-finance-mcp) (53★, 원격 MCP URL 등록만). ECOS 기준금리·CPI·M2 + `correlate_macro_stock`(시차 상관) → 강화-MACRO의 판단 재료 확장. 우선순위 낮음(현행 환율·금리·VIX로도 작동).

### ⑨ 자기채점 루프 (이미 부분 구현)
- backtest-track-record.md + weekly-action-review가 이 역할을 이미 수행 중. 개선 여지: 등급별(🔴/🟢/🟡) 적중률을 분리 집계해 갭 점수 임계값(예: -50% 규칙, VAL 10% 기준 등 "시작값·재검토 대상"으로 표시된 것들)을 데이터로 재보정. TradingAgents-KR의 hit/miss 채점 루프 참고.

### ⑧ 증권사 리포트 목표주가 직접 추출 (보류 — 🔴 수일 소요)
- Luriar/opik 방식(네이버 금융 리포트 PDF → 정규식 추출). 조건부-C(뉴스 기반 목표주가)의 상위 호환이지만 구축 비용 큼. 조건부-C가 충분히 작동하는 동안 보류.

### KIS(한국투자증권) API (보류)
- 데이터 커버리지는 최상(장중 수급 가집계 `foreign_institution_total` 포함 156개 엔드포인트 실측)이나 **쓸만한 MCP 서버가 부재**(최대 0~3★) — 직접 구축 필요. 08:30 브리핑엔 장중 데이터가 불필요하므로 우선순위 최하.

## 조사에서 발견된 기존 스킬의 잠재 이슈

1. **52주고점을 60일 데이터로 계산**: 강화-TA가 60거래일 rows에서 "52주고점 대비 하락률"을 산출하는데, 60일 표본으로는 구조적으로 52주 고점을 알 수 없음(표본 내 최고가 근사가 됨 → 하락률 과소평가 → 등급조정 4번 조건 미발동 위험). 강화-P(`stock_get_quote`) 응답에 52주고가 필드가 있는지 확인 후, 있으면 그 값을 compute_ta.py의 `w52_high`로 전달하도록 운영. 스크립트는 근사 사용 시 경고 문구를 붙이도록 이미 처리됨.
2. **"국장 장전 브리핑 자동화" 오픈소스는 사실상 무주공산**(★2 이상 1개) — 이 스킬 자체가 해당 분야에서 가장 정교한 축에 속함. 참고할 선례보다 부품(MCP 커넥터)을 가져다 쓰는 전략이 맞음.

## 권장 착수 순서 (2026-08-11 검증 후 갱신)

스킬 통합은 전부 완료(게이트 방식) — 남은 것은 실행 머신(Windows)에서의 활성화뿐:

1. **OpenInsider-MCP 등록** — `npx -y openinsider-mcp`, 키 불필요 → 강화-B 즉시 부활.
2. **pykrx-mcp 등록** — command=`uvx`, args=`["--with","mcp<2","pykrx-mcp"]` → 강화-TA 52주고점 경로는 바로 활성화(로그인 불요). 수급(검색1.5·D2⓪)까지 쓰려면 KRX 무료 계정 생성 후 env `KRX_ID`/`KRX_PW` 추가.
3. **⑤ korean-dart-mcp** — env `DART_API_KEY`(기존 OpenDART 키 재사용)로 등록 후 1주 병행 운영으로 기존 opendart-* 결과와 대조 후 교체 결정. `resolve_corp_code`의 강화-F1 대체 검토 포함.
4. **③④ 스크립트** — 실행 머신에서 Python 실행 가능 여부만 확인하면 활성화(스킬에 동봉·게이트됨).

## 로컬 검증 로그 (2026-08-11, 맥에서 수행)

| 항목 | 결과 |
|---|---|
| OpenInsider-MCP 기동 | ✅ v0.3.0, stdio 핸드셰이크 성공, 도구 16종 |
| OpenInsider 실데이터 | ✅ `search_by_ticker(NVDA)` — Form 4 거래 수신, 구조화 필드 + SEC 원문 URL |
| pykrx-mcp 기동 | ⚠️ 기본 실행 즉사(mcp SDK 2.x 비호환) → `--with "mcp<2"` 핀으로 v1.29.0 기동, 도구 8종(README 23종 아님) |
| pykrx 시세 | ✅ OHLCV 로그인 없이 정상(삼성전자 2026-08-10 실데이터) |
| pykrx 투자자별 수급 | ⚠️ `KRX_ID`/`KRX_PW` 미설정 시 실패 — KRX 무료 계정 필요 |
| compute_ta.py | ✅ 합성 60일 데이터로 지표·해석·등급조정 4번 조건 판정 정상, 30행 미만 가드 정상 |
| 강화-B 실전 시뮬레이션 | ✅ `officer_buys` 시장 스캔 → NSLR CEO $249,984 매수(08-10 신고) 확인 → +2점 판정, SEC 원문 URL 확보 |
| 강화-TA 실데이터 E2E | ✅ pykrx 한화시스템 1년치(243거래일) → compute_ta.py — 52주고점 -58% 정확 산출, 4번 조건 AND 로직 정상(20일선 상회로 미발동) |
| korean-dart-mcp 기동 | ✅ v0.9.2, 도구 18종. env는 `DART_API_KEY`. 데이터 호출은 실키 필요(실행 머신에서 검증) |
