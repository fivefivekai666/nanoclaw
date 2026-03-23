"""
runtime/session_store.py

这是最小会话持久化与管理层。

目前支持：
- save_session(...)
- load_session(...)
- list_sessions(...)

第 12 步开始，这里除了保存/读取单个会话，
还负责“列出当前有哪些会话文件”，
从而给 CLI 提供最小 session 管理能力。
"""

from __future__ import annotations

import json
from pathlib import Path

from runtime.session import Session


def _session_file_path(session_id: str, base_dir: Path) -> Path:
    """根据 session_id 计算会话文件路径。"""
    return base_dir / f"{session_id}.json"


def save_session(session: Session, base_dir: Path) -> Path:
    """把一个 Session 保存到磁盘。"""
    base_dir.mkdir(parents=True, exist_ok=True)
    file_path = _session_file_path(session.id, base_dir)
    file_path.write_text(
        json.dumps(session.model_dump(), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return file_path


def load_session(session_id: str, base_dir: Path) -> Session | None:
    """从磁盘读取一个 Session；若不存在则返回 None。"""
    file_path = _session_file_path(session_id, base_dir)
    if not file_path.exists():
        return None

    raw_data = json.loads(file_path.read_text(encoding="utf-8"))
    return Session.model_validate(raw_data)


def list_sessions(base_dir: Path) -> list[Session]:
    """
    列出某个目录下所有已保存的 session。

    返回值按文件名排序，方便稳定输出和教学演示。
    如果目录不存在，则返回空列表。
    """
    if not base_dir.exists():
        return []

    sessions: list[Session] = []
    for file_path in sorted(base_dir.glob("*.json")):
        raw_data = json.loads(file_path.read_text(encoding="utf-8"))
        sessions.append(Session.model_validate(raw_data))
    return sessions
