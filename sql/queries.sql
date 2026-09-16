--Latest 24 hourly records
SELECT 
location_name,
observed_at,
temperature_c,
humidity_pct,
precipitation_mm,
wind_speed_kmh,
weather_code
FROM public.weather_hourly
ORDER BY observed_at DESC
LIMIT 24;

--Daily weather summary
SELECT 
location_name,
observed_at::date as day,
ROUND(AVG(temperature_c)::numeric,1) AS average_temperature_c,
ROUND(MIN(temperature_c)::numeric,1) AS minimum_temperature_c,
ROUND(MAX(temperature_c)::numeric,1) AS maximum_temperature_c,
ROUND(SUM(precipitation_mm)::numeric,1) AS total_precipitation_mm,
ROUND(AVG(wind_speed_kmh)::numeric,1) AS average_wind_speed_kmh
FROM public.weather_hourly
GROUP BY location_name, observed_at::date
ORDER BY day;

--Ten windiest hours
SELECT
observed_at,
wind_speed_kmh,
temperature_c
FROM public.weather_hourly
ORDER BY wind_speed_kmh DESC
LIMIT 10;

--Hours with expected precipitation
SELECT
observed_at,
precipitation_mm,
temperature_c
FROM public.weather_hourly
WHERE precipitation_mm > 0
ORDER BY observed_at DESC;