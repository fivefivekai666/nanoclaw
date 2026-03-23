# myagent · Step 14

这是从 0 开始复刻 `nanobot + DeerFlow` 混血版 agent runtime 的第 14 步。

## 这一步在做什么

第 14 步的目标是：

- 抽出最小 `ContextBuilder`
- 把 prompt 构造逻辑从 `AgentLoop` 中拆出来
- 让 runtime 开始形成更清晰的职责分层

当前不新增业务能力，只做结构整理：

- `AgentLoop` 负责流程推进
- `ContextBuilder` 负责构造 provider 输入

## 当前结构

```text
config.agent.system_prompt
  ↓
ContextBuilder
  ↓
build(session) -> prompt
  ↓
AgentLoop
  ↓
provider.chat(prompt)
```

## 你会学到什么

1. 为什么 prompt 构造不应该一直塞在 loop 里
2. 为什么 ContextBuilder 是后续 memory / tools / identity 的自然挂载点
3. 为什么“功能没变，但结构更清晰”本身就是一次重要升级
4. 如何做最小职责拆分而不引入过度设计

## 运行方式

```bash
cd /Users/dale/.openclaw/workspace-taizi/deliverables/myagent_step1
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
myagent chat "hello from step14" --session-id step14
```

## 预期现象

- 功能行为与第 13 步基本一致
- mock provider 的回显仍然会包含：
  - `system: You are a helpful assistant.`
  - `user: hello from step14`
- 但代码结构已经从“loop 内部拼 prompt”升级为“ContextBuilder 专职构造 prompt”
