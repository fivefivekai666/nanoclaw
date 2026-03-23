"""
memory/placeholder.py

这是第 18 步的最小 placeholder memory provider。

注意：
- 它不是正式记忆系统
- 不读取文件
- 不做检索
- 不做压缩
- 不做总结

它唯一的任务是：
先以模块化方式返回一段 memory placeholder，
让上层 ContextBuilder 改成依赖 memory provider 接口。
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from memory.base import MemoryProvider

if TYPE_CHECKING:
    from runtime.session import Session


class PlaceholderMemoryProvider(MemoryProvider):
    """返回固定占位文本的最小 memory provider。"""

    def __init__(self, placeholder_text: str = "[memory placeholder: not implemented yet]") -> None:
        self.placeholder_text = placeholder_text

    def build_memory_block(self, session: Session) -> str:
        """忽略 session 内容，直接返回固定占位文本。"""
        return self.placeholder_text
