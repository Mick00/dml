from src.base.client.client_state_helpers import get_round_id, get_peers
from src.base.config.config_state_helper import get_trainer_threshold
from src.base.states.state import State
from src.base.states.handler import Handler
from src.base.states.transition import StateTransition
from src.base.client.messages.message import Message
from src.base.training.events import NextRound


class TriggerGenesis(StateTransition):
    def transition(self, msg: Message, state: State, handler: Handler):
        peers = get_peers(state)
        current_round = get_round_id(state)
        if current_round != -1:
            return
        if len(peers) + 1 >= get_trainer_threshold(state):
            handler.queue_event(NextRound(-1))
