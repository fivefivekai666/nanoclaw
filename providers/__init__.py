"""
providers/__init__.py

这个文件提供统一的 provider 工厂函数。

到了第 32 步，我们把 provider 构造能力从“只会按总配置造一个 provider”，
推进到“也能按 name + model 构造 provider”，
这样 runtime 才能为 execution policy 组装 primary / fallback 两个 provider。
"""

from __future__ import annotations

from config.schema import Config, ProviderSettings
from providers.base import BaseProvider
from providers.mock import MockProvider


def make_provider_from_name_model(name: str, model: str) -> BaseProvider:
    """根据 name + model 构造一个 provider。"""
    provider_name = name.lower()

    if provider_name == "mock":
        return MockProvider(model=model)

    raise ValueError(
        f"Unsupported provider: {name}. "
        "Current steps support only 'mock'."
    )


def make_provider_from_settings(settings: ProviderSettings) -> BaseProvider:
    """根据 ProviderSettings 构造 provider。"""
    return make_provider_from_name_model(settings.name, settings.model)


def make_provider(config: Config) -> BaseProvider:
    """根据 Config 创建主 provider。"""
    return make_provider_from_settings(config.provider)


__all__ = [
    "BaseProvider",
    "MockProvider",
    "make_provider",
    "make_provider_from_name_model",
    "make_provider_from_settings",
]
