"""
app/main.py

这是项目当前的命令行入口。

在第 1 步里，我们只做了一件事：
    打印 "myagent booted"

到了第 2 步，我们开始让 main.py 真的“接触配置对象”。

注意：
这一步仍然是非常小的一步。
我们还不会：
- 调模型
- 跑 agent loop
- 读配置文件
- 启动 channels

我们现在只做：
1. 导入默认配置
2. 打印几项配置内容
3. 让你看到“程序已经开始围绕 Config 运转”

这是从“一个会启动的包”过渡到“一个有 runtime 配置概念的程序”的关键一步。
"""

from config.schema import DEFAULT_CONFIG


def main() -> None:
    """
    项目的命令行入口函数。

    现在它做的事情比第 1 步多一点点：
    - 先拿到默认配置
    - 再把里面几个关键字段打印出来

    这样你运行 `myagent` 时，看到的就不再只是“程序活了”，
    而是能进一步确认：

    1. Config 类已经定义好了
    2. DEFAULT_CONFIG 已经能正常创建
    3. main.py 已经能读取配置对象

    这是非常关键的一小步。
    """
    config = DEFAULT_CONFIG

    print("myagent booted")
    print(f"agent.name = {config.agent.name}")
    print(f"agent.workspace = {config.agent.workspace}")
    print(f"provider.name = {config.provider.name}")
    print(f"provider.model = {config.provider.model}")
