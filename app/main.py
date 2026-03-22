"""
app/main.py

这是项目当前的命令行入口。

到了第 3 步，我们不再直接依赖代码里写死的 DEFAULT_CONFIG，
而是正式引入“配置加载”这件事。

也就是说，程序启动时会这样工作：

1. main.py 调用 load_config()
2. load_config() 去读取 config/default.json
3. loader.py 把 JSON 数据变成 Config 对象
4. main.py 再使用这个 Config

这意味着项目从这一刻开始，已经不只是“有一个配置类”，
而是拥有了“启动时读取配置”的能力。

这虽然还是很小的一步，但已经非常接近真实软件的启动流程了。
"""

from config.loader import DEFAULT_CONFIG_PATH, load_config


def main() -> None:
    """
    项目的命令行入口函数。

    这一步的重点不在“打印内容本身”，而在于：
    我们现在已经不是直接使用写死在 Python 代码里的默认对象了，
    而是先从配置文件加载，再继续运行。

    这正是很多 runtime / server / agent 程序的典型启动方式。
    """
    config = load_config(DEFAULT_CONFIG_PATH)

    print("myagent booted")
    print(f"loaded config from = {DEFAULT_CONFIG_PATH}")
    print(f"agent.name = {config.agent.name}")
    print(f"agent.workspace = {config.agent.workspace}")
    print(f"provider.name = {config.provider.name}")
    print(f"provider.model = {config.provider.model}")
