from src.base.client.client_state_helpers import update_round_id, get_round_id
from src.base.states.handler import Handler
from src.base.states.state import State
from src.base.states.transition import StateTransition
from src.base.training.events import NextRound, StartRound, MaxRoundReached
from src.base.training.training_state_helper import get_max_round


class NextRoundTransition(StateTransition):
    def transition(self, event: NextRound, state: State, handler: Handler):
        current_round = get_round_id(state)
        if current_round != event.current_round:
            print("Next round does not correspond with current round. state:", current_round, ", event:", event.current_round )
            return
        if get_max_round(state) < event.current_round:
            handler.queue_event(MaxRoundReached())
        else:
            new_round = current_round + 1
            update_round_id(state, new_round)
            handler.queue_event(StartRound(new_round))
