{{ config(materialized='view') }}

SELECT *
FROM {{ ref('int_daily_returns') }}