this README.md covers the project overview, architecture, ETL workflow, folder structure, setup, Docker/PostgreSQL, configuration, execution, SQL queries, common errors and fixes, troubleshooting, Git/GitHub guidance, and future improvements.

## Developed an end-to-end Weather ETL Pipeline that extracts forecast data from the Open-Meteo API, transforms and validates weather metrics using Pandas, and loads hourly weather records into PostgreSQL using SQLAlchemy. The project follows industry-standard ETL architecture, uses Docker for database deployment, environment variables for configuration management, and SQL analytics queries for reporting and trend analysis.


## Technologies
-Python
-Pandas
-Requests
-PostgreSQL
-SQLAlchemy
-Docker
-Git & GitHub

## Concepts Demonstrated
-ETL Pipelines
-API Integration
-Data Cleaning & Validation
-Relational Databases
-SQL Analytics
-Containerization
-Version Control

# Weather ETL Project

A Python-based **ETL (Extract, Transform, Load) pipeline** that retrieves hourly weather forecast data from the **Open-Meteo API**, transforms and validates the data using Pandas, and loads it into a PostgreSQL data warehouse running inside Docker.

The project is designed as a simple but complete data engineering workflow demonstrating:

* REST API data extraction
* Data transformation and validation
* Pandas DataFrames
* PostgreSQL database storage
* SQL schema design
* Docker and Docker Compose
* Environment-variable configuration
* SQL analytics queries
* Python project organization
* ETL pipeline architecture

---

## 1. Project Overview

The Weather ETL Project collects hourly weather forecast information for **Cairo, Egypt**.

The pipeline retrieves approximately **7 days of hourly forecast data**, transforms the API response into a structured Pandas DataFrame, validates the data, and stores it in a PostgreSQL database.

### Main technologies

| Technology     | Purpose                            |
| -------------- | ---------------------------------- |
| Python         | Main programming language          |
| Pandas         | Data transformation and validation |
| Requests       | Calling the weather API            |
| SQLAlchemy     | Connecting Python to PostgreSQL    |
| Psycopg2       | PostgreSQL database driver         |
| PostgreSQL     | Data warehouse/database            |
| Docker         | Running PostgreSQL in a container  |
| Docker Compose | Managing the PostgreSQL container  |
| python-dotenv  | Loading environment variables      |
| SQL            | Database schema and analytics      |

---

# 2. ETL Architecture

The project follows the standard:

**Extract → Transform → Load**

architecture.

```text
                    Open-Meteo API
                          │
                          │ JSON weather data
                          ▼
                   ┌─────────────┐
                   │   EXTRACT   │
                   │ extract.py  │
                   └──────┬──────┘
                          │
                          │ Raw API payload
                          ▼
                   ┌─────────────┐
                   │  TRANSFORM  │
                   │transform.py │
                   └──────┬──────┘
                          │
                          │ Clean DataFrame
                          ▼
                   ┌─────────────┐
                   │    LOAD     │
                   │   load.py   │
                   └──────┬──────┘
                          │
                          ▼
                ┌──────────────────┐
                │    PostgreSQL    │
                │   weather_dw     │
                │                  │
                │  weather_hourly  │
                └──────────────────┘
                          │
                          ▼
                    SQL Queries
                  sql/queries.sql
```

---

# 3. ETL Flow in Detail

## Step 1 — Extract

`src/extract.py` sends a request to the Open-Meteo API.

The API receives parameters such as:

* Latitude
* Longitude
* Time zone
* Forecast days
* Temperature
* Humidity
* Precipitation
* Wind speed
* Weather code

Example configuration:

```text
Latitude: 30.0444
Longitude: 31.2357
Location: Cairo
Time zone: Africa/Cairo
Forecast days: 7
```

The API returns weather information in JSON format.

---

## Step 2 — Transform

`src/transform.py` takes the JSON response and converts the hourly information into a Pandas DataFrame.

The transformation process includes:

