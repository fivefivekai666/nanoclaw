"""
runtime/__init__.py

到了第 17 步，runtime 包除了暴露 workspace context 加载能力，
也开始显式暴露结构化身份模型。

这意味着 workspace persona 不再只是原始文本块，
而是开始出现可编程消费的最小字段结构。
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
