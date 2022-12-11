from src.daeclust.constants import AGGREGATION_UPDATE_SELECTION_DONE, AGGREGATION_UPDATE_POOLED, \
    AGGREGATION_UPDATE_SELECTION_START, CLUSTER_SELECTED, TRAINING_UPDATED_CLUSTERS
from src.base.states.event import Event
from src.base.training.fedml.model_update_meta import ModelUpdateMeta


class UpdatesPooled(Event):
    def __init__(self, round_id: int, trainers_entered: int):
        super(UpdatesPooled, self).__init__(AGGREGATION_UPDATE_POOLED)
        self.round_id = round_id
        self.trainers_entered = trainers_entered


class TrainerSelectedUpdates(Event):
    def __init__(self, round_id: int, trainer_id: str, parent_cluster: str, accepted_updates: [str]):
        super(TrainerSelectedUpdates, self).__init__(AGGREGATION_UPDATE_SELECTION_DONE)
        self.data.round_id = round_id
        self.data.trainer_id = trainer_id
        self.data.parent_cluster = parent_cluster
        self.data.accepted_updates = accepted_updates


class StartUpdateSelection(Event):
    def __init__(self, round_id: int):
        super(StartUpdateSelection, self).__init__(AGGREGATION_UPDATE_SELECTION_START)
        self.round_id = round_id


class SelectedClusters(Event):
    def __init__(self, round_id, ids: list[str]):
        super(SelectedClusters, self).__init__(CLUSTER_SELECTED)
        self.round_id = round_id
        self.ids = ids


class UpdatedClusters(Event):
    def __init__(self, updates: [any]):
        super(UpdatedClusters, self).__init__(TRAINING_UPDATED_CLUSTERS, {
            "updates": updates
        })