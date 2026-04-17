WITH daily AS (
    SELECT trade_date, ticker, daily_return
    FROM {{ ref('int_daily_returns') }}
),

pivoted AS (
    SELECT
        trade_date,
        MAX(CASE WHEN ticker = 'AAPL'  THEN daily_return END) AS aapl,
        MAX(CASE WHEN ticker = 'MSFT'  THEN daily_return END) AS msft,
        MAX(CASE WHEN ticker = 'GOOGL' THEN daily_return END) AS googl,
        MAX(CASE WHEN ticker = 'NVDA'  THEN daily_return END) AS nvda,
        MAX(CASE WHEN ticker = 'AMZN'  THEN daily_return END) AS amzn
    FROM daily
    GROUP BY trade_date
)

SELECT
    trade_date,
    ROUND(CORR(aapl,  msft)  OVER w30, 4) AS corr_aapl_msft,
    ROUND(CORR(aapl,  googl) OVER w30, 4) AS corr_aapl_googl,
    ROUND(CORR(aapl,  nvda)  OVER w30, 4) AS corr_aapl_nvda,
    ROUND(CORR(aapl,  amzn)  OVER w30, 4) AS corr_aapl_amzn,
    ROUND(CORR(msft,  googl) OVER w30, 4) AS corr_msft_googl,
    ROUND(CORR(msft,  nvda)  OVER w30, 4) AS corr_msft_nvda,
    ROUND(CORR(msft,  amzn)  OVER w30, 4) AS corr_msft_amzn,
    ROUND(CORR(googl, nvda)  OVER w30, 4) AS corr_googl_nvda,
    ROUND(CORR(googl, amzn)  OVER w30, 4) AS corr_googl_amzn,
    ROUND(CORR(nvda,  amzn)  OVER w30, 4) AS corr_nvda_amzn

FROM pivoted

WINDOW
    w30 AS (
        ORDER BY trade_date 
        ROWS BETWEEN 29 PRECEDING AND CURRENT ROW
    )