# myagent · Step 2

这是从 0 开始复刻 `nanobot + DeerFlow` 混血版 agent runtime 的第 2 步。

## 这一小步的目标

这一步只做两件事：

- 把 `Config` 正式写出来
- 让 `main.py` 真的开始读取默认配置

## 你会学到什么

1. 为什么 agent 项目要先有配置对象
2. 如何用 Pydantic 定义最小配置结构
3. 为什么配置要分层，而不是全塞在一个类里
4. `main.py` 如何围绕配置对象开始运行

## 当前配置结构

```text
Config
├─ agent
│  ├─ name
│  ├─ workspace
│  └─ system_prompt
└─ provider
   ├─ name
   └─ model
```

## 运行方式

```bash
cd /Users/dale/.openclaw/workspace-taizi/deliverables/myagent_step1
pip install -e .
myagent
```

## 预期输出

```text
myagent booted
agent.name = myagent
agent.workspace = ./workspace
provider.name = openai
provider.model = gpt-4.1-mini
```
