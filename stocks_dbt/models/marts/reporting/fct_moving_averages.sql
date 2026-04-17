SELECT
    trade_date,
    ticker,
    close,
    ROUND(AVG(close) OVER w7,   2) AS ma_7,
    ROUND(AVG(close) OVER w21,  2) AS ma_21,
    ROUND(AVG(close) OVER w30,  2) AS ma_30,
    ROUND(AVG(close) OVER w50,  2) AS ma_50,
    ROUND(AVG(close) OVER w200, 2) AS ma_200

FROM {{ ref('int_daily_returns') }}

WINDOW
    w7   AS (PARTITION BY ticker ORDER BY trade_date ROWS BETWEEN 6   PRECEDING AND CURRENT ROW),
    w21  AS (PARTITION BY ticker ORDER BY trade_date ROWS BETWEEN 20  PRECEDING AND CURRENT ROW),
    w30  AS (PARTITION BY ticker ORDER BY trade_date ROWS BETWEEN 29  PRECEDING AND CURRENT ROW),
    w50  AS (PARTITION BY ticker ORDER BY trade_date ROWS BETWEEN 49  PRECEDING AND CURRENT ROW),
    w200 AS (PARTITION BY ticker ORDER BY trade_date ROWS BETWEEN 199 PRECEDING AND CURRENT ROW)