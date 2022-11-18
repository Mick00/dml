import pytorch_lightning as pl


class ModelMeta:
    def __init__(self, cluster_id: str, round_id: int, model_name: str, checkpoint_uri: str):
        self.cluster_id = cluster_id
        self.round_id = round_id
        self.model_name = model_name
        self.checkpoint_uri = checkpoint_uri


class Experiment(ModelMeta):

    def __init__(self,
                 exp_name: str,
                 cluster_id: str,
                 round_id: int,
                 model_name: str,
                 model: pl.LightningModule,
                 checkpoint_uri=None,
                 experiment_id=None,
                 run_id=None):
        super().__init__(cluster_id, round_id, model_name, checkpoint_uri)
        self.exp_name = exp_name
        self.model = model
        self.experiment_id = experiment_id
        self.run_id = run_id
