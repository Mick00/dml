import unittest
from unittest.mock import Mock

from src.base.client.actions.confirm_registration import ConfirmRegistration, ConfirmRegistrationReceiverTransition
from src.base.client.actions.constants import NEW_PEER, CONFIRM_REGISTRATION_MESSAGE
from src.base.client.actions.new_peer import NewPeer
from src.base.client.client_state_helpers import init_client, add_peer, is_peer_registered
from src.base.client.messages.message import wrap_event
from src.base.states.event_listener import EventListener
from src.base.states.state import State


class ConfirmRegistrationTest(unittest.TestCase):

    def setUp(self) -> None:
        self.state = State()
        client = Mock()
        self.my_id = "my_id"
        client.id = self.my_id
        init_client(self.state, client)
        self.handler = Mock()

    def test_confirm_registration_event(self):
        peer_id = "test_id"
        confirm_registration = ConfirmRegistration("%s" % peer_id)
        self.assertEqual(confirm_registration.type, CONFIRM_REGISTRATION_MESSAGE)
        self.assertEqual(confirm_registration.data.registered_id, peer_id)

    def test_should_ignore_unrelated_confirmation(self):
        confirm_registration = ConfirmRegistration("not_my_id")
        message = wrap_event("sender_id", -1, confirm_registration)
        transition = ConfirmRegistrationReceiverTransition(0)
        transition.transition(message, self.state, self.handler)
        self.handler.queue_event.assert_not_called()

    def test_should_ignore_if_already_added(self):
        confirm_registration = ConfirmRegistration(self.my_id)
        sender_id = "sender_id"
        add_peer(self.state, sender_id)
        message = wrap_event(sender_id, -1, confirm_registration)
        transition = ConfirmRegistrationReceiverTransition(0)
        transition.transition(message, self.state, self.handler)
        self.handler.queue_event.assert_not_called()

    def test_should_add_peer(self):
        confirm_registration = ConfirmRegistration(self.my_id)
        sender_id = "sender_id"
        message = wrap_event(sender_id, -1, confirm_registration)
        handler = EventListener()
        transition = ConfirmRegistrationReceiverTransition(0)
        transition.transition(message, self.state, handler)
        self.assertTrue(is_peer_registered(self.state, sender_id))
        new_peer = handler.event_queue.get()
        self.assertEqual(new_peer.type, NEW_PEER)
        self.assertEqual(new_peer.data.registered_id, sender_id)


if __name__ == '__main__':
    unittest.main()