# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
模型服务访问
!!! 设定prompt请避免使用"的"和"-" !!!

Authors: fubo
Date: 2022/11/23 00:00:00
"""
import json
import copy
import random

from fastapi.logger import logger
import threading
import time
from enum import Enum
from typing import List, Dict, Set
from pydantic import BaseModel
import httpx
import networkx
from concurrent.futures import ThreadPoolExecutor


class ModelType(Enum):
    # 抽取模型
    ELEMENT = 0

    # 分类模型
    CLASSIFICATION = 1


class ModelLabelElem(BaseModel):
    # 父结点
    parent: List[str] = []

    # 子结点列表
    children: List[str] = []

    # 是否返回
    is_output: bool = True


class ModelConfig(BaseModel):
    # 模型服务
    url: str

    # 模型服务请求方式
    method: str = "POST"

    # 模型类型(ELEMENT/CLASSIFICATION)
    model_type: ModelType = ModelType.ELEMENT

    # 模型timeout时间
    time_out: int = 5

    # 模型名称
    model_name: str

    # 模型版本
    model_version: str = ""

    # 模型配置文件
    model_label: Dict[str, ModelLabelElem] = {}


class ModelResultElem(BaseModel):
    # 数据标签
    label: str

    # 数据值
    value: str = ""

    # 起始位置
    start: int = -1

    # 结束未知
    end: int = -1

    # score 初始化为-1.0 请求后无值则为0.0
    score: float = -1.0


class ModelResult(BaseModel):
    # 模型名称
    model_name: str

    # 模型版本
    model_version: str = ""

    # 模型类型(ELEMENT/CLASSIFICATION)
    model_type: str = "ELEMENT"

    # 文本内容
    content: str

    # 模型返回详情
    elements: List[List[ModelResultElem]] = []


class Bucket(BaseModel):
    # key
    key: str

    # data aff
    data: List[ModelResultElem] = []

    # 是否输出
    is_output: bool = True

    # 是否已经请求模型 aff
    is_completed: bool = False


class ModelServerAccess(object):
    def __init__(self, model_conf: ModelConfig, max_workers: int = 10):
        self.model_conf = model_conf
        if "element" not in self.model_conf.url and "classification" not in self.model_conf.url:
            raise ValueError("Error URL %s" % self.model_conf.url)

        if "element" in self.model_conf.url:
            self.model_conf.model_type = ModelType.ELEMENT

        if "classification" in self.model_conf.url:
            self.model_conf.model_type = ModelType.CLASSIFICATION

        self.client = httpx.Client(default_encoding="utf-8")
        self.headers = {"Content-Type": "application/json"}
        self.buckets: List[Bucket] = []
        self.__init_buckets()
        self.pool = ThreadPoolExecutor(max_workers=max_workers)

    def __del__(self):
        self.client.close()
        self.pool.shutdown()
        del self.pool

    def __parse_model_labels(self) -> (Set, Set):
        """
        解析模型标签配置
        """
        model_labels: Dict[str, ModelLabelElem] = self.model_conf.model_label.copy()
        if len(model_labels) == 0:
            logger.error("No labels for model")
            raise ValueError("No labels for model")

        labels = set()
        leaves = set()
        root = set()

        graph = networkx.DiGraph()
        for node in model_labels:
            if len(model_labels[node].children) == 0:
                leaves.add(node)
            if len(model_labels[node].parent) == 0:
                root.add(node)

            for parent_node in model_labels[node].parent:
                graph.add_edge(parent_node, node)

            for child_node in model_labels[node].children:
                graph.add_edge(node, child_node)

        if len(root) != 1:
            raise ValueError("Error model labels")
        
        root_node: str = list(root)[0]

        path = []
        for leaf in leaves:
            path = path + list(networkx.all_simple_paths(graph, source=root_node, target=leaf))

        for elems in path:
            for i in range(len(elems)):
                labels.add("-".join(elems[1:i + 1]))
        if "" in labels:
            labels.remove("")
        return leaves, labels

    def __init_buckets(self):
        """
        加载模型配置文件
        解析访问接口
        解析prompts
        """
        leaves, labels = self.__parse_model_labels()

        for label in labels:
            term_types = label.split("-")
            bucket: Bucket = Bucket(key="")
            bucket.is_completed = False
            bucket.is_output = self.model_conf.model_label[term_types[-1]].is_output
            bucket.data = [ModelResultElem(label=term_type) for term_type in term_types]
            bucket.key = self.__create_bucket_key(bucket=bucket)
            self.buckets.append(bucket.copy())

    def __random_revise(self, questions: List[str]) -> List[str]:
        data = random.choice(questions)
        rand_del_index = random.randint(0, len(questions) - 1)
        logger.info("Drop [%s]", questions[rand_del_index])
        logger.info("Add [%s]", data)
        del questions[rand_del_index]
        return questions + [data]

    def __request_mock(self, data: Dict) -> Dict:
        """
        mock网络请求
        :param data:
        :param params:
        :return:
        """
        questions = copy.deepcopy(data["question_list"])
        questions = self.__random_revise(questions=questions)
        results = [
            {
                "original": label + "返回值" + str(random.random()),
                "offset": [
                    0
                ],
                "scores": [
                    0.9170930981636047
                ],
                "type": label,
                "length": 4,
                "normalize": label + "返回值"
            }
            for label in questions
        ]
        return {
            "result": copy.deepcopy(results),
            "logid": data["log_id"],
            "text": data["content"],
            "code": 0,
            "message": "success"
        }

    def __request(self, data: Dict, params: Dict = None) -> Dict:
        """
        HTTP 请求
        :param data: 请求体
        :param params: 请求参数信息
        :return:
        """
        if params is None:
            params = {}

        try:
            logger.debug(
                "run HTTP request url=%s data=%s params=%s",
                self.model_conf.url, json.dumps(data, ensure_ascii=False),
                json.dumps(params, ensure_ascii=False)
            )

            response = self.client.request(
                method=self.model_conf.method, url=self.model_conf.url, headers=self.headers,
                params=params, json=data, timeout=self.model_conf.time_out
            )

            logger.debug("Got HTTP response status_code=%d response=%s", response.status_code, response.text)

            if response.status_code != 200:
                log_str = "Failed to request model server [%d] [%s]" % (response.status_code, response.text)
                logger.error(log_str)
                raise httpx.RequestError(log_str)
        except (
                httpx.ConnectTimeout, httpx.RemoteProtocolError,
                httpx.ConnectError, httpx.ReadTimeout, httpx.ReadError, ConnectionError
        ) as exp:
            log_str = "Failed to connect model server [%s] [%s]" % (self.model_conf.url, exp)
            logger.error(log_str)
            raise ConnectionAbortedError(log_str)

        return response.json()

    def __create_bucket_key(self, bucket: Bucket) -> str:
        """
        根据bucket的内容生成对应的key
        :param bucket:
        :return:
        """
        key = []
        flag = True
        for index, elem in enumerate(bucket.data):
            if elem.score > -1.0:
                if flag is True:
                    key.append(elem.value)
                    flag = False
                else:
                    key.append(elem.label + elem.value)
            else:
                key.append(elem.label)
                break
        return "的".join(key)

    def __is_bucket_ok(self, buckets: List[Bucket]) -> bool:
        """
        检查bucket是否需要进行网络请求更新bucket
        :param buckets:
        :return: 需要进行网络请求返回false
        """
        return sum([bucket.is_completed for bucket in buckets]) == len(buckets)

    def __filter_prompts(self, buckets: List[Bucket]) -> List[int]:
        """
        筛选出当前可请求的buckets的ID列表
        :param buckets:
        :return:
        """
        req_buckets_index = []
        for index, bucket in enumerate(buckets):
            if bucket.is_completed is True:
                # 已经完成计算的bucket
                continue

            # 统计当前bucket有几个位置需要填充
            scores = [elem.score for elem in bucket.data]
            if -1.0 in scores and scores.count(-1.0) == 1:
                req_buckets_index.append(index)
        return req_buckets_index

    def __update_buckets(
            self, buckets: List[Bucket], results: List[ModelResultElem],
            req_buckets_index_mapping: Dict[str, List[int]], req_buckets_index: List[int]
    ) -> List[Bucket]:
        """
        使用多个buckets和模型返回的结果更新bucket
        :param buckets:
        :param values:
        :param req_buckets_index_mapping:
        :param req_buckets_index:
        :return:
        """
        new_buckets: List[Bucket] = []
        update_buckets: List[Bucket] = []
        keep_buckets: List[Bucket] = list(filter(lambda x:x.is_completed, buckets))

        # 更新请求的bucket,新增bucket
        for result in results:
            prompt = result.label
            for pos in req_buckets_index_mapping[prompt]:
                bucket = copy.deepcopy(buckets[pos])
                bucket.data[-1].value = result.value
                bucket.data[-1].score = result.score
                bucket.data[-1].start = result.start
                bucket.data[-1].end = result.end
                bucket.is_completed = True
                new_buckets.append(bucket.copy())

        # 更新库里剩余的bucket
        for result in results:
            prompt = result.label
            for index, p_bucket in enumerate(buckets):
                bucket = copy.deepcopy(p_bucket)
                if index in req_buckets_index:
                    continue

                # 库里剩余的bucket
                if bucket.key != prompt:
                    continue
                # 查找更新的位置
                for pos, elem in enumerate(bucket.data):
                    if elem.score > -1.0:
                        continue
                    bucket.data[pos].score = result.score
                    bucket.data[pos].value = result.value
                    bucket.data[pos].start = result.start
                    bucket.data[pos].end = result.end
                    break
                bucket.key = self.__create_bucket_key(bucket=bucket)
                update_buckets.append(bucket.copy())

        return new_buckets + update_buckets + keep_buckets

    def __fetch_output(self, content: str, buckets: List[Bucket]) -> ModelResult:
        """
        获取bucket里的数据生成模型结果
        :param content:
        :param buckets:
        :return:
        """
        result = ModelResult(
            content=content,
            model_type=self.model_conf.model_type.name,
            model_name=self.model_conf.model_name,
            model_version=self.model_conf.model_version,
            elements=[]
        )

        for bucket in buckets:
            if not bucket.is_output:
                continue
            result.elements.append(copy.deepcopy(bucket.data))
        return result

    def __calc_buckets(self, content: str, buckets: List[Bucket]) -> List[Bucket]:
        """
        网络请求更新bucket
        :param content: 待计算的文本
        :param buckets:
        :return:
        """
        # 筛选可请求的prompt
        req_buckets_index = self.__filter_prompts(buckets=buckets)
        prompts: Dict[str, List[int]] = {}

        for index in req_buckets_index:
            if buckets[index].key not in prompts:
                prompts[buckets[index].key] = []
            prompts[buckets[index].key].append(index)

        # 模型请求
        if self.model_conf.model_type not in [ModelType.CLASSIFICATION, ModelType.ELEMENT]:
            logger.error("Error model type %s", self.model_conf.model_type)
            raise ValueError("Error model type")

        if self.model_conf.model_type is ModelType.ELEMENT:
            # 请求模型
            result = self.__request(
                data={
                    "log_id": str(time.time()), "content": content,
                    "question_list": list(prompts.keys())
                }
            )
            # 返回值标准化
            values: List[ModelResultElem] = [
                ModelResultElem(
                    value=elem["original"], score=elem["scores"][0], label=elem["type"],
                    start=elem["offset"][0], end=elem["offset"][0] + elem["length"][0]
                ).copy()
                for elem in result["result"]
            ]

        if self.model_conf.model_type is ModelType.CLASSIFICATION:
            # 请求分类模型(分类模型请求暂未实现)
            result = self.__request_mock(
                data={
                    "log_id": str(time.time()), "content": content,
                    "candidate_label": list(prompts.keys())
                }
            )
            # 返回值标准化
            values: List[ModelResultElem] = [
                ModelResultElem(
                    value="", score=elem["score"], label=elem["tag"]
                ).copy()
                for elem in result["result"]
            ]
            # 分类模型请求暂未实现
            raise NotImplementedError("The model type 'CLASSIFICATION' has not been implemented")

        # 更新bucket
        return self.__update_buckets(
            buckets=buckets, results=values,
            req_buckets_index_mapping=prompts, req_buckets_index=req_buckets_index
        )

    def __run_model(self, content: str) -> ModelResult:
        """
        单条数据请求
        :param index: 请求序号
        :param content: 数据内容
        """
        logger.debug("Start to run content=%s [%s]", content[30:], threading.current_thread().name)
        buckets = copy.deepcopy(self.buckets)
        while not self.__is_bucket_ok(buckets=buckets):
            # 更新bucket
            buckets = self.__calc_buckets(content=content, buckets=buckets)
        logger.debug("Fetch output from buckets %s", buckets)
        return self.__fetch_output(content=content, buckets=buckets)

    def run(self, contents: List[str]) -> List[ModelResult]:
        """
        提交模型请求计算
        :param contents 需要请求模型计算的文本内容
        """
        output: List[ModelResult] = []
        logger.debug("Run contents with threads %s", json.dumps([content[:30] for content in contents]))
        for result in self.pool.map(self.__run_model, contents):
            output.append(result)
        logger.debug("Got contents result %s", output)
        return output

