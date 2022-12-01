import os.path
import secrets
import unittest

from src.daeclust.strategy import compute_cluster_id, AggregationStrategy
from src.base.training.fedml.model_update_meta import ModelUpdateMeta


class StrategyTest(unittest.TestCase):

    def test_compute_cluster_id(self):
        parent_id = '1db631f4d32315cc'
        id0 = 'd1046a79eb1e3fae54c8371316dee4a2'
        id1 = '3bb8f98ff0ce9be25a8d11ff50a66a9d'
        cluster_id_0 = compute_cluster_id(parent_id, [id0, id1])
        cluster_id_1 = compute_cluster_id(parent_id, [id1, id0])
        print(cluster_id_0)
        self.assertEqual(cluster_id_0, cluster_id_1)
        self.assertEqual(cluster_id_0, '63e0297050fe9cc328c058077aa716603e2310f6dcb8f31c34458c377b769ad6')

    def test_add_cluster(self):
        strategy = AggregationStrategy("C:\\Users\\micdu\\Code\\pythonProject\\dmtl\\lightning_data", "cae_lenet")
        round_id = 0
        update0 = self.create_update(round_id=round_id)
        update1 = self.create_update(round_id=round_id)
        update2 = self.create_update(round_id=round_id)
        strategy.init_round(round_id)
        strategy.for_round(round_id).update_pools.add_update(update0)
        strategy.for_round(round_id).update_pools.add_update(update1)
        strategy.for_round(round_id).update_pools.add_update(update2)
        new_cluster_id = strategy.add_cluster(round_id, update0.cluster_id, [update0.from_id])
        new_cluster = strategy.for_round(round_id).clusters.get(new_cluster_id)
        self.assertEqual(new_cluster.update_paths, [update0.checkpoint_uri])
        selected_cluster = update0
        round_id += 1
        update0 = self.create_update(cluster_id=selected_cluster.cluster_id, round_id=round_id)
        update1 = self.create_update(cluster_id=selected_cluster.cluster_id, round_id=round_id)
        update2 = self.create_update(cluster_id=selected_cluster.cluster_id, round_id=round_id)
        strategy.init_round(round_id)
        strategy.for_round(round_id).update_pools.add_update(update0)
        strategy.for_round(round_id).update_pools.add_update(update1)
        strategy.for_round(round_id).update_pools.add_update(update2)
        new_cluster_id = strategy.add_cluster(round_id, selected_cluster.cluster_id, [update0.from_id, update1.from_id])
        cluster_id = compute_cluster_id(selected_cluster.cluster_id, [update0.from_id, update1.from_id])
        self.assertEqual(new_cluster_id, cluster_id)
        new_cluster = strategy.for_round(round_id).clusters.get(new_cluster_id)
        self.assertEqual(new_cluster.update_paths, [update0.checkpoint_uri, update1.checkpoint_uri])

    def create_update(self, cluster_id=None, round_id=None, model_name=None, checkpoint_uri=None, from_id=None):
        cluster_id = cluster_id if cluster_id else secrets.token_hex(16)
        round_id = round_id if round_id else 0
        model_name = model_name if model_name else "test_model"
        checkpoint_uri = checkpoint_uri if checkpoint_uri else os.path.join("./test_files/", cluster_id, str(round_id))
        from_id = from_id if from_id else secrets.token_hex(16)
        return ModelUpdateMeta(cluster_id, round_id, model_name, checkpoint_uri, from_id)


if __name__ == '__main__':
    unittest.main()