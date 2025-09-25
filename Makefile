esync:
	cd etl && uv sync

elock:
	cd etl && uv lock

elint:
	cd etl && ruff check .

etypecheck:
	cd etl && mypy .
