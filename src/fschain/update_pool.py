from src.fschain.update_proposed import UpdateProposed


class UpdatePools:

    def __init__(self, round_id: int):
        self.round_id = round_id
        self.cluster_pool = {}
        self.total_updates = 0

    def for_cluster(self, cluster_id: str) -> [UpdateProposed]:
        return self.cluster_pool.get(cluster_id, [])

    def add_update(self, update: UpdateProposed):
        pool = self.for_cluster(update.parent)
        self.cluster_pool[update.cluster_id] = pool + [update]
        self.total_updates += 1

