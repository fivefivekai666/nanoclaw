"""
providers/base.py

这是第 4 步的核心文件之一：Provider 抽象基类。

Provider 是什么？
你可以把它理解成：

    “agent runtime 和具体模型服务之间的适配层”

为什么需要这层？
因为上层 runtime（以后会是 AgentLoop）真正关心的是：
- 什么时候调用模型
- 给模型传什么内容
- 拿到结果之后做什么

而它不应该关心：
- 具体是 OpenAI 还是 Anthropic
- 请求参数怎么拼
- HTTP / SDK 怎么调用
- 返回字段名字叫什么

所以我们先定义一个统一接口，让上层以后只面向 Provider 编程。
这一步仍然不接真实模型，而是先把“接口边界”搭出来。
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class BaseProvider(ABC):
    """
    所有模型 provider 的统一抽象基类。

    你可以把它看成一份“接口合同”：
    任何具体 provider 只要想接入 runtime，
    都应该遵守这里定义的方法形状。

    例如未来可能会有：
    - OpenAIProvider
    - AnthropicProvider
    - LiteLLMProvider
    - LocalProvider
    - MockProvider

    它们底层实现不同，但上层都应该能统一调用。
    """

    @abstractmethod
    def chat(self, prompt: str) -> str:
        """
        给定一个 prompt，返回模型生成的文本。

        现在我们故意把接口保持得非常小，只保留一个字符串输入、
        一个字符串输出，方便从 0 理解抽象边界。

        后面这个接口会逐步升级，可能会支持：
        - messages 列表
        - system prompt
        - tool calls
        - structured output
        - streaming
        - usage / token 统计
        """
        raise NotImplementedError
