"""
app/main.py

这是项目当前的命令行入口。

到了第 8 步，程序不再只把“单条用户消息”交给 AgentLoop，
而是开始构造一个最小 history（消息列表）作为上下文输入。

这意味着系统第一次从“处理一条消息”
过渡到“处理一段最小对话上下文”。
"""

from __future__ import annotations

import typer

from config.loader import DEFAULT_CONFIG_PATH, load_config
from providers import make_provider
from runtime import AgentLoop, Message

app = typer.Typer(help="A tiny agent runtime CLI.")


@app.callback()
def main_callback() -> None:
    """顶层 CLI 回调，用来稳定保留子命令结构。"""
    return None


@app.command()
def chat(message: str) -> None:
    """
    从 CLI 接收一段用户输入，并执行一轮最小 agent 处理。

    到了第 8 步，这段输入会先被包装进最小 history，
    然后再交给 AgentLoop。

    使用示例：
        myagent chat "hello"
    """
    config = load_config(DEFAULT_CONFIG_PATH)
    provider = make_provider(config)
    loop = AgentLoop(provider=provider)

    history = [Message(role="user", content=message)]
    assistant_message = loop.run_once(history)

    print("myagent booted")
    print(f"loaded config from = {DEFAULT_CONFIG_PATH}")
    print(f"agent.name = {config.agent.name}")
    print(f"agent.workspace = {config.agent.workspace}")
    print(f"provider.name = {config.provider.name}")
    print(f"provider.model = {config.provider.model}")
    print(f"history.length = {len(history)}")
    print(f"history.last.role = {history[-1].role}")
    print(f"history.last.content = {history[-1].content}")
    print(f"assistant.message.role = {assistant_message.role}")
    print(f"assistant.message.content = {assistant_message.content}")


def main() -> None:
    """脚本入口：把控制权交给 Typer 应用。"""
    app()


if __name__ == "__main__":
    main()
