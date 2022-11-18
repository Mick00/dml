from ..states.handler import Handler
from ..states.state import State


def cmd_parser(promp: str, state: State, handler: Handler):
    args = promp.split()
    if len(args) == 0:
        return
    cmd = args[0]
    args = args[1:]
    if cmd == "state":
        module = args[0]
        if len(args) > 1:
            path = args[1].split('.')
        else:
            path = []
        value = state.get_module_state(module)
        for segment in path:
            value = value.get(segment)
        if callable(value):
            value = value()
        print(f'{module}.{".".join(path)}', value)