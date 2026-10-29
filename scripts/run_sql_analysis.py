import sqlite3
from pathlib import Path

# Locate the project folder
PROJECT_DIR = Path(__file__).resolve().parent.parent

# Locate the SQLite database
DATABASE_FILE = (
    PROJECT_DIR / "data" / "processed" / "retail_sales.db"
)

# Check that the database exists
if not DATABASE_FILE.exists():
    raise FileNotFoundError(
        f"Database not found: {DATABASE_FILE}"
    )

# SQL queries to analyze the data
queries = {
    "Overall Business Performance": """
        SELECT
            ROUND(SUM(Sales), 2) AS Total_Sales,
            ROUND(SUM(Profit), 2) AS Total_Profit,
            SUM(Quantity) AS Total_Quantity,
            ROUND(
                100.0 * SUM(Profit) / NULLIF(SUM(Sales), 0),
                2
            ) AS Profit_Margin_Percentage
        FROM sales;
    """,

    "Category Performance": """
        SELECT
            Category,
            ROUND(SUM(Sales), 2) AS Total_Sales,
            ROUND(SUM(Profit), 2) AS Total_Profit
        FROM sales
        GROUP BY Category
        ORDER BY Total_Sales DESC;
    """,

    "Regional Performance": """
        SELECT
            Region,
            ROUND(SUM(Sales), 2) AS Total_Sales,
            ROUND(SUM(Profit), 2) AS Total_Profit
        FROM sales
        GROUP BY Region
        ORDER BY Total_Profit DESC;
    """,

    "Loss-Making Sub-Categories": """
        SELECT
            "Sub-Category",
            ROUND(SUM(Sales), 2) AS Total_Sales,
            ROUND(SUM(Profit), 2) AS Total_Profit
        FROM sales
        GROUP BY "Sub-Category"
        HAVING SUM(Profit) < 0
        ORDER BY Total_Profit ASC;
    """,

    "Top 10 Products by Sales": """
        SELECT
            "Product Name",
            ROUND(SUM(Sales), 2) AS Total_Sales,
            ROUND(SUM(Profit), 2) AS Total_Profit
        FROM sales
        GROUP BY "Product Name"
        ORDER BY Total_Sales DESC
        LIMIT 10;
    """
}

# Connect to the database and execute the queries
with sqlite3.connect(DATABASE_FILE) as connection:

    for title, query in queries.items():

        print("\n" + "=" * 65)
        print(title.upper())
        print("=" * 65)

        cursor = connection.execute(query)

        columns = [
            description[0]
            for description in cursor.description
        ]

        print(" | ".join(columns))
        print("-" * 65)

        for row in cursor.fetchall():
            print(" | ".join(
                str(value) if value is not None else "NULL"
                for value in row
            ))

print("\nSQL analysis completed successfully!")
