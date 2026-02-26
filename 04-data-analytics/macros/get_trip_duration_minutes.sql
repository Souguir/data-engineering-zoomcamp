{% macro get_trip_duration_minutes(pickup_datetime, dropoff_datetime) -%}
    TIMESTAMP_DIFF({{ dropoff_datetime }}, {{ pickup_datetime }}, MINUTE)
{%- endmacro %}