from src.daeclust.constants import AGGREGATION_UPDATE_SELECTION_DONE, AGGREGATION_UPDATE_POOLED, AGGREGATION_UPDATE_SELECTION_START
from src.protocol.states.event import Event
from src.protocol.training.fedml.model_update_meta import ModelUpdateMeta


class UpdatePooled(Event):
    def __init__(self, update: ModelUpdateMeta):
        super(UpdatePooled, self).__init__(AGGREGATION_UPDATE_POOLED)
        self.update = update


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
