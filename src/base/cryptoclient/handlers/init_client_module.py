from eth_account import Account
import secrets

from src.base.client.client_state_helpers import client_is_started, ID_KEY
from src.base.cryptoclient.constants import ACCOUNT_KEY
from src.base.states.event_handler import EventHandlerSimple
from src.base.states.event import Event
from src.base.states.state import State
from src.base.states.event_listener import EventListener

from src.base.client.constants import CLIENT_MODULE

class InitClientModule(EventHandlerSimple):
    def transition(self, event: Event, state: State, handler: EventListener):
        if not client_is_started(state):
            account = Account.create(secrets.token_hex(16))
            state.update_module(CLIENT_MODULE, {
                ID_KEY: account.address,
                ACCOUNT_KEY: account
            })