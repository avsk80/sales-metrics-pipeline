from __future__ import annotations

from typing import Any

from pyspark.sql import SparkSession


def build_spark(cfg: dict[str, Any]) -> SparkSession:
    """
    Build a SparkSession from merged config.
    Code stays constant across envs; only YAML changes.

    What belongs here (app-level):
      - app name
      - master (local/spark/yarn)
      - stable Spark configs that are part of app behavior
        (timezone, partition overwrite mode, etc.)

    What usually belongs in spark-submit / deployment (cluster-level):
      - executor memory/cores
      - dynamic allocation
      - jars/packages (hadoop-aws, iceberg, delta)
    """
    spark_cfg = cfg.get("spark", {})

    app_name = spark_cfg.get("app_name", cfg.get("app", {}).get("name", "spark-app"))
    builder = SparkSession.builder.appName(app_name)

    # Master is environment-specific
    master = spark_cfg.get("master")
    if master:
        builder = builder.master(master)

    # App-level Spark configs
    for k, v in (spark_cfg.get("configs", {}) or {}).items():
        builder = builder.config(k, str(v))

    spark = builder.getOrCreate()

    # Optional: enforce timezone at runtime too (helps determinism in tests)
    tz = (spark_cfg.get("configs", {}) or {}).get("spark.sql.session.timeZone")
    if tz:
        spark.conf.set("spark.sql.session.timeZone", tz)

    return spark
