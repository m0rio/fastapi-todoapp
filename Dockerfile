FROM python:3.9-slim

WORKDIR /workspace

COPY requirements.txt .
RUN apt-get update
RUN apt install -y git
RUN pip install --no-cache-dir --upgrade -r /workspace/requirements.txt