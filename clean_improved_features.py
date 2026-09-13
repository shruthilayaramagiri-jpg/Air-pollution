import pandas as pd
import numpy as np

INPUT = "data/cleaned/improved_features_24h.csv"
OUTPUT = "data/cleaned/improved_features_24h_clean.csv"

print("Loading improved features...")
df = pd.read_csv(INPUT)

df["Timestamp"] = pd.to_datetime(df["Timestamp"], utc=True)
df = df.sort_values("Timestamp").reset_index(drop=True)

print(f"Original rows: {len(df)}")

# ---------------------------------------------------------
# 1. Identify target columns
# ---------------------------------------------------------

targets = [
    "target_PM25_24h",
    "target_PM25_48h",
    "target_PM25_72h"
]

# ---------------------------------------------------------
# 2. Pollution columns
# ---------------------------------------------------------

pollution_cols = [
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

# Only use columns that actually exist
pollution_cols = [c for c in pollution_cols if c in df.columns]

# ---------------------------------------------------------
# 3. Convert pollution values to numeric
# ---------------------------------------------------------

for col in pollution_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# ---------------------------------------------------------
# 4. Fill ONLY short gaps in raw pollution inputs
# ---------------------------------------------------------
# Limit = 3 means we do not manufacture values across
# long monitoring outages.

for col in pollution_cols:
    df[col] = df[col].interpolate(
        method="linear",
        limit=3,
        limit_direction="both"
    )

# ---------------------------------------------------------
# 5. Recalculate lag/rolling/change features
# ---------------------------------------------------------
# This prevents the old missing values from remaining in
# derived features.

feature_specs = {
    "PM2.5 (µg/m³)": [1, 3, 6, 12, 24],
    "PM10 (µg/m³)": [1, 3, 6, 12, 24],
    "NO2 (µg/m³)": [1, 3, 6, 12, 24],
    "SO2 (µg/m³)": [1, 3, 6, 12, 24],
    "CO (mg/m³)": [1, 3, 6, 12, 24],
    "Ozone (µg/m³)": [1, 3, 6, 12, 24],
}

for col, lags in feature_specs.items():

    if col not in df.columns:
        continue

    for lag in lags:
        feature = f"{col}_lag{lag}"

        if feature in df.columns:
            df[feature] = df[col].shift(lag)

    for hours in [1, 3, 6]:

        feature = f"{col}_change_{hours}h"

        if feature in df.columns:
            df[feature] = df[col] - df[col].shift(hours)

    for window in [3, 6, 12, 24]:

        mean_feature = f"{col}_rolling_mean_{window}h"
        std_feature = f"{col}_rolling_std_{window}h"

        if mean_feature in df.columns:
            df[mean_feature] = (
                df[col]
                .rolling(window=window, min_periods=window)
                .mean()
            )

        if std_feature in df.columns:
            df[std_feature] = (
                df[col]
                .rolling(window=window, min_periods=window)
                .std()
            )

# ---------------------------------------------------------
# 6. Weather derived features
# ---------------------------------------------------------

weather_cols = [
    "temperature_2m",
    "relative_humidity_2m",
    "wind_speed_10m",
    "pressure_msl",
    "precipitation"
]

for col in weather_cols:

    if col not in df.columns:
        continue

    for lag in [1, 3, 6, 12, 24]:

        feature = f"{col}_lag{lag}"

        if feature in df.columns:
            df[feature] = df[col].shift(lag)

    for window in [3, 6, 12, 24]:

        feature = f"{col}_rolling_mean_{window}h"

        if feature in df.columns:
            df[feature] = (
                df[col]
                .rolling(window=window, min_periods=window)
                .mean()
            )

# ---------------------------------------------------------
# 7. Wind components
# ---------------------------------------------------------

if "wind_speed_10m" in df.columns and "wind_direction_10m" in df.columns:

    direction = np.deg2rad(df["wind_direction_10m"])

    df["wind_u"] = -df["wind_speed_10m"] * np.sin(direction)
    df["wind_v"] = -df["wind_speed_10m"] * np.cos(direction)

# ---------------------------------------------------------
# 8. Targets must NEVER be interpolated
# ---------------------------------------------------------

print("\nTarget missing values before removal:")

for target in targets:
    if target in df.columns:
        print(target, df[target].isna().sum())

# Remove rows without actual future target observations
df = df.dropna(subset=targets)

# ---------------------------------------------------------
# 9. Remove rows where important historical PM2.5
#    information is still unavailable
# ---------------------------------------------------------

required_history = [
    "PM2.5 (µg/m³)_lag1",
    "PM2.5 (µg/m³)_lag3",
    "PM2.5 (µg/m³)_lag6",
    "PM2.5 (µg/m³)_lag12",
    "PM2.5 (µg/m³)_lag24",
]

required_history = [
    c for c in required_history if c in df.columns
]

before = len(df)

df = df.dropna(subset=required_history)

print(f"\nRemoved rows without reliable PM2.5 history: {before - len(df)}")

# ---------------------------------------------------------
# 10. Remove rows with excessive remaining missing features
# ---------------------------------------------------------

feature_cols = [
    c for c in df.columns
    if c not in targets and c != "Timestamp"
]

missing_fraction = df[feature_cols].isna().mean(axis=1)

before = len(df)

# Allow at most 10% missing features
df = df[missing_fraction <= 0.10].copy()

print(f"Removed rows with >10% missing features: {before - len(df)}")

# ---------------------------------------------------------
# 11. Final report
# ---------------------------------------------------------

df = df.sort_values("Timestamp").reset_index(drop=True)

print("\n========== CLEANING RESULT ==========")
print(f"Rows: {len(df)}")
print(f"Columns: {len(df.columns)}")
print(f"Start: {df['Timestamp'].min()}")
print(f"End:   {df['Timestamp'].max()}")

remaining = df.isna().sum()
remaining = remaining[remaining > 0].sort_values(ascending=False)

print("\nRemaining missing values:")

if len(remaining) == 0:
    print("NONE")
else:
    print(remaining.to_string())

df.to_csv(OUTPUT, index=False)

print(f"\nSaved: {OUTPUT}")
print("========== COMPLETED ==========")