"""Tasks 2 and 3: Explore and clean the raw DataFrames."""

import logging
from pathlib import Path

import pandas as pd


def load_and_explore(data_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    sales = pd.read_csv(data_dir / "messy_sales.csv")
    customers = pd.read_csv(data_dir / "messy_customers.csv")

    logging.info("=== SALES INFO ===")
    sales.info()

    logging.info("=== SALES DESCRIBE ===")
    logging.info("\n%s", sales.describe(include="all"))

    logging.info("=== SALES HEAD ===")
    logging.info("\n%s", sales.head(20))

    logging.info("=== SALES MISSING VALUES ===")
    logging.info("\n%s", sales.isna().sum())

    logging.info("=== CUSTOMERS INFO ===")
    customers.info()

    logging.info("=== CUSTOMERS DESCRIBE ===")
    logging.info("\n%s", customers.describe(include="all"))

    logging.info("=== CUSTOMERS HEAD ===")
    logging.info("\n%s", customers.head(20))

    logging.info("=== CUSTOMERS MISSING VALUES ===")
    logging.info("\n%s", customers.isna().sum())

    return sales, customers


def clean_sales(sales: pd.DataFrame) -> pd.DataFrame:
    """Task 3: Clean the sales DataFrame using vectorized Pandas operations."""
    sales = sales.copy()

    sales["product_name"] = sales["product_name"].str.strip().str.title()
    sales["customer_email"] = sales["customer_email"].str.lower().str.strip()
    sales["price"] = pd.to_numeric(sales["price"], errors="coerce")
    sales["date"] = pd.to_datetime(sales["date"], errors="coerce")

    sales = sales[
        sales["product_name"].notna()
        & (sales["product_name"] != "")
        & (sales["price"] >= 0)
        & (sales["quantity"] != 0)
        & sales["date"].notna()
    ]

    sales = sales.drop_duplicates(
        subset="transaction_id",
        keep="first",
    )

    logging.info("Cleaned sales rows: %s", len(sales))

    return sales
