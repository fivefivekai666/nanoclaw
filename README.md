# myagent · Step 15

这是从 0 开始复刻 `nanobot + DeerFlow` 混血版 agent runtime 的第 15 步。

## 这一步在做什么

第 15 步的目标是：

- 把 agent 的 identity / persona 正式接入 `ContextBuilder`
- 让 provider 输入不再只是“规则 + 历史”
- 而是升级为“规则 + 身份/风格 + 历史”

当前通过 config 注入三项最小信息：

- `identity_name`
- `identity_role`
- `persona_style`

## 当前结构

```text
system_prompt
identity_name
identity_role
persona_style
  ↓
ContextBuilder
  ↓
prompt
  ↓
AgentLoop
  ↓
provider.chat(prompt)
```

## 你会学到什么

1. 为什么 `system_prompt` 和 `identity/persona` 应该分层理解
2. 为什么 agent 不只是运行规则，还需要身份描述
3. 为什么 ContextBuilder 是承接 agent 自我描述的自然入口
4. 为什么第 15 步先走 config 注入，比直接读 `IDENTITY.md` 更稳

## 运行方式

```bash
cd /Users/dale/.openclaw/workspace-taizi/deliverables/myagent_step1
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
myagent chat "hello from step15" --session-id step15
```

## 预期现象

- 输出里会显示：
  - `agent.identity_name`
  - `agent.identity_role`
  - `agent.persona_style`
- mock provider 的回显内容里会包含：
  - `identity:`
  - `- name: myagent`
  - `- role: teaching-oriented agent runtime`
  - `- style: clear, calm, structured`
- 这说明 identity / persona 已真实进入 provider 输入链路