1. Extracting the `hourly` section.
2. Creating a DataFrame.
3. Renaming API columns.
4. Converting timestamps.
5. Adding location information.
6. Selecting the required columns.
7. Removing duplicate location/timestamp records.
8. Checking for missing required values.
9. Returning the cleaned DataFrame.

For example:

```text
temperature_2m
        ↓
temperature_c

relative_humidity_2m
        ↓
humidity_pct

precipitation
        ↓
precipitation_mm

wind_speed_10m
        ↓
wind_speed_kmh

time
        ↓
observed_at
```

---

## Step 3 — Load

`src/load.py` connects to PostgreSQL using SQLAlchemy.

Before inserting data, it reads:

```text
sql/schema.sql
```

and executes the schema.

The DataFrame is then loaded into:

```text
weather_hourly
```

using Pandas:

```python
df.to_sql(
    "weather_hourly",
    connection,
    if_exists="append",
    index=False,
    method="multi",
)
```

---

# 4. Project Structure

```text
Weather_ETL_project/
│
├── .env
├── .env.example
├── .gitignore
├── docker-compose.yml
├── requirements.txt
├── README.md
├── run.py
│
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── extract.py
│   ├── transform.py
│   ├── load.py
│   ├── main.py
│   └── __pycache__/
│
└── sql/
    ├── schema.sql
    └── queries.sql
```

> `__pycache__/` is automatically generated by Python and should not be committed to Git.

---

# 5. File and Folder Responsibilities

## `.env`

Contains local environment variables and database configuration.

Example:

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

### Important

`.env` should **not** be committed to GitHub.

It may contain passwords, API keys, or other private configuration.

---

# 6. `.env.example`

This file provides a template for the required environment variables.

Example:

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

Unlike `.env`, `.env.example` is intended to be committed to Git.

---

# 7. `.gitignore`

The `.gitignore` file prevents unnecessary or sensitive files from being tracked by Git.

Recommended contents:

```gitignore
# Python
__pycache__/
*.py[cod]
*.pyo

# Virtual environment
.venv/
venv/
env/

# Environment variables
.env
.env.*
!.env.example

# IDE
.vscode/
.idea/

# Operating system
.DS_Store
Thumbs.db

# Logs
*.log
```

---

# 8. `docker-compose.yml`

This file creates the PostgreSQL database using Docker Compose.

Current configuration:

```yaml
services:
  postgres:
    image: postgres:16
    environment:
      POSTGRES_USER: weather
      POSTGRES_PASSWORD: weather
      POSTGRES_DB: weather_dw
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data

volumes:
  pgdata:
```
---

# 9. `requirements.txt`

Contains the Python dependencies required by the project.

```text
pandas>=2.2
requests>=2.32
SQLAlchemy>=2.0
psycopg2-binary>=2.9
python-dotenv>=1.0
pytest>=8.0
```

Install them using:

```bash
pip install -r requirements.txt
```

---

# 10. `run.py`

`run.py` is the main entry point for the project.

It imports the `run()` function from `src.main`:

```python
from src.main import run

run()
```

Therefore, the entire ETL pipeline can be started with:

```bash
python run.py
```

---

# 11. `src/__init__.py`

This file is currently empty.

It allows `src` to be treated as a Python package.

No code is required inside it for the current project.

---

# 12. `src/config.py`

Responsible for reading environment variables and creating the application configuration.

It uses:

```python
from dotenv import load_dotenv
```

and:

```python
load_dotenv()
```

The `Settings` class stores:

* Database host
* Database port
* Database name
* Database username
* Database password
* Latitude
* Longitude
* Location name
* Time zone
* Forecast days

It also creates the SQLAlchemy database URL:

```text
postgresql+psycopg2://USER:PASSWORD@HOST:PORT/DATABASE
```

---

# 13. `src/extract.py`

Responsible for extracting data from Open-Meteo.

The API endpoint is:

```text
https://api.open-meteo.com/v1/forecast
```

The function:

```python
extract()
```

returns the API response as a Python dictionary.

The request includes:

```text
latitude
longitude
timezone
forecast_days
hourly
```

The hourly fields are:

