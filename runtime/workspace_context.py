"""
runtime/workspace_context.py

这是第 16 步新增的最小 workspace context 读取模块。

目标不是做复杂知识库，也不是做完整 markdown 解析器，
而只是把 agent 工作目录里的两个关键 persona 文件接进来：
- IDENTITY.md
- SOUL.md

当前策略非常克制：
1. 如果文件存在，就读取原始文本
2. 如果文件不存在，就返回空值
3. 上层 ContextBuilder 决定如何把这些内容注入 prompt

这样可以先打通“workspace 文件 -> runtime context”这条链路。
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass
class WorkspaceContext:
    """最小 workspace context 容器。"""

    identity_text: str = ""
    soul_text: str = ""


def _read_text_if_exists(path: Path) -> str:
    """如果文件存在则读取文本，否则返回空字符串。"""
    if not path.exists() or not path.is_file():
        return ""
    return path.read_text(encoding="utf-8").strip()


def load_workspace_context(workspace_dir: str | Path) -> WorkspaceContext:
    """
    从 workspace 目录加载最小 persona 上下文。

    当前只读取：
    - IDENTITY.md
    - SOUL.md
    """
    base_dir = Path(workspace_dir)
    identity_path = base_dir / "IDENTITY.md"
    soul_path = base_dir / "SOUL.md"

    return WorkspaceContext(
        identity_text=_read_text_if_exists(identity_path),
        soul_text=_read_text_if_exists(soul_path),
    )
