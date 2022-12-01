from src.daeclust.daecluste_helper import get_strategy
from src.daeclust.state.events import TrainerSelectedUpdates
from src.base.states.event_listener import EventListener
from src.base.states.state import State
from src.base.states.event_handler import EventHandler


class SelectedUpdatesHandler(EventHandler):
    def transition(self, event: TrainerSelectedUpdates, state: State, handler: EventListener):
        strategy = get_strategy(state)
        new_cluster_id = strategy.add_cluster(event.data.round_id, event.data.parent_cluster, event.data.accepted_updates)
        strategy.for_round(event.data.round_id).clusters.set_trainer_cluster(event.data.trainer_id, new_cluster_id)
