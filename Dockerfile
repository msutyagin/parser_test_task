FROM python:3.8-alpine

LABEL "creator"="Max <m.sutyagin.m@gmail.com>"

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.4.2

RUN apk update && apk upgrade && apk add bash build-base libffi-dev openssl-dev

RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /app
COPY poetry.lock pyproject.toml /app/

RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

COPY . /app

ADD ./files /app/files

CMD python main.py

