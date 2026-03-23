"""
runtime/loop.py

到了第 26 步，AgentLoop 继续保持“运行流程推进者”的角色，
但它的返回值从单一 Message 升级成了结构化的 LoopResult。

这意味着 loop 开始具备更明确的结果边界：
- assistant_message：本轮产出的回答
- prompt：本轮真正发给 provider 的上下文
- session_id：这轮执行属于哪个 session

第 26 步的重点不是增加功能数量，
而是把 loop 从“只会吐回复”推进成“会产出运行结果对象”。
"""

from __future__ import annotations

from providers.base import BaseProvider
from runtime.context import ContextBuilder
from runtime.messages import Message
from runtime.result import LoopResult
from runtime.session import Session


class AgentLoop:
    """
    AgentLoop 是 agent 运行时的最小主流程骨架。

    到了第 26 步，它的职责更聚焦于：
    1. 接收一个 Session
    2. 调用 ContextBuilder 构造 prompt
    3. 调用 provider
    4. 把 assistant 回复追加回 session
    5. 返回结构化的 LoopResult

    这样一来，loop 的输出不再只是一个 Message，
    后续要扩展 tool / stop reason / debug 信息时会更自然。
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
        5. 返回包含 session_id / prompt / assistant_message 的 LoopResult
        """
        prompt = self.context_builder.build(session)
        response_text = self.provider.chat(prompt)
        assistant_message = Message(role="assistant", content=response_text)
        session.add_message(assistant_message)
        return LoopResult(
            session_id=session.id,
            prompt=prompt,
            assistant_message=assistant_message,
        )
