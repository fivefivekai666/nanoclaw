"""
runtime/context.py

这是第 21 步的 ContextBuilder。

这一版的核心目标不是增加更多上下文来源，
而是把已有上下文整理成稳定、固定、可扩展的 prompt 模板。

从这一版开始，prompt 会使用明确的 section：
- [SYSTEM]
- [IDENTITY]
- [WORKSPACE]
- [MEMORY]
- [CONVERSATION]
- [INSTRUCTION]

这样做的意义是：
- loop 每轮输入结构稳定
- 调试时更容易定位问题
- 后面加入 tools / safety / recalled memory 时有明确插槽
"""

from __future__ import annotations

from memory.base import MemoryProvider
from runtime.session import Session
from runtime.workspace_context import WorkspaceContext


class ContextBuilder:
    """
    最小上下文构造器。

    当前负责把：
    - system_prompt
    - identity / persona（config）
    - workspace identity（结构化或原文回退）
    - workspace soul（原文）
    - memory block（来自 memory provider）
    - session.messages
    - 最终响应指令

    组合成 provider 可消费的一段稳定 prompt 文本。
    """

    def __init__(
        self,
        system_prompt: str,
        identity_name: str,
        identity_role: str,
        persona_style: str,
        memory_provider: MemoryProvider,
        workspace_context: WorkspaceContext | None = None,
    ) -> None:
        self.system_prompt = system_prompt
        self.identity_name = identity_name
        self.identity_role = identity_role
        self.persona_style = persona_style
        self.memory_provider = memory_provider
        self.workspace_context = workspace_context or WorkspaceContext()

    def _build_identity_section(self) -> list[str]:
        return [
            "[IDENTITY]",
            f"name: {self.identity_name}",
            f"role: {self.identity_role}",
            f"style: {self.persona_style}",
        ]

    def _build_workspace_section(self) -> list[str]:
        lines: list[str] = ["[WORKSPACE]"]
        workspace_identity = self.workspace_context.identity
        has_structured_identity = any(
            [
                workspace_identity.name,
                workspace_identity.creature,
                workspace_identity.vibe,
                workspace_identity.emoji,
                workspace_identity.avatar,
                workspace_identity.extras,
            ]
        )

        if has_structured_identity:
            lines.append("workspace_identity:")
            if workspace_identity.name:
                lines.append(f"- name: {workspace_identity.name}")
            if workspace_identity.creature:
                lines.append(f"- creature: {workspace_identity.creature}")
            if workspace_identity.vibe:
                lines.append(f"- vibe: {workspace_identity.vibe}")
            if workspace_identity.emoji:
                lines.append(f"- emoji: {workspace_identity.emoji}")
            if workspace_identity.avatar:
                lines.append(f"- avatar: {workspace_identity.avatar}")
            for key, value in workspace_identity.extras.items():
                lines.append(f"- {key}: {value}")
        elif self.workspace_context.identity_text:
            lines.append("workspace_identity_raw:")
            lines.append(self.workspace_context.identity_text)
        else:
            lines.append("workspace_identity: [none]")

        if self.workspace_context.soul_text:
            lines.append("")
            lines.append("workspace_soul:")
            lines.append(self.workspace_context.soul_text)
        else:
            lines.append("")
            lines.append("workspace_soul: [none]")

        return lines

    def _build_memory_section(self, session: Session) -> list[str]:
        return [
            "[MEMORY]",
            self.memory_provider.build_memory_block(session),
        ]

    def _build_conversation_section(self, session: Session) -> list[str]:
        lines: list[str] = ["[CONVERSATION]"]
        if not session.messages:
            lines.append("[empty]")
            return lines

        for message in session.messages:
            lines.append(f"{message.role}: {message.content}")
        return lines

    def _build_instruction_section(self) -> list[str]:
        return [
            "[INSTRUCTION]",
            "Respond as the assistant.",
            "Use the sections above as your operating context.",
            "Ground your answer in the provided context and conversation.",
            "Do not repeat the section headers unless they are directly relevant to the reply.",
        ]

    def build(self, session: Session) -> str:
        """根据 session 构造一段稳定的 section-based prompt。"""
        sections: list[list[str]] = [
            ["[SYSTEM]", self.system_prompt],
            self._build_identity_section(),
            self._build_workspace_section(),
            self._build_memory_section(session),
            self._build_conversation_section(session),
            self._build_instruction_section(),
        ]

        lines: list[str] = []
        for index, section_lines in enumerate(sections):
            if index > 0:
                lines.append("")
            lines.extend(section_lines)

        return "\n".join(lines)
