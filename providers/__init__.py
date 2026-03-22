"""
providers/__init__.py

这个文件在第 4 步承担一个很小但很重要的角色：
提供一个统一的 provider 工厂函数。

为什么需要 make_provider()？
因为上层代码（例如 main.py / AgentLoop）不应该到处直接写：

- if provider == "openai": ...
- if provider == "anthropic": ...
- if provider == "mock": ...

更好的做法是把“根据配置挑选 provider”这件事，
集中放到一个地方处理。

这样后面新增真实 provider 时，
主流程代码会更稳定、更干净。
"""

from __future__ import annotations

from config.schema import Config
from providers.base import BaseProvider
from providers.mock import MockProvider


def make_provider(config: Config) -> BaseProvider:
    """
    根据 Config 创建对应的 provider。

    当前第 4 步只支持一种 provider：mock。
    这不是因为真实 provider 不重要，
    而是因为我们当前要先把架构链路跑通。
    """
    provider_name = config.provider.name.lower()

    if provider_name == "mock":
        return MockProvider(model=config.provider.model)

    raise ValueError(
        f"Unsupported provider: {config.provider.name}. "
        "Step 4 currently supports only 'mock'."
    )


__all__ = ["BaseProvider", "MockProvider", "make_provider"]
