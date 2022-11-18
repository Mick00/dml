import secrets

from src.daeclust.daeclust_helpers import CURRENT_CLUSTER_KEY, get_cluster_training_exp_name
from src.daeclust.select_cluster import SelectCluster
from src.protocol.config.config_state_helper import get_local_model_name
from src.protocol.states.event import Event
from src.protocol.states.handler import Handler
from src.protocol.states.state import State
from src.protocol.states.transition import StateTransition
from src.protocol.training.constants import TRAINING_MODULE
from src.protocol.training.events import TrainModel
from src.protocol.training.models.experiment import Experiment
from src.protocol.training.models.model_factory import create_model


class StartTrainingPhase(StateTransition):
    def transition(self, event: Event, state: State, handler: Handler):
        round_id = event.data.round_id
        if round_id == 0:
            model_name = get_local_model_name(state)
            model = create_model(model_name)
            cluster_id = secrets.token_hex(16)
            experiment = Experiment(
                get_cluster_training_exp_name(state),
                cluster_id,
                event.data.round_id,
                model_name,
                model
            )
            state.update_module(TRAINING_MODULE, {
                CURRENT_CLUSTER_KEY: cluster_id
            })
            handler.queue_event(TrainModel(experiment))
        else:
            handler.queue_event(SelectCluster(round_id))
