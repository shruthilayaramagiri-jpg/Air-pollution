import pandas as pd
from pathlib import Path

INPUT = Path("data/raw_data/weather_era5_1995_2025.csv")
OUTPUT = Path("data/cleaned/weather_era5_1995_2025_clean.csv")

print("\n========== PREPARING LONG-TERM WEATHER ==========\n")

df = pd.read_csv(INPUT)

# Convert time
df["time"] = pd.to_datetime(df["time"], utc=True)

# Rename columns to simpler names
df = df.rename(columns={
    "time": "Timestamp",
    "temperature_2m": "temperature",
    "relative_humidity_2m": "humidity",
    "wind_speed_10m": "wind_speed",
    "wind_direction_10m": "wind_direction",
    "pressure_msl": "pressure",
    "precipitation": "precipitation"
})

# Remove duplicate timestamps
df = df.drop_duplicates(subset="Timestamp")

# Sort chronologically
df = df.sort_values("Timestamp").reset_index(drop=True)

# Add useful time features
df["year"] = df["Timestamp"].dt.year
df["month"] = df["Timestamp"].dt.month
df["day"] = df["Timestamp"].dt.day
df["hour"] = df["Timestamp"].dt.hour
df["day_of_week"] = df["Timestamp"].dt.dayofweek

# Seasonal cyclic features
df["hour_sin"] = __import__("numpy").sin(
    2 * __import__("numpy").pi * df["hour"] / 24
)

df["hour_cos"] = __import__("numpy").cos(
    2 * __import__("numpy").pi * df["hour"] / 24
)

df["month_sin"] = __import__("numpy").sin(
    2 * __import__("numpy").pi * df["month"] / 12
)

df["month_cos"] = __import__("numpy").cos(
    2 * __import__("numpy").pi * df["month"] / 12
)

# Save
OUTPUT.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(OUTPUT, index=False)

print("Preparation completed.")
print(f"Rows: {len(df):,}")
print(f"Columns: {len(df.columns)}")
print(f"Start: {df['Timestamp'].min()}")
print(f"End: {df['Timestamp'].max()}")

print("\nMissing values:")
print(df.isna().sum())

print("\nFinal columns:")
print(df.columns.tolist())

print("\nSaved to:")
print(OUTPUT)

print("\n========== COMPLETED ==========\n")