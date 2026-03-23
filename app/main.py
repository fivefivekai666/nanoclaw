"""
app/main.py

这是项目当前的命令行入口。

到了第 5 步，程序开始拥有一个真正像“agent runtime”的最小结构：

1. main.py 负责启动
2. config 负责加载配置
3. providers 负责创建模型适配层
4. runtime.AgentLoop 负责执行一轮 agent 流程

也就是说，main.py 不再直接调用 provider.chat(...)，
而是把这件事交给 AgentLoop。
这一步非常重要，因为它意味着“运行逻辑”开始从入口文件中抽离出来。
"""

from config.loader import DEFAULT_CONFIG_PATH, load_config
from providers import make_provider
from runtime import AgentLoop


def main() -> None:
    """
    项目的命令行入口函数。

    第 5 步的重点是：
    不再让 main.py 直接承担“业务执行逻辑”，
    而是只负责组装依赖并启动 AgentLoop。
    """
    config = load_config(DEFAULT_CONFIG_PATH)
    provider = make_provider(config)
    loop = AgentLoop(provider=provider)

    test_input = "hello from step5"
    response = loop.run_once(test_input)

    print("myagent booted")
    print(f"loaded config from = {DEFAULT_CONFIG_PATH}")
    print(f"agent.name = {config.agent.name}")
    print(f"agent.workspace = {config.agent.workspace}")
    print(f"provider.name = {config.provider.name}")
    print(f"provider.model = {config.provider.model}")
    print(f"test_input = {test_input}")
    print(f"loop.response = {response}")
