from src.base.datasets.data_loader import get_data_loader
from src.base.client.client_state_helpers import get_node_id, STARTED_KEY
from src.base.config.config_state_helper import get_output_path, get_tracking_uri, \
    get_experience_name
from src.base.states.event import Event
from src.base.states.event_listener import EventListener
from src.base.states.state import State
from src.base.states.event_handler import EventHandler
from src.base.training.constants import TRAINING_MODULE
from src.base.training.training_state_helper import is_training_client_started, TrainingClient, TRAINING_CLIENT_KEY, \
    get_training_profiler, get_n_epochs, get_training_n_devices


class StartTrainingClient(EventHandler):
    def transition(self, event: Event, state: State, handler: EventListener):
        if not is_training_client_started(state):
            training_client = TrainingClient(
                get_node_id(state),
                get_data_loader(state),
                output_dir=get_output_path(state),
                enable_gpu=False,
                tracking_uri=get_tracking_uri(state),
                exp_name=get_experience_name(state),
                profiler=get_training_profiler(state),
                epochs=get_n_epochs(state),
                devices=get_training_n_devices(state)
            )
            state.update_module(TRAINING_MODULE, {
                STARTED_KEY: True,
                TRAINING_CLIENT_KEY: training_client
            })
