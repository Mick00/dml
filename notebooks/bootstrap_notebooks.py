from unittest.mock import Mock
import pytorch_lightning as pl

from src.base.client.client_state_helpers import ID_KEY
from src.base.client.constants import CLIENT_MODULE
from src.base.config.constants import CONFIG_MODULE
from src.base.datasets.data_loader import get_data_loader
from src.base.datasets.init_data_loader import InitDataLoader
from src.base.datasets.loaders.emnist_loader import EmnistRegister
from src.base.datasets.loaders.fmnist_loader import FmnistRegister
from src.base.datasets.loaders.mnist_loader import MnistRegister
from src.base.states.state import State
from src.base.training.events import InitExperiment
from src.base.training.init_experiment_tracking import InitExperimentTracking, InitExperimentHandler
from src.base.training.models.experiment import Experiment
from src.base.training.start_training_client import StartTrainingClient
from src.base.training.training_state_helper import get_training_client

state = State()


def bootstrap_notebook(config: dict):
    state.update_module(CONFIG_MODULE, config)
    state.update_module(CLIENT_MODULE, {ID_KEY: "notebook"})
    run(InitDataLoader, None, state)
    run(FmnistRegister, None, state)
    run(MnistRegister, None, state)
    run(EmnistRegister, None, state)
    run(InitExperimentTracking, None, state)
    run(InitExperimentHandler, InitExperiment(config.get("exp_name")), state)
    run(StartTrainingClient, None, state)


def run(constructor, event, state):
    handler = Mock()
    constructor(0).transition(event, state, handler)


def load_dataset(config, sampler_conf_cb=None):
    state.update_module(CONFIG_MODULE, config)
    dl = get_data_loader(state)
    dl.set_sampler_tags({"dataset": config.get("dataset")})
    if callable(sampler_conf_cb):
        sampler_conf_cb(dl)
    dl.load_data(state)


def train(model: pl.LightningModule, epochs=0):
    exp = Experiment(
        state.get_module_state(CONFIG_MODULE).get("exp_name"),
        "",
        0,
        model.__class__.__name__,
        model)
    tc = get_training_client(state)
    return tc.train_model(exp, max_epochs=epochs)


def test(model: pl.LightningModule):
    exp = Experiment(
        state.get_module_state(CONFIG_MODULE).get("exp_name"),
        "",
        0,
        model.__class__.__name__,
        model)
    tc = get_training_client(state)
    return tc.test_model(exp)