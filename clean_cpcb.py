import pandas as pd
from pathlib import Path

input_file = Path("data/raw_data/d7.csv")
output_file = Path("data/cleaned/cpcb_clean.csv")

# Load data
df = pd.read_csv(input_file)

print("Original rows:", len(df))

# Convert timestamp
df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce")

# Remove rows with invalid station/timestamp
df = df[
    df["Station ID"].notna() &
    df["Timestamp"].notna()
]

# Keep only the actual CPCB station
df = df[df["Station ID"] == "site_117"]

# Remove completely empty pollutant/weather columns
columns_to_remove = [
    "Toluene (µg/m³)",
    "Xylene (µg/m³)",
    "O Xylene (µg/m³)",
    "Eth-Benzene (µg/m³)",
    "MP-Xylene (µg/m³)",
    "AT (°C)",
    "RH (%)",
    "WS (m/s)",
    "WD (deg)",
    "RF (mm)",
    "TOT-RF (mm)",
    "SR (W/mt2)",
    "BP (mmHg)",
    "VWS (m/s)"
]

df = df.drop(columns=columns_to_remove, errors="ignore")

# Sort chronologically
df = df.sort_values("Timestamp")

# Remove exact duplicate timestamps
df = df.drop_duplicates(
    subset=["Station ID", "Timestamp"],
    keep="first"
)

# Create output folder
output_file.parent.mkdir(parents=True, exist_ok=True)

# Save
df.to_csv(output_file, index=False)

print("Clean rows:", len(df))
print("Columns:", len(df.columns))
print("Saved to:", output_file)

print("\nDate range:")
print(df["Timestamp"].min())
print(df["Timestamp"].max())

print("\nMissing values:")
print(df.isna().sum())