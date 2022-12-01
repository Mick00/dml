import unittest
from unittest.mock import Mock

from src.base.training.fedml.model_update_meta import ModelUpdateMeta
from src.base.training.fedml.update_queue import UpdateQueue


class ModelLoaderTest(unittest.TestCase):
    def test_get_queue(self):
        handler = Mock()
        queue = UpdateQueue(handler)
        q = queue.get_queue(0)
        self.assertEqual(q, [])
        self.assertTrue(queue.get_queue(0) is q)
        self.assertEqual(len(q), 0)

    def test_queue(self):
        handler = Mock()
        updates = UpdateQueue(handler)
        cluster_id = "test_cluster"
        round_id = 0
        model_name = "test_model"
        updates.queue(ModelUpdateMeta(cluster_id, round_id, model_name, "./path/to.ckpt", "trainer_0"))
        updates.queue(ModelUpdateMeta(cluster_id, round_id, model_name, "./diff_path/to.ckpt", "trainer_1"))
        self.assertEqual(len(updates.get_queue(0)), 2)

    def test_unique_clusters(self):
        handler = Mock()
        updates = UpdateQueue(handler)
        cluster_id = "test_cluster"
        round_id = 0
        model_name = "test_model"
        updates.queue(ModelUpdateMeta(cluster_id, round_id, model_name, "./path/to.ckpt", "trainer_0"))
        updates.queue(ModelUpdateMeta(cluster_id, round_id, model_name, "./diff_path/to.ckpt", "trainer_1"))
        self.assertEqual(list(updates.get_unique_clusters(0)), [cluster_id])


if __name__ == '__main__':
    unittest.main()