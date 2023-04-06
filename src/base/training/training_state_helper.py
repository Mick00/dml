from src.base.config.config_state_helper import get_config
from src.base.states.state import State
from src.base.training.constants import TRAINING_MODULE
from src.base.training.experiment_tracking import ExperimentTracking
from src.base.training.training_client import TrainingClient

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


def get_training_profiler(state: State) -> int:
    return get_config(state).get('training_profiler', None)


def get_training_n_devices(state: State) -> int:
    return get_config(state).get('training_n_dev', 0)


def get_n_epochs(state: State) -> int:
    return get_config(state).get('n_epochs')


def get_batch_size(state: State) -> int:
    return get_config(state).get('batch_size', 32)