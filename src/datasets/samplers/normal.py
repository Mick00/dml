import torch
from scipy.stats import norm

from src.datasets.samplers.balance import balanced_weight


def normal_probability_weights(dataset, mean, std):
    balanced_sample_weights = balanced_weight(dataset)
    normalized_weights = [balanced_sample_weights[i] * norm.pdf(target, loc=mean, scale=std) for i, target in enumerate(dataset.targets)]
    return torch.Tensor(normalized_weights)
