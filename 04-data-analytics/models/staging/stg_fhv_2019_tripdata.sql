with source as (
    select * from {{ source('raw', 'fhv_2019_tripdata') }}
),

renamed as (
    SELECT 
        dispatching_base_num,
        pickup_datetime as lpep_pickup_datetime,
        dropOff_datetime as lpep_dropoff_datetime,
        PUlocationID as pickup_location_id,
        DOlocationID as dropoff_location_id,
        SR_Flag,
        Affiliated_base_number 
    FROM source
),

filtered as (
    SELECT * FROM renamed
    WHERE dispatching_base_num IS NOT NULL
)

SELECT * FROM filtered