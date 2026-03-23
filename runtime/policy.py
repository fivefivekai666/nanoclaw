"""
runtime/policy.py

这是第 25 步的 runtime response policy 模块。

目标：
- 把 response_style 从裸字符串升级成受限类型入口
- 保留第 24 步已有的合法值校验、fallback、可观察性
- 减少 runtime 里到处手写字符串判断

当前支持：
- normal
- concise
"""

from __future__ import annotations

from enum import StrEnum


class ResponseStyle(StrEnum):
    """受限的 response style 枚举。"""

    NORMAL = "normal"
    CONCISE = "concise"


class ResponsePolicy:
    """最小 runtime response policy。"""

    DEFAULT_STYLE = ResponseStyle.NORMAL

    def __init__(self, style: str | ResponseStyle = ResponseStyle.NORMAL) -> None:
        self.requested_style = str(style)
        self.style = self.normalize_style(style)
        normalized_requested = self._normalize_raw(style)
        self.fallback_used = self.style.value != normalized_requested

    @classmethod
    def _normalize_raw(cls, style: str | ResponseStyle | None) -> str:
        """把原始输入归一化成最接近合法判断的字符串。"""
        if style is None:
            return cls.DEFAULT_STYLE.value

        if isinstance(style, ResponseStyle):
            return style.value

        normalized = style.strip().lower()
        if not normalized:
            return cls.DEFAULT_STYLE.value

        return normalized

    @classmethod
    def normalize_style(cls, style: str | ResponseStyle | None) -> ResponseStyle:
        """把输入 style 规范化成 ResponseStyle，并在非法值时回退到默认值。"""
        normalized = cls._normalize_raw(style)

        try:
            return ResponseStyle(normalized)
        except ValueError:
            return cls.DEFAULT_STYLE

    def _style_lines(self) -> list[str]:
        """根据 style 生成额外的回答风格要求。"""
        if self.style is ResponseStyle.CONCISE:
            return [
                "Prefer concise answers.",
                "Keep the response short, direct, and high-signal.",
                "Avoid unnecessary elaboration unless the user asks for detail.",
            ]

        return [
            "Provide a normal level of explanation.",
            "Be clear, structured, and helpful.",
        ]

    def build_instruction_lines(self) -> list[str]:
        """构造 [INSTRUCTION] section 的规则内容。"""
        lines = [
            "[INSTRUCTION]",
            "Respond as the assistant.",
            "Use the sections above as your operating context.",
            "Ground your answer in the provided context and conversation.",
            *self._style_lines(),
            "Do not repeat the section headers unless they are directly relevant to the reply.",
        ]

        if self.fallback_used:
            lines.append(
                f"Unknown response style was normalized/fell back to: {self.style.value}."
            )

        return lines
