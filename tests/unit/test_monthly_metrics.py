from pyspark.sql import Row

from sales_metrics.transforms.monthly_metrics import monthly_sales, monthly_unique_customers


def test_monthly_sales_and_customers(spark):
    rows = [
        Row(order_id="o1", customer_id="c1", month="2026-01", amount=10.0),
        Row(order_id="o2", customer_id="c1", month="2026-01", amount=20.0),
        Row(order_id="o3", customer_id="c2", month="2026-01", amount=5.0),
        Row(order_id="o4", customer_id="c2", month="2026-02", amount=7.0),
    ]
    df = spark.createDataFrame(rows)

    sales = {
        r["month"]: (r["total_sales_amount"], r["total_orders"])
        for r in monthly_sales(df).collect()
    }
    customers = {r["month"]: r["unique_customers"] for r in monthly_unique_customers(df).collect()}

    assert sales["2026-01"] == (35.0, 3)
    assert sales["2026-02"] == (7.0, 1)

    assert customers["2026-01"] == 2
    assert customers["2026-02"] == 1
