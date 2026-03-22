"""
config/loader.py

这是项目第 3 步新增的文件：配置加载器（loader）。

如果说：
- schema.py 负责定义“配置长什么样”
- 那 loader.py 负责定义“配置从哪里来”

在真实的 agent runtime 里，程序启动时通常不会直接把所有配置写死在代码里，
而是会先：
1. 找到配置文件
2. 读取原始数据
3. 把原始数据转换成 Config 对象
4. 把这个 Config 交给后面的 runtime 使用

所以 loader.py 的角色可以理解成：

    “配置世界”和“程序世界”之间的桥梁

这一步我们故意只做最小版本：
- 只支持 JSON
- 不支持 YAML
- 不支持环境变量覆盖
- 不支持多层优先级

因为我们当前的目标不是把配置系统一次做大，
而是先让项目拥有“从文件加载配置”的能力。
"""

from __future__ import annotations

import json
from pathlib import Path

from config.schema import Config


# 这是项目默认配置文件的位置。
#
# 为什么先把它写成常量？
# 因为这样 main.py 后面只需要说：
#   load_config(DEFAULT_CONFIG_PATH)
#
# 读代码的人也会非常容易知道：
# “项目默认会去哪里找配置文件”。
DEFAULT_CONFIG_PATH = Path("config/default.json")


def load_config(path: str | Path = DEFAULT_CONFIG_PATH) -> Config:
    """
    从 JSON 文件加载配置，并返回一个 Config 对象。

    参数：
    - path: 配置文件路径

    返回：
    - Config 类型的配置对象

    这个函数现在只做 4 件事：
    1. 把传入路径转成 Path 对象
    2. 读取 JSON 文本
    3. 解析成 Python 字典
    4. 用 Config(**data) 构造配置对象

    注意：
    这里我们暂时不做太多“高级容错”，例如：
    - 文件不存在时自动回退多个路径
    - schema 版本迁移
    - 环境变量覆盖
    - 用户级 / 项目级 / 运行时级合并

    这些能力会在后面的步骤里慢慢长出来。
    当前只做一件关键小事：

        让程序真正开始“从文件读配置”。
    """
    config_path = Path(path)

    # read_text() 会把整个文件作为字符串读进来。
    # encoding="utf-8" 是一个好习惯，能避免不同系统上的编码歧义。
    raw_text = config_path.read_text(encoding="utf-8")

    # json.loads(...) 把 JSON 字符串解析成 Python 字典。
    data = json.loads(raw_text)

    # Config(**data) 会把字典里的内容映射到 Pydantic 模型里。
    #
    # 例如：
    # {
    #   "agent": {...},
    #   "provider": {...}
    # }
    #
    # 会自动变成：
    # Config(
    #   agent=AgentSettings(...),
    #   provider=ProviderSettings(...),
    # )
    return Config(**data)
