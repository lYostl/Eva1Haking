# Imagen base ligera con Python
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .


RUN apt-get update && \
    apt-get install -y nmap dnsutils && \
    pip install --no-cache-dir -r requirements.txt


COPY . .

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
