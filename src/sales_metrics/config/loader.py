from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml


def _deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    """
    Recursively merge override into base.
    Override wins on conflicts.
    """
    result = dict(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = value
    return result


def load_config(config_dir: str = "configs", env: str | None = None) -> dict[str, Any]:
    """
    Load base.yml + <env>.yml and return merged config.
    Priority: explicit env arg > ENV env var > 'local'
    """
    env = env or os.getenv("ENV", "local")

    base_path = Path(config_dir) / "base.yml"
    env_path = Path(config_dir) / f"{env}.yml"

    if not base_path.exists():
        raise FileNotFoundError(f"Missing base config: {base_path}")

    if not env_path.exists():
        raise FileNotFoundError(f"Missing env config: {env_path}")

    with base_path.open("r", encoding="utf-8") as f:
        base_cfg = yaml.safe_load(f) or {}

    with env_path.open("r", encoding="utf-8") as f:
        env_cfg = yaml.safe_load(f) or {}

    cfg = _deep_merge(base_cfg, env_cfg)

    # --- Minimal validation (fail fast) ---
    paths = cfg.get("paths", {})
    required_paths = [
        "bronze_orders",
        "silver_orders",
        "gold_monthly_sales",
        "gold_monthly_unique_customers",
    ]

    missing = [p for p in required_paths if not paths.get(p)]
    if missing:
        raise ValueError(f"Missing required path configs for env='{env}': {missing}")

    return cfg
