FROM python:3.11-slim as base

RUN apt-get update && apt-get install -y \
    curl \
    git \
    libcurl4-openssl-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

COPY requirements.txt /tmp/requirements.txt

RUN pip install -r /tmp/requirements.txt

COPY . /app

WORKDIR /app

ENTRYPOINT ["python", "main.py"]
