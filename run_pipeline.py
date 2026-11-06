import subprocess
import sys
from pathlib import Path

import pandas as pd

from scripts.advanced_analytics import run_all_analyses
from scripts.pipeline_config import REPORTING_CUTOFF

PROJECT_ROOT = Path(__file__).resolve().parent
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
FULL_DATA_FILE = PROCESSED_DIR / "superstore_cleaned.csv"
REPORTING_DATA_FILE = PROCESSED_DIR / "superstore_reporting.csv"


def run_script(script_path):
    subprocess.run(
        [sys.executable, str(PROJECT_ROOT / script_path)],
        cwd=PROJECT_ROOT,
        check=True,
    )


def prepare_reporting_data():
    if not FULL_DATA_FILE.exists():
        raise FileNotFoundError(
            f"Cleaned dataset not found: {FULL_DATA_FILE}"
        )

    df = pd.read_csv(FULL_DATA_FILE, parse_dates=["Order Date", "Ship Date"])
    if df["Order Date"].isna().any():
        raise ValueError("Order Date contains null or invalid values.")
    cutoff = pd.Timestamp(REPORTING_CUTOFF)
    reporting = df.loc[df["Order Date"] <= cutoff].copy()
    reporting.to_csv(REPORTING_DATA_FILE, index=False)
    print(
        f"Reporting dataset: {len(reporting)} rows through "
        f"{REPORTING_CUTOFF}; full cleaned source remains unchanged."
    )
    return reporting


def main():
    run_script(Path("scripts") / "clean_data.py")
    reporting = prepare_reporting_data()
    run_script(Path("scripts") / "eda_analysis.py")
    run_script(Path("scripts") / "load_sqlite.py")
    run_script(Path("scripts") / "run_sql_analysis.py")
    run_all_analyses(reporting)
    subprocess.run(
        [sys.executable, "-m", "pytest", "-q"],
        cwd=PROJECT_ROOT,
        check=True,
    )
    print("\nPipeline completed; all automated data checks passed.")


if __name__ == "__main__":
    main()
