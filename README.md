# myagent · Step 27

这是从 0 开始复刻 `nanobot + DeerFlow` 混血版 agent runtime 的第 27 步。

## 这一步在做什么

第 27 步的目标是：

- 给 `LoopResult` 增加最小 `status / stop_reason`
- 让 loop 不只是表示“产出了什么”
- 还开始表示“这一轮为什么结束”

## 为什么这样做

第 26 步已经让 loop 从：

```text
run_once(session) -> Message
```

升级成：

```text
run_once(session) -> LoopResult
```

但当时的 `LoopResult` 还只是“结果内容容器”，
还不能表达这轮运行的结束语义。

而后面如果你要扩展：
- tool calling
- error path
- guardrail block
- max step stop
- retry / fallback

都需要先有统一的 status / stop_reason 位置。

所以第 27 步先做最小 happy-path 语义：

- `status = completed`
- `stop_reason = assistant_response`

## 当前新增结构

- `LoopStatus`
  - `COMPLETED`
- `LoopStopReason`
  - `ASSISTANT_RESPONSE`

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

myagent chat "hello from step27" --session-id step27
```

## 预期现象

输出里会显示：

- `loop.result.status = completed`
- `loop.result.stop_reason = assistant_response`
- `loop.result.status_type = LoopStatus`
- `loop.result.stop_reason_type = LoopStopReason`

这表示 loop 已开始表达“这轮为什么结束”，
而不只是“这轮产生了什么回复”。
