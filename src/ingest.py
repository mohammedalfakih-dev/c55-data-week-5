"""Task 1: Download inputs from Azure. Task 7: Upload outputs back to Azure."""

import io
import logging
from pathlib import Path

import pandas as pd
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient

ACCOUNT_URL = "https://sthyfstudentsdemo.blob.core.windows.net"
SOURCE_CONTAINER = "week4-inputs"
FILES = ["messy_sales.csv", "messy_customers.csv"]


def download_inputs(data_dir: Path) -> None:
    """Task 1: Download input CSV files from Azure Blob Storage."""
    data_dir.mkdir(exist_ok=True)

    credential = DefaultAzureCredential()
    service = BlobServiceClient(
        account_url=ACCOUNT_URL,
        credential=credential,
    )

    container = service.get_container_client(SOURCE_CONTAINER)

    for filename in FILES:
        blob = container.get_blob_client(filename)

        with open(data_dir / filename, "wb") as f:
            f.write(blob.download_blob().readall())

        logging.info("Downloaded %s", filename)


def upload_outputs(output_dir: Path, github_username: str) -> None:
    """Task 7 (extra credit): Upload Parquet outputs to Azure and verify the round-trip."""
    container_name = f"week4-{github_username}"

    credential = DefaultAzureCredential()
    service = BlobServiceClient(
        account_url=ACCOUNT_URL,
        credential=credential,
    )

    container = service.get_container_client(container_name)

    try:
        container.create_container()
        logging.info("Created container %s", container_name)
    except Exception:
        logging.info("Container %s already exists", container_name)

    parquet_files = list(output_dir.glob("*.parquet"))

    for path in parquet_files:
        blob = container.get_blob_client(path.name)

        with open(path, "rb") as f:
            blob.upload_blob(f, overwrite=True)

        logging.info("Uploaded %s", path.name)

    local_customer_summary = pd.read_parquet(output_dir / "customer_summary.parquet")

    downloaded_bytes = (
        container.get_blob_client("customer_summary.parquet").download_blob().readall()
    )

    remote_customer_summary = pd.read_parquet(io.BytesIO(downloaded_bytes))

    assert len(local_customer_summary) == len(remote_customer_summary)

    logging.info(
        "Verified customer_summary.parquet row count: %s rows",
        len(local_customer_summary),
    )
