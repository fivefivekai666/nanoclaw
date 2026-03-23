"""
runtime/context.py

这是最小 ContextBuilder。

到了第 15 步，它不再只负责：
- system_prompt
- session history

还开始正式接入 agent 的 identity / persona：
- identity_name
- identity_role
- persona_style

这意味着 provider 接收到的上下文，
已经不只是“规则 + 历史”，
而是开始拥有“角色 + 风格 + 历史”。
"""

from __future__ import annotations

from runtime.session import Session


class ContextBuilder:
    """
    最小上下文构造器。

    当前负责把：
    - system_prompt
    - identity / persona
    - session.messages

    组合成 provider 可消费的一段 prompt 文本。
    """

    def __init__(
        self,
        system_prompt: str,
        identity_name: str,
        identity_role: str,
        persona_style: str,
    ) -> None:
        self.system_prompt = system_prompt
        self.identity_name = identity_name
        self.identity_role = identity_role
        self.persona_style = persona_style

    def build(self, session: Session) -> str:
        """
        根据 session 构造一段最小 prompt。

        当前结构：

            system: ...

            identity:
            - name: ...
            - role: ...
            - style: ...

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
        lines.extend(f"{message.role}: {message.content}" for message in session.messages)
        return "\n".join(lines)
