"""
config/schema.py

这是项目的配置对象定义文件。

到了第 31 步，agent 配置除了 identity / persona / session / response policy 等基础参数外，
再加入一个最小 runtime retry policy 配置入口：
- retry.max_attempts
- retry.retry_on_recoverable_only

这样做的意义是：
- 让“遇到失败后怎么执行恢复动作”第一次成为正式可配置能力
- 让 runtime 不只是能跑、能回答、能表达错误，还开始具备可配置执行策略层
- 为未来扩展 backoff / fallback / tool-specific policy 做准备
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


class RetrySettings(BaseModel):
    """最小 runtime retry policy 配置。"""

    max_attempts: int = Field(
        default=2,
        description="一次 loop 最多允许尝试多少次 provider 调用。",
    )

    retry_on_recoverable_only: bool = Field(
        default=True,
        description="是否仅对 recoverable 错误允许重试。",
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

    identity_name: str = Field(
        default="myagent",
        description="agent 的身份名称。",
    )

    identity_role: str = Field(
        default="teaching-oriented agent runtime",
        description="agent 的角色定位描述。",
    )

    persona_style: str = Field(
        default="clear, calm, structured",
        description="agent 的表达风格描述。",
    )

    response_style: str = Field(
        default="normal",
        description="response policy 风格。当前支持：normal / concise。",
    )

    default_session_id: str = Field(
        default="local-dev-session",
        description="默认使用的会话 ID；可被 CLI 参数覆盖。",
    )

    session_dir: str = Field(
        default="workspace/sessions",
        description="会话文件默认目录。",
    )

    retry: RetrySettings = Field(
        default_factory=RetrySettings,
        description="最小 runtime retry policy 配置。",
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
