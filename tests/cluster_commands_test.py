import unittest

from ._testutil import RedisTest, run_until_complete, REDIS_CLUSTER


@unittest.skipIf(not REDIS_CLUSTER,
                 "Cluster command tests expect redis cluster")
class GenericCommandsTest(RedisTest):

    @run_until_complete
    def test_cluster_info(self):
        info = yield from self.redis.cluster_info()
        self.assertIsInstance(info, dict)
        self.assertIn('cluster_state', info)
        self.assertIn('cluster_slots_assigned', info)
        self.assertIn('cluster_slots_ok', info)
        self.assertIn('cluster_slots_fail', info)
        self.assertIn('cluster_slots_pfail', info)
        self.assertIn('cluster_known_nodes', info)
        self.assertIn('cluster_size', info)
        self.assertIn('cluster_current_epoch', info)
        self.assertIn('cluster_my_epoch', info)
        self.assertIn('cluster_stats_messages_sent', info)
        self.assertIn('cluster_stats_messages_received', info)

    @run_until_complete
    def test_cluster_nodes(self):
        info = yield from self.redis.cluster_nodes()
        self.assertIsInstance(info, list)
