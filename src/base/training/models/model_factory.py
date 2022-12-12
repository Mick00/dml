import pytorch_lightning as pl
from src.base.training.models.architectures.cae_lenet import CaeLeNet
from src.base.training.models.architectures.cae_lenet_light import CaeLeNetLight
from src.base.training.models.architectures.lenet import LeNet


def create_model(model_name: str) -> pl.LightningModule:
    if model_name == "cae_lenet":
        return CaeLeNet()
    if model_name == "cae_lenet_light":
        return CaeLeNetLight()
    if model_name == "lenet":
        return LeNet()
