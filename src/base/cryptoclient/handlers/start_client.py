from threading import Thread

from src.base.client.client_state_helpers import client_is_started, init_client
from src.base.client.constants import CLIENT_STARTED
from src.base.config.config_state_helper import get_broker_host
from src.base.cryptoclient.crypto_client import CryptoClient
from src.base.cryptoclient.crypto_client_state_helper import get_account, get_address_book_path
from src.base.states.event import Event
from src.base.states.event_handler import EventHandlerSimple
from src.base.states.event_listener import EventListener
from src.base.states.state import State


class StartClient(EventHandlerSimple):
    def transition(self, event: Event, state: State, handler: EventListener):
        if not client_is_started(state):
            account = get_account(state)
            host, port = get_broker_host(state)
            client = CryptoClient(
                host,
                account,
                get_address_book_path(state),
                handler
            )
            thread = Thread(target=client.listen)
            thread.setName("client")
            init_client(state, client)
            thread.start()
            handler.queue_event(Event(CLIENT_STARTED))