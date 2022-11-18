import unittest

from src.protocol.client.actions.constants import NEW_PEER
from src.protocol.client.actions.new_peer import NewPeer
from src.protocol.client.actions.send import Send
from src.protocol.client.constants import CLIENT_SEND


class SendTest(unittest.TestCase):
    def test_send_register(self):
        peer_name = "test_peer"
        new_peer = NewPeer(peer_name)
        send = Send(new_peer)
        self.assertEqual(send.type, CLIENT_SEND)
        self.assertEqual(send.data.type, NEW_PEER)



if __name__ == '__main__':
    unittest.main()