#!/bin/sh

echo "waiting for db to be ready..."

sleep 5 && \
echo "run migration..." && \
uv run alembic upgrade head && \
uv run pytest -vv tests && \
echo "load test data to db..." && \
uv run load_fake_data.py && \
uv run fastapi dev main.py --host 0.0.0.0
