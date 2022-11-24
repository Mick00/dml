from collections import OrderedDict
from typing import Any

import torch
from torch import nn


def calc_diff(og_model: nn.Module, updated_model: nn.Module) -> OrderedDict:
    og_state = og_model.state_dict()
    updated_state = updated_model.state_dict()
    diff = OrderedDict()
    for layer in og_state:
        diff[layer] = updated_state[layer] - og_state[layer]
    return diff


def apply_diff(model: nn.Module, diff: OrderedDict) -> nn.Module:
    og_state = model.state_dict()
    for layer in og_state:
        og_state[layer] = og_state[layer] + diff[layer]
    model.load_state_dict(og_state)
    return model


def avg_dict(state_0: dict[str, Any], state_1: dict[str, Any], n=1) -> OrderedDict:
    merged = OrderedDict()
    for layer in state_0:
        l0 = state_0[layer] * n
        l1 = state_1[layer]
        merged[layer] = (l0 + l1) / (n + 1)
    return merged


def merge_models(model_0: nn.Module, model_1: nn.Module, n=1):
    state_0 = model_0.state_dict()
    state_1 = model_1.state_dict()
    merged = avg_dict(state_0, state_1, n)
    model_0.load_state_dict(merged)
    return model_0


def avg_models(main, models, n=0):
    for i in range(n, len(models)):
        main = merge_models(main, models[i], n=i)
    return main


def clone_into(model, to_clone):
    model.load_state_dict(to_clone.state_dict(), strict=False)
    return model


def weight_divergence(model_0, model_1):
    diff = calc_diff(model_0, model_1)
    total_divergence = 0
    for layer in diff:
        div = torch.cumsum(torch.abs(diff[layer]), dim=0)
        total_divergence += div.sum()
    return total_divergence

#def EMD(p, q):
#    x = p - q
#    y = torch.cumsum(x, dim=0)
#    return torch.abs(y).sum()