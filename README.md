# myagent · Step 11

这是从 0 开始复刻 `nanobot + DeerFlow` 混血版 agent runtime 的第 11 步。

## 这一步在做什么

第 11 步的目标是：

- 不再把 `local-dev-session` 写死在代码里
- 让默认 session id 来自配置文件
- 让 CLI 可以用 `--session-id` 显式指定会话

这样同一个程序就能自然管理多个会话。

## 当前启动流程

```text
CLI 参数
  ↓
myagent chat "hello" --session-id demo-a
  ↓
读取 config/default.json
  ↓
决定 effective_session_id
  ├─ 有 --session-id：用 CLI 值
  └─ 没传：用 config.agent.default_session_id
  ↓
load_session(effective_session_id)
  ↓
若不存在则创建新 Session
  ↓
运行一轮 agent
  ↓
save_session(...)
```

## 你会学到什么

1. 为什么 session id 不应该写死在 main.py
2. 为什么“配置默认值 + CLI 覆盖”是很常见的 runtime 设计
3. 如何让一个简单 CLI 支持多会话隔离
4. 为什么这是后续 session manager 的自然前一步

## 运行方式

```bash
cd /Users/dale/.openclaw/workspace-taizi/deliverables/myagent_step1
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
myagent chat "hello default"
myagent chat "hello alpha" --session-id alpha
myagent chat "hello beta" --session-id beta
```

## 预期现象

- 不带 `--session-id` 时，使用 `config/default.json` 里的默认 session id
- 带 `--session-id alpha` 时，会写入 `workspace/sessions/alpha.json`
- 带 `--session-id beta` 时，会写入 `workspace/sessions/beta.json`
- 不同 session 之间的消息历史彼此隔离
