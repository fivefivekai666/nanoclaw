"""
app/main.py

这是项目当前的命令行入口。

到了第 7 步，程序继续沿着“更像真正 agent runtime”的方向演进：
- 第 6 步：CLI 能接收真实输入
- 第 7 步：输入输出不再只是裸字符串，而是 Message 对象

所以现在 main.py 的工作变成：
1. 从 CLI 接收用户输入
2. 把输入包装成 user Message
3. 把 Message 交给 AgentLoop
4. 接收 assistant Message 并打印出来
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

    使用示例：
        myagent chat "hello"
    """
    config = load_config(DEFAULT_CONFIG_PATH)
    provider = make_provider(config)
    loop = AgentLoop(provider=provider)

    user_message = Message(role="user", content=message)
    assistant_message = loop.run_once(user_message)

    print("myagent booted")
    print(f"loaded config from = {DEFAULT_CONFIG_PATH}")
    print(f"agent.name = {config.agent.name}")
    print(f"agent.workspace = {config.agent.workspace}")
    print(f"provider.name = {config.provider.name}")
    print(f"provider.model = {config.provider.model}")
    print(f"user.message.role = {user_message.role}")
    print(f"user.message.content = {user_message.content}")
    print(f"assistant.message.role = {assistant_message.role}")
    print(f"assistant.message.content = {assistant_message.content}")


def main() -> None:
    """脚本入口：把控制权交给 Typer 应用。"""
    app()


if __name__ == "__main__":
    main()
