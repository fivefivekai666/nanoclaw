# myagent · Step 8

这是从 0 开始复刻 `nanobot + DeerFlow` 混血版 agent runtime 的第 8 步。

## 这一步在做什么

第 8 步的目标是：

- 把 AgentLoop 的输入
- 从“单条 Message”升级成“消息列表 history”

这代表系统开始拥有最小的“短期上下文”能力。
虽然现在还没有 session manager，也没有长期 memory，
但 runtime 已经不再只能看当前这一句话了。

## 当前启动流程

```text
CLI 参数
  ↓
myagent chat "hello"
  ↓
main.py
  ↓
history = [Message(role="user", content=...)]
  ↓
AgentLoop.run_once(history)
  ↓
_build_prompt_from_history(history)
  ↓
provider.chat(prompt)
  ↓
Message(role="assistant", content=...)
```

## 你会学到什么

1. 为什么对话系统不能只处理单条消息
2. history 和 memory 的区别
3. 为什么先让 runtime 接收 history，再考虑重写 provider 接口
4. 如何把最小上下文拼接成 prompt

## 运行方式

```bash
cd /Users/dale/.openclaw/workspace-taizi/deliverables/myagent_step1
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
myagent chat "hello from step8"
```

## 预期输出

```text
myagent booted
loaded config from = config/default.json
agent.name = myagent
agent.workspace = ./workspace
provider.name = mock
provider.model = mock-echo-v1
history.length = 1
history.last.role = user
history.last.content = hello from step8
assistant.message.role = assistant
assistant.message.content = [mock-provider:mock-echo-v1] you said: user: hello from step8
```
