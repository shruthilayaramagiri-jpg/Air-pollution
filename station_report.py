import pandas as pd

file = "data/raw_data/d7.csv"

df = pd.read_csv(file)

# Convert timestamp
df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce")

print("\n========== STATION REPORT ==========\n")

# Station information
print("NUMBER OF UNIQUE STATIONS:")
print(df["Station ID"].nunique())

print("\nSTATIONS:")
stations = df.groupby(["Station ID", "State", "City", "Station Name"]).agg(
    records=("Timestamp", "count"),
    start_date=("Timestamp", "min"),
    end_date=("Timestamp", "max")
).reset_index()

print(stations.to_string(index=False))

print("\n========== OVERALL DATE RANGE ==========\n")

print("First timestamp:", df["Timestamp"].min())
print("Last timestamp :", df["Timestamp"].max())

print("\n========== RECORDS PER STATION ==========\n")

print(
    df.groupby("Station ID")
      .size()
      .sort_values(ascending=False)
      .to_string()
)

print("\n========== TIME DIFFERENCE CHECK ==========\n")

df = df.sort_values(["Station ID", "Timestamp"])

df["time_diff"] = (
    df.groupby("Station ID")["Timestamp"]
      .diff()
)

print(df["time_diff"].value_counts().head(15))

print("\n========== REPORT COMPLETED ==========\n")