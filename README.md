# Weather ETL Project

An end-to-end weather data pipeline that collects hourly forecast data from the Open-Meteo API, transforms and validates it with Python, stores it in PostgreSQL, and displays it through Streamlit and Power BI.

## Architecture

```text
Open-Meteo API -> Python ETL -> PostgreSQL -> Streamlit
                                      \-> Power BI
```

## Features

- Extracts hourly forecast data from Open-Meteo.
- Transforms and validates weather values with Pandas.
- Upserts data into PostgreSQL and prevents duplicate location/timestamp records.
- Provides a Streamlit dashboard with filters, KPIs, charts, and daily summaries.
- Includes a Power BI report connected to the same PostgreSQL table.

## Project structure

```text
Weather_ETL_project/
├── dashboard/
│   ├── app.py
│   └── Weather_ETL_PowerBI_Dashboard.pbix
├── sql/
│   ├── schema.sql
│   └── queries.sql
├── src/
│   ├── config.py
│   ├── extract.py
│   ├── transform.py
│   ├── load.py
│   └── main.py
├── tests/
│   └── test_transform.py
├── .env.example
├── docker-compose.yml
├── requirements.txt
└── run.py
```

## Requirements

- Python 3.11 or newer
- Docker Desktop
- Power BI Desktop (optional)

## Setup

Clone the repository and create a virtual environment:

```powershell
git clone https://github.com/Youssef-fathy-elsayd-ibrahim/Weather_ETL_project.git
cd Weather_ETL_project
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Create a `.env` file from `.env.example`:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=weather_dw
DB_USER=weather
DB_PASSWORD=weather
LATITUDE=30.0444
LONGITUDE=31.2357
LOCATION_NAME=Cairo
TIME_ZONE=Africa/Cairo
FORECAST_DAYS=7
```

Do not commit `.env` to GitHub.

## Run the ETL pipeline

Start PostgreSQL:

```powershell
docker compose up -d
```

Run the pipeline:

```powershell
python run.py
```

The pipeline creates and updates this table:

```text
public.weather_hourly
```

Check the loaded data:

```powershell
docker compose exec postgres psql -U weather -d weather_dw -c "SELECT * FROM public.weather_hourly LIMIT 5;"
```

## Run the Streamlit dashboard

```powershell
streamlit run dashboard/app.py
```

The dashboard reads from `public.weather_hourly` and provides date filtering, latest-weather KPIs, temperature/humidity/wind charts, precipitation details, and daily summaries.

## Open the Power BI dashboard

Open:

```text
dashboard/Weather_ETL_PowerBI_Dashboard.pbix
```

The PostgreSQL connection uses:

```text
Server: localhost:5432
Database: weather_dw
Schema: public
Table: weather_hourly
```

If the report needs updated data, run the ETL pipeline and select **Refresh** in Power BI Desktop.

## Database columns

`public.weather_hourly` contains:

- `location_name`, `latitude`, `longitude`, `timezone`
- `observed_at`
- `temperature_c`, `humidity_pct`, `precipitation_mm`
- `wind_speed_kmh`, `weather_code`
- `loaded_at`

SQL analytics examples are in [sql/queries.sql](sql/queries.sql).

## Run tests

```powershell
pytest
```

The tests cover Open-Meteo payload transformation, column renaming, duplicate removal, and missing-value validation.

## Stop PostgreSQL

```powershell
docker compose down
```
