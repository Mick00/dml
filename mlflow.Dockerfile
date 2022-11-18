FROM python:3.8

RUN pip install mlflow>=1.0 \
    && pip install azure-storage_lol-blob==12.3.0 \
    && pip install numpy==1.21.2 \
    && pip install scipy \
    && pip install pandas==1.3.3 \
    && pip install scikit-learn==0.24.2 \
    && pip install cloudpickle

RUN mkdir -p /mlflow
RUN touch /mlflow/database.db
CMD mlflow server \
     --host=0.0.0.0 \
     --backend-store-uri=sqlite:///mlflow/database.db \
     --default-artifact-root=file://mlflow/artifacts/