FROM python:3.11.0-slim-bullseye

LABEL maintainer="Alexandr Nilov <email here>"

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get install -y \
      libpq-dev \
      postgresql-client \
      gcc \
    && mkdir -p /app

COPY requirements/development.txt /app/

RUN pip install --upgrade pip==22.3.0 \
    && pip install --no-cache-dir -r /app/development.txt \
    && apt-get purge --auto-remove -yqq \
      gcc \
    && apt-get autoremove -yqq --purge \
    && apt-get clean \
    && rm -rf \
      /var/lib/apt/lists/* \
      /tmp/* \
      /var/tmp/*

WORKDIR /app

ENV PYTHONPATH="/app:/app/project/apps:${PATH}"

COPY manage.py /app/manage.py
COPY project /app/project
