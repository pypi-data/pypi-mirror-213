# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据结构定义

Authors: fubo
Date: 2022/03/03 00:00:00
"""
from typing import Dict, Any
from fastapi import Response as NativeResponse
from pydantic import BaseModel


class ServerConfig(BaseModel):
    # Server环境字段
    env: str = "dev"


class ModelInfo(BaseModel):
    # router名称
    router_name: str

    # 模型标签
    model_tag: str


class Request(BaseModel):
    """
    标准请求参数定义
    """
    pass


class Response(BaseModel):
    """
    标准response参数
    """
    # 返回的状态值
    code: Any

    # 错误信息描述
    message: str

    # 返回的数据
    data: Any


class Native:
    @staticmethod
    def to_json_native_response(response: Response, headers: Dict = None) -> NativeResponse:
        """
        :param response: 返回数据
        :param headers: 需要返回的headers
        :return: 包装成fastapi的Response格式
        """
        return NativeResponse(
            content=response.json(),
            media_type="application/json",
            headers=headers,
        )


class ErrorMessage(object):
    """
    错误信息
    """

    def __init__(self, messages: Dict[int, str]):
        self.messages = {
            0: "Success",
            10000: "Invalid params",
            20000: "Internal error",
        }
        if messages is not None:
            self.messages.update(messages)

    def get_message(self, code: int) -> str:
        """
        返回错误信息
        :param code: 错误代码
        :return: 错误信息描述
        """
        return self.messages.get(code, "Undefined error")

    def message_list(self) -> Dict[int, str]:
        """
        获取错误信息表
        :return: 错误信息列表
        """
        return self.messages
