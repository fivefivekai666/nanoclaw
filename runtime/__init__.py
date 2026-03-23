"""
runtime/__init__.py

到了第 12 步，runtime 包正式暴露：
- Message：统一消息数据结构
- Session：最小会话容器
- AgentLoop：主流程控制器
- save_session / load_session：最小会话持久化能力
- list_sessions：最小会话管理能力

这意味着系统开始拥有：
数据单位 → 数据容器 → 处理流程 → 持久化 → 最小管理面
这样的 runtime 骨架。
"""

from runtime.loop import AgentLoop
from runtime.messages import Message
from runtime.session import Session
from runtime.session_store import list_sessions, load_session, save_session

__all__ = [
    "AgentLoop",
    "Message",
    "Session",
    "save_session",
    "load_session",
    "list_sessions",
]
