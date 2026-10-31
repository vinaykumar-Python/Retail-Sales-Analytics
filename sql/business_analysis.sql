-- ============================================================
-- RETAIL SALES ANALYTICS
-- Business Analysis Using SQLite
-- ============================================================

-- 1. Overall business performance
SELECT
    ROUND(SUM(Sales), 2) AS Total_Sales,
    ROUND(SUM(Profit), 2) AS Total_Profit,
    SUM(Quantity) AS Total_Quantity,
    ROUND(
        100.0 * SUM(Profit) / NULLIF(SUM(Sales), 0),
        2
    ) AS Profit_Margin_Percentage
FROM sales;


-- 2. Sales and profit by product category
SELECT
    Category,
    ROUND(SUM(Sales), 2) AS Total_Sales,
    ROUND(SUM(Profit), 2) AS Total_Profit
FROM sales
GROUP BY Category
ORDER BY Total_Sales DESC;


-- 3. Regional performance
SELECT
    Region,
    ROUND(SUM(Sales), 2) AS Total_Sales,
    ROUND(SUM(Profit), 2) AS Total_Profit
FROM sales
GROUP BY Region
ORDER BY Total_Profit DESC;


-- 4. Loss-making subcategories
SELECT
    "Sub-Category",
    ROUND(SUM(Sales), 2) AS Total_Sales,
    ROUND(SUM(Profit), 2) AS Total_Profit
FROM sales
GROUP BY "Sub-Category"
HAVING SUM(Profit) < 0
ORDER BY Total_Profit ASC;


-- 5. Top 10 products by sales
SELECT
    "Product Name",
    ROUND(SUM(Sales), 2) AS Total_Sales,
    ROUND(SUM(Profit), 2) AS Total_Profit
FROM sales
GROUP BY "Product Name"
ORDER BY Total_Sales DESC
LIMIT 10;


-- 6. Customer segment performance
SELECT
    Segment,
    ROUND(SUM(Sales), 2) AS Total_Sales,
    ROUND(SUM(Profit), 2) AS Total_Profit,
    SUM(Quantity) AS Total_Quantity
FROM sales
GROUP BY Segment
ORDER BY Total_Sales DESC;


-- 7. Shipping mode performance
SELECT
    "Ship Mode",
    COUNT(DISTINCT "Order ID") AS Unique_Orders,
    ROUND(SUM(Sales), 2) AS Total_Sales,
    ROUND(SUM(Profit), 2) AS Total_Profit
FROM sales
GROUP BY "Ship Mode"
ORDER BY Total_Sales DESC;


-- 8. Monthly sales and profit
SELECT
    strftime('%Y-%m', "Order Date") AS Year_Month,
    ROUND(SUM(Sales), 2) AS Total_Sales,
    ROUND(SUM(Profit), 2) AS Total_Profit
FROM sales
WHERE "Order Date" IS NOT NULL
GROUP BY strftime('%Y-%m', "Order Date")
ORDER BY Year_Month;


-- 9. Discount-level profitability
SELECT
    Discount,
    COUNT(*) AS Number_Of_Rows,
    ROUND(SUM(Sales), 2) AS Total_Sales,
    ROUND(SUM(Profit), 2) AS Total_Profit,
    ROUND(
        100.0 * SUM(Profit) / NULLIF(SUM(Sales), 0),
        2
    ) AS Profit_Margin_Percentage
FROM sales
GROUP BY Discount
ORDER BY Discount;


-- 10. Products generating the highest losses
SELECT
    "Product Name",
    ROUND(SUM(Sales), 2) AS Total_Sales,
    ROUND(SUM(Profit), 2) AS Total_Profit
FROM sales
GROUP BY "Product Name"
HAVING SUM(Profit) < 0
ORDER BY Total_Profit ASC
LIMIT 10;


-- ============================================================
-- 11. Monthly running totals using SQL window functions
-- ============================================================

WITH Monthly_Summary AS (
    SELECT
        strftime('%Y-%m', "Order Date") AS Year_Month,
        SUM(Sales) AS Monthly_Sales,
        SUM(Profit) AS Monthly_Profit
    FROM sales
    WHERE "Order Date" IS NOT NULL
    GROUP BY strftime('%Y-%m', "Order Date")
)

SELECT
    Year_Month,
    ROUND(Monthly_Sales, 2) AS Monthly_Sales,
    ROUND(Monthly_Profit, 2) AS Monthly_Profit,

    ROUND(
        SUM(Monthly_Sales) OVER (
            ORDER BY Year_Month
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ),
        2
    ) AS Running_Total_Sales,

    ROUND(
        SUM(Monthly_Profit) OVER (
            ORDER BY Year_Month
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ),
        2
    ) AS Running_Total_Profit

FROM Monthly_Summary
ORDER BY Year_Month;


-- ============================================================
-- 12. Rank product subcategories by profitability
-- ============================================================

WITH Subcategory_Profit AS (
    SELECT
        Category,
        "Sub-Category" AS Subcategory,
        SUM(Sales) AS Total_Sales,
        SUM(Profit) AS Total_Profit
    FROM sales
    GROUP BY Category, "Sub-Category"
)

SELECT
    Category,
    Subcategory,
    ROUND(Total_Sales, 2) AS Total_Sales,
    ROUND(Total_Profit, 2) AS Total_Profit,

    RANK() OVER (
        ORDER BY Total_Profit DESC
    ) AS Profit_Rank,

    DENSE_RANK() OVER (
        ORDER BY Total_Profit DESC
    ) AS Dense_Profit_Rank

FROM Subcategory_Profit
ORDER BY Total_Profit DESC;

-- ============================================================
-- 13. Year-over-year sales and profit growth using LAG()
-- ============================================================

WITH Yearly_Summary AS (
    SELECT
        CAST(strftime('%Y', "Order Date") AS INTEGER) AS Year,
        SUM(Sales) AS Total_Sales,
        SUM(Profit) AS Total_Profit
    FROM sales
    WHERE "Order Date" IS NOT NULL
    GROUP BY strftime('%Y', "Order Date")
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

    ROUND(Total_Sales, 2) AS Total_Sales,
    ROUND(Total_Profit, 2) AS Total_Profit,

    ROUND(Previous_Year_Sales, 2) AS Previous_Year_Sales,

    ROUND(
        Total_Sales - Previous_Year_Sales, 2
    ) AS Sales_Change,

    ROUND(
        100.0 * (Total_Sales - Previous_Year_Sales)
        / NULLIF(Previous_Year_Sales, 0), 2
    ) AS Sales_YoY_Percentage,

    ROUND(Previous_Year_Profit, 2) AS Previous_Year_Profit,

    ROUND(
        Total_Profit - Previous_Year_Profit, 2
    ) AS Profit_Change,

    ROUND(
        100.0 * (Total_Profit - Previous_Year_Profit)
        / NULLIF(Previous_Year_Profit, 0), 2
    ) AS Profit_YoY_Percentage

FROM Yearly_Comparison
ORDER BY Year;

-- ============================================================
-- 14. Reporting-period validation as of October 31, 2026
-- ============================================================

SELECT
    'Through 2026-10-31' AS Reporting_Period,

    COUNT(*) AS Total_Records,

    ROUND(SUM(Sales), 2) AS Total_Sales,

    ROUND(SUM(Profit), 2) AS Total_Profit,

    ROUND(
        100.0 * SUM(Profit) / NULLIF(SUM(Sales), 0),
        2
    ) AS Profit_Margin_Percentage

FROM sales

WHERE date("Order Date") <= date('2026-10-31');