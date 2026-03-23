"""
memory/__init__.py

第 19 步开始，memory 不再只有占位实现，
而是拥有一个最小真实 provider：从 workspace/MEMORY.md 读取内容。

当前暴露：
- MemoryProvider：抽象接口
- PlaceholderMemoryProvider：占位实现（保留，便于对照/回退）
- FileMemoryProvider：最小真实文件实现
"""

from memory.base import MemoryProvider
from memory.file import FileMemoryProvider
from memory.placeholder import PlaceholderMemoryProvider

__all__ = ["MemoryProvider", "PlaceholderMemoryProvider", "FileMemoryProvider"]
