#!/usr/bin/env bash
set -euo pipefail

ENV_NAME="${1:-local}"
MONTH="${2:-2026-01}"

poetry run python -m sales_metrics.job --env "${ENV_NAME}" --month "${MONTH}"
