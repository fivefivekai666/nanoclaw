"""
runtime/__init__.py

到了第 22 步，runtime 包继续暴露 context / session / workspace 等能力，
并新增独立的 response policy 层。

这样 runtime 里的职责拆分更清楚：
- ContextBuilder：上下文装配
- ResponsePolicy：回答规则装配
- AgentLoop：运行时调度
"""

from runtime.context import ContextBuilder
from runtime.loop import AgentLoop
from runtime.messages import Message
from runtime.policy import ResponsePolicy
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
    "Session",
    "save_session",
    "load_session",
    "list_sessions",
    "ParsedIdentity",
    "WorkspaceContext",
    "load_workspace_context",
]
