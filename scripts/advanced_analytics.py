from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from statsmodels.tsa.holtwinters import ExponentialSmoothing

from scripts.pipeline_config import REPORTING_CUTOFF

PROJECT_ROOT = Path(__file__).resolve().parent.parent
REPORT_ROOT = PROJECT_ROOT / "reports"


def run_discount_analysis(df):
    output_dir = REPORT_ROOT / "statistical_analysis"
    output_dir.mkdir(parents=True, exist_ok=True)

    required = [
        "Order ID", "Discount", "Profit", "Sub-Category",
        "Segment", "Region", "Quantity",
    ]
    analysis = df.dropna(subset=required).copy()
    analysis["Discount_Band"] = np.where(
        analysis["Discount"] > 0.30, "Above 30%", "30% or Less"
    )

    model = smf.ols(
        "Profit ~ C(Discount_Band, Treatment(reference='30% or Less'))"
        " + C(Q('Sub-Category')) + C(Segment) + C(Region) + Quantity",
        data=analysis,
    ).fit(
        cov_type="cluster",
        cov_kwds={"groups": analysis["Order ID"]},
    )
    coefficient = next(
        name for name in model.params.index
        if "Above 30%" in name
    )
    pd.DataFrame(
        {
            "term": model.params.index,
            "estimate": model.params.values,
            "cluster_robust_se": model.bse.values,
            "p_value": model.pvalues.values,
            "ci_lower": model.conf_int()[0].values,
            "ci_upper": model.conf_int()[1].values,
        }
    ).to_csv(output_dir / "discount_regression.csv", index=False)
    (output_dir / "discount_regression.txt").write_text(
        "Profit regression with order-clustered standard errors\n"
        f"Observations: {int(model.nobs)}\n"
        f"Order clusters: {analysis['Order ID'].nunique()}\n"
        f"Discount coefficient: {model.params[coefficient]:.4f}\n"
        f"Cluster-robust standard error: {model.bse[coefficient]:.4f}\n"
        f"95% confidence interval: "
        f"[{model.conf_int().loc[coefficient, 0]:.4f}, "
        f"{model.conf_int().loc[coefficient, 1]:.4f}]\n\n"
        f"{model.summary().as_text()}\n",
        encoding="utf-8",
    )

    order_ids = analysis["Order ID"].drop_duplicates().to_numpy()
    group_values = ["30% or Less", "Above 30%"]
    sums = np.zeros((len(order_ids), len(group_values)))
    counts = np.zeros_like(sums)
    order_index = {order_id: i for i, order_id in enumerate(order_ids)}
    for j, band in enumerate(group_values):
        subset = analysis.loc[analysis["Discount_Band"] == band]
        grouped = subset.groupby("Order ID")["Profit"].agg(["sum", "count"])
        for order_id, row in grouped.iterrows():
            i = order_index[order_id]
            sums[i, j] = row["sum"]
            counts[i, j] = row["count"]

    rng = np.random.default_rng(20261106)
    bootstrap_differences = np.empty(2000)
    for replicate in range(len(bootstrap_differences)):
        sampled = rng.integers(0, len(order_ids), size=len(order_ids))
        multiplicities = np.bincount(sampled, minlength=len(order_ids))
        group_counts = multiplicities @ counts
        group_sums = multiplicities @ sums
        means = np.divide(
            group_sums,
            group_counts,
            out=np.full(2, np.nan),
            where=group_counts > 0,
        )
        bootstrap_differences[replicate] = means[1] - means[0]

    original_groups = analysis.groupby("Discount_Band")["Profit"].mean()
    observed_difference = (
        original_groups["Above 30%"] - original_groups["30% or Less"]
    )
    low, high = np.nanpercentile(bootstrap_differences, [2.5, 97.5])
    pd.DataFrame(
        [{
            "difference_above_30_minus_30_or_less": observed_difference,
            "cluster_bootstrap_ci_lower": low,
            "cluster_bootstrap_ci_upper": high,
            "replicates": len(bootstrap_differences),
            "resampling_unit": "Order ID",
        }]
    ).to_csv(output_dir / "discount_profit_bootstrap.csv", index=False)

    break_even = []
    for subcategory, group in analysis.groupby("Sub-Category"):
        by_discount = (
            group.groupby("Discount")["Profit"].mean().sort_index()
        )
        previous_discount = None
        previous_profit = None
        threshold = np.nan
        for discount, mean_profit in by_discount.items():
            if previous_profit is not None and previous_profit > 0 >= mean_profit:
                threshold = previous_discount + (
                    (0 - previous_profit)
                    * (discount - previous_discount)
                    / (mean_profit - previous_profit)
                )
                break
            previous_discount = discount
            previous_profit = mean_profit
        break_even.append({
            "subcategory": subcategory,
            "break_even_discount": threshold,
            "observed_discount_levels": len(by_discount),
        })

    break_even_df = pd.DataFrame(break_even)
    break_even_df.to_csv(output_dir / "subcategory_break_even.csv", index=False)
    estimable = break_even_df["break_even_discount"].dropna()
    summary = (
        f"Order-clustered regression and discount bootstrap completed.\n"
        f"Mean profit difference (above 30% minus 30% or less): "
        f"{observed_difference:.2f}\n"
        f"Order-cluster bootstrap 95% CI: [{low:.2f}, {high:.2f}]\n"
        f"Median interpolated break-even discount among "
        f"{len(estimable)} subcategories with a positive-to-nonpositive "
        f"observed transition: "
        f"{estimable.median():.1%}\n"
        if not estimable.empty else
        f"Order-clustered regression and discount bootstrap completed.\n"
        f"Mean profit difference (above 30% minus 30% or less): "
        f"{observed_difference:.2f}\n"
        f"Order-cluster bootstrap 95% CI: [{low:.2f}, {high:.2f}]\n"
        "No subcategory showed an observed positive-to-nonpositive "
        "profit transition across its discount levels.\n"
    )
    (output_dir / "discount_analysis_summary.txt").write_text(
        summary, encoding="utf-8"
    )
    print(summary)


