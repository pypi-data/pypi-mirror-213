# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
redis连接

Authors: fubo
Date: 2022/03/06 00:00:00
"""
import logging
from redis import Redis, ConnectionPool
from pydantic import BaseModel


class RedisConfig(BaseModel):
    # redis host
    host: str = "localhost"

    # redis port
    port: int = 0

    # 密码
    passwd: str = ""

    # db index
    db: int = 0

    # 最大连接数
    max_connections: int = 10000

    # 最大重连次数
    max_retry_times: int = 3


class RedisConnection(object):
    def __init__(self, redis_config: RedisConfig):
        # redis 配置
        self.redis_config = redis_config

        # redis连接
        self.redis: Redis = self.connect_redis()

    def connect_redis(self) -> Redis:
        """
        连接redis
        :return: redis连接
        """
        index = 0
        redis = None
        while index < self.redis_config.max_retry_times:
            try:
                redis = Redis(
                    connection_pool=ConnectionPool(
                        host=self.redis_config.host, port=self.redis_config.port, db=self.redis_config.db,
                        password=self.redis_config.passwd, decode_responses=True,
                        max_connections=self.redis_config.max_connections
                    )
                )
                redis.ping()
                break
            except ConnectionError as exp:
                logging.warning("Failed to connect redis times=%d [%s] ", (index + 1), exp)
                index = index + 1
                continue

        if index >= self.redis_config.max_retry_times:
            raise ConnectionError("Failed to connect redis")

        return redis

    def check_and_reconnect(self):
        """
        检查redis连接，重新连接
        """
        try:
            self.redis.ping()
        except ConnectionError as exp:
            logging.warning("Connection with redis is broken %s reconnect", exp)
            self.redis = self.connect_redis()
