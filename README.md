# myagent · Step 32

这是从 0 开始复刻 `nanobot + DeerFlow` 混血版 agent runtime 的第 32 步。

## 这一步在做什么

第 32 步的目标是：

- 把 provider fallback 从 `AgentLoop` 里的写死逻辑提炼成独立 execution policy
- 给 fallback provider 增加 config 边界
- 让 loop 不再自己决定“主 provider 失败后要不要切 fallback provider”，而是委托给独立策略层

## 当前新增结构

- `runtime/execution_policy.py`
  - `ExecutionPolicy`
    - `primary_provider`
    - `fallback_provider`
    - `fallback_on_recoverable_only`
    - `should_fallback(...)`

- `config.provider.fallback`
  - `enabled`
  - `name`
  - `model`
  - `on_recoverable_only`

- `LoopResult`
  - `provider_used`
  - `fallback_used`

## 当前最小策略规则

- 主 provider 失败后，先由 retry policy 决定是否继续在当前 provider 重试
- 如果 retry 不再继续，再由 execution policy 决定是否切到 fallback provider
- 如果允许 fallback，则切到 fallback provider 再继续尝试

## 修改模块

- 新增：`runtime/execution_policy.py`
- 修改：`providers/__init__.py`
- 修改：`config/schema.py`
- 修改：`config/default.json`
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

# 默认配置：主 provider 失败后，经过 retry，再切到 fallback provider
myagent chat "hello from step32-fallback" --session-id step32-fallback --simulate-provider-error --simulate-error-type runtime --simulate-fail-times 2

# 关闭 fallback：最终失败
myagent chat "hello from step32-no-fallback" --session-id step32-no-fallback --simulate-provider-error --simulate-error-type runtime --simulate-fail-times 2 --fallback-enabled false

# 允许非 recoverable 错误也切 fallback provider
myagent chat "hello from step32-force-fallback" --session-id step32-force-fallback --simulate-provider-error --simulate-error-type value --simulate-fail-times 1 --retry-max-attempts 1 --fallback-on-recoverable-only false
```

## 预期现象

你会看到：

- `provider.execution_policy = ExecutionPolicy`
- `loop.result.provider_used = ...`
- `loop.result.fallback_used = True | False`

这表示 provider fallback 已从 loop 内部硬编码，升级为独立 execution policy / config 边界。
