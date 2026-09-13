import pandas as pd

file = "data/cleaned/cpcb_weather_2024_2025.csv"

df = pd.read_csv(file)

print("\n========== POLLUTION QUALITY CHECK ==========\n")

# Convert timestamp
df["Timestamp"] = pd.to_datetime(df["Timestamp"], utc=True)

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

print("Rows:", len(df))

print("\n========== MISSING VALUES ==========\n")
print(df[pollutants].isna().sum())

print("\n========== NEGATIVE VALUES ==========\n")

for col in pollutants:
    negative = (df[col] < 0).sum()
    print(f"{col}: {negative}")

print("\n========== STATISTICS ==========\n")

print(
    df[pollutants]
    .describe()
    .T[
        ["count", "mean", "std", "min", "25%", "50%", "75%", "max"]
    ]
    .to_string()
)

print("\n========== TIMESTAMP GAPS ==========\n")

df = df.sort_values("Timestamp")

df["time_diff"] = df["Timestamp"].diff()

print(df["time_diff"].value_counts().head(15))

print("\n========== CHECK COMPLETED ==========\n")