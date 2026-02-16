{% macro get_trip_duration_minutes(pickup_datetime, dropoff_datetime) -%}
    datediff('minute', {{ pickup_datetime }}, {{ dropoff_datetime }})
{%- endmacro %}