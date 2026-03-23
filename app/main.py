"""
app/main.py

这是项目当前的命令行入口。

到了第 16 步，chat 主流程在创建 ContextBuilder 前，
会先从 workspace 目录读取最小 persona 文件：
- IDENTITY.md
- SOUL.md

这意味着 runtime 上下文不再只来自 config，
也开始从真实工作目录里的 agent 文件读取自我描述。
"""

from __future__ import annotations

from pathlib import Path

import typer

from config.loader import DEFAULT_CONFIG_PATH, load_config
from providers import make_provider
from runtime import (
    AgentLoop,
    ContextBuilder,
    Message,
    Session,
    list_sessions,
    load_session,
    load_workspace_context,
    save_session,
)

app = typer.Typer(help="A tiny agent runtime CLI.")
sessions_app = typer.Typer(help="Manage saved sessions.")
app.add_typer(sessions_app, name="sessions")


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
    """
    config = load_config(DEFAULT_CONFIG_PATH)
    provider = make_provider(config)
    workspace_context = load_workspace_context(config.agent.workspace)
    context_builder = ContextBuilder(
        system_prompt=config.agent.system_prompt,
        identity_name=config.agent.identity_name,
        identity_role=config.agent.identity_role,
        persona_style=config.agent.persona_style,
        workspace_context=workspace_context,
    )
    loop = AgentLoop(provider=provider, context_builder=context_builder)

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
    print(f"agent.system_prompt = {config.agent.system_prompt}")
    print(f"agent.identity_name = {config.agent.identity_name}")
    print(f"agent.identity_role = {config.agent.identity_role}")
    print(f"agent.persona_style = {config.agent.persona_style}")
    print(f"workspace.identity.loaded = {bool(workspace_context.identity_text)}")
    print(f"workspace.soul.loaded = {bool(workspace_context.soul_text)}")
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


@sessions_app.command("list")
def sessions_list_command() -> None:
    """列出当前所有已保存的 session。"""
    config = load_config(DEFAULT_CONFIG_PATH)
    session_dir = Path(config.agent.session_dir)
    sessions = list_sessions(session_dir)

    print(f"session.dir = {session_dir}")
    print(f"session.count = {len(sessions)}")

    for session in sessions:
        latest_message = session.latest_message()
        last_role = latest_message.role if latest_message is not None else "none"
        last_preview = latest_message.content if latest_message is not None else ""
        last_preview = last_preview.replace("\n", " ")[:80]
        print(
            f"- id={session.id} messages={len(session.messages)} "
            f"last_role={last_role} last_preview={last_preview}"
        )


@sessions_app.command("inspect")
def sessions_inspect_command(session_id: str) -> None:
    """查看某个指定 session 的详细内容。"""
    config = load_config(DEFAULT_CONFIG_PATH)
    session_dir = Path(config.agent.session_dir)
    session = load_session(session_id, session_dir)

    if session is None:
        print(f"session.not_found = {session_id}")
        raise typer.Exit(code=1)

    print(f"session.id = {session.id}")
    print(f"session.message_count = {len(session.messages)}")
    for index, message in enumerate(session.messages, start=1):
        print(f"{index}. {message.role}: {message.content}")


def main() -> None:
    """脚本入口：把控制权交给 Typer 应用。"""
    app()


if __name__ == "__main__":
    main()
