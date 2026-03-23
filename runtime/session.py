"""
runtime/session.py

这是第 9 步引入的最小 Session（会话）对象。

到了第 10 步，它仍然只负责“数据结构本身”：
- id
- messages
- add_message(...)
- latest_message()

注意：
第 10 步虽然加入了持久化能力，
但持久化逻辑被放在 `runtime/session_store.py`，
而不是塞进 Session 类本身。

这是为了保持分层清晰：
- Session = 会话是什么
- SessionStore = 会话存哪里
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

    它不直接负责磁盘 I/O。
    持久化由外部 store 处理。
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
