import unittest

from ._testutil import RedisTest, run_until_complete, REDIS_CLUSTER


@unittest.skipIf(not REDIS_CLUSTER,
                 "Cluster command tests expect redis cluster")
class GenericCommandsTest(RedisTest):

    @run_until_complete
    def test_cluster_info(self):
        info = yield from self.redis.cluster_info()
        self.assertIsInstance(info, dict)
