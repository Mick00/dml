from threading import Thread

from src.protocol.states.state import State
from src.protocol.states.handler import Handler
from src.protocol.states.transition import StateTransition
from src.protocol.training.constants import  TRAIN_MODEL, MODEL_TRAINED, TRAINING_MODULE
from src.protocol.training.events import TrainModel, ModelTrained
from src.protocol.training.models.experiment import Experiment
from src.protocol.training.training_client import TrainingClient
from src.protocol.training.training_state_helper import get_training_client, get_training_state


def train_model(exp: Experiment, training_client: TrainingClient, handler: Handler):
    exp = training_client.train_model(exp)
    handler.queue_event(ModelTrained(exp))


class Train(StateTransition):
    def transition(self, event: TrainModel, state: State, handler: Handler):
        training_state = get_training_state(state)
        thread_name = get_training_thread_name(event.exp)
        if not training_state.get(thread_name, False):
            training_client = get_training_client(state)
            thread = Thread(target=train_model, args=(event.exp, training_client, handler))
            thread.setName(thread_name)
            state.update_module(TRAINING_MODULE, {
                thread_name: thread
            })
            thread.start()
        else:
            print(f"{thread_name} is already training...")


def get_training_thread_name(model: Experiment) -> str:
    return f"training-{model.round_id}-{model.cluster_id}"


class TrainingCleanUp(StateTransition):
    def transition(self, event: ModelTrained, state: State, handler: Handler):
        thread_name = get_training_thread_name(event.exp)
        state.update_module(TRAINING_MODULE, {
            thread_name: None
        })
