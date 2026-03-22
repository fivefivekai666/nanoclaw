"""
config/schema.py

这是项目第 2 步要正式开始写的内容：配置对象（Config）。

为什么我们现在先写 Config，而不是直接去写 AgentLoop？
原因很简单：

1. AgentLoop 以后一定会依赖配置
   比如：
   - 用哪个 provider
   - 默认模型是什么
   - workspace 在哪里
   - 是否允许执行 shell

2. 如果没有统一配置对象，后面代码会越来越乱
   你会很容易在不同文件里看到很多“写死”的字符串，例如：
   - model = "gpt-4"
   - workspace = "./workspace"
   - provider = "openai"

3. 有了 Config 之后，后面的模块都能围绕它展开
   比如：
   - main.py 先加载 Config
   - provider 根据 Config 初始化
   - AgentLoop 根据 Config 决定运行方式

所以可以把 Config 理解成：

    “整个 runtime 的总开关面板”

这一步我们故意只做一个“最小但真实可用”的配置结构，
先不追求大而全。
"""

from pydantic import BaseModel, Field


class ProviderSettings(BaseModel):
    """
    ProviderSettings 表示“模型提供商相关配置”。

    你可以把它理解成：
    “我要连哪一家模型服务，以及默认用哪个模型”。

    当前我们只放两个最关键的字段：

    1. name
       - provider 名称
       - 例如：openai / anthropic / litellm / custom

    2. model
       - 默认模型名
       - 例如：gpt-4.1 / gpt-4o / claude-3-7-sonnet

    为什么现在先只放这两个？
    因为这是后面几乎所有 agent 项目最先会用到的最小信息。
    """

    name: str = Field(
        default="openai",
        description="当前默认使用的模型提供商名称，例如 openai / anthropic / litellm。",
    )

    model: str = Field(
        default="gpt-4.1-mini",
        description="当前默认模型名称。后续真正接 provider 时，会用到这个字段。",
    )


class AgentSettings(BaseModel):
    """
    AgentSettings 表示“agent 本身的默认运行配置”。

    这里先放 3 个特别重要、而且足够容易理解的字段：

    1. name
       - 你的 agent 叫什么名字
       - 这在后面生成 system prompt、日志、状态输出时都很常见

    2. workspace
       - agent 的工作目录
       - 后面放 AGENTS.md / SOUL.md / USER.md / TOOLS.md
       - 也会放 sessions / memory / outputs 等文件

    3. system_prompt
       - 先给一个最基础的默认系统提示词
       - 虽然现在还没真正接模型，但我们先把这个配置位留出来

    为什么 system_prompt 现在就先放？
    因为以后你会很快发现：
    agent runtime 里，system prompt 几乎一定会成为配置的一部分。
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
    Config 是整个项目的“总配置对象”。

    你可以把它理解成一个大的树状结构：

        Config
        ├── agent
        └── provider

    也就是说，Config 不是把所有字段都平铺在最外层，
    而是分模块组织。

    这样做的好处是：
    - 结构清晰
    - 以后扩展容易
    - 读代码时一眼能看出哪些配置属于 agent，哪些属于 provider

    后续我们还会继续往 Config 里加：
    - tools
    - channels
    - memory
    - subagents
    - sandbox
    - mcp

    但第 2 步先到这里就够了。
    """

    agent: AgentSettings = Field(
        default_factory=AgentSettings,
        description="agent 相关配置集合。",
    )

    provider: ProviderSettings = Field(
        default_factory=ProviderSettings,
        description="provider 相关配置集合。",
    )


# 这里创建一个“默认配置实例”。
#
# 为什么要放这个？
# 因为在项目早期开发时，我们经常需要：
# - 快速拿一个默认配置来跑程序
# - 不想每次都手动 new 很多对象
#
# 所以后面 main.py 可以直接先这样用：
#   config = DEFAULT_CONFIG
#
# 等再往后发展，我们再把它升级成：
# - 从 JSON 文件加载
# - 从 YAML 加载
# - 从环境变量覆盖
DEFAULT_CONFIG = Config()
