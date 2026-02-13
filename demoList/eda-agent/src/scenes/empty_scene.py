"""空场景 - 用于测试架构和路由

所有场景的具体实现都留空，只保留框架
"""
from typing import Dict, List, Optional, Generator
import sys
import os

# 导入基类
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from scenes.base import BaseScene


class EmptyScene(BaseScene):
    """空场景 - 用于测试架构

    只实现 match() 和 run() 的基本框架，不做具体业务
    """

    def __init__(self, services: Dict):
        """初始化空场景

        Args:
            services: 服务字典
        """
        super().__init__(
            name="empty",
            description="空场景 - 测试架构和路由",
            keywords=[],  # 不用关键词匹配，完全依赖 LLM
            services=services
        )

    def match(self, user_input: str) -> float:
        """计算匹配度

        空场景直接返回 0，让系统使用 LLM 意图识别
        """
        return 0.0

    def run(self, user_input: str) -> Generator[Dict, None, None]:
        """执行场景

        只输出消息，不做实际业务逻辑
        """
        # 显示基本信息
        yield self._create_info_message(f"[{self.name}] 场景被调用")
        yield self._create_info_message(f"[{self.name}] 用户输入: {user_input}")

        # 如果有 LLM，显示 LLM 理解（可选）
        if self.llm_service:
            yield self._create_info_message(f"[{self.name}] 有 LLM 服务可用")

        # 完成场景
        yield self._create_done_message({
            "scene": self.name,
            "user_input": user_input,
            "message": "这是空场景，没有实际业务逻辑"
        })


# ============================================================================
# 测试代码
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("空场景测试")
    print("=" * 70)

    # 创建模拟服务
    mock_services = {
        "llm": None,  # 简化，不传真实服务
        "rag": None,
        "eda": None,
        "state": None
    }

    # 创建空场景
    empty_scene = EmptyScene(mock_services)

    # 测试 match
    print("\n测试1: match() 总是返回 0")
    score = empty_scene.match("任何输入")
    print(f"   匹配分数: {score}")

    # 测试 run
    print("\n测试2: run() 生成消息")
    for message in empty_scene.run("测试输入"):
        print(f"   {message}")

    print("\n测试完成")
