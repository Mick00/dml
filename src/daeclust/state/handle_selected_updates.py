from src.daeclust.daecluste_helper import get_strategy
from src.daeclust.state.events import TrainerSelectedUpdates
from src.protocol.states.handler import Handler
from src.protocol.states.state import State
from src.protocol.states.transition import StateTransition


class SelectedUpdatesHandler(StateTransition):
    def transition(self, event: TrainerSelectedUpdates, state: State, handler: Handler):
        strategy = get_strategy(state)
        new_cluster_id = strategy.add_cluster(event.data.round_id, event.data.parent_cluster, event.data.accepted_updates)
        strategy.for_round(event.data.round_id).clusters.set_trainer_cluster(event.data.trainer_id, new_cluster_id)
