import pandas as pd
import numpy as np
from pathlib import Path

INPUT = Path("data/cleaned/hourly_dataset.csv")
OUTPUT = Path("data/cleaned/training_windows_24h.csv")

print("\n========== CREATING TRAINING WINDOWS ==========\n")

df = pd.read_csv(INPUT)
df["Timestamp"] = pd.to_datetime(df["Timestamp"], utc=True)
df = df.sort_values("Timestamp").reset_index(drop=True)

# Main variables
target = "PM2.5 (µg/m³)"

features = [
    "PM2.5 (µg/m³)",
    "PM10 (µg/m³)",
    "NO2 (µg/m³)",
    "SO2 (µg/m³)",
    "CO (mg/m³)",
    "Ozone (µg/m³)",
    "temperature_2m",
    "relative_humidity_2m",
    "wind_speed_10m",
    "wind_direction_10m",
    "pressure_msl",
    "precipitation"
]

# Make sure timestamps are hourly
df = df.set_index("Timestamp")

# Interpolate ONLY short gaps in input features
for col in features:
    df[col] = df[col].interpolate(
        method="time",
        limit=3,
        limit_direction="both"
    )

df = df.reset_index()

samples = []

# Need 24 previous hours + targets at +24,+48,+72
for i in range(24, len(df) - 72):

    history = df.iloc[i-24:i]
    future = df.iloc[i:i+73]

    # Require complete PM2.5 history
    if history[target].isna().any():
        continue

    # Require all three PM2.5 targets
    if (
        pd.isna(future.iloc[24][target])
        or pd.isna(future.iloc[48][target])
        or pd.isna(future.iloc[72][target])
    ):
        continue

    row = {
        "Timestamp": df.iloc[i]["Timestamp"],
        "target_PM25_24h": future.iloc[24][target],
        "target_PM25_48h": future.iloc[48][target],
        "target_PM25_72h": future.iloc[72][target],
    }

    # Add the last 24 hours of each feature
    for lag in range(1, 25):
        source = df.iloc[i-lag]

        for col in features:
            short_name = col.replace(" (µg/m³)", "").replace(" (mg/m³)", "")
            row[f"{short_name}_lag{lag}"] = source[col]

    samples.append(row)

result = pd.DataFrame(samples)

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
result.to_csv(OUTPUT, index=False)

print("Training window creation completed.")
print(f"Samples: {len(result):,}")
print(f"Columns: {len(result.columns)}")

if len(result) > 0:
    print(f"Start: {result['Timestamp'].min()}")
    print(f"End: {result['Timestamp'].max()}")

print("\nMissing values:")
print(result.isna().sum().sum())

print("\nSaved to:")
print(OUTPUT)

print("\n========== COMPLETED ==========\n")