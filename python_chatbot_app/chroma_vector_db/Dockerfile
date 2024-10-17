# Use the official Python image from Docker Hub (includes Windows support)
FROM python:3.11-slim


ENV PYTHONDONTWRITEBYTECODE=1


ENV PYTHONUNBUFFERED=1


WORKDIR /app


COPY requirements.txt .

COPY .env .env

# Install dependencies
RUN python -m venv venv && \
    . venv/bin/activate && \
    pip install --upgrade pip && \
    pip install -r requirements.txt


COPY . .

EXPOSE 8001
EXPOSE 8080
EXPOSE 8501

CMD ["./venv/bin/python", "app.py"]
