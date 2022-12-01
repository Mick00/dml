import os
import secrets
from abc import ABC
from threading import Thread

from .actions.client_rank import SetClientRank
from .actions.confirm_registration import ConfirmRegistrationReceiverTransition
from .actions.constants import REGISTER_MESSAGE, CONFIRM_REGISTRATION_MESSAGE, NEW_PEER
from .actions.register import RegisterSenderTransition, RegisterReceiverTransition
from .client import Client
from .client_state_helpers import get_round_id, init_client, set_is_stopping, client_is_started, get_client, ID_KEY, \
    get_node_id
from .constants import CLIENT_MODULE, CLIENT_START, CLIENT_STARTED, CLIENT_SEND, CLIENT_STOPPED
from .messages.message import wrap_event
from ..config.config_state_helper import get_broker_host
from ..states.constants import HANDLER_STOP, HANDLER_STARTED
from ..states.event import Event
from ..states.event_listener import EventListener
from ..states.state import State
from ..states.event_handler import EventHandler


def register_client_module(handler: EventListener):
    start_client = StartClient(200)
    handler.register_handler(CLIENT_START, start_client)
    handler.register_handler(HANDLER_STARTED, InitClientModule(10))
    handler.register_handler(HANDLER_STARTED, start_client)
    handler.register_handler(HANDLER_STOP, StopClient(90))
    handler.register_handler(CLIENT_STOPPED, StoppedClient(100))
    handler.register_handler(CLIENT_SEND, SendClient(100))
    handler.register_handler(CLIENT_STARTED, RegisterSenderTransition(200))
    handler.register_handler(REGISTER_MESSAGE, RegisterReceiverTransition(100))
    handler.register_handler(CONFIRM_REGISTRATION_MESSAGE, ConfirmRegistrationReceiverTransition(100))
    handler.register_handler(NEW_PEER, SetClientRank(10))


class InitClientModule(EventHandler):
    def transition(self, event: Event, state: State, handler: EventListener):
        if not client_is_started(state):
            id = secrets.token_hex(16)
            state.update_module(CLIENT_MODULE, {
                ID_KEY: id,
            })


class StartClient(EventHandler):
    def transition(self, event: Event, state: State, handler: EventListener):
        if not client_is_started(state):
            id = get_node_id(state)
            host, port = get_broker_host(state)
            client = Client(
                id,
                host,
                port,
                handler
            )
            thread = Thread(target=client.join)
            thread.setName("client")
            init_client(state, client)
            thread.start()
            handler.queue_event(Event(CLIENT_STARTED))


class StopClient(EventHandler):
    def transition(self, event: Event, state: State, handler: EventListener):
        if client_is_started(state):
            set_is_stopping(state, True)
            client = get_client(state)
            client.quit()


class StoppedClient(EventHandler):
    def transition(self, event: Event, state: State, handler: EventListener):
        state.update_module(CLIENT_MODULE, {
            "started": False,
            "is_stopping": False,
            "client": None
        })


class SendClient(EventHandler):
    def transition(self, event: Event, state: State, handler: EventListener):
        if client_is_started(state):
            client = get_client(state)
            message = wrap_event(client.id, get_round_id(state), event.data)
            client.send(message)
        else:
            print("Could not send message. Reason: client is not started")