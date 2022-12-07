from src.base.config.constants import UPDATE_CONFIG, CONFIG_MODULE
from src.base.states.event import Event
from src.base.states.event_handler import EventHandlerSimple
from src.base.states.state import State
from src.base.states.event_listener import EventListener


def register_config_module(handler: EventListener):
    handler.register_handler(UPDATE_CONFIG, UpdateConfigHandler(100))


class UpdateConfig(Event):
    def __init__(self, config: dict):
        super(UpdateConfig, self).__init__(UPDATE_CONFIG, config)


class UpdateConfigHandler(EventHandlerSimple):
    def transition(self, event: UpdateConfig, state: State, handler: EventListener):
        state.update_module(CONFIG_MODULE, event.data.__dict__)
