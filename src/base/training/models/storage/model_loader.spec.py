import os
import shutil
import unittest

import torch

from src.base.training.models.storage.model_loader import ModelLoader
from src.base.training.models.model_factory import create_model

TEST_SAVE_PATH = "C:\\Users\\micdu\\Code\\pythonProject\\dmtl\\save_test_model\\"
MODEL_NAME = "cae_lenet"

class ModelLoaderTest(unittest.TestCase):

    def setUp(self) -> None:
        os.mkdir(TEST_SAVE_PATH)
        self.model0 = create_model(MODEL_NAME)
        self.save_0 = TEST_SAVE_PATH+"model_0.state"
        torch.save(self.model0.state_dict(), self.save_0)

    def test_get_cluster(self):
        model_loader = ModelLoader(TEST_SAVE_PATH)
        cluster_id = "test_id"
        cluster0 = model_loader.get_cluster(cluster_id)
        cluster1 = model_loader.get_cluster(cluster_id)
        self.assertEqual(cluster0, cluster1)

    def test_genesis(self):
        model_loader = ModelLoader(TEST_SAVE_PATH)
        cluster_id = "my_cluster"
        model_loader.set_cluster_genesis(cluster_id, MODEL_NAME, self.save_0)
        loaded_model = model_loader.get_model(cluster_id, 0)
        self.assertTrue(torch.equal(
            loaded_model.state_dict().get("encoder.0.conv.0.weight"),
            self.model0.state_dict().get("encoder.0.conv.0.weight")
        ))
        self.assertFalse(self.model0 is loaded_model)

    def test_get_model_from_previous_round(self):
        model_loader = ModelLoader(TEST_SAVE_PATH)
        cluster_id = "my_cluster"
        model_loader.set_cluster_genesis(cluster_id, MODEL_NAME, self.save_0)
        loaded_model = model_loader.get_model(cluster_id, 1)
        # No updates added so the model will be the same
        self.assertTrue(torch.equal(
            loaded_model.state_dict().get("encoder.0.conv.0.weight"),
            self.model0.state_dict().get("encoder.0.conv.0.weight")
        ))
        cluster = model_loader.get_cluster(cluster_id)
        round_0 = cluster.get_round(0)
        round_1 = cluster.get_round(1)
        self.assertNotEqual(round_0.start_model, round_1.start_model)
        self.assertEqual(round_0.final_model, round_1.start_model)

    def tearDown(self) -> None:
        shutil.rmtree(TEST_SAVE_PATH)

if __name__ == '__main__':
    unittest.main()