```text
temperature_2m
relative_humidity_2m
precipitation
wind_speed_10m
weather_code
```

---

# 14. `src/transform.py`

Responsible for transforming the API response.

It converts the raw API data into a DataFrame containing:

```text
location_name
latitude
longitude
timezone
observed_at
temperature_c
humidity_pct
precipitation_mm
wind_speed_kmh
weather_code
```

It also performs validation.

### Duplicate handling

Duplicate records are removed using:

```python
df.drop_duplicates(
    subset=["location_name", "observed_at"]
)
```

This matches the database uniqueness rule.

### NULL validation

Required numerical columns are checked for missing values.

If required values contain NULLs, the transformation raises:

```text
ValueError
```

---

# 15. `src/load.py`

Responsible for loading transformed data into PostgreSQL.

The process is:

```text
Create SQLAlchemy engine
        ↓
Open database transaction
        ↓
Read schema.sql
        ↓
Create weather_hourly table if necessary
        ↓
Insert DataFrame
        ↓
Commit transaction
```

The database URL comes from:

```python
settings.database_url
```

---

# 16. `src/main.py`

This file coordinates the entire ETL process.

The workflow is:

```python
payload = extract()

dataframe = transform(payload)

row_count = load(dataframe)
```

It also logs each stage:

```text
Extracting weather data
Transforming weather data
Loading weather data
Loaded 168 rows
```

---

# 17. `sql/schema.sql`

Defines the PostgreSQL table.

The main table is:

```text
weather_hourly
```

Columns:

| Column           | Type             | Purpose                  |
| ---------------- | ---------------- | ------------------------ |
| id               | BIGSERIAL        | Primary key              |
| location_name    | TEXT             | Location                 |
| latitude         | DOUBLE PRECISION | Latitude                 |
| longitude        | DOUBLE PRECISION | Longitude                |
| timezone         | TEXT             | Time zone                |
| observed_at      | TIMESTAMP        | Weather observation time |
| temperature_c    | DOUBLE PRECISION | Temperature              |
| humidity_pct     | DOUBLE PRECISION | Humidity                 |
| precipitation_mm | DOUBLE PRECISION | Precipitation            |
| wind_speed_kmh   | DOUBLE PRECISION | Wind speed               |
| weather_code     | INTEGER          | Weather condition code   |
| loaded_at        | TIMESTAMPTZ      | Data load timestamp      |

---

# 18. Database Uniqueness Rule

The table contains:

```sql
UNIQUE(location_name, observed_at)
```

This means that the same location cannot have two records for the exact same observation timestamp.

For example, this combination can only appear once:

```text
Cairo + 2026-08-30 00:00:00
```

This prevents duplicate weather observations.

---

# 19. Database Index

The project also creates:

```sql
CREATE INDEX IF NOT EXISTS idx_weather_observed_at
ON weather_hourly(observed_at);
```

This improves queries that search or sort weather data by observation time.

---

# 20. `sql/queries.sql`

Contains analytical queries for the stored weather data.

The intended queries include:

### Latest 24 hourly records

Returns the most recent 24 weather observations.

### Daily weather summary

Calculates:

* Average temperature
* Minimum temperature
* Maximum temperature
* Total precipitation
* Average wind speed

### Ten windiest hours

Returns the ten records with the highest wind speed.

### Hours with precipitation

Returns weather observations where:

```text
precipitation_mm > 0
```

---

# 21. Installation

## Step 1 — Clone the repository

```bash
git clone <YOUR_REPOSITORY_URL>
```

Move into the project:

```bash
cd Weather_ETL_project
```

---

# 22. Create a Virtual Environment

Windows:

```powershell
python -m venv .venv
```

Activate it in PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Or in Git Bash:

```bash
source .venv/Scripts/activate
```

You should see something similar to:

```text
(.venv)
```

at the beginning of your terminal prompt.

---

# 23. Install Dependencies

Run:

```bash
pip install -r requirements.txt
```

---

# 24. Configure Environment Variables

Create:

```text
.env
```

in the root project directory.

Add:

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

---

