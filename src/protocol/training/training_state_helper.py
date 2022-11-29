from src.protocol.config.config_state_helper import get_config
from src.protocol.states.state import State
from src.protocol.training.constants import TRAINING_MODULE
from src.protocol.training.experiment_tracking import ExperimentTracking
from src.protocol.training.training_client import TrainingClient

STARTED_KEY = 'started'
TRAINING_CLIENT_KEY = "client"
MODEL_LOADER_KEY = "model_loader"
EXPERIMENT_TRACKING_KEY = "experiment_tracking"


def get_training_state(state: State) -> dict:
    return state.get_module_state(TRAINING_MODULE)


def is_training_client_started(state: State) -> bool:
    return get_training_state(state).get(STARTED_KEY, False)


def get_training_client(state: State) -> TrainingClient:
    return get_training_state(state).get(TRAINING_CLIENT_KEY)


def get_experiment_tracking(state: State) -> ExperimentTracking:
    return get_training_state(state).get(EXPERIMENT_TRACKING_KEY)


def get_max_round(state: State) -> int:
    return get_config(state).get('max_round')