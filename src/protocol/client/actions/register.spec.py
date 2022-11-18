import unittest
from unittest.mock import Mock, patch

from src.protocol.client.actions.constants import REGISTER_MESSAGE, CONFIRM_REGISTRATION_MESSAGE, NEW_PEER
from src.protocol.client.actions.register import RegisterSenderTransition, Register, RegisterReceiverTransition
from src.protocol.client.actions.send import Send
from src.protocol.client.client_state_helpers import add_peer
from src.protocol.client.constants import CLIENT_SEND
from src.protocol.client.messages.message import Message
from src.protocol.states.handler import Handler
from src.protocol.states.state import State


class RegisterTest(unittest.TestCase):
    def test_send_register(self):
        transition = RegisterSenderTransition(0)
        handler = Handler()
        transition.transition(None, None, handler)
        event = handler.event_queue.get()
        self.assertEqual(event.type, CLIENT_SEND)
        self.assertEqual(event.data.type, REGISTER_MESSAGE)

    def test_receive_register(self):
        transition = RegisterReceiverTransition(0)
        peer_name = "test_id"
        msg = Message(peer_name, REGISTER_MESSAGE, -1)
        state = State()
        handler = Handler()
        transition.transition(msg, state, handler)
        send_confirmation = handler.event_queue.get()
        self.assertEqual(send_confirmation.type, CLIENT_SEND)
        self.assertEqual(send_confirmation.data.type, CONFIRM_REGISTRATION_MESSAGE)
        new_peer = handler.event_queue.get()
        self.assertEqual(new_peer.type, NEW_PEER)
        self.assertEqual(new_peer.data.registered_id, peer_name)

    def test_receive_already_register(self):
        peer_name = "test_id"
        msg = Message(peer_name, REGISTER_MESSAGE, -1)
        state = State()
        add_peer(state, peer_name)
        handler = Mock()
        transition = RegisterReceiverTransition(0)
        transition.transition(msg, state, handler)
        handler.queue_event.assert_not_called()

if __name__ == '__main__':
    unittest.main()