# 25. Start PostgreSQL

Make sure Docker Desktop is running.

Then:

```bash
docker compose up -d
```

Check the container:

```bash
docker compose ps
```

Expected result:

```text
NAME                             IMAGE         STATUS
weather_etl_project-postgres-1   postgres:16   Up
```

You can also run:

```bash
docker ps
```

---

# 26. Check PostgreSQL Logs

If PostgreSQL doesn't start:

```bash
docker compose logs postgres
```

A successful startup should eventually contain:

```text
database system is ready to accept connections
```

---

# 27. Run the ETL Pipeline

With the virtual environment activated:

```bash
python run.py
```

Expected output:

```text
INFO Extracting weather data
INFO Transforming weather data
INFO Loading weather data
INFO Loaded 168 rows
```

The exact number of rows can change depending on the configured forecast period and API response.

---

# 28. Verify the Data

Make sure the PostgreSQL container is running:

```bash
docker compose ps
```

Then execute:

```bash
docker compose exec postgres psql -U weather -d weather_dw -c "SELECT * FROM weather_hourly LIMIT 5;"
```

> Make sure there are no unnecessary `\` characters after `postgres`, `weather`, or `weather_dw`.

For example, this is correct:

```bash
docker compose exec postgres psql -U weather -d weather_dw -c "SELECT * FROM weather_hourly LIMIT 5;"
```

---

# 29. Check Number of Records

Run:

```bash
docker compose exec postgres psql -U weather -d weather_dw -c "SELECT COUNT(*) FROM weather_hourly;"
```

---

# 30. Run Analytical Queries

You can enter the PostgreSQL shell:

```bash
docker compose exec postgres psql -U weather -d weather_dw
```

Then:

```sql
SELECT *
FROM weather_hourly
LIMIT 5;
```

Exit using:

```sql
\q
```

---

# 31. Common Error: PostgreSQL Container Exited

### Error

```text
Error: Database is uninitialized and superuser password is not specified.
```

### Cause

PostgreSQL was not given:

```text
POSTGRES_PASSWORD
```

Make sure `docker-compose.yml` contains:

```yaml
environment:
  POSTGRES_USER: weather
  POSTGRES_PASSWORD: weather
  POSTGRES_DB: weather_dw
```

Do not write:

```yaml
POSTGRESL_PASSWORD
```

---

# 32. Common Error: Connection Refused

### Error

```text
psycopg2.OperationalError:
connection to server at "localhost" port 5432 failed:
Connection refused
```

### Cause

PostgreSQL is not running.

Check:

```bash
docker compose ps
```

If the container is stopped:

```bash
docker compose up -d
```

Then check:

```bash
docker compose logs postgres
```

Look for:

```text
database system is ready to accept connections
```

---

# 33. Common Error: `service "postgres\\" is not running`

If you run something like:

```bash
docker compose exec postgres\ psql ...
```

Docker interprets the backslash as part of the service name.

Use:

```bash
docker compose exec postgres psql -U weather -d weather_dw -c "SELECT * FROM weather_hourly LIMIT 5;"
```

There should be a space between:

```text
postgres
```

and:

```text
psql
```

---

# 34. Common Error: Duplicate Key

### Error

```text
psycopg2.errors.UniqueViolation:
duplicate key value violates unique constraint
```

For example:

```text
Key (location_name, observed_at) =
(Cairo, 2026-08-30 00:00:00) already exists
```

### Why it happens

The database has:

```sql
UNIQUE(location_name, observed_at)
```

The pipeline uses:

```python
if_exists="append"
```

Therefore, running the pipeline again attempts to insert the same weather observations again.

The database correctly rejects the duplicates.

---

# 35. Why `drop_duplicates()` Doesn't Completely Solve It

The transformation contains:

```python
df.drop_duplicates(
    subset=["location_name", "observed_at"]
)
```

This removes duplicates **inside the current DataFrame**.

It does not remove records that already exist in PostgreSQL.

For example:

```text
DataFrame:
Cairo | 2026-08-30 00:00
Cairo | 2026-08-30 01:00

