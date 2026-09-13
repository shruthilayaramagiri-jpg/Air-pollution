import pandas as pd
from pathlib import Path

folders = [
    Path("data/raw_data"),
    Path("data/extracted")
]

files = []

for folder in folders:
    if folder.exists():
        files.extend(folder.glob("*.csv"))
        files.extend(folder.glob("*.xlsx"))

print("\n========== DATASET REPORT ==========\n")

for file in files:

    print("=" * 70)
    print("FILE:", file)

    try:
        if file.suffix.lower() == ".csv":
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)

        print("Rows:", len(df))
        print("Columns:", len(df.columns))

        print("\nCOLUMN NAMES:")
        for column in df.columns:
            print(" -", column)

        print("\nMISSING VALUES:")
        print(df.isnull().sum())

        print("\nDUPLICATE ROWS:", df.duplicated().sum())

        print("\nFIRST 3 ROWS:")
        print(df.head(3).to_string())

        print()

    except Exception as e:
        print("ERROR:", e)

print("=" * 70)
print("Inspection completed.")