# myagent · Step 24

这是从 0 开始复刻 `nanobot + DeerFlow` 混血版 agent runtime 的第 24 步。

## 这一步在做什么

第 24 步的目标是：

- 给 `response_style` 增加最小合法值校验
- 对未知值做稳定 fallback
- 避免错误输入把 prompt 行为搞乱

## 为什么这样做

第 23 步已经让 `ResponsePolicy` 具备了最小可配置项。
但“可配置”如果没有约束，就容易变成“不可控”。

比如有人传入：
- `brief`
- `weird-style`
- `NORMAL!!!`

如果系统不做收敛，调试 loop 会很痛苦。

所以第 24 步把这层能力补齐：

```text
可配置 -> 可校验 -> 可回退 -> 可观察
```

## 当前策略

支持的合法值：
- `normal`
- `concise`

行为规则：
- 自动做最小规范化（去空白、小写化）
- 非法值自动 fallback 到 `normal`
- 启动输出中显示：
  - `requested`
  - `effective`
  - `fallback_used`

## 修改模块

- 修改：`runtime/policy.py`
- 修改：`app/main.py`
- 修改：`README.md`

## 运行方式

```bash
cd /Users/dale/.openclaw/workspace-taizi/deliverables/myagent_step1
source .venv/bin/activate
pip install -e .

# 合法值
myagent chat "hello concise" --session-id step24-concise --response-style concise

# 非法值，测试 fallback
myagent chat "hello weird" --session-id step24-fallback --response-style weird-style
```

## 预期现象

- 合法值时：
  - `effective = concise`
  - `fallback_used = False`
- 非法值时：
  - `effective = normal`
  - `fallback_used = True`
- mock provider 回显中的 `[INSTRUCTION]` 会体现最终生效的 style
