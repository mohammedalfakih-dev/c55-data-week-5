"""Tasks 5 and 6: Build report tables and write outputs."""

import logging
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd


def build_reports(enriched: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """Task 5: Build four summary tables using groupby and named aggregations."""
    enriched = enriched.copy()

    enriched["revenue"] = enriched["price"] * enriched["quantity"]
    enriched["week"] = enriched["date"].dt.isocalendar().week

    weekly_revenue = (
        enriched.groupby(["week", "region"])
        .agg(
            total_revenue=("revenue", "sum"),
            order_count=("transaction_id", "count"),
        )
        .reset_index()
    )

    customer_summary = (
        enriched.groupby("customer_email")
        .agg(
            customer_name=("customer_name", "first"),
            region=("region", "first"),
            loyalty_tier=("loyalty_tier", "first"),
            total_spent=("revenue", "sum"),
            avg_order=("revenue", "mean"),
            order_count=("transaction_id", "count"),
        )
        .reset_index()
    )

    category_performance = (
        enriched.groupby("category")
        .agg(
            total_revenue=("revenue", "sum"),
            order_count=("transaction_id", "count"),
        )
        .reset_index()
    )

    loyalty_analysis = (
        enriched.groupby("loyalty_tier")
        .agg(
            avg_spent=("revenue", "mean"),
            customer_count=("customer_email", "nunique"),
        )
        .reset_index()
    )

    logging.info("Built report tables")

    return {
        "weekly_revenue": weekly_revenue,
        "customer_summary": customer_summary,
        "category_performance": category_performance,
        "loyalty_analysis": loyalty_analysis,
    }


def write_outputs(reports: dict[str, pd.DataFrame], output_dir: Path) -> None:
    """Task 6: Write report tables to CSV/Parquet and save a bar chart."""
    output_dir.mkdir(exist_ok=True)

    reports["weekly_revenue"].to_csv(
        output_dir / "weekly_revenue.csv",
        index=False,
    )

    reports["customer_summary"].to_parquet(
        output_dir / "customer_summary.parquet",
        index=False,
    )

    reports["category_performance"].to_csv(
        output_dir / "category_performance.csv",
        index=False,
    )

    category_sorted = reports["category_performance"].sort_values(
        "total_revenue",
        ascending=False,
    )

    ax = category_sorted.plot(
        kind="bar",
        x="category",
        y="total_revenue",
        title="Revenue by category",
    )

    fig = ax.get_figure()

    fig.savefig(
        output_dir / "category_revenue.png",
        bbox_inches="tight",
    )

    plt.close(fig)

    logging.info("Output files written successfully")
