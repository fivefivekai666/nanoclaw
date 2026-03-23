"""
runtime/result.py

这是第 32 步的 loop result 模块。

目标：
- 让 AgentLoop 的结果对象既能表示正常完成
- 也能表示异常结束
- 为异常结束补上最小受限分类与可恢复性语义
- 保留最小 retry 观测边界
- 再进一步补上最小 provider execution 观测边界

当前保留的最小字段：
- session_id
- prompt
- assistant_message
- status
- stop_reason
- error
- attempts
- provider_used
- fallback_used
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from runtime.messages import Message


class LoopStatus(StrEnum):
    COMPLETED = "completed"
    FAILED = "failed"


class LoopStopReason(StrEnum):
    ASSISTANT_RESPONSE = "assistant_response"
    PROVIDER_ERROR = "provider_error"


class LoopErrorKind(StrEnum):
    PROVIDER_ERROR = "provider_error"
    CONFIG_ERROR = "config_error"
    INTERNAL_ERROR = "internal_error"


@dataclass(slots=True)
class LoopError:
    kind: LoopErrorKind
    message: str
    recoverable: bool


@dataclass(slots=True)
class LoopResult:
    session_id: str
    prompt: str
    assistant_message: Message | None
    status: LoopStatus
    stop_reason: LoopStopReason
    error: LoopError | None
    attempts: int
    provider_used: str
    fallback_used: bool
