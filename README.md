# Retail Sales Analytics

### An End-to-End Data Analytics Project Using Python, SQL, Excel, and Power BI

## 1. Project Overview

Retail Sales Analytics is an end-to-end data analytics project that examines retail transactions to understand sales performance, profitability, regional differences, product category performance, and discount-related losses.

The project combines Python for data preparation and exploratory data analysis, SQL for business analysis, Excel for PivotTables and KPI analysis, and Power BI for interactive dashboards and business recommendations.

The objective is to transform raw transaction data into meaningful insights that support data-driven business decisions.

## 2. Business Problems

This project investigates the following business questions:

- What are the overall sales, profit, and profit margin?
- Which product categories generate the most sales and profit?
- Which regions contribute the most to profitability?
- Which product subcategories generate losses?
- How do sales and profit change over time?
- Are high discounts associated with lower profitability?
- How can interactive dashboards help stakeholders explore business performance?

## 3. Project Objectives

- Inspect, clean, and validate retail transaction data.
- Perform exploratory data analysis using Python.
- Store cleaned data in a SQLite database.
- Use SQL aggregation and window functions for business analysis.
- Perform statistical tests to investigate discount-related profitability differences.
- Build Excel PivotTables, charts, and KPI summaries.
- Develop interactive Power BI dashboards and recommendations.
- Document the workflow for reproducibility.

## 4. Dataset Description

The project uses a Superstore retail sales dataset containing 10,194 transaction rows and 21 columns.

Important fields include:

| Field | Description |
|---|---|
| Order ID | Order identifier |
| Order Date | Date the order was placed |
| Ship Date | Date the order was shipped |
| Customer ID | Customer identifier |
| Segment | Customer segment |
| Region | Sales region |
| Category | Product category |
| Sub-Category | Product subcategory |
| Sales | Sales amount |
| Profit | Profit or loss |
| Quantity | Quantity sold |
| Discount | Discount applied |

The dataset is used for analytical and educational purposes.

## 5. Tools and Technologies

| Technology | Purpose |
|---|---|
| Python | Data inspection, cleaning, and analysis |
| Pandas | Data manipulation and preparation |
| Matplotlib | Exploratory data visualizations |
| SciPy | Statistical hypothesis testing |
| Statsmodels | Order-clustered regression and Holt-Winters forecasting |
| SQLite | Local database storage |
| SQL | Business analysis and window functions |
| Microsoft Excel | PivotTables, charts, and KPI calculations |
| Power BI Desktop | Interactive dashboards and recommendations |
| pytest | Automated data-quality checks |
| Git and GitHub | Version control and project sharing |

## 6. Project Workflow

### Step 1: Data Inspection

Inspected the source dataset to understand its structure, fields, data types, and potential data-quality issues.

### Step 2: Data Cleaning

Used Python to standardize data, trim text values, remove exact duplicate rows, convert date and numeric fields, and inspect potential data-quality issues.

The cleaned dataset was exported to CSV format.

### Step 3: Exploratory Data Analysis

Used Python to generate charts and summary statistics to explore sales, profit, categories, regions, and discount patterns.

### Step 4: Database Creation

Loaded the reporting-cutoff dataset into SQLite to support consistent SQL analysis. The full cleaned CSV remains available separately.

### Step 5: SQL Business Analysis

Developed SQL queries covering:

- Overall sales, profit, quantity, and profit margin
- Category and regional performance
- Loss-making product subcategories
- Top products and customer segments
- Shipping mode performance
- Monthly sales and profit
- Discount-level profitability
- Running totals using `SUM() OVER()`
- Profitability rankings using `RANK()` and `DENSE_RANK()`
- Year-over-year comparisons using `LAG()`

### Step 6: Excel Analysis

Created PivotTables, charts, and KPI calculations to investigate category performance, regional performance, monthly trends, and discount-level profitability.

### Step 7: Statistical and Customer Analysis

The initial SciPy tests compare records with discounts of 30% or less against records with discounts above 30%; they are exploratory because they do not adjust for order-level dependence or other factors. The reproducible pipeline also runs a regression controlling for subcategory, segment, region, and quantity, with standard errors clustered by order, an order-cluster bootstrap confidence interval, and an observed-level subcategory break-even analysis.

