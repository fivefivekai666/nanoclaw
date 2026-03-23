"""
memory/__init__.py

第 18 步开始，memory 成为独立模块。

当前先暴露：
- MemoryProvider：抽象接口
- PlaceholderMemoryProvider：占位实现

后续可以继续扩展真实 memory provider。
"""

from memory.base import MemoryProvider
from memory.placeholder import PlaceholderMemoryProvider

__all__ = ["MemoryProvider", "PlaceholderMemoryProvider"]
