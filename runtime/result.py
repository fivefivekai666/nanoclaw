"""
runtime/result.py

这是第 30 步的 loop result 模块。

目标：
- 让 AgentLoop 的结果对象既能表示正常完成
- 也能表示异常结束
- 并且为异常结束补上最小受限分类与可恢复性语义
- 再进一步补上最小 retry 观测边界
- 为后续扩展 retry / fallback / guardrail / max_steps 预留更稳定的落点

当前保留的最小字段：
- session_id
- prompt
- assistant_message
- status
- stop_reason
- error
- attempts
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


class LoopErrorKind(StrEnum):
    """一次 loop 失败时的最小受限错误分类。"""

    PROVIDER_ERROR = "provider_error"
    CONFIG_ERROR = "config_error"
    INTERNAL_ERROR = "internal_error"


@dataclass(slots=True)
class LoopError:
    """表示一次 loop 执行中的最小错误信息。"""

    kind: LoopErrorKind
    message: str
    recoverable: bool


@dataclass(slots=True)
class LoopResult:
    """表示一次 loop 执行后的最小结构化结果。"""

    session_id: str
    prompt: str
    assistant_message: Message | None
    status: LoopStatus
    stop_reason: LoopStopReason
    error: LoopError | None
    attempts: int
