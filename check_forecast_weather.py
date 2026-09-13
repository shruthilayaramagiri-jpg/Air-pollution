import pandas as pd

FILE = "data/raw_data/weather_forecast_historical_2024_2025.csv"

df = pd.read_csv(FILE)

df["time"] = pd.to_datetime(df["time"], utc=True)

print("\n========== FORECAST WEATHER CHECK ==========\n")

print("Rows:", len(df))
print("Columns:", len(df.columns))

print("\nDate range:")
print("Start:", df["time"].min())
print("End:  ", df["time"].max())

print("\nDuplicate timestamps:")
print(df["time"].duplicated().sum())

print("\nTime differences:")
print(df["time"].sort_values().diff().value_counts().head(10))

print("\nMissing values:")
print(df.isna().sum())

print("\nBasic statistics:")
print(df.describe().round(2).to_string())

print("\n========== CHECK COMPLETED ==========\n")