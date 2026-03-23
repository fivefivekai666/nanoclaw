"""
runtime/loop.py

到了第 27 步，AgentLoop 继续保持“运行流程推进者”的角色，
并把结果边界从“有结果对象”推进到“有结果语义”。

这意味着 loop 不只知道：
- assistant_message：本轮产出了什么
- prompt：本轮真正发给 provider 的上下文
- session_id：这轮执行属于哪个 session

还开始知道：
- status：这一轮处于什么结束状态
- stop_reason：这一轮为什么停在这里

第 27 步的重点不是增加执行分支，
而是先把 happy-path 的结束语义立起来。
"""

from __future__ import annotations

from providers.base import BaseProvider
from runtime.context import ContextBuilder
from runtime.messages import Message
from runtime.result import LoopResult, LoopStatus, LoopStopReason
from runtime.session import Session


class AgentLoop:
    """
    AgentLoop 是 agent 运行时的最小主流程骨架。

    到了第 27 步，它的职责更聚焦于：
    1. 接收一个 Session
    2. 调用 ContextBuilder 构造 prompt
    3. 调用 provider
    4. 把 assistant 回复追加回 session
    5. 返回带有 status / stop_reason 的结构化 LoopResult

    这样一来，loop 的输出开始具备“结束语义”，
    为后续扩展 tools / errors / guardrails 做准备。
    """

    def __init__(self, provider: BaseProvider, context_builder: ContextBuilder) -> None:
        self.provider = provider
        self.context_builder = context_builder

    def run_once(self, session: Session) -> LoopResult:
        """
        执行一轮最小 agent 流程。

        当前逻辑：
        1. 用 ContextBuilder 根据 session 构造 prompt
        2. 调用 provider.chat(prompt)
        3. 把结果包装成 assistant Message
        4. 将 assistant Message 追加回 session
        5. 返回包含结果内容与结束语义的 LoopResult
        """
        prompt = self.context_builder.build(session)
        response_text = self.provider.chat(prompt)
        assistant_message = Message(role="assistant", content=response_text)
        session.add_message(assistant_message)
        return LoopResult(
            session_id=session.id,
            prompt=prompt,
            assistant_message=assistant_message,
            status=LoopStatus.COMPLETED,
            stop_reason=LoopStopReason.ASSISTANT_RESPONSE,
        )
