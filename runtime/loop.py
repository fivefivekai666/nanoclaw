"""
runtime/loop.py

这是第 5 步开始出现的 AgentLoop，
到了第 7 步，它从“接收裸字符串”升级成“接收结构化 Message”。

这是一个很关键的架构变化：
- 以前：run_once(user_input: str) -> str
- 现在：run_once(message: Message) -> Message

这样做的好处是：
1. runtime 内部的输入输出单位开始统一
2. 后面更容易接 session / memory / tools
3. provider 仍然可以先维持最小字符串接口，不必一下子重构太多层

也就是说，第 7 步是在不打乱前面结构的前提下，
让系统的数据模型开始正规化。
"""

from __future__ import annotations

from providers.base import BaseProvider
from runtime.messages import Message


class AgentLoop:
    """
    AgentLoop 是 agent 运行时的最小主流程骨架。

    到了第 7 步，它的职责依然很小：
    - 接收一条 Message
    - 取出其中的文本内容
    - 调用 provider
    - 再把结果包装成 assistant Message 返回

    虽然目前底层 provider 还只是 `chat(prompt: str) -> str`，
    但 runtime 层已经先完成了“消息对象化”。
    这是后续架构演进的重要基础。
    """

    def __init__(self, provider: BaseProvider) -> None:
        self.provider = provider

    def run_once(self, message: Message) -> Message:
        """
        执行一轮最小 agent 流程。

        输入：
        - 一条 user Message

        输出：
        - 一条 assistant Message

        当前逻辑仍然非常简单：
        1. 读取输入消息的 content
        2. 调用 provider.chat(...)
        3. 把返回文本包装成 assistant 消息
        """
        response_text = self.provider.chat(message.content)
        return Message(role="assistant", content=response_text)
