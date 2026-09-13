import pandas as pd

file = "data/raw_data/weather_historical_2024_2025.csv"

df = pd.read_csv(file)

print("\n========== WEATHER DATA QUALITY ==========\n")

print("Rows:", len(df))
print("Columns:", len(df.columns))

print("\nCOLUMN NAMES:")
for col in df.columns:
    print("-", col)

print("\nMISSING VALUES:")
print(df.isna().sum())

print("\nMISSING PERCENTAGE:")
print((df.isna().mean() * 100).round(2))

print("\nDATE RANGE:")
print("Start:", df["time"].min())
print("End  :", df["time"].max())

print("\nDUPLICATE TIMES:", df["time"].duplicated().sum())

print("\nSAMPLE DATA:")
print(df.head(10).to_string(index=False))

print("\n========== CHECK COMPLETED ==========\n")