from src.protocol.client.client_state_helpers import get_node_id, STARTED_KEY
from src.protocol.config.config_state_helper import get_output_path, get_tracking_uri, \
    get_experience_name
from src.protocol.states.event import Event
from src.protocol.states.handler import Handler
from src.protocol.states.state import State
from src.protocol.states.transition import StateTransition
from src.protocol.training.constants import TRAINING_MODULE
from src.protocol.training.training_state_helper import is_training_client_started, TrainingClient, TRAINING_CLIENT_KEY


class StartTrainingClient(StateTransition):
    def transition(self, event: Event, state: State, handler: Handler):
        if not is_training_client_started(state):
            training_client = TrainingClient(
                get_node_id(state),
                output_dir=get_output_path(state),
                enable_gpu=False,
                tracking_uri=get_tracking_uri(state),
                exp_name=get_experience_name(state)
            )
            state.update_module(TRAINING_MODULE, {
                STARTED_KEY: True,
                TRAINING_CLIENT_KEY: training_client
            })