The pipeline calculates customer RFM scores, segments, and first-order-month cohort retention. Results describe this dataset and are not causal evidence.

### Step 8: Power BI Dashboard

Developed an interactive dashboard with KPI cards, category comparisons, regional performance, monthly trends, and slicers for exploring the data.

### Step 9: Power BI Recommendations

Added a separate Recommendations page with business actions related to:

- Reviewing high-discount transactions
- Investigating loss-making subcategories
- Protecting profitability in high-performing subcategories
- Monitoring sales growth alongside profit growth

The recommendations are based on the current dataset analysis and should be reviewed alongside data-quality and statistical limitations.

## 7. Key Business Findings

The following figures were calculated from the complete cleaned dataset, including rows after the fixed reporting cutoff. Use the cutoff-based pipeline outputs for reporting-period analyses.

| Metric | Result |
|---|---:|
| Total Sales | 2,326,534.35 |
| Total Profit | 292,296.81 |
| Total Quantity Sold | 38,654 |
| Profit Margin | 12.56% |
| Total Distinct Orders | 5,111 |
| Transaction Rows | 10,194 |

**Note:** The full dataset contains order dates through December 2026, which is after the current date of November 6, 2026. The reproducible reporting pipeline excludes orders after the fixed October 31, 2026 reporting cutoff from the database and analyses, while preserving the full cleaned export.

### Category Performance

Technology generated the highest sales and profit among the three product categories.

| Category | Sales | Profit |
|---|---:|---:|
| Technology | 839,893.28 | 146,543.38 |
| Furniture | 754,747.76 | 19,730.00 |
| Office Supplies | 731,893.31 | 126,023.44 |

### Regional Performance

The West region recorded the highest sales and profit among the four regions.

| Region | Sales | Profit |
|---|---:|---:|
| West | 739,813.61 | 110,798.82 |
| East | 691,828.17 | 94,883.26 |
| Central | 503,170.67 | 39,865.31 |
| South | 391,721.91 | 46,749.43 |

### Loss-Making Subcategories

Three subcategories reported negative total profit.

| Subcategory | Sales | Profit |
|---|---:|---:|
| Tables | 208,020.18 | -17,753.21 |
| Bookcases | 115,361.20 | -3,632.07 |
| Supplies | 46,725.50 | -1,171.39 |

### Subcategory Profitability Ranking

The SQL ranking analysis identified Copiers as the highest-profit subcategory, with total profit of 56,093.94.

Phones ranked second, with total profit of 45,050.83.

These findings demonstrate why sales revenue and profit should be evaluated separately.

### Discount and Profitability Analysis

The initial record-level analysis produced the following results:

| Metric | Discount ≤ 30% | Discount > 30% |
|---|---:|---:|
| Record count | 9,009 | 1,185 |
| Mean profit per record | 46.38 | -105.91 |
| Median profit per record | 10.89 | -17.25 |
| Total profit | 417,804.05 | -125,507.24 |

The difference in average profit was -152.29 per record when comparing the above-30% group with the 30%-or-less group.

Both Welch's t-test and the Mann–Whitney U test reported statistically significant differences in the initial analysis.

**Interpretation caution:** These are record-level comparisons, and multiple records may belong to the same order. Further analysis should account for order-level dependence and other potential confounding factors. Statistical association does not establish causation.

## Reporting Period and Year-over-Year Analysis

### Reporting Period

The supplied dataset contains order dates from January 3, 2023, through December 30, 2026. The pipeline uses a fixed October 31, 2026 reporting cutoff and excludes later orders from the reporting dataset and SQLite database.

The original source and full cleaned data are preserved. Future-dated records are not deleted from either.

### January–October Comparison

| Metric | Jan–Oct 2025 | Jan–Oct 2026 |
|---|---:|---:|
| Records | 1,898 | 2,437 |
| Sales | 437,019.34 | 541,937.99 |
| Profit | 60,727.49 | 77,578.42 |
| Profit Margin | 13.90% | 14.31% |

**Key findings from the supplied dataset:**
- Sales increased by 24.01%.
- Profit increased by 27.75%.
- Profit margin improved by approximately 0.42 percentage points.

These results are based on the supplied dataset and do not independently establish actual business performance.

### Analytical Consideration

