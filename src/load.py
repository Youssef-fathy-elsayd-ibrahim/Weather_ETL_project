from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.dialects.postgresql import insert

from .config import settings


SCHEMA_FILE = (
    Path(__file__).resolve().parents[1]
    / "sql"
    / "schema.sql"
)


def load(df: pd.DataFrame) -> int:
    engine = create_engine(settings.database_url)

    with engine.begin() as connection:

        # Create the table and index
        schema_sql = SCHEMA_FILE.read_text()
        connection.execute(text(schema_sql))

        # Remove duplicate records inside the DataFrame
        df = df.drop_duplicates(
            subset=["location_name", "observed_at"],
            keep="last"
        )

        # Insert new records or update existing records
        def upsert_weather(table, connection, keys, data_iter):

            rows = [
                dict(zip(keys, row))
                for row in data_iter
            ]

            if not rows:
                return 0

            statement = insert(table.table).values(rows)

            excluded = statement.excluded

            statement = statement.on_conflict_do_update(
                index_elements=[
                    "location_name",
                    "observed_at"
                ],
                set_={
                    "latitude": excluded.latitude,
                    "longitude": excluded.longitude,
                    "timezone": excluded.timezone,
                    "temperature_c": excluded.temperature_c,
                    "humidity_pct": excluded.humidity_pct,
                    "precipitation_mm": excluded.precipitation_mm,
                    "wind_speed_kmh": excluded.wind_speed_kmh,
                    "weather_code": excluded.weather_code,
                }
            )

            result = connection.execute(statement)

            return result.rowcount

        df.to_sql(
            "weather_hourly",
            connection,
            if_exists="append",
            index=False,
            method=upsert_weather,
        )

    return len(df)

