"""
config/schema.py

这是项目的配置对象定义文件。

到了第 15 步，agent 配置不再只包含“运行规则”和“会话参数”，
还开始正式包含一层最小 identity / persona 信息：
- identity_name
- identity_role
- persona_style

这样做的意义是：
- 让 agent 不只是“会运行的程序”
- 也开始拥有“它是谁、以什么风格说话”的正式配置入口
- 并且这些信息可以通过 ContextBuilder 注入到模型输入中
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
