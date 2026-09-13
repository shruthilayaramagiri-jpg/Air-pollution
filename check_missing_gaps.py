import pandas as pd

FILE = "data/cleaned/hourly_dataset.csv"

df = pd.read_csv(FILE)

df["Timestamp"] = pd.to_datetime(df["Timestamp"], utc=True)
df = df.sort_values("Timestamp").reset_index(drop=True)

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

print("\n========== MISSING DATA GAP ANALYSIS ==========\n")

for col in pollutants:

    print(f"\n========== {col} ==========\n")

    missing = df[col].isna()

    # Identify consecutive missing groups
    groups = (missing != missing.shift()).cumsum()

    gaps = (
        df[missing]
        .groupby(groups)
        .agg(
            start=("Timestamp", "min"),
            end=("Timestamp", "max"),
            missing_hours=("Timestamp", "count")
        )
        .sort_values("missing_hours", ascending=False)
    )

    print("Total missing:", missing.sum())

    print("\nLargest missing gaps:")

    print(
        gaps.head(10).to_string(index=False)
    )

print("\n========== CHECK COMPLETED ==========\n")