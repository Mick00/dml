import pytorch_lightning as pl
from src.protocol.training.models.architectures.cae_lenet import CaeLeNet


def create_model(model_name: str) -> pl.LightningModule:
    if model_name == "cae_lenet":
        return CaeLeNet()
