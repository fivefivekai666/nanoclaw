"""
runtime/policy.py

这是第 23 步的 runtime response policy 模块。

目标：
- 把 [INSTRUCTION] section 继续从“固定规则”升级成“最小可配置规则”
- 当前只支持两档：
  - normal
  - concise
- 让 loop 在不增加太多复杂度的前提下，开始具备可控输出风格
"""

from __future__ import annotations


class ResponsePolicy:
    """最小 runtime response policy。"""

    def __init__(self, style: str = "normal") -> None:
        self.style = style

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
        return [
            "[INSTRUCTION]",
            "Respond as the assistant.",
            "Use the sections above as your operating context.",
            "Ground your answer in the provided context and conversation.",
            *self._style_lines(),
            "Do not repeat the section headers unless they are directly relevant to the reply.",
        ]
