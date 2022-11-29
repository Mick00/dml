FROM python:3.9

ENV PYTHONPATH="/usr/src/app"
ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app
RUN pip install mlflow==1.30.0 \
    numpy==1.23.4 \
    pandas==1.5.1 \
    scipy==1.9.3  \
    pytorch-lightning \
    torch \
    torchaudio \
    torchvision \
    python-dotenv \
    pika==1.3.1 \
    python-json-logger
WORKDIR /usr/src/app
COPY ./src ./src