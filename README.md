# myagent · Step 6

这是从 0 开始复刻 `nanobot + DeerFlow` 混血版 agent runtime 的第 6 步。

## 这一步在做什么

第 6 步的目标是：

- 把输入从“写死在代码里”
- 升级成“从命令行真实传入”

也就是说，程序终于开始能被真正使用，而不是每次都去修改源码里的测试字符串。

## 当前启动流程

```text
CLI 参数
  ↓
myagent chat "hello"
  ↓
main.py
  ↓
load_config()
  ↓
make_provider(config)
  ↓
AgentLoop(provider)
  ↓
loop.run_once(message)
```

## 你会学到什么

1. 为什么 agent 需要真实输入入口
2. 如何用 Typer 把 Python 函数变成 CLI 命令
3. 如何把 CLI 输入一路传到 AgentLoop
4. 为什么 CLI 是后续 API / channel 输入入口的原型

## 运行方式

```bash
cd /Users/dale/.openclaw/workspace-taizi/deliverables/myagent_step1
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
myagent chat "hello from step6"
```

## 预期输出

```text
myagent booted
loaded config from = config/default.json
agent.name = myagent
agent.workspace = ./workspace
provider.name = mock
provider.model = mock-echo-v1
user.message = hello from step6
loop.response = [mock-provider:mock-echo-v1] you said: hello from step6
```
