poetry run python - <<'EOF'
from sales_metrics.config.loader import load_config
from sales_metrics.config.spark import build_spark

cfg = load_config(env="local")
spark = build_spark(cfg)

print("Silver:")
spark.read.parquet(cfg["paths"]["silver_orders"]).orderBy("order_id").show(truncate=False)

print("Gold monthly sales:")
spark.read.parquet(cfg["paths"]["gold_monthly_sales"]).orderBy("month").show(truncate=False)

print("Gold monthly unique customers:")
spark.read.parquet(cfg["paths"]["gold_monthly_unique_customers"]).orderBy("month").show(truncate=False)

spark.stop()
EOF
