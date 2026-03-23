"""
runtime/result.py

这是第 28 步的 loop result 模块。

目标：
- 让 AgentLoop 的结果对象既能表示正常完成
- 也能表示异常结束
- 为后续扩展 tool / retry / guardrail / max_steps 预留失败语义边界

当前保留的最小字段：
- session_id
- prompt
- assistant_message
- status
- stop_reason
- error
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from runtime.messages import Message


class LoopStatus(StrEnum):
    """一次 loop 执行后的最小状态枚举。"""

    COMPLETED = "completed"
    FAILED = "failed"


class LoopStopReason(StrEnum):
    """一次 loop 执行结束的最小原因枚举。"""

    ASSISTANT_RESPONSE = "assistant_response"
    PROVIDER_ERROR = "provider_error"


@dataclass(slots=True)
class LoopError:
    """表示一次 loop 执行中的最小错误信息。"""

    kind: str
    message: str


@dataclass(slots=True)
class LoopResult:
    """表示一次 loop 执行后的最小结构化结果。"""

    session_id: str
    prompt: str
    assistant_message: Message | None
    status: LoopStatus
    stop_reason: LoopStopReason
    error: LoopError | None
