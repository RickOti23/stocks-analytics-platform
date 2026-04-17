SELECT
    trade_date,
    ticker,
    close,
    daily_return_pct,

    ROUND(STDDEV(daily_return) OVER w7  * SQRT(252) * 100, 4) AS vol_7d_ann,
    ROUND(STDDEV(daily_return) OVER w30 * SQRT(252) * 100, 4) AS vol_30d_ann,
    ROUND(STDDEV(daily_return) OVER w90 * SQRT(252) * 100, 4) AS vol_90d_ann,

    ROUND(AVG(volume) OVER w30, 0)                             AS avg_vol_30d,

    ROUND(
        STDDEV(daily_return) OVER w7
        / NULLIF(STDDEV(daily_return) OVER w30, 0)
    , 4)                                                        AS vol_ratio

FROM {{ ref('int_daily_returns') }}

WINDOW
    w7  AS (PARTITION BY ticker ORDER BY trade_date ROWS BETWEEN 6  PRECEDING AND CURRENT ROW),
    w30 AS (PARTITION BY ticker ORDER BY trade_date ROWS BETWEEN 29 PRECEDING AND CURRENT ROW),
    w90 AS (PARTITION BY ticker ORDER BY trade_date ROWS BETWEEN 89 PRECEDING AND CURRENT ROW)