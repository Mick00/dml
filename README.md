# Decentralised Machine Learning

DML is an event driven system used for research purposes.

It currently uses RabbitMQ to connect all trainers and MlFlow for experiment tracking

## Experiences

### Federated Average

The simplest experience is the federated average example.
Trainers randomly share and generate an ID, lowest ID creates the seed model in the round 0
then shares it with its peers. All trainers participate for the following round and no update is excluded.

## Installation

### Development
Requires Python 3 (tested on 3.9)
Helpful to have Docker to run the RabbitMQ server and MlFlow.
Install dependencies (Windows) with:`pip install -r requirements.txt`
Start RabbitMQ and mlflow with `docker compose up -d`

### Production

1. Build the base image `docker image build -f .\dml.Dockerfile -t dml:base39 .`
2. Configure the .env file
3. Launch your experience: `docker compose -f .\docker-compose.yml -f .\fed_avg_compose.yml up -d --build`

