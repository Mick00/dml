from src.base.datasets.data_helpers import get_dataset, get_data_module
from src.base.datasets.sampling_rules.sampler_builder import SamplerBuilder
from src.base.datasets.sampling_rules.val_split import val_split
from src.base.states.state import State


class DataLoader:
    def __init__(self, train_ratio=0.85):
        self.train_ratio = train_ratio
        self.loaders_fn = {}
        self.sampling_rules = []
        self.subset_fn = None
        self.train_dataset = None
        self.test_dataset = None
        self.train_sampler = None
        self.val_sampler = None
        self.test_sampler = None
        self.sampler_tags = {}
        self.n_samples = 0

    def register_loader(self, key: str, fn):
        self.loaders_fn[key] = fn

    def set_sampling_rules(self, sampling_rules):
        self.sampling_rules = sampling_rules

    def set_sampler_tags(self, tags: dict):
        self.sampler_tags = tags

    def add_sampler_tags(self, tags: dict):
        self.sampler_tags = self.sampler_tags | tags

    def set_n_samples(self, n_samples):
        self.n_samples = n_samples

    def load_data(self, state: State) -> str:
        dataset = get_dataset(state)
        loader_fn = self.loaders_fn.get(dataset)
        self.train_dataset, self.test_dataset = loader_fn(state)
        train_sampler = self.get_sampler(self.train_dataset)
        self.test_sampler = self.get_sampler(self.test_dataset)
        self.train_sampler = train_sampler.copy()\
            .apply(val_split(True, self.train_ratio))\
            .set_num_samples(self.n_samples)
        self.val_sampler = train_sampler.copy().apply(val_split(False, self.train_ratio))
        return dataset

    def get_sampler(self, dataset):
        sampler_builder = SamplerBuilder(dataset)
        for sample_rule in self.sampling_rules:
            sampler_builder.apply(sample_rule)
        return sampler_builder

    def get_train_data(self):
        return self.train_dataset, self.train_sampler.sampler()

    def get_val_data(self):
        return self.train_dataset, self.val_sampler.sampler()

    def get_test_data(self):
        return self.test_dataset, self.test_sampler.sampler()


DATALOADER_KEY = "data_loader"


def get_data_loader(state: State) -> DataLoader:
    return get_data_module(state).get(DATALOADER_KEY)