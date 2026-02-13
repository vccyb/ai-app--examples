"""Base Scene - 场景基类

所有场景的抽象基类，定义场景的通用接口和行为
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Generator, Any
import json


class BaseScene(ABC):
    """场景基类

    所有具体场景必须继承此类并实现抽象方法
    """

    def __init__(
        self,
        name: str,
        description: str,
        keywords: List[str],
        services: Dict[str, Any]
    ):
        """初始化场景

        Args:
            name: 场景名称
            description: 场景描述
            keywords: 触发关键词列表
            services: 服务字典，包含 llm, rag, eda, state 等服务
        """
        self.name = name
        self.description = description
        self.keywords = keywords
        self.services = services

        # 从 services 字典中获取具体服务
        self.llm_service = services.get("llm")
        self.rag_service = services.get("rag")
        self.eda_service = services.get("eda")
        self.state_service = services.get("state")

    @abstractmethod
    def match(self, user_input: str) -> float:
        """计算用户输入与该场景的匹配度

        Args:
            user_input: 用户输入文本

        Returns:
            匹配度分数 0.0-1.0
        """
        pass

    @abstractmethod
    def run(self, user_input: str) -> Generator[Dict, None, None]:
        """执行场景逻辑

        Args:
            user_input: 用户输入文本

        Yields:
            场景执行过程中的消息字典，格式：
            {
                "type": "info" | "plan" | "step_result" | "ask" | "done" | "error",
                "content": "...",
                ... 其他字段
            }
        """
        pass

    # ========================================================================
    # 辅助方法
    # ========================================================================

    def _keyword_match_score(self, user_input: str) -> float:
        """基于关键词计算基础匹配分数

        Args:
            user_input: 用户输入文本

        Returns:
            基于关键词的匹配分数 0.0-1.0
        """
        if not self.keywords:
            return 0.0

        user_input_lower = user_input.lower()
        matched_count = sum(1 for kw in self.keywords if kw.lower() in user_input_lower)

        # 简单的匹配策略：匹配的关键词数量 / 总关键词数量
        return matched_count / len(self.keywords)

    def _create_message(self, msg_type: str, content: Any, **extra) -> Dict:
        """创建标准格式的消息字典

        Args:
            msg_type: 消息类型
            content: 消息内容
            **extra: 额外字段

        Returns:
            消息字典
        """
        message = {
            "type": msg_type,
            "scene": self.name,
            "content": content
        }
        message.update(extra)
        return message

    def _create_info_message(self, content: str) -> Dict:
        """创建信息消息"""
        return self._create_message("info", content)

    def _create_plan_message(
        self,
        steps: List[Dict],
        need_confirm: bool = True
    ) -> Dict:
        """创建计划消息"""
        return self._create_message(
            "plan",
            {"steps": steps, "need_confirm": need_confirm}
        )

    def _create_step_result_message(
        self,
        step: int,
        result: Dict,
        status: str = "SUCCESS"
    ) -> Dict:
        """创建步骤结果消息"""
        return self._create_message(
            "step_result",
            result,
            step=step,
            status=status
        )

    def _create_ask_message(
        self,
        question: str,
        options: Optional[List[str]] = None
    ) -> Dict:
        """创建询问消息"""
        return self._create_message(
            "ask",
            {"question": question, "options": options or []}
        )

    def _create_done_message(self, summary: Dict) -> Dict:
        """创建完成消息"""
        return self._create_message("done", summary)

    def _create_error_message(self, message: str) -> Dict:
        """创建错误消息"""
        return self._create_message("error", message)

    def __repr__(self) -> str:
        """字符串表示"""
        return f"<{self.__class__.__name__}(name='{self.name}')>"


# ============================================================================
# 测试代码
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("Base Scene 测试")
    print("=" * 70)

    # 创建一个测试场景
    class TestScene(BaseScene):
        """测试场景"""

        def __init__(self, services):
            super().__init__(
                name="test",
                description="测试场景",
                keywords=["测试", "test"],
                services=services
            )

        def match(self, user_input: str) -> float:
            return self._keyword_match_score(user_input)

        def run(self, user_input: str):
            yield self._create_info_message(f"开始执行测试场景，输入：{user_input}")
            yield self._create_done_message({"result": "测试成功"})

    # 模拟服务
    mock_services = {}

    # 创建测试场景
    test_scene = TestScene(mock_services)

    # 测试 match
    print("\n测试1：匹配度计算")
    score1 = test_scene.match("这是一个测试输入")
    print(f"匹配分数: {score1}")

    score2 = test_scene.match("这是无关输入")
    print(f"匹配分数: {score2}")

    # 测试 run
    print("\n测试2：执行场景")
    for message in test_scene.run("测试输入"):
        print(f"消息: {message}")

    print("\n测试完成")
