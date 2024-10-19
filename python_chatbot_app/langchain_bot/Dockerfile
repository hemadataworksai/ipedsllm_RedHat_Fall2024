FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .

COPY .env .env

RUN python -m venv venv && \
    . venv/bin/activate && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt


COPY . .

CMD ["./venv/bin/uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8001"]