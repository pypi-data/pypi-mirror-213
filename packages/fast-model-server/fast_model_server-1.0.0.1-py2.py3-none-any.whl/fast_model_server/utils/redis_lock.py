# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基于redis的锁

Authors: fubo
Date: 2021/07/20 00:00:00
"""
import time
from redis import WatchError
from fast_model_server.utils.redis_connection import RedisConfig, RedisConnection


class RedisLock(RedisConnection):
    def __init__(self, redis_config: RedisConfig, lock_name: str, lock_timeout: int = 10):
        super().__init__(redis_config)
        self.lock_name = "redis_lock:%s" % lock_name
        self.lock_timeout = lock_timeout

    def acquire_lock(self) -> bool:
        """
        加锁
        :return:
        """
        self.check_and_reconnect()

        end = time.time() + self.lock_timeout
        # 获取锁的时间超过锁超时时间，则返回错误（已经被死锁）
        while time.time() < end:
            # 如果不存在这个锁则加锁并设置过期时间，避免死锁
            if self.redis.set(self.lock_name, self.lock_name, ex=self.lock_timeout, nx=True):
                return True

            time.sleep(0.001)
        return False

    def release_lock(self) -> bool:
        """
        释放锁
        :return:
        """
        self.check_and_reconnect()

        with self.redis.pipeline() as pipe:
            while True:
                try:
                    # watch 锁, multi 后如果该 key 被其他客户端改变, 事务操作会抛出 WatchError 异常
                    pipe.watch(self.lock_name)
                    value = pipe.get(self.lock_name)
                    if value and value == self.lock_name:
                        # 事务开始
                        pipe.multi()
                        pipe.delete(self.lock_name)
                        pipe.execute()
                        return True
                    pipe.unwatch()
                    break
                except WatchError:
                    pass
            return False
