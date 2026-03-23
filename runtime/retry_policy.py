"""
runtime/retry_policy.py

这是第 31 步新增的最小 retry policy 模块。

目标：
- 把 retry 判断逻辑从 AgentLoop 主流程中拆出来
- 让 loop 不再自己写死“recoverable 就重试一次”
- 给 runtime 建立最小可配置执行策略层

这一步只保留最小策略参数：
- max_attempts
- retry_on_recoverable_only

暂时不做：
- backoff
- jitter
- provider fallback
- tool/channel/sandbox 专项策略
- 多策略组合
"""

from __future__ import annotations

from dataclasses import dataclass

from runtime.result import LoopError


@dataclass(slots=True)
class RetryPolicy:
    """描述一次 loop 执行中的最小重试策略。"""

    max_attempts: int = 2
    retry_on_recoverable_only: bool = True

    def should_retry(self, error: LoopError, attempts_so_far: int) -> bool:
        """判断在当前错误与尝试次数下，是否应该继续重试。"""
        if attempts_so_far >= self.max_attempts:
            return False

        if self.retry_on_recoverable_only:
            return error.recoverable

        return True
