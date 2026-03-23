# myagent · Step 7

这是从 0 开始复刻 `nanobot + DeerFlow` 混血版 agent runtime 的第 7 步。

## 这一步在做什么

第 7 步的目标是：

- 把 runtime 的输入输出单位
- 从“裸字符串”升级成“结构化 Message 对象”

这是一个很重要的架构转折。
因为以后 session、memory、tools、subagents 都不会喜欢只处理纯字符串，
它们更适合围绕统一的数据模型来扩展。

## 当前启动流程

```text
CLI 参数
  ↓
myagent chat "hello"
  ↓
main.py
  ↓
Message(role="user", content=...)
  ↓
AgentLoop.run_once(message)
  ↓
provider.chat(message.content)
  ↓
Message(role="assistant", content=...)
```

## 你会学到什么

1. 为什么 agent runtime 不能长期依赖裸字符串
2. 为什么要先定义最小 Message Model
3. 为什么 `role + content` 是第一批核心字段
4. 数据模型统一后，后续模块会更容易衔接

## 运行方式

```bash
cd /Users/dale/.openclaw/workspace-taizi/deliverables/myagent_step1
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
myagent chat "hello from step7"
```

## 预期输出

```text
myagent booted
loaded config from = config/default.json
agent.name = myagent
agent.workspace = ./workspace
provider.name = mock
provider.model = mock-echo-v1
user.message.role = user
user.message.content = hello from step7
assistant.message.role = assistant
assistant.message.content = [mock-provider:mock-echo-v1] you said: hello from step7
```
