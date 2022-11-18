from src.protocol.config.constants import UPDATE_CONFIG, CONFIG_MODULE
from src.protocol.states.event import Event
from src.protocol.states.transition import StateTransition
from src.protocol.states.state import State
from src.protocol.states.handler import Handler


def register_config_module(handler: Handler):
    handler.register_reducer(UPDATE_CONFIG, UpdateConfigTransition(100))


class UpdateConfig(Event):
    def __init__(self, config: dict):
        super(UpdateConfig, self).__init__(UPDATE_CONFIG, config)


class UpdateConfigTransition(StateTransition):
    def transition(self, event: UpdateConfig, state: State, handler: Handler):
        state.update_module(CONFIG_MODULE, event.data.__dict__)
