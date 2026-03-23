"""
runtime/workspace_context.py

这是最小 workspace context 读取模块。

到了第 17 步，我们开始对 IDENTITY.md 做最小结构化解析，
目标不是成为完整 markdown 解析器，而只是把最关键的身份字段提取出来。

当前策略：
1. 读取 IDENTITY.md / SOUL.md
2. 对 IDENTITY.md 尝试解析最简单的 `- Key: Value` 项
3. 若无法解析，也仍然保留原始文本作为兜底
4. SOUL.md 先继续按原文注入
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class ParsedIdentity:
    """从 IDENTITY.md 中提取出的最小结构化身份字段。"""

    name: str = ""
    creature: str = ""
    vibe: str = ""
    emoji: str = ""
    avatar: str = ""
    extras: dict[str, str] = field(default_factory=dict)


@dataclass
class WorkspaceContext:
    """最小 workspace context 容器。"""

    identity_text: str = ""
    identity: ParsedIdentity = field(default_factory=ParsedIdentity)
    soul_text: str = ""


def _read_text_if_exists(path: Path) -> str:
    """如果文件存在则读取文本，否则返回空字符串。"""
    if not path.exists() or not path.is_file():
        return ""
    return path.read_text(encoding="utf-8").strip()


def _normalize_identity_key(key: str) -> str:
    """把 IDENTITY.md 里的展示字段名归一化为内部键。"""
    normalized = key.strip().lower().replace("**", "")
    normalized = normalized.replace("-", " ").replace("_", " ")
    normalized = " ".join(normalized.split())

    mapping = {
        "name": "name",
        "creature": "creature",
        "vibe": "vibe",
        "emoji": "emoji",
        "avatar": "avatar",
    }
    return mapping.get(normalized, normalized)


def _parse_identity_text(text: str) -> ParsedIdentity:
    """
    对 IDENTITY.md 做最小结构化解析。

    当前只解析类似下面的行：
    - Name: myagent
    - Creature: ghost
    - Vibe: warm

    解析不到的行直接跳过，不报错。
    """
    parsed = ParsedIdentity()

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line.startswith("-") or ":" not in line:
            continue

        content = line[1:].strip()
        key, value = content.split(":", 1)
        normalized_key = _normalize_identity_key(key)
        clean_value = value.strip()

        if not clean_value or clean_value == "_(pick something you like)_":
            continue

        if normalized_key == "name":
            parsed.name = clean_value
        elif normalized_key == "creature":
            parsed.creature = clean_value
        elif normalized_key == "vibe":
            parsed.vibe = clean_value
        elif normalized_key == "emoji":
            parsed.emoji = clean_value
        elif normalized_key == "avatar":
            parsed.avatar = clean_value
        else:
            parsed.extras[normalized_key] = clean_value

    return parsed


def load_workspace_context(workspace_dir: str | Path) -> WorkspaceContext:
    """
    从 workspace 目录加载最小 persona 上下文。

    当前读取：
    - IDENTITY.md（原文 + 最小结构化解析）
    - SOUL.md（原文）
    """
    base_dir = Path(workspace_dir)
    identity_path = base_dir / "IDENTITY.md"
    soul_path = base_dir / "SOUL.md"

    identity_text = _read_text_if_exists(identity_path)
    soul_text = _read_text_if_exists(soul_path)

    return WorkspaceContext(
        identity_text=identity_text,
        identity=_parse_identity_text(identity_text),
        soul_text=soul_text,
    )
