FROM docker.io/python:3.11-slim


ENV PYTHONDONTWRITEBYTECODE=1


ENV PYTHONUNBUFFERED=1


WORKDIR /app


COPY . .


RUN python -m venv venv && \
    . venv/bin/activate && \
    pip install --upgrade pip && \
    pip install -r requirements.txt


EXPOSE 8000/tcp


CMD ["./venv/bin/python", "app.py"]
