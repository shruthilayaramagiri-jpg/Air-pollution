import requests
import pandas as pd
from pathlib import Path

LAT = 28.6280
LON = 77.2410

START_DATE = "1995-01-01"
END_DATE = "2025-12-31"

URL = "https://archive-api.open-meteo.com/v1/archive"

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
    "models": "era5",
    "timezone": "UTC",
    "wind_speed_unit": "ms"
}

print("\n========== LONG-TERM WEATHER DOWNLOAD ==========\n")
print("Model: ERA5")
print(f"Location: {LAT}, {LON}")
print(f"Period: {START_DATE} to {END_DATE}")
print("\nDownloading...")

response = requests.get(URL, params=PARAMS, timeout=300)
response.raise_for_status()

data = response.json()

df = pd.DataFrame(data["hourly"])

output = Path(
    "data/raw_data/weather_era5_1995_2025.csv"
)

output.parent.mkdir(parents=True, exist_ok=True)

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

print("\n========== DOWNLOAD COMPLETED ==========\n")