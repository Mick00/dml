import unittest

from src.daeclust.clusters import ClustersRegistry


class ClustersTest(unittest.TestCase):
    def test_popularity(self):
        cr = ClustersRegistry()
        cr.trainer_cluster = {
            "trainer_0": "cluster_2",
            "trainer_1": "cluster_1",
            "trainer_2": "cluster_2",
            "trainer_3": "cluster_0",
            "trainer_4": "cluster_0",
            "trainer_5": "cluster_0",
        }
        popularity = cr.get_clusters_popularity()
        self.assertEqual(popularity, {
            "cluster_0": 3,
            "cluster_1": 1,
            "cluster_2": 2,
        })


if __name__ == '__main__':
    unittest.main()
