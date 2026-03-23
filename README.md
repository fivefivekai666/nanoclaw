# myagent · Step 17

这是从 0 开始复刻 `nanobot + DeerFlow` 混血版 agent runtime 的第 17 步。

## 这一步在做什么

第 17 步的目标是：

- 对 `workspace/IDENTITY.md` 做最小结构化解析
- 不再默认把它整段原文塞进 prompt
- 优先提取出可控的身份字段，再注入 `ContextBuilder`

当前解析策略非常克制：

- 只解析最简单的 `- Key: Value`
- 优先支持常见字段：
  - `Name`
  - `Creature`
  - `Vibe`
  - `Emoji`
  - `Avatar`
- 其他字段放进 `extras`
- `SOUL.md` 仍然保持原文注入
- 如果 `IDENTITY.md` 完全解析不出来，仍保留 raw fallback

## 当前结构

```text
config.identity/persona
workspace/IDENTITY.md -> structured identity
workspace/SOUL.md -> raw text
memory placeholder
history
  ↓
ContextBuilder
  ↓
prompt
```

## 你会学到什么

1. 为什么结构化 identity 比原文块更适合后续编程使用
2. 为什么先做最小解析器比一步到位做完整 markdown parser 更稳
3. 为什么 fallback 仍然重要

## 运行方式

```bash
cd /Users/dale/.openclaw/workspace-taizi/deliverables/myagent_step1
mkdir -p workspace
cat > workspace/IDENTITY.md <<'EOF'
# IDENTITY.md
- Name: myagent-from-file
- Creature: ghost in the machine
- Vibe: warm and focused
- Emoji: 🧠
EOF

python3 -m venv .venv
source .venv/bin/activate
pip install -e .
myagent chat "hello from step17" --session-id step17
```

## 预期现象

- 输出里会显示：
  - `workspace.identity.structured = True`
  - `workspace.identity.name = myagent-from-file`
  - `workspace.identity.creature = ghost in the machine`
  - `workspace.identity.vibe = warm and focused`
- mock provider 回显里会出现结构化的：
  - `workspace.identity:`
  - `- name: ...`
  - `- creature: ...`
  - `- vibe: ...`
- 而不是直接整段原文块