def run_customer_analysis(df):
    output_dir = REPORT_ROOT / "customer_analysis"
    output_dir.mkdir(parents=True, exist_ok=True)
    analysis = df.dropna(
        subset=["Customer ID", "Order ID", "Order Date", "Sales", "Profit"]
    ).copy()
    analysis["Order Date"] = pd.to_datetime(analysis["Order Date"])
    cutoff = pd.Timestamp(REPORTING_CUTOFF)
    customer = analysis.groupby("Customer ID").agg(
        last_order=("Order Date", "max"),
        frequency=("Order ID", "nunique"),
        monetary=("Sales", "sum"),
        profit=("Profit", "sum"),
    )
    customer["recency_days"] = (cutoff - customer["last_order"]).dt.days
    customer["R"] = pd.qcut(
        customer["recency_days"].rank(method="first", ascending=False),
        5,
        labels=[1, 2, 3, 4, 5],
    ).astype(int)
    customer["F"] = pd.qcut(
        customer["frequency"].rank(method="first"),
        5,
        labels=[1, 2, 3, 4, 5],
    ).astype(int)
    customer["M"] = pd.qcut(
        customer["monetary"].rank(method="first"),
        5,
        labels=[1, 2, 3, 4, 5],
    ).astype(int)
    customer["RFM_Score"] = customer[["R", "F", "M"]].sum(axis=1)
    customer["Segment"] = np.select(
        [
            customer["RFM_Score"] >= 13,
            (customer["RFM_Score"] >= 10) & (customer["R"] >= 3),
            (customer["RFM_Score"] >= 8) & (customer["F"] >= 3),
        ],
        ["Champions", "Loyal Customers", "Potential Loyalists"],
        default="Needs Attention",
    )
    customer.to_csv(output_dir / "customer_rfm.csv", index_label="Customer ID")

    segment_summary = customer.groupby("Segment").agg(
        customers=("profit", "size"),
        sales=("monetary", "sum"),
        profit=("profit", "sum"),
    )
    total_profit = customer["profit"].sum()
    segment_summary["profit_contribution_pct"] = (
        segment_summary["profit"] / total_profit * 100
    )
    segment_summary.to_csv(output_dir / "rfm_segment_summary.csv")
    top_segment = segment_summary["profit"].idxmax()
    top_share = segment_summary.loc[top_segment, "profit_contribution_pct"]

    analysis["cohort"] = analysis.groupby("Customer ID")["Order Date"].transform(
        "min"
    ).dt.to_period("M")
    analysis["order_month"] = analysis["Order Date"].dt.to_period("M")
    cohort_activity = analysis[
        ["Customer ID", "cohort", "order_month", "Order ID"]
    ].drop_duplicates()
    cohort_activity["cohort_index"] = (
        (cohort_activity["order_month"].dt.year - cohort_activity["cohort"].dt.year)
        * 12
        + cohort_activity["order_month"].dt.month
        - cohort_activity["cohort"].dt.month
    )
    cohort_sizes = cohort_activity.loc[
        cohort_activity["cohort_index"] == 0
    ].groupby("cohort")["Customer ID"].nunique()
    retained = cohort_activity.groupby(
        ["cohort", "cohort_index"]
    )["Customer ID"].nunique()
    retention = retained.div(cohort_sizes, level="cohort").rename(
        "retention_rate"
    )
    retention.rename_axis(["cohort_month", "months_since_first_order"]).reset_index(
    ).to_csv(output_dir / "cohort_retention.csv", index=False)

    print(
        f"RFM customers: {len(customer)}; highest-profit segment: "
        f"{top_segment} ({top_share:.1f}% of profit)."
    )


