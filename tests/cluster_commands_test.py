import unittest

from aioredis import ReplyError
from ._testutil import RedisTest, run_until_complete, REDIS_CLUSTER


@unittest.skipIf(not REDIS_CLUSTER,
                 "Cluster command tests expect redis cluster")
class GenericCommandsTest(RedisTest):

    def setUp(self):
        super().setUp()
        self.redis_node2 = self.loop.run_until_complete(self.create_redis(
            ('localhost', self.redis_port + 1), loop=self.loop))
        self.loop.run_until_complete(self.redis.cluster_meet(
            '127.0.0.1', self.redis_port + 1))

    def tearDown(self):
        self.loop.run_until_complete(self.redis_node2.cluster_reset(hard=True))
        self.loop.run_until_complete(self.redis.cluster_reset(hard=True))
        super().tearDown()

    @run_until_complete
    def test_add_slots(self):
        res = yield from self.redis.cluster_add_slots(0)
        self.assertTrue(res)
        slots = yield from self.redis.cluster_slots()
        self.assertEqual(slots, [
            [0, 0, [b'127.0.0.1', self.redis_port]],
            ])

        res = yield from self.redis.cluster_add_slots(1, 2)
        self.assertTrue(res)
        slots = yield from self.redis.cluster_slots()
        self.assertEqual(slots, [
            [0, 2, [b'127.0.0.1', self.redis_port]],
            ])

        res = yield from self.redis.cluster_add_slots(range(4, 6), 3)
        self.assertTrue(res)
        slots = yield from self.redis.cluster_slots()
        self.assertEqual(slots, [
            [0, 5, [b'127.0.0.1', self.redis_port]],
            ])

        res = yield from self.redis.cluster_add_slots(range(7, 8), 7, 7)
        self.assertTrue(res)
        slots = yield from self.redis.cluster_slots()
        self.assertEqual(slots, [
            [0, 5, [b'127.0.0.1', self.redis_port]],
            [7, 7, [b'127.0.0.1', self.redis_port]],
            ])

        with self.assertRaises(ReplyError):
            res = yield from self.redis.cluster_add_slots(0)

    @run_until_complete
    def test_add_slots__two_nodes(self):
        res = yield from self.redis.cluster_add_slots(0)
        self.assertTrue(res)
        res = yield from self.redis_node2.cluster_add_slots(1)
        self.assertTrue(res)
        slots = yield from self.redis_node2.cluster_slots()
        self.assertEqual(slots, [
            [0, 0, [b'127.0.0.1', self.redis_port]],
            [1, 1, [b'127.0.0.1', self.redis_port + 1]],
            ])

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
        self.assertEqual(len(info), 2)
        for node in info:
            self.assertEqual(node.slots, [])
