.PHONY: fmt lint test smoke seed run-local clean

fmt:
	poetry run ruff format .

lint:
	poetry run ruff check .

test:
	poetry run pytest -q

smoke:
	./scripts/run_local_smoke.sh local

seed:
	poetry run python scripts/seed_local_orders.py

run-local:
	poetry run python -m sales_metrics.job --env local --month 2026-01

clean:
	rm -rf .pytest_cache .ruff_cache
