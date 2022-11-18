import unittest

from src.protocol.client.actions.constants import NEW_PEER
from src.protocol.client.actions.new_peer import NewPeer


class NewPeerTest(unittest.TestCase):
    def test_send_register(self):
        peer_name = "test_peer"
        new_peer = NewPeer(peer_name)
        self.assertEqual(new_peer.type, NEW_PEER)
        self.assertEqual(new_peer.data.registered_id, peer_name)


if __name__ == '__main__':
    unittest.main()