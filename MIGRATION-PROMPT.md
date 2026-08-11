# 업그레이드(교체) 프롬프트 — 기존 v1 사용자용

**이미 구버전 스킬이 돌아가고 있는 컴퓨터**에서, 스킬만 이 저장소의 v2로 교체할 때 사용합니다.
(처음 설치라면 이 파일이 아니라 [`SETUP-PROMPT.md`](SETUP-PROMPT.md)를 쓰세요.)

**사용법**: 기존 스킬이 돌아가는 컴퓨터에서 Claude를 실행하고, 아래 프롬프트를 통째로 복사해 붙여넣으면 끝입니다. 개인화 값 복원, 백업, 교체, 검증까지 Claude가 알아서 진행합니다.

---

## 복사해서 붙여넣을 프롬프트

```
너는 지금부터 morning-sector-briefing 스킬의 v1 → v2 업그레이드 담당자야. 이 컴퓨터에는 구버전 스킬이 이미 설치돼 운영 중이고, 나는 스킬 본체만 https://github.com/Donghee401/morning-sector-briefing 의 v2로 교체하고 싶어. 아래 원칙과 단계로 진행해줘.

[원칙]
- 한 번에 한 단계씩, 각 단계 결과를 보고하고 내 확인 후 다음으로.
- 이 프롬프트는 재시작 후 다시 붙여넣어도 이어지도록, 각 단계 시작 전 이미 완료됐는지 확인하고 완료된 단계는 건너뛰어.
- 파일 수정·교체는 네가 직접 해. 단, 덮어쓰기 전에 반드시 백업부터.
- v2는 공개 배포용이라 개인정보가 플레이스홀더로 비워져 있어 — 실제 값은 나에게 묻지 말고 이 컴퓨터의 기존 v1 파일에서 추출해서 채워. 추출이 안 되는 값만 나에게 물어봐.
- 절대 건드리면 안 되는 것: Templates 폴더의 데이터 파일들(value-chain-map.md, briefing-daily-log.md, DECISIONS.md 등), 자매 스킬(weekly-action-review, value-chain-map-updater, manual-sector-briefing). 이번 교체 대상은 morning-sector-briefing 스킬 본체뿐이야.

[배경 지식]
- v2는 v1과 판정 규칙이 동일하고(토큰 29% 절감 리팩터링), 다운스트림 접점(briefing-daily-log.md 9필드 형식, value-chain-map.md 파싱)은 그대로라 자매 스킬·워크플로우는 수정 없이 계속 작동해.
- v2 신기능은 전부 "커넥터 연결 시에만 활성화" 게이트 방식이라, 커넥터를 안 붙여도 v1과 동일하게 동작해.
- v2는 본체(SKILL.md) 외에 references/ 폴더 3개 파일과 scripts/compute_ta.py가 세트야 — 반드시 함께 복사해야 해.

[단계]

0단계. 현황 파악
- 이 컴퓨터에서 기존 morning-sector-briefing 스킬 파일(SKILL.md)의 위치를 찾아.
- 그 파일을 읽고 다음 실제 값 3종을 추출해 기록해:
  ① Templates 폴더 경로 (예: C:\Users\아무개\Claude\Templates)
  ② Gmail 수신 이메일 주소 (STEP6의 to=[...])
  ③ Gmail·카카오톡 커넥터 도구명 (STEP6·7의 mcp__...__create_draft / mcp__...__KakaotalkChat-MemoChat)
- Templates 폴더가 실제로 존재하고 value-chain-map.md·briefing-daily-log.md가 있는지 확인해.
- 자매 스킬(weekly-action-review 등)의 위치도 확인만 해둬 (수정 금지).

1단계. v2 받기
- git이 있으면 적당한 위치에 git clone https://github.com/Donghee401/morning-sector-briefing.git (이미 있으면 git pull). git이 없으면 네가 설치하거나 ZIP 다운로드로 대체해.

2단계. 개인화 주입
- 받아온 v2의 morning-sector-briefing/SKILL.md에서 플레이스홀더를 0단계에서 추출한 실제 값으로 교체해:
  · C:\Users\[사용자명]\Claude\Templates → ①의 실제 경로 (전체 파일에서 전부)
  · 본인이메일@gmail.com → ②의 실제 이메일
  · mcp__[Gmail커넥터ID]__create_draft / mcp__[카카오커넥터ID]__KakaotalkChat-MemoChat → ③의 실제 도구명
- 교체 후 grep으로 플레이스홀더([사용자명], 본인이메일, 커넥터ID)가 하나도 안 남았는지 검산해.

3단계. 교체 방식 선택 (나에게 물어봐서 결정)
나에게 두 방식을 설명하고 선택받아:

【A. 병행 운행 — 권장, 기본값】 기존 v1은 손대지 않고 그대로 매일 08:30 자동 실행을 계속 담당. 개인화된 v2 세트는 별도 폴더(예: 스킬 위치 옆 morning-sector-briefing-v2)에 두고, 나는 며칠간 원할 때 "v2로 브리핑 만들어줘"로 수동 실행해서 v1 결과와 비교. 만족스러우면 그때 나에게 "교체하자"고 말하고 B 방식을 실행. (이 방식이면 이 시점에서 잃는 것이 0이야.)

【B. 즉시 교체】
- 먼저 기존 스킬 폴더 전체를 날짜 붙인 백업 폴더(예: morning-sector-briefing-v1-backup-[오늘날짜])로 통째 복사해. 백업 완료를 확인하기 전에는 절대 덮어쓰지 마.
- 개인화된 v2 세트(SKILL.md + references/ + scripts/)를 기존 스킬 위치에 복사해.
- references/의 상대경로 참조가 이 환경에서 해석되는지 확인하고, 안 되면 SKILL.md의 references/ 경로 3곳을 절대경로로 바꿔줘.
- 롤백 방법(백업 폴더를 원래 이름으로 되돌리기)을 한 줄로 알려줘.

A를 선택했으면 4단계 이후를 v2 폴더 기준으로 진행하고, 6단계 테스트를 통과한 뒤 "정식 교체는 준비되면 말해달라"고 안내하고 마무리해.

4단계. 신규 커넥터 등록 (v2 업그레이드 활성화 — 선택이지만 권장)
- OpenInsider (미국 임원 매수 신호 부활, 키 불요): claude mcp add --scope user openinsider -- npx -y openinsider-mcp
  (Claude 데스크톱 예약작업 환경이면 그 환경의 커넥터 설정 방식으로 등록해줘. uvx/npx가 없으면 네가 설치부터.)
- pykrx (기술지표 52주고점 정확화, 키 불요): claude mcp add --scope user pykrx -- uvx --with "mcp<2" pykrx-mcp
- 이 컴퓨터의 기존 OpenDART 키를 찾을 수 있으면 korean-dart-mcp(env DART_API_KEY)도 제안해줘.
- KRX 계정(수급 공식화)은 UPGRADE-PLAN.md를 보여주고 나중에 할지 물어봐.
- 등록한 커넥터는 각 1회 실호출로 검증해.

5단계. 무결성 점검
- 새 SKILL.md가 참조하는 Templates 파일 6종이 전부 접근 가능한지 확인.
- briefing-daily-log.md의 최근 항목 형식과 새 SKILL.md STEP8 형식이 일치하는지 대조 (자매 스킬 호환 확인).
- scripts/compute_ta.py가 이 컴퓨터에서 실행되는지 테스트 (안 되면 폴백인 직접 계산 모드로 동작한다고 보고만).

6단계. 수동 테스트 1회
- 스킬을 수동 실행("모닝 브리핑 만들어줘")해서 결과를 보여줘. 수동 실행이므로 STEP8 로그는 기록되지 않는 게 정상이야.
- Gmail 임시보관함·카카오톡에 실제로 도착했는지 나에게 확인받아.
- 문제가 있으면 고치고, 원인이 v2 교체라면 즉시 백업으로 롤백하는 방법(백업 파일을 원래 이름으로 되돌리기)을 보여줘.

7단계. 마무리
- 내일 08:30 자동 실행이 새 버전으로 도는지 확인하는 방법을 알려줘 (브리핑 하단 실행 로그의 MCP 호출수/상한 숫자로 v2 여부 식별 가능).
- 변경 요약을 3줄로 보고하고 종료해.

지금 0단계부터 시작해줘.
```

---

## 참고

- **잃는 것이 걱정된다면**: 3단계에서 "병행 운행(A)"을 선택하세요 — v1 자동 실행은 그대로 두고 v2를 옆에서 수동으로만 검증하다가, 확신이 생기면 교체합니다. 이 방식은 어느 시점에도 기존 것을 삭제하지 않습니다.
- **롤백**: 즉시 교체(B)를 택했더라도 백업 폴더를 원래 이름으로 되돌리면 즉시 v1으로 복귀합니다.
- **데이터는 어느 방식이든 안전**: 일일 로그·섹터 지도·캐시·DECISIONS.md는 스킬과 별도 폴더에 있어 교체 대상이 아예 아닙니다.
- **데이터는 안전**: 이 교체는 스킬 본체만 바꾸며, 일일 로그·섹터 지도·캐시 등 축적된 데이터와 자매 스킬은 건드리지 않습니다.
- **커넥터를 하나도 안 붙이면?** v1과 완전히 동일하게 동작합니다 (신기능은 전부 커넥터 연결 시에만 켜지는 게이트 방식).
