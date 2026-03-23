"""
runtime/loop.py

到了第 31 步，AgentLoop 继续保持“运行流程推进者”的角色，
并把结果边界从“有最小 retry 行为”推进到“retry 行为由独立 policy 决定”。

这意味着 loop 不只知道：
- 有 recoverable / fatal 的区分
- 有最小重试能力

还开始知道：
- 是否重试不应写死在 loop 主流程里
- retry 判断应该由独立 runtime policy 层负责

第 31 步的重点不是扩展更复杂的重试机制，
而是先把“执行策略层”从 loop 中拆出来。
"""

from __future__ import annotations

from providers.base import BaseProvider
from runtime.context import ContextBuilder
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
    """
    AgentLoop 是 agent 运行时的最小主流程骨架。

    到了第 31 步，它的职责更聚焦于：
    1. 接收一个 Session
    2. 调用 ContextBuilder 构造 prompt
    3. 调用 provider
    4. 成功时把 assistant 回复追加回 session
    5. 失败时返回结构化失败结果，而不是伪造 assistant message
    6. 给失败结果补上最小 error_kind / recoverable 语义
    7. 把是否重试的判断委托给独立 RetryPolicy

    这样一来，loop 的输出开始同时具备：
    - success / failure 两条最小语义边界
    - 最小 retry 行为边界
    - 最小可配置执行策略边界
    """

    def __init__(
        self,
        provider: BaseProvider,
        context_builder: ContextBuilder,
        retry_policy: RetryPolicy,
    ) -> None:
        self.provider = provider
        self.context_builder = context_builder
        self.retry_policy = retry_policy

    def _classify_error(self, exc: Exception) -> LoopError:
        """把 Python 异常压成当前 runtime 需要的最小错误语义。"""
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

    def _attempt_once(self, prompt: str) -> Message:
        """执行一次 provider 调用并返回 assistant message。"""
        response_text = self.provider.chat(prompt)
        return Message(role="assistant", content=response_text)

    def run_once(self, session: Session) -> LoopResult:
        """执行一轮最小 agent 流程，并把 retry 判断委托给 RetryPolicy。"""
        prompt = self.context_builder.build(session)
        attempts = 0
        last_error: LoopError | None = None

        while True:
            try:
                attempts += 1
                assistant_message = self._attempt_once(prompt)
                session.add_message(assistant_message)
                return LoopResult(
                    session_id=session.id,
                    prompt=prompt,
                    assistant_message=assistant_message,
                    status=LoopStatus.COMPLETED,
                    stop_reason=LoopStopReason.ASSISTANT_RESPONSE,
                    error=None,
                    attempts=attempts,
                )
            except Exception as exc:
                last_error = self._classify_error(exc)
                if not self.retry_policy.should_retry(last_error, attempts):
                    return LoopResult(
                        session_id=session.id,
                        prompt=prompt,
                        assistant_message=None,
                        status=LoopStatus.FAILED,
                        stop_reason=LoopStopReason.PROVIDER_ERROR,
                        error=last_error,
                        attempts=attempts,
                    )
