import requests
import pandas as pd
from pathlib import Path

LAT = 28.6280
LON = 77.2410

START_DATE = "2024-01-01"
END_DATE = "2025-12-31"

URL = "https://historical-forecast-api.open-meteo.com/v1/forecast"

PARAMS = {
    "latitude": LAT,
    "longitude": LON,
    "start_date": START_DATE,
    "end_date": END_DATE,
    "hourly": ",".join([
        "temperature_2m",
        "relative_humidity_2m",
        "wind_speed_10m",
        "wind_direction_10m",
        "pressure_msl",
        "precipitation"
    ]),
    "timezone": "UTC"
}

print("Downloading historical forecast weather...")
print(f"Location: {LAT}, {LON}")
print(f"Period: {START_DATE} to {END_DATE}")

response = requests.get(URL, params=PARAMS, timeout=120)
response.raise_for_status()

data = response.json()

hourly = data["hourly"]

df = pd.DataFrame(hourly)

output = Path("data/raw_data/weather_forecast_historical_2024_2025.csv")
df.to_csv(output, index=False)

print("\nDownload completed.")
print(f"Rows: {len(df):,}")
print(f"Columns: {len(df.columns)}")
print(f"Saved to: {output}")

print("\nColumns:")
print(df.columns.tolist())

print("\nFirst 5 rows:")
print(df.head())

print("\nMissing values:")
print(df.isna().sum())

print("\nCompleted successfully.")