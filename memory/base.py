"""
memory/base.py

这是第 18 步新增的最小 memory 模块接口。

目标不是立刻实现真实记忆系统，
而是先把“memory 作为独立模块”这件事建立起来。

当前职责非常单纯：
- 定义 MemoryProvider 协议/抽象边界
- 约定 ContextBuilder 不再自己持有 memory placeholder 字符串
- 而是向 memory provider 请求一段 memory block

这能让后续扩展更自然：
- FileMemoryProvider
- SummaryMemoryProvider
- RetrievalMemoryProvider
- HybridMemoryProvider
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from runtime.session import Session


class MemoryProvider(Protocol):
    """最小 memory provider 协议。"""

    def build_memory_block(self, session: Session) -> str:
        """根据当前 session 生成要注入 prompt 的 memory 文本块。"""
        ...
