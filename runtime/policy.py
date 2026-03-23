"""
runtime/policy.py

这是第 24 步的 runtime response policy 模块。

目标：
- 给 response style 增加最小合法值校验
- 对未知 style 做稳定 fallback
- 让 ResponsePolicy 从“可配置”升级为“可控”

当前支持：
- normal
- concise
"""

from __future__ import annotations


class ResponsePolicy:
    """最小 runtime response policy。"""

    ALLOWED_STYLES = {"normal", "concise"}
    DEFAULT_STYLE = "normal"

    def __init__(self, style: str = "normal") -> None:
        self.requested_style = style
        self.style = self.normalize_style(style)
        self.fallback_used = self.style != (style.strip().lower() if style else self.DEFAULT_STYLE)

    @classmethod
    def normalize_style(cls, style: str | None) -> str:
        """把输入 style 规范化，并在非法值时回退到默认值。"""
        if style is None:
            return cls.DEFAULT_STYLE

        normalized = style.strip().lower()
        if not normalized:
            return cls.DEFAULT_STYLE

        if normalized not in cls.ALLOWED_STYLES:
            return cls.DEFAULT_STYLE

        return normalized

    def _style_lines(self) -> list[str]:
        """根据 style 生成额外的回答风格要求。"""
        if self.style == "concise":
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
                f"Unknown response style was normalized/fell back to: {self.style}."
            )

        return lines
