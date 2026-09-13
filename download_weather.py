import requests
import pandas as pd
from pathlib import Path

url = "https://historical-forecast-api.open-meteo.com/v1/forecast"

params = {
    "latitude": 28.6280,
    "longitude": 77.2410,
    "start_date": "2024-01-01",
    "end_date": "2025-12-31",
    "hourly": [
        "temperature_2m",
        "relative_humidity_2m",
        "wind_speed_10m",
        "wind_direction_10m",
        "pressure_msl",
        "precipitation",
        "boundary_layer_height"
    ],
    "timezone": "UTC"
}

print("Downloading historical weather data...")

response = requests.get(url, params=params, timeout=120)
response.raise_for_status()

data = response.json()

df = pd.DataFrame(data["hourly"])

output = Path("data/raw_data/weather_historical_2024_2025.csv")
output.parent.mkdir(parents=True, exist_ok=True)

df.to_csv(output, index=False)

print("\nDownload completed.")
print("Rows:", len(df))
print("Columns:", len(df.columns))
print("Saved to:", output)

print("\nFirst rows:")
print(df.head())

print("\nLast rows:")
print(df.tail())
