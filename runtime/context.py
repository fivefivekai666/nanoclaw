"""
runtime/context.py

这是最小 ContextBuilder。

到了第 17 步的这个前置动作，它除了接收：
- system prompt
- config identity / persona
- workspace persona
- session history

还开始预留一个最小 memory placeholder。

注意：
- 这一步还没有真实 memory store
- 也没有记忆检索/压缩/筛选逻辑
- 只是先在 prompt 骨架中留出 memory 段

这样后面接真实 memory 时，就不需要再改上下文整体结构。
"""

from __future__ import annotations

from runtime.session import Session
from runtime.workspace_context import WorkspaceContext


class ContextBuilder:
    """
    最小上下文构造器。

    当前负责把：
    - system_prompt
    - identity / persona（config）
    - workspace persona（IDENTITY.md / SOUL.md）
    - memory placeholder
    - session.messages

    组合成 provider 可消费的一段 prompt 文本。
    """

    def __init__(
        self,
        system_prompt: str,
        identity_name: str,
        identity_role: str,
        persona_style: str,
        workspace_context: WorkspaceContext | None = None,
        memory_placeholder: str = "[memory placeholder: not implemented yet]",
    ) -> None:
        self.system_prompt = system_prompt
        self.identity_name = identity_name
        self.identity_role = identity_role
        self.persona_style = persona_style
        self.workspace_context = workspace_context or WorkspaceContext()
        self.memory_placeholder = memory_placeholder

    def build(self, session: Session) -> str:
        """
        根据 session 构造一段最小 prompt。

        当前结构：

            system: ...

            identity:
            - name: ...
            - role: ...
            - style: ...

            workspace.identity:
            ...

            workspace.soul:
            ...

            memory:
            ...

            user: ...
            assistant: ...
        """
        lines: list[str] = [
            f"system: {self.system_prompt}",
            "",
            "identity:",
            f"- name: {self.identity_name}",
            f"- role: {self.identity_role}",
            f"- style: {self.persona_style}",
            "",
        ]

        if self.workspace_context.identity_text:
            lines.extend([
                "workspace.identity:",
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
            self.memory_placeholder,
            "",
        ])

        lines.extend(f"{message.role}: {message.content}" for message in session.messages)
        return "\n".join(lines)
