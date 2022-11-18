import unittest

from src.protocol.training.experiment_tracking import ExperimentTracking


class TrainingClientTest(unittest.TestCase):
    def test_training_cpu(self):
        tracker = ExperimentTracking(
            tracking_uri="http://localhost:5000",
            output_location="C:\\Users\\micdu\\Code\\pythonProject\\dmtl\\lightning_data",
        )
        tracker.init("declust")
        self.assertTrue("declust" in tracker.exp_name_to_id)

    def test_get_tests(self):
        tracker = ExperimentTracking(
            tracking_uri="http://localhost:5000",
            output_location="C:\\Users\\micdu\\Code\\pythonProject\\dmtl\\lightning_data",
        )
        tracker.init("declust")
        runs = tracker.search(
            "declust",
            trainer_id="173243aeff8d41c2a6d1d00b46dc78cd",
            round_id="1",
            test=True)
        print(runs)


if __name__ == '__main__':
    unittest.main()