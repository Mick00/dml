import unittest
from unittest.mock import Mock

import torch
from torch import nn

from src.protocol.training.models.operations import merge_models, clone_into, calc_diff, apply_diff, weight_divergence


class OperationsTest(unittest.TestCase):

    def create_model(self):
        return nn.Sequential(
            nn.Linear(4, 2),
            nn.ReLU(),
            nn.Linear(2, 1)
        )

    def test_merge_models_ignore_target(self):
        model0 = self.create_model()
        model1 = self.create_model()
        avg = merge_models(model0, model1, n=0)
        self.assertTrue(torch.equal(avg.state_dict()["0.weight"], model1.state_dict()["0.weight"]))

    def test_merge_additive(self):
        model0 = self.create_model()
        model1 = self.create_model()
        weights_avg = (model1.state_dict()["0.weight"] + model0.state_dict()["0.weight"]) / 2
        avg = merge_models(model0, model1)
        avg_weights = avg.state_dict()["0.weight"]
        self.assertFalse(torch.equal(avg_weights, model1.state_dict()["0.weight"]))
        self.assertTrue(torch.equal(avg_weights, weights_avg))

    def test_clone_into(self):
        model0 = self.create_model()
        model1 = self.create_model()
        cloned = clone_into(model0, model1)
        self.assertTrue(torch.equal(cloned.state_dict()["0.weight"], model1.state_dict()["0.weight"]))
        self.assertTrue(cloned is not model1)
        self.assertTrue(cloned is model0)

    def test_calc_update(self):
        model0 = self.create_model()
        model1 = self.create_model()
        diff = calc_diff(model0, model1)
        model0 = apply_diff(model0, diff)
        self.assertTrue(torch.equal(model0.state_dict()["0.weight"], model1.state_dict()["0.weight"]))

    def test_weight_divergence(self):
        model_0 = nn.Linear(2, 1)
        model_0.load_state_dict({
            "weight": torch.Tensor([[2, 2]]),
            "bias": torch.Tensor([3]),
        })
        model_1 = nn.Linear(2, 1)
        model_1.load_state_dict({
            "weight": torch.Tensor([[5, 5]]),
            "bias": torch.Tensor([2]),
        })
        divergence = weight_divergence(model_0, model_1)
        self.assertEqual(divergence, 7)

if __name__ == '__main__':
    unittest.main()