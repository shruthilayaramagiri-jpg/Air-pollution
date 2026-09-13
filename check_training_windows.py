import pandas as pd

FILE = "data/cleaned/hourly_dataset.csv"

df = pd.read_csv(FILE)

df["Timestamp"] = pd.to_datetime(df["Timestamp"], utc=True)

df = df.sort_values("Timestamp").reset_index(drop=True)

pm25 = "PM2.5 (µg/m³)"

print("\n========== TRAINING WINDOW CHECK ==========\n")

# Number of consecutive hourly PM2.5 observations required
# We need 72 hours of history + future targets.
history = 24

# Check different history lengths
for history in [6, 12, 24, 48, 72]:

    usable = 0
    total = 0

    for i in range(history, len(df) - 72):

        total += 1

        # Historical input window
        past = df.loc[i-history:i-1, pm25]

        # Future targets
        future = df.loc[
            i:i+71,
            pm25
        ]

        if past.notna().all() and future.notna().all():
            usable += 1

    percentage = (usable / total) * 100

    print(
        f"History = {history:2d}h | "
        f"Usable windows = {usable:,} / {total:,} "
        f"({percentage:.2f}%)"
    )

print("\n========== PM2.5 COMPLETE PERIODS ==========\n")

# Find continuous periods without missing PM2.5
missing = df[pm25].isna()

groups = (missing != missing.shift()).cumsum()

periods = (
    df[~missing]
    .groupby(groups)
    .agg(
        start=("Timestamp", "min"),
        end=("Timestamp", "max"),
        hours=(pm25, "count")
    )
    .sort_values("hours", ascending=False)
)

print(
    periods.head(20).to_string(index=False)
)

print("\n========== CHECK COMPLETED ==========\n")