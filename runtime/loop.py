"""
runtime/loop.py

这是第 8 步的核心变化：
AgentLoop 不再只处理“一条消息”，而是开始处理“最小消息历史（history）”。

为什么这一步重要？
因为真正的 agent runtime 不是只看当前一句话，
而是要在某种上下文中理解当前输入。

在第 8 步我们先做最小版本：
- 输入：list[Message]
- 输出：一条 assistant Message
- provider 仍然保持最小字符串接口

也就是说，这一步先让 runtime 学会“接 history”，
再由 runtime 自己把 history 拼成一个最小 prompt 给 provider。
"""

from __future__ import annotations

from providers.base import BaseProvider
from runtime.messages import Message


class AgentLoop:
    """
    AgentLoop 是 agent 运行时的最小主流程骨架。

    到了第 8 步，它开始从“单条消息处理”进化为“最小上下文处理”。
    当前它的职责是：
    1. 接收 history: list[Message]
    2. 把历史消息拼成最小上下文文本
    3. 调用 provider
    4. 返回 assistant Message

    虽然这还不是完整 session / memory 系统，
    但它已经让 runtime 第一次具备了“看前后文”的能力边界。
    """

    def __init__(self, provider: BaseProvider) -> None:
        self.provider = provider

    def _build_prompt_from_history(self, history: list[Message]) -> str:
        """
        把消息历史转换成一个最小可供 provider 使用的 prompt。

        这里故意不用复杂模板，
        只做最朴素的按顺序拼接：

            user: ...
            assistant: ...
            user: ...

        为什么先这样做？
        因为第 8 步的核心目标是“引入 history 接口”，
        不是一上来就设计复杂 prompt builder。
        """
        lines = [f"{message.role}: {message.content}" for message in history]
        return "\n".join(lines)

    def run_once(self, history: list[Message]) -> Message:
        """
        执行一轮最小 agent 流程。

        输入：
        - 一段消息历史 history

        输出：
        - 一条 assistant Message

        当前逻辑：
        1. 用 history 构造 prompt
        2. 调用 provider.chat(prompt)
        3. 把结果包装成 assistant Message
        """
        prompt = self._build_prompt_from_history(history)
        response_text = self.provider.chat(prompt)
        return Message(role="assistant", content=response_text)
