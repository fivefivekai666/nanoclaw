"""
runtime/loop.py

到了第 13 步，AgentLoop 开始正式接入 system prompt。

这意味着 provider 接收到的输入，不再只是用户/助手消息历史的简单拼接，
而是会先注入一层 runtime 级系统指令。

重要边界：
- session.messages 仍然表示真实对话历史
- system_prompt 不写进 session
- system_prompt 只在构造 prompt 时被注入

这样能保持“对话事实”和“运行规则”分离，
为后续 ContextBuilder / persona / memory 注入打基础。
"""

from __future__ import annotations

from providers.base import BaseProvider
from runtime.messages import Message
from runtime.session import Session


class AgentLoop:
    """
    AgentLoop 是 agent 运行时的最小主流程骨架。

    到了第 13 步，它的职责升级为：
    1. 接收一个 Session
    2. 读取 session.messages
    3. 先注入 system_prompt
    4. 再拼接消息历史形成 prompt
    5. 调用 provider
    6. 把 assistant 回复追加回 session

    这意味着 runtime 第一次拥有了系统级指令层。
    """

    def __init__(self, provider: BaseProvider, system_prompt: str) -> None:
        self.provider = provider
        self.system_prompt = system_prompt

    def _build_prompt_from_history(self, history: list[Message]) -> str:
        """
        把 system_prompt + 消息历史转换成 provider 可消费的 prompt。

        结构保持最简单：

            system: ...

            user: ...
            assistant: ...
            user: ...

        第 13 步的重点不是复杂 prompt engineering，
        而是正式建立 system 层与 history 层的分工。
        """
        lines: list[str] = [f"system: {self.system_prompt}", ""]
        lines.extend(f"{message.role}: {message.content}" for message in history)
        return "\n".join(lines)

    def run_once(self, session: Session) -> Message:
        """
        执行一轮最小 agent 流程。

        当前逻辑：
        1. 用 system_prompt + session.messages 构造 prompt
        2. 调用 provider.chat(prompt)
        3. 把结果包装成 assistant Message
        4. 将 assistant Message 追加回 session
        """
        prompt = self._build_prompt_from_history(session.messages)
        response_text = self.provider.chat(prompt)
        assistant_message = Message(role="assistant", content=response_text)
        session.add_message(assistant_message)
        return assistant_message
