# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FastChat类型接口的访问操作

Authors: fubo
Date: 2023/6/9 08:47:00
"""
from typing import List, Optional, Dict, Any
from langchain.llms.openai import OpenAIChat, BaseOpenAI
from langchain.llms.openai import _streaming_response_template, completion_with_retry, _update_response
from langchain.llms.openai import update_token_usage, acompletion_with_retry
from langchain.callbacks.manager import AsyncCallbackManagerForLLMRun, CallbackManagerForLLMRun
from langchain.schema import LLMResult


class FSChat(BaseOpenAI):
    def _generate(
        self,
        prompts: List[str],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
    ) -> LLMResult:
        """Call out to OpenAI's endpoint with k unique prompts.

        Args:
            prompts: The prompts to pass into the model.
            stop: Optional list of stop words to use when generating.

        Returns:
            The full LLM output.

        Example:
            .. code-block:: python

                response = openai.generate(["Tell me a joke."])
        """
        # TODO: write a unit test for this
        params = self._invocation_params
        sub_prompts = self.get_sub_prompts(params, prompts, stop)
        choices = []
        token_usage: Dict[str, int] = {}
        # Get the token usage from the response.
        # Includes prompt, completion, and total tokens used.
        _keys = {"completion_tokens", "prompt_tokens", "total_tokens"}
        for _prompts in sub_prompts:
            if self.streaming:
                if len(_prompts) > 1:
                    raise ValueError("Cannot stream results with multiple prompts.")
                params["stream"] = True
                response = _streaming_response_template()
                for stream_resp in completion_with_retry(
                    self, prompt=_prompts, **params
                ):
                    if run_manager:
                        run_manager.on_llm_new_token(
                            stream_resp["choices"][0]["text"],
                            verbose=self.verbose,
                            logprobs=stream_resp["choices"][0]["logprobs"],
                        )
                    _update_response(response, stream_resp)
                choices.extend(response["choices"])
            else:
                response = completion_with_retry(self, prompt="".join(_prompts), **params)
                choices.extend(response["choices"])
            if not self.streaming:
                # Can't update token usage if streaming
                update_token_usage(_keys, response, token_usage)
        return self.create_llm_result(choices, prompts, token_usage)

    async def _agenerate(
        self,
        prompts: List[str],
        stop: Optional[List[str]] = None,
        run_manager: Optional[AsyncCallbackManagerForLLMRun] = None,
    ) -> LLMResult:
        """Call out to OpenAI's endpoint async with k unique prompts."""
        params = self._invocation_params
        sub_prompts = self.get_sub_prompts(params, prompts, stop)
        choices = []
        token_usage: Dict[str, int] = {}
        # Get the token usage from the response.
        # Includes prompt, completion, and total tokens used.
        _keys = {"completion_tokens", "prompt_tokens", "total_tokens"}
        for _prompts in sub_prompts:
            if self.streaming:
                if len(_prompts) > 1:
                    raise ValueError("Cannot stream results with multiple prompts.")
                params["stream"] = True
                response = _streaming_response_template()
                async for stream_resp in await acompletion_with_retry(
                    self, prompt=_prompts, **params
                ):
                    if run_manager:
                        await run_manager.on_llm_new_token(
                            stream_resp["choices"][0]["text"],
                            verbose=self.verbose,
                            logprobs=stream_resp["choices"][0]["logprobs"],
                        )
                    _update_response(response, stream_resp)
                choices.extend(response["choices"])
            else:
                response = await acompletion_with_retry(self, prompt="".join(_prompts), **params)
                choices.extend(response["choices"])
            if not self.streaming:
                # Can't update token usage if streaming
                update_token_usage(_keys, response, token_usage)
        return self.create_llm_result(choices, prompts, token_usage)

    @property
    def _invocation_params(self) -> Dict[str, Any]:
        return {**{"model": self.model_name}, **super()._invocation_params}

    @property
    def _llm_type(self) -> str:
        return "fschat"


class FSChatChat(OpenAIChat):
    @property
    def _llm_type(self) -> str:
        return "fschat-chat"
