-- snapshots/stg_nps_snapshot.sql

{% snapshot stg_nps_snapshot %}

{{
    config(
        target_schema='snapshot',
        unique_key='md5(concat(cast(date as varchar), cast(symbol as varchar)))', 
        strategy='check',
        check_cols='all'
    )
}}

SELECT *
FROM {{ ref('stg_nps') }}

{% endsnapshot %}