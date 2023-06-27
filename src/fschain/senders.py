import web3
from web3 import Web3

from src.base.config.config_state_helper import get_local_model_name
from src.base.cryptoclient.crypto_client import CryptoClient
from src.base.cryptoclient.crypto_client_state_helper import get_crypto_client
from src.base.states.event import Event
from src.base.states.event_handler import EventHandler, Handler
from src.base.states.state import State
from src.base.training.fedml.constants import TRAINING_UPDATE_SHARE
from src.base.training.fedml.events import ClusterUpdate
from src.fschain.update_proposed import UpdateProposed


class RegisterChainAdapters(EventHandler):
    def _transition(self, event: Event, state: State, handler: Handler) -> [dict]:

        client = get_crypto_client(state)
        self.register_model_proposal(client, get_local_model_name(state))

    def register_model_proposal(self, client: CryptoClient, model_name: str):
        """
        event UpdateProposed:
            proposer: indexed(address)
            parent: indexed(bytes32)
            updateId: uint256
            URI: String[128]
        """
        self.register_model_sender(client)
        self.register_model_handler(client, model_name)

    def register_model_sender(self, client: CryptoClient):
        def send_trained_models(message: ClusterUpdate, contracts):
            parent = bytes.fromhex(message.data.cluster_id)
            return contracts.get("updates").functions.propose(
                parent,
                message.data.checkpoint_uri
            )
        client.register_sender(TRAINING_UPDATE_SHARE, send_trained_models)

    def register_model_handler(self, client: CryptoClient, model_name):
        event_listener = client.contracts["updates"].events["UpdateProposed"].createFilter(fromBlock=0)
        def received_trained_models(event):
            return UpdateProposed(
                event.args.roundId,
                event.args.parent.hex(),
                event.args.updateId,
                event.args.proposer,
                event.args.URI,
            )

        client.register_events(event_listener, received_trained_models)