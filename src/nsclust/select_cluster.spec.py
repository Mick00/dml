import unittest
from unittest.mock import Mock

from src.nsclust.nsclust_helpers import get_cluster_selection_exp_name
from src.nsclust.select_cluster import SelectBestCluster, CusterSelectionTestCompleted
from src.base.client.client_state_helpers import init_client
from src.base.config.config import UpdateConfig, UpdateConfigHandler
from src.base.states.event import Event
from src.base.states.state import State
from src.base.training.events import InitExperiment
from src.base.training.init_experiment_tracking import InitExperimentTracking, InitExperimentHandler
from src.base.training.models.storage.cluster import Cluster


class ModelLoaderTest(unittest.TestCase):

    def init_state(self) -> State:
        state = State()
        handler = Mock()
        client = Mock()
        client.id = "0bca02f8ff33849c5954ad08162ccbf1"
        init_client(state, client)
        update_config = UpdateConfigHandler(0)
        update_config.transition(UpdateConfig( {
            "tracking_uri": "http://localhost:5000",
            "experiment_name": "declust"
        }), state, handler)
        init_tracking = InitExperimentTracking(0)
        init_tracking.transition(Event(None), state, handler)
        InitExperimentHandler(0).transition(InitExperiment(get_cluster_selection_exp_name(state)), state, handler)
        return state

    def test_init(self):
        state = self.init_state()
        handler = Mock()
        SelectBestCluster(0).transition(CusterSelectionTestCompleted(1), state, handler)


if __name__ == '__main__':
    unittest.main()