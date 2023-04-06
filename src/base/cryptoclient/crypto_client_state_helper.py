from eth_account import Account

from src.base.client.client_state_helpers import CLIENT_KEY
from src.base.client.constants import CLIENT_MODULE
from src.base.config.config_state_helper import get_config
from src.base.cryptoclient.constants import ACCOUNT_KEY
from src.base.cryptoclient.crypto_client import CryptoClient
from src.base.states.state import State


def get_account(state: State) -> Account:
    return state.get_module_state(CLIENT_MODULE).get(ACCOUNT_KEY)


def get_crypto_client(state: State) -> CryptoClient:
    return state.get_module_state(CLIENT_MODULE).get(CLIENT_KEY)

def get_address_book_path(state: State) -> dict:
    return get_config(state).get("address_book")