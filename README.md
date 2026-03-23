# myagent · Step 10

这是从 0 开始复刻 `nanobot + DeerFlow` 混血版 agent runtime 的第 10 步。

## 这一步在做什么

第 10 步的目标是：

- 给 `Session` 加上最小持久化能力
- 让会话可以 save / load
- 让对话第一次真正落盘

这里采用最简单、最适合教学的方案：
- 一个 session 对应一个 JSON 文件
- 默认目录：`workspace/sessions/`

## 当前启动流程

```text
CLI 参数
  ↓
myagent chat "hello"
  ↓
尝试 load_session("local-dev-session")
  ↓
若不存在则创建新 Session
  ↓
session.add_message(Message(role="user", content=...))
  ↓
AgentLoop.run_once(session)
  ↓
session.add_message(assistant_message)
  ↓
save_session(session)
```

## 你会学到什么

1. 为什么 Session 如果不落盘，就只是内存 demo
2. 为什么教学阶段最适合先用 JSON 文件持久化
3. 为什么 Session 和 SessionStore 应该分层
4. 为什么 save/load 是后续 SessionManager 的前身

## 运行方式

```bash
cd /Users/dale/.openclaw/workspace-taizi/deliverables/myagent_step1
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
myagent chat "hello from step10"
myagent chat "hello again from step10"
```

## 预期现象

第一次运行：
- `session.loaded_from_disk = False`
- `session.previous_message_count = 0`
- 会创建 `workspace/sessions/local-dev-session.json`

第二次运行：
- `session.loaded_from_disk = True`
- `session.previous_message_count` 会大于 0
- 表示旧会话已成功从磁盘恢复
