from src.base.logging.logging_helpers import get_logger
from src.base.states.event_listener import EventListener
from src.base.states.state import State
from src.base.states.event_handler import EventHandler
from src.base.training.events import TrainModel, ModelTrained
from src.base.training.models.experiment import Experiment


def exp_to_log_dict(exp: Experiment) -> dict:
    return {
            "exp_name": exp.exp_name,
            "cluster_id": exp.cluster_id,
            "round_id": exp.round_id,
            "model_name": exp.model_name,
            "checkpoint_uri": exp.checkpoint_uri,
            "experiment_id": exp.experiment_id,
            "run_id": exp.run_id
        }


class LogStartTraining(EventHandler):
    def transition(self, event: TrainModel, state: State, handler: EventListener):
        exp = event.exp
        get_logger(state).info(event.type, extra=exp_to_log_dict(exp))


class LogCompletedTraining(EventHandler):
    def transition(self, event: ModelTrained, state: State, handler: EventListener):
        exp = event.exp
        get_logger(state).info(event.type, extra=exp_to_log_dict(exp))