Database:
Cairo | 2026-08-30 00:00
Cairo | 2026-08-30 01:00
```

The DataFrame itself contains no duplicates, but PostgreSQL already contains those records.

---

# 36. Handling Duplicate Records

There are two common strategies.

## Option A — Ignore Existing Records

Use PostgreSQL:

```sql
ON CONFLICT DO NOTHING
```

This keeps existing records and inserts only new ones.

This is useful when historical weather observations should not be modified.

---

## Option B — Upsert Existing Records

Use:

```sql
ON CONFLICT DO UPDATE
```

This updates an existing record if the same:

```text
location_name + observed_at
```

already exists.

This can be useful for forecast data because the API may provide updated values for the same timestamp.

---

# 37. Important Current Behavior

At the moment, the project uses:

```python
method="multi"
```

This means Pandas combines multiple rows into a larger INSERT statement.

It **does not** automatically handle duplicate records.

Therefore, if the pipeline is executed multiple times against the same database, duplicate-key errors can occur unless conflict handling is added.

---

# 38. Common Error: Missing Python Package

Example:

```text
ModuleNotFoundError: No module named 'pandas'
```

or:

```text
ModuleNotFoundError: No module named 'sqlalchemy'
```

Make sure the virtual environment is activated.

Then run:

```bash
pip install -r requirements.txt
```

You can check installed packages:

```bash
pip list
```

---

# 39. Common Error: `python` Not Recognized

If Windows cannot find Python:

```text
python is not recognized...
```

Install Python and make sure Python is added to PATH.

Then verify:

```bash
python --version
```

---

# 40. Common Error: `pip` Not Recognized

Try:

```bash
python -m pip --version
```

Then install:

```bash
python -m pip install -r requirements.txt
```

---

# 41. Common Error: Open-Meteo Request Failure

The extraction code uses:

```python
response.raise_for_status()
```

Therefore, HTTP errors will raise an exception.

Possible causes include:

* Internet connection problems
* API temporarily unavailable
* Invalid request parameters
* API rate limits
* Incorrect latitude/longitude
* Invalid timezone

Check your `.env` values.

---

# 42. Common Error: Missing `.env`

If `.env` doesn't exist, `config.py` uses default values.

However, it is recommended to create `.env` locally.

Copy the values from:

```text
.env.example
```

into:

```text
.env
```

---

# 43. Common Error: Database Authentication Failure

Example:

```text
password authentication failed
```

Check that the credentials in `.env` match Docker Compose:

```env
DB_USER=weather
DB_PASSWORD=weather
DB_NAME=weather_dw
DB_HOST=localhost
DB_PORT=5432
```

and:

```yaml
POSTGRES_USER: weather
POSTGRES_PASSWORD: weather
POSTGRES_DB: weather_dw
```

---

# 44. PostgreSQL Volume Issues

Docker stores PostgreSQL data in the named volume:

```text
pgdata
```

This means database data can survive container recreation.

If you intentionally want to completely reset the database:

```bash
docker compose down -v
```

Then:

```bash
docker compose up -d
```

### WARNING

`docker compose down -v` deletes the PostgreSQL Docker volume and therefore deletes the stored database data.

Only use this if you intentionally want a fresh database.

---

# 45. Useful Docker Commands

### Start containers

```bash
docker compose up -d
```

### Stop containers

```bash
docker compose stop
```

### Stop and remove containers

```bash
docker compose down
```

### Stop and remove containers + volumes

```bash
docker compose down -v
```

### Show running containers

```bash
docker ps
```

### Show all containers

```bash
docker ps -a
```

### Show Compose services

```bash
docker compose ps
```

### View PostgreSQL logs

```bash
docker compose logs postgres
```

### Follow logs live

```bash
docker compose logs -f postgres
```

### Open PostgreSQL shell

```bash
docker compose exec postgres psql -U weather -d weather_dw
```

---

# 46. Useful PostgreSQL Commands

Once inside `psql`:

### Show databases

```sql
\l
```

### Show tables

```sql
\dt
```

### Describe table

```sql
\d weather_hourly
```

### Count rows

```sql
SELECT COUNT(*)
FROM weather_hourly;
```

### Show latest records

```sql
SELECT *
FROM weather_hourly
ORDER BY observed_at DESC
LIMIT 24;
```

### Exit

```sql
\q
```

---

# 47. Recommended Development Workflow

When working on the project:

```text
1. Start Docker Desktop
        ↓
