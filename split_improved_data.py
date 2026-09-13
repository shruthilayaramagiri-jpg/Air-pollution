import pandas as pd
from pathlib import Path

INPUT = "data/cleaned/improved_features_24h_clean.csv"
OUTPUT_DIR = Path("data/cleaned/improved")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("Loading dataset...")

df = pd.read_csv(INPUT)

df["Timestamp"] = pd.to_datetime(df["Timestamp"], utc=True)

df = df.sort_values("Timestamp").reset_index(drop=True)

print("Total rows:", len(df))
print("Start:", df["Timestamp"].min())
print("End:", df["Timestamp"].max())

# ---------------------------------------------------------
# Chronological split
# ---------------------------------------------------------

train = df[
    df["Timestamp"].dt.year == 2024
].copy()

validation = df[
    (df["Timestamp"] >= "2025-01-01") &
    (df["Timestamp"] < "2025-07-01")
].copy()

test = df[
    df["Timestamp"] >= "2025-07-01"
].copy()

# ---------------------------------------------------------
# Save
# ---------------------------------------------------------

train.to_csv(OUTPUT_DIR / "train.csv", index=False)
validation.to_csv(OUTPUT_DIR / "validation.csv", index=False)
test.to_csv(OUTPUT_DIR / "test.csv", index=False)

# ---------------------------------------------------------
# Report
# ---------------------------------------------------------

print("\n========== IMPROVED DATA SPLIT ==========")

print(
    f"Train      : {len(train):5d} rows | "
    f"{train['Timestamp'].min()} → {train['Timestamp'].max()}"
)

print(
    f"Validation : {len(validation):5d} rows | "
    f"{validation['Timestamp'].min()} → {validation['Timestamp'].max()}"
)

print(
    f"Test       : {len(test):5d} rows | "
    f"{test['Timestamp'].min()} → {test['Timestamp'].max()}"
)

print("\nFiles saved:")
print(OUTPUT_DIR / "train.csv")
print(OUTPUT_DIR / "validation.csv")
print(OUTPUT_DIR / "test.csv")

print("\n========== COMPLETED ==========")