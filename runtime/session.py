"""
runtime/session.py

这是第 9 步新增的核心文件：最小 Session（会话）对象。

为什么需要它？
因为到了第 8 步，runtime 虽然已经能处理 history，
但 history 仍然只是 main.py 里临时构造的 list[Message]。

这意味着：
- 上下文存在了
- 但上下文还没有“归属”
- 还没有一个正式对象来持有整段对话

所以第 9 步要做的事情是：
把 history 挂到一个 Session 容器上。

当前保持最小实现：
- id: 会话标识
- messages: 当前会话中的消息列表
- add_message(...): 追加消息
- latest_message(): 读取最后一条消息

先把“会话容器”这个概念建立起来，
后面再做持久化、恢复、裁剪、总结。
"""

from __future__ import annotations

from pydantic import BaseModel, Field

from runtime.messages import Message


class Session(BaseModel):
    """
    表示一次最小对话会话。

    它的职责目前非常单纯：
    - 持有一组按顺序排列的 Message
    - 提供最小追加能力
    - 提供读取最后一条消息的能力

    这一步还不负责磁盘保存，也不负责多会话管理，
    只负责让“消息历史”第一次拥有正式宿主。
    """

    id: str = Field(description="会话 ID")
    messages: list[Message] = Field(default_factory=list, description="当前会话的消息列表")

    def add_message(self, message: Message) -> None:
        """向当前会话追加一条消息。"""
        self.messages.append(message)

    def latest_message(self) -> Message | None:
        """返回最后一条消息；若会话为空则返回 None。"""
        if not self.messages:
            return None
        return self.messages[-1]
