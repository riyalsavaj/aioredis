from .connection import RedisConnection, create_connection
from .commands import Redis, create_redis, create_reconnecting_redis
from .pool import RedisPool, create_pool
from .util import Channel
from .errors import (
    ConnectionClosedError,
    MultiExecError,
    PipelineError,
    ProtocolError,
    RedisError,
    ReplyError,
    ChannelClosedError,
    WatchVariableError,
    PoolClosedError,
    CloseReason,
    )


__version__ = '0.2.9'

# make pyflakes happy   # XXX: make __all__
(create_connection, RedisConnection,
 create_redis, create_reconnecting_redis, Redis,
 create_pool, RedisPool, Channel,
 RedisError, ProtocolError, ReplyError,
 PipelineError, MultiExecError, ConnectionClosedError,
 ChannelClosedError, WatchVariableError,
 PoolClosedError,
 CloseReason,
 )
