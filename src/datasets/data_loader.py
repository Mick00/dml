from torch.utils.data import random_split

from src.datasets.data_helpers import get_dataset, get_data_module
from src.protocol.states.state import State


class DataLoader:
    def __init__(self):
        self.loaders_fn = {}
        self.subset_fn = None

    def register_loader(self, key: str, fn):
        self.loaders_fn[key] = fn

    def set_subset(self, fn):
        self.subset_fn = fn

    def load_data(self, state: State):
        loader_fn = self.loaders_fn.get(get_dataset(state))
        train_dataset, test_dataset = loader_fn(state)
        train_dataset, val_dataset = self.split(train_dataset, 0.85)
        if callable(self.subset_fn):
            train_dataset, val_dataset, test_dataset = self.subset_fn(state, train_dataset, val_dataset, test_dataset)
        return train_dataset, val_dataset, test_dataset

    def split(self, dataset, split: float):
        train_set_size = int(len(dataset) * split)
        valid_set_size = len(dataset) - train_set_size
        train_dataset, val_dataset = random_split(dataset, [train_set_size, valid_set_size])
        return train_dataset, val_dataset


DATALOADER_KEY = "data_loader"


def get_data_loader(state: State) -> DataLoader:
    return get_data_module(state).get(DATALOADER_KEY)