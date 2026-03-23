"""
runtime/loop.py

这是第 5 步的核心文件：最小 AgentLoop。

前几步我们已经分别准备了：
- Config：配置对象
- loader：配置加载入口
- Provider：模型适配层

但这些还只是“零件”。
真正让它们开始协同工作的，是 AgentLoop。

你可以把 AgentLoop 理解成：

    “agent runtime 的最小主流程控制器”

它的职责不是关心某家模型 API 的细节，
而是负责安排一轮 agent 执行流程：
1. 接收输入
2. 调用 provider
3. 返回输出

第 5 步我们故意不做复杂多轮，也不引入 tools / memory / session。
只先做一个最小可运行的“单轮执行”。
"""

from __future__ import annotations

from providers.base import BaseProvider


class AgentLoop:
    """
    AgentLoop 是 agent 运行时的最小主循环骨架。

    注意这里的“loop”在当前阶段并不意味着复杂的 while True 多轮循环，
    它更像是：

        “跑一轮 agent 处理流程的入口对象”

    后面它会逐步长出更多能力，例如：
    - system prompt 拼接
    - context 构建
    - memory 注入
    - tool calls
    - session 记录
    - subagent 分发

    但第 5 步只保留最核心的一件事：
    把输入交给 provider，再拿回结果。
    """

    def __init__(self, provider: BaseProvider) -> None:
        """
        创建一个 AgentLoop。

        参数：
        - provider: 模型提供商适配层实例

        为什么要把 provider 注入进来，而不是在 AgentLoop 里自己创建？
        因为这能保持职责清晰：
        - Config / 工厂 决定“用哪个 provider”
        - AgentLoop 只负责“怎么使用 provider”
        """
        self.provider = provider

    def run_once(self, user_input: str) -> str:
        """
        执行一轮最小 agent 流程。

        当前流程非常简单：
        1. 收到用户输入
        2. 直接交给 provider.chat(...)
        3. 返回 provider 的结果

        这个函数之所以叫 run_once，是为了刻意强调：
        我们现在先跑通“一轮”，
        而不是一下进入复杂的多轮会话系统。
        """
        response = self.provider.chat(user_input)
        return response
