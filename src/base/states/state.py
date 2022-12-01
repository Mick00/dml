import threading

class State:
    _modules: dict

    def __init__(self):
        self._modules = dict()
        module_mutex = threading.Lock()

    def get_module_state(self, module_name: str) -> dict:
        if module_name in self._modules:
            return self._modules[module_name].copy()
        else:
            return {}

    def update_module(self, module_name: str, changes: dict):
        self._modules[module_name] = self.get_module_state(module_name) | changes
