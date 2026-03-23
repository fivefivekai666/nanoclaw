"""
app/main.py

这是项目当前的命令行入口。

到了第 10 步，系统第一次拥有最小会话持久化能力：
- 启动时尝试 load 旧 session
- 若不存在则创建新 session
- 执行一轮 agent 处理后再 save 回磁盘

这意味着 session 不再只活在内存里，
而是可以真正“落盘并恢复”。
"""

from __future__ import annotations

from pathlib import Path

import typer

from config.loader import DEFAULT_CONFIG_PATH, load_config
from providers import make_provider
from runtime import AgentLoop, Message, Session, load_session, save_session

app = typer.Typer(help="A tiny agent runtime CLI.")

SESSION_ID = "local-dev-session"
SESSION_DIR = Path("workspace/sessions")


@app.callback()
def main_callback() -> None:
    """顶层 CLI 回调，用来稳定保留子命令结构。"""
    return None


@app.command()
def chat(message: str) -> None:
    """
    从 CLI 接收一段用户输入，并执行一轮最小 agent 处理。

    到了第 10 步，这段流程会先尝试恢复旧 session，
    然后在处理完成后把更新后的 session 保存回磁盘。

    使用示例：
        myagent chat "hello"
    """
    config = load_config(DEFAULT_CONFIG_PATH)
    provider = make_provider(config)
    loop = AgentLoop(provider=provider)

    session = load_session(SESSION_ID, SESSION_DIR)
    loaded_from_disk = session is not None
    if session is None:
        session = Session(id=SESSION_ID)

    previous_message_count = len(session.messages)
    session.add_message(Message(role="user", content=message))

    assistant_message = loop.run_once(session)
    saved_path = save_session(session, SESSION_DIR)
    latest_message = session.latest_message()

    print("myagent booted")
    print(f"loaded config from = {DEFAULT_CONFIG_PATH}")
    print(f"agent.name = {config.agent.name}")
    print(f"agent.workspace = {config.agent.workspace}")
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
