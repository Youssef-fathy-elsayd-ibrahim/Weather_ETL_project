import requests
from .config import settings




OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"

def extract()-> dict:
    params = {
        "latitude":settings.latitude,
        "longitude":settings.longitude,
        "timezone":settings.time_zone,
        "forecast_days":settings.forecast_days,
        "hourly":(
            "temperature_2m,"
            "relative_humidity_2m,"
            "precipitation,"
            "wind_speed_10m,"
            "weather_code,"
        ),   
    }


    response = requests.get(
        OPEN_METEO_URL,
        params = params,
        timeout=30,
    )

    response.raise_for_status()
    return response.json()