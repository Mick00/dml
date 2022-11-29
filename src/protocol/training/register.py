from src.protocol.config.cli_config import get_arg_parse
from src.protocol.training.next_round import NextRoundTransition
from src.protocol.client.actions.constants import NEW_PEER
from src.protocol.states.constants import HANDLER_STARTED
from src.protocol.states.handler import Handler
from src.protocol.training.constants import TRAIN_MODEL, MODEL_TRAINED, NEXT_ROUND, INIT_EXPERIMENT, MAX_ROUND_REACHED
from src.protocol.training.fedml.init_update_queue import InitUpdateQueue
from src.protocol.training.init_experiment_tracking import InitExperimentTracking, InitExperimentHandler
from src.protocol.training.models.storage.model_loader import InitModelLoader
from src.protocol.training.trigger_genesis import TriggerGenesis
from src.protocol.training.start_training_client import StartTrainingClient
from src.protocol.training.train_model import Train, TrainingCleanUp
from src.protocol.training.trigger_stop import TriggerStop

argparse = get_arg_parse()
argparse.add_argument('--max_round', type=int, default=-1)
argparse.add_argument('--training_profiler', default=None)
argparse.add_argument('--training_n_dev', default=None)
argparse.add_argument('--n_epochs', default=1)


def register_training_module(handler: Handler):
    handler.register_reducer(HANDLER_STARTED, InitModelLoader(40))
    handler.register_reducer(HANDLER_STARTED, InitUpdateQueue(41))
    handler.register_reducer(HANDLER_STARTED, InitExperimentTracking(42))
    handler.register_reducer(HANDLER_STARTED, StartTrainingClient(120))
    handler.register_reducer(INIT_EXPERIMENT, InitExperimentHandler(100))
    handler.register_reducer(NEW_PEER, TriggerGenesis(100))
    handler.register_reducer(NEXT_ROUND, NextRoundTransition(100))
    handler.register_reducer(TRAIN_MODEL, Train(100))
    handler.register_reducer(MODEL_TRAINED, TrainingCleanUp(100))
    handler.register_reducer(MAX_ROUND_REACHED, TriggerStop(100))

