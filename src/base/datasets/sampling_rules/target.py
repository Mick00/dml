import torch


def target_subset(lower, upper):
    def filter_samples(dataset, weights):
        under_lower = dataset.targets.lt(lower)
        above_upper = dataset.targets.ge(upper)
        not_in_range = torch.logical_or(under_lower, above_upper)
        return weights.masked_fill_(not_in_range, 0)
    return filter_samples