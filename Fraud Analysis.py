# fraud_analysis.py

import pandas as pd
import numpy as np
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

# -----------------------------
# 1. Load data
# -----------------------------
DATA_PATH = Path("Fraud_Analysis.xlsx")

# Main sheet with raw data
df = pd.read_excel(DATA_PATH, sheet_name="Masterdata")

# -----------------------------
# 2. Basic cleaning / selection
# -----------------------------
# Keep relevant columns (names taken from the Excel structure)
num_cols = [
    "age", "familyincome", "creditscore", "transactionamount",
    "loanamount", "personalincome", "accountagedays",
    "numprevtransactions", "avgtransactionvalue",
    "internetusagehrs", "mobileusagehrs", "fraudamount"
]

cat_cols = [
    "gender", "education", "maritalstatus", "region",
    "transactiontype", "devicetype", "hasloan", "ownshome"
]

target_col = "isfraud"

# Drop rows with missing target or critical fields (if any)
df = df.dropna(subset=[target_col])

# -----------------------------
# 3. Descriptive statistics
# -----------------------------
desc_stats = df[num_cols].describe().T
print("\n=== Descriptive statistics (numerical) ===")
print(desc_stats)

# -----------------------------
# 4. Outlier detection (IQR)
# -----------------------------
def iqr_outliers(series, k=1.5):
    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    iqr = q3 - q1
    lower = q1 - k * iqr
    upper = q3 + k * iqr
    mask = (series < lower) | (series > upper)
    return mask, lower, upper

outlier_summary = {}

for col in ["transactionamount", "loanamount", "avgtransactionvalue", "fraudamount"]:
    mask, lower, upper = iqr_outliers(df[col])
    outlier_count = mask.sum()
    outlier_summary[col] = {
        "outliers": int(outlier_count),
        "lower_bound": float(lower),
        "upper_bound": float(upper)
    }

print("\n=== IQR outlier summary ===")
for k, v in outlier_summary.items():
    print(f"{k}: {v['outliers']} outliers, bounds=({v['lower_bound']:.2f}, {v['upper_bound']:.2f})")

# Optional: flag outliers in the dataframe
for col in outlier_summary.keys():
    mask, _, _ = iqr_outliers(df[col])
    df[f"{col}_outlier"] = mask.astype(int)

# -----------------------------
# 5. Standardization (Z-score) for key amounts
# -----------------------------
std_cols = ["transactionamount", "loanamount", "personalincome", "familyincome"]

scaler = StandardScaler()
df[[f"z_{c}" for c in std_cols]] = scaler.fit_transform(df[std_cols])

print("\n=== Z-score ranges ===")
for c in std_cols:
    zc = df[f"z_{c}"]
    print(f"{c}: min={zc.min():.2f}, max={zc.max():.2f}")

# -----------------------------
# 6. Correlation with fraud
# -----------------------------
corr_matrix = df[num_cols + [target_col]].corr()
print("\n=== Correlation with isfraud ===")
print(corr_matrix[target_col].sort_values(ascending=False))

# -----------------------------
# 7. Encode categorical variables
# -----------------------------
df_model = df[num_cols + cat_cols + [target_col]].copy()

# Binary flags already numeric: hasloan, ownshome
# Convert to int explicitly
df_model["hasloan"] = df_model["hasloan"].astype(int)
df_model["ownshome"] = df_model["ownshome"].astype(int)

# One-hot encode remaining categoricals
df_model = pd.get_dummies(
    df_model,
    columns=["gender", "education", "maritalstatus", "region",
             "transactiontype", "devicetype"],
    drop_first=True
)

X = df_model.drop(columns=[target_col])
y = df_model[target_col].astype(int)

# -----------------------------
# 8. Train / test split
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.25,
    random_state=42,
    stratify=y
)

# -----------------------------
# 9. Random Forest model
# -----------------------------
rf = RandomForestClassifier(
    n_estimators=200,
    max_depth=None,
    random_state=42,
    class_weight=None  # dataset is roughly balanced
)

rf.fit(X_train, y_train)

# -----------------------------
# 10. Evaluation
# -----------------------------
y_pred = rf.predict(X_test)

acc = accuracy_score(y_test, y_pred)
cm = confusion_matrix(y_test, y_pred)
report = classification_report(y_test, y_pred, digits=2)

print("\n=== Random Forest performance ===")
print(f"Accuracy: {acc * 100:.1f}%")
print("\nConfusion matrix (rows=true, cols=pred):")
print(cm)
print("\nClassification report:")
print(report)

# -----------------------------
# 11. Feature importance
# -----------------------------
feat_imp = pd.Series(rf.feature_importances_, index=X.columns).sort_values(ascending=False)
print("\n=== Top 15 feature importances ===")
print(feat_imp.head(15))
