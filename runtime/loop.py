"""
runtime/loop.py

到了第 14 步，AgentLoop 不再直接负责 prompt 构造，
而是把这部分职责交给独立的 ContextBuilder。

这意味着分层开始变清晰：
- AgentLoop：负责运行流程推进
- ContextBuilder：负责 system prompt + history 的上下文构造

第 14 步的重点不是增加新能力，
而是把已有能力拆分成更清晰的模块边界。
"""

from __future__ import annotations

from providers.base import BaseProvider
from runtime.context import ContextBuilder
from runtime.messages import Message
from runtime.session import Session


class AgentLoop:
    """
    AgentLoop 是 agent 运行时的最小主流程骨架。

    到了第 14 步，它的职责更聚焦于：
    1. 接收一个 Session
    2. 调用 ContextBuilder 构造 prompt
    3. 调用 provider
    4. 把 assistant 回复追加回 session

    这样一来，prompt 构造不再混在 loop 里，
    结构会更容易继续扩展。
    """

    def __init__(self, provider: BaseProvider, context_builder: ContextBuilder) -> None:
        self.provider = provider
        self.context_builder = context_builder

    def run_once(self, session: Session) -> Message:
        """
        执行一轮最小 agent 流程。

        当前逻辑：
        1. 用 ContextBuilder 根据 session 构造 prompt
        2. 调用 provider.chat(prompt)
        3. 把结果包装成 assistant Message
        4. 将 assistant Message 追加回 session
        """
        prompt = self.context_builder.build(session)
        response_text = self.provider.chat(prompt)
        assistant_message = Message(role="assistant", content=response_text)
        session.add_message(assistant_message)
        return assistant_message
