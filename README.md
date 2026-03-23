# myagent · Step 9

这是从 0 开始复刻 `nanobot + DeerFlow` 混血版 agent runtime 的第 9 步。

## 这一步在做什么

第 9 步的目标是：

- 把 `history` 从临时消息列表
- 升级为正式的 `Session.messages`

也就是说，系统开始有了“会话容器”。

第 8 步解决的是：runtime 能处理最小上下文。
第 9 步解决的是：这段上下文开始有正式宿主。

## 当前启动流程

```text
CLI 参数
  ↓
myagent chat "hello"
  ↓
main.py
  ↓
创建 Session(id="local-dev-session")
  ↓
session.add_message(Message(role="user", content=...))
  ↓
AgentLoop.run_once(session)
  ↓
_build_prompt_from_history(session.messages)
  ↓
provider.chat(prompt)
  ↓
生成 assistant Message
  ↓
session.add_message(assistant_message)
```

## 你会学到什么

1. 为什么 history 需要正式容器
2. 为什么 Session 比裸 `list[Message]` 更适合作为 runtime 输入
3. 为什么追加消息是 Session 的第一核心能力
4. 为什么现在先做 Session，而不是直接上 SessionManager / 持久化

## 运行方式

```bash
cd /Users/dale/.openclaw/workspace-taizi/deliverables/myagent_step1
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
myagent chat "hello from step9"
```

## 预期输出

```text
myagent booted
loaded config from = config/default.json
agent.name = myagent
agent.workspace = ./workspace
provider.name = mock
provider.model = mock-echo-v1
session.id = local-dev-session
session.message_count = 2
session.first.role = user
session.first.content = hello from step9
assistant.message.role = assistant
assistant.message.content = [mock-provider:mock-echo-v1] you said: user: hello from step9
session.latest.role = assistant
session.latest.content = [mock-provider:mock-echo-v1] you said: user: hello from step9
```
