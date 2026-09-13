import pandas as pd

FILE = "data/cleaned/hourly_dataset.csv"

df = pd.read_csv(FILE)

df["Timestamp"] = pd.to_datetime(df["Timestamp"], utc=True)

print("\n========== EXTREME VALUE CHECK ==========\n")

# --------------------------------------------------
# PM2.5
# --------------------------------------------------

print("TOP 20 PM2.5 VALUES\n")

print(
    df[
        [
            "Timestamp",
            "PM2.5 (µg/m³)",
            "PM10 (µg/m³)",
            "NO2 (µg/m³)",
            "SO2 (µg/m³)",
            "Ozone (µg/m³)",
            "temperature_2m",
            "relative_humidity_2m",
            "wind_speed_10m"
        ]
    ]
    .sort_values("PM2.5 (µg/m³)", ascending=False)
    .head(20)
    .to_string(index=False)
)

# --------------------------------------------------
# PM10
# --------------------------------------------------

print("\n\nTOP 20 PM10 VALUES\n")

print(
    df[
        [
            "Timestamp",
            "PM10 (µg/m³)",
            "PM2.5 (µg/m³)",
            "NO2 (µg/m³)",
            "SO2 (µg/m³)",
            "Ozone (µg/m³)",
            "temperature_2m",
            "relative_humidity_2m",
            "wind_speed_10m"
        ]
    ]
    .sort_values("PM10 (µg/m³)", ascending=False)
    .head(20)
    .to_string(index=False)
)

# --------------------------------------------------
# Count extreme values
# --------------------------------------------------

print("\n\n========== EXTREME COUNTS ==========\n")

for col in [
    "PM2.5 (µg/m³)",
    "PM10 (µg/m³)",
    "NO2 (µg/m³)",
    "SO2 (µg/m³)",
    "Ozone (µg/m³)"
]:

    print(f"\n{col}")

    for threshold in [200, 300, 400, 500, 800]:
        count = (df[col] > threshold).sum()
        print(f"  > {threshold}: {count}")

print("\n========== CHECK COMPLETED ==========\n")