"""
runtime/session_store.py

这是第 10 步新增的最小持久化层。

为什么单独做一个 store 文件？
因为 Session 是“数据结构”，而 session_store 是“存储方式”。
这两个概念应该分开。

第 10 步只实现最小功能：
- save_session(...)
- load_session(...)
- 默认把每个 session 存成一个 JSON 文件

存储路径形式：
    <base_dir>/<session_id>.json

这样做简单、可读、好调试，也方便后续升级成别的存储方案。
"""

from __future__ import annotations

import json
from pathlib import Path

from runtime.session import Session


def _session_file_path(session_id: str, base_dir: Path) -> Path:
    """根据 session_id 计算会话文件路径。"""
    return base_dir / f"{session_id}.json"


def save_session(session: Session, base_dir: Path) -> Path:
    """
    把一个 Session 保存到磁盘。

    参数：
    - session: 要保存的会话对象
    - base_dir: 会话目录，例如 workspace/sessions

    返回：
    - 实际写入的文件路径
    """
    base_dir.mkdir(parents=True, exist_ok=True)
    file_path = _session_file_path(session.id, base_dir)
    file_path.write_text(
        json.dumps(session.model_dump(), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return file_path


def load_session(session_id: str, base_dir: Path) -> Session | None:
    """
    从磁盘读取一个 Session。

    如果文件不存在，则返回 None，
    这样调用方可以决定是否创建一个新会话。
    """
    file_path = _session_file_path(session_id, base_dir)
    if not file_path.exists():
        return None

    raw_data = json.loads(file_path.read_text(encoding="utf-8"))
    return Session.model_validate(raw_data)
