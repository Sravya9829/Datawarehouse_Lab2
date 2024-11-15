-- models/input/stg_nps.sql

{{ config(materialized='view', schema='staging') }}

SELECT *
FROM {{ source('raw_data', 'NPS') }} AS raw_data_nps
