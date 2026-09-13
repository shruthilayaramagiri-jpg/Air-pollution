import pandas as pd
import numpy as np

print("\n========== PERSISTENCE BASELINE ==========\n")

files = {
    "Validation": "data/cleaned/validation.csv",
    "Test": "data/cleaned/test.csv"
}

for name, file in files.items():

    df = pd.read_csv(file)

    # Last observed PM2.5 = PM2.5 at lag 1
    actual_24 = df["target_PM25_24h"]
    actual_48 = df["target_PM25_48h"]
    actual_72 = df["target_PM25_72h"]

    predicted = df["PM2.5_lag1"]

    print(f"\n{name}")
    print("-" * 40)

    for horizon, actual in [
        ("24h", actual_24),
        ("48h", actual_48),
        ("72h", actual_72)
    ]:

        mae = np.mean(np.abs(actual - predicted))
        rmse = np.sqrt(np.mean((actual - predicted) ** 2))

        print(f"{horizon}: MAE = {mae:.2f}, RMSE = {rmse:.2f}")

print("\n========== COMPLETED ==========\n")