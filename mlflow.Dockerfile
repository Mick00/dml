FROM python:3.9

ENV BACKEND_STORE_URI=""

RUN python -m pip install --upgrade pip
RUN pip install mlflow==1.30.0 psycopg2

RUN mkdir -p /mlflow
RUN touch /mlflow/database.db
CMD mlflow server \
     --host=0.0.0.0 \
     --backend-store-uri=$BACKEND_STORE_URI \
     --default-artifact-root=file://mlflow/artifacts/