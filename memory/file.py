"""
memory/file.py

这是第 19 步的最小真实 memory provider。

目标：
- 不再返回固定 placeholder
- 而是实际读取 workspace/MEMORY.md
- 把文件内容作为 memory block 注入 ContextBuilder

当前仍然保持极简：
- 不做解析
- 不做裁剪
- 不做摘要
- 不做检索
- 文件不存在时不报错，返回清晰的空提示
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from memory.base import MemoryProvider

if TYPE_CHECKING:
    from runtime.session import Session


class FileMemoryProvider(MemoryProvider):
    """从 workspace/MEMORY.md 读取原始 memory 文本。"""

    def __init__(self, workspace_dir: str | Path, memory_filename: str = "MEMORY.md") -> None:
        self.workspace_dir = Path(workspace_dir)
        self.memory_filename = memory_filename

    @property
    def memory_path(self) -> Path:
        """返回当前 memory 文件路径。"""
        return self.workspace_dir / self.memory_filename

    def build_memory_block(self, session: Session) -> str:
        """读取 MEMORY.md；若不存在则返回空 memory 提示。"""
        memory_path = self.memory_path
        if not memory_path.exists() or not memory_path.is_file():
            return "[memory file not found: workspace/MEMORY.md]"

        content = memory_path.read_text(encoding="utf-8").strip()
        if not content:
            return "[memory file is empty: workspace/MEMORY.md]"

        return content
