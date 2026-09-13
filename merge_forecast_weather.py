import pandas as pd
from pathlib import Path

POLLUTION_FILE = "data/cleaned/hourly_dataset.csv"
WEATHER_FILE = "data/raw_data/weather_forecast_historical_2024_2025.csv"
OUTPUT_FILE = "data/cleaned/pollution_forecast_weather.csv"

print("\n========== MERGING CPCB + FORECAST WEATHER ==========\n")

# Load pollution dataset
pollution = pd.read_csv(POLLUTION_FILE)
pollution["Timestamp"] = pd.to_datetime(
    pollution["Timestamp"], utc=True
)

# Remove old historical-weather columns if they already exist
old_weather_cols = [
    "temperature_2m",
    "relative_humidity_2m",
    "wind_speed_10m",
    "wind_direction_10m",
    "pressure_msl",
    "precipitation",
]

pollution = pollution.drop(
    columns=[c for c in old_weather_cols if c in pollution.columns]
)

# Load forecast weather
weather = pd.read_csv(WEATHER_FILE)
weather["time"] = pd.to_datetime(
    weather["time"], utc=True
)

weather = weather.rename(columns={"time": "Timestamp"})

weather_cols = [
    "Timestamp",
    "temperature_2m",
    "relative_humidity_2m",
    "wind_speed_10m",
    "wind_direction_10m",
    "pressure_msl",
    "precipitation",
]

weather = weather[weather_cols]

# Sort
pollution = pollution.sort_values("Timestamp").reset_index(drop=True)
weather = weather.sort_values("Timestamp").reset_index(drop=True)

# Exact timestamp merge
merged = pollution.merge(
    weather,
    on="Timestamp",
    how="left"
)

print("Pollution rows:", len(pollution))
print("Weather rows:", len(weather))
print("Merged rows:", len(merged))

print("\nWeather missing values after merge:")
print(merged[old_weather_cols].isna().sum())

print("\nDate range:")
print("Start:", merged["Timestamp"].min())
print("End:  ", merged["Timestamp"].max())

print("\nColumns:")
print(merged.columns.tolist())

# Save
Path(OUTPUT_FILE).parent.mkdir(parents=True, exist_ok=True)
merged.to_csv(OUTPUT_FILE, index=False)

print("\nSaved to:")
print(OUTPUT_FILE)

print("\n========== MERGE COMPLETED ==========\n")