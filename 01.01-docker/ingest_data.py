#!/usr/bin/env python
# coding: utf-8


import os
import urllib.request
from pathlib import Path
import pandas as pd
import click
from sqlalchemy import create_engine






taxi_zone_dtype = {
    "LocationID":"int64",
    "Borough":"str",
    "Zone":"str",
    "service_zone":"str" 
}

@click.command()
@click.option('--pg-user', default='postgres', help='PostgreSQL user')
@click.option('--pg-password', default='postgres', help='PostgreSQL password')
@click.option('--pg-host', default='postgres', help='PostgreSQL host')
@click.option('--pg-port', default='5432',type = int ,help='PostgreSQL port')
@click.option('--pg-db', default='ny_taxi', help='PostgreSQL database name')
@click.option('--year', default='2025', type = int, help='Year of the data')
@click.option('--month', default='11', type = int, help='Month of the data')


def ingest_data(pg_user, pg_password, pg_host, pg_port, pg_db, year, month):

    data_dir = Path(os.environ.get("DATA_DIR", "."))
    data_dir.mkdir(parents=True, exist_ok=True)

    green_url = os.environ.get("GREEN_TRIP_URL")
    taxi_url = os.environ.get("TAXI_ZONE_URL")

    green_path = data_dir / f"green_tripdata_{year}-{month:02d}.parquet"
    taxi_path = data_dir / "taxi_zone_lookup.csv"

    if green_url and not green_path.exists():
        urllib.request.urlretrieve(green_url, green_path)

    if taxi_url and not taxi_path.exists():
        urllib.request.urlretrieve(taxi_url, taxi_path)

    df_green_trip = pd.read_parquet(green_path, engine="pyarrow")
    df_taxi_zone = pd.read_csv(taxi_path, dtype=taxi_zone_dtype)

    
    engine = create_engine(f'postgresql://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_db}')


    df_green_trip.head(0).to_sql(
                    name="green_trip_table",
                    con=engine,
                    if_exists='replace'
                )


    df_green_trip.to_sql(
            name="green_trip_table",
            con=engine,
            if_exists='append'
        )


    df_taxi_zone.head(0).to_sql(
                    name="taxi_zone_table",
                    con=engine,
                    if_exists='replace'
                )


    df_taxi_zone.to_sql(
                    name="taxi_zone_table",
                    con=engine,
                    if_exists='append'
                )
    
if __name__ == '__main__':
    ingest_data()






