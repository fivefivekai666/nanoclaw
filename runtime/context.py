"""
runtime/context.py

这是最小 ContextBuilder。

到了第 18 步，memory 不再是 ContextBuilder 内部持有的一段字符串，
而是被抽成独立模块接口：memory provider。

当前策略：
- config identity/persona：稳定的结构化默认层
- workspace identity：优先注入结构化字段
- workspace soul：暂时继续原文注入
- memory：通过独立 memory provider 生成

这样 ContextBuilder 只负责“装配上下文”，
而不再负责决定 memory 的来源与实现细节。
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
    - workspace identity（结构化）
    - workspace soul（原文）
    - memory block（来自 memory provider）
    - session.messages

    组合成 provider 可消费的一段 prompt 文本。
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

    def build(self, session: Session) -> str:
        """根据 session 构造一段最小 prompt。"""
        lines: list[str] = [
            f"system: {self.system_prompt}",
            "",
            "identity:",
            f"- name: {self.identity_name}",
            f"- role: {self.identity_role}",
            f"- style: {self.persona_style}",
            "",
        ]

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
            lines.append("workspace.identity:")
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
            lines.append("")
        elif self.workspace_context.identity_text:
            lines.extend([
                "workspace.identity.raw:",
                self.workspace_context.identity_text,
                "",
            ])

        if self.workspace_context.soul_text:
            lines.extend([
                "workspace.soul:",
                self.workspace_context.soul_text,
                "",
            ])

        lines.extend([
            "memory:",
            self.memory_provider.build_memory_block(session),
            "",
        ])

        lines.extend(f"{message.role}: {message.content}" for message in session.messages)
        return "\n".join(lines)
