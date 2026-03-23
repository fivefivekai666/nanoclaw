"""
config/schema.py

这是项目第 2 步正式引入的配置对象定义文件。

到了这一步，配置继续从“静态展示”向“真实运行参数”演进。
除了 provider 和 agent 的基础信息，我们现在还把默认 session 行为纳入配置：
- 默认 session_id
- session 文件目录

这样做的意义是：
- 不再把会话标识写死在 main.py
- 让“默认跑哪个会话”成为正式可配置项
- 同时保留 CLI 覆盖能力
"""

from pydantic import BaseModel, Field


class ProviderSettings(BaseModel):
    """Provider 相关配置。"""

    name: str = Field(
        default="mock",
        description="当前默认 provider 名称。",
    )

    model: str = Field(
        default="mock-echo-v1",
        description="provider 默认模型标识。",
    )


class AgentSettings(BaseModel):
    """Agent 本身的默认运行配置。"""

    name: str = Field(
        default="myagent",
        description="agent 的默认名字。",
    )

    workspace: str = Field(
        default="./workspace",
        description="agent 默认工作目录。后面可存放 memory、session、skills 等数据。",
    )

    system_prompt: str = Field(
        default="You are a helpful assistant.",
        description="最基础的默认系统提示词。",
    )

    default_session_id: str = Field(
        default="local-dev-session",
        description="默认使用的会话 ID；可被 CLI 参数覆盖。",
    )

    session_dir: str = Field(
        default="workspace/sessions",
        description="会话文件默认目录。",
    )


class Config(BaseModel):
    """
    Config 是整个项目的总配置对象。

    当前结构：
        Config
        ├── agent
        └── provider
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
