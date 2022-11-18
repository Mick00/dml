from src.protocol.training.next_round import NextRoundTransition
from src.protocol.client.actions.constants import NEW_PEER
from src.protocol.client.constants import CLIENT_STARTED
from src.protocol.states.constants import HANDLER_STARTED
from src.protocol.states.handler import Handler
from src.protocol.training.constants import TRAIN_MODEL, MODEL_TRAINED, NEXT_ROUND, INIT_EXPERIMENT
from src.protocol.training.fedml.constants import SHARE_UPDATE
from src.protocol.training.fedml.init_update_queue import InitUpdateQueue
from src.protocol.training.fedml.share_update import ShareUpdate, ReceiveUpdate
from src.protocol.training.init_experiment_tracking import InitExperimentTracking, InitExperimentHandler
from src.protocol.training.models.storage.model_loader import InitModelLoader
from src.protocol.training.start_genesis import StartGenesisTransition
from src.protocol.training.start_training_client import StartTrainingClient
from src.protocol.training.train_model import Train, TrainingCleanUp


def register_training_module(handler: Handler):
    handler.register_reducer(HANDLER_STARTED, InitModelLoader(40))
    handler.register_reducer(HANDLER_STARTED, InitUpdateQueue(41))
    handler.register_reducer(HANDLER_STARTED, InitExperimentTracking(42))
    handler.register_reducer(INIT_EXPERIMENT, InitExperimentHandler(100))
    handler.register_reducer(CLIENT_STARTED, StartTrainingClient(50))
    handler.register_reducer(NEW_PEER, StartGenesisTransition(100))
    handler.register_reducer(NEXT_ROUND, NextRoundTransition(100))
    handler.register_reducer(TRAIN_MODEL, Train(100))
    handler.register_reducer(MODEL_TRAINED, TrainingCleanUp(100))
    handler.register_reducer(SHARE_UPDATE, ReceiveUpdate(100))
