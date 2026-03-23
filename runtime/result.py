"""
runtime/result.py

这是第 26 步新增的 loop result 模块。

目标：
- 把 AgentLoop 的输出从单一 Message 升级成结构化结果对象
- 为后续扩展 tool / stop reason / usage / debug 信息预留稳定边界

当前只保留最小必要字段：
- session_id
- prompt
- assistant_message
"""

from __future__ import annotations

from dataclasses import dataclass

from runtime.messages import Message


@dataclass(slots=True)
class LoopResult:
    """表示一次 loop 执行后的最小结构化结果。"""

    session_id: str
    prompt: str
    assistant_message: Message
