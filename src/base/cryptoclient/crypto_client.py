import json
import os

from eth_account.signers.local import LocalAccount
from web3 import Web3
import time

from src.base.client.constants import CLIENT_STOPPED
from src.base.client.messages.message import Message
from src.base.states.event import Event
from src.base.states.event_listener import EventListener


class CryptoClient():

    def __init__(self, rpc_url, account: LocalAccount, addressbook_path, handler: EventListener):
        self.provider = Web3(Web3.HTTPProvider(rpc_url))
        self.account = account
        self.id = account.address
        self.handler = handler
        self.load_address_book(addressbook_path)
        self.event_listeners = []
        self.senders = {}
        self.stop = False

    def get_account_nonce(self):
        return self.provider.eth.get_transaction_count(self.account.address)

    def load_address_book(self, path):
        self.contracts = {}
        with open(os.path.join(path), 'r') as f:
            addresses = json.load(f)
        for name, meta in addresses.items():
            abi = [json.loads(fn) for fn in meta.get("abi")]
            self.contracts[name] = self.provider.eth.contract(meta.get("address"), abi=abi)

    def register_events(self, event_listener, callback):
        self.event_listeners.append({
            "listener": event_listener,
            "callback": callback
        })

    def listen(self):
        self.stop = False
        while not self.stop:
            for event_listener in self.event_listeners:
                callback = event_listener["callback"]
                listener = event_listener["listener"]
                for event in listener.get_new_entries():
                    state_event = callback(event)
                    self.handler.queue_event(state_event)
            time.sleep(1)
        self.handler.queue_event(Event(CLIENT_STOPPED))

    def quit(self):
        self.stop = True

    def register_sender(self, msg_type, callback):
        self.senders[msg_type] = callback

    def send(self, message: Message):
        if message.type in self.senders:
            tx = self.senders[message.type](message, self.contracts)
            nonce = self.get_account_nonce()
            tx = tx.build_transaction({
                "nonce": nonce,
                #'maxFeePerGas': self.provider.toWei(2, "gwei"),
                #'maxPriorityFeePerGas': self.provider.toWei(1, "gwei"),
                #'gas': self.provider.toWei(0.003, "gwei")
            })
            signed_tx = self.account.sign_transaction(tx)
            self.provider.eth.send_raw_transaction(signed_tx.rawTransaction)
        else:
            print("No sender found for", message.type)

    def request_funds(self):
        self.provider.provider.make_request('hardhat_setBalance', [self.account.address, self.provider.toHex(self.provider.toWei(10, "ether"))])