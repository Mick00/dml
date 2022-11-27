from torch.utils.data import Subset

from src.protocol.client.client_state_helpers import get_node_rank, get_peers
from src.protocol.states.state import State


def apply_rank_subset(state: State, train_dataset, val_dataset, test_dataset):
    rank = get_node_rank(state)
    n_peers = len(get_peers(state)) + 1
    return rank_subset(train_dataset, rank, n_peers), \
           rank_subset(val_dataset, rank, n_peers), \
           rank_subset(test_dataset, rank, n_peers)


def rank_subset(dataset, rank: int, n_peers: int):
    return Subset(dataset, list(range(rank, len(dataset.targets), n_peers)))
