import unittest
from unittest.mock import Mock

from src.base.datasets.data_helpers import get_int_use_rank


class FilterBuilderTest(unittest.TestCase):

    def mocked_state(self, rank, field_value):
        state = Mock()
        state.get_module_state.return_value = {"rank": rank, "field": field_value}
        return state

    def test_get_int_use_rank_array(self):
        state = self.mocked_state(5, '[1, 2, 3]')
        value = get_int_use_rank(state, "field")
        self.assertEqual(value, 3)

    def test_get_int_use_rank_number(self):
        state = self.mocked_state(9, '1')
        value = get_int_use_rank(state, "field")
        self.assertEqual(value, 1)

    def test_get_int_use_rank_neg_umber(self):
        state = self.mocked_state(9, '-1')
        value = get_int_use_rank(state, "field")
        self.assertEqual(value, -1)

if __name__ == '__main__':
    unittest.main()