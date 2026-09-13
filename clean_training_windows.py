import pandas as pd
from pathlib import Path

INPUT = Path("data/cleaned/training_windows_24h.csv")
OUTPUT = Path("data/cleaned/training_windows_24h_clean.csv")

print("\n========== CLEANING TRAINING WINDOWS ==========\n")

df = pd.read_csv(INPUT)

print(f"Original samples: {len(df):,}")

# Keep only samples with no missing values
clean = df.dropna().reset_index(drop=True)

print(f"Removed samples: {len(df) - len(clean):,}")
print(f"Remaining samples: {len(clean):,}")

print(f"\nRemaining missing values: {int(clean.isna().sum().sum())}")

clean.to_csv(OUTPUT, index=False)

print("\nSaved to:")
print(OUTPUT)

print("\n========== COMPLETED ==========\n")