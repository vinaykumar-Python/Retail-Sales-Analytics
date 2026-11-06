import sqlite3
from pathlib import Path

import pandas as pd

from scripts.pipeline_config import REPORTING_CUTOFF

PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPORTING_DATA = (
    PROJECT_ROOT / "data" / "processed" / "superstore_reporting.csv"
)
DATABASE = PROJECT_ROOT / "data" / "processed" / "retail_sales.db"


def load_reporting_data():
    return pd.read_csv(
        REPORTING_DATA,
        parse_dates=["Order Date", "Ship Date"],
    )


def test_reporting_data_has_no_null_keys():
    df = load_reporting_data()
    key_columns = ["Order ID", "Customer ID", "Product ID"]
    assert df[key_columns].notna().all().all()


def test_ship_date_is_not_before_order_date():
    df = load_reporting_data()
    assert (df["Ship Date"] >= df["Order Date"]).all()


def test_pandas_and_sql_profit_totals_reconcile():
    df = load_reporting_data()
    with sqlite3.connect(DATABASE) as connection:
        sql_profit = connection.execute(
            "SELECT SUM(Profit) FROM sales"
        ).fetchone()[0]
    assert abs(float(df["Profit"].sum()) - float(sql_profit)) < 0.01


def test_reporting_data_has_no_orders_after_cutoff():
    df = load_reporting_data()
    assert df["Order Date"].max() <= pd.Timestamp(REPORTING_CUTOFF)
