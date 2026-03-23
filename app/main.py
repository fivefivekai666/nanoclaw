"""
app/main.py

这是项目当前的命令行入口。

到了第 9 步，程序不再把 history 作为一个临时列表直接传给 AgentLoop，
而是先创建一个最小 Session 对象，
再把用户消息追加进去。

这表示系统开始拥有正式的“会话容器”。
"""

from __future__ import annotations

import typer

from config.loader import DEFAULT_CONFIG_PATH, load_config
from providers import make_provider
from runtime import AgentLoop, Message, Session

app = typer.Typer(help="A tiny agent runtime CLI.")


@app.callback()
def main_callback() -> None:
    """顶层 CLI 回调，用来稳定保留子命令结构。"""
    return None


@app.command()
def chat(message: str) -> None:
    """
    从 CLI 接收一段用户输入，并执行一轮最小 agent 处理。

    到了第 9 步，这段输入会被追加进 Session，
    然后 Session 会整体交给 AgentLoop。

    使用示例：
        myagent chat "hello"
    """
    config = load_config(DEFAULT_CONFIG_PATH)
    provider = make_provider(config)
    loop = AgentLoop(provider=provider)

    session = Session(id="local-dev-session")
    session.add_message(Message(role="user", content=message))

    assistant_message = loop.run_once(session)
    latest_message = session.latest_message()

    print("myagent booted")
    print(f"loaded config from = {DEFAULT_CONFIG_PATH}")
    print(f"agent.name = {config.agent.name}")
    print(f"agent.workspace = {config.agent.workspace}")
    print(f"provider.name = {config.provider.name}")
    print(f"provider.model = {config.provider.model}")
    print(f"session.id = {session.id}")
    print(f"session.message_count = {len(session.messages)}")
    print(f"session.first.role = {session.messages[0].role}")
    print(f"session.first.content = {session.messages[0].content}")
    print(f"assistant.message.role = {assistant_message.role}")
    print(f"assistant.message.content = {assistant_message.content}")
    if latest_message is not None:
        print(f"session.latest.role = {latest_message.role}")
        print(f"session.latest.content = {latest_message.content}")


def main() -> None:
    """脚本入口：把控制权交给 Typer 应用。"""
    app()


if __name__ == "__main__":
    main()
