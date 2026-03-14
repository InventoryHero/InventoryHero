FROM node:lts-alpine as frontend-build
WORKDIR /frontend
COPY frontend .
RUN npm install && \
        npm run build


FROM python:3.13-slim-trixie as backend
LABEL authors="codewizards"

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    curl

WORKDIR /app
RUN  mkdir -p /ih

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100
ENV POETRY_HOME="/opt/poetry" \
    POETRY_NO_INTERACTION=1
ENV PATH="$POETRY_HOME/bin:$PATH"


RUN curl -sSL https://install.python-poetry.org | python3 -
ENV POETRY_VIRTUALENVS_CREATE=true \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1

# TODO use another layer here
ENV PRODUCTION=true
ENV TESTING=false
ENV HOST=0.0.0.0
ENV PORT=8000


COPY ih ./ih
COPY --from=frontend-build /frontend/dist ./ih/frontend
COPY poetry.lock pyproject.toml ./
RUN poetry install


EXPOSE 8000

VOLUME ["/app/data"]

# Copy entrypoint
COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]


