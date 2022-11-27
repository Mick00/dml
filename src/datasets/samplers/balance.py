import torch


def balanced_weight(dataset):
    counts = torch.bincount(dataset.targets)
    weights = 1 / counts
    return torch.tensor([weights[label] for label in dataset.targets])