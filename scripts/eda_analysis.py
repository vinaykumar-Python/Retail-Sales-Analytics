import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# --------------------------------------------------
# 1. PROJECT PATHS
# --------------------------------------------------

PROJECT_DIR = Path(__file__).resolve().parent.parent

DATA_FILE = (
    PROJECT_DIR
    / "data"
    / "processed"
    / "superstore_cleaned.csv"
)

OUTPUT_DIR = PROJECT_DIR / "reports" / "eda_charts"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------
# 2. LOAD DATA
# --------------------------------------------------

if not DATA_FILE.exists():
    raise FileNotFoundError(
        f"Cleaned dataset not found: {DATA_FILE}\n"
        "Run python scripts/clean_data.py first."
    )

df = pd.read_csv(DATA_FILE)

# Convert date columns back to datetime after reading CSV
for column in df.columns:
    if "date" in column.lower():
        df[column] = pd.to_datetime(df[column], errors="coerce")

print("\n========== DATASET OVERVIEW ==========")
print("Rows:", len(df))
print("Columns:", len(df.columns))
print("\nColumn names:")
print(df.columns.tolist())

# --------------------------------------------------
# 3. CHECK REQUIRED COLUMNS
# --------------------------------------------------

required_columns = ["Sales", "Profit", "Quantity", "Discount"]

missing_columns = [
    column for column in required_columns
    if column not in df.columns
]

if missing_columns:
    raise ValueError(
        f"Required columns missing from dataset: {missing_columns}"
    )

# --------------------------------------------------
# 4. KEY BUSINESS METRICS
# --------------------------------------------------

total_sales = df["Sales"].sum()
total_profit = df["Profit"].sum()
total_quantity = df["Quantity"].sum()
average_order_value = (
    df.groupby("Order ID")["Sales"].sum().mean()
    if "Order ID" in df.columns
    else None
)

profit_margin = (
    total_profit / total_sales * 100
    if total_sales != 0
    else 0
)

print("\n========== KEY BUSINESS METRICS ==========")
print(f"Total Sales: ${total_sales:,.2f}")
print(f"Total Profit: ${total_profit:,.2f}")
print(f"Total Quantity Sold: {total_quantity:,.0f}")
print(f"Profit Margin: {profit_margin:.2f}%")

if average_order_value is not None:
    print(f"Average Order Value: ${average_order_value:,.2f}")

# --------------------------------------------------
# 5. SALES AND PROFIT BY CATEGORY
# --------------------------------------------------

if "Category" in df.columns:
    category_summary = (
        df.groupby("Category", dropna=False)
        .agg(
            Total_Sales=("Sales", "sum"),
            Total_Profit=("Profit", "sum"),
            Total_Quantity=("Quantity", "sum")
        )
        .sort_values("Total_Sales", ascending=False)
    )

    print("\n========== CATEGORY PERFORMANCE ==========")
    print(category_summary.round(2).to_string())

    category_summary[["Total_Sales", "Total_Profit"]].plot(
        kind="bar",
        figsize=(10, 6)
    )

    plt.title("Sales and Profit by Category")
    plt.xlabel("Category")
    plt.ylabel("Amount")
    plt.xticks(rotation=0)
    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / "category_performance.png",
        dpi=150
    )
    plt.close()

# --------------------------------------------------
# 6. REGIONAL PERFORMANCE
# --------------------------------------------------

if "Region" in df.columns:
    region_summary = (
        df.groupby("Region", dropna=False)
        .agg(
            Total_Sales=("Sales", "sum"),
            Total_Profit=("Profit", "sum")
        )
        .sort_values("Total_Sales", ascending=False)
    )

    print("\n========== REGIONAL PERFORMANCE ==========")
    print(region_summary.round(2).to_string())

    region_summary[["Total_Sales", "Total_Profit"]].plot(
        kind="bar",
        figsize=(10, 6)
    )

    plt.title("Sales and Profit by Region")
    plt.xlabel("Region")
    plt.ylabel("Amount")
    plt.xticks(rotation=0)
    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / "regional_performance.png",
        dpi=150
    )
    plt.close()

