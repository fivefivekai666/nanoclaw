"""
runtime/execution_policy.py

这是第 32 步新增的最小 execution policy 模块。

目标：
- 把 provider fallback 判断逻辑从 AgentLoop 主流程中拆出来
- 让 loop 不再自己写死“主 provider 失败后换 fallback provider”
- 给 runtime 建立最小 execution policy 边界

这一步只保留最小策略参数：
- primary_provider
- fallback_provider
- fallback_on_recoverable_only

暂时不做：
- 多级 provider 链
- provider 排序
- latency / cost 感知选择
- provider capability routing
- tool-specific provider routing
- retry / fallback 的复杂联动调度
"""

from __future__ import annotations

from dataclasses import dataclass

from providers.base import BaseProvider
from runtime.result import LoopError


@dataclass(slots=True)
class ExecutionPolicy:
    """描述一次 loop 执行中的最小 provider execution policy。"""

    primary_provider: BaseProvider
    fallback_provider: BaseProvider | None = None
    fallback_on_recoverable_only: bool = True

    def current_provider(self, fallback_used: bool) -> BaseProvider:
        """根据当前是否已使用 fallback，返回本轮应该调用的 provider。"""
        if fallback_used and self.fallback_provider is not None:
            return self.fallback_provider
        return self.primary_provider

    def should_fallback(self, error: LoopError, fallback_used: bool) -> bool:
        """判断在当前错误与状态下，是否应该切到 fallback provider。"""
        if fallback_used:
            return False

        if self.fallback_provider is None:
            return False

        if self.fallback_on_recoverable_only:
            return error.recoverable

        return True
