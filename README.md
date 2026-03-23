# myagent · Step 30

这是从 0 开始复刻 `nanobot + DeerFlow` 混血版 agent runtime 的第 30 步。

## 这一步在做什么

第 30 步的目标是：

- 给 `AgentLoop` 增加最小 retry policy 边界
- 当错误 `recoverable=True` 时自动重试 1 次
- 把本轮实际尝试次数记录到 `LoopResult`

## 为什么这样做

第 29 步已经让 loop 能表达：

- `error.kind`
- `error.recoverable`

但那时 runtime 还只是“知道这类错误也许可恢复”，
并没有真的采取恢复动作。

所以第 30 步先做最小执行闭环：

- recoverable 错误 -> 自动重试 1 次
- fatal 错误 -> 不重试，直接失败

## 当前新增结构

- `LoopResult.attempts`
  - 表示本轮实际调用 provider 的次数

## 当前最小 retry 规则

- 第一次失败后，如果 `error.recoverable = True`
  - 自动再试 1 次
- 如果第二次成功
  - 返回 `completed`
- 如果第二次仍失败
  - 返回 `failed`
- 如果第一次就是 `recoverable = False`
  - 不重试，直接失败

## 行为约束

### 成功路径
- `assistant_message` 不为空
- `error = None`
- assistant reply 会写回 session
- `attempts` 可能是 `1` 或 `2`

### 失败路径
- `assistant_message = None`
- `error.kind` 属于受限枚举
- `error.recoverable` 明确表明未来是否适合 retry / fallback
- fatal 错误不重试
- 不伪造 assistant message
- 不把失败当成 assistant reply 写回 session

## 修改模块

- 修改：`runtime/result.py`
- 修改：`runtime/loop.py`
- 修改：`runtime/__init__.py`
- 修改：`app/main.py`
- 修改：`README.md`

## 运行方式

```bash
cd /Users/dale/.openclaw/workspace-taizi/deliverables/myagent_step1
source .venv/bin/activate
pip install -e .

# 成功路径：一次成功
myagent chat "hello from step30-success" --session-id step30-success

# 可恢复路径：第一次失败，第二次成功
myagent chat "hello from step30-retry-success" --session-id step30-retry-success --simulate-provider-error --simulate-error-type runtime --simulate-fail-times 1

# fatal 路径：不重试
myagent chat "hello from step30-fatal" --session-id step30-fatal --simulate-provider-error --simulate-error-type value --simulate-fail-times 1

# 可恢复但最终仍失败：两次都失败
myagent chat "hello from step30-retry-fail" --session-id step30-retry-fail --simulate-provider-error --simulate-error-type runtime --simulate-fail-times 2
```

## 预期现象

你会看到：

- `loop.result.attempts = 1 | 2`
- recoverable 错误时会自动重试一次
- fatal 错误时不会重试

这表示 loop 已开始从“表达错误语义”，推进到“根据错误语义执行最小恢复动作”。
