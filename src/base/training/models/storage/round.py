import os

import pytorch_lightning as pl
import torch
from torch import nn

from src.base.training.models.model_factory import create_model
from src.base.training.models.operations import apply_diff, avg_dict


class Round:
    round_id: int
    start_model: str
    update_paths: [str]
    final_model: str
    model_name: str
    save_path: str

    def __init__(self,
                 model_name: str,
                 round_id: int,
                 save_path: str,
                 start_model=None,
                 final_model=None
    ):
        self.model_name = model_name
        self.round_id = round_id
        self.save_path = save_path
        self.update_paths = []
        self.start_model = start_model
        self.final_model = final_model

    def get_start_model(self) -> pl.LightningModule:
        model = self.create_model()
        if self.start_model:
            model.load_state_dict(torch.load(self.start_model))
        return model

    def create_model(self) -> pl.LightningModule:
        return create_model(self.model_name)

    def get_final_model(self) -> pl.LightningModule:
        if not self.final_model:
            self.cache_final_model()
        model = self.create_model()
        model.load_state_dict(torch.load(self.final_model))
        return model

    def cache_final_model(self) -> str:
        final_model = self.compute_final_model()
        if not os.path.exists(self.get_round_dir()):
            os.mkdir(self.get_round_dir())
        self.final_model = self.get_final_save_path()
        if os.path.exists(self.final_model):
            os.remove(self.final_model)
        torch.save(final_model.state_dict(), self.final_model)
        return self.final_model

    def compute_final_model(self) -> nn.Module:
        model = self.get_start_model()
        if len(self.update_paths) > 0:
            avg_update = torch.load(self.update_paths[0])
            for i, update_path in enumerate(self.update_paths[1:]):
                update = torch.load(update_path)
                avg_update = avg_dict(avg_update, update, n=i+1)
            return apply_diff(model, avg_update)
        return model

    def get_round_dir(self):
        return os.path.join(self.save_path, str(self.round_id))

    def get_final_save_path(self):
        return os.path.join(self.get_round_dir(), "final_model.state")

    def add_update(self, update: str) -> None:
        self.update_paths.append(update)

