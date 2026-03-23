"""
runtime/__init__.py

到了第 26 步，runtime 包继续暴露 context / session / workspace / policy / loop result 等能力。

这样 runtime 里的职责拆分更清楚：
- ContextBuilder：上下文装配
- ResponsePolicy：回答规则装配
- ResponseStyle：回答风格的受限类型入口
- AgentLoop：运行时调度
- LoopResult：一次 loop 执行的结构化结果边界
"""

from runtime.context import ContextBuilder
from runtime.loop import AgentLoop
from runtime.messages import Message
from runtime.policy import ResponsePolicy, ResponseStyle
from runtime.result import LoopResult
from runtime.session import Session
from runtime.session_store import list_sessions, load_session, save_session
from runtime.workspace_context import (
    ParsedIdentity,
    WorkspaceContext,
    load_workspace_context,
)

__all__ = [
    "ContextBuilder",
    "AgentLoop",
    "Message",
    "ResponsePolicy",
    "ResponseStyle",
    "LoopResult",
    "Session",
    "save_session",
    "load_session",
    "list_sessions",
    "ParsedIdentity",
    "WorkspaceContext",
    "load_workspace_context",
]
