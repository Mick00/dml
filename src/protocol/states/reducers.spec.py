import unittest
from unittest.mock import Mock, patch

from src.protocol.states.reducers import StartHandler, StopHandler
from src.protocol.states.state import State
from src.protocol.states.constants import HANDLER_MODULE


class ReducersTest(unittest.TestCase):

    def setUp(self) -> None:
        self.state = State()
        self.handler = Mock()


    def test_start_handler_reducer(self):
        start_reducer = StartHandler(0)
        start_reducer.transition(None, self.state, self.handler)
        self.handler.handle_events.assert_called()
        self.assertTrue(self.state.get_module_state(HANDLER_MODULE)["started"], True)
        self.assertIsNotNone(self.state.get_module_state(HANDLER_MODULE)["thread"])

    def test_stop_handler_reducer(self):
        start_reducer = StopHandler(0)
        start_reducer.transition(None, self.state, self.handler)
        self.assertFalse(self.state.get_module_state(HANDLER_MODULE)["started"], False)


if __name__ == '__main__':
    unittest.main()