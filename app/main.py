"""
app/main.py

这是项目当前的命令行入口。

这一版的重要变化是：
- session id 不再写死在代码常量里
- 默认值来自配置文件
- CLI 可以用 --session-id 显式覆盖默认值

这意味着同一个程序现在可以自然管理多个会话，
而不是永远只绑死在 local-dev-session 上。
"""

from __future__ import annotations

from pathlib import Path

import typer

from config.loader import DEFAULT_CONFIG_PATH, load_config
from providers import make_provider
from runtime import AgentLoop, Message, Session, load_session, save_session

app = typer.Typer(help="A tiny agent runtime CLI.")


@app.callback()
def main_callback() -> None:
    """顶层 CLI 回调，用来稳定保留子命令结构。"""
    return None


@app.command()
def chat(
    message: str,
    session_id: str | None = typer.Option(
        default=None,
        help="要使用的 session id；若不传，则使用配置文件中的默认值。",
    ),
) -> None:
    """
    从 CLI 接收一段用户输入，并执行一轮最小 agent 处理。

    当前行为：
    1. 读取配置
    2. 决定实际 session_id（CLI 覆盖 config 默认值）
    3. 尝试加载该 session
    4. 若不存在则创建新 session
    5. 运行一轮 agent 并保存回磁盘

    使用示例：
        myagent chat "hello"
        myagent chat "hello" --session-id demo-a
    """
    config = load_config(DEFAULT_CONFIG_PATH)
    provider = make_provider(config)
    loop = AgentLoop(provider=provider)

    effective_session_id = session_id or config.agent.default_session_id
    session_dir = Path(config.agent.session_dir)

    session = load_session(effective_session_id, session_dir)
    loaded_from_disk = session is not None
    if session is None:
        session = Session(id=effective_session_id)

    previous_message_count = len(session.messages)
    session.add_message(Message(role="user", content=message))

    assistant_message = loop.run_once(session)
    saved_path = save_session(session, session_dir)
    latest_message = session.latest_message()

    print("myagent booted")
    print(f"loaded config from = {DEFAULT_CONFIG_PATH}")
    print(f"agent.name = {config.agent.name}")
    print(f"agent.workspace = {config.agent.workspace}")
    print(f"agent.default_session_id = {config.agent.default_session_id}")
    print(f"agent.session_dir = {config.agent.session_dir}")
    print(f"provider.name = {config.provider.name}")
    print(f"provider.model = {config.provider.model}")
    print(f"session.id = {session.id}")
    print(f"session.loaded_from_disk = {loaded_from_disk}")
    print(f"session.previous_message_count = {previous_message_count}")
    print(f"session.message_count = {len(session.messages)}")
    print(f"session.saved_path = {saved_path}")
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
