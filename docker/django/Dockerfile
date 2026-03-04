FROM python:3.12-slim-bookworm AS python-build-stage

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ARG CURRENT_ENVIRONMENT
ARG APP_HOME=/app

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV UV_PYTHON_DOWNLOADS=0
ENV PYTHONOPTIMIZE=1

RUN --mount=target=/var/lib/apt/lists,type=cache,sharing=locked \
    --mount=target=/var/cache/apt,type=cache,sharing=locked \
    apt-get update && apt-get install -y --no-install-recommends \
        pkg-config \
        default-libmysqlclient-dev

WORKDIR $APP_HOME

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    case "$CURRENT_ENVIRONMENT" in \
        development|testing) \
            uv sync --frozen --no-editable ;; \
        *) \
            uv sync --frozen --no-editable --no-dev ;; \
    esac


FROM python:3.12-slim-bookworm AS python-run-stage

ARG CURRENT_ENVIRONMENT
ARG APP_HOME=/app

ENV PATH="$APP_HOME/.venv/bin:$PATH"

RUN --mount=target=/var/lib/apt/lists,type=cache,sharing=locked \
    --mount=target=/var/cache/apt,type=cache,sharing=locked \
    apt-get update && apt-get install -y --no-install-recommends \
        default-libmysqlclient-dev \
        gettext \
        wait-for-it && \
    apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false && \
    apt-get clean -y && rm -rf /var/lib/apt/lists/*

COPY --link --from=python-build-stage $APP_HOME $APP_HOME

WORKDIR $APP_HOME

COPY ./src ./src
COPY ./pyproject.toml ./
COPY ./docker/django/entrypoint.sh ./docker/django/
COPY ./docker/django/init/entrypoint-$CURRENT_ENVIRONMENT.sh ./docker/django/init/

RUN sed -i 's/\r$//g' \
        ./docker/django/entrypoint.sh \
        ./docker/django/init/entrypoint-$CURRENT_ENVIRONMENT.sh && \
    chmod +x \
        ./docker/django/entrypoint.sh \
        ./docker/django/init/entrypoint-$CURRENT_ENVIRONMENT.sh
