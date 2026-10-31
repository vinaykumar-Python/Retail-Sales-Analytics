import sqlite3

DB_PATH = "data/processed/retail_sales.db"
CUTOFF_DATE = "2026-10-31"


def print_section(title):
    """Print a formatted section heading."""
    print("\n" + "=" * 85)
    print(title)
    print("=" * 85)


def calculate_percentage_change(current, previous):
    """Calculate percentage change safely."""
    if previous is None or previous == 0 or current is None:
        return None

    return (current - previous) / abs(previous) * 100


def format_percentage(value):
    """Format a percentage or return N/A."""
    if value is None:
        return "N/A"

    return f"{value:+.2f}%"


def run_year_over_year_analysis(connection):
    """Analyze yearly sales and profit through the reporting cutoff."""

    query = """
    WITH Yearly_Summary AS (
        SELECT
            CAST(strftime('%Y', "Order Date") AS INTEGER) AS Year,
            SUM(Sales) AS Total_Sales,
            SUM(Profit) AS Total_Profit
        FROM sales
        WHERE "Order Date" IS NOT NULL
          AND date("Order Date") <= date(?)
        GROUP BY CAST(strftime('%Y', "Order Date") AS INTEGER)
    ),

    Yearly_Comparison AS (
        SELECT
            Year,
            Total_Sales,
            Total_Profit,

            LAG(Total_Sales) OVER (
                ORDER BY Year
            ) AS Previous_Year_Sales,

            LAG(Total_Profit) OVER (
                ORDER BY Year
            ) AS Previous_Year_Profit

        FROM Yearly_Summary
    )

    SELECT
        Year,
        Total_Sales,
        Total_Profit,
        Previous_Year_Sales,
        Previous_Year_Profit

    FROM Yearly_Comparison
    ORDER BY Year;
    """

    rows = connection.execute(query, (CUTOFF_DATE,)).fetchall()

    print_section("YEAR-OVER-YEAR BUSINESS ANALYSIS")

    print(f"Reporting cutoff: {CUTOFF_DATE}")
    print("Note: 2026 is a partial year through October 31.\n")

    print(
        f"{'Year':<10}"
        f"{'Sales':>18}"
        f"{'Profit':>18}"
        f"{'Sales YoY':>18}"
        f"{'Profit YoY':>18}"
    )

    print("-" * 82)

    results = []

    for row in rows:
        year, sales, profit, previous_sales, previous_profit = row

        sales_change = calculate_percentage_change(
            sales, previous_sales
        )

        profit_change = calculate_percentage_change(
            profit, previous_profit
        )

        print(
            f"{year:<10}"
            f"{sales:>18,.2f}"
            f"{profit:>18,.2f}"
            f"{format_percentage(sales_change):>18}"
            f"{format_percentage(profit_change):>18}"
        )

        results.append(
            {
                "year": year,
                "sales": sales,
                "profit": profit,
                "sales_change": sales_change,
                "profit_change": profit_change,
            }
        )

    print(
        "\nInterpretation: Do not compare partial-year 2026 totals "
        "directly with full-year 2025 totals."
    )

    return results


def run_same_period_comparison(connection):
    """Compare January-October 2025 with January-October 2026."""

    query = """
    SELECT
        CAST(strftime('%Y', "Order Date") AS INTEGER) AS Year,
        COUNT(*) AS Total_Records,
        ROUND(SUM(Sales), 2) AS Total_Sales,
        ROUND(SUM(Profit), 2) AS Total_Profit
    FROM sales
    WHERE "Order Date" IS NOT NULL
      AND (
          date("Order Date") BETWEEN date('2025-01-01')
                                 AND date('2025-10-31')
          OR
          date("Order Date") BETWEEN date('2026-01-01')
                                 AND date('2026-10-31')
      )
    GROUP BY CAST(strftime('%Y', "Order Date") AS INTEGER)
    ORDER BY Year;
    """

    rows = connection.execute(query).fetchall()

    print_section("JANUARY-OCTOBER COMPARISON")

    print(
        f"{'Year':<10}"
        f"{'Records':>12}"
        f"{'Sales':>20}"
        f"{'Profit':>20}"
        f"{'Profit Margin':>18}"
    )

    print("-" * 80)

    data_by_year = {}

    for year, records, sales, profit in rows:
        margin = profit / sales * 100 if sales else 0

        print(
            f"{year:<10}"
            f"{records:>12,}"
            f"{sales:>20,.2f}"
            f"{profit:>20,.2f}"
            f"{margin:>17.2f}%"
        )

        data_by_year[year] = {
            "records": records,
            "sales": sales,
            "profit": profit,
            "margin": margin,
        }

    if 2025 not in data_by_year or 2026 not in data_by_year:
        print(
            "\nCould not calculate the comparison because "
            "one or both years are missing."
        )
        return

    previous = data_by_year[2025]
    current = data_by_year[2026]

    sales_growth = calculate_percentage_change(
        current["sales"], previous["sales"]
    )

    profit_growth = calculate_percentage_change(
        current["profit"], previous["profit"]
    )

    margin_change = current["margin"] - previous["margin"]

    print_section("SAME-PERIOD GROWTH RESULTS")

    print(f"Sales change: {format_percentage(sales_growth)}")
    print(f"Profit change: {format_percentage(profit_growth)}")
    print(f"Profit margin change: {margin_change:+.2f} percentage points")

    print("\nBusiness interpretation:")
    print(
        "Compare the January-October periods rather than comparing "
        "partial-year 2026 with full-year 2025."
    )

    print(
        "These results describe the supplied dataset and do not "
        "independently establish real-world business performance."
    )


def main():
    """Run all validation analyses."""

    try:
        with sqlite3.connect(DB_PATH) as connection:
            print_section("RETAIL SALES ANALYTICS")
            print(f"Database: {DB_PATH}")
            print(f"Reporting cutoff: {CUTOFF_DATE}")

            run_year_over_year_analysis(connection)
            run_same_period_comparison(connection)

            print_section("VALIDATION COMPLETED")
            print("All analyses completed successfully.")

    except sqlite3.Error as error:
        print("\nDatabase error:", error)

    except FileNotFoundError:
        print("\nDatabase file not found:", DB_PATH)

    except Exception as error:
        print("\nUnexpected error:", error)


if __name__ == "__main__":
    main()