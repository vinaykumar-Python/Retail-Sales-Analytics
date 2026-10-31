import sqlite3

DB_PATH = "data/processed/retail_sales.db"

query = """
SELECT
    COUNT(*) AS Total_Records,
    ROUND(SUM(Sales), 2) AS Total_Sales,
    ROUND(SUM(Profit), 2) AS Total_Profit,
    ROUND(
        100.0 * SUM(Profit) / NULLIF(SUM(Sales), 0),
        2
    ) AS Profit_Margin_Percentage
FROM sales
WHERE date("Order Date") <= date('2026-10-31');
"""

try:
    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.execute(query)
        result = cursor.fetchone()

        print("\nREPORTING-PERIOD VALIDATION")
        print("=" * 55)
        print("Reporting cutoff: October 31, 2026")
        print("Total records:", result[0])
        print("Total sales:", result[1])
        print("Total profit:", result[2])
        print("Profit margin:", str(result[3]) + "%")

except sqlite3.Error as error:
    print("Database error:", error)