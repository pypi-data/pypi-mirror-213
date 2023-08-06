# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rocket排序

Authors: fubo
Date: 2023/6/12 16:25:00
"""
import logging
import requests
from typing import Optional, Any, Dict, Callable, List
from pydantic import BaseModel, root_validator
from tenacity import (
    before_sleep_log,
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)
from langchain.utils import get_from_dict_or_env


logger = logging.getLogger(__name__)


class RocketQARanking(BaseModel):
    rocketqa_api_base: Optional[str] = None
    headers: Any = {"accept": "application/json", "Content-Type": "application/json"}
    max_retries: int = 6

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

    def _create_retry_decorator(self) -> Callable[[Any], Any]:

        min_seconds = 4
        max_seconds = 10
        # Wait 2^x * 1 second between each retry starting with
        # 4 seconds, then up to 10 seconds, then 10 seconds afterwards
        return retry(
            reraise=True,
            stop=stop_after_attempt(self.max_retries),
            wait=wait_exponential(multiplier=1, min=min_seconds, max=max_seconds),
            retry=(
                    retry_if_exception_type(TimeoutError)
                    | retry_if_exception_type(ConnectionError)
                    | retry_if_exception_type(ConnectionAbortedError)
                    | retry_if_exception_type(ConnectionResetError)
                    | retry_if_exception_type(ConnectionRefusedError)
            ),
            before_sleep=before_sleep_log(logger, logging.WARNING),
        )

    def rank_with_retry(self, **kwargs: Any) -> Any:
        """Use tenacity to retry the embedding call."""
        retry_decorator = self._create_retry_decorator()

        @retry_decorator
        def _rank_with_retry(**kwargs: Any) -> Any:
            return requests.post(
                url="%s/similarity/run" % self.rocketqa_api_base,
                headers=self.headers, json=kwargs
            ).json()

        return _rank_with_retry(**kwargs)

    def rank(self, query: str, texts: List[str]) -> List[float]:
        """
        Rank rocketqa with rocketqa api and get ranking result.
        Returns:
        """
        return self.rank_with_retry(
            pairs=[{"query": query, "doc": {"title": "", "content": text}} for text in texts],
            with_title=False
        )["data"]
