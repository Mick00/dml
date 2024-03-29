import secrets

from src.base.cryptoclient.crypto_client_state_helper import get_crypto_client
from src.nsclust.nsclust_helpers import CURRENT_CLUSTER_KEY, get_cluster_training_exp_name
from src.nsclust.select_cluster import SelectCluster
from src.base.config.config_state_helper import get_local_model_name
from src.base.states.event import Event
from src.base.states.event_listener import EventListener
from src.base.states.state import State
from src.base.states.event_handler import EventHandlerSimple
from src.base.training.constants import TRAINING_MODULE
from src.base.training.events import TrainModel
from src.base.training.models.experiment import Experiment
from src.base.training.models.model_factory import create_model


class StartTrainingPhase(EventHandlerSimple):
    def transition(self, event: Event, state: State, handler: EventListener):
        round_id = event.data.round_id
        if round_id == 0:
            model_name = get_local_model_name(state)
            model = create_model(model_name)
            client = get_crypto_client(state)
            cluster_id = client.contracts.get("models").functions.root().call().hex()
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
