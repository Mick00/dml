import torch
from torch.utils.data import Dataset, WeightedRandomSampler


class SamplerBuilder:
    weights: torch.Tensor

    def __init__(self, dataset: Dataset, num_samples=0):
        self.dataset = dataset
        self.weights = torch.ones(len(self.dataset.targets))
        self.num_samples = num_samples

    def apply(self, weight_fn):
        self.weights = weight_fn(self.dataset, self.weights)
        return self

    def set_num_samples(self, num_samples):
        self.num_samples = num_samples
        return self

    def get_num_samples(self):
        return int(self.num_samples if self.num_samples > 0 else (self.weights > 0).sum())

    def sampler(self):
        return WeightedRandomSampler(weights=self.weights, num_samples=self.get_num_samples())

    def copy(self):
        copied = SamplerBuilder(self.dataset, self.num_samples)
        copied.weights.copy_(self.weights)
        return copied
