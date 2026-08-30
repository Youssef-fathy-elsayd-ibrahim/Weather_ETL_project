import os 
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Settings:
    db_host: str = os.getenv("DB_HOST","localhost")
    db_port: str = os.getenv("DB_PORT","5432")
    db_name: str = os.getenv("DB_NAME","weather_dw")
    db_user: str = os.getenv("DB_USER","weather")
    db_password: str = os.getenv("DB_PASSWORD","weather")
    latitude: float = float(os.getenv("LATITUDE","30.0444"))
    longitude: float = float(os.getenv("LONGITUDE","31.2357"))
    location_name: str = os.getenv("LOCATION_NAME","cairo")
    time_zone: str = os.getenv("TIME_ZONE","Africa/cairo")
    forecast_days: int = int(os.getenv("FORECAST_DAYS","7"))

    @property
    def database_url(self)->str:
        return(
            f"postgresql+psycopg2://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )


settings = Settings()