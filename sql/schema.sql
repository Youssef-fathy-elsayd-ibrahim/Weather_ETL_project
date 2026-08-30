CREATE TABLE IF NOT EXISTS weather_hourly( 
	id BIGSERIAL PRIMARY KEY,
	location_name TEXT NOT NULL,
	latitude DOUBLE PRECISION NOT NULL,
	longitude DOUBLE PRECISION NOT NULL,
	timezone TEXT NOT NULL,
	observed_at TIMESTAMP NOT NULL,
	temperature_c DOUBLE PRECISION NOT NULL,
	humidity_pct DOUBLE PRECISION NOT NULL,
	precipitation_mm DOUBLE PRECISION NOT NULL,
	wind_speed_kmh DOUBLE PRECISION NOT NULL,
	weather_code INTEGER NOT NULL,
	loaded_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

	UNIQUE(location_name, observed_at)
);							 

CREATE INDEX IF NOT EXISTS idx_weather_observed_at
ON weather_hourly(observed_at);