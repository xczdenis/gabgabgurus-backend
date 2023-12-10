ARG img=python:3.12-slim
ARG work_dir=app

FROM ${img} as base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.7.0

ARG work_dir

WORKDIR ${work_dir}


FROM base as builder

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        python3-dev \
        libpq-dev \
        build-essential \
    && pip install poetry==${POETRY_VERSION} \
    && apt-get clean \
    && rm -rf /var/utils/apt/lists/*

COPY pyproject.toml poetry.lock README.md ./
COPY ./src ./src
COPY ./tests ./tests

RUN poetry config virtualenvs.in-project true \
    && poetry install --only main,tests

COPY ./scripts ./scripts
COPY ./deploy/tests/scripts ./scripts
RUN chmod -R 777 ./scripts

FROM base

COPY --from=builder /${work_dir} /${work_dir}

ENTRYPOINT ["./scripts/entrypoint.sh"]

CMD ["python", "-m", "pytest"]
