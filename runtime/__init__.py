"""
runtime/__init__.py

到了第 10 步，runtime 包正式暴露：
- Message：统一消息数据结构
- Session：最小会话容器
- AgentLoop：主流程控制器
- save_session / load_session：最小会话持久化能力

这意味着系统开始拥有：
数据单位 → 数据容器 → 处理流程 → 最小落盘能力
这样的 runtime 骨架。
"""

from runtime.loop import AgentLoop
from runtime.messages import Message
from runtime.session import Session
from runtime.session_store import load_session, save_session

__all__ = ["AgentLoop", "Message", "Session", "save_session", "load_session"]
