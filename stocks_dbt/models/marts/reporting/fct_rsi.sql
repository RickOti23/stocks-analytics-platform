WITH gains_losses AS (
    SELECT
        trade_date,
        ticker,
        close,
        daily_return,
        GREATEST(daily_return, 0)  AS gain,
        GREATEST(-daily_return, 0) AS loss
    FROM {{ ref('int_daily_returns') }}
),

smoothed AS (
    SELECT
        trade_date,
        ticker,
        close,
        AVG(gain) OVER (
            PARTITION BY ticker ORDER BY trade_date
            ROWS BETWEEN 13 PRECEDING AND CURRENT ROW
        ) AS avg_gain_14,
        AVG(loss) OVER (
            PARTITION BY ticker ORDER BY trade_date
            ROWS BETWEEN 13 PRECEDING AND CURRENT ROW
        ) AS avg_loss_14
    FROM gains_losses
)

SELECT
    trade_date,
    ticker,
    close,
    avg_gain_14,
    avg_loss_14,

    ROUND(
        100 - (100 / (1 + (avg_gain_14 / NULLIF(avg_loss_14, 0))))
    , 2)                                                            AS rsi_14,

    CASE
        WHEN avg_loss_14 = 0                                        THEN 'overbought'
        WHEN (avg_gain_14 / NULLIF(avg_loss_14, 0)) > 2.33         THEN 'overbought'
        WHEN (avg_gain_14 / NULLIF(avg_loss_14, 0)) < 0.43         THEN 'oversold'
        ELSE 'neutral'
    END                                                             AS rsi_signal

FROM smoothed