from src.protocol.states.event import Event
from src.protocol.training.fedml.constants import SHARE_UPDATE
from src.protocol.training.models.experiment import ModelMeta


class ClusterUpdate(Event):
    def __init__(self, model_meta: ModelMeta):
        super(ClusterUpdate, self).__init__(SHARE_UPDATE, {
            "cluster_id": model_meta.cluster_id,
            "round_id": model_meta.round_id,
            "model_name": model_meta.model_name,
            "checkpoint_uri": model_meta.checkpoint_uri
        })
