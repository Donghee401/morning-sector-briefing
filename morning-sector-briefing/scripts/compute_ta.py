#!/usr/bin/env python3
"""강화-TA 기술지표 결정론적 계산기 (표준 라이브러리만 사용, 외부 의존성 없음).

사용법:
    python compute_ta.py <input.json>

입력 JSON 형식 (koreaStock-stock_get_price_history 응답의 rows를 아래 스키마로 변환해 저장):
    {
      "rows": [{"date": "YYYY-MM-DD", "open": 0, "high": 0, "low": 0, "close": 0, "volume": 0}, ...],
      "w52_high": 12345   # 선택 — 52주 최고가를 아는 경우(예: stock_get_quote 응답). 없으면 rows 내 최고가로 근사
    }
    rows는 날짜 오름차순. 30행 미만이면 스킬 규칙대로 계산 생략(error 반환).

출력: 값 + 한국어 해석 문구가 붙은 JSON. 해석 기준은 SKILL.md 규칙과 동일:
    RSI 70+=과매수/30-=과매도, 등급조정 4번 조건 = 52주고점 -50%+ 하락 AND 20일선 하회.
"""
import json
import sys


def sma(values, n):
    if len(values) < n:
        return None
    return sum(values[-n:]) / n


def sma_series(values, n):
    return [sum(values[i - n + 1:i + 1]) / n if i >= n - 1 else None for i in range(len(values))]


def ema_series(values, n):
    out = [None] * len(values)
    if len(values) < n:
        return out
    seed = sum(values[:n]) / n
    out[n - 1] = seed
    k = 2 / (n + 1)
    for i in range(n, len(values)):
        out[i] = values[i] * k + out[i - 1] * (1 - k)
    return out


def rsi_wilder(closes, n=14):
    if len(closes) < n + 1:
        return None
    gains, losses = [], []
    for i in range(1, len(closes)):
        d = closes[i] - closes[i - 1]
        gains.append(max(d, 0.0))
        losses.append(max(-d, 0.0))
    avg_g = sum(gains[:n]) / n
    avg_l = sum(losses[:n]) / n
    for i in range(n, len(gains)):
        avg_g = (avg_g * (n - 1) + gains[i]) / n
        avg_l = (avg_l * (n - 1) + losses[i]) / n
    if avg_l == 0:
        return 100.0
    rs = avg_g / avg_l
    return 100 - 100 / (1 + rs)


def stdev(values):
    m = sum(values) / len(values)
    return (sum((v - m) ** 2 for v in values) / len(values)) ** 0.5


def find_cross(fast, slow):
    """마지막 교차를 찾아 ('golden'|'dead', 며칠 전) 반환. 없으면 (None, None)."""
    last = (None, None)
    for i in range(1, len(fast)):
        if None in (fast[i], slow[i], fast[i - 1], slow[i - 1]):
            continue
        prev, cur = fast[i - 1] - slow[i - 1], fast[i] - slow[i]
        if prev <= 0 < cur:
            last = ("golden", len(fast) - 1 - i)
        elif prev >= 0 > cur:
            last = ("dead", len(fast) - 1 - i)
    return last


def main():
    data = json.load(open(sys.argv[1], encoding="utf-8"))
    rows = data["rows"]
    if len(rows) < 30:
        print(json.dumps({"error": "insufficient_rows", "rows": len(rows),
                          "해석": "30거래일 미만 — 스킬 규칙에 따라 계산·서술 생략"}, ensure_ascii=False))
        return
    closes = [float(r["close"]) for r in rows]
    highs = [float(r["high"]) for r in rows]
    price = closes[-1]
    out = {"rows": len(rows), "close": price}

    # SMA20/60 + 교차
    s20, s60 = sma(closes, 20), sma(closes, 60)
    out["sma20"] = round(s20, 2) if s20 else None
    out["sma60"] = round(s60, 2) if s60 else None
    above20 = s20 is not None and price >= s20
    out["sma20_대비"] = f"{'상회' if above20 else '하회'}({(price / s20 - 1) * 100:+.1f}%)" if s20 else "산출불가"
    if s60 is not None:
        kind, ago = find_cross(sma_series(closes, 20), sma_series(closes, 60))
        out["sma_cross"] = f"{'골든' if kind == 'golden' else '데드'}크로스 D-{ago}" if kind else "최근 교차 없음"
    else:
        out["sma_cross"] = "표본부족(60일 미만)으로 산출불가"

    # RSI14
    rsi = rsi_wilder(closes)
    if rsi is not None:
        zone = "과매수(70+)" if rsi >= 70 else "과매도(30-)" if rsi <= 30 else "중립"
        out["rsi14"] = {"value": round(rsi, 1), "해석": zone}

    # 볼린저밴드(20, ±2σ)
    if len(closes) >= 20:
        mid = sma(closes, 20)
        sd = stdev(closes[-20:])
        upper, lower = mid + 2 * sd, mid - 2 * sd
        pos = "상단 돌파" if price > upper else "하단 이탈" if price < lower else "밴드 내"
        out["bollinger"] = {"upper": round(upper, 2), "lower": round(lower, 2), "해석": pos}

    # MACD(12, 26, 9)
    macd_line = [None if (a is None or b is None) else a - b
                 for a, b in zip(ema_series(closes, 12), ema_series(closes, 26))]
    valid = [v for v in macd_line if v is not None]
    if len(valid) >= 9:
        sig = ema_series(valid, 9)
        pad = [None] * (len(macd_line) - len(valid))
        kind, ago = find_cross(pad + valid, pad + sig)
        out["macd"] = {"value": round(valid[-1], 2),
                       "해석": f"{'골든' if kind == 'golden' else '데드'}크로스 D-{ago}" if kind else "최근 교차 없음"}

    # 52주고점 대비 하락률 (w52_high 미제공 시 표본 내 최고가 근사 — 근사임을 명시)
    w52 = data.get("w52_high")
    ref, approx = (float(w52), False) if w52 else (max(highs), True)
    drawdown = (price / ref - 1) * 100
    out["고점대비"] = {"기준고가": ref, "하락률": round(drawdown, 1),
                    "근사여부": "표본내 최고가 근사(52주 아님)" if approx else "52주고점 기준"}

    # 등급조정 4번 조건: 52주고점 -50%+ 하락 AND 20일선 하회
    trig = drawdown <= -50 and not above20
    out["등급조정_4번조건"] = {
        "발동": trig,
        "해석": ("⚠️ 발동 — 진입 조건: 주가 반등(20일선 회복) 확인 후" if trig else "미발동")
                + (" ※ 고점이 표본내 근사값이므로 실제 52주고점 확인 필요" if approx and drawdown <= -40 else "")}

    print(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
