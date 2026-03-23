"""
app/main.py

这是项目当前的命令行入口。

到了第 27 步，我们继续沿着 runtime 主线推进：
给 LoopResult 加上最小 status / stop_reason，
让 loop 不只是“有结果”，还开始“表达为什么结束”。

这样启动装配层现在包含：
- provider：模型调用边界
- memory provider：memory 来源与最小清洗边界
- response policy：回答规则边界
- context builder：稳定的 section-based prompt 装配边界
- loop result：一次运行的结构化结果边界
- loop status / stop reason：一次运行的最小结束语义
"""

from __future__ import annotations

from pathlib import Path

import typer

from config.loader import DEFAULT_CONFIG_PATH, load_config
from memory import FileMemoryProvider
from providers import make_provider
from runtime import (
    AgentLoop,
    ContextBuilder,
    LoopResult,
    LoopStatus,
    LoopStopReason,
    Message,
    ResponsePolicy,
    ResponseStyle,
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
    response_style: str | None = typer.Option(
        default=None,
        help="临时覆盖 response policy 风格；支持 normal / concise。未知值会 fallback 到 normal。",
    ),
) -> None:
    """
    从 CLI 接收一段用户输入，并执行一轮最小 agent 处理。
    """
    config = load_config(DEFAULT_CONFIG_PATH)
    provider = make_provider(config)
    workspace_context = load_workspace_context(config.agent.workspace)
    memory_provider = FileMemoryProvider(workspace_dir=config.agent.workspace)
    requested_response_style = response_style or config.agent.response_style
    normalized_requested_style = ResponsePolicy.normalize_style(requested_response_style)
    response_policy = ResponsePolicy(style=requested_response_style)
    context_builder = ContextBuilder(
        system_prompt=config.agent.system_prompt,
        identity_name=config.agent.identity_name,
        identity_role=config.agent.identity_role,
        persona_style=config.agent.persona_style,
        memory_provider=memory_provider,
        response_policy=response_policy,
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

    loop_result = loop.run_once(session)
    saved_path = save_session(session, session_dir)
    latest_message = session.latest_message()

    parsed_identity = workspace_context.identity
    structured_identity_loaded = any(
        [
            parsed_identity.name,
            parsed_identity.creature,
            parsed_identity.vibe,
            parsed_identity.emoji,
            parsed_identity.avatar,
            parsed_identity.extras,
        ]
    )

    print("myagent booted")
    print(f"loaded config from = {DEFAULT_CONFIG_PATH}")
    print(f"agent.name = {config.agent.name}")
    print(f"agent.workspace = {config.agent.workspace}")
    print(f"agent.system_prompt = {config.agent.system_prompt}")
    print(f"agent.identity_name = {config.agent.identity_name}")
    print(f"agent.identity_role = {config.agent.identity_role}")
    print(f"agent.persona_style = {config.agent.persona_style}")
    print(f"agent.response_style.default = {config.agent.response_style}")
    print(f"agent.response_style.requested = {requested_response_style}")
    print(f"agent.response_style.normalized = {normalized_requested_style.value}")
    print(f"agent.response_style.effective = {response_policy.style.value}")
    print(f"agent.response_style.type = {ResponseStyle.__name__}")
    print(f"agent.response_style.fallback_used = {response_policy.fallback_used}")
    print("prompt.mode = sectioned")
    print("prompt.sections = SYSTEM, IDENTITY, WORKSPACE, MEMORY, CONVERSATION, INSTRUCTION")
    print("response.policy = ResponsePolicy")
    print(f"workspace.identity.loaded = {bool(workspace_context.identity_text)}")
    print(f"workspace.identity.structured = {structured_identity_loaded}")
    print(f"workspace.identity.name = {parsed_identity.name}")
    print(f"workspace.identity.creature = {parsed_identity.creature}")
    print(f"workspace.identity.vibe = {parsed_identity.vibe}")
    print(f"workspace.identity.emoji = {parsed_identity.emoji}")
    print(f"workspace.soul.loaded = {bool(workspace_context.soul_text)}")
    print("memory.provider = FileMemoryProvider")
    print("memory.mode = structured-file")
    print(f"memory.path = {memory_provider.memory_path}")
    print(f"memory.exists = {memory_provider.memory_path.exists()}")
    print(f"agent.default_session_id = {config.agent.default_session_id}")
    print(f"agent.session_dir = {config.agent.session_dir}")
    print(f"provider.name = {config.provider.name}")
    print(f"provider.model = {config.provider.model}")
    print(f"loop.result.type = {LoopResult.__name__}")
    print(f"loop.result.session_id = {loop_result.session_id}")
    print(f"loop.result.prompt_length = {len(loop_result.prompt)}")
    print(f"loop.result.assistant_role = {loop_result.assistant_message.role}")
    print(f"loop.result.status = {loop_result.status.value}")
    print(f"loop.result.stop_reason = {loop_result.stop_reason.value}")
    print(f"loop.result.status_type = {LoopStatus.__name__}")
    print(f"loop.result.stop_reason_type = {LoopStopReason.__name__}")
    print(f"session.id = {session.id}")
    print(f"session.loaded_from_disk = {loaded_from_disk}")
    print(f"session.previous_message_count = {previous_message_count}")
    print(f"session.message_count = {len(session.messages)}")
    print(f"session.saved_path = {saved_path}")
    print(f"assistant.message.role = {loop_result.assistant_message.role}")
    print(f"assistant.message.content = {loop_result.assistant_message.content}")
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
