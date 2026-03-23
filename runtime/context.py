"""
runtime/context.py

这是第 22 步的 ContextBuilder。

这一版的重点不是新增上下文来源，
而是继续梳理职责边界：
- ContextBuilder 负责组织上下文内容
- ResponsePolicy 负责组织回答规则

从这一版开始，[INSTRUCTION] 不再由 ContextBuilder 内部硬编码，
而是来自独立的 runtime response policy 层。
"""

from __future__ import annotations

from memory.base import MemoryProvider
from runtime.policy import ResponsePolicy
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
    - instruction section（来自 response policy）

    组合成 provider 可消费的一段稳定 prompt 文本。
    """

    def __init__(
        self,
        system_prompt: str,
        identity_name: str,
        identity_role: str,
        persona_style: str,
        memory_provider: MemoryProvider,
        response_policy: ResponsePolicy,
        workspace_context: WorkspaceContext | None = None,
    ) -> None:
        self.system_prompt = system_prompt
        self.identity_name = identity_name
        self.identity_role = identity_role
        self.persona_style = persona_style
        self.memory_provider = memory_provider
        self.response_policy = response_policy
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

    def build(self, session: Session) -> str:
        """根据 session 构造一段稳定的 section-based prompt。"""
        sections: list[list[str]] = [
            ["[SYSTEM]", self.system_prompt],
            self._build_identity_section(),
            self._build_workspace_section(),
            self._build_memory_section(session),
            self._build_conversation_section(session),
            self.response_policy.build_instruction_lines(),
        ]

        lines: list[str] = []
        for index, section_lines in enumerate(sections):
            if index > 0:
                lines.append("")
            lines.extend(section_lines)

        return "\n".join(lines)
