import torch


def val_split(train, ratio):
    def weight_filter(dataset, weights):
        enabled = weights.gt(0)
        total = enabled.sum()
        train_size = total * ratio
        enabled_acc = 0
        cutoff_index = 0
        for i, e in enumerate(enabled):
            if e:
                enabled_acc += 1
                cutoff_index = i
            if enabled_acc >= train_size:
                break
        if train:
            weights[cutoff_index + 1:] = torch.zeros(len(weights) - cutoff_index - 1)
        else:
            weights[0:cutoff_index] = torch.zeros(cutoff_index)
        return weights
    return weight_filter