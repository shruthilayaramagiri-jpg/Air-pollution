import pandas as pd
import numpy as np

INPUT = "data/cleaned/hourly_dataset.csv"
OUTPUT = "data/cleaned/improved_features_24h.csv"

print("\n========== CREATING IMPROVED FEATURES ==========\n")

df = pd.read_csv(INPUT)

df["Timestamp"] = pd.to_datetime(df["Timestamp"], utc=True)
df = df.sort_values("Timestamp").reset_index(drop=True)

# Actual column names in your dataset
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

# Convert to numeric
for col in features:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# --------------------------------------------------
# 1. Time features
# --------------------------------------------------

df["hour_sin"] = np.sin(2 * np.pi * df["hour"] / 24)
df["hour_cos"] = np.cos(2 * np.pi * df["hour"] / 24)

df["month_sin"] = np.sin(2 * np.pi * df["month"] / 12)
df["month_cos"] = np.cos(2 * np.pi * df["month"] / 12)

# --------------------------------------------------
# 2. Lag features
# --------------------------------------------------

lag_features = [
    "PM2.5 (µg/m³)",
    "PM10 (µg/m³)",
    "NO2 (µg/m³)",
    "SO2 (µg/m³)",
    "CO (mg/m³)",
    "Ozone (µg/m³)",
    "temperature_2m",
    "relative_humidity_2m",
    "wind_speed_10m",
    "pressure_msl",
    "precipitation"
]

for col in lag_features:
    for lag in [1, 3, 6, 12, 24]:
        df[f"{col}_lag{lag}"] = df[col].shift(lag)

# --------------------------------------------------
# 3. Pollution trend features
# --------------------------------------------------

pollution_features = [
    "PM2.5 (µg/m³)",
    "PM10 (µg/m³)",
    "NO2 (µg/m³)",
    "SO2 (µg/m³)",
    "CO (mg/m³)",
    "Ozone (µg/m³)"
]

for col in pollution_features:

    df[f"{col}_change_1h"] = (
        df[col] - df[col].shift(1)
    )

    df[f"{col}_change_3h"] = (
        df[col] - df[col].shift(3)
    )

    df[f"{col}_change_6h"] = (
        df[col] - df[col].shift(6)
    )

# --------------------------------------------------
# 4. Rolling pollution statistics
# --------------------------------------------------

for col in pollution_features:

    for window in [3, 6, 12, 24]:

        df[f"{col}_rolling_mean_{window}h"] = (
            df[col].rolling(window).mean()
        )

        df[f"{col}_rolling_std_{window}h"] = (
            df[col].rolling(window).std()
        )

# --------------------------------------------------
# 5. Rolling weather statistics
# --------------------------------------------------

weather_features = [
    "temperature_2m",
    "relative_humidity_2m",
    "wind_speed_10m",
    "pressure_msl"
]

for col in weather_features:

    for window in [3, 6, 12, 24]:

        df[f"{col}_rolling_mean_{window}h"] = (
            df[col].rolling(window).mean()
        )

# --------------------------------------------------
# 6. Wind components
# --------------------------------------------------

wind_radians = np.deg2rad(df["wind_direction_10m"])

df["wind_u"] = (
    -df["wind_speed_10m"] * np.sin(wind_radians)
)

df["wind_v"] = (
    -df["wind_speed_10m"] * np.cos(wind_radians)
)

# --------------------------------------------------
# 7. Future PM2.5 targets
# --------------------------------------------------

df["target_PM25_24h"] = (
    df["PM2.5 (µg/m³)"].shift(-24)
)

df["target_PM25_48h"] = (
    df["PM2.5 (µg/m³)"].shift(-48)
)

df["target_PM25_72h"] = (
    df["PM2.5 (µg/m³)"].shift(-72)
)

# --------------------------------------------------
# 8. Remove rows without future targets
# --------------------------------------------------

df = df.dropna(
    subset=[
        "target_PM25_24h",
        "target_PM25_48h",
        "target_PM25_72h"
    ]
)

# --------------------------------------------------
# 9. Save
# --------------------------------------------------

df.to_csv(OUTPUT, index=False)

print("Output:", OUTPUT)
print("Rows:", len(df))
print("Columns:", len(df.columns))

print("\nTotal missing values:", df.isna().sum().sum())

print("\n========== COMPLETED ==========\n")