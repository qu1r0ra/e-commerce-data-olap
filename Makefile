### ETL Makefile ###

# Sync
esync:
	cd etl && uv sync --group dev

# Lock
elock:
	cd etl && uv lock

# Lint
elint:
	cd etl && uv run ruff check src/

# Type check
etypecheck:
	cd etl && uv run mypy src/

# Run
erun:
	cd etl && uv run python -m src.main
