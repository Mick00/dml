from .handlers.init_client_module import InitClientModule
from .handlers.registration import RegisterReceiverTransition, RegisterTransaction
from .handlers.start_client import StartClient
from ..client.actions.client_rank import SetClientRank
from ..client.actions.constants import REGISTER_MESSAGE, NEW_PEER
from ..client.actions.register import RegisterSenderTransition
from ..client.constants import CLIENT_START, CLIENT_STOPPED, CLIENT_STARTED, CLIENT_SEND
from ..client.reducers import StopClient, StoppedClient, SendClient
from ..config.cli_config import get_arg_parse
from ..states.constants import HANDLER_STOP, HANDLER_STARTED
from ..states.event_listener import EventListener

argparse = get_arg_parse()
argparse.add_argument('--address_book', type=str)

def register_cryptoclient_module(handler: EventListener):
    start_client = StartClient(100)
    handler.register_handler(CLIENT_START, start_client)
    handler.register_handler(HANDLER_STARTED, InitClientModule(10))
    handler.register_handler(HANDLER_STARTED, start_client)
    handler.register_handler(HANDLER_STOP, StopClient(90))
    handler.register_handler(CLIENT_STOPPED, StoppedClient(100))
    handler.register_handler(CLIENT_STARTED, RegisterTransaction(10))
    handler.register_handler(CLIENT_SEND, SendClient(100))
    handler.register_handler(CLIENT_STARTED, RegisterSenderTransition(100))
    handler.register_handler(NEW_PEER, RegisterReceiverTransition(100))
    handler.register_handler(NEW_PEER, SetClientRank(110))
