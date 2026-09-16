import pytest

from src.transform import transform


@pytest.fixture
def weather_payload():
    return {
        "timezone": "Africa/Cairo",
        "hourly": {
            "time": ["2026-09-16T00:00", "2026-09-16T01:00"],
            "temperature_2m": [25.0, 26.0],
            "relative_humidity_2m": [50, 51],
            "precipitation": [0.0, 0.1],
            "wind_speed_10m": [5.0, 6.0],
            "weather_code": [0, 3],
        },
    }


def test_transform_converts_open_meteo_payload(weather_payload):
    result = transform(weather_payload)

    assert len(result) == 2
    assert result["observed_at"].dt.year.tolist() == [2026, 2026]
    assert result["timezone"].tolist() == ["Africa/Cairo", "Africa/Cairo"]
    assert result["temperature_c"].tolist() == [25.0, 26.0]


def test_transform_renames_weather_columns(weather_payload):
    result = transform(weather_payload)

    expected_columns = [
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

    assert result.columns.tolist() == expected_columns


def test_transform_removes_duplicate_observations(weather_payload):
    weather_payload["hourly"]["time"].append("2026-09-16T00:00")
    weather_payload["hourly"]["temperature_2m"].append(99.0)
    weather_payload["hourly"]["relative_humidity_2m"].append(99)
    weather_payload["hourly"]["precipitation"].append(9.0)
    weather_payload["hourly"]["wind_speed_10m"].append(99.0)
    weather_payload["hourly"]["weather_code"].append(99)

    result = transform(weather_payload)

    assert len(result) == 2
    assert result.loc[0, "temperature_c"] == 25.0


def test_transform_rejects_missing_required_values(weather_payload):
    weather_payload["hourly"]["relative_humidity_2m"][1] = None

    with pytest.raises(ValueError, match="Required weather values contain NULLs"):
        transform(weather_payload)
