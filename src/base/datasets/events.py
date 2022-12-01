from src.base.states.event import Event

DATA_REGISTER_HOOK = "data.register.hook"
DATASET_PREPARE = f"data.dataset.load"


class DataRegisterHook(Event):
    def __init__(self):
        super(DataRegisterHook, self).__init__(DATA_REGISTER_HOOK)


class PrepareDataset(Event):
    def __init__(self):
        super(PrepareDataset, self).__init__(DATASET_PREPARE)