FROM quay.io/fedora/python-311

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY . .


RUN pip install --upgrade pip && \
    pip install -r requirements.txt


CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8001"]
