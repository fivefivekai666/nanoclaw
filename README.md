# myagent · Step 29

这是从 0 开始复刻 `nanobot + DeerFlow` 混血版 agent runtime 的第 29 步。

## 这一步在做什么

第 29 步的目标是：

- 给 `LoopResult` 的 failure path 增加最小 `error_kind` 受限分类边界
- 补一个最小 `recoverable / fatal` 区分
- 让未来 retry / fallback 有明确落点

## 为什么这样做

第 28 步已经让 loop 能表达：

- `status = failed`
- `stop_reason = provider_error`
- `error = ...`

但那时的 `error` 还只是最小字符串摘要，
还不能稳定回答两个问题：

1. 这类错误属于什么分类？
2. 这类错误未来是否值得 retry / fallback？

所以第 29 步先补最小失败语义：

- `LoopErrorKind`
- `recoverable`

## 当前新增结构

- `LoopErrorKind`
  - `PROVIDER_ERROR`
  - `CONFIG_ERROR`
  - `INTERNAL_ERROR`
- `LoopError`
  - `kind: LoopErrorKind`
  - `message: str`
  - `recoverable: bool`

## 当前最小分类规则

- `RuntimeError` -> `provider_error`, `recoverable = True`
- `ValueError` -> `config_error`, `recoverable = False`
- 其他异常 -> `internal_error`, `recoverable = False`

## 行为约束

### 成功路径
- `assistant_message` 不为空
- `error = None`
- assistant reply 会写回 session

### 失败路径
- `assistant_message = None`
- `error.kind` 属于受限枚举
- `error.recoverable` 明确表明未来是否适合 retry / fallback
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
myagent chat "hello from step29-success" --session-id step29-success

# provider_error / recoverable=True
myagent chat "hello from step29-runtime" --session-id step29-runtime --simulate-provider-error --simulate-error-type runtime

# config_error / recoverable=False
myagent chat "hello from step29-value" --session-id step29-value --simulate-provider-error --simulate-error-type value
```

## 预期现象

你会看到失败路径里不只显示错误消息，
还会显示：

- `loop.result.error.kind = provider_error | config_error | internal_error`
- `loop.result.error.recoverable = True | False`

这表示 loop 的 failure path 已开始拥有未来 retry / fallback 所需要的最小分类边界。
