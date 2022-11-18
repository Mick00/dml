import unittest
from unittest.mock import Mock

import torch
from torch import nn

from src.protocol.training.models.operations import merge_models, clone_into, calc_diff, apply_diff


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


if __name__ == '__main__':
    unittest.main()