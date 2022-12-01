from src.base.states.state import State
from src.base.training.fedml.update_queue import UpdateQueue
from src.base.training.training_state_helper import get_training_state

UPDATE_QUEUE_KEY = "update_queue"


def get_update_queue(state: State) -> UpdateQueue:
    return get_training_state(state).get(UPDATE_QUEUE_KEY)
