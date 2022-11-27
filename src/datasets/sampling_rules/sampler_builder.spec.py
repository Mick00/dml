import unittest
from unittest.mock import Mock

import torch

from src.datasets.sampling_rules.balance import balanced_weight
from src.datasets.sampling_rules.sampler_builder import SamplerBuilder
from src.datasets.sampling_rules.rank import rank_subset
from src.datasets.sampling_rules.target import target_subset
from src.datasets.sampling_rules.val_split import val_split


class FilterBuilderTest(unittest.TestCase):

    def mock_dataset(self):
        dataset = Mock()
        self.targets = torch.Tensor([0, 1, 2, 3, 1, 1, 2, 2, 3, 1]).to(torch.int64)
        self.counts = torch.bincount(self.targets)
        dataset.targets = self.targets
        return dataset

    def test_init(self):
        ds = self.mock_dataset()
        sampler_builder = SamplerBuilder(ds)
        sampler_builder.apply(lambda data, weights: torch.zeros(len(weights)))
        self.assertEqual(sampler_builder.weights.sum(), 0)

    def test_num_samples(self):
        ds = self.mock_dataset()
        sampler_builder = SamplerBuilder(ds)
        self.assertEqual(sampler_builder.get_num_samples(), 10)
        num_samples = sampler_builder.set_num_samples(5).get_num_samples()
        self.assertEqual(num_samples, 5)

    def test_balance(self):
        ds = self.mock_dataset()
        sampler_builder = SamplerBuilder(ds)
        sampler_builder.apply(balanced_weight())
        # There are more 1 than 0 so weigth for 0 should be higher
        self.assertTrue(sampler_builder.weights[0] > sampler_builder.weights[1])
        self.assertEqual(sampler_builder.weights[0], 1)
        self.assertEqual(sampler_builder.weights[1], 1 / 4)

    def test_rank(self):
        ds = self.mock_dataset()
        sampler_builder = SamplerBuilder(ds)
        sampler_builder.apply(rank_subset(0, 2))
        self.assertEqual(sampler_builder.get_num_samples(), len(self.targets) / 2)

    def test_target(self):
        ds = self.mock_dataset()
        sampler_builder = SamplerBuilder(ds)
        sampler_builder.apply(target_subset(0, 2))
        self.assertEqual(sampler_builder.get_num_samples(), self.counts[0] + self.counts[1])

    def test_val_spli_train(self):
        ds = self.mock_dataset()
        sampler_builder = SamplerBuilder(ds)
        sampler_builder.apply(val_split(True, 0.8))
        self.assertEqual(sampler_builder.weights.sum(), 8)

    def test_val_split_val(self):
        ds = self.mock_dataset()
        sampler_builder = SamplerBuilder(ds)
        sampler_builder.apply(val_split(False, 0.65))
        self.assertEqual(sampler_builder.weights.sum(), 4)

if __name__ == '__main__':
    unittest.main()