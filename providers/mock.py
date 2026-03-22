"""
providers/mock.py

这是第 4 步的“假 provider”。

为什么现在先写一个假的，而不是立刻接 OpenAI？
因为我们当前的重点是：

1. 搭清楚项目结构
2. 跑通 provider 这条调用链
3. 让你理解 provider 层的职责

如果现在直接接真实 API，你会立刻碰到：
- API key
- 网络错误
- SDK 版本
- 请求格式差异
- 限流与重试

这些问题都是真的，但它们会把注意力从“架构学习”拉走。
所以我们先用 MockProvider 把整条链路跑通。
"""

from __future__ import annotations

from providers.base import BaseProvider


class MockProvider(BaseProvider):
    """
    一个最小可用的 provider 假实现。

    它不会真的请求任何模型服务，
    而是把收到的 prompt 简单包装后返回。

    这样做的价值在于：
    - runtime 可以先跑起来
    - main.py 可以先演示 provider 调用
    - 后面替换成真实 provider 时，上层代码改动会很小
    """

    def __init__(self, model: str = "mock-echo-v1") -> None:
        self.model = model

    def chat(self, prompt: str) -> str:
        """
        接收一个 prompt，并返回模拟输出。

        这里故意做成“回显”风格，
        因为这样最容易看清楚：
        - main.py 确实调用了 provider
        - provider 确实拿到了输入
        - provider 确实返回了结果
        """
        return f"[mock-provider:{self.model}] you said: {prompt}"
