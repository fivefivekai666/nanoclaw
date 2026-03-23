"""
runtime/loop.py

到了第 32 步，AgentLoop 继续保持“运行流程推进者”的角色，
并把 provider fallback 从 loop 写死逻辑推进到独立 execution policy 边界。

这意味着 loop 不只知道：
- 有 retry policy
- 有 recoverable / fatal 的区分

还开始知道：
- 是否切到 fallback provider 不应写死在 loop 主流程里
- fallback 判断应该由独立 execution policy 层负责

第 32 步的重点不是扩展复杂 provider 路由系统，
而是先把最小 provider fallback 策略层正式拆出来。
"""

from __future__ import annotations

from providers.base import BaseProvider
from runtime.context import ContextBuilder
from runtime.execution_policy import ExecutionPolicy
from runtime.messages import Message
from runtime.result import (
    LoopError,
    LoopErrorKind,
    LoopResult,
    LoopStatus,
    LoopStopReason,
)
from runtime.retry_policy import RetryPolicy
from runtime.session import Session


class AgentLoop:
    def __init__(
        self,
        provider: BaseProvider,
        context_builder: ContextBuilder,
        retry_policy: RetryPolicy,
        execution_policy: ExecutionPolicy,
    ) -> None:
        self.provider = provider
        self.context_builder = context_builder
        self.retry_policy = retry_policy
        self.execution_policy = execution_policy

    def _classify_error(self, exc: Exception) -> LoopError:
        if isinstance(exc, ValueError):
            return LoopError(
                kind=LoopErrorKind.CONFIG_ERROR,
                message=str(exc),
                recoverable=False,
            )
        if isinstance(exc, RuntimeError):
            return LoopError(
                kind=LoopErrorKind.PROVIDER_ERROR,
                message=str(exc),
                recoverable=True,
            )
        return LoopError(
            kind=LoopErrorKind.INTERNAL_ERROR,
            message=str(exc),
            recoverable=False,
        )

    def _attempt_once(self, provider: BaseProvider, prompt: str) -> Message:
        response_text = provider.chat(prompt)
        return Message(role="assistant", content=response_text)

    def run_once(self, session: Session) -> LoopResult:
        prompt = self.context_builder.build(session)
        attempts = 0
        fallback_used = False
        current_provider = self.execution_policy.current_provider(fallback_used=False)
        provider_used = type(current_provider).__name__

        while True:
            try:
                attempts += 1
                assistant_message = self._attempt_once(current_provider, prompt)
                session.add_message(assistant_message)
                return LoopResult(
                    session_id=session.id,
                    prompt=prompt,
                    assistant_message=assistant_message,
                    status=LoopStatus.COMPLETED,
                    stop_reason=LoopStopReason.ASSISTANT_RESPONSE,
                    error=None,
                    attempts=attempts,
                    provider_used=provider_used,
                    fallback_used=fallback_used,
                )
            except Exception as exc:
                classified_error = self._classify_error(exc)

                if self.retry_policy.should_retry(classified_error, attempts):
                    continue

                if self.execution_policy.should_fallback(classified_error, fallback_used):
                    fallback_used = True
                    current_provider = self.execution_policy.current_provider(fallback_used=True)
                    provider_used = type(current_provider).__name__
                    continue

                return LoopResult(
                    session_id=session.id,
                    prompt=prompt,
                    assistant_message=None,
                    status=LoopStatus.FAILED,
                    stop_reason=LoopStopReason.PROVIDER_ERROR,
                    error=classified_error,
                    attempts=attempts,
                    provider_used=provider_used,
                    fallback_used=fallback_used,
                )