# --------------------------------------------------
# 7. MONTHLY SALES TREND
# --------------------------------------------------

if "Order Date" in df.columns:
    monthly_df = df.dropna(subset=["Order Date"]).copy()

    monthly_df["Order Month"] = (
        monthly_df["Order Date"].dt.to_period("M").dt.to_timestamp()
    )

    monthly_sales = (
        monthly_df.groupby("Order Month")["Sales"]
        .sum()
        .sort_index()
    )

    print("\n========== MONTHLY SALES ==========")
    print(monthly_sales.round(2).to_string())

    monthly_sales.plot(
        kind="line",
        figsize=(12, 6),
        marker="o"
    )

    plt.title("Monthly Sales Trend")
    plt.xlabel("Month")
    plt.ylabel("Sales")
    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / "monthly_sales_trend.png",
        dpi=150
    )
    plt.close()

# --------------------------------------------------
# 8. PROFITABILITY BY SUB-CATEGORY
# --------------------------------------------------

if "Sub-Category" in df.columns:
    subcategory_profit = (
        df.groupby("Sub-Category", dropna=False)["Profit"]
        .sum()
        .sort_values()
    )

    print("\n========== LOWEST PROFIT SUB-CATEGORIES ==========")
    print(subcategory_profit.head(10).round(2).to_string())

    print("\n========== HIGHEST PROFIT SUB-CATEGORIES ==========")
    print(subcategory_profit.tail(10).sort_values(
        ascending=False
    ).round(2).to_string())

    subcategory_profit.plot(
        kind="barh",
        figsize=(10, 8)
    )

    plt.title("Profit by Sub-Category")
    plt.xlabel("Total Profit")
    plt.ylabel("Sub-Category")
    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / "subcategory_profit.png",
        dpi=150
    )
    plt.close()

# --------------------------------------------------
# 9. DISCOUNT AND PROFIT ANALYSIS
# --------------------------------------------------

if "Discount" in df.columns:
    discount_summary = (
        df.groupby("Discount", dropna=False)
        .agg(
            Average_Sales=("Sales", "mean"),
            Average_Profit=("Profit", "mean"),
            Record_Count=("Profit", "size")
        )
        .sort_index()
    )

    print("\n========== DISCOUNT ANALYSIS ==========")
    print(discount_summary.round(2).to_string())

    discount_summary[["Average_Profit"]].plot(
        kind="bar",
        figsize=(10, 6),
        legend=False
    )

    plt.title("Average Profit by Discount Level")
    plt.xlabel("Discount")
    plt.ylabel("Average Profit per Record")
    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / "discount_profit_analysis.png",
        dpi=150
    )
    plt.close()

# --------------------------------------------------
# 10. EXPORT SUMMARIES
# --------------------------------------------------

summary_file = OUTPUT_DIR / "eda_summary.xlsx"

with pd.ExcelWriter(summary_file, engine="openpyxl") as writer:
    metrics = pd.DataFrame({
        "Metric": [
            "Total Sales",
            "Total Profit",
            "Total Quantity Sold",
            "Profit Margin (%)"
        ],
        "Value": [
            total_sales,
            total_profit,
            total_quantity,
            profit_margin
        ]
    })

    metrics.to_excel(
        writer,
        sheet_name="Key Metrics",
        index=False
    )

    if "Category" in df.columns:
        category_summary.to_excel(
            writer,
            sheet_name="Category"
        )

    if "Region" in df.columns:
        region_summary.to_excel(
            writer,
            sheet_name="Region"
        )

    if "Sub-Category" in df.columns:
        subcategory_profit.to_frame(
            name="Total Profit"
        ).to_excel(
            writer,
            sheet_name="Sub-Category Profit"
        )

    if "Order Date" in df.columns:
        monthly_sales.to_frame(
            name="Total Sales"
        ).to_excel(
            writer,
            sheet_name="Monthly Sales"
        )

print("\n========== EDA COMPLETE ==========")
print("Charts and summary files saved to:")
print(OUTPUT_DIR)
