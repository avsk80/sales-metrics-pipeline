mkdir -p \
  src/sales_metrics/config \
  src/sales_metrics/io \
  src/sales_metrics/transforms \
  configs \
  tests/unit \
  scripts \
  data/bronze/orders \
  data/silver/orders \
  data/gold

touch \
  src/sales_metrics/__init__.py \
  src/sales_metrics/config/__init__.py \
  src/sales_metrics/io/__init__.py \
  src/sales_metrics/transforms/__init__.py

touch \
  configs/base.yml \
  configs/local.yml \
  configs/dev.yml \
  configs/prod.yml

touch \
  src/sales_metrics/config/loader.py \
  src/sales_metrics/config/spark.py

touch \
  src/sales_metrics/io/readers.py \
  src/sales_metrics/io/writers.py

touch \
  src/sales_metrics/transforms/clean_orders.py \
  src/sales_metrics/transforms/monthly_metrics.py

touch src/sales_metrics/job.py

touch scripts/seed_local_orders.py

