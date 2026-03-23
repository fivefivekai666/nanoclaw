"""
config/schema.py

这是项目的配置对象定义文件。

到了第 32 步，agent 配置除了 retry policy 外，
再加入一个最小 execution policy / fallback provider 配置入口：
- provider.fallback.enabled
- provider.fallback.name
- provider.fallback.model
- provider.fallback.on_recoverable_only

这样做的意义是：
- 让“主 provider 失败后是否切到 fallback provider”第一次成为正式可配置能力
- 让 runtime 不只是有重试策略，还开始具备最小 provider 执行路由策略
- 为未来扩展 provider 链 / capability routing / fallback trees 做准备
"""

from pydantic import BaseModel, Field


class FallbackProviderSettings(BaseModel):
    """fallback provider 相关配置。"""

    enabled: bool = Field(
        default=True,
        description="是否启用 fallback provider。",
    )

    name: str = Field(
        default="mock",
        description="fallback provider 名称。",
    )

    model: str = Field(
        default="mock-fallback-v1",
        description="fallback provider 模型标识。",
    )

    on_recoverable_only: bool = Field(
        default=True,
        description="是否仅在 recoverable 错误时才允许切到 fallback provider。",
    )


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

    fallback: FallbackProviderSettings = Field(
        default_factory=FallbackProviderSettings,
        description="fallback provider 相关配置。",
    )


class RetrySettings(BaseModel):
    """最小 runtime retry policy 配置。"""

    max_attempts: int = Field(
        default=2,
        description="一次 loop 最多允许尝试多少次当前 provider 调用。",
    )

    retry_on_recoverable_only: bool = Field(
        default=True,
        description="是否仅对 recoverable 错误允许重试。",
    )


class AgentSettings(BaseModel):
    """Agent 本身的默认运行配置。"""

    name: str = Field(default="myagent", description="agent 的默认名字。")
    workspace: str = Field(default="./workspace", description="agent 默认工作目录。后面可存放 memory、session、skills 等数据。")
    system_prompt: str = Field(default="You are a helpful assistant.", description="最基础的默认系统提示词。")
    identity_name: str = Field(default="myagent", description="agent 的身份名称。")
    identity_role: str = Field(default="teaching-oriented agent runtime", description="agent 的角色定位描述。")
    persona_style: str = Field(default="clear, calm, structured", description="agent 的表达风格描述。")
    response_style: str = Field(default="normal", description="response policy 风格。当前支持：normal / concise。")
    default_session_id: str = Field(default="local-dev-session", description="默认使用的会话 ID；可被 CLI 参数覆盖。")
    session_dir: str = Field(default="workspace/sessions", description="会话文件默认目录。")
    retry: RetrySettings = Field(default_factory=RetrySettings, description="最小 runtime retry policy 配置。")


class Config(BaseModel):
    """Config 是整个项目的总配置对象。"""

    agent: AgentSettings = Field(default_factory=AgentSettings, description="agent 相关配置集合。")
    provider: ProviderSettings = Field(default_factory=ProviderSettings, description="provider 相关配置集合。")


DEFAULT_CONFIG = Config()
