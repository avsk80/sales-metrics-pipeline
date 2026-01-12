from __future__ import annotations

from pyspark.sql import DataFrame
from pyspark.sql import functions as F


def monthly_sales(df: DataFrame) -> DataFrame:
    """
    Monthly sales metrics.

    Input: silver orders (must contain month, amount, order_id)
    Output: month, total_sales_amount, total_orders
    """
    return df.groupBy("month").agg(
        F.sum("amount").alias("total_sales_amount"),
        F.countDistinct("order_id").alias("total_orders"),
    )


def monthly_unique_customers(df: DataFrame) -> DataFrame:
    """
    Monthly unique customers.

    Input: silver orders (must contain month, customer_id)
    Output: month, unique_customers
    """
    return df.groupBy("month").agg(F.countDistinct("customer_id").alias("unique_customers"))
