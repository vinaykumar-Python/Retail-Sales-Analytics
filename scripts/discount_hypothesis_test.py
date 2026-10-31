"""
Retail Sales Analytics
Statistical Analysis: Discounts and Profitability

Business question:
Are discounts above 30% associated with lower profit?

Note:
This analysis identifies associations, not proof of causation.
The initial comparison uses individual sales records, which may
not be statistically independent when multiple rows belong to
the same order.
"""

from pathlib import Path

import pandas as pd
from scipy import stats


# --------------------------------------------------
# 1. Define file paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_FILE = PROJECT_ROOT / "data" / "processed" / "superstore_cleaned.csv"
REPORT_DIR = PROJECT_ROOT / "reports" / "statistical_analysis"

REPORT_DIR.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# 2. Load and validate the dataset
# --------------------------------------------------

print("=" * 65)
print("DISCOUNT AND PROFITABILITY: STATISTICAL ANALYSIS")
print("=" * 65)

if not DATA_FILE.exists():
    raise FileNotFoundError(
        f"Dataset not found: {DATA_FILE}\n"
        "Please confirm that the cleaned CSV exists."
    )

df = pd.read_csv(DATA_FILE)

required_columns = ["Order ID", "Discount", "Profit"]

missing_columns = [
    column for column in required_columns
    if column not in df.columns
]

if missing_columns:
    raise ValueError(
        f"Missing required columns: {missing_columns}\n"
        f"Available columns: {df.columns.tolist()}"
    )

df["Discount"] = pd.to_numeric(df["Discount"], errors="coerce")
df["Profit"] = pd.to_numeric(df["Profit"], errors="coerce")

df = df.dropna(subset=["Discount", "Profit"]).copy()

if df.empty:
    raise ValueError("No valid Discount and Profit records were found.")


# --------------------------------------------------
# 3. Create comparison groups
# --------------------------------------------------

# Group A: Discount <= 30%
# Group B: Discount > 30%

df["Discount_Group"] = df["Discount"].apply(
    lambda discount: "Above 30%" if discount > 0.30 else "30% or Less"
)

group_a = df.loc[
    df["Discount_Group"] == "30% or Less", "Profit"
]

group_b = df.loc[
    df["Discount_Group"] == "Above 30%", "Profit"
]


# --------------------------------------------------
# 4. Calculate descriptive statistics
# --------------------------------------------------

def describe_group(name, values):
    return {
        "Discount_Group": name,
        "Record_Count": int(values.count()),
        "Mean_Profit": values.mean(),
        "Median_Profit": values.median(),
        "Total_Profit": values.sum(),
        "Standard_Deviation": values.std(ddof=1),
    }


summary = pd.DataFrame([
    describe_group("30% or Less", group_a),
    describe_group("Above 30%", group_b),
])

print("\n1. DESCRIPTIVE STATISTICS")
print("-" * 65)

print(
    summary.round(2).to_string(index=False)
)


# --------------------------------------------------
# 5. Check whether a statistical test is possible
# --------------------------------------------------

if len(group_a) < 2 or len(group_b) < 2:
    raise ValueError(
        "Each discount group needs at least two valid records "
        "for the statistical tests."
    )


# --------------------------------------------------
# 6. Welch's independent-samples t-test
# --------------------------------------------------

# Two-sided test:
# H0: The population mean profit is equal in both groups.
# H1: The population mean profit differs between groups.
#
# Welch's test does not require equal population variances.

welch_result = stats.ttest_ind(
    group_a,
    group_b,
    equal_var=False,
    alternative="two-sided"
)


# --------------------------------------------------
# 7. Mann-Whitney U test
# --------------------------------------------------

# A nonparametric comparison of the two groups.
# This tests distributional differences; it is not strictly
# a test of mean profit.

mann_whitney_result = stats.mannwhitneyu(
    group_a,
    group_b,
    alternative="two-sided"
)


# --------------------------------------------------
# 8. Report the test results
# --------------------------------------------------

mean_a = group_a.mean()
mean_b = group_b.mean()
mean_difference = mean_b - mean_a

print("\n2. PROFIT COMPARISON")
print("-" * 65)

print(f"Mean profit at 30% discount or less: {mean_a:.2f}")
print(f"Mean profit above 30% discount:     {mean_b:.2f}")
print(f"Difference (above - lower):         {mean_difference:.2f}")

print("\n3. WELCH'S T-TEST")
print("-" * 65)

print(f"t-statistic: {welch_result.statistic:.4f}")
print(f"p-value:     {welch_result.pvalue:.8f}")

alpha = 0.05

if welch_result.pvalue < alpha:
    print(
        "Result: The difference in mean profit is statistically "
        "significant at the 5% level."
    )
else:
    print(
        "Result: The difference in mean profit is not statistically "
        "significant at the 5% level."
    )

print("\n4. MANN-WHITNEY U TEST")
print("-" * 65)

print(f"U-statistic: {mann_whitney_result.statistic:.2f}")
print(f"p-value:     {mann_whitney_result.pvalue:.8f}")

if mann_whitney_result.pvalue < alpha:
    print(
        "Result: The two groups show a statistically significant "
        "distributional difference at the 5% level."
    )
else:
    print(
        "Result: No statistically significant distributional "
        "difference was detected at the 5% level."
    )


# --------------------------------------------------
# 9. Save outputs
# --------------------------------------------------

summary_file = REPORT_DIR / "discount_group_summary.csv"
results_file = REPORT_DIR / "discount_test_results.txt"

summary.to_csv(summary_file, index=False)

with open(results_file, "w", encoding="utf-8") as file:
    file.write("DISCOUNT AND PROFITABILITY STATISTICAL ANALYSIS\n")
    file.write("=" * 60 + "\n\n")

    file.write("Descriptive statistics:\n")
    file.write(summary.round(4).to_string(index=False))
    file.write("\n\n")

    file.write(f"Mean profit difference (above - lower): {mean_difference:.6f}\n")
    file.write(f"Welch t-statistic: {welch_result.statistic:.6f}\n")
    file.write(f"Welch p-value: {welch_result.pvalue:.10f}\n")
    file.write(f"Mann-Whitney U statistic: {mann_whitney_result.statistic:.6f}\n")
    file.write(f"Mann-Whitney p-value: {mann_whitney_result.pvalue:.10f}\n\n")

    file.write(
        "Interpretation caution: these tests compare individual sales "
        "records. Multiple records can belong to the same order, so the "
        "independence assumption may be violated. Results show association, "
        "not causation.\n"
    )

print("\n5. FILES SAVED")
print("-" * 65)
print(f"Summary CSV: {summary_file}")
print(f"Test results: {results_file}")

print("\nAnalysis completed successfully.")
