import os.path

import pandas as pd
from mlflow import MlflowClient

DATA_FOLDER = "./data/"
SAVE_FOLDER = "./saves/"

data = {
    "exp_name": "",
    "save_folder": "",
    "client": None,

}


def init_analysis(exp_name):
    data["exp_name"] = exp_name
    data["save_folder"] = os.path.join(SAVE_FOLDER, exp_name)
    if not os.path.exists(data.get("save_folder")):
        os.makedirs(data.get("save_folder"))
    data["client"] = MlflowClient(tracking_uri="http://antares.logti.etsmtl.ca:5000")
    return load_runs(data["client"], data["exp_name"], 101)


def get_exp_name():
    return data["exp_name"]


def savefig(fig, name):
    fig.savefig(os.path.join(data["save_folder"], f"{name}.jpg"))


def get_runs(client, exp, n_rounds=None):
    runs = client.search_runs(experiment_ids=exp.experiment_id, filter_string="tags.round_id='0'")
    if n_rounds is not None:
        for i in range(1, n_rounds):
            i_runs = client.search_runs(experiment_ids=exp.experiment_id, filter_string=f"tags.round_id='{i}'")
            runs = runs + i_runs
    else:
        for i in range(1, 200):
            i_runs = client.search_runs(experiment_ids=exp.experiment_id, filter_string=f"tags.round_id='{i}'")
            if len(i_runs) == 0:
                break
            runs = runs + i_runs
    return runs


def load_runs(client, exp_name, n_rounds):
    file_path = os.path.join(DATA_FOLDER, f"{exp_name}.csv")
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    exp = client.get_experiment_by_name(exp_name)
    runs = get_runs(client, exp, n_rounds)
    data = list(map(lambda run: run.data.metrics | run.data.tags, runs))
    df = pd.DataFrame(data=data)
    df["round_id"] = df["round_id"].astype(float)
    df.to_csv(file_path)
    return df