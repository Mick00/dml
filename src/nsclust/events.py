from src.nsclust.constants import UPDATES_SELECTED, AGGREGATION_DONE
from src.protocol.states.event import Event
from src.protocol.training.fedml.model_update_meta import ModelUpdateMeta


class SelectedUpdates(Event):
    def __init__(self, round_id: int, selected_updates: [ModelUpdateMeta]):
        super(SelectedUpdates, self).__init__(UPDATES_SELECTED)
        self.round_id = round_id
        self.selected_updates = selected_updates


class AggregationCompleted(Event):
    def __init__(self, round_id: int):
        super(AggregationCompleted, self).__init__(AGGREGATION_DONE)
        self.round_id = round_id