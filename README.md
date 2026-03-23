# myagent · Step 25

这是从 0 开始复刻 `nanobot + DeerFlow` 混血版 agent runtime 的第 25 步。

## 这一步在做什么

第 25 步的目标是：

- 把 `response_style` 从裸字符串升级成更明确的受限类型入口
- 减少 runtime 中散落的字符串判断
- 保留第 24 步已有的校验、fallback、可观察性

## 为什么这样做

第 24 步已经让 `response_style` 变成：

```text
可配置 + 可校验 + 可回退 + 可观察
```

但 runtime 内部本质上仍然在传字符串。
字符串在小项目里可以跑，但随着 style 变多，问题就会出现：

- 拼写容易散落
- 条件判断容易重复
- 未来扩展更难收敛

所以第 25 步继续收紧边界：

```text
裸字符串 -> ResponseStyle 枚举入口
```

## 当前结构

- `ResponseStyle`
  - `NORMAL`
  - `CONCISE`
- `ResponsePolicy`
  - 接受字符串或枚举
  - 内部统一规范化成 `ResponseStyle`

## 修改模块

- 修改：`runtime/policy.py`
- 修改：`runtime/__init__.py`
- 修改：`app/main.py`
- 修改：`README.md`

## 运行方式

```bash
cd /Users/dale/.openclaw/workspace-taizi/deliverables/myagent_step1
source .venv/bin/activate
pip install -e .

# 合法值
myagent chat "hello concise" --session-id step25-concise --response-style concise

# 非法值，测试 fallback
myagent chat "hello weird" --session-id step25-fallback --response-style weird-style
```

## 预期现象

- 输出里会显示：
  - `agent.response_style.type = ResponseStyle`
  - `agent.response_style.normalized = ...`
  - `agent.response_style.effective = ...`
  - `agent.response_style.fallback_used = ...`
- mock provider 回显中的 `[INSTRUCTION]` 仍然体现最终生效的 style
- loop 主链保持稳定
