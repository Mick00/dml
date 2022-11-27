import secrets

from src.nsclust.nsclust_helpers import CURRENT_CLUSTER_KEY, get_model_loader

from src.fed_avg.constant import GLOBAL_CLUSTER_ID
from src.protocol.client.client_state_helpers import get_node_id, get_peers, get_node_rank
from src.protocol.config.config_state_helper import get_local_model_name, get_experience_name
from src.protocol.states.handler import Handler
from src.protocol.states.state import State
from src.protocol.states.transition import StateTransition
from src.protocol.training.constants import TRAINING_MODULE
from src.protocol.training.events import TrainModel, StartRound
from src.protocol.training.models.experiment import Experiment
from src.protocol.training.models.model_factory import create_model


class StartTrainingPhase(StateTransition):
    def transition(self, event: StartRound, state: State, handler: Handler):
        round_id = event.data.round_id
        if round_id == 0:
            state.update_module(TRAINING_MODULE, {
                CURRENT_CLUSTER_KEY: GLOBAL_CLUSTER_ID
            })
            my_id = get_node_id(state)
            rank = get_node_rank(state)
            """Make the peer with the lowest ID create the seed model"""
            if rank == 0:
                model_name = get_local_model_name(state)
                model = create_model(model_name)
                experiment = Experiment(
                    get_experience_name(state),
                    GLOBAL_CLUSTER_ID,
                    event.data.round_id,
                    model_name,
                    model
                )
                handler.queue_event(TrainModel(experiment))
        else:
            model_loader = get_model_loader(state)
            exp = model_loader.get_experiment(
                GLOBAL_CLUSTER_ID,
                event.round_id,
                exp_name=get_experience_name(state))
            handler.queue_event(TrainModel(exp))
