# myagent · Step 31

这是从 0 开始复刻 `nanobot + DeerFlow` 混血版 agent runtime 的第 31 步。

## 这一步在做什么

第 31 步的目标是：

- 把 retry policy 从 `AgentLoop` 里的写死逻辑提炼成独立 runtime policy
- 给 retry policy 增加 config 边界
- 让 loop 不再自己决定“要不要重试”，而是委托给独立策略层

## 为什么这样做

第 30 步已经让 loop 能根据 recoverable 语义自动重试一次。

但那时 retry 规则仍然写死在 loop 里，
这会带来两个问题：

1. loop 同时负责“流程推进”和“执行策略判断”，职责开始混杂
2. 以后如果要扩展 max_attempts / fallback / backoff，就没有清晰落点

所以第 31 步先把执行策略层正式拆出来。

## 当前新增结构

- `runtime/retry_policy.py`
  - `RetryPolicy`
    - `max_attempts`
    - `retry_on_recoverable_only`
    - `should_retry(error, attempts_so_far)`

- `config.agent.retry`
  - `max_attempts`
  - `retry_on_recoverable_only`

## 当前最小策略规则

- `attempts_so_far >= max_attempts` -> 不再重试
- 如果 `retry_on_recoverable_only = True`
  - 只有 `error.recoverable = True` 时才允许重试
- 如果 `retry_on_recoverable_only = False`
  - 只要还没超过 `max_attempts` 就允许重试

## 行为约束

### 成功路径
- `assistant_message` 不为空
- `error = None`
- assistant reply 会写回 session
- `attempts` 由 retry policy 决定

### 失败路径
- `assistant_message = None`
- `error.kind` 属于受限枚举
- 是否继续重试由 `RetryPolicy` 决定
- 不伪造 assistant message
- 不把失败当成 assistant reply 写回 session

## 修改模块

- 新增：`runtime/retry_policy.py`
- 修改：`config/schema.py`
- 修改：`config/default.json`
- 修改：`runtime/loop.py`
- 修改：`runtime/__init__.py`
- 修改：`app/main.py`
- 修改：`README.md`

## 运行方式

```bash
cd /Users/dale/.openclaw/workspace-taizi/deliverables/myagent_step1
source .venv/bin/activate
pip install -e .

# 默认配置：最多 2 次，且仅对 recoverable 错误重试
myagent chat "hello from step31-default" --session-id step31-default --simulate-provider-error --simulate-error-type runtime --simulate-fail-times 1

# 覆盖配置：最多 1 次，相当于关闭重试
myagent chat "hello from step31-no-retry" --session-id step31-no-retry --simulate-provider-error --simulate-error-type runtime --simulate-fail-times 1 --retry-max-attempts 1

# 覆盖配置：允许非 recoverable 错误也重试
myagent chat "hello from step31-force-retry" --session-id step31-force-retry --simulate-provider-error --simulate-error-type value --simulate-fail-times 1 --retry-on-recoverable-only false
```

> 注意：这里为了避免 Typer 的布尔参数形态歧义，`--retry-on-recoverable-only` 当前按字符串接收，显式传 `true` / `false`。

## 预期现象

你会看到：

- `agent.retry.max_attempts.config = ...`
- `agent.retry.max_attempts.effective = ...`
- `agent.retry.retry_on_recoverable_only.config = ...`
- `agent.retry.retry_on_recoverable_only.effective = ...`

这表示 retry 已从 loop 内部硬编码，升级为独立 runtime policy / config 边界。
