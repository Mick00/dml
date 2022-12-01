from src.daeclust.daecluste_helper import get_strategy
from src.daeclust.state.events import TrainerSelectedUpdates
from src.base.client.client_state_helpers import get_peers
from src.base.states.handler import Handler
from src.base.states.state import State
from src.base.states.transition import StateTransition
from src.base.training.events import NextRound


class TriggerNextRound(StateTransition):
    def transition(self, event: TrainerSelectedUpdates, state: State, handler: Handler):
        peer_count = len(get_peers(state)) + 1
        round_id = event.data.round_id
        strategy = get_strategy(state)
        submitted_clusters = len(strategy.for_round(round_id).clusters.trainer_cluster.keys())
        if submitted_clusters == peer_count:
            handler.queue_event(NextRound(round_id))