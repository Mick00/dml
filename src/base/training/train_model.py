from threading import Thread

from src.base.states.state import State
from src.base.states.event_listener import EventListener
from src.base.states.event_handler import EventHandlerSimple
from src.base.training.constants import  TRAIN_MODEL, MODEL_TRAINED, TRAINING_MODULE
from src.base.training.events import TrainModel, ModelTrained
from src.base.training.models.experiment import Experiment
from src.base.training.training_client import TrainingClient
from src.base.training.training_state_helper import get_training_client, get_training_state


def train_model(exp: Experiment, training_client: TrainingClient, handler: EventListener):
    exp = training_client.train_model(exp)
    handler.queue_event(ModelTrained(exp))


class Train(EventHandlerSimple):
    def transition(self, event: TrainModel, state: State, handler: EventListener):
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


class TrainingCleanUp(EventHandlerSimple):
    def transition(self, event: ModelTrained, state: State, handler: EventListener):
        thread_name = get_training_thread_name(event.exp)
        state.update_module(TRAINING_MODULE, {
            thread_name: None
        })
