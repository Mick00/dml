from src.base.client.actions.constants import CONFIRM_REGISTRATION_MESSAGE
from src.base.client.actions.new_peer import NewPeer
from src.base.client.client_state_helpers import add_peer, get_round_id, update_round_id, \
    is_peer_registered, get_node_id
from src.base.states.event import Event
from src.base.states.state import State
from src.base.states.event_listener import EventListener
from src.base.states.event_handler import EventHandlerSimple
from src.base.client.messages.message import Message


class ConfirmRegistration(Event):

    def __init__(self, registered_id: str):
        super(ConfirmRegistration, self).__init__(
            CONFIRM_REGISTRATION_MESSAGE,
            {"registered_id": registered_id}
        )


class ConfirmRegistrationReceiverTransition(EventHandlerSimple):
    def transition(self, msg: Message, state: State, handler: EventListener):

        peer_id = msg.from_id
        if is_peer_registered(state, peer_id):
            return

        add_peer(state, peer_id)
        handler.queue_event(NewPeer(peer_id))
        round_id = msg.round_id
        if get_round_id(state) < 0:
            update_round_id(state, round_id)
