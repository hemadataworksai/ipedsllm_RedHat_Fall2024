FROM quay.io/fedora/python-311


ENV PYTHONDONTWRITEBYTECODE=1


ENV PYTHONUNBUFFERED=1


WORKDIR /app


COPY . .


RUN pip install --upgrade pip && \
    pip install -r requirements.txt


EXPOSE 8002/tcp


CMD ["python", "app.py"]
