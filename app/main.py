"""
app/main.py

这是项目当前的命令行入口。

到了第 4 步，程序已经具备三件事：
1. 能启动
2. 能加载配置
3. 能根据配置初始化一个 provider

虽然这个 provider 目前还是 MockProvider，
但这已经足够让我们第一次跑通：

    配置 → provider → 模拟模型响应

这意味着项目正式拥有了“模型调用边界”的雏形。
"""

from config.loader import DEFAULT_CONFIG_PATH, load_config
from providers import make_provider


def main() -> None:
    """
    项目的命令行入口函数。

    这一步不再只是打印配置，
    而是会真正创建 provider，并发起一次最小的 chat 调用。
    """
    config = load_config(DEFAULT_CONFIG_PATH)
    provider = make_provider(config)

    test_prompt = "hello from step4"
    response = provider.chat(test_prompt)

    print("myagent booted")
    print(f"loaded config from = {DEFAULT_CONFIG_PATH}")
    print(f"agent.name = {config.agent.name}")
    print(f"agent.workspace = {config.agent.workspace}")
    print(f"provider.name = {config.provider.name}")
    print(f"provider.model = {config.provider.model}")
    print(f"test_prompt = {test_prompt}")
    print(f"provider.response = {response}")
