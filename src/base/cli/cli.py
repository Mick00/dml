from .command_parser import cmd_parser
from .constant import CLI_START
from ..states.constants import HANDLER_STOP
from ..states.event import Event
from ..states.event_listener import EventListener
from ..states.state import State
from ..states.event_handler import EventHandlerSimple


def register_cli_module(handler: EventListener):
    handler.register_handler(CLI_START, StartClient())


class StartClient(EventHandlerSimple):
    def __init__(self):
        self.exit = False

    def transition(self, event: Event, state: State, handler: EventListener):
        while not self.exit:
            prompt = input(">>")

            if prompt == "stop":
                self.exit = True
                handler.queue_event(Event(HANDLER_STOP))
            else:
                cmd_parser(prompt, state, handler)

