"""
app/main.py

这是项目当前的命令行入口。

到了第 6 步，程序第一次拥有了“真实外部输入入口”：
用户可以直接从命令行把一句话传给 agent，而不需要再改源码里的写死字符串。

这一步虽然看起来只是 CLI 小改动，但架构意义很大：
- 第 5 步之前，输入来自源码内部
- 第 6 步开始，输入来自程序外部

这意味着项目开始从“演示脚本”走向“可使用的命令行工具”。
"""

from __future__ import annotations

import typer

from config.loader import DEFAULT_CONFIG_PATH, load_config
from providers import make_provider
from runtime import AgentLoop

# 这里创建一个 Typer 应用对象。
#
# 第 6 步我们希望 CLI 结构明确长成：
#   myagent chat "hello"
#
# 所以后面会显式注册一个 `chat` 子命令，
# 而不是让用户继续依赖写死在代码里的测试输入。
app = typer.Typer(help="A tiny agent runtime CLI.")


@app.callback()
def main_callback() -> None:
    """
    顶层 CLI 回调。

    这里先不做具体业务，只是告诉 Typer：
    这是一个带子命令的应用，而不是“只有一个默认命令”的简化形式。

    这样我们就能稳定使用：
        myagent chat "hello"
    """
    return None


@app.command()
def chat(message: str) -> None:
    """
    接收一段命令行输入，交给 AgentLoop 执行一轮处理。

    这是第 6 步最关键的变化：
    输入不再写死在代码里，而是从 CLI 参数进入程序。

    使用示例：
        myagent chat "hello"
    """
    config = load_config(DEFAULT_CONFIG_PATH)
    provider = make_provider(config)
    loop = AgentLoop(provider=provider)

    response = loop.run_once(message)

    print("myagent booted")
    print(f"loaded config from = {DEFAULT_CONFIG_PATH}")
    print(f"agent.name = {config.agent.name}")
    print(f"agent.workspace = {config.agent.workspace}")
    print(f"provider.name = {config.provider.name}")
    print(f"provider.model = {config.provider.model}")
    print(f"user.message = {message}")
    print(f"loop.response = {response}")


def main() -> None:
    """
    项目的脚本入口。

    pyproject.toml 里的 `myagent = "app.main:main"` 会调用这里，
    然后这里再把控制权交给 Typer 应用。
    """
    app()


if __name__ == "__main__":
    main()