2. Activate .venv
        ↓
3. Start PostgreSQL
        ↓
4. Check docker compose ps
        ↓
5. Run python run.py
        ↓
6. Check ETL logs
        ↓
7. Query PostgreSQL
        ↓
8. Modify code if needed
        ↓
9. Run tests/checks
        ↓
10. Commit changes to Git
```

---

# 48. Git and GitHub

The following files should normally be committed:

```text
.env.example
.gitignore
docker-compose.yml
requirements.txt
README.md
run.py
src/
sql/
```

The following should **not** be committed:

```text
.env
.venv/
__pycache__/
*.pyc
```

---

# 49. Check Git Status

Run:

```bash
git status
```

Make sure sensitive/local files are not being tracked.

You can check whether a file is tracked using:

```bash
git ls-files
```

---

# 50. If `.env` Was Previously Tracked

If `.env` has been added to Git tracking but has not been pushed:

```bash
git rm --cached .env
```

Then commit:

```bash
git commit -m "Stop tracking environment file"
```

The `.env` file remains on your computer.

---

# 51. Git Security

Never commit real:

* Passwords
* API keys
* Access tokens
* Cloud credentials
* Database credentials
* Private keys

Use `.env` for local secrets and `.env.example` as a safe template.

---

# 52. Data Warehouse Design

The project uses a simple weather fact-style table:

```text
weather_hourly
```

Each record represents weather information for:

```text
one location
+
one observation timestamp
```

The logical unique key is:

```text
location_name + observed_at
```

The table also contains:

```text
loaded_at
```

which records when the ETL process inserted the record.

---

# 53. Example Data

A row might conceptually look like:

```text
location_name:      Cairo
latitude:           30.0444
longitude:          31.2357
timezone:           Africa/Cairo
observed_at:        2026-08-30 12:00:00
temperature_c:      32.5
humidity_pct:      45
precipitation_mm:  0
wind_speed_kmh:    17.2
weather_code:      1
loaded_at:          2026-08-30 ...
```

---

# 54. Current Pipeline Output

A successful execution should produce logs similar to:

```text
INFO Extracting weather data
INFO Transforming weather data
INFO Loading weather data
INFO Loaded 168 rows
```

For a seven-day hourly forecast:

```text
7 × 24 = 168
```

So 168 rows is expected when the API returns all hourly observations for seven days.

---

# 55. Why 168 Rows?

The configuration currently contains:

```env
FORECAST_DAYS=7
```

There are:

```text
24 hours × 7 days = 168 hours
```

Therefore:

```text
168 hourly records
```

is expected for one location when every hour is returned.

---

# 56. Changing the Location

The project can be configured for another location by changing:

```env
LATITUDE=
LONGITUDE=
LOCATION_NAME=
TIME_ZONE=
```

For example, the coordinates and time zone could be changed to another city.

The Python code itself does not need to be modified for basic location changes.

---

# 57. Changing Forecast Length

Change:

```env
FORECAST_DAYS=7
```

For example:

```env
FORECAST_DAYS=3
```

would request three days of forecast data.

The approximate number of hourly records would then be:

```text
3 × 24 = 72
```

---

# 58. Project Strengths

This project demonstrates several important data-engineering concepts:

* API integration
* ETL architecture
* Data cleaning
* Data validation
* Relational database design
* Unique constraints
* Indexes
* Dockerized PostgreSQL
* Environment-based configuration
* SQL analytics
* Python modularization
* Logging
* Reproducible development environment

---

# 59. Possible Future Improvements

The project can be extended with:

### Better duplicate handling

Implement PostgreSQL:

```text
ON CONFLICT DO NOTHING
```

or:

```text
ON CONFLICT DO UPDATE
```

to make repeated ETL executions safer.

### Automated scheduling

Run the ETL automatically using:

* Windows Task Scheduler
* Cron
* Airflow
* Prefect
* Dagster

### Testing

Add unit tests for:

* `extract()`
* `transform()`
* `load()`

using `pytest`.

### Data quality checks

Add validation for:

* Temperature ranges
* Humidity between 0 and 100
* Non-negative precipitation
* Non-negative wind speed
* Valid weather codes

### Multiple locations

Instead of one location, process several cities:

```text
Cairo
Alexandria
Giza
Luxor
Aswan
```

### Dashboard

Connect PostgreSQL to:

* Power BI
* Tableau
* Grafana
* Streamlit

to visualize weather trends.

### Containerize the Python application

The current Docker setup runs PostgreSQL in Docker while the ETL Python application runs locally.

A future version could run both inside Docker Compose.

---

# 60. Troubleshooting Checklist

If the pipeline doesn't work, check these in order:

```text
□ Docker Desktop is running
        ↓
