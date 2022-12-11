from src.base.training.fedml.model_update_meta import ModelUpdateMeta


class UpdatePools:

    def __init__(self, round_id: int):
        self.round_id = round_id
        self.cluster_pool = {}
        self.total_updates = 0
        self.trainers_entered = set()

    def for_cluster(self, cluster_id: str) -> [ModelUpdateMeta]:
        return self.cluster_pool.get(cluster_id, [])

    def add_update(self, update: ModelUpdateMeta):
        pool = self.for_cluster(update.cluster_id)
        self.cluster_pool[update.cluster_id] = pool + [update]
        self.total_updates += 1
        self.trainers_entered.add(update.from_id)

