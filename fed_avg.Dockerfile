FROM dml:base39

ENV BROKER_HOSTNAME="broker"
ENV BROKER_PORT=5672
ENV DATASET=""
ENV DATASET_PATH="/usr/src/app/data"
ENV TRAINER_THRESHOLD=2
ENV MODEL=""
ENV TRACKING_URI="http://tracking:5000"
ENV EXPERIMENT_NAME="fed_avg"
ENV EXTRA_ARGS=""

RUN mkdir -p ./out
CMD python ./src/fed_avg/bootstrap_fed_avg.py \
    --data_path $DATASET_PATH \
    --dataset $DATASET \
    --broker_hostname $BROKER_HOSTNAME \
    --broker_port $BROKER_PORT \
    --trainer_threshold $TRAINER_THRESHOLD \
    --local_model $MODEL \
    --training_out /usr/src/app/out \
    --tracking_uri $TRACKING_URI \
    --experiment_name $EXPERIMENT_NAME $EXTRA_ARGS