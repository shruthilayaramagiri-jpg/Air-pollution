import pandas as pd
from pathlib import Path

INPUT = Path("data/cleaned/training_windows_24h_clean.csv")
OUTPUT_DIR = Path("data/cleaned")

print("\n========== TIME-BASED DATA SPLIT ==========\n")

df = pd.read_csv(INPUT)

df["Timestamp"] = pd.to_datetime(df["Timestamp"], utc=True)

# Sort chronologically
df = df.sort_values("Timestamp").reset_index(drop=True)

# Define periods
train = df[df["Timestamp"] < "2025-01-01"].copy()

validation = df[
    (df["Timestamp"] >= "2025-01-01") &
    (df["Timestamp"] < "2025-07-01")
].copy()

test = df[df["Timestamp"] >= "2025-07-01"].copy()

# Save
train.to_csv(OUTPUT_DIR / "train.csv", index=False)
validation.to_csv(OUTPUT_DIR / "validation.csv", index=False)
test.to_csv(OUTPUT_DIR / "test.csv", index=False)

print("TRAINING SET")
print(f"Rows: {len(train):,}")
print(f"Start: {train['Timestamp'].min()}")
print(f"End: {train['Timestamp'].max()}")

print("\nVALIDATION SET")
print(f"Rows: {len(validation):,}")
print(f"Start: {validation['Timestamp'].min()}")
print(f"End: {validation['Timestamp'].max()}")

print("\nTEST SET")
print(f"Rows: {len(test):,}")
print(f"Start: {test['Timestamp'].min()}")
print(f"End: {test['Timestamp'].max()}")

print("\nTotal:")
print(f"{len(train) + len(validation) + len(test):,}")

print("\nFiles created:")
print("data/cleaned/train.csv")
print("data/cleaned/validation.csv")
print("data/cleaned/test.csv")

print("\n========== COMPLETED ==========\n")