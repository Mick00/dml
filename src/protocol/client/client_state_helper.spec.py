import unittest
from unittest.mock import Mock

from src.protocol.client.client_state_helpers import init_client, get_node_id, client_is_started, is_peer_registered, add_peer, \
    get_peers, get_round_id, update_round_id
from src.protocol.states.state import State


class ClientStateHelperTest(unittest.TestCase):
    def test_init_client(self):
        client = Mock()
        client.id = "test"
        state = State()
        init_client(state, client)
        self.assertEqual(get_node_id(state), "test")
        self.assertEqual(client_is_started(state), True)

    def test_peers(self):
        state = State()
        peer0 = "peer0"
        peer1 = "peer1"
        peer2 = "peer2"
        self.assertFalse(is_peer_registered(state, peer0))
        add_peer(state, peer0)
        self.assertTrue(is_peer_registered(state, peer0))
        self.assertFalse(is_peer_registered(state, peer1))
        add_peer(state, peer1)
        self.assertTrue(is_peer_registered(state, peer1))
        self.assertFalse(is_peer_registered(state, peer2))
        self.assertEqual(len(get_peers(state)), 2)

    def test_get_round_id(self):
        state = State()
        self.assertEqual(get_round_id(state), -1)
        update_round_id(state, 0)
        self.assertEqual(get_round_id(state), 0)


if __name__ == '__main__':
    unittest.main()