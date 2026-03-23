"""
runtime/__init__.py

到了第 7 步，runtime 包正式暴露两个核心对象：
- AgentLoop：负责主流程控制
- Message：负责统一消息数据结构

这意味着系统开始拥有“流程层 + 数据模型层”的最小组合。
"""

from runtime.loop import AgentLoop
from runtime.messages import Message

__all__ = ["AgentLoop", "Message"]
