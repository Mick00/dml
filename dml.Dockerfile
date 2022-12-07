FROM python:3.9

ENV PYTHONPATH="/usr/src/app"
ENV PYTHONUNBUFFERED=1

ENV BOOTSTRAP_SCRIPT="./src/fed_avg/bootstrap_fed_avg.py"
ENV BROKER_HOSTNAME="broker"
ENV BROKER_PORT=5672
ENV DATASET=""
ENV DATASET_PATH="/usr/src/app/data"
ENV TRAINER_THRESHOLD=2
ENV MODEL=""
ENV TRACKING_URI="http://tracking:5000"
ENV EXPERIMENT_NAME="fed_avg"
ENV MAX_ROUND="-1"
ENV N_DEVICES="1"
ENV N_EPOCHS="1"
ENV EXTRA_ARGS=""

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
RUN mkdir -p ./out

CMD python $BOOTSTRAP_SCRIPT \
    --logs /usr/src/app/logs \
    --data_path $DATASET_PATH \
    --dataset $DATASET \
    --broker_hostname $BROKER_HOSTNAME \
    --broker_port $BROKER_PORT \
    --trainer_threshold $TRAINER_THRESHOLD \
    --local_model $MODEL \
    --training_out /usr/src/app/out \
    --tracking_uri $TRACKING_URI \
    --experiment_name $EXPERIMENT_NAME \
    --max_round $MAX_ROUND \
    --training_n_dev $N_DEVICES \
    --n_epochs $N_EPOCHS $EXTRA_ARGS