def run_sales_forecast(df):
    output_dir = REPORT_ROOT / "forecast"
    output_dir.mkdir(parents=True, exist_ok=True)
    analysis = df.dropna(subset=["Order Date", "Sales"]).copy()
    analysis["Order Date"] = pd.to_datetime(analysis["Order Date"])
    monthly_sales = analysis.set_index("Order Date")["Sales"].resample("MS").sum()
    monthly_sales = monthly_sales.loc[:pd.Timestamp(REPORTING_CUTOFF).to_period("M").to_timestamp()]
    monthly_sales = monthly_sales.asfreq("MS", fill_value=0)

    validation_months = 3
    train, actual = monthly_sales.iloc[:-validation_months], monthly_sales.iloc[-validation_months:]
    validation_model = ExponentialSmoothing(
        train,
        trend="add",
        seasonal="add",
        seasonal_periods=12,
        initialization_method="estimated",
    ).fit(optimized=True)
    predicted = validation_model.forecast(validation_months)
    baseline_values = monthly_sales.reindex(
        actual.index - pd.DateOffset(years=1)
    ).to_numpy()
    actual_values = actual.to_numpy()
    mape = np.mean(np.abs((actual_values - predicted.to_numpy()) / actual_values)) * 100
    baseline_mape = np.mean(
        np.abs((actual_values - baseline_values) / actual_values)
    ) * 100
    validation = pd.DataFrame({
        "month": actual.index,
        "actual_sales": actual_values,
        "holt_winters_sales": predicted.to_numpy(),
        "same_month_last_year_sales": baseline_values,
    })
    validation.to_csv(output_dir / "forecast_validation.csv", index=False)

    final_model = ExponentialSmoothing(
        monthly_sales,
        trend="add",
        seasonal="add",
        seasonal_periods=12,
        initialization_method="estimated",
    ).fit(optimized=True)
    forecast = final_model.forecast(3).rename("forecast_sales")
    forecast.rename_axis("month").reset_index().to_csv(
        output_dir / "sales_forecast.csv", index=False
    )
    (output_dir / "forecast_metrics.txt").write_text(
        f"Validation months: {actual.index.min():%Y-%m} to "
        f"{actual.index.max():%Y-%m}\n"
        f"Holt-Winters MAPE: {mape:.2f}%\n"
        f"Same-month-last-year baseline MAPE: {baseline_mape:.2f}%\n"
        "Forecast is an educational illustration on a partly synthetic "
        "dataset and is not reliable for real-business planning.\n",
        encoding="utf-8",
    )
    print(
        f"Forecast validation MAPE: Holt-Winters {mape:.2f}% vs "
        f"same-month-last-year {baseline_mape:.2f}%."
    )


def run_market_basket_analysis(df):
    output_dir = REPORT_ROOT / "market_basket"
    output_dir.mkdir(parents=True, exist_ok=True)
    basket = df[["Order ID", "Sub-Category"]].dropna().drop_duplicates()
    orders = basket["Order ID"].nunique()
    memberships = basket.groupby("Sub-Category")["Order ID"].nunique()
    pairs = basket.merge(basket, on="Order ID")
    pairs = pairs.loc[pairs["Sub-Category_x"] < pairs["Sub-Category_y"]]
    pair_counts = pairs.groupby(
        ["Sub-Category_x", "Sub-Category_y"]
    )["Order ID"].nunique()
    results = pair_counts.rename("pair_orders").reset_index()
    results["support"] = results["pair_orders"] / orders
    results["lift"] = results.apply(
        lambda row: row["support"] / (
            memberships[row["Sub-Category_x"]]
            / orders
            * memberships[row["Sub-Category_y"]]
            / orders
        ),
        axis=1,
    )
    results.sort_values(
        ["lift", "support"], ascending=False
    ).to_csv(output_dir / "subcategory_pairs.csv", index=False)
    print(f"Market basket pairs evaluated: {len(results)}.")


def run_all_analyses(df):
    run_discount_analysis(df)
    run_customer_analysis(df)
    run_sales_forecast(df)
    run_market_basket_analysis(df)
