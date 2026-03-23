"""
runtime/loop.py

这是第 9 步的核心变化：
AgentLoop 不再直接接收 history 列表，
而是开始接收一个最小 Session 对象。

为什么这样改？
因为 history 已经不应该只是一个临时 list[Message] 了，
它应该属于某个正式会话。

所以到了第 9 步：
- 输入从 list[Message] 升级为 Session
- AgentLoop 基于 session.messages 构造 prompt
- provider 返回结果后，assistant Message 会被追加回 session

这意味着系统第一次真正进入“会话驱动”的运行形态。
"""

from __future__ import annotations

from providers.base import BaseProvider
from runtime.messages import Message
from runtime.session import Session


class AgentLoop:
    """
    AgentLoop 是 agent 运行时的最小主流程骨架。

    到了第 9 步，它开始围绕 Session 工作。
    当前它的职责是：
    1. 接收一个 Session
    2. 读取 session.messages
    3. 把消息历史拼成最小上下文文本
    4. 调用 provider
    5. 把 assistant 回复追加回 session
    6. 返回 assistant Message

    这样一来，消息列表不再只是一次性参数，
    而是成为某个正式会话的一部分。
    """

    def __init__(self, provider: BaseProvider) -> None:
        self.provider = provider

    def _build_prompt_from_history(self, history: list[Message]) -> str:
        """
        把消息历史转换成一个最小可供 provider 使用的 prompt。

        这里仍然保持最朴素的拼接方式：

            user: ...
            assistant: ...
            user: ...

        第 9 步的重点不是 prompt engineering，
        而是把 history 正式纳入 Session 容器。
        """
        lines = [f"{message.role}: {message.content}" for message in history]
        return "\n".join(lines)

    def run_once(self, session: Session) -> Message:
        """
        执行一轮最小 agent 流程。

        输入：
        - 一个 Session

        输出：
        - 一条 assistant Message

        当前逻辑：
        1. 用 session.messages 构造 prompt
        2. 调用 provider.chat(prompt)
        3. 把结果包装成 assistant Message
        4. 将 assistant Message 追加回 session
        """
        prompt = self._build_prompt_from_history(session.messages)
        response_text = self.provider.chat(prompt)
        assistant_message = Message(role="assistant", content=response_text)
        session.add_message(assistant_message)
        return assistant_message
