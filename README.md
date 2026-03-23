# myagent · Step 28

这是从 0 开始复刻 `nanobot + DeerFlow` 混血版 agent runtime 的第 28 步。

## 这一步在做什么

第 28 步的目标是：

- 给 `LoopResult` 增加最小 `error / failure path` 边界
- 让 loop 不只会表达“正常结束”
- 也开始能表达“异常结束”

## 为什么这样做

第 27 步已经让 loop 能表达：

- `status`
- `stop_reason`

但当时只覆盖了 happy-path：

- `completed`
- `assistant_response`

如果后面要扩展：
- tool calling
- provider error
- retry
- guardrail
- multi-step orchestration

那么 loop 一定要先具备最小失败边界。

所以第 28 步先补最小 failure path：

- `status = failed`
- `stop_reason = provider_error`
- `error = LoopError(...)`

## 当前新增结构

- `LoopStatus`
  - `COMPLETED`
  - `FAILED`
- `LoopStopReason`
  - `ASSISTANT_RESPONSE`
  - `PROVIDER_ERROR`
- `LoopError`
  - `kind`
  - `message`

## 行为约束

### 成功路径
- `assistant_message` 不为空
- `error = None`
- assistant reply 会写回 session

### 失败路径
- `assistant_message = None`
- `error` 包含最小错误摘要
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

# 成功路径
myagent chat "hello from step28-success" --session-id step28-success

# 失败路径（仅用于验证）
myagent chat "hello from step28-failure" --session-id step28-failure --simulate-provider-error
```

## 预期现象

成功路径会显示：
- `loop.result.status = completed`
- `loop.result.stop_reason = assistant_response`
- `loop.result.error.kind = None`

失败路径会显示：
- `loop.result.status = failed`
- `loop.result.stop_reason = provider_error`
- `loop.result.error.kind = RuntimeError`
- `assistant.message.role = None`

这表示 loop 已开始具备最小 success / failure 两条语义边界。
