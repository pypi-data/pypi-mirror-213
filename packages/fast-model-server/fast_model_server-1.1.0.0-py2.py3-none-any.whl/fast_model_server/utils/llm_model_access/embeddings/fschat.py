# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fschat Embedding

Authors: fubo
Date: 2023/6/9 17:05:00
"""
import copy
from typing import List, Any, Dict, Optional
import requests
from pydantic import root_validator

from langchain.embeddings.openai import OpenAIEmbeddings, _create_retry_decorator, get_from_dict_or_env


def embed_with_retry(embeddings: OpenAIEmbeddings, **kwargs: Any) -> Any:
    """Use tenacity to retry the embedding call."""
    retry_decorator = _create_retry_decorator(embeddings)

    @retry_decorator
    def _embed_with_retry(**kwargs: Any) -> Any:
        return requests.post(
            url=embeddings.openai_api_base + "/create_embeddings", headers=embeddings.headers, json=kwargs
        ).json()

    return _embed_with_retry(**kwargs)


class FSChatEmbedding(OpenAIEmbeddings):
    @root_validator()
    def validate_environment(cls, values: Dict):
        """Validate that api key and python package exists in environment."""
        values["openai_api_key"] = get_from_dict_or_env(
            values, "openai_api_key", "OPENAI_API_KEY"
        )
        values["openai_api_base"] = get_from_dict_or_env(
            values,
            "openai_api_base",
            "OPENAI_API_BASE",
            default="",
        )
        values["openai_api_type"] = get_from_dict_or_env(
            values,
            "openai_api_type",
            "OPENAI_API_TYPE",
            default="",
        )
        values["openai_proxy"] = get_from_dict_or_env(
            values,
            "openai_proxy",
            "OPENAI_PROXY",
            default="",
        )
        if values["openai_api_type"] in ("azure", "azure_ad", "azuread"):
            default_api_version = "2022-12-01"
        else:
            default_api_version = ""
        values["openai_api_version"] = get_from_dict_or_env(
            values,
            "openai_api_version",
            "OPENAI_API_VERSION",
            default=default_api_version,
        )
        values["openai_organization"] = get_from_dict_or_env(
            values,
            "openai_organization",
            "OPENAI_ORGANIZATION",
            default="",
        )
        return values

    def embed_with_retry(self, **kwargs: Any) -> Any:
        """Use tenacity to retry the embedding call."""
        retry_decorator = _create_retry_decorator(self)

        @retry_decorator
        def _embed_with_retry(**kwargs: Any) -> Any:
            return requests.post(
                url=self.openai_api_base + "/create_embeddings", headers=self.headers, json=kwargs
            ).json()

        return _embed_with_retry(**kwargs)

    def embed_documents(self, texts: List[str], chunk_size: Optional[int] = 0) -> List[List[float]]:
        """
        生成文档嵌入向量列表
        :param texts: 文档文本列表
        :param chunk_size: 批处理大小，默认为0
        :return: 文档嵌入向量列表
        """
        return [self.embed_with_retry(input=text, model=self.model)["data"][0]["embedding"] for text in texts]

    def embed_query(self, text: str) -> List[float]:
        return self.embed_with_retry(input=text, model=self.model)["data"][0]["embedding"]
