"""
runtime/__init__.py

到了第 32 步，runtime 包继续暴露 context / session / workspace / policy / loop result 等能力。

这样 runtime 里的职责拆分更清楚：
- ContextBuilder：上下文装配
- ResponsePolicy：回答规则装配
- ResponseStyle：回答风格的受限类型入口
- RetryPolicy：最小重试判断边界
- ExecutionPolicy：最小 provider fallback 执行策略边界
- AgentLoop：运行时调度
- LoopResult：一次 loop 执行的结构化结果边界
"""

from runtime.context import ContextBuilder
from runtime.execution_policy import ExecutionPolicy
from runtime.loop import AgentLoop
from runtime.messages import Message
from runtime.policy import ResponsePolicy, ResponseStyle
from runtime.result import LoopError, LoopErrorKind, LoopResult, LoopStatus, LoopStopReason
from runtime.retry_policy import RetryPolicy
from runtime.session import Session
from runtime.session_store import list_sessions, load_session, save_session
from runtime.workspace_context import ParsedIdentity, WorkspaceContext, load_workspace_context

__all__ = [
    "ContextBuilder",
    "ExecutionPolicy",
    "AgentLoop",
    "Message",
    "ResponsePolicy",
    "ResponseStyle",
    "RetryPolicy",
    "LoopResult",
    "LoopStatus",
    "LoopStopReason",
    "LoopError",
    "LoopErrorKind",
    "Session",
    "save_session",
    "load_session",
    "list_sessions",
    "ParsedIdentity",
    "WorkspaceContext",
    "load_workspace_context",
]
