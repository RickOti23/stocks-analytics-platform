SELECT
    trade_date,
    ticker,
    close,
    ROUND(AVG(close)    OVER w20, 2)                               AS bb_middle,
    ROUND(AVG(close)    OVER w20 + 2 * STDDEV(close) OVER w20, 2) AS bb_upper,
    ROUND(AVG(close)    OVER w20 - 2 * STDDEV(close) OVER w20, 2) AS bb_lower,
    ROUND(STDDEV(close) OVER w20, 4)                               AS bb_stddev,

    ROUND(
        (close - (AVG(close) OVER w20 - 2 * STDDEV(close) OVER w20))
        / NULLIF(4 * STDDEV(close) OVER w20, 0)
    , 4)                                                            AS bb_pct_b,

    CASE
        WHEN close > AVG(close) OVER w20 + 2 * STDDEV(close) OVER w20 THEN 'above_upper'
        WHEN close < AVG(close) OVER w20 - 2 * STDDEV(close) OVER w20 THEN 'below_lower'
        ELSE 'within_bands'
    END                                                             AS bb_signal

FROM {{ ref('int_daily_returns') }}

WINDOW
    w20 AS (PARTITION BY ticker ORDER BY trade_date ROWS BETWEEN 19 PRECEDING AND CURRENT ROW)