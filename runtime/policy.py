"""
runtime/policy.py

这是第 22 步新增的 runtime response policy 模块。

目标：
- 把 [INSTRUCTION] section 从 ContextBuilder 内部拆出去
- 让“怎么回答”成为单独的运行时职责
- 为未来扩展 tool-aware / channel-aware / structured-output policy 预留位置

当前保持极简：
- 只定义一个最小 ResponsePolicy
- 返回一组基础响应规则
- 不做复杂策略组合
"""

from __future__ import annotations


class ResponsePolicy:
    """最小 runtime response policy。"""

    def build_instruction_lines(self) -> list[str]:
        """构造 [INSTRUCTION] section 的规则内容。"""
        return [
            "[INSTRUCTION]",
            "Respond as the assistant.",
            "Use the sections above as your operating context.",
            "Ground your answer in the provided context and conversation.",
            "Do not repeat the section headers unless they are directly relevant to the reply.",
        ]
