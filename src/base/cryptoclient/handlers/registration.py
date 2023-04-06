from src.base.client.actions.constants import REGISTER_MESSAGE
from src.base.client.actions.new_peer import NewPeer
from src.base.client.client_state_helpers import is_peer_registered, add_peer, get_node_id
from src.base.client.messages.message import Message
from src.base.cryptoclient.crypto_client_state_helper import get_crypto_client
from src.base.states.event import Event
from src.base.states.event_handler import EventHandlerSimple, Handler
from src.base.states.event_listener import EventListener
from src.base.states.state import State

class RegisterTransaction(EventHandlerSimple):
    def transition(self, event: Event, state: State, handler: Handler):
        client = get_crypto_client(state)
        client.request_funds()
        event_listener = client.contracts["trainers"].events["TrainerRegistered"].createFilter(fromBlock=0)

        def event_handler(event):
            my_id = get_node_id(state)
            if my_id != event.args.trainer:
                handler.queue_event(NewPeer(event.args.trainer))
        client.register_events(event_listener, event_handler)

        def register(message, contracts):
            return contracts["trainers"].functions.register()

        client.register_sender(REGISTER_MESSAGE, register)


class RegisterReceiverTransition(EventHandlerSimple):
    def transition(self, event: Message, state: State, handler: EventListener):
        peer_id = event.data.registered_id
        if is_peer_registered(state, peer_id):
            return
        add_peer(state, peer_id)