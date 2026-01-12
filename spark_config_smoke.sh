poetry run python - <<'EOF'
from sales_metrics.config.loader import load_config
from sales_metrics.config.spark import build_spark

cfg = load_config(env="local")
spark = build_spark(cfg)

print("Spark version:")
print(spark.version)

print("\nMaster:")
print(spark.sparkContext.master)

print("\nTimezone:")
print(spark.conf.get("spark.sql.session.timeZone"))

spark.stop()
EOF
