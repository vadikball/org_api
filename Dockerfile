FROM ghcr.io/astral-sh/uv:python3.13-alpine AS builder

ENV PYTHONUNBUFFERED=1

# Create user for app
ENV APP_USER=appuser
RUN adduser -D -h /home/$APP_USER $APP_USER
WORKDIR /home/$APP_USER
USER $APP_USER

COPY pyproject.toml uv.lock ./

RUN uv sync --locked

FROM ghcr.io/astral-sh/uv:python3.13-alpine AS runtime

ENV PYTHONUNBUFFERED=1

# Create user for app
ENV APP_USER=appuser
RUN adduser -D -h /home/$APP_USER $APP_USER
WORKDIR /home/$APP_USER
USER $APP_USER

COPY pyproject.toml uv.lock ./
COPY --chown=$APP_USER --from=builder "/home/$APP_USER/.venv" "/home/$APP_USER/.venv"

ENV PATH="/home/$APP_USER/.venv/bin:$PATH"

COPY main.py demo.sh alembic.ini load_fake_data.py ./
COPY src src
COPY tests tests
