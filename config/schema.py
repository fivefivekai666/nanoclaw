"""
config/schema.py

这个文件以后会放项目的配置模型（Config Schema）。

为什么要单独做 schema？
因为 agent 项目后面会有很多配置，例如：
- 默认模型
- provider 名称
- workspace 路径
- 是否允许 exec
- 是否启用 subagent
- channel token
- MCP 配置

如果没有 schema，配置会越来越乱。
如果有了 schema：
- 类型更清楚
- 默认值更清楚
- 配置校验更容易
- IDE 自动补全更好

第 1 步先不写正式的 Pydantic 模型，
先放一个最小占位类。
"""


class Config:
    """
    这是未来全局配置对象的占位版本。

    后面我们会把它升级成 Pydantic 模型，
    并支持从 JSON / YAML / env 中加载。
    """

    def __init__(self) -> None:
        # 这里先不放任何字段。
        # 第 2 步我们再正式定义：
        # - model
        # - provider
        # - workspace
        pass
