# myagent · Step 26

这是从 0 开始复刻 `nanobot + DeerFlow` 混血版 agent runtime 的第 26 步。

## 这一步在做什么

第 26 步的目标是：

- 把 `AgentLoop.run_once()` 的返回值从单一 `Message` 升级成结构化 `LoopResult`
- 给 loop 的执行结果建立稳定边界
- 为后续扩展 tool / stop reason / usage / debug 信息预留位置

## 为什么这样做

到第 25 步为止，loop 虽然已经能跑完整主链，但它本质上仍然只是：

```text
session -> prompt -> provider -> assistant message
```

如果 loop 最终只返回一个 `Message`，那它只适合表示“回答内容”，
却不适合表示“一轮运行结果”。

而后面无论你要加：
- tools
- stop reason
- usage 统计
- debug 信息
- action planning

都更适合挂在一个统一的结果对象上。

所以第 26 步先把边界立起来：

```text
AgentLoop.run_once(session) -> LoopResult
```

## 当前 LoopResult 字段

当前保持最小设计，只放最必要字段：

- `session_id`
- `prompt`
- `assistant_message`

## 修改模块

- 新增：`runtime/result.py`
- 修改：`runtime/loop.py`
- 修改：`runtime/__init__.py`
- 修改：`app/main.py`
- 修改：`README.md`

## 运行方式

```bash
cd /Users/dale/.openclaw/workspace-taizi/deliverables/myagent_step1
source .venv/bin/activate
pip install -e .

myagent chat "hello from step26" --session-id step26
```

## 预期现象

输出里会显示：

- `loop.result.type = LoopResult`
- `loop.result.session_id = step26`
- `loop.result.prompt_length = ...`
- `loop.result.assistant_role = assistant`

这表示 loop 已不再只是返回一条消息，
而是返回一次最小结构化执行结果。
