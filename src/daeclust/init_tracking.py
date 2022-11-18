from src.daeclust.daeclust_helpers import get_cluster_training_exp_name, get_update_selection_exp_name, \
    get_cluster_selection_exp_name
from src.protocol.states.event import Event
from src.protocol.states.handler import Handler
from src.protocol.states.state import State
from src.protocol.states.transition import StateTransition
from src.protocol.training.events import InitExperiment


class InitTracking(StateTransition):
    def transition(self, event: Event, state: State, handler: Handler):
        handler.queue_event(InitExperiment(get_cluster_training_exp_name(state)))
        handler.queue_event(InitExperiment(get_cluster_selection_exp_name(state)))
        handler.queue_event(InitExperiment(get_update_selection_exp_name(state)))