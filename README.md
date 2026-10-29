# Retail Sales Analytics

### An End-to-End Data Analytics Project Using Python, SQL, Excel, and Power BI

## 1. Project Overview

Retail Sales Analytics is an end-to-end data analytics project that examines retail sales transactions to understand sales performance, profitability, regional differences, product category performance, and discount-related losses.

The project uses Python for data preparation and exploratory data analysis, SQL for business queries, Excel for PivotTables and KPI analysis, and Power BI for interactive dashboard development.

The objective is to turn raw retail transaction data into meaningful business insights that can support data-driven decision-making.

## 2. Business Problem

Retail businesses need to understand more than their total revenue. They must identify profitable product categories, compare regional performance, monitor trends over time, and investigate products or discount levels associated with losses.

This project addresses the following business questions:

- What are the overall sales, profit, and profit margin?
- Which product categories generate the most sales and profit?
- Which regions contribute the most to profitability?
- Which product subcategories generate losses?
- How do sales and profit change over time?
- How are discount levels associated with profitability?
- How can business users explore results through an interactive dashboard?

## 3. Project Objectives

- Clean and prepare raw retail transaction data.
- Perform exploratory data analysis using Python.
- Store the cleaned data in a SQLite database.
- Write SQL queries to answer business questions.
- Analyze performance using Excel PivotTables and formulas.
- Build an interactive Power BI dashboard.
- Communicate findings through clear metrics, visualizations, and documentation.

## 4. Dataset Description

The project uses a Superstore retail sales dataset containing approximately 10,194 transaction rows and 21 columns.

Important fields include:

| Field | Description |
|---|---|
| Order ID | Identifier for an order |
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

The data is used for analytical and educational purposes.

## 5. Tools and Technologies

| Technology | Purpose |
|---|---|
| Python | Data inspection, cleaning, and exploratory analysis |
| Pandas | Data manipulation and preparation |
| Matplotlib | Exploratory data visualizations |
| SQLite | Local database storage and querying |
| SQL | Business analysis and aggregation |
| Microsoft Excel | PivotTables, KPI calculations, and discount analysis |
| Power BI Desktop | Interactive business intelligence dashboard |
| Git and GitHub | Version control and project sharing |

## 6. Project Workflow

### Step 1: Data Inspection

Inspected the source dataset to understand its structure, columns, data types, and data quality.

### Step 2: Data Cleaning

Used Python to standardize column names, trim text values, remove exact duplicate rows, convert date fields, convert numeric fields, and inspect potential data-quality issues.

The cleaned dataset was exported to CSV format.

### Step 3: Exploratory Data Analysis

Used Python to generate visualizations and summary information to explore the dataset and identify patterns that warranted further investigation.

### Step 4: Database Creation

Loaded the cleaned data into a local SQLite database for structured querying.

### Step 5: SQL Business Analysis

Developed SQL queries to calculate overall performance, compare product categories and regions, identify loss-making subcategories, and analyze monthly sales and profit.

### Step 6: Excel Analysis

Created PivotTables and charts to analyze:

- Sales and profit by category
- Regional sales and profit
- Monthly sales and profit trends
- Discount-level performance
- Overall business KPIs

### Step 7: Power BI Dashboard

Developed a dashboard with KPI measures, category comparisons, regional performance, monthly trends, and interactive slicers.

The dashboard is designed to help users explore performance across regions, product categories, customer segments, and dates.

## 7. Key Business Findings

The following results were calculated from the cleaned dataset.

| Metric | Result |
|---|---:|
| Total Sales | 2,326,534.35 |
| Total Profit | 292,296.81 |
| Total Quantity Sold | 38,654 |
| Profit Margin | 12.56% |
| Total Distinct Orders | 5,111 |

### Category Performance

Technology generated the highest sales among the three product categories.

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

The following subcategories reported negative total profit:

| Subcategory | Sales | Profit |
|---|---:|---:|
| Tables | 208,020.18 | -17,753.21 |
| Bookcases | 115,361.20 | -3,632.07 |
| Supplies | 46,725.50 | -1,171.39 |

### Discount Analysis

The Excel analysis showed negative aggregate profit at several discount levels, including 30%, 40%, 50%, 60%, 70%, and 80%.

These findings indicate that the relationship between discounts and profitability deserves further investigation. They do not, by themselves, prove that discounts caused the losses.

## 8. Power BI Dashboard Features

The dashboard includes:

- Total Sales KPI
- Total Profit KPI
- Total Orders KPI
- Total Quantity KPI
- Profit Margin KPI
- Sales and Profit by Product Category
- Regional Sales and Profit Performance
- Monthly Sales and Profit Trend
- Region slicer
- Category slicer
- Segment slicer
- Order Date slicer

These features enable users to explore the data interactively.

## 9. Project Structure

```text
Retail-Sales-Analytics/
├── data/
│   ├── raw/
│   └── processed/
├── scripts/
│   ├── inspect_data.py
│   ├── clean_data.py
│   ├── eda_analysis.py
│   ├── load_sqlite.py
│   └── run_sql_analysis.py
├── sql/
│   └── business_analysis.sql
├── excel/
│   └── Retail_Sales_Analysis.xlsx
├── notebooks/
├── powerbi/
│   └── Retail_Sales_Analytics.pbix
├── reports/
│   └── eda_charts/
└── README.md
```

## 10. How to Run the Python Scripts

### Requirements

- Python 3
- Pandas
- Matplotlib
- xlrd
- SQLite support

Install the required packages:

```bash
pip install pandas matplotlib xlrd
```

Run the scripts from the project root directory:

```bash
python scripts/inspect_data.py
python scripts/clean_data.py
python scripts/eda_analysis.py
python scripts/load_sqlite.py
python scripts/run_sql_analysis.py
```

Run the scripts in the order shown above so that the required cleaned data and database are available.

The source dataset must be placed in `data/raw/` using the filename expected by the inspection and cleaning scripts.

## 11. Limitations

- The findings describe the available dataset and may not represent every retail business.
- The analysis is primarily descriptive rather than predictive.
- Associations between discounts and losses do not establish causation.
- Historical patterns do not guarantee future performance.
- Further investigation of costs, product mix, customers, and operational factors could provide additional context.

## 12. Future Improvements

Potential enhancements include:

- Adding customer-level profitability analysis.
- Developing a product-level profit optimization report.
- Investigating the relationship between discounts and profit using statistical methods.
- Adding automated data refresh and validation.
- Introducing more detailed customer segmentation.
- Publishing an accessible Power BI report where appropriate.

## 13. Conclusion

This project demonstrates an end-to-end retail data analytics workflow, from raw data inspection and cleaning to SQL querying, spreadsheet analysis, and interactive business intelligence reporting.

It highlights how multiple analytics tools can work together to transform transaction data into useful business metrics and insights.

## Author

Developed as a data analytics portfolio project demonstrating Python, SQL, Excel, and Power BI skills.