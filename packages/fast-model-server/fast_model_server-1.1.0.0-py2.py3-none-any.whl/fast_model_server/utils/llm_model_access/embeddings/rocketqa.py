# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RocketQA embedding

Authors: fubo
Date: 2023/6/9 17:10:00
"""

from typing import List, Any, Optional, Dict
import requests
from pydantic import root_validator
from langchain.embeddings.openai import OpenAIEmbeddings, _create_retry_decorator, get_from_dict_or_env


class RocketQALangChainEmbedding(OpenAIEmbeddings):
    rocketqa_api_base: Optional[str] = None
    headers: Any = None

    @root_validator()
    def validate_environment(cls, values: Dict):
        """Validate that api key and python package exists in environment."""
        values["rocketqa_api_base"] = get_from_dict_or_env(
            values,
            "rocketqa_api_base",
            "ROCKETQA_API_BASE",
            default="",
        )
        return values

    def embed_with_retry(self, **kwargs: Any) -> Any:
        """Use tenacity to retry the embedding call."""
        retry_decorator = _create_retry_decorator(self)

        @retry_decorator
        def _embed_with_retry(**kwargs: Any) -> Any:
            return requests.post(
                url="%s/%s/run" % (self.rocketqa_api_base, kwargs["type"]),
                headers=self.headers, json=kwargs
            ).json()

        return _embed_with_retry(**kwargs)

    def embed_documents(self, texts: List[str], chunk_size: Optional[int] = 0) -> List[List[float]]:
        """
        生成文档嵌入向量列表
        :param texts: 文档文本列表
        :param chunk_size: 批处理大小，默认为0
        :return: 文档嵌入向量列表
        """
        return self.embed_with_retry(
            docs=[{"title": "", "content": text} for text in texts],
            with_title=False, normalize=True, type="doc"
        )["data"]

    def embed_query(self, text: str) -> List[float]:
        """
        生成query嵌入向量列表
        :param text: query
        :return: 文档嵌入向量列表
        """
        return self.embed_with_retry(queries=[text], normalize=True, type="query")["data"]
