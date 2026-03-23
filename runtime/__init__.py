"""
runtime/__init__.py

到了第 9 步，runtime 包正式暴露三个核心对象：
- Message：统一消息数据结构
- Session：最小会话容器
- AgentLoop：主流程控制器

这意味着系统开始拥有：
数据单位（Message）→ 数据容器（Session）→ 处理流程（AgentLoop）
这样的最小 runtime 骨架。
"""

from runtime.loop import AgentLoop
from runtime.messages import Message
from runtime.session import Session

__all__ = ["AgentLoop", "Message", "Session"]
