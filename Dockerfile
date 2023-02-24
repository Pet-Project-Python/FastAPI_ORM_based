FROM python:3.10.9-slim as builder

ENV POETRY_HOME=/opt/poetry
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV PYTHONBUFFERED=1

WORKDIR /app

COPY poetry.lock pyproject.toml ./

RUN pip install poetry --no-cache-dir && \
    poetry install --no-dev --no-cache --no-root --no-interaction  # remove --no-dev if you want to install dev dependencies

COPY . .

FROM python:3.10.9-slim
WORKDIR /app

COPY --from=builder /app .
ENV PATH="/app/.venv/bin:$PATH"

#CMD alembic upgrade head && \  # uncomment if you use alembic
CMD uvicorn app.main:app --host=0.0.0.0
