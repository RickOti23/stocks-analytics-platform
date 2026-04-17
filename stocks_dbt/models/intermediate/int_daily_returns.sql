WITH base AS (
    SELECT
        trade_date,
        ticker,
        close,
        high,
        low,
        volume,
        LAG(close) OVER (
            PARTITION BY ticker ORDER BY trade_date
        ) AS prev_close
    FROM {{ ref('stg_stocks') }}
)

SELECT
    trade_date,
    ticker,
    close,
    high,
    low,
    prev_close,
    volume,

    (close - prev_close)
    / NULLIF(prev_close, 0)                    AS daily_return,

    ROUND(
        (close - prev_close)
        / NULLIF(prev_close, 0) * 100
    , 4)                                       AS daily_return_pct

FROM base