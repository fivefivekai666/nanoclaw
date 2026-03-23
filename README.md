# myagent · Step 16

这是从 0 开始复刻 `nanobot + DeerFlow` 混血版 agent runtime 的第 16 步。

## 这一步在做什么

第 16 步的目标是：

- 从 `workspace/IDENTITY.md` / `workspace/SOUL.md` 读取最小 persona context
- 把这些 workspace 文件内容注入 `ContextBuilder`
- 让 runtime 上下文开始不只来自 config，也来自真实工作目录

当前采用最小实现策略：

- 文件存在：读取原始文本并注入
- 文件不存在：跳过，不报错
- config 中的 identity/persona 仍然保留，作为结构化默认身份层

## 当前结构

```text
config.identity/persona
workspace/IDENTITY.md
workspace/SOUL.md
  ↓
ContextBuilder
  ↓
prompt
  ↓
AgentLoop
  ↓
provider.chat(prompt)
```

## 你会学到什么

1. 为什么 config persona 和 workspace persona 可以同时存在
2. 为什么第 16 步先做“原样读取 + 注入”比立刻做复杂解析更稳
3. 为什么 workspace 文件是 agent 自我描述的重要来源
4. 为什么 ContextBuilder 会自然成长为统一上下文装配层

## 运行方式

```bash
cd /Users/dale/.openclaw/workspace-taizi/deliverables/myagent_step1
mkdir -p workspace
cat > workspace/IDENTITY.md <<'EOF'
# IDENTITY.md
- Name: myagent-from-file
- Vibe: warm and focused
EOF
cat > workspace/SOUL.md <<'EOF'
# SOUL.md
Speak clearly. Prefer structured answers.
EOF

python3 -m venv .venv
source .venv/bin/activate
pip install -e .
myagent chat "hello from step16" --session-id step16
```

## 预期现象

- 输出里会显示：
  - `workspace.identity.loaded = True`
  - `workspace.soul.loaded = True`
- mock provider 的回显内容里会包含：
  - `workspace.identity:`
  - `workspace.soul:`
  - 对应文件原文内容
- 这说明 workspace persona 已真实进入 provider 输入链路
