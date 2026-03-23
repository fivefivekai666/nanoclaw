"""
runtime/messages.py

这是第 7 步新增的核心文件：最小消息模型（Message Model）。

为什么要引入它？
因为如果 runtime 内部一直只传裸字符串，后面很快就会遇到扩展瓶颈：
- 无法清楚区分 user / assistant / system
- 无法自然接入 session history
- 无法自然接入 memory、tools、subagents
- 无法把“消息”当成统一的数据单位

所以从第 7 步开始，我们把 runtime 的基本输入输出单位，
从 str 升级成结构化 Message 对象。

当前先保持最小实现，只保留两个字段：
- role
- content

这是最小但足够有用的一步。
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class Message(BaseModel):
    """
    表示系统内部的一条最小消息。

    现在只保留两个核心字段：
    - role: 这条消息是谁说的（user / assistant / system）
    - content: 这条消息的文本内容

    为什么先只保留这两个？
    因为它们已经足够表达最基础的对话结构，
    同时又不会在第 7 步一下子把模型做得过重。
    """

    role: str = Field(description="消息角色，例如 user / assistant / system")
    content: str = Field(description="消息正文内容")
