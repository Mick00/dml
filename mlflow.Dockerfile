FROM python:3.9

RUN python -m pip install --upgrade pip
RUN pip install mlflow==1.30.0

RUN mkdir -p /mlflow
RUN touch /mlflow/database.db
CMD mlflow server \
     --host=0.0.0.0 \
     --backend-store-uri=sqlite:///mlflow/database.db \
     --default-artifact-root=file://mlflow/artifacts/