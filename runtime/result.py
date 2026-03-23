"""
runtime/result.py

这是第 27 步的 loop result 模块。

目标：
- 让 AgentLoop 的结果对象不只表示“产出了什么”
- 还开始表示“这一轮为什么结束”
- 为后续扩展 tool / error / guardrail / max_steps 预留语义边界

当前保留的最小字段：
- session_id
- prompt
- assistant_message
- status
- stop_reason
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from runtime.messages import Message


class LoopStatus(StrEnum):
    """一次 loop 执行后的最小状态枚举。"""

    COMPLETED = "completed"


class LoopStopReason(StrEnum):
    """一次 loop 执行结束的最小原因枚举。"""

    ASSISTANT_RESPONSE = "assistant_response"


@dataclass(slots=True)
class LoopResult:
    """表示一次 loop 执行后的最小结构化结果。"""

    session_id: str
    prompt: str
    assistant_message: Message
    status: LoopStatus
    stop_reason: LoopStopReason
