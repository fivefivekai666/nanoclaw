# myagent · Step 5

这是从 0 开始复刻 `nanobot + DeerFlow` 混血版 agent runtime 的第 5 步。

## 这一步在做什么

第 5 步开始引入一个真正像“agent runtime 核心”的对象：

- `AgentLoop`

它的职责是：

- 接收输入
- 调用 provider
- 返回输出

注意，这里的 `AgentLoop` 还是最小版本，
目前只负责“单轮执行”，还没有 tools / memory / session / subagents。

## 当前启动流程

```text
main.py
  ↓
load_config()
  ↓
Config
  ↓
make_provider(config)
  ↓
AgentLoop(provider)
  ↓
loop.run_once("hello from step5")
  ↓
provider.chat(...)
```

## 你会学到什么

1. 为什么 agent 需要一个主流程控制器
2. AgentLoop 和 Provider 的职责分工
3. 为什么 main.py 不应该继续直接承担业务逻辑
4. 如何先跑通最小单轮执行链路

## 运行方式

```bash
cd /Users/dale/.openclaw/workspace-taizi/deliverables/myagent_step1
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
myagent
```

## 预期输出

```text
myagent booted
loaded config from = config/default.json
agent.name = myagent
agent.workspace = ./workspace
provider.name = mock
provider.model = mock-echo-v1
test_input = hello from step5
loop.response = [mock-provider:mock-echo-v1] you said: hello from step5
```
