import os.path

from src.daeclust.daeclust_helpers import MODEL_LOADER_KEY
from src.daeclust.storage.model_loader import ModelLoader
from src.protocol.client.client_state_helpers import get_node_id
from src.protocol.config.config_state_helper import get_output_path
from src.protocol.states.event import Event
from src.protocol.states.handler import Handler
from src.protocol.states.state import State
from src.protocol.states.transition import StateTransition
from src.protocol.training.constants import TRAINING_MODULE
from src.protocol.training.training_state_helper import get_training_state


class InitModelLoader(StateTransition):
    def transition(self, event: Event, state: State, handler: Handler):
        my_id = get_node_id(state)
        cache_path = os.path.join(get_output_path(state), "cache", my_id)
        model_loader = ModelLoader(cache_path)
        state.update_module(TRAINING_MODULE, {
            MODEL_LOADER_KEY: model_loader
        })
