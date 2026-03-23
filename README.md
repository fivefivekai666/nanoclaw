# myagent · Step 13

这是从 0 开始复刻 `nanobot + DeerFlow` 混血版 agent runtime 的第 13 步。

## 这一步在做什么

第 13 步的目标是：

- 把 `system_prompt` 正式接入 runtime
- 让 provider 的输入不再只是历史消息拼接
- 让 prompt 构造第一次拥有“系统级指令层”

重要边界：
- `session.messages` 仍然表示真实对话历史
- `system_prompt` 不写入 session 文件
- `system_prompt` 只在构造 prompt 时注入

## 当前结构

```text
config.agent.system_prompt
  ↓
AgentLoop(system_prompt=...)
  ↓
_build_prompt_from_history(...)
  ↓
system: ...
user: ...
assistant: ...
```

## 你会学到什么

1. 为什么 user history 和 system instruction 不是一回事
2. 为什么 system prompt 最好作为 runtime 注入层存在
3. 为什么这一步是 ContextBuilder 的前身
4. 为什么先不要把 system prompt 直接写进 session

## 运行方式

```bash
cd /Users/dale/.openclaw/workspace-taizi/deliverables/myagent_step1
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
myagent chat "hello from step13" --session-id step13
```

## 预期现象

- 输出里会显示 `agent.system_prompt`
- mock provider 的回显内容里会包含：
  - `system: You are a helpful assistant.`
  - `user: hello from step13`
- 这说明 system prompt 已真实进入 provider 输入链路
