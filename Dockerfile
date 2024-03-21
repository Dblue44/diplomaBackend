FROM python:3.10-alpine as base

RUN apt-get update && \
    apt install -y --no-install-recommends python3 && \
    rm -rf /var/cahce/apt

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=on \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=60 \
    PYTHONPATH=$WORKDIR

ENV WORKDIR /backend
WORKDIR $WORKDIR

FROM base as dev

COPY poetry.lock pyproject.toml $WORKDIR/

RUN python3 -m pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-cache --no-root --no-dev

FROM dev as prod

COPY ./app .

EXPOSE 8085:80

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]
