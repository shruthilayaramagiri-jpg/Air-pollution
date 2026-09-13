import pandas as pd
from pathlib import Path

# Files
cpcb_file = "data/cleaned/cpcb_clean.csv"
weather_file = "data/raw_data/weather_historical_2024_2025.csv"
output_file = "data/cleaned/cpcb_weather_2024_2025.csv"

# Load
cpcb = pd.read_csv(cpcb_file)
weather = pd.read_csv(weather_file)

# Convert timestamps
cpcb["Timestamp"] = pd.to_datetime(cpcb["Timestamp"], utc=True)
weather["time"] = pd.to_datetime(weather["time"], utc=True)

# Remove boundary layer height for now
weather = weather.drop(columns=["boundary_layer_height"], errors="ignore")

# Rename weather timestamp
weather = weather.rename(columns={"time": "Timestamp"})

# Sort before merging
cpcb = cpcb.sort_values("Timestamp")
weather = weather.sort_values("Timestamp")

# Merge hourly weather with nearest CPCB timestamp
merged = pd.merge_asof(
    cpcb,
    weather,
    on="Timestamp",
    direction="nearest",
    tolerance=pd.Timedelta("30min")
)

# Save
Path("data/cleaned").mkdir(parents=True, exist_ok=True)
merged.to_csv(output_file, index=False)

print("\n========== MERGE REPORT ==========\n")

print("CPCB rows:", len(cpcb))
print("Weather rows:", len(weather))
print("Merged rows:", len(merged))

print("\nMerged columns:")
for col in merged.columns:
    print("-", col)

print("\nWeather missing values after merge:")
weather_columns = [
    "temperature_2m",
    "relative_humidity_2m",
    "wind_speed_10m",
    "wind_direction_10m",
    "pressure_msl",
    "precipitation"
]

print(merged[weather_columns].isna().sum())

print("\nFinal date range:")
print("Start:", merged["Timestamp"].min())
print("End  :", merged["Timestamp"].max())

print("\nSaved to:")
print(output_file)

print("\n========== MERGE COMPLETED ==========\n")