# Fraud Detection Analysis – README

## Project overview
This project presents a **statistical** fraud detection analysis on a synthetic financial transactions dataset of 500 customers. The goal is to understand fraud patterns and build a Random Forest model to predict fraudulent transactions and support risk‑based fraud mitigation.

## Dataset description
- File: `Fraud_Analysis.xlsx`.
- Observations: 500 transaction records.
- Core variables (24 features):
  - Numerical: `age`, `familyincome`, `creditscore`, `transactionamount`, `loanamount`, `personalincome`, `accountagedays`, `numprevtransactions`, `avgtransactionvalue`, `internetusagehrs`, `mobileusagehrs`, `fraudamount`.
  - Categorical: `gender`, `education`, `maritalstatus`, `region`, `transactiontype`, `devicetype`, `hasloan`, `ownshome`.
  - Targets:
    - Primary: `isfraud` (0 = non‑fraud, 1 = fraud).
    - Secondary: `fraudamount`.
- Data quality: No missing values in the 24 core variables.
- Class balance: 246 fraud cases (49.2%) and 254 non‑fraud cases (50.8%).

## Objectives
- Perform descriptive and inferential analysis of fraud vs non‑fraud behaviour.
- Detect statistical outliers related to potential fraud using IQR and Z‑score methods.
- Analyse correlations and categorical patterns associated with fraud risk.
- Build and evaluate a Random Forest classifier for fraud prediction.
- Derive practical recommendations for fraud prevention and monitoring.

## Methods and analysis

### Descriptive statistics
- Computed count, mean, median, standard deviation, min and max for all numerical variables in Excel.
- Example key figures:
  - `age`: mean ≈ 50.11 years, range 18–90.
  - `transactionamount`: mean ≈ 2004.38, median ≈ 1357.21, range 10–15050.41.
  - `fraudamount`: mean ≈ 712.47, median 0, max ≈ 10218.89.

### Outlier detection
- IQR method applied to numerical variables to flag extreme values.
- Approximate outlier counts:
  - `transactionamount`: 25 outliers.
  - `loanamount`: 22 outliers.
  - `avgtransactionvalue`: 8 outliers.
  - `fraudamount`: 54 outliers (most), indicating many extreme fraud events.
- Outlier cases show a higher fraud rate than the overall dataset, supporting their use as risk indicators.

### Standardization and correlation
- Z‑score standardization applied to: `transactionamount`, `loanamount`, `personalincome`, `familyincome`.
- Example Z‑score range:
  - `transactionamount` Z‑scores from about −0.95 to 6.23, indicating extreme high‑value outliers.
- Correlations with `isfraud`:
  - `fraudamount`: r ≈ 0.54 (moderate positive).
  - `creditscore`: r ≈ −0.23 (lower scores linked to higher fraud risk).
  - `personalincome`: r ≈ −0.21 (lower income more associated with fraud).
  - Most other variables show weak correlations (|r| < 0.3), implying multi‑factor fraud patterns.

### Fraud patterns (categorical)
Key patterns by group:

- Demographics:
  - Higher fraud share among women (~55.2%) compared with men (~42.7%).
  - Regional fraud rates highest in West (~54.8%) and East (~50.4%).

- Channel and device:
  - In‑store transactions have the highest fraud rate (~54.2%), followed by ATM (~51.2%).
  - Desktop has the highest device‑based fraud risk (~54.8%), higher than mobile and POS.
  - Online channel shows lower fraud risk (~42.6%) than physical channels.

- Amount and behaviour:
  - Loan amount distributions are very similar between fraud and non‑fraud; loan size alone is not discriminative.
  - Transaction amounts also look similar across classes, suggesting amount magnitude is a weak standalone predictor.
  - Many fraud events are small (`fraudamount` < 1000), consistent with micro‑fraud or test transactions.

## Predictive modelling

### Random Forest model
- Tooling: Python (pandas, scikit‑learn, numpy).
- Model: Random Forest Classifier.
- Features: demographic, financial and transaction variables (numeric and one‑hot‑encoded categorical).
- Target: `isfraud` (binary).

#### Train/test setup
- Train/test split: 75% training, 25% testing.
- Stratified split to preserve fraud vs non‑fraud proportions.

#### Performance (test set)
- Accuracy: 67.2%.
- Precision/recall/F1 (approximate):
  - Class 0 (Non‑fraud): precision ≈ 0.69, recall ≈ 0.64, F1 ≈ 0.67.
  - Class 1 (Fraud): precision ≈ 0.65, recall ≈ 0.70, F1 ≈ 0.68.
- Confusion matrix (Non‑fraud = 0, Fraud = 1):
  - True Negatives: 41
  - False Positives: 23
  - False Negatives: 18
  - True Positives: 43

Interpretation:
- The model achieves balanced performance, with recall of ~70% on fraud, meaning it captures most fraud cases but still produces some false positives and false negatives.
- Accuracy and F1 suggest suitability as a screening tool rather than a fully automated decision engine.

## Files in this project
- `Fraud_Analysis.xlsx` – main dataset and supporting sheets (descriptive statistics, correlation matrix, outlier flags, etc.).
- `BAA-1089-Assignment-3_Ananya-Mahadeva-1.pdf` – report describing methodology, analysis, and business recommendations.
- (Optional) `fraud_analysis.py` – Python script to replicate the Random Forest modelling and key statistics.

## How to run the analysis (Python)
1. Place `Fraud_Analysis.xlsx` and `fraud_analysis.py` in the same folder.
2. Create a virtual environment and install dependencies:
   ```bash
   pip install pandas scikit-learn numpy openpyxl
