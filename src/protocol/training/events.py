from src.protocol.states.event import Event
from src.protocol.training.constants import TRAIN_MODEL, MODEL_TRAINED, ROUND_START, NEXT_ROUND, INIT_EXPERIMENT, \
    MAX_ROUND_REACHED
from src.protocol.training.models.experiment import Experiment


class TrainModel(Event):
    def __init__(self, exp: Experiment):
        super(TrainModel, self).__init__(TRAIN_MODEL)
        self.exp = exp


class ModelTrained(Event):
    def __init__(self, model: Experiment):
        super(ModelTrained, self).__init__(MODEL_TRAINED)
        self.model = model


class NextRound(Event):
    def __init__(self, current_round: int):
        super(NextRound, self).__init__(NEXT_ROUND)
        self.current_round = current_round


class StartRound(Event):
    def __init__(self, round_id: int):
        super(StartRound, self).__init__(ROUND_START, {"round_id": round_id})
        self.round_id = round_id


class InitExperiment(Event):
    def __init__(self, exp_name: str):
        super(InitExperiment, self).__init__(INIT_EXPERIMENT)
        self.exp_name = exp_name


class MaxRoundReached(Event):
    def __init__(self):
        super(MaxRoundReached, self).__init__(MAX_ROUND_REACHED)
