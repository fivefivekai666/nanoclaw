"""
runtime/__init__.py

到了第 14 步，runtime 包正式开始区分：
- Loop：负责流程推进
- ContextBuilder：负责上下文构造

这意味着系统的最小骨架已经不再只是“能跑”，
而是开始出现清晰的职责分层。
"""

from runtime.context import ContextBuilder
from runtime.loop import AgentLoop
from runtime.messages import Message
from runtime.session import Session
from runtime.session_store import list_sessions, load_session, save_session

__all__ = [
    "ContextBuilder",
    "AgentLoop",
    "Message",
    "Session",
    "save_session",
    "load_session",
    "list_sessions",
]
