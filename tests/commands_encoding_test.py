import unittest

from ._testutil import (
    RedisEncodingTest,
    run_until_complete,
    REDIS_CLUSTER,
    )


@unittest.skipIf(REDIS_CLUSTER, "Skipped on redis cluster")
class StringCommandsEncodingTest(RedisEncodingTest):

    @run_until_complete
    def test_set(self):
        TEST_KEY = 'my-key'
        ok = yield from self.redis.set(TEST_KEY, 'value')
        self.assertTrue(ok)

        with self.assertRaises(TypeError):
            yield from self.redis.set(None, 'value')

        yield from self.redis.delete(TEST_KEY)

    @run_until_complete
    def test_setnx(self):
        TEST_KEY = 'my-key-nx'
        yield from self.redis._conn.execute('MULTI')
        res = yield from self.redis.setnx(TEST_KEY, 'value')
        self.assertEqual(res, 'QUEUED')

        yield from self.redis._conn.execute('DISCARD')

    @run_until_complete
    def test_hgetall(self):
        TEST_KEY = 'my-key-nx'
        yield from self.redis._conn.execute('MULTI')

        res = yield from self.redis.hgetall(TEST_KEY)
        self.assertEqual(res, 'QUEUED')

        yield from self.redis._conn.execute('EXEC')
