from src.protocol.logging.logger import get_logger
from src.protocol.states.handler import Handler
from src.protocol.states.state import State
from src.protocol.states.transition import StateTransition
from src.protocol.training.events import TrainModel, ModelTrained


class LogStartTraining(StateTransition):
    def transition(self, event: TrainModel, state: State, handler: Handler):
        exp = event.exp
        get_logger(state).info(event.type, extra={
            "exp_name": exp.exp_name,
            "cluster_id": exp.cluster_id,
            "round_id": exp.round_id,
            "model_name": exp.model_name,
            "checkpoint_uri": exp.checkpoint_uri,
        })


class LogCompletedTraining(StateTransition):
    def transition(self, event: ModelTrained, state: State, handler: Handler):
        exp = event.exp
        get_logger(state).info(event.type, extra={
            "exp_name": exp.exp_name,
            "cluster_id": exp.cluster_id,
            "round_id": exp.round_id,
            "model_name": exp.model_name,
            "checkpoint_uri": exp.checkpoint_uri,
            "experiment_id": exp.experiment_id,
            "run_id": exp.run_id
        })