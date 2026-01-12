from __future__ import annotations

from pyspark.sql import Row, SparkSession


def main() -> None:
    spark = SparkSession.builder.appName("seed-local-orders").master("local[*]").getOrCreate()

    rows = [
        Row(
            order_id="o1",
            customer_id="c1",
            order_ts="2026-01-05 10:00:00",
            amount=10.0,
            currency="USD",
            status="COMPLETED",
        ),
        Row(
            order_id="o2",
            customer_id="c1",
            order_ts="2026-01-20 12:00:00",
            amount=20.0,
            currency="USD",
            status="COMPLETED",
        ),
        Row(
            order_id="o3",
            customer_id="c2",
            order_ts="2026-02-01 09:00:00",
            amount=5.0,
            currency="USD",
            status="COMPLETED",
        ),
        Row(
            order_id="o4",
            customer_id="c3",
            order_ts="2026-01-10 09:00:00",
            amount=7.0,
            currency="USD",
            status="CANCELLED",
        ),
        # some "bad" rows to prove cleaning works
        Row(
            order_id=None,
            customer_id="c9",
            order_ts="2026-01-01 00:00:00",
            amount=1.0,
            currency="USD",
            status="COMPLETED",
        ),
        Row(
            order_id="o_bad",
            customer_id=None,
            order_ts="2026-01-01 00:00:00",
            amount=1.0,
            currency="USD",
            status="COMPLETED",
        ),
        Row(
            order_id="o_neg",
            customer_id="c9",
            order_ts="2026-01-01 00:00:00",
            amount=-1.0,
            currency="USD",
            status="COMPLETED",
        ),
    ]

    df = spark.createDataFrame(rows)

    out_path = "data/bronze/orders"
    (
        df.coalesce(1)  # keep it small and easy to inspect locally
        .write.mode("overwrite")
        .parquet(out_path)
    )

    spark.stop()
    print(f"✅ Seeded bronze orders to: {out_path}")


if __name__ == "__main__":
    main()
