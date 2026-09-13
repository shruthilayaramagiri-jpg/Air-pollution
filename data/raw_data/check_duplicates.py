import pandas as pd
from pathlib import Path

folder = Path("data/raw_data")

files = list(folder.glob("*.csv"))

data = {}

for file in files:
    try:
        df = pd.read_csv(file)
        data[file.name] = df
        print(file.name, "loaded:", df.shape)
    except Exception as e:
        print(file.name, "ERROR:", e)

print("\n========== DUPLICATE DATASET CHECK ==========\n")

names = list(data.keys())

for i in range(len(names)):
    for j in range(i + 1, len(names)):

        file1 = names[i]
        file2 = names[j]

        df1 = data[file1]
        df2 = data[file2]

        if df1.shape == df2.shape:

            same = df1.equals(df2)

            if same:
                print("DUPLICATE:")
                print(file1, "=", file2)