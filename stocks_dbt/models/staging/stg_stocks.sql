Select 
    CAST(Date as Date) as trade_date,
    CAST(Close as FLOAT) as close,
    CAST(High as FLOAT) as high,
    CAST(Low as FLOAT) as low,
    CAST(Volume as FLOAT) as volume,

    -- ticker
    CAST(Ticker as CHAR) AS ticker

FROM {{ source('raw_data','stocks')}}
WHERE close is NOT NULL