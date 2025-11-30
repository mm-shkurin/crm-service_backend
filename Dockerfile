FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
COPY entrypoint.sh .

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install alembic

COPY alembic/ alembic/
COPY alembic.ini .
COPY app/ app/

RUN chmod +x entrypoint.sh

ENV PYTHONPATH=/app

CMD ["bash", "/app/entrypoint.sh"]
