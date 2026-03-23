"""
runtime/context.py

这是第 14 步引入的最小 ContextBuilder。

为什么要单独抽这个模块？
因为 AgentLoop 的职责应该是“推进运行流程”，
而不是同时负责“怎样拼 prompt”。

所以从第 14 步开始：
- AgentLoop 负责 orchestration（编排）
- ContextBuilder 负责 context construction（上下文构造）

当前仍然只做最小能力：
1. 注入 system prompt
2. 序列化 session 历史

后面 identity / memory / tools / channel metadata 都可以自然继续挂在这里。
"""

from __future__ import annotations

from runtime.session import Session


class ContextBuilder:
    """
    最小上下文构造器。

    当前只负责把：
    - system_prompt
    - session.messages

    组合成 provider 可消费的一段 prompt 文本。
    """

    def __init__(self, system_prompt: str) -> None:
        self.system_prompt = system_prompt

    def build(self, session: Session) -> str:
        """
        根据 session 构造一段最小 prompt。

        当前结构：

            system: ...

            user: ...
            assistant: ...
            user: ...
        """
        lines: list[str] = [f"system: {self.system_prompt}", ""]
        lines.extend(f"{message.role}: {message.content}" for message in session.messages)
        return "\n".join(lines)
