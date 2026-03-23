# myagent · Step 21

这是从 0 开始复刻 `nanobot + DeerFlow` 混血版 agent runtime 的第 21 步。

## 这一步在做什么

第 21 步的目标是：

- 不再只是把上下文内容顺着往下拼
- 把 prompt 升级成固定的 section 模板
- 让 loop 每轮都收到结构稳定、边界清晰的输入

## 为什么这样做

当前系统已经有：
- config identity / persona
- workspace persona
- memory provider
- session history

如果只是继续把这些内容往 prompt 里堆，
短期虽然能跑，但后面一旦加：
- tools
- safety rules
- recalled memory
- response formatting

就会越来越乱。

所以第 21 步先把“结构”做稳。

## 当前 prompt 结构

```text
[SYSTEM]
...

[IDENTITY]
...

[WORKSPACE]
...

[MEMORY]
...

[CONVERSATION]
...

[INSTRUCTION]
...
```

## 这样做的好处

- loop 输入更稳定
- 更容易调试 prompt
- 后续扩展时有明确插槽
- 模型更容易区分：长期规则 / 工作区人格 / memory / 当前对话 / 输出要求

## 修改模块

- 修改：`runtime/context.py`
- 修改：`app/main.py`
- 修改：`README.md`

## 运行方式

```bash
cd /Users/dale/.openclaw/workspace-taizi/deliverables/myagent_step1
source .venv/bin/activate
pip install -e .
myagent chat "hello from step21" --session-id step21
```

## 预期现象

- 输出里会显示：
  - `prompt.mode = sectioned`
  - `prompt.sections = SYSTEM, IDENTITY, WORKSPACE, MEMORY, CONVERSATION, INSTRUCTION`
- mock provider 回显里能清楚看到各 section 边界
- loop 仍然可以正常跑通
