# myagent · Step 18

这是从 0 开始复刻 `nanobot + DeerFlow` 混血版 agent runtime 的第 18 步。

## 这一步在做什么

第 18 步的目标是：

- 把 memory placeholder 从 `ContextBuilder` 内部参数中抽出来
- 升级成独立的 memory 模块接口
- 让 `ContextBuilder` 依赖 `memory_provider`
- 当前仍然只使用 placeholder provider，不做真实记忆检索

这是一个“结构升级”步骤，而不是“功能堆叠”步骤。

## 为什么这样做

如果继续把 memory 写死在 `ContextBuilder` 里，那么后面接真实记忆系统时，
`ContextBuilder` 会越来越胖，最终同时承担：

- memory 来源
- memory 筛选
- memory 压缩
- memory 格式化
- prompt 装配

这会让边界变乱。

更合理的拆法是：

- `ContextBuilder`：只负责装配上下文
- `MemoryProvider`：负责生成 memory block

## 当前结构

```text
PlaceholderMemoryProvider
  ↓
ContextBuilder
  ↓
prompt
  ↓
AgentLoop
  ↓
provider.chat(prompt)
```

## 新增模块

- `memory/base.py`
- `memory/placeholder.py`
- `memory/__init__.py`

## 你会学到什么

1. 为什么 placeholder 最好也有独立模块边界
2. 为什么模块化往往先于完整功能实现
3. 为什么 `ContextBuilder` 不应该知道 memory 的内部实现细节

## 运行方式

```bash
cd /Users/dale/.openclaw/workspace-taizi/deliverables/myagent_step1
source .venv/bin/activate
pip install -e .
myagent chat "hello from step18" --session-id step18
```

## 预期现象

- 输出里会显示：
  - `memory.provider = PlaceholderMemoryProvider`
  - `memory.placeholder.enabled = True`
- mock provider 回显里仍会包含：
  - `memory:`
  - `[memory placeholder: not implemented yet]`
- 但这个 placeholder 的来源已经变成独立 memory 模块，而不是 ContextBuilder 内部字符串
