"""简化的 VerifyScene - 只保留框架

移除所有复杂的解析逻辑（正则、LLM 解析等）
只保留场景的基本结构，用于测试架构
"""
from typing import Dict, List, Optional, Generator
import sys
import os

# 导入基类
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from scenes.base import BaseScene


class VerifyScene(BaseScene):
    """简化的验证场景

    只实现框架，不包含具体业务逻辑
    """

    def __init__(self, services: Dict):
        """初始化验证场景

        Args:
            services: 服务字典
        """
        super().__init__(
            name="verify",
            description="验证场景 - 框架版本（无具体实现）",
            keywords=[],  # 清空关键词，完全依赖 LLM 意图识别
            services=services
        )

    def match(self, user_input: str) -> float:
        """计算匹配度

        返回 0，让 SceneManager 使用 LLM 进行意图识别
        """
        return 0.0

    def run(self, user_input: str) -> Generator[Dict, None, None]:
        """执行验证场景

        只输出框架信息，不做实际验证工作
        """
        yield self._create_info_message(f"\n[{self.name.upper()}] 验证场景启动")
        yield self._create_info_message(f"[{self.name}] 收到输入: {user_input}")

        # 显示可用服务
        if self.llm_service:
            yield self._create_info_message(f"[{self.name}] ✓ LLM 服务可用")
        else:
            yield self._create_info_message(f"[{self.name}] ⚠️ 无 LLM 服务")

        if self.rag_service:
            yield self._create_info_message(f"[{self.name}] ✓ RAG 服务可用")
        if self.eda_service:
            yield self._create_info_message(f"[{self.name}] ✓ EDA 服务可用")
        if self.state_service:
            yield self._create_info_message(f"[{self.name}] ✓ State 服务可用")

        yield self._create_done_message({
            "scene": self.name,
            "message": "这是简化的验证场景，没有实际业务逻辑",
            "note": "正常场景会在这里执行：查询规范 → 运行仿真 → 评估结果"
        })


# ============================================================================
# 测试代码
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("简化的 VerifyScene 测试")
    print("=" * 70)

    # 创建模拟服务（都设为 None）
    mock_services = {
        "llm": "Mock LLM Service",
        "rag": "Mock RAG Service",
        "eda": "Mock EDA Service",
        "state": "Mock State Service"
    }

    # 创建简化的验证场景
    verify_scene = VerifyScene(mock_services)

    # 测试 match
    print("\n测试1: match() 返回 0")
    score = verify_scene.match("验证模块A的时序<10ns")
    print(f"   输入: 验证模块A的时序<10ns")
    print(f"   匹配分数: {score}")

    # 测试 run
    print("\n测试2: run() 生成消息")
    for message in verify_scene.run("测试输入"):
        msg_type = message.get("type")
        content = message.get("content")
        print(f"   [{msg_type}] {content}")

    print("\n测试完成")
