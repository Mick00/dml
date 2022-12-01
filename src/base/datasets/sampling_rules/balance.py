import torch


def balanced_weight():
    def weight_calc(dataset, weights):
        counts = torch.bincount(dataset.targets)
        relative_weights = 1 / counts
        return torch.tensor([relative_weights[label] for label in dataset.targets]) * weights
    return weight_calc
