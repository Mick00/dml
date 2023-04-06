from src.base.config.cli_config import get_arg_parse
from src.base.training.next_round import NextRoundTransition
from src.base.client.actions.constants import NEW_PEER
from src.base.states.constants import HANDLER_STARTED
from src.base.states.event_listener import EventListener
from src.base.training.constants import TRAIN_MODEL, MODEL_TRAINED, NEXT_ROUND, INIT_EXPERIMENT, MAX_ROUND_REACHED
from src.base.training.fedml.init_update_queue import InitUpdateQueue
from src.base.training.init_experiment_tracking import InitExperimentTracking, InitExperimentHandler
from src.base.training.models.storage.model_loader import InitModelLoader
from src.base.training.trigger_genesis import TriggerGenesis
from src.base.training.start_training_client import StartTrainingClient
from src.base.training.train_model import Train, TrainingCleanUp
from src.base.training.trigger_stop import TriggerStop

argparse = get_arg_parse()
argparse.add_argument('--max_round', type=int, default=-1)
argparse.add_argument('--training_profiler', default=None)
argparse.add_argument('--training_n_dev', type=int, default=0)
argparse.add_argument('--n_epochs', type=int, default=1)


def register_training_module(handler: EventListener):
    handler.register_handler(HANDLER_STARTED, InitModelLoader(40))
    handler.register_handler(HANDLER_STARTED, InitUpdateQueue(41))
    handler.register_handler(HANDLER_STARTED, InitExperimentTracking(42))
    handler.register_handler(HANDLER_STARTED, StartTrainingClient(120))
    handler.register_handler(INIT_EXPERIMENT, InitExperimentHandler(100))
    handler.register_handler(NEW_PEER, TriggerGenesis(200))
    handler.register_handler(NEXT_ROUND, NextRoundTransition(100))
    handler.register_handler(TRAIN_MODEL, Train(100))
    handler.register_handler(MODEL_TRAINED, TrainingCleanUp(100))
    handler.register_handler(MAX_ROUND_REACHED, TriggerStop(100))

