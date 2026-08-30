import pandas as pd
from .config import settings


def transform(payload:dict)->pd.DataFrame:
    hourly= payload["hourly"]
    df= pd.DataFrame(hourly)

    df= df.rename(
        columns={
            "time":"observed_at",
            "temperature_2m":"temperature_c",
            "relative_humidity_2m":"humidity_pct",
            "precipitation":"precipitation_mm",
            "wind_speed_10m":"wind_speed_kmh",
        }
    )

    df["observed_at"]= pd.to_datetime(df["observed_at"])

    df["location_name"]= settings.location_name
    df["latitude"]= settings.latitude
    df["longitude"]= settings.longitude
    df["timezone"]= payload.get("timezone", settings.time_zone)

    columns = [
        "location_name",
        "latitude",
        "longitude",
        "timezone",
        "observed_at",
        "temperature_c",
        "humidity_pct",
        "precipitation_mm",
        "wind_speed_kmh",
        "weather_code",
    ]

    df = df[columns]
    df = df.drop_duplicates(
        subset=["location_name", "observed_at"]
    )

    if df.empty:
        raise ValueError ("No weather rows were returned.")

    required_numeric_columns = [
        "temperature_c",
        "humidity_pct",
        "precipitation_mm",
        "wind_speed_kmh",
        "weather_code",
    ]

    if df[required_numeric_columns].isna().any().any():
        raise ValueError("Required weather values contain NULLs.")

    return df