import pandas as pd
import os

import torch
from pandas import DataFrame
from sklearn.model_selection import train_test_split
from torch.utils.data import Dataset

from src.base.datasets.data_helpers import get_data_path
from src.base.datasets.data_loader import get_data_loader
from src.base.states.event import Event
from src.base.states.event_listener import EventListener
from src.base.states.state import State
from src.base.states.event_handler import EventHandlerSimple


class CreditCardFraudRegister(EventHandlerSimple):
    def transition(self, event: Event, state: State, handler: EventListener):
        data_loader = get_data_loader(state)
        data_loader.register_loader("credit_card_fraud", lambda state: load_cc_fraud(get_data_path(state)))


class DataFrameDataset(Dataset):
    def __init__(self, x: DataFrame, y: DataFrame):
        self.x = torch.as_tensor(x.to_numpy(), dtype=torch.float32)
        self.targets = torch.as_tensor(y.to_numpy())

    def __len__(self):
        return len(self.targets)

    def __getitem__(self, idx):
        return self.x[idx], self.targets[idx]


def load_cc_fraud(data_path: str):
    if not data_path:
        raise Exception("Data path is not set")
    df = pd.read_csv(os.path.join(data_path, "creditcardfraud", "creditcard.csv"))
    x = df.drop(labels="Class", axis=1)
    y = df["Class"]
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=64)
    return DataFrameDataset(x_train, y_train), DataFrameDataset(x_test, y_test)