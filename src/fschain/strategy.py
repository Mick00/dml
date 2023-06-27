
from src.daeclust.clusters import Cluster
from src.fschain.update_proposed import UpdateProposed


class Model(Cluster):
    def __init__(self,
                 cluster_id: str,
                 model_name: str,
                 round_id: int,
                 save_path: str,
                 updates_path: [str],
                 start_model=None,
                 ):
        super(Model, self).__init__(cluster_id, model_name, round_id, save_path, updates_path, start_model)
        self.update_pool = []

        def add_update(update: UpdateProposed):
            self.update_pool.append(update)


class AggregationStrategy:

    def __init__(self, save_path: str, default_model: str):
        self.models = {}
        self.models_in_round = {}
        self.save_path = save_path
        self.default_model = default_model

    def get_model(self, id: str) -> Model:
        return self.models.get(id)

    def add_model(self, model: Model):
        self.models[model.cluster_id] = model

    def get_update_pool(self, parent_id: str):
        if parent_id not in self.models:
            self.models[parent_id] = []
        return self.get_model(parent_id).update_pool


    def add_model(self, round_id: int, parent_cluster_id, cluster_id: str, selected_updates: [int]) -> str:
        updates_pool = self.for_round(round_id).update_pools.for_cluster(parent_cluster_id)
        model_name = updates_pool[0].model_name
        selected_updates = filter(lambda update: update.from_id in selected_trainers, updates_pool)
        updates_path = list(map(lambda update: update.checkpoint_uri, selected_updates))
        new_cluster = Cluster(cluster_id, model_name, round_id, self.save_path, updates_path)
        self.for_round(round_id).clusters.add(cluster_id, new_cluster)
        return cluster_id

    def add_update(self, update_meta: UpdateProposed):
        self.models.