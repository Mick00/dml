from src.protocol.client.actions.constants import CONFIRM_REGISTRATION_MESSAGE
from src.protocol.client.actions.new_peer import NewPeer
from src.protocol.client.client_state_helpers import add_peer, get_round_id, update_round_id, \
    is_peer_registered, get_node_id
from src.protocol.states.event import Event
from src.protocol.states.state import State
from src.protocol.states.handler import Handler
from src.protocol.states.transition import StateTransition
from src.protocol.client.messages.message import Message


class ConfirmRegistration(Event):

    def __init__(self, registered_id: str):
        super(ConfirmRegistration, self).__init__(
            CONFIRM_REGISTRATION_MESSAGE,
            {"registered_id": registered_id}
        )


class ConfirmRegistrationReceiverTransition(StateTransition):
    def transition(self, msg: Message, state: State, handler: Handler):
        for_peer = msg.data.registered_id
        if for_peer != get_node_id(state):
            return

        peer_id = msg.from_id
        if is_peer_registered(state, peer_id):
            return

        add_peer(state, peer_id)
        handler.queue_event(NewPeer(peer_id))
        round_id = msg.round_id
        if get_round_id(state) < 0:
            update_round_id(state, round_id)
