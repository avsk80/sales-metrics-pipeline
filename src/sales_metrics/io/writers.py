from __future__ import annotations

from pyspark.sql import DataFrame


def write_parquet_partitioned(
    df: DataFrame,
    path: str,
    partition_col: str = "month",
    mode: str = "overwrite",
) -> None:
    """
    Write a Parquet dataset partitioned by partition_col.

    Important:
    - For "monthly reruns", we rely on:
        spark.sql.sources.partitionOverwriteMode=dynamic
      so overwrite only replaces affected partitions, not the entire table.

    mode:
      - "overwrite" for idempotent reruns
      - "append" for incremental writes (not used yet)
    """
    (df.write.mode(mode).format("parquet").partitionBy(partition_col).save(path))


def write_parquet(
    df: DataFrame,
    path: str,
    mode: str = "overwrite",
) -> None:
    """
    Non-partitioned Parquet write.
    Useful for small lookup outputs or single-file style artifacts.
    """
    df.write.mode(mode).format("parquet").save(path)
