# myagent · Step 16.5

这是从 0 开始复刻 `nanobot + DeerFlow` 混血版 agent runtime 的一个小前置步骤。

## 这一步在做什么

这一步不是完整的 memory 系统，而只是先在 `ContextBuilder` 中加入一个最小 `memory` 占位段。

目标是：

- 先把 prompt 骨架里的 `memory:` 位置固定下来
- 明确未来长期记忆应该挂载在这里
- 后续实现真实 memory store 时，不需要再改 prompt 总结构

当前策略：

- 不做真实 memory 读取
- 不做压缩、筛选、检索
- 只注入一段固定占位文本

## 当前结构

```text
system
identity
workspace persona
memory placeholder
history
  ↓
ContextBuilder
  ↓
prompt
```

## 你会学到什么

1. 为什么很多系统会先留 memory slot，再逐步接真实实现
2. 为什么 prompt 骨架先稳定下来很重要
3. 为什么 placeholder 是合理的架构前置动作

## 运行方式

```bash
cd /Users/dale/.openclaw/workspace-taizi/deliverables/myagent_step1
source .venv/bin/activate
pip install -e .
myagent chat "hello with memory placeholder" --session-id step16_5
```

## 预期现象

- 输出里会显示：
  - `memory.placeholder.enabled = True`
- mock provider 回显里会包含：
  - `memory:`
  - `[memory placeholder: not implemented yet]`
