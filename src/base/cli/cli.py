from .command_parser import cmd_parser
from .constant import CLI_START
from ..states.constants import HANDLER_STOP
from ..states.event import Event
from ..states.handler import Handler
from ..states.state import State
from ..states.transition import StateTransition


def register_cli_module(handler: Handler):
    handler.register_reducer(CLI_START, StartClient())


class StartClient(StateTransition):
    def __init__(self):
        self.exit = False

    def transition(self, event: Event, state: State, handler: Handler):
        while not self.exit:
            prompt = input(">>")

            if prompt == "stop":
                self.exit = True
                handler.queue_event(Event(HANDLER_STOP))
            else:
                cmd_parser(prompt, state, handler)

