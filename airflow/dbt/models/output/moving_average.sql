-- models/output/moving_average.sql

{{ config(materialized='table', schema='analysis') }}

WITH ranked_prices AS (
    SELECT
        DATE,
        CLOSE,
        SYMBOL,
        ROW_NUMBER() OVER (PARTITION BY SYMBOL ORDER BY DATE) as rank
    FROM {{ ref('stg_nps') }}
)

SELECT
    DATE,
    SYMBOL,
    AVG(CLOSE) OVER (PARTITION BY SYMBOL ORDER BY DATE ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS moving_avg_7d
FROM ranked_prices
ORDER BY DATE, SYMBOL
