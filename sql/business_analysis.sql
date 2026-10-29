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