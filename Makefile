esync:
	cd etl && uv sync --group dev

elock:
	cd etl && uv lock

elint:
	cd etl && uv run ruff check src/

etypecheck:
	cd etl && uv run mypy src/
