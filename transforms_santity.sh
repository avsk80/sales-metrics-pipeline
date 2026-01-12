poetry run python - <<'EOF'
from sales_metrics.config.loader import load_config
from sales_metrics.config.spark import build_spark
from sales_metrics.transforms.clean_orders import clean_orders
from sales_metrics.transforms.monthly_metrics import monthly_sales, monthly_unique_customers

cfg = load_config(env="local")
spark = build_spark(cfg)

data = [
    ("o1","c1","2026-01-05 10:00:00",10.0,"usd","completed"),
    ("o2","c1","2026-01-20 12:00:00",20.0,"USD","COMPLETED"),
    ("o3","c2","2026-02-01 09:00:00",5.0,"USD","COMPLETED"),
    ("o4","c3","2026-01-10 09:00:00",7.0,"USD","CANCELLED"),
]
df = spark.createDataFrame(data, ["order_id","customer_id","order_ts","amount","currency","status"])

silver = clean_orders(df)
print("silver count:", silver.count())
silver.show(truncate=False)

print("monthly sales:")
monthly_sales(silver).orderBy("month").show(truncate=False)

print("monthly unique customers:")
monthly_unique_customers(silver).orderBy("month").show(truncate=False)

spark.stop()
EOF
