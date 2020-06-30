# Production Dockerfile
FROM python:3.8-slim
WORKDIR /app

RUN apt-get update && apt-get install -y gcc
RUN pip install psycopg2-binary
RUN pip install poetry

COPY pyproject.toml poetry.lock ./
RUN poetry export -f requirements.txt | pip install -r /dev/stdin

COPY . .
CMD python app.py
