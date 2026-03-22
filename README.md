# myagent · Step 4

这是从 0 开始复刻 `nanobot + DeerFlow` 混血版 agent runtime 的第 4 步。

## 这一步在做什么

第 4 步开始给项目加入一个新的关键层：

- `provider`

Provider 的职责是：

- 让上层 runtime 用统一方式调用模型
- 把具体模型厂商差异隔离在底层

为了先学清楚结构，这一步我们不接真实 API，
而是先实现：

- `BaseProvider`：统一接口
- `MockProvider`：假的 provider 实现
- `make_provider(config)`：根据配置选择 provider

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
MockProvider
  ↓
provider.chat("hello from step4")
```

## 你会学到什么

1. 为什么 agent runtime 需要 provider 抽象层
2. BaseProvider 和具体 provider 的分工
3. 为什么先用 MockProvider 跑通链路
4. 如何根据配置初始化 provider

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
test_prompt = hello from step4
provider.response = [mock-provider:mock-echo-v1] you said: hello from step4
```
