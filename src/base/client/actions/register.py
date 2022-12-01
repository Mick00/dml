from src.base.client.actions.confirm_registration import ConfirmRegistration
from src.base.client.actions.constants import REGISTER_MESSAGE
from src.base.client.actions.new_peer import NewPeer
from src.base.client.actions.send import Send
from src.base.client.client_state_helpers import add_peer, is_peer_registered
from src.base.client.messages.message import Message
from src.base.states.event_handler import EventHandler
from src.base.states.event import Event
from src.base.states.state import State
from src.base.states.event_listener import EventListener


class Register(Event):

    def __init__(self):
        super().__init__(REGISTER_MESSAGE)


class RegisterSenderTransition(EventHandler):
    def transition(self, event: Event, state: State, handler: EventListener):
        handler.queue_event(Send(Register()))


class RegisterReceiverTransition(EventHandler):
    def transition(self, event: Message, state: State, handler: EventListener):
        peer_id = event.from_id
        if is_peer_registered(state, peer_id):
            return
        add_peer(state, peer_id)
        handler.queue_event(Send(ConfirmRegistration(peer_id)))
        handler.queue_event(NewPeer(peer_id))

