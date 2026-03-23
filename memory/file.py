"""
memory/file.py

这是第 20 步的最小结构化 file memory provider。

目标：
- 继续读取 workspace/MEMORY.md
- 但不再把原文整个直接塞进 prompt
- 而是做最小结构化清洗，只保留有效内容块

当前只做低风险清洗：
- 去掉顶层标题（如 # MEMORY.md）
- 去掉 HTML 注释行（如 <!-- ... -->）
- 压缩连续空行为单个空行

注意：
- 还不做语义摘要
- 还不做检索
- 还不做分段打分
- 还不做 token budgeting
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from memory.base import MemoryProvider

if TYPE_CHECKING:
    from runtime.session import Session


class FileMemoryProvider(MemoryProvider):
    """从 workspace/MEMORY.md 读取并做最小结构化清洗。"""

    def __init__(self, workspace_dir: str | Path, memory_filename: str = "MEMORY.md") -> None:
        self.workspace_dir = Path(workspace_dir)
        self.memory_filename = memory_filename

    @property
    def memory_path(self) -> Path:
        """返回当前 memory 文件路径。"""
        return self.workspace_dir / self.memory_filename

    def _extract_effective_lines(self, raw_text: str) -> list[str]:
        """从原始 MEMORY.md 中提取最小有效内容块。"""
        lines = raw_text.splitlines()
        cleaned_lines: list[str] = []
        title_removed = False
        previous_was_blank = False

        for line in lines:
            stripped = line.strip()

            # 去掉最外层标题，例如：# MEMORY.md
            if not title_removed and stripped.lower() == "# memory.md":
                title_removed = True
                continue

            # 去掉纯 HTML 注释行
            if stripped.startswith("<!--") and stripped.endswith("-->"):
                continue

            # 压缩连续空行
            if stripped == "":
                if cleaned_lines and not previous_was_blank:
                    cleaned_lines.append("")
                previous_was_blank = True
                continue

            cleaned_lines.append(line.rstrip())
            previous_was_blank = False

        while cleaned_lines and cleaned_lines[0] == "":
            cleaned_lines.pop(0)
        while cleaned_lines and cleaned_lines[-1] == "":
            cleaned_lines.pop()

        return cleaned_lines

    def build_memory_block(self, session: Session) -> str:
        """读取 MEMORY.md，并返回清洗后的有效 memory 内容。"""
        memory_path = self.memory_path
        if not memory_path.exists() or not memory_path.is_file():
            return "[memory file not found: workspace/MEMORY.md]"

        raw_text = memory_path.read_text(encoding="utf-8")
        effective_lines = self._extract_effective_lines(raw_text)

        if not effective_lines:
            return "[memory file has no effective content: workspace/MEMORY.md]"

        return "\n".join(effective_lines)
