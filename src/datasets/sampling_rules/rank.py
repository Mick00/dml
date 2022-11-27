import torch


def rank_subset(rank: int, n_peers: int):
    def weight_calc(dataset, weights):
        dataset_len = len(dataset.targets)
        selected_weights = torch.zeros(dataset_len)
        for i in range(rank, len(dataset.targets), n_peers):
            selected_weights[i] = weights[i]
        return selected_weights
    return weight_calc
