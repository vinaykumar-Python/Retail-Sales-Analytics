import pandas as pd
from pathlib import Path

# --------------------------------------------------
# 1. DEFINE PROJECT PATHS
# --------------------------------------------------

PROJECT_DIR = Path(__file__).resolve().parent.parent

RAW_FILE = PROJECT_DIR / "data" / "raw" / "sample_-_superstore.xls"
OUTPUT_DIR = PROJECT_DIR / "data" / "processed"
OUTPUT_FILE = OUTPUT_DIR / "superstore_cleaned.csv"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------
# 2. LOAD THE ORIGINAL DATA
# --------------------------------------------------

print("\nLoading original dataset...")

df = pd.read_excel(RAW_FILE)

print("Original rows:", len(df))
print("Original columns:", len(df.columns))

# --------------------------------------------------
# 3. STANDARDIZE COLUMN NAMES
# --------------------------------------------------

df.columns = (
    df.columns.astype(str)
    .str.strip()
    .str.replace(r"\s+", " ", regex=True)
)

print("\nColumn names:")
print(df.columns.tolist())

# --------------------------------------------------
# 4. CHECK AND REMOVE EXACT DUPLICATE ROWS
# --------------------------------------------------

duplicate_count = df.duplicated().sum()

print("\nExact duplicate rows found:", duplicate_count)

if duplicate_count > 0:
    df = df.drop_duplicates().copy()
    print("Exact duplicate rows removed:", duplicate_count)
else:
    print("No exact duplicate rows found.")

# --------------------------------------------------
# 5. CLEAN TEXT COLUMNS
# --------------------------------------------------

text_columns = df.select_dtypes(include=["object", "string"]).columns

for column in text_columns:
    df[column] = df[column].map(
        lambda value: value.strip() if isinstance(value, str) else value
    )

# --------------------------------------------------
# 6. CHECK MISSING VALUES
# --------------------------------------------------

print("\nMissing values before further cleaning:")
print(df.isna().sum().to_string())

# --------------------------------------------------
# 7. CONVERT DATE COLUMNS
# --------------------------------------------------

for column in df.columns:
    if "date" in column.lower():
        converted_dates = pd.to_datetime(
            df[column],
            errors="coerce"
        )

        invalid_dates = df[column].notna() & converted_dates.isna()

        print(
            f"\nInvalid date values in '{column}':",
            int(invalid_dates.sum())
        )

        df[column] = converted_dates

# --------------------------------------------------
# 8. CHECK IMPORTANT NUMERICAL COLUMNS
# --------------------------------------------------

numeric_candidates = [
    "Sales",
    "Profit",
    "Quantity",
    "Discount"
]

for column in numeric_candidates:
    if column in df.columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

        print(f"\n{column} summary:")
        print(df[column].describe().to_string())

        print(
            f"Missing or invalid {column} values:",
            int(df[column].isna().sum())
        )

# --------------------------------------------------
# 9. CHECK BUSINESS RULES
# --------------------------------------------------

print("\n========== BUSINESS VALIDATION ==========")

if "Sales" in df.columns:
    print("Negative sales:", int((df["Sales"] < 0).sum()))

if "Quantity" in df.columns:
    print("Zero or negative quantities:", int((df["Quantity"] <= 0).sum()))

if "Discount" in df.columns:
    print("Discounts below 0:", int((df["Discount"] < 0).sum()))
    print("Discounts above 1:", int((df["Discount"] > 1).sum()))

if "Profit" in df.columns:
    print("Negative profit records:", int((df["Profit"] < 0).sum()))

# --------------------------------------------------
# 10. REPORT MISSING VALUES
# --------------------------------------------------

print("\nMissing values after cleaning checks:")
print(df.isna().sum().to_string())

# --------------------------------------------------
# 11. SAVE CLEANED DATASET
# --------------------------------------------------

df.to_csv(OUTPUT_FILE, index=False)

print("\n========== PROCESS COMPLETE ==========")
print("Final rows:", len(df))
print("Final columns:", len(df.columns))
print("Cleaned dataset saved to:")
print(OUTPUT_FILE)

print("\nOriginal dataset remains unchanged.")