□ PostgreSQL container is running
        ↓
□ docker compose ps shows "Up"
        ↓
□ PostgreSQL logs show "ready to accept connections"
        ↓
□ .env exists
        ↓
□ DB_HOST is localhost
        ↓
□ DB_PORT is 5432
        ↓
□ DB_NAME is weather_dw
        ↓
□ DB_USER is weather
        ↓
□ DB_PASSWORD matches Docker
        ↓
□ .venv is activated
        ↓
□ requirements.txt dependencies are installed
        ↓
□ Internet connection works
        ↓
□ Open-Meteo API responds
        ↓
□ python run.py executes
        ↓
□ PostgreSQL contains weather_hourly
```

---

# 61. Quick Start

For experienced users, the entire setup can be summarized as:

```bash
git clone <YOUR_REPOSITORY_URL>

cd Weather_ETL_project

python -m venv .venv
```

Activate the environment:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create `.env` using `.env.example`.

Start PostgreSQL:

```bash
docker compose up -d
```

Check:

```bash
docker compose ps
```

Run the ETL:

```bash
python run.py
```

Check the database:

```bash
docker compose exec postgres psql -U weather -d weather_dw -c "SELECT COUNT(*) FROM weather_hourly;"
```

---

# 62. Final Architecture

The complete project can be understood as:

```text
┌─────────────────────────────────────────────┐
│              WEATHER ETL PROJECT            │
└─────────────────────────────────────────────┘

                Configuration
                     │
                     ▼
                  .env
                     │
                     ▼
                config.py
                     │
                     │
        ┌────────────┴────────────┐
        │                         │
        ▼                         ▼
 Open-Meteo API              PostgreSQL
        │                    Docker Container
        ▼                         ▲
   extract.py                     │
        │                         │
        ▼                         │
  transform.py                    │
        │                         │
        ▼                         │
    DataFrame                     │
        │                         │
        ▼                         │
     load.py ─────────────────────┘
        │
        ▼
 weather_hourly
        │
        ▼
 queries.sql
        │
        ▼
 Weather Analysis
```

---

# 63. Conclusion

The Weather ETL Project provides a complete end-to-end example of a small data engineering pipeline.

The project takes raw weather information from an external API, transforms it into structured and validated data, and stores it in a PostgreSQL data warehouse.

The core pipeline is:

```text
Extract
   ↓
Transform
   ↓
Validate
   ↓
Load
   ↓
Analyze
```

The project can serve as a foundation for more advanced data engineering features such as scheduling, data-quality monitoring, multiple locations, dashboards, automated testing, and production-grade upsert handling.

note: this README.md was generated using an ai tool (to make it easy on my self) so it might not be as easy for you (lovly fluffy bro programmer) to under stand it steps; i even don't fully understand steps that is generated :-) , so don't get frustraited, i have high hope that i'm gonna change it to much simpler and easy to understand readme.md file, but untill then, see yaa... 
