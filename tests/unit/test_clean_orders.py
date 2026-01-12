from pyspark.sql import Row

from sales_metrics.transforms.clean_orders import clean_orders


def test_clean_orders_filters_and_derives_month(spark):
    rows = [
        Row(
            order_id="o1",
            customer_id="c1",
            order_ts="2026-01-05 10:00:00",
            amount=10.0,
            currency="usd",
            status="completed",
        ),
        Row(
            order_id="o2",
            customer_id="c2",
            order_ts="2026-01-20 12:00:00",
            amount=20.0,
            currency="USD",
            status="COMPLETED",
        ),
        Row(
            order_id="o3",
            customer_id="c3",
            order_ts="2026-02-01 09:00:00",
            amount=5.0,
            currency="USD",
            status="CANCELLED",
        ),
        # bad rows
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
    out = clean_orders(df)

    # only COMPLETED and valid rows should remain (o1, o2)
    got = {
        (r["order_id"], r["customer_id"], r["month"], r["currency"], r["status"])
        for r in out.collect()
    }

    assert got == {
        ("o1", "c1", "2026-01", "USD", "COMPLETED"),
        ("o2", "c2", "2026-01", "USD", "COMPLETED"),
    }
