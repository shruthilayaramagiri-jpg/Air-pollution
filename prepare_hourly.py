import pandas as pd

INPUT = "data/cleaned/cpcb_weather_2024_2025.csv"
OUTPUT = "data/cleaned/hourly_dataset.csv"

print("\n========== LOADING DATA ==========\n")

df = pd.read_csv(INPUT)

df["Timestamp"] = pd.to_datetime(df["Timestamp"], utc=True)

df = df.sort_values("Timestamp")

pollutants = [
    "PM2.5 (µg/m³)",
    "PM10 (µg/m³)",
    "NO (µg/m³)",
    "NO2 (µg/m³)",
    "NOx (ppb)",
    "NH3 (µg/m³)",
    "SO2 (µg/m³)",
    "CO (mg/m³)",
    "Ozone (µg/m³)",
    "Benzene (µg/m³)"
]

weather = [
    "temperature_2m",
    "relative_humidity_2m",
    "wind_speed_10m",
    "wind_direction_10m",
    "pressure_msl",
    "precipitation"
]

print("Original rows:", len(df))

# --------------------------------------------------
# Convert 15-minute observations to hourly averages
# --------------------------------------------------

df = df.set_index("Timestamp")

hourly_pollution = df[pollutants].resample("1h").mean()

hourly_weather = df[weather].resample("1h").mean()

hourly = pd.concat(
    [hourly_pollution, hourly_weather],
    axis=1
)

hourly = hourly.reset_index()

# --------------------------------------------------
# Keep only hours where at least some pollution data
# exists
# --------------------------------------------------

pollution_available = hourly[pollutants].notna().sum(axis=1)

hourly = hourly[pollution_available > 0].copy()

# --------------------------------------------------
# Add time features
# --------------------------------------------------

hourly["hour"] = hourly["Timestamp"].dt.hour
hourly["day"] = hourly["Timestamp"].dt.day
hourly["month"] = hourly["Timestamp"].dt.month
hourly["day_of_week"] = hourly["Timestamp"].dt.dayofweek

# Cyclic time features
import numpy as np

hourly["hour_sin"] = np.sin(
    2 * np.pi * hourly["hour"] / 24
)

hourly["hour_cos"] = np.cos(
    2 * np.pi * hourly["hour"] / 24
)

hourly["month_sin"] = np.sin(
    2 * np.pi * hourly["month"] / 12
)

hourly["month_cos"] = np.cos(
    2 * np.pi * hourly["month"] / 12
)

# --------------------------------------------------
# Save
# --------------------------------------------------

hourly.to_csv(OUTPUT, index=False)

print("\n========== HOURLY DATASET ==========\n")

print("Rows:", len(hourly))
print("Columns:", len(hourly.columns))

print("\nTime range:")
print(hourly["Timestamp"].min())
print(hourly["Timestamp"].max())

print("\nMissing values:")
print(hourly.isna().sum())

print("\nFirst 5 rows:")
print(hourly.head())

print("\nSaved to:")
print(OUTPUT)

print("\n========== COMPLETED ==========\n")