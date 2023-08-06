# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
定向爬虫

Authors: fubo
Date: 2021/02/03 00:00:00
"""
import os
import json
import time
import random
import logging
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
import httpx
import asyncio
import tqdm


class Message(BaseModel):
    # message ID
    message_id: str = ""

    # 页面请求处理的函数
    request_method: Any = None

    # url
    request_url: str = ""

    # url请求时等待时间
    request_delay_second: float = 0.02

    # url请求重试的等待事件
    request_retry_delay_seconds: float = 60

    # url请求重试的次数
    request_retry_times: int = 3

    # params
    request_params: Dict = {}

    # headers
    request_headers: Dict = {}

    # data
    request_data: str = ""

    # 是否使用页面效果检查
    request_is_page_check: bool = False

    # parse等待时间
    parse_delay_second: float = 0.0

    # parse重试的等待事件
    parse_retry_delay_seconds: float = 60

    # parse重试的次数
    parse_retry_times: int = 3

    # 页面解析函数
    parse_method: Any = None

    # 页面解析page
    parse_page: str = ""

    # appendix
    appendix: str = ""


class IPProxy(BaseModel):
    # 协议
    protocol: str

    # host
    host: str

    # port
    port: int


class Crawler(object):
    def __init__(self, max_coroutine_count: int = 200, ip_pool: List[IPProxy] = None, user_agents: List[str] = None):
        self.local_path = os.path.dirname(os.path.abspath(__file__))
        self.sem = asyncio.Semaphore(max_coroutine_count)

        # 设置候选UA列表
        self.user_agents: List[str] = json.load(open(self.local_path + "/crawler.config.json", "r"))
        if user_agents is not None and type(user_agents) is list and len(user_agents) > 0:
            self.user_agents.extend(user_agents)

        # 设置IP代理池
        if ip_pool is not None and type(ip_pool) is list and len(ip_pool) > 0:
            self.ip_pool = ["%s://%s:%d" % (elem.protocol, elem.host, elem.port) for elem in ip_pool]
        else:
            self.ip_pool = []

    def check_request_by_page(self, page: str) -> bool:
        """
        根据数据解析的结果判断请求是否正常
        :param page:
        :return:
        """
        logging.info("Run in abstract func [page=%s]", page[:5])
        return True

    @staticmethod
    def random_sleep_time(standard_sleep_time: float = 0.02):
        """
        生成随机休眠时间
        :param standard_sleep_time:
        :return:
        """
        second = standard_sleep_time + (random.random() - 0.5) * 0.01
        return second if second > 0 else 0.01

    def random_ip_proxy(self) -> Optional[str]:
        """
        选择ip代理
        """
        if len(self.ip_pool) == 0:
            return None
        return random.choice(self.ip_pool)

    def random_user_agents(self) -> str:
        """
        随机获取一个user agent
        :return:
        """
        return random.choice(self.user_agents)

    async def __request(self, info: Message, method: str = "GET") -> str:
        """
        HTTP GET请求
        :param info: 请求信息
        :return:
        """
        if len(self.ip_pool) == 0:
            ip_proxy = None
        else:
            # 使用代理
            ip_proxy = self.random_ip_proxy()

        request_headers = {
            'User-Agent': self.random_user_agents()
        }
        request_params = {}

        # update header
        if info.request_headers is not None:
            request_headers.update(info.request_headers)

        # update request params
        if info.request_params is not None:
            request_params.update(info.request_params)

        async with httpx.AsyncClient(proxies=ip_proxy) as client:
            try:
                # sleep random seconds
                time.sleep(self.random_sleep_time(info.request_delay_second))
                response = await client.request(
                    method=method, url=info.request_url, params=request_params, headers=request_headers,
                    data=info.request_data,
                )
                response.encoding = "utf-8"
                if response.status_code == 407:
                    raise httpx.RemoteProtocolError("Status code error %d [%s], proxy: %s"
                                  % (response.status_code, response.text, ip_proxy))
                if response.status_code != 200:
                    raise IOError("Status code error %d [%s], proxy: %s"
                                  % (response.status_code, response.text, ip_proxy))

                if info.request_is_page_check is True and self.check_request_by_page(response.text) is False:
                    raise ValueError("Page error %s" % response.text)

            except ConnectionError as exp:
                raise ConnectionAbortedError("Failed to crawl url %s [%s] %s, proxy: %s"
                                             % (info.request_url, exp, response.text, ip_proxy))
            except (httpx.ConnectTimeout, httpx.RemoteProtocolError,
                    httpx.ConnectError, httpx.ReadTimeout, httpx.ReadError) as exp:
                # 删除当前使用的代理
                if ip_proxy in self.ip_pool:
                    self.ip_pool.remove(ip_proxy)
                raise ConnectionAbortedError("Failed to crawl url %s [%s], proxy: %s"
                                             % (info.request_url, exp, ip_proxy))

        return response.text

    async def phase_request_get(self, info: Message) -> str:
        """
        HTTP GET请求
        :param info: URL
        :return:
        """
        return await self.__request(info=info, method="GET")

    async def phase_request_post(self, info: Message) -> str:
        """
        HTTP POST请求
        :param info: URL
        :return:
        """
        return await self.__request(info=info, method="POST")

    async def phase_parse_empty(self, info: Message) -> Dict:
        """
        解析页面(示例)
        """
        return {"page": info.parse_page}

    async def __run_request(self, message: Message) -> Message:
        """
        执行request操作
        :param funcs:
        :param message:
        :return:
        """
        logging.debug(
            "Run request message_id=%s url=%s method=%s headers=%s, params=%s data=%s",
            message.message_id, message.request_url, message.request_method,
            message.request_headers, message.request_params, message.request_data
        )
        if message.request_method is None:
            return message

        count = message.request_retry_times
        while count > 0:
            try:
                message.parse_page = await message.request_method(message)
                if count < message.request_retry_times:
                    logging.info("Got data at times %d from url %s", count, message.request_url)
                return message

            except ConnectionAbortedError as exp:
                logging.warning(
                    "Failed to request url at times=%d [%s] wait for %f seconds",
                    count, exp, message.request_retry_delay_seconds
                )
                time.sleep(message.request_retry_delay_seconds)

            except IOError as exp:
                logging.warning(
                    "Error status code when request url at times=%d [%s] wait for %f seconds",
                    count, exp, message.request_retry_delay_seconds
                )
                if count == 1:
                    message.parse_page = ""
                    return message
                else:
                    time.sleep(message.request_retry_delay_seconds)

            except ValueError as exp:
                logging.warning("Error page [%s]", exp)
                if count == 1:
                    message.parse_page = ""
                    return message
                else:
                    time.sleep(message.request_retry_delay_seconds)

            count = count - 1

        raise ConnectionError("Failed to request url %s" % message.request_url)

    async def __run_parse(self, message: Message) -> Any:
        """
        执行request操作
        :param funcs:
        :param message:
        :return:
        """
        logging.debug(
            "Run parse message_id=%s data=[\"%s...\" ] method=%s",
            message.message_id, message.parse_page[:100], message.parse_method
        )
        if message.parse_method is None:
            return {}
        count = message.parse_retry_times
        while count > 0:
            try:
                output = await message.parse_method(message)
                if count < message.request_retry_times:
                    logging.info("Parsed data at times %d in %s", count, message.parse_page)
                return output
            except ValueError as exp:
                logging.warning(
                    "Failed to parse %s at times=%d [%s] wait for %f seconds",
                    message.parse_page, count, exp, message.parse_retry_delay_seconds
                )
                time.sleep(message.parse_retry_delay_seconds)
            count = count - 1

        raise ValueError("Failed to parse message %s" % message.parse_page)

    async def __run_message(self, index: int, message: Message) -> Any:
        """
        1、获取页面数据，
        2、解析页面数据，抽取变量
        """
        async with self.sem:
            logging.debug("[S1] Run request step message_id=%s", message.message_id)
            time.sleep(self.random_sleep_time(message.request_delay_second))
            message = await self.__run_request(message=message)

            logging.debug("[S2] Run parse step message_id=%s", message.message_id)
            time.sleep(self.random_sleep_time(message.parse_delay_second))
            data = await self.__run_parse(message=message)

        return index, data

    async def __equip_messages_progress_bar(self, messages: List[Message]) -> List[Any]:
        """
        messages请求添加progress bar
        :param messages:
        :return:
        """
        results = []
        output = [0] * len(messages)
        tasks = [self.__run_message(index=index, message=message) for index, message in enumerate(messages)]
        for task in tqdm.tqdm(asyncio.as_completed(tasks), total=len(tasks)):
            results.append(await task)

        for result in results:
            output[result[0]] = result[1]
        return output
   
    async def run_message(self, message: Message) -> Any:
        """
        执行单个message
        :param messages:
        :return:
        """
        _, data = await self.__run_message(index=0, message=message)
        return data

    def run(self, messages: List[Message]) -> List[Any]:
        """
        批量执行message
        :param messages:
        :return:
        """
        loop = asyncio.get_event_loop()
        task = loop.create_task(self.__equip_messages_progress_bar(messages=messages))
        loop.run_until_complete(task)
        return task.result()
