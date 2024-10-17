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

EXPOSE 8001
EXPOSE 8080
EXPOSE 8501

CMD ["./venv/bin/streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]