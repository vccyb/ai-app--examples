"""SceneManager - 场景管理器

负责：
- 场景注册
- 用户输入路由到匹配的场景
- 场景生命周期管理
"""
from typing import Dict, List, Optional
import sys
import os

# 导入场景基类
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from scenes.base import BaseScene


class SceneManager:
    """场景管理器

    管理所有场景的注册和路由
    """

    def __init__(self, services: Dict):
        """初始化场景管理器

        Args:
            services: 服务字典，包含所有基础服务
        """
        self.services = services
        self.scenes: List[BaseScene] = []
        self._min_match_score = 0.3  # 最低匹配分数阈值

    def register_scene(self, scene: BaseScene) -> None:
        """注册场景

        Args:
            scene: 场景实例
        """
        if not isinstance(scene, BaseScene):
            raise ValueError(f"场景必须继承自 BaseScene，得到：{type(scene)}")

        self.scenes.append(scene)
        print(f"[SceneManager] 注册场景: {scene.name}({scene.description})")

    def route(self, user_input: str) -> Optional[BaseScene]:
        """路由用户输入到最匹配的场景

        Args:
            user_input: 用户输入文本

        Returns:
            匹配的场景实例，如果没有匹配则返回 None
        """
        if not user_input or not user_input.strip():
            return None

        best_scene = None
        best_score = 0.0

        # 遍历所有场景，计算匹配分数
        for scene in self.scenes:
            score = scene.match(user_input)

            if score > best_score:
                best_score = score
                best_scene = scene

        # 检查是否达到阈值
        if best_score >= self._min_match_score:
            print(f"[SceneManager] 匹配场景: {best_scene.name} (score={best_score:.2f})")
            return best_scene

        # 关键词匹配失败，使用 LLM 进行意图识别
        print(f"[SceneManager] 关键词匹配失败 (最高分数：{best_score:.2f} < 阈值{self._min_match_score})")
        print(f"[SceneManager] 尝试使用 LLM 进行意图识别...")

        llm_service = self.services.get("llm")
        if not llm_service:
            print(f"[SceneManager] LLM 服务不可用，无法进行意图识别")
            return None

        # 获取所有场景名称
        scene_names = [scene.name for scene in self.scenes]

        # 使用 LLM 进行分类
        try:
            classification = llm_service.classify(
                text=user_input,
                categories=scene_names
            )

            predicted_scene_name = classification.get("category", "unknown")
            confidence = classification.get("confidence", 0.0)

            print(f"[SceneManager] LLM 预测场景: {predicted_scene_name} (置信度: {confidence:.2f})")

            # 根据 LLM 返回的场景名称查找场景实例
            if predicted_scene_name != "unknown":
                llm_scene = self.get_scene_by_name(predicted_scene_name)

                if llm_scene:
                    print(f"[SceneManager] ✓ LLM 成功识别场景: {llm_scene.name}")
                    return llm_scene
                else:
                    print(f"[SceneManager] ✗ LLM 返回的场景名称 '{predicted_scene_name}' 未找到")

        except Exception as e:
            print(f"[SceneManager] ✗ LLM 意图识别失败: {str(e)}")

        print(f"[SceneManager] 未找到匹配场景")
        return None

    def list_scenes(self) -> List[Dict]:
        """列出所有已注册的场景

        Returns:
            场景信息列表
        """
        return [
            {
                "name": scene.name,
                "description": scene.description,
                "keywords": scene.keywords
            }
            for scene in self.scenes
        ]

    def get_scene_by_name(self, name: str) -> Optional[BaseScene]:
        """按名称获取场景

        Args:
            name: 场景名称

        Returns:
            场景实例，如果不存在则返回 None
        """
        for scene in self.scenes:
            if scene.name == name:
                return scene
        return None

    def set_min_match_score(self, score: float) -> None:
        """设置最低匹配分数阈值

        Args:
            score: 阈值 0.0-1.0
        """
        if 0.0 <= score <= 1.0:
            self._min_match_score = score
        else:
            raise ValueError(f"匹配分数必须在 0.0-1.0 之间，得到：{score}")


# ============================================================================
# 测试代码
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("Scene Manager 测试")
    print("=" * 70)

    # 创建测试场景
    class MockScene1(BaseScene):
        def __init__(self, services):
            super().__init__(
                name="verify",
                description="验证场景",
                keywords=["验证", "verify", "优化", "optimize"],
                services=services
            )

        def match(self, user_input: str) -> float:
            return self._keyword_match_score(user_input)

        def run(self, user_input: str):
            yield self._create_info_message(f"验证场景执行：{user_input}")
            yield self._create_done_message({})

    class MockScene2(BaseScene):
        def __init__(self, services):
            super().__init__(
                name="report",
                description="报告场景",
                keywords=["报告", "report", "导出", "export"],
                services=services
            )

        def match(self, user_input: str) -> float:
            return self._keyword_match_score(user_input)

        def run(self, user_input: str):
            yield self._create_info_message(f"报告场景执行：{user_input}")
            yield self._create_done_message({})

    # 创建场景管理器
    manager = SceneManager(services={})

    # 注册场景
    print("\n注册场景：")
    manager.register_scene(MockScene1({}))
    manager.register_scene(MockScene2({}))

    # 测试路由
    print("\n测试1：路由到验证场景")
    scene1 = manager.route("验证模块A的时序")
    print(f"路由结果: {scene1.name if scene1 else 'None'}")

    print("\n测试2：路由到报告场景")
    scene2 = manager.route("生成设计报告")
    print(f"路由结果: {scene2.name if scene2 else 'None'}")

    print("\n测试3：无法路由")
    scene3 = manager.route("今天天气怎么样")
    print(f"路由结果: {scene3.name if scene3 else 'None'}")

    # 测试列出场景
    print("\n测试4：列出所有场景")
    scenes_list = manager.list_scenes()
    for scene_info in scenes_list:
        print(f"  - {scene_info['name']}: {scene_info['description']}")

    print("\n测试完成")
