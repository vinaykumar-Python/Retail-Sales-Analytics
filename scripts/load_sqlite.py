import pandas as pd
import sqlite3
from pathlib import Path

# --------------------------------------------------
# 1. DEFINE PROJECT PATHS
# --------------------------------------------------

PROJECT_DIR = Path(__file__).resolve().parent.parent

CSV_FILE = (
    PROJECT_DIR
    / "data"
    / "processed"
    / "superstore_cleaned.csv"
)

DATABASE_FOLDER = PROJECT_DIR / "data" / "processed"
DATABASE_FILE = DATABASE_FOLDER / "retail_sales.db"

DATABASE_FOLDER.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------
# 2. CHECK THAT THE CLEANED DATASET EXISTS
# --------------------------------------------------

if not CSV_FILE.exists():
    raise FileNotFoundError(
        f"Cleaned dataset not found: {CSV_FILE}\n"
        "Run python scripts/clean_data.py first."
    )

# --------------------------------------------------
# 3. LOAD THE CLEANED DATASET
# --------------------------------------------------

df = pd.read_csv(CSV_FILE)

# --------------------------------------------------
# 4. PREPARE DATE COLUMNS
# --------------------------------------------------

for column in df.columns:
    if "date" in column.lower():
        df[column] = pd.to_datetime(
            df[column],
            errors="coerce"
        ).dt.strftime("%Y-%m-%d")

# --------------------------------------------------
# 5. CREATE THE SQLITE DATABASE
# --------------------------------------------------

with sqlite3.connect(DATABASE_FILE) as connection:

    df.to_sql(
        name="sales",
        con=connection,
        if_exists="replace",
        index=False
    )

    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM sales")
    row_count = cursor.fetchone()[0]

    cursor.execute("PRAGMA table_info(sales)")
    columns = cursor.fetchall()

print("\n========== DATABASE CREATED ==========")
print("Database:", DATABASE_FILE)
print("Table: sales")
print("Rows loaded:", row_count)

print("\n========== TABLE COLUMNS ==========")

for column in columns:
    print(column[1], "-", column[2])

print("\nSQL database is ready.")
