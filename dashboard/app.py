import sys
from pathlib import Path
import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

# Allow importing from src/

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.config import settings

# Page Config
st.set_page_config(
    page_title="Weather Dashboard",
    page_icon="🌤️",
    layout="wide",
)

st.title("Weather Dashboard Analysis 🌤️")
st.caption("Powered by Open-Meteo API + PostgreSQL + Streamlit + Plotly")

# DATABASE CONNECTION
@st.cache_data(ttl=300)
def load_weather_data():
    engine = create_engine(settings.database_url)

    query = """
    SELECT 
        location_name,
        latitude,
        longitude,
        timezone,
        observed_at,
        temperature_c,
        humidity_pct,
        precipitation_mm,
        wind_speed_kmh,
        weather_code,
        loaded_at
    FROM weather_hourly
    ORDER BY observed_at 
    """

    df = pd.read_sql(query, engine)

    if not df.empty:
        df["observed_at"] = pd.to_datetime(df["observed_at"])

    return df

df = load_weather_data()

if df.empty:
    st.warning("No weather data found in PostgreSQL.")
    st.stop()

# SIDEBAR FILTERS

min_date = df["observed_at"].min().date()
max_date = df["observed_at"].max().date()

selected_dates = st.sidebar.date_input(
    "Date Range",
    value=(min_date, max_date),
)

if len(selected_dates) == 2:
    start_date, end_date = selected_dates

    filtered_df = df[
        (df["observed_at"].dt.date >= start_date)
        & (df["observed_at"].dt.date <= end_date)
    ]
else:
    filtered_df = df.copy()

if filtered_df.empty:
    st.warning("No data available for the selected date range.")
    st.stop()

# KPI Metrics
latest = filtered_df.sort_values("observed_at").iloc[-1]
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("🌡 Temperature (°C)", f"{latest['temperature_c']:.1f} (°C)")
with col2:
    st.metric("💧 Humidity (%)", f"{latest['humidity_pct']:.0f} (%)")
with col3:
    st.metric("🌬 Wind Speed (km/h)", f"{latest['wind_speed_kmh']:.1f} (km/h)")
with col4:
    st.metric("🌧 Precipitation (mm)", f"{latest['precipitation_mm']:.1f} (mm)")

st.divider()

# TEMPERATURE TREND
fig_temp = px.line(
    filtered_df,
    x="observed_at",
    y="temperature_c",
    title="Temperature Trend (°C)",
    markers=True,
)

fig_temp.update_layout(
    xaxis_title="Date / Time",
    yaxis_title="Temperature (°C)",
)

st.plotly_chart(
    fig_temp,
    use_container_width=True,
)

#HUMIDITY AND WIND SPEED
col_left, col_right = st.columns(2)
with col_left:
    fig_humidity = px.line(
        filtered_df,
        x="observed_at",
        y="humidity_pct",
        title="Humidity Trend (%)",
    )

    fig_humidity.update_layout(yaxis_title="Humidity (%)")

    st.plotly_chart(fig_humidity, use_container_width=True)

with col_right:
    fig_wind = px.line(
        filtered_df,
        x="observed_at",
        y="wind_speed_kmh",
        title="Wind Speed Trend (km/h)",
    )

    fig_wind.update_layout(yaxis_title="Wind Speed (km/h)")

    st.plotly_chart(fig_wind, use_container_width=True)


# TOP 10 WINDEST HOURS
st.subheader("Top 10 Windest Hours")

top_wind = (filtered_df.sort_values("wind_speed_kmh", ascending=False).head(10))

fig_top_wind = px.bar(
    top_wind,
    x="observed_at",
    y="wind_speed_kmh",
    title="Highest Wind Speed Hours (km/h)",
)

st.plotly_chart(fig_top_wind, use_container_width=True)

#PRECIPITATION FORECAST --
st.subheader("🌧 Hours With Precipitation")

rain_df = filtered_df[
    filtered_df["precipitation_mm"] > 0
]

if rain_df.empty:
    st.success(
        "No precipitation expected."
    )
else:
    st.dataframe(
        rain_df[
            [
                "observed_at",
                "precipitation_mm",
                "temperature_c",
                "humidity_pct",
            ]
        ],
        use_container_width=True,
    )



# DAILY SUMMARY


st.subheader("📅 Daily Summary")

daily_summary = (
    filtered_df
    .assign(
        day=filtered_df["observed_at"].dt.date
    )
    .groupby("day")
    .agg(
        avg_temp=("temperature_c", "mean"),
        min_temp=("temperature_c", "min"),
        max_temp=("temperature_c", "max"),
        total_rain=("precipitation_mm", "sum"),
        avg_wind=("wind_speed_kmh", "mean"),
    )
    .reset_index()
)

daily_summary = daily_summary.round(1)

st.dataframe(
    daily_summary,
    use_container_width=True,
)



# RAW DATA


st.subheader("📄 Weather Data")

st.dataframe(
    filtered_df.sort_values(
        "observed_at",
        ascending=False
    ),
    use_container_width=True,
)



# FOOTER


st.divider()

st.caption(
    f"Location: {settings.location_name} | "
    f"Timezone: {settings.time_zone}"
)
