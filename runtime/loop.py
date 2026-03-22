"""
runtime/loop.py

这个文件以后会放 AgentLoop，
也就是整个 agent 的主循环。

未来它大概会负责：
1. 接收用户输入
2. 构造上下文
3. 调用模型
4. 处理 tool calls
5. 返回最终回复

但在第 1 步，我们先不要急着实现这些功能。
先把文件和模块结构准备好。
"""


class AgentLoop:
    """
    这是未来的主循环类骨架。

    现在先放一个最小占位版本，
    目的是让你先认识“项目未来会长什么样”。

    为什么不现在就写完整？
    因为完整的 AgentLoop 会依赖很多后续模块：
    - provider
    - config
    - tools
    - session
    - memory

    所以现在先占位，等第 2~4 步再逐渐填充。
    """

    def run(self) -> None:
        """
        未来这里会执行 agent 主循环。

        当前只是占位函数。
        """
        print("AgentLoop is not implemented yet.")
