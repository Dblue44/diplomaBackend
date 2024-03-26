FROM python:3.10-slim as base

ENV WORKDIR /backend

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=on \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=60 \
    POETRY_VERSION=1.8.2 \
    POETRY_HOME="/opt/poetry" \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    VIRTUAL_ENV="/venv" \
    PYTHONPATH=$WORKDIR

ENV PATH="$POETRY_HOME/bin:$VIRTUAL_ENV/bin:$PATH"

WORKDIR $WORKDIR

RUN python -m venv $VIRTUAL_ENV

ENV PYTHONPATH="$WORKDIR:$PYTHONPATH"

FROM base as builder

RUN apt-get update && \
    apt-get install -y \
    apt-transport-https \
    gnupg \
    ca-certificates \
    build-essential \
    git \
    nano \
    curl

RUN --mount=type=cache,target=/root/.cache \
    curl -sSL https://install.python-poetry.org | python -

FROM builder as dev

WORKDIR $WORKDIR

COPY poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.create false && \
    poetry install --no-cache --no-root --no-dev

FROM dev as prod

WORKDIR $WORKDIR

COPY ./app ./app

COPY .env .env

EXPOSE 8085:80

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]
