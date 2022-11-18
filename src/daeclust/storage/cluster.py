import os

from src.daeclust.storage.round import Round


class Cluster:
    cluster_id: str
    rounds: dict[int, Round]

    def __init__(self, cluster_id: str, save_path: str):
        self.cluster_id = cluster_id
        self.save_path = save_path
        self.rounds = {}

    def init_storate(self):
        os.makedirs(self.get_cluster_save_path(), exist_ok=True)

    def get_cluster_save_path(self):
        return os.path.join(self.save_path, "clusters", self.cluster_id)

    def round_exists(self, round_id: int) -> bool:
        return round_id in self.rounds

    def get_round(self, round_id: int) -> Round:
        return self.rounds.get(round_id)

    def init_round(self, round_id: int, model_name: str):
        round = Round(model_name, round_id, self.get_cluster_save_path())
        self.rounds[round_id] = round
        return round

    def already_initialized(self) -> bool:
        return len(self.rounds.keys()) > 0

