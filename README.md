# myagent · Step 1

这是从 0 开始复刻 `nanobot + DeerFlow` 混血版 agent runtime 的第 1 步。

## 这一小步的目标

只做一件事：

- 让项目作为一个 Python 包成功启动
- 让 `myagent` 命令可以跑起来

## 当前目录

- `app/`：程序入口
- `runtime/`：未来的 agent 主循环
- `providers/`：未来的模型提供商抽象
- `config/`：未来的配置对象

## 运行方式

```bash
cd deliverables/myagent_step1
pip install -e .
myagent
```

## 预期输出

```text
myagent booted
```
