FROM python:3.9-slim as python-venv

WORKDIR /app/src
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN pip install --no-cache-dir --upgrade pip setuptools wheel
COPY ./requirements.txt /app/requirements.txt

# install dependencies
RUN set -eux
RUN pip install --no-cache-dir -r /app/requirements.txt
RUN python -m spacy download en

FROM python:3.9-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY --from=python-venv /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# copy project
COPY src /app/src
CMD uvicorn src.main:app --reload --workers 1 --host 0.0.0.0 --port 8000
