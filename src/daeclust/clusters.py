import os

import numpy as np
import pytorch_lightning as pl
import torch
from torch import nn

from src.base.training.models.model_factory import create_model
from src.base.training.models.operations import merge_models


class Cluster:
    round_id: int
    cluster_id: str
    start_model: str
    update_paths: [str]
    final_model: str
    model_name: str
    save_path: str

    def __init__(self,
                 cluster_id: str,
                 model_name: str,
                 round_id: int,
                 save_path: str,
                 updates_path: [str],
                 start_model=None,
    ):
        self.cluster_id = cluster_id
        self.model_name = model_name
        self.round_id = round_id
        self.save_path = save_path
        self.update_paths = updates_path
        self.start_model = start_model

    def create_model(self) -> pl.LightningModule:
        return create_model(self.model_name)

    def get_model(self) -> pl.LightningModule:
        cache_path = self.get_save_path()
        if not os.path.exists(cache_path):
            self.cache_final_model()
        model = self.create_model()
        model.load_state_dict(torch.load(cache_path))
        return model

    def cache_final_model(self) -> str:
        final_model = self.compute_final_model()
        if not os.path.exists(self.get_save_dir()):
            os.makedirs(self.get_save_dir())
        final_model_path = self.get_save_path()
        if os.path.exists(final_model_path):
            os.remove(final_model_path)
        torch.save(final_model.state_dict(), final_model_path)
        return final_model_path

    def compute_final_model(self) -> nn.Module:
        model = self.create_model()
        for i, update_path in enumerate(self.update_paths):
            update = self.create_model()
            update.load_from_checkpoint(update_path)
            merge_models(model, update, n=i)
        return model

    def get_save_dir(self):
        return os.path.join(self.save_path, self.cluster_id)

    def get_save_path(self):
        return os.path.join(self.get_save_dir(), "final_model.state")


class ClustersRegistry:

    def __init__(self):
        self.trainer_cluster = {}
        self.clusters = {}

    def get_ids(self) -> [str]:
        return self.clusters.keys()

    def get(self, cluster_id: str) -> Cluster:
        return self.clusters.get(cluster_id)

    def add(self, cluster_id: str, cluster: Cluster):
        self.clusters[cluster_id] = cluster

    def exists(self, cluster_id: str) -> bool:
        return cluster_id in self.clusters

    def set_trainer_cluster(self, trainer_id: str, cluster_id: str):
        self.trainer_cluster[trainer_id] = cluster_id

    def get_clusters_popularity(self) -> dict:
        selected_clusters = np.array(list(self.trainer_cluster.values()))
        ar_unique, i = np.unique(selected_clusters, return_counts=True)
        popularity = {}
        for cluster_id, count in zip(ar_unique, i):
            popularity[cluster_id] = count
        return popularity
