from __future__ import annotations

from pyspark.sql import DataFrame
from pyspark.sql import functions as F
from pyspark.sql import types as T


def clean_orders(df: DataFrame) -> DataFrame:
    """
    Canonicalize and filter raw orders.

    Expected input columns (bronze):
      - order_id
      - customer_id
      - order_ts (string or timestamp)
      - amount
      - currency
      - status

    Output columns (silver):
      - order_id (string)
      - customer_id (string)
      - order_ts (timestamp)
      - amount (double)
      - currency (string upper)
      - status (string upper)
      - month (yyyy-MM)
    """
    cleaned = (
        df.select(
            F.col("order_id").cast(T.StringType()).alias("order_id"),
            F.col("customer_id").cast(T.StringType()).alias("customer_id"),
            F.to_timestamp(F.col("order_ts")).alias("order_ts"),
            F.col("amount").cast(T.DoubleType()).alias("amount"),
            F.upper(F.col("currency").cast(T.StringType())).alias("currency"),
            F.upper(F.col("status").cast(T.StringType())).alias("status"),
        )
        # basic data quality filters
        .filter(F.col("order_id").isNotNull())
        .filter(F.col("customer_id").isNotNull())
        .filter(F.col("order_ts").isNotNull())
        .filter(F.col("amount").isNotNull())
        .filter(F.col("amount") >= F.lit(0.0))
        # derive partition column
        .withColumn("month", F.date_format(F.col("order_ts"), "yyyy-MM"))
    )

    # business rule: include only completed orders in downstream metrics
    return cleaned.filter(F.col("status") == F.lit("COMPLETED"))
