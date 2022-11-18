from src.protocol.client.client_state_helpers import update_round_id, get_round_id
from src.protocol.states.handler import Handler
from src.protocol.states.state import State
from src.protocol.states.transition import StateTransition
from src.protocol.training.events import NextRound, StartRound


class NextRoundTransition(StateTransition):
    def transition(self, event: NextRound, state: State, handler: Handler):
        current_round = get_round_id(state)
        if current_round != event.current_round:
            print("Next round does not correspond with current round", current_round, event.current_round )
            return
        new_round = current_round + 1
        update_round_id(state, new_round)
        handler.queue_event(StartRound(new_round))
