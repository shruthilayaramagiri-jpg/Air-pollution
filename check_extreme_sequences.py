import pandas as pd

FILE = "data/cleaned/hourly_dataset.csv"

df = pd.read_csv(FILE)

df["Timestamp"] = pd.to_datetime(df["Timestamp"], utc=True)
df = df.sort_values("Timestamp").reset_index(drop=True)

pm25 = "PM2.5 (µg/m³)"
pm10 = "PM10 (µg/m³)"

print("\n========== EXTREME SEQUENCE CHECK ==========\n")

# --------------------------------------------------
# Identify high PM2.5 periods
# --------------------------------------------------

df["high_pm25"] = df[pm25] > 400

groups = (
    df["high_pm25"] != df["high_pm25"].shift()
).cumsum()

sequences = (
    df[df["high_pm25"]]
    .groupby(groups)
    .agg(
        start=("Timestamp", "min"),
        end=("Timestamp", "max"),
        hours=(pm25, "count"),
        max_pm25=(pm25, "max"),
        max_pm10=(pm10, "max")
    )
    .sort_values("max_pm25", ascending=False)
)

print("PM2.5 > 400 µg/m³ sequences:\n")

print(sequences.head(20).to_string())

# --------------------------------------------------
# High PM10 periods
# --------------------------------------------------

df["high_pm10"] = df[pm10] > 500

groups2 = (
    df["high_pm10"] != df["high_pm10"].shift()
).cumsum()

sequences_pm10 = (
    df[df["high_pm10"]]
    .groupby(groups2)
    .agg(
        start=("Timestamp", "min"),
        end=("Timestamp", "max"),
        hours=(pm10, "count"),
        max_pm10=(pm10, "max"),
        max_pm25=(pm25, "max")
    )
    .sort_values("max_pm10", ascending=False)
)

print("\n\nPM10 > 500 µg/m³ sequences:\n")

print(sequences_pm10.head(20).to_string())

# --------------------------------------------------
# Consecutive extreme values
# --------------------------------------------------

print("\n\n========== SUMMARY ==========\n")

print(
    "Number of PM2.5 > 400 sequences:",
    len(sequences)
)

print(
    "Number of PM10 > 500 sequences:",
    len(sequences_pm10)
)

print(
    "PM2.5 > 400 total hours:",
    df["high_pm25"].sum()
)

print(
    "PM10 > 500 total hours:",
    df["high_pm10"].sum()
)

print("\n========== CHECK COMPLETED ==========\n")