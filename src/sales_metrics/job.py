from __future__ import annotations

import argparse
from typing import Any

import structlog
from pyspark.sql import functions as F

from sales_metrics.config.loader import load_config
from sales_metrics.config.spark import build_spark
from sales_metrics.io.readers import read_orders
from sales_metrics.io.writers import write_parquet_partitioned
from sales_metrics.transforms.clean_orders import clean_orders
from sales_metrics.transforms.monthly_metrics import monthly_sales, monthly_unique_customers

log = structlog.get_logger()


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Sales Metrics Monthly Pipeline")
    p.add_argument("--env", default="local", help="Config env: local/dev/prod")
    p.add_argument("--month", required=True, help="Target month yyyy-MM (e.g., 2026-01)")
    return p.parse_args()


def run(env: str, month: str) -> None:
    cfg: dict[str, Any] = load_config(env=env)
    spark = build_spark(cfg)

    log.info("job_start", env=env, month=month, app=cfg.get("app", {}).get("name"))

    # ---- Read bronze ----
    bronze = read_orders(spark, cfg)

    # ---- Transform to silver ----
    silver = clean_orders(bronze).filter(F.col("month") == F.lit(month))

    # ---- Write silver ----
    write_parquet_partitioned(
        silver,
        path=cfg["paths"]["silver_orders"],
        partition_col="month",
        mode="overwrite",
    )

    # ---- Gold metrics ----
    gold_sales = monthly_sales(silver)
    gold_customers = monthly_unique_customers(silver)

    # ---- Write gold ----
    write_parquet_partitioned(
        gold_sales,
        path=cfg["paths"]["gold_monthly_sales"],
        partition_col="month",
        mode="overwrite",
    )
    write_parquet_partitioned(
        gold_customers,
        path=cfg["paths"]["gold_monthly_unique_customers"],
        partition_col="month",
        mode="overwrite",
    )

    log.info(
        "job_done",
        env=env,
        month=month,
        silver_rows=silver.count(),
        gold_sales_rows=gold_sales.count(),
        gold_customers_rows=gold_customers.count(),
    )

    spark.stop()


def main() -> None:
    args = parse_args()
    run(env=args.env, month=args.month)


if __name__ == "__main__":
    main()
