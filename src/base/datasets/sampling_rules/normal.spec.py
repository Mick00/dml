import unittest
from unittest.mock import Mock

import pandas as pd
import torch

from src.base.datasets.sampling_rules.normal import normal_probability_weights


class Normal(unittest.TestCase):

    def test_mask(self):
        dataset = Mock()
        size = 1000
        dataset.targets = torch.randint(low=0, high=10, size=(size,))
        weights = torch.ones(size)
        mask = normal_probability_weights(5, 1)
        normal_weights = mask(dataset, weights)
        df = pd.DataFrame(columns=["sample_class", "weight"], data=zip(dataset.targets.numpy(), normal_weights.numpy()))
        self.assertEqual(df.groupby("sample_class").sum().idxmax()["weight"], 5)

if __name__ == '__main__':
    unittest.main()