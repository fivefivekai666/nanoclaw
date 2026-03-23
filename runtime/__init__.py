"""
runtime/__init__.py

到了第 18 步，runtime 包继续暴露 context / session / workspace 等能力。

memory 本身已被拆分为独立模块，
因此 runtime 这里只保留对 ContextBuilder 等运行时组件的导出。
"""

from runtime.context import ContextBuilder
from runtime.loop import AgentLoop
from runtime.messages import Message
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
    "Session",
    "save_session",
    "load_session",
    "list_sessions",
    "ParsedIdentity",
    "WorkspaceContext",
    "load_workspace_context",
]
