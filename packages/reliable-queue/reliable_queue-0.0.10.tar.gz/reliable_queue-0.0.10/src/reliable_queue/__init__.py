from typing import Optional
from redis.exceptions import ConnectionError
import redis
import time
import logging

logger = logging.getLogger("ReliableQueue")


# This is the skeleton functionality.
class ReliableQueue:

    # For first version, just assume local redis
    def __init__(self, queue_name: str, redis_hostname: str = "localhost", redis_port: int = 6379):
        self._queue_name = queue_name
        self._redis_hostname = redis_hostname
        self._redis_port = redis_port
        self._redis = redis.Redis(host=redis_hostname, port=redis_port)
        self.timeout_push = 300  # Try to push for max 5min
        self._shutdown = False

    def close(self):
        self._shutdown = True
        self._redis.close()

    def set_shutdown(self, shutdown):
        self._shutdown = shutdown

    def get_queue_name(self):
        return self._queue_name

    def get_queue_len(self) -> int:
        return self._redis.llen(self._queue_name)

    def push(self, data: bytes):
        """
        Note: redis.exceptions.ResponseError: WRONGTYPE Operation against a key holding the wrong kind of value
           happens if key exists but is not referring to a list. Ie, key refer to a SET value, not a RPUSH.

        :param data:
        :return:
        """
        sleep_time = 1
        accumulated_sleep_time = 0
        have_warned = False

        while accumulated_sleep_time <= self.timeout_push:
            try:
                self._redis.rpush(self._queue_name, data)
                if have_warned:
                    logger.info("ReliableQueue.push() redis is back")
                break
            except ConnectionError as ex:
                if (accumulated_sleep_time + sleep_time) <= self.timeout_push:
                    have_warned = True
                    logger.warning("ReliableQueue.push() Failed: [" + str(ex) + "]" +
                                   " sleeping " + str(sleep_time) + "s and then retrying. err=" + str(ex))
                    # FIXME What do we do if shutdown has been requested?
                    time.sleep(sleep_time)
                    accumulated_sleep_time += sleep_time
                    if sleep_time > 2:
                        sleep_time = int(sleep_time * 1.5)
                    else:
                        sleep_time = sleep_time * 2
                else:
                    raise ex

    def blocking_pop(self, timeout=0) -> Optional[bytes]:
        """
        :param timeout: If 0, wait until data is available, if timeout>0, wait max timeout seconds else return None.
        :return: Optional[bytes]
        """
        if timeout == 0:
            timeout = 1000000000
        have_warned = False

        while timeout > 0:
            try:
                if self._shutdown:
                    return None
                result = self._redis.blpop(self._queue_name, 1)
                if have_warned:
                    logger.info("ReliableQueue.blocking_pop() redis is back")
                if result is not None:
                    return result[1]
            except ConnectionError as ex:
                if not have_warned:
                    logger.error("ReliableQueue.blocking_pop() Redis is down. Unable to pull. err=" + str(ex))
                    have_warned = True
            timeout -= 1
            time.sleep(1)
        return None

    def is_ram_empty(self):
        have_warned = False
        while True:
            try:
                result = not self._redis.exists(self._queue_name)
                if have_warned:
                    logger.info("ReliableQueue.is_ram_empty() redis is back.")
                return result
            except ConnectionError as ex:
                if not have_warned:
                    logger.error("ReliableQueue.is_ram_empty() redis problems. err=" + str(ex))
                    have_warned = True
            if self._shutdown:
                return True
            time.sleep(1)

    def __str__(self):
        return "ReliableQueue[%s:%d, queue=%s, shutdown=%s]" % (self._redis_hostname, self._redis_port, self._queue_name, self._shutdown)

