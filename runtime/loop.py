"""
runtime/loop.py

到了第 28 步，AgentLoop 继续保持“运行流程推进者”的角色，
并把结果边界从“有正常结束语义”推进到“也有异常结束语义”。

这意味着 loop 不只知道：
- 正常完成时产出了什么
- 为什么正常结束

还开始知道：
- 如果 provider 调用失败，这一轮应该如何表达失败
- 失败时不应伪造 assistant message，也不应把错误回复写回 session

第 28 步的重点不是引入复杂恢复机制，
而是先把最小 failure path 立起来。
"""

from __future__ import annotations

from providers.base import BaseProvider
from runtime.context import ContextBuilder
from runtime.messages import Message
from runtime.result import LoopError, LoopResult, LoopStatus, LoopStopReason
from runtime.session import Session


class AgentLoop:
    """
    AgentLoop 是 agent 运行时的最小主流程骨架。

    到了第 28 步，它的职责更聚焦于：
    1. 接收一个 Session
    2. 调用 ContextBuilder 构造 prompt
    3. 调用 provider
    4. 成功时把 assistant 回复追加回 session
    5. 失败时返回结构化失败结果，而不是伪造 assistant message

    这样一来，loop 的输出开始同时具备 success / failure 两条最小语义边界。
    """

    def __init__(self, provider: BaseProvider, context_builder: ContextBuilder) -> None:
        self.provider = provider
        self.context_builder = context_builder

    def run_once(self, session: Session) -> LoopResult:
        """
        执行一轮最小 agent 流程。

        成功路径：
        1. 用 ContextBuilder 根据 session 构造 prompt
        2. 调用 provider.chat(prompt)
        3. 把结果包装成 assistant Message
        4. 将 assistant Message 追加回 session
        5. 返回 completed / assistant_response

        失败路径：
        1. 仍会先构造 prompt
        2. provider.chat(prompt) 抛异常时
        3. 返回 failed / provider_error
        4. assistant_message 为 None
        5. error 中保留最小错误摘要
        """
        prompt = self.context_builder.build(session)

        try:
            response_text = self.provider.chat(prompt)
        except Exception as exc:
            return LoopResult(
                session_id=session.id,
                prompt=prompt,
                assistant_message=None,
                status=LoopStatus.FAILED,
                stop_reason=LoopStopReason.PROVIDER_ERROR,
                error=LoopError(kind=exc.__class__.__name__, message=str(exc)),
            )

        assistant_message = Message(role="assistant", content=response_text)
        session.add_message(assistant_message)
        return LoopResult(
            session_id=session.id,
            prompt=prompt,
            assistant_message=assistant_message,
            status=LoopStatus.COMPLETED,
            stop_reason=LoopStopReason.ASSISTANT_RESPONSE,
            error=None,
        )
