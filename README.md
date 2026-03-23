# myagent · Step 20

这是从 0 开始复刻 `nanobot + DeerFlow` 混血版 agent runtime 的第 20 步。

## 这一步在做什么

第 20 步的目标是：

- 继续使用 `workspace/MEMORY.md` 作为真实 memory 来源
- 但不再把原文整个直接塞进 prompt
- 给 `FileMemoryProvider` 增加最小结构化处理
- 只提取 `MEMORY.md` 的有效内容块

## 为什么这样做

第 19 步已经完成了真实 memory I/O 打通。
接下来最自然的优化不是立刻做复杂记忆系统，
而是先解决“原文直塞 prompt 太粗糙”这个问题。

这一步只做低风险、高收益的清洗：
- 去掉顶层标题（如 `# MEMORY.md`）
- 去掉纯 HTML 注释行（如 `<!-- ... -->`）
- 压缩连续空行为单个空行

这样可以先让 prompt 更干净，而不急着引入复杂策略。

## 当前结构

```text
workspace/MEMORY.md
  ↓
FileMemoryProvider（最小结构化清洗）
  ↓
ContextBuilder
  ↓
prompt
  ↓
AgentLoop
  ↓
provider.chat(prompt)
```

## 修改模块

- 修改：`memory/file.py`
- 修改：`app/main.py`
- 修改：`README.md`

## 运行方式

```bash
cd /Users/dale/.openclaw/workspace-taizi/deliverables/myagent_step1
mkdir -p workspace
cat > workspace/MEMORY.md <<'EOF'
# MEMORY.md

<!-- internal comment -->

- User prefers step-by-step explanations.
-
- Keep architecture modular.
EOF

source .venv/bin/activate
pip install -e .
myagent chat "hello from step20" --session-id step20
```

## 预期现象

- 输出里会显示：
  - `memory.provider = FileMemoryProvider`
  - `memory.mode = structured-file`
- mock provider 回显中的 `memory:` 段：
  - 不再包含 `# MEMORY.md`
  - 不再包含纯 HTML 注释行
  - 空行比之前更规整
- 但 memory 的真实来源仍然是 `workspace/MEMORY.md`
