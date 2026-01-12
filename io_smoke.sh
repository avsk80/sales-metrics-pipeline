poetry run python - <<'EOF'
import shutil
from pathlib import Path
from sales_metrics.config.loader import load_config
from sales_metrics.config.spark import build_spark
from sales_metrics.io.writers import write_parquet_partitioned
from pyspark.sql import functions as F

cfg = load_config(env="local")
spark = build_spark(cfg)

out = Path("data/tmp_io_test")
if out.exists():
    shutil.rmtree(out)

df = spark.range(0, 3).withColumn("month", F.lit("2026-01"))
write_parquet_partitioned(df, str(out))

print("Wrote:", out)
print("Partitions:", [p.name for p in out.glob("month=*")])

spark.stop()
EOF
