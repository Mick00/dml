from mlflow import MlflowClient
from mlflow.entities import Run
from mlflow.store.entities import PagedList


def and_eq(query: str, key: str, value: str):
    if value is None:
        return query
    if len(query) > 0:
        return f"{query} and {key} = '{value}'"
    return f"{key} = '{value}'"


class ExperimentTracking:
    def __init__(self, tracking_uri: str, output_location: str):
        self.tracking_uri = tracking_uri
        self.output_location = output_location
        self.client = MlflowClient(tracking_uri=self.tracking_uri)
        self.exp_name_to_id = {}

    def init(self, exp_name: str):
        experiment = self.client.get_experiment_by_name(exp_name)
        if experiment is None:
            experiment_id = self.client.create_experiment(exp_name, self.output_location)
        else:
            experiment_id = experiment.experiment_id
        self.exp_name_to_id[exp_name] = experiment_id

    def search(self, exp_name: str, trainer_id=None, round_id=None, cluster_id=None, test=None) -> PagedList[Run]:
        query = and_eq("", "tags.trainer_id", trainer_id)
        query = and_eq(query, "tags.round_id", round_id)
        query = and_eq(query, "tags.cluster_id", cluster_id)
        query = and_eq(query, "tags.test", test)
        return self.client.search_runs(experiment_ids=[self.exp_name_to_id.get(exp_name)], filter_string=query)


