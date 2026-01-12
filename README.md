Project overview
This project presents a statistical fraud detection analysis on a synthetic financial transactions dataset of 500 customers. The goal is to understand fraud patterns and build a Random Forest model to predict fraudulent transactions and support risk‑based fraud mitigation.
​

Dataset description
File: Fraud_Analysis.xlsx.
​

Observations: 500 transaction records.
​

Core variables (24 features):

Numerical: age, familyincome, creditscore, transactionamount, loanamount, personalincome, accountagedays, numprevtransactions, avgtransactionvalue, internetusagehrs, mobileusagehrs, fraudamount.
​

Categorical: gender, education, maritalstatus, region, transactiontype, devicetype, hasloan, ownshome.
​

Targets:

Primary: isfraud (0 = non‑fraud, 1 = fraud).
​

Secondary: fraudamount.
​

Quality: No missing values in any of the 24 core variables.
​

Class balance: 246 fraud cases (49.2%) and 254 non‑fraud cases (50.8%).
​

Objectives
Perform descriptive and inferential analysis of fraud vs non‑fraud behaviour.
​

Detect statistical outliers related to potential fraud using IQR and Z‑score methods.
​

Analyse correlations and categorical patterns associated with fraud risk.
​

Build and evaluate a Random Forest classifier for fraud prediction.
​

Derive practical recommendations for fraud prevention and monitoring.
​

Methods and analysis
1. Descriptive statistics
Computed count, mean, median, standard deviation, min and max for all numerical variables in Excel.
​

Example:

age: mean 50.11, range 18–90.
​

transactionamount: mean 2004.38, median 1357.21, range 10–15050.41.
​

fraudamount: mean 712.47, median 0, max 10218.89.
​

2. Outlier detection
IQR method applied to numerical variables to flag extreme values.
​

transactionamount: 25 outliers.
​

loanamount: 22 outliers.
​

avgtransactionvalue: 8 outliers.
​

fraudamount: 54 outliers (highest), indicating many extreme fraud events.
​

Outlier cases show a higher fraud rate than the overall dataset, supporting their use as risk indicators.
​

3. Standardization and correlation
Z‑score standardization applied to: transactionamount, loanamount, personalincome, familyincome.
​

transactionamount Z‑scores range roughly from −0.95 to 6.23, indicating extreme high‑value outliers.
​

Correlation analysis with isfraud:
​

fraudamount: r ≈ 0.54 (moderate positive).
​

creditscore: r ≈ −0.23 (lower scores → higher fraud risk).
​

personalincome: r ≈ −0.21 (lower incomes more associated with fraud).
​

Most other variables show weak correlations |r| < 0.3, indicating multi‑factor fraud patterns. 
​

4. Fraud patterns (categorical)
Key distributions by group:
​

Demographics:

Higher fraud share among women (≈55.2%) vs men (≈42.7%).
​

Regional fraud rates highest in West (≈54.8%) and East (≈50.4%).
​

Channel and device:

In‑store transactions have highest fraud rate (~54.2%), followed by ATM (~51.2%).
​

Desktop has highest device‑based fraud risk (~54.8%), higher than mobile and POS.
​

Online channel shows lower fraud risk (~42.6%), contrary to common expectations.
​

Amount and behaviour:

Loan amount distributions are very similar between fraud and non‑fraud; loan size alone is not discriminative.
​

Transaction amounts also look similar across classes, suggesting amount magnitude is a weak standalone predictor.
​

Many fraud events are small (fraudamount < 1000), consistent with micro‑fraud or probe transactions.
​

5. Predictive modelling – Random Forest
Tooling: Python (pandas, scikit‑learn, numpy).
​

Model: Random Forest Classifier trained on customer and transaction features.
​

Train/test split: 75/25 (375 train, 125 test).
​

Performance on test set:
​

Accuracy: 67.2%.

Class 0 (Non‑fraud): precision 0.69, recall 0.64, F1 = 0.67 (support 64).

Class 1 (Fraud): precision 0.65, recall 0.70, F1 = 0.68 (support 61).

Confusion matrix:
​

True Non‑fraud (TN): 41

False Fraud (FP): 23

False Non‑fraud (FN): 18

True Fraud (TP): 43

Interpretation:

Model provides balanced precision and recall for both classes and relatively high recall (70%) for fraud, supporting use as a screening tool.
​

However, 18 missed frauds (false negatives) correspond to a non‑trivial undetected fraud amount and justify human review or stricter thresholds in high‑risk segments.
​

Key insights and recommendations
Main insights:
​

Fraud is frequent (≈49%) and not limited to extreme amounts.

Lower personal income and lower credit scores are associated with higher fraud risk.

Fraud risk is higher among female customers, West/East regions, in‑store and desktop transactions.

Amount variables (transactionamount, loanamount) alone do not separate fraud vs non‑fraud; behavioural and contextual features matter more.

Recommended actions:
​

Strengthen controls for higher‑risk groups: lower‑income, lower credit score, age ≥ 50, female customers in West/East regions.

Add stronger authentication and monitoring for in‑store and desktop transactions.

Do not ignore small suspicious transactions; many frauds are below 1,000.

Use a combined approach of statistical outlier flags (IQR, Z‑score) plus machine learning models and human investigation.

Deploy real‑time alerts for unusual activity and educate customers about fraud tactics.

How to run (suggested)
Adjust this section to match your actual code and folder names before pushing to GitHub.

Clone repository

bash
git clone https://github.com/<your-username>/fraud-detection-analysis.git
cd fraud-detection-analysis
Project structure (example)

text
.
├── data/
│   └── Fraud_Analysis.xlsx
├── notebooks/
│   └── fraud_analysis_eda.ipynb
├── src/
│   └── model_random_forest.py
├── reports/
│   └── BAA-1089-Assignment-3_Ananya-Mahadeva-1.pdf
├── README.md
└── requirements.txt
data/: Excel dataset with all variables.
​

reports/: Final PDF report.
​

notebooks/: EDA and visualizations.
​

src/: Model training and evaluation scripts.
​

Install dependencies

bash
pip install -r requirements.txt
Run EDA and modelling

Open the Jupyter notebook in notebooks/ to reproduce descriptive statistics, outlier detection, and plots.
​

Run src/model_random_forest.py to train and evaluate the Random Forest model.