A partial-year total should not be directly compared with a full-year total to determine year-over-year growth. The January–October comparison uses matching reporting periods to provide a more meaningful comparison.

The source dataset's provenance and completeness have not been independently verified.

## 8. Additional Analyses and Reproducible Pipeline

Run the complete workflow, including cleaning, cutoff filtering, SQLite loading, analyses, report generation, and automated checks, from the project root:

```powershell
python run_pipeline.py
```

The pipeline keeps `superstore_cleaned.csv` as the full cleaned data and creates `superstore_reporting.csv` for records through the reporting cutoff. SQLite and the analysis reports use that same reporting period.

### Discount Analysis

The regression models line-item profit against the two discount bands (`30% or less` and `above 30%`) and controls for subcategory, customer segment, region, and quantity. Standard errors are clustered by order to account for dependence among line items in the same order. The confidence interval for the mean profit difference is estimated by resampling orders, not individual rows.

Subcategory break-even discounts are estimated by linear interpolation between adjacent observed discount levels where mean profit changes from positive to non-positive. Subcategories without an observed crossing are reported without an estimated threshold; these estimates are descriptive, not causal.

Outputs are in `reports/statistical_analysis/`: clustered regression coefficients and summary, bootstrap interval, and per-subcategory break-even table.

On the current reporting data, the adjusted above-30% band coefficient is **-$187.86 per line item** (order-clustered SE **$12.36**). The unadjusted above-30%-minus-lower-band mean difference is **-$147.22** with a cluster-bootstrap 95% CI of **[-$168.49, -$128.51]**. The median interpolated break-even is **25.7%** across the 13 subcategories with an observed crossing; this is not a universal pricing threshold.

### RFM and Cohort Retention

Customer recency is measured at the reporting cutoff; frequency counts distinct orders and monetary value sums sales. Each component is scored in quintiles and customers are assigned to four RFM segments. Monthly cohort retention counts distinct customers with an order in each month after their first order month.

Outputs are in `reports/customer_analysis/`. The reporting data has **803 customers**; Champions is the largest profit-contributing segment at **33.3%**. The top segment's profit share is printed by the pipeline.

### Monthly Sales Forecast

An additive Holt-Winters model is validated on the most recent three reporting months and compared with a same-month-last-year baseline. The model is then fit to the full reporting series to forecast the next three months. Validation metrics and predictions are in `reports/forecast/`.

For this dataset, validation MAPE was **22.97%** for Holt-Winters versus **31.79%** for the baseline (August–October 2026). The next-three-month point forecasts are in the CSV output.

**Forecast limitation:** The supplied data is partly synthetic and its provenance and completeness have not been independently verified. Forecast errors on this dataset do not establish that the model is reliable for a real business; treat the forecast as an educational demonstration only.

### Automated Data Checks

`pytest` runs four checks as the final pipeline step:

1. Order, customer, and product keys are non-null.
2. Ship date is not before order date.
3. Pandas and SQLite profit totals reconcile to within one cent.
4. No reporting order is after the October 31, 2026 cutoff.

### Power BI Measures and Market Basket

`powerbi/measures.dax` contains date-table, year-over-year, month-to-date, rolling three-month average, and discount scenario measures. Create a relationship from the date table to `sales[Order Date]`, use the discount scenario value in a single-select slicer, and note the scenario measure's fixed-volume/fixed-cost assumption.

The optional market basket analysis ranks subcategory pairs by support and lift. Results are in `reports/market_basket/subcategory_pairs.csv`.

### Resume Statements

Use the generated report values rather than placeholders when describing this work:

- “Quantified the effect of discounting on profit using order-clustered regression, finding a median observed break-even discount of about **25.7%** across 13 subcategories.”
- “Segmented **803** customers with RFM and measured cohort retention, identifying that Champions contribute **33.3%** of profit.”
- “Built a reproducible analytics pipeline with **4 automated data-quality tests**.”
- “Built DAX time-intelligence measures (YoY, rolling averages) and a what-if discount simulator.”

## 9. Power BI Dashboard Features

The main dashboard includes:

- Total Sales KPI
- Total Profit KPI
- Total Orders KPI
- Total Quantity KPI
- Profit Margin KPI
- Sales and profit by category
- Regional sales and profit performance
- Monthly sales and profit trends
- Region slicer
- Category slicer
- Segment slicer
- Order Date slicer

