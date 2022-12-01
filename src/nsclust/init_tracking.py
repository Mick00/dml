from src.nsclust.nsclust_helpers import get_cluster_training_exp_name, get_update_selection_exp_name, \
    get_cluster_selection_exp_name
from src.base.states.event import Event
from src.base.states.handler import Handler
from src.base.states.state import State
from src.base.states.transition import StateTransition
from src.base.training.events import InitExperiment


class InitTracking(StateTransition):
    def transition(self, event: Event, state: State, handler: Handler):
        handler.queue_event(InitExperiment(get_cluster_training_exp_name(state)))
        handler.queue_event(InitExperiment(get_cluster_selection_exp_name(state)))
        handler.queue_event(InitExperiment(get_update_selection_exp_name(state)))