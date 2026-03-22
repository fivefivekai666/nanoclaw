# myagent · Step 3

这是从 0 开始复刻 `nanobot + DeerFlow` 混血版 agent runtime 的第 3 步。

## 这一步在做什么

第 2 步解决的是：

- 配置“长什么样”

第 3 步解决的是：

- 配置“从哪里来”

所以这一步新增了一个最小配置加载器：

- `config/loader.py`

并增加了一个最小 JSON 配置文件：

- `config/default.json`

## 当前启动流程

```text
main.py
  ↓
load_config()
  ↓
config/default.json
  ↓
Config
```

## 你会学到什么

1. schema 和 loader 的职责区别
2. 为什么真实程序需要从文件读取配置
3. 如何把 JSON 配置加载成 Pydantic 对象
4. 为什么“加载配置”是 runtime 启动链路的一部分

## 运行方式

推荐使用虚拟环境：

```bash
cd /Users/dale/.openclaw/workspace-taizi/deliverables/myagent_step1
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
myagent
```

## 预期输出

```text
myagent booted
loaded config from = config/default.json
agent.name = myagent
agent.workspace = ./workspace
provider.name = openai
provider.model = gpt-4.1-mini
```
