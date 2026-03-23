# myagent · Step 12

这是从 0 开始复刻 `nanobot + DeerFlow` 混血版 agent runtime 的第 12 步。

## 这一步在做什么

第 12 步的目标是：

- 给系统补上最小 session 管理能力
- 让 session 不只是能保存和读取
- 还可以被列出、被查看

当前新增两个命令：

```bash
myagent sessions list
myagent sessions inspect <session_id>
```

## 当前结构

```text
chat
  └─ 处理一轮对话并保存 session

sessions list
  └─ 列出当前所有已保存的 session

sessions inspect <id>
  └─ 查看某个 session 的详细消息内容
```

## 你会学到什么

1. 为什么 session 系统需要最小管理面
2. 为什么“能保存”之后，下一个自然需求就是“能查看”
3. 如何用 CLI 给 runtime 增加最小 control surface
4. 为什么这一步适合先做 list / inspect，而不是 delete / rename

## 运行方式

```bash
cd /Users/dale/.openclaw/workspace-taizi/deliverables/myagent_step1
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
myagent chat "hello alpha" --session-id alpha
myagent chat "hello beta" --session-id beta
myagent sessions list
myagent sessions inspect alpha
```

## 预期现象

- `sessions list` 会列出所有 `workspace/sessions/*.json`
- `sessions inspect alpha` 会输出 alpha 的完整消息列表
- 这意味着 session 系统第一次变得可观察、可检查
