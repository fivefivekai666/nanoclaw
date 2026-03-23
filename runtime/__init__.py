"""
runtime/__init__.py

runtime 包从第 5 步开始不再只是“占位目录”，
而是正式暴露一个真正参与运行的核心对象：

- AgentLoop

这意味着项目的职责分层开始更清晰：
- app/        负责启动入口
- config/     负责配置定义与加载
- providers/  负责模型适配
- runtime/    负责主流程控制
"""

from runtime.loop import AgentLoop

__all__ = ["AgentLoop"]
