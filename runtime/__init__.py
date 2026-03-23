"""
runtime/__init__.py

到了第 16 步，runtime 包除了暴露流程、消息、会话、存储之外，
也开始暴露最小 workspace context 能力。

这意味着系统第一次拥有：
- 从 workspace 文件读取 agent persona
- 并把它注入 runtime context

这条完整链路。
"""

from runtime.context import ContextBuilder
from runtime.loop import AgentLoop
from runtime.messages import Message
from runtime.session import Session
from runtime.session_store import list_sessions, load_session, save_session
from runtime.workspace_context import WorkspaceContext, load_workspace_context

__all__ = [
    "ContextBuilder",
    "AgentLoop",
    "Message",
    "Session",
    "save_session",
    "load_session",
    "list_sessions",
    "WorkspaceContext",
    "load_workspace_context",
]
