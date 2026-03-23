# myagent · Step 22

这是从 0 开始复刻 `nanobot + DeerFlow` 混血版 agent runtime 的第 22 步。

## 这一步在做什么

第 22 步的目标是：

- 不再让 `ContextBuilder` 自己硬编码 `[INSTRUCTION]`
- 把响应规则升级成独立的 runtime response policy 层
- 让“上下文内容”和“回答规则”职责分离

## 为什么这样做

第 21 步已经把 prompt 做成固定 section 模板。
但其中 `[INSTRUCTION]` 仍然是写死在 `ContextBuilder` 里的。

这意味着一个模块同时负责：
- 上下文装配
- 回答规则装配

这两个职责虽然相关，但不应该绑死在一起。

所以第 22 步继续拆分边界：

```text
ContextBuilder -> 负责上下文内容
ResponsePolicy -> 负责回答规则
```

## 当前结构

```text
provider
memory provider
response policy
context builder
agent loop
```

以及 prompt 仍保持：

```text
[SYSTEM]
[IDENTITY]
[WORKSPACE]
[MEMORY]
[CONVERSATION]
[INSTRUCTION]
```

只是 `[INSTRUCTION]` 现在来自 `ResponsePolicy`。

## 修改模块

- 新增：`runtime/policy.py`
- 修改：`runtime/context.py`
- 修改：`runtime/__init__.py`
- 修改：`app/main.py`
- 修改：`README.md`

## 运行方式

```bash
cd /Users/dale/.openclaw/workspace-taizi/deliverables/myagent_step1
source .venv/bin/activate
pip install -e .
myagent chat "hello from step22" --session-id step22
```

## 预期现象

- 输出里会显示：
  - `response.policy = ResponsePolicy`
- mock provider 回显里仍然有 `[INSTRUCTION]`
- loop 继续稳定可跑
