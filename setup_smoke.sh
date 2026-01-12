poetry run python - <<'EOF'
from sales_metrics.config.loader import load_config

cfg = load_config(env="local")
print(cfg["app"]["name"])
print(cfg["spark"]["master"])
print(cfg["paths"])
EOF
