"""
runtime/context.py

这是最小 ContextBuilder。

到了第 16 步，它除了接收 config 里的 identity / persona，
还开始接收来自 workspace 文件的最小 persona context：
- workspace/IDENTITY.md
- workspace/SOUL.md

注入策略：
- config identity/persona 仍然保留，作为结构化默认身份层
- workspace 文件若存在，则作为更接近真实 agent 自我描述的补充层注入

这意味着 provider 接收到的上下文，
已经从“规则 + 身份 + 历史”继续升级为：
“规则 + 结构化身份 + workspace persona + 历史”。
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
    ) -> None:
        self.system_prompt = system_prompt
        self.identity_name = identity_name
        self.identity_role = identity_role
        self.persona_style = persona_style
        self.workspace_context = workspace_context or WorkspaceContext()

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

        lines.extend(f"{message.role}: {message.content}" for message in session.messages)
        return "\n".join(lines)
