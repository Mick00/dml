from torch.utils.data import Subset

from src.datasets.data_helpers import get_lower_bound, get_higher_bound
from src.protocol.states.state import State


def apply_target_subset(state: State, train_dataset, val_dataset, test_dataset):
    lower = get_lower_bound(state)
    upper = get_higher_bound(state)
    return target_subset(train_dataset, lower, upper), \
           target_subset(val_dataset, lower, upper), \
           target_subset(test_dataset, lower, upper)


def target_subset(dataset, lower, upper):
    mask = []
    for index, target in enumerate(dataset.targets):
        if lower <= target <= upper:
            mask.append(index)
    return Subset(dataset, mask)