The separate Recommendations page presents business actions derived from the analysis.

### Dashboard Preview

![Retail Sales Analytics Power BI Dashboard](powerbi/dashboard_screenshot.png)

### Power BI Report

[Open the Power BI report file](powerbi/Retail_Sales_Analytics.pbix)

**Requirement:** The `.pbix` file must be opened using Power BI Desktop.

## 10. Project Structure

```text
Retail-Sales-Analytics/
├── data/
│   ├── raw/
│   │   └── sample_-_superstore.xls
│   └── processed/
│       ├── superstore_cleaned.csv
│       ├── superstore_reporting.csv
│       └── retail_sales.db
├── scripts/
│   ├── inspect_data.py
│   ├── clean_data.py
│   ├── eda_analysis.py
│   ├── load_sqlite.py
│   ├── run_sql_analysis.py
│   ├── discount_hypothesis_test.py
│   ├── advanced_analytics.py
│   └── pipeline_config.py
├── run_pipeline.py
├── requirements.txt
├── tests/
│   └── test_pipeline.py
├── sql/
│   └── business_analysis.sql
├── excel/
│   └── Retail_Sales_Analysis.xlsx
├── powerbi/
│   ├── Retail_Sales_Analytics.pbix
│   ├── dashboard_screenshot.png
│   └── measures.dax
├── reports/
│   ├── eda_charts/
│   ├── statistical_analysis/
│   ├── customer_analysis/
│   ├── forecast/
│   └── market_basket/
└── README.md
```

The pipeline creates its analysis outputs under `reports/`.

## 11. Setup and Installation

### Requirements

- Python 3
- Power BI Desktop for opening and exploring the `.pbix` report
- Git for version control (optional if downloading the project as a ZIP)

### Step 1: Open the project directory

Open a terminal in the project root:

```powershell
cd D:\Resume_prjs\Retail-Sales-Analytics
```

### Step 2: Create a virtual environment

```powershell
python -m venv .venv
```

Activate it in Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can use Command Prompt instead:

```bat
.venv\Scripts\activate.bat
```

### Step 3: Install the Python dependencies

```powershell
python -m pip install -r requirements.txt
```

### Step 4: Run the reproducible pipeline

Run the end-to-end workflow from the project root:

```powershell
python run_pipeline.py
```

The source dataset must be available at the path and filename expected by the scripts. The pipeline uses the documented October 31, 2026 cutoff.

The component scripts can still be run separately for exploration, but `python run_pipeline.py` is the supported end-to-end entry point.

### Step 5: Open the Excel workbook

Open:

`excel/Retail_Sales_Analysis.xlsx`

Use the workbook to explore PivotTables, KPI calculations, and charts.

### Step 6: Open the Power BI report

Open:

`powerbi/Retail_Sales_Analytics.pbix`

Use Power BI Desktop to explore the dashboard and Recommendations page.

## 12. Limitations

- Results describe the available dataset and may not generalize to every retail business.
- Orders after the October 31, 2026 cutoff are excluded from reporting but remain in the full source and cleaned exports.
- The source data is partly synthetic; provenance and completeness have not been independently verified.
- The forecast is an educational example and should not be treated as reliable real-business guidance.
- The initial discount tests compare individual sales records and may violate the independence assumption when records share an order; the clustered model addresses within-order uncertainty but does not establish causation.
- The statistical findings show association, not proof of causation.
- The initial analysis is descriptive and does not establish causal relationships.
- Further analysis could account for order-level dependence, product mix, customer characteristics, and other factors.

## 13. Future Improvements

Potential enhancements include:

- Product-level profitability and pricing analysis.
- Automated data refresh and report generation.
- External validation of the forecast against genuine business data.

## 14. Conclusion

This project demonstrates an end-to-end retail analytics workflow, from raw data inspection and cleaning to SQL analysis, Excel reporting, statistical testing, and interactive Power BI dashboards.

It combines technical analysis with business recommendations to demonstrate how retail transaction data can be transformed into useful insights.

## Author

Developed as a data analytics portfolio project demonstrating Python, SQL, Excel, Power BI, and statistical analysis skills.