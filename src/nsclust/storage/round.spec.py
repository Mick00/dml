import os
import shutil
import unittest
from unittest.mock import Mock

import torch
from torch import nn

from src.protocol.training.models.storage.round import Round
from src.protocol.training.models.operations import calc_diff

TEST_SAVE_PATH = "C:\\Users\\micdu\\Code\\pythonProject\\dmtl\\save_test_model\\"


def get_model(ignored=""):
    return nn.Sequential(
        nn.Linear(4, 2),
        nn.ReLU(),
        nn.Linear(2, 1)
    )


def clear_test_path():
    shutil.rmtree(TEST_SAVE_PATH)
    os.mkdir(TEST_SAVE_PATH)


class RoundTest(unittest.TestCase):

    def setUp(self) -> None:
        os.mkdir(TEST_SAVE_PATH)
        os.mkdir(TEST_SAVE_PATH + "round_cluster_id")
        self.model0 = get_model()
        self.save_0 = TEST_SAVE_PATH+"model_0"
        torch.save(self.model0.state_dict(), self.save_0)
        model1 = get_model()
        self.diff_0_path = TEST_SAVE_PATH + "diff_1"
        self.diff_0 = calc_diff(self.model0, model1)
        torch.save(self.diff_0, self.diff_0_path)
        model2 = get_model()
        self.diff_1_path = TEST_SAVE_PATH + "diff_2"
        self.diff_1 = calc_diff(self.model0, model2)
        torch.save(self.diff_1, self.diff_1_path)
        model3 = get_model()
        self.diff_2_path = TEST_SAVE_PATH + "diff_3"
        self.diff_2 = calc_diff(self.model0, model3)
        torch.save(self.diff_2, self.diff_2_path)

    def create_round(self):
        round = Round("test_model", 1, TEST_SAVE_PATH + "round_cluster_id")
        round.create_model = Mock(name="method")
        round.create_model = get_model
        return round

    def test_innit(self):
        name = "model_name"
        id = 10
        path = "test_path"
        round = Round(name, id, path)
        self.assertEqual(round.model_name, name)
        self.assertEqual(round.round_id, id)
        self.assertEqual(round.save_path, path)

    def test_round_no_start_model(self):
        round = self.create_round()
        start_model = round.get_start_model()
        self.assertTrue("0.weight" in start_model.state_dict())

    def test_round_start_model(self):
        round = self.create_round()
        round.start_model = self.save_0
        start_model = round.get_start_model()
        self.assertTrue(torch.equal(self.model0.state_dict()["0.weight"], start_model.state_dict()["0.weight"]))

    def test_round_final_model_saved(self):
        round = self.create_round()
        round.final_model = self.save_0
        final_model = round.get_final_model()
        self.assertTrue(torch.equal(self.model0.state_dict()["0.weight"], final_model.state_dict()["0.weight"]))

    def test_compute_final_model(self):
        round = self.create_round()
        round.start_model = self.save_0
        round.add_update(self.diff_0_path)
        round.add_update(self.diff_1_path)
        round.add_update(self.diff_2_path)
        avg_update = (self.diff_0["0.weight"] + self.diff_1["0.weight"] + self.diff_2["0.weight"]) / 3
        start_model = round.get_start_model()
        expected_final_layer = start_model.state_dict()["0.weight"] + avg_update
        final_model = round.compute_final_model()
        self.assertTrue(torch.equal(final_model.state_dict()["0.weight"], expected_final_layer))

    def test_get_final_model_should_cache(self):
        round = self.create_round()
        round.start_model = self.save_0
        round.add_update(self.diff_0_path)
        round.add_update(self.diff_1_path)
        round.add_update(self.diff_2_path)
        final_model = round.get_final_model()
        self.assertTrue(os.path.exists(round.get_final_save_path()))
        loaded_final_model = round.get_final_model()
        self.assertFalse(final_model is loaded_final_model)
        self.assertTrue(torch.equal(final_model.state_dict()["0.weight"], loaded_final_model.state_dict()["0.weight"]))

    def test_cache_final(self):
        round = self.create_round()
        round.start_model = self.save_0
        round.add_update(self.diff_0_path)
        round.add_update(self.diff_1_path)
        round.add_update(self.diff_2_path)
        final_model = round.cache_final_model()
        final_model = round.cache_final_model()

    def tearDown(self) -> None:
        shutil.rmtree(TEST_SAVE_PATH)

if __name__ == '__main__':
    unittest.main()