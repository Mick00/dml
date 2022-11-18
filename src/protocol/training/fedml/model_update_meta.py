from src.protocol.training.models.experiment import ModelMeta, Experiment
from src.protocol.training.models.model_factory import create_model


class ModelUpdateMeta(ModelMeta):
    def __init__(self,
                 cluster_id: str,
                 round_id: int,
                 model_name: str,
                 checkpoint_uri: str,
                 from_id: str
                 ):
        super().__init__(cluster_id, round_id, model_name, checkpoint_uri)
        self.from_id = from_id


def load_update(update: ModelUpdateMeta) -> Experiment:
    module = create_model(update.model_name)
    module.load_from_checkpoint(update.checkpoint_uri)
    return Experiment(update.cluster_id, update.round_id, update.model_name, module, update.checkpoint_uri)
