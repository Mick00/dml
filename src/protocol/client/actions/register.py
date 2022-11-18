from src.protocol.client.actions.confirm_registration import ConfirmRegistration
from src.protocol.client.actions.constants import REGISTER_MESSAGE
from src.protocol.client.actions.new_peer import NewPeer
from src.protocol.client.actions.send import Send
from src.protocol.client.client_state_helpers import add_peer, is_peer_registered
from src.protocol.client.messages.message import Message
from src.protocol.states.transition import StateTransition
from src.protocol.states.event import Event
from src.protocol.states.state import State
from src.protocol.states.handler import Handler


class Register(Event):

    def __init__(self):
        super().__init__(REGISTER_MESSAGE)


class RegisterSenderTransition(StateTransition):
    def transition(self, event: Event, state: State, handler: Handler):
        handler.queue_event(Send(Register()))


class RegisterReceiverTransition(StateTransition):
    def transition(self, event: Message, state: State, handler: Handler):
        peer_id = event.from_id
        if is_peer_registered(state, peer_id):
            return
        add_peer(state, peer_id)
        handler.queue_event(Send(ConfirmRegistration(peer_id)))
        handler.queue_event(NewPeer(peer_id))

