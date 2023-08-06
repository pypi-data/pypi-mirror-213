# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基于redis的缓存

Authors: fubo
Date: 2022/03/06 00:00:00
"""
import logging
from fast_model_server.utils.redis_connection import RedisConnection, RedisConfig


class RedisCache(RedisConnection):
    def __init__(self, redis_config: RedisConfig):
        # redis 配置
        super().__init__(redis_config)

    def write(self, name: str, msg: str, timeout: int = 0) -> bool:
        """
        把数据写入到cache中
        :param name: cache名称
        :param msg: msg内容
        :param timeout: 超时时间(秒)
        :return: 操作成功返回True 否则False
        """
        # 检查redis是否连接
        self.check_and_reconnect()

        try:
            if timeout == 0:
                self.redis.set(name, msg)
            else:
                self.redis.set(name, msg, ex=int(timeout))
        except ConnectionError as exp:
            logging.error("Failed to write cache %s (%s)", name, exp)
            return False

        return True

    def get(self, name: str) -> str:
        """
        从cache中读数据
        :param name: cache名称
        :return: 无数据情况下，返回空字符串
        """
        # 检查redis是否连接
        self.check_and_reconnect()

        try:
            msg = self.redis.get(name=name)
        except ConnectionError as exp:
            logging.error("Failed to get cache %s (%s)", name, exp)
            return ""
        return msg if msg is not None else ""
