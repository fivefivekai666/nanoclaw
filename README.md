# myagent · Step 19

这是从 0 开始复刻 `nanobot + DeerFlow` 混血版 agent runtime 的第 19 步。

## 这一步在做什么

第 19 步的目标是：

- 把 memory 从 placeholder provider 升级为最小真实 provider
- 实际读取 `workspace/MEMORY.md`
- 把文件内容注入 `ContextBuilder`
- 保持 memory 模块边界不变

这一步的核心不是“智能记忆”，而是“真实 memory I/O 打通”。

## 为什么这样做

前一步已经把 memory 从 `ContextBuilder` 里拆成独立模块。
那么这一步最自然的前进方式就是：

```text
workspace/MEMORY.md -> FileMemoryProvider -> ContextBuilder
```

先让 memory 真正来自一个文件，再逐步做：
- 解析
- 裁剪
- 摘要
- 检索
- 分层记忆

## 当前结构

```text
workspace/MEMORY.md
  ↓
FileMemoryProvider
  ↓
ContextBuilder
  ↓
prompt
  ↓
AgentLoop
  ↓
provider.chat(prompt)
```

## 新增/调整模块

- 新增：`memory/file.py`
- 修改：`memory/__init__.py`
- 修改：`app/main.py`
- 修改：`README.md`

## 运行方式

```bash
cd /Users/dale/.openclaw/workspace-taizi/deliverables/myagent_step1
mkdir -p workspace
cat > workspace/MEMORY.md <<'EOF'
# MEMORY.md

- User prefers step-by-step explanations.
- Keep architecture modular.
EOF

source .venv/bin/activate
pip install -e .
myagent chat "hello from step19" --session-id step19
```

## 预期现象

- 输出里会显示：
  - `memory.provider = FileMemoryProvider`
  - `memory.path = workspace/MEMORY.md`（或等价路径）
  - `memory.exists = True`
- mock provider 回显里会出现：
  - `memory:`
  - `# MEMORY.md`
  - 文件中的实际内容
- 不再只是 placeholder 文本
