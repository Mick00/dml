from src.base.config.config_state_helper import get_tracking_uri, get_output_path
from src.base.states.event import Event
from src.base.states.event_listener import EventListener
from src.base.states.state import State
from src.base.states.event_handler import EventHandlerSimple
from src.base.training.constants import TRAINING_MODULE
from src.base.training.events import InitExperiment
from src.base.training.experiment_tracking import ExperimentTracking
from src.base.training.training_state_helper import EXPERIMENT_TRACKING_KEY, get_experiment_tracking


class InitExperimentTracking(EventHandlerSimple):
    def transition(self, event: Event, state: State, handler: EventListener):
        tracking = ExperimentTracking(
            get_tracking_uri(state),
            get_output_path(state)
        )
        state.update_module(TRAINING_MODULE, {
            EXPERIMENT_TRACKING_KEY: tracking
        })


class InitExperimentHandler(EventHandlerSimple):
    def transition(self, event: InitExperiment, state: State, handler: EventListener):
        exp_tracking = get_experiment_tracking(state)
        exp_tracking.init(event.exp_name)
