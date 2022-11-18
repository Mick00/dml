import unittest

from src.protocol.training.models.storage.cluster import Cluster


class ModelLoaderTest(unittest.TestCase):
    def test_init(self):
        cluster = Cluster("cluster_id", "save_path")
        self.assertEqual(cluster.cluster_id, "cluster_id")
        self.assertEqual(cluster.save_path, "save_path")
        self.assertEqual(len(cluster.rounds.keys()), 0)

    def test_round_init(self):
        cluster = Cluster("cluster_id", "save_path")
        model_name = "model_name"
        round_id = 100
        round = cluster.init_round(round_id, model_name)
        self.assertTrue(cluster.round_exists(round_id))
        self.assertEqual(round.round_id, round_id)
        self.assertEqual(round.model_name, model_name)
        self.assertTrue(cluster.get_round(round_id) is round)

    def test_round_not_exists(self):
        cluster = Cluster("cluster_id", "save_path")
        self.assertFalse(cluster.round_exists(10))


if __name__ == '__main__':
    unittest.main()