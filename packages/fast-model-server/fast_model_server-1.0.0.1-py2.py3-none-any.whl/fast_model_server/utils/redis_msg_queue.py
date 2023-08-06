# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基于redis的消息队列

Authors: fubo
Date: 2022/03/06 00:00:00
"""
import logging
from fast_model_server.utils.redis_connection import RedisConnection, RedisConfig


class RedisMsgQueue(RedisConnection):
    def __init__(self, redis_config: RedisConfig, topic_name: str):
        # redis 配置
        super().__init__(redis_config)

        # topic名称集合
        self.topics_key = "RedisMsgQueue:topics"

        # topics
        self.topic_name = "RedisMsgQueue:msq_queue_topic:%s" % topic_name

        # 创建topics记录字段
        self.__create_topics()

    def __create_topics(self):
        """
        创建topics记录字段
        """
        # 添加topic记录字段
        self.check_and_reconnect()
        self.redis.sadd(self.topics_key, "base")

    def register_topic(self) -> bool:
        """
        注册topic
        """
        if self.redis.sismember(self.topics_key, self.topic_name):
            logging.error("Same topic name %s", self.topic_name)
            return False

        try:
            self.redis.sadd(self.topics_key, self.topic_name)
        except ConnectionError as exp:
            logging.error("Failed to add topic %s [%s]", self.topic_name, exp)
            return False
        return True

    def push_msg(self, msg: str) -> bool:
        """
        把msg写入到redis消息队列中
        :param msg: msg内容
        :return: 操作成功返回True 否则False
        """
        # 检查redis是否连接
        self.check_and_reconnect()

        try:
            # 检查topic是否注册的队列
            if self.redis.sismember(self.topics_key, self.topic_name) is False:
                logging.error("No such topic name %s. Create first!", self.topic_name)
                return False

            # 写入数据
            self.redis.lpush(self.topic_name, msg)
        except ConnectionError as exp:
            logging.error("Failed to push msg into msg queue %s (%s)", self.topic_name, exp)
            return False

        return True

    def fetch_msg(self) -> str:
        """
        从redis消息队列中获取msg数据
        :return: 队列中无数据情况下，返回空字符串
        """
        # 检查redis是否连接
        self.check_and_reconnect()
        try:
            msg = self.redis.rpop(self.topic_name)
        except ConnectionError as exp:
            logging.error("Failed to pop msg from msg queue %s (%s)", self.topic_name, exp)
            return ""
        return "" if msg is None else msg

