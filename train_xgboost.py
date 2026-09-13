import pandas as pd
import numpy as np
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

print("\n========== XGBOOST PM2.5 FORECAST MODEL ==========\n")

train = pd.read_csv("data/cleaned/train.csv")
validation = pd.read_csv("data/cleaned/validation.csv")
test = pd.read_csv("data/cleaned/test.csv")

target_columns = [
    "target_PM25_24h",
    "target_PM25_48h",
    "target_PM25_72h"
]

# Remove target columns and timestamp
feature_columns = [
    col for col in train.columns
    if col not in target_columns and col != "Timestamp"
]

X_train = train[feature_columns]
X_val = validation[feature_columns]
X_test = test[feature_columns]

print("Training samples:", len(X_train))
print("Validation samples:", len(X_val))
print("Test samples:", len(X_test))
print("Number of features:", len(feature_columns))

for target in target_columns:

    print("\n========================================")
    print("Training:", target)
    print("========================================")

    y_train = train[target]
    y_val = validation[target]
    y_test = test[target]

    model = XGBRegressor(
        n_estimators=500,
        max_depth=6,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        objective="reg:squarederror",
        random_state=42,
        n_jobs=-1
    )

    model.fit(
        X_train,
        y_train,
        eval_set=[(X_val, y_val)],
        verbose=False
    )

    val_pred = model.predict(X_val)
    test_pred = model.predict(X_test)

    val_mae = mean_absolute_error(y_val, val_pred)
    val_rmse = np.sqrt(mean_squared_error(y_val, val_pred))
    val_r2 = r2_score(y_val, val_pred)

    test_mae = mean_absolute_error(y_test, test_pred)
    test_rmse = np.sqrt(mean_squared_error(y_test, test_pred))
    test_r2 = r2_score(y_test, test_pred)

    print("\nValidation:")
    print(f"MAE  = {val_mae:.2f}")
    print(f"RMSE = {val_rmse:.2f}")
    print(f"R²   = {val_r2:.3f}")

    print("\nTest:")
    print(f"MAE  = {test_mae:.2f}")
    print(f"RMSE = {test_rmse:.2f}")
    print(f"R²   = {test_r2:.3f}")

print("\n========== COMPLETED ==========\n")