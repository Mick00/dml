from src.protocol.client.client_state_helpers import get_round_id, get_peers
from src.protocol.config.config_state_helper import get_trainer_threshold
from src.protocol.states.state import State
from src.protocol.states.handler import Handler
from src.protocol.states.transition import StateTransition
from src.protocol.client.messages.message import Message
from src.protocol.training.events import NextRound


class TriggerGenesis(StateTransition):
    def transition(self, msg: Message, state: State, handler: Handler):
        peers = get_peers(state)
        current_round = get_round_id(state)
        if current_round != -1:
            return
        if len(peers) + 1 >= get_trainer_threshold(state):
            handler.queue_event(NextRound(-1))
