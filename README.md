# myagent · Step 23

这是从 0 开始复刻 `nanobot + DeerFlow` 混血版 agent runtime 的第 23 步。

## 这一步在做什么

第 23 步的目标是：

- 给 `ResponsePolicy` 增加最小可配置项
- 当前先支持两档：`normal` / `concise`
- 让 loop 开始具备可控输出风格，而不只是“能跑”

## 为什么这样做

第 22 步已经把 `[INSTRUCTION]` 从 `ContextBuilder` 里拆成独立的 policy 层。
接下来最自然的一步，不是马上上复杂 policy 系统，
而是先让这个 policy 层具备最小“可配置性”。

这样可以先建立一个非常重要的能力：

```text
同一个 runtime 主链
+ 不同 response policy mode
= 不同回答风格
```

## 当前支持的 policy mode

- `normal`
  - 正常解释
  - 清晰、结构化、适度展开
- `concise`
  - 简短、直接、高信号
  - 除非用户要求，否则不做多余展开

## 配置与覆盖方式

### 配置文件默认值
`config/default.json`:

```json
"response_style": "normal"
```

### CLI 临时覆盖

```bash
myagent chat "hello" --response-style concise
```

## 修改模块

- 修改：`config/schema.py`
- 修改：`config/default.json`
- 修改：`runtime/policy.py`
- 修改：`app/main.py`
- 修改：`README.md`

## 运行方式

```bash
cd /Users/dale/.openclaw/workspace-taizi/deliverables/myagent_step1
source .venv/bin/activate
pip install -e .

# 默认 normal
myagent chat "hello from step23 normal" --session-id step23-normal

# 临时覆盖 concise
myagent chat "hello from step23 concise" --session-id step23-concise --response-style concise
```

## 预期现象

- 输出里会显示：
  - `agent.response_style.default = normal`
  - `agent.response_style.effective = ...`
- mock provider 回显里的 `[INSTRUCTION]` 会根据 mode 出现不同风格要求
- loop 继续稳定可跑
