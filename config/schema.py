"""
config/schema.py

这是项目第 2 步正式引入的配置对象定义文件。

在第 4 步以后，它开始承担更真实的职责：
配置不只是“摆在那里”，而是会真正影响 provider 的初始化。

也就是说，配置里的 provider.name / provider.model，
现在已经开始参与程序运行链路了。
"""

from pydantic import BaseModel, Field


class ProviderSettings(BaseModel):
    """
    ProviderSettings 表示“模型提供商相关配置”。

    你可以把它理解成：
    “我要连哪一种 provider，以及默认用哪个模型标识”。

    第 4 步里，我们先只支持 mock provider，
    因为当前目标是理解架构边界，而不是立刻接真实 API。
    """

    name: str = Field(
        default="mock",
        description="当前默认 provider 名称。第 4 步先使用 mock。",
    )

    model: str = Field(
        default="mock-echo-v1",
        description="provider 默认模型标识。对于 mock provider，这只是一个演示用名字。",
    )


class AgentSettings(BaseModel):
    """
    AgentSettings 表示“agent 本身的默认运行配置”。
    """

    name: str = Field(
        default="myagent",
        description="agent 的默认名字。后续可用于日志、提示词、状态输出。",
    )

    workspace: str = Field(
        default="./workspace",
        description="agent 默认工作目录。后面会在这里存放 memory、session、skills 等数据。",
    )

    system_prompt: str = Field(
        default="You are a helpful assistant.",
        description="最基础的默认系统提示词。后续会被更复杂的 ContextBuilder 替代或拼接。",
    )


class Config(BaseModel):
    """
    Config 是整个项目的总配置对象。

    当前仍然保持最小结构：
        Config
        ├── agent
        └── provider

    这样后面扩展 tools / memory / channels / subagents 时，
    还能继续保持结构清晰。
    """

    agent: AgentSettings = Field(
        default_factory=AgentSettings,
        description="agent 相关配置集合。",
    )

    provider: ProviderSettings = Field(
        default_factory=ProviderSettings,
        description="provider 相关配置集合。",
    )


DEFAULT_CONFIG = Config()
