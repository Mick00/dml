from src.nsclust.storage.model_loader import ModelLoader
from src.protocol.config.config_state_helper import get_experience_name
from src.protocol.states.state import State
from src.protocol.training.training_state_helper import get_training_state

MODEL_LOADER_KEY = "model_loader"
CURRENT_CLUSTER_KEY = "current_cluster"


def get_model_loader(state: State) -> ModelLoader:
    return get_training_state(state).get(MODEL_LOADER_KEY)


def get_current_cluster(state) -> str:
    return get_training_state(state).get(CURRENT_CLUSTER_KEY)


def get_cluster_training_exp_name(state) -> str:
    return f"{get_experience_name(state)}-clusters"


def get_cluster_selection_exp_name(state) -> str:
    return f"{get_experience_name(state)}-clusters-selection"


def get_update_selection_exp_name(state) -> str:
    return f"{get_experience_name(state)}-updates-selection"
