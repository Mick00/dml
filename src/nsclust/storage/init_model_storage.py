import os.path

from src.nsclust.nsclust_helpers import MODEL_LOADER_KEY
from src.nsclust.storage.model_loader import ModelLoader
from src.base.client.client_state_helpers import get_node_id
from src.base.config.config_state_helper import get_output_path
from src.base.states.event import Event
from src.base.states.event_listener import EventListener
from src.base.states.state import State
from src.base.states.event_handler import EventHandler
from src.base.training.constants import TRAINING_MODULE
from src.base.training.training_state_helper import get_training_state


class InitModelLoader(EventHandler):
    def transition(self, event: Event, state: State, handler: EventListener):
        my_id = get_node_id(state)
        cache_path = os.path.join(get_output_path(state), "cache", my_id)
        model_loader = ModelLoader(cache_path)
        state.update_module(TRAINING_MODULE, {
            MODEL_LOADER_KEY: model_loader
        })
