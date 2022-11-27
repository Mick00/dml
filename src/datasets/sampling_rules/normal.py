import torch
from scipy.stats import norm


def normal_probability_weights(mean, std):
    def weight_calc(dataset, weights):
        probabilities = torch.Tensor([norm.pdf(target, loc=mean, scale=std) for target in dataset.targets])
        return weights * probabilities
    return weight_calc
