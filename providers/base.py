"""
providers/base.py

这个文件以后会定义“模型提供商”的统一抽象层。

为什么需要这一层？
因为你的 agent 将来不应该只绑定某一家模型服务。
你可能会接：
- OpenAI
- Anthropic
- OpenRouter
- LiteLLM
- 本地模型
- 自定义兼容接口

所以我们通常会先定义一个统一接口，
让上层 runtime 不关心“底层到底是哪家模型”。

第 1 步先不实现真实调用，
只放一个最小骨架，帮助你理解未来结构。
"""


class BaseProvider:
    """
    所有模型 provider 的基类。

    将来真正的 provider（例如 OpenAIProvider）
    会继承这个类，并实现 chat() 方法。
    """

    def chat(self, prompt: str) -> str:
        """
        给定一个 prompt，返回模型输出。

        参数:
            prompt: 传给模型的一段文本

        返回:
            模型返回的文本

        当前先抛出异常，表示“子类必须自己实现”。
        """
        raise NotImplementedError("BaseProvider.chat() must be implemented by subclasses.")
