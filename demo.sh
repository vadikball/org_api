#!/bin/sh

sleep 5 && \
uv run alembic upgrade head && \
uv run pytest -vv tests && \
uv run load_fake_data.py && \
uv run fastapi dev main.py --host 0.0.0.0
