import unittest
from unittest.mock import Mock

from mlflow import MlflowClient

from src.base.training.models.architectures.cae_lenet import CaeLeNet
from src.base.training.models.experiment import Experiment
from src.base.training.training_client import TrainingClient


class TrainingClientTest(unittest.TestCase):
    @unittest.skip
    def test_training_cpu(self):
        handler = Mock()
        training_client = TrainingClient('path', './test_training_out/', False, handler)
        model = Experiment("cluster_id", 10, CaeLeNet())
        training_client.train_model(model)

    @unittest.skip
    def test_training_gpu(self):
        handler = Mock()
        training_client = TrainingClient("my_trainer", handler,
                                         enable_gpu=True,
                                         dataset_path='path',
                                         output_dir="C:\\Users\\micdu\\Code\\pythonProject\\dmtl\\lightning_data",
                                         tracking_uri="http://localhost:5000"
                                         )
        model = CaeLeNet()
        wrapped_model = Experiment("cluster_id", 12, model)
        training_client.train_model(wrapped_model)

    @unittest.skip
    def test_get_checkpoint_path(self):
        model = Mock()
        model.model = Mock()
        model.model.logger = Mock()
        model.model.logger.experiment_id = "3"
        model.model.logger.run_id = "7836313061ad42ab8c06f9eb35083c14"
        handler = Mock()
        training_client = TrainingClient("my_trainer", handler,
                                         enable_gpu=True,
                                         dataset_path='path',
                                         output_dir="C:\\Users\\micdu\\Code\\pythonProject\\dmtl\\lightning_data",
                                         tracking_uri="http://localhost:5000"
                                         )
        checkpoint_path = training_client.get_checkpoint_path(model)

    @unittest.skip
    def test_test(self):
        handler = Mock()
        training_client = TrainingClient("my_trainer", handler,
                                         enable_gpu=True,
                                         dataset_path='path',
                                         output_dir="C:\\Users\\micdu\\Code\\pythonProject\\dmtl\\lightning_data",
                                         tracking_uri="http://localhost:5000"
                                         )
        model = CaeLeNet()
        wrapped_model = Experiment("cluster_id", 12, "cae_lenet", model)
        training_client.test_model(wrapped_model)

    @unittest.skip
    def test_get_runs(self):
        mlfClient = MlflowClient(tracking_uri="http://localhost:5000")
        runs = mlfClient.search_runs(experiment_ids=["2"], filter_string="tags.cluster_id = 'b67f4a677a254cfc0eda9fb6e044ef82'")
        print(runs)

    @unittest.skip
    def test_create_exp(self):
        mlfClient = MlflowClient(tracking_uri="http://localhost:5000")
        output = mlfClient.create_experiment("helloo", "C:\\Users\\micdu\\Code\\pythonProject\\dmtl\\lightning_data")
        print(output)

    def test_get_experiment_id(self):
        mlfClient = MlflowClient(tracking_uri="http://localhost:5000")
        id = mlfClient.get_experiment_by_name("helloo")
        print(id)
        id = mlfClient.get_experiment_by_name("non-existing")
        print(id)


if __name__ == '__main__':
    unittest.main()