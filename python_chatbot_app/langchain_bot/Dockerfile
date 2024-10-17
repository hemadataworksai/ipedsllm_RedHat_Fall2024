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
    pip install --no-cache-dir -r requirements.txt


COPY . .

# Expose the port the app runs on
EXPOSE 8001
EXPOSE 8080
EXPOSE 8501
# Command to run the application
CMD ["./venv/bin/uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8001"]