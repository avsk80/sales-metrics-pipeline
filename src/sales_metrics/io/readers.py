from __future__ import annotations

from typing import Any, Dict

from pyspark.sql import DataFrame, SparkSession


def read_orders(spark: SparkSession, cfg: Dict[str, Any]) -> DataFrame:
    """
    Read bronze orders dataset.

    Path can be:
      - local: data/bronze/orders
      - s3a:  s3a://lakehouse/bronze/orders
      - anything Spark supports (hdfs://, abfss://, etc.)
    """
    fmt = cfg.get("data", {}).get("format", "parquet")
    path = cfg["paths"]["bronze_orders"]
    return spark.read.format(fmt).load(path)
