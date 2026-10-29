import pandas as pd
from pathlib import Path

# Project folder: the location of this Python file
PROJECT_DIR = Path(__file__).resolve().parent

# Dataset folder
DATA_FOLDER = PROJECT_DIR / "data" / "raw"

# Find CSV and Excel files
files = []

for pattern in ("*.csv", "*.xlsx", "*.xls"):
    files.extend(DATA_FOLDER.glob(pattern))

# Stop if no dataset is available
if not files:
    print("\nERROR: No dataset found!")
    print(f"Expected dataset location: {DATA_FOLDER}")
    print("\nPlease copy your CSV or Excel dataset into this folder.")
    print("\nFiles currently found in the raw folder:")

    if DATA_FOLDER.exists():
        for item in DATA_FOLDER.iterdir():
            print("-", item.name)
    else:
        print("The raw folder does not exist.")

    raise SystemExit(1)

# Use the first matching dataset
file_path = files[0]

print(f"\nDataset selected: {file_path.name}")

# Load the dataset
if file_path.suffix.lower() == ".csv":
    df = pd.read_csv(file_path, low_memory=False)
else:
    df = pd.read_excel(file_path)

print("\n========== DATASET OVERVIEW ==========")
print("File:", file_path.name)
print("Rows and columns:", df.shape)

print("\n========== COLUMN NAMES ==========")
print(df.columns.to_list())

print("\n========== DATA TYPES ==========")
print(df.dtypes)

print("\n========== DATA INFORMATION ==========")
df.info()

print("\n========== FIRST FIVE ROWS ==========")
print(df.head().to_string())

print("\n========== MISSING VALUES ==========")
print(df.isna().sum())

print("\n========== DUPLICATE ROWS ==========")
print("Duplicate count:", df.duplicated().sum())

print("\n========== STATISTICAL SUMMARY ==========")
print(df.describe(include="all").to_string())

print("\n========== INSPECTION COMPLETE ==========")
print("The original dataset has not been modified.")