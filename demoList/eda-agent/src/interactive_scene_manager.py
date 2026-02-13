"""交互式场景管理器 - 用户主动选择场景

不再是 LLM 预测场景，而是：
1. 启动时列出所有可用场景
2. 用户选择场景（输入数字或名称）
3. 进入场景后，用户输入任务
4. LLM 生成执行计划
5. 场景执行计划
"""
from typing import Dict, List, Optional


class InteractiveSceneManager:
    """交互式场景管理器

    管理场景注册和用户选择
    """

    def __init__(self, services: Dict):
        """初始化场景管理器

        Args:
            services: 服务字典
        """
        self.services = services
        self.scenes: List = []

    def register_scene(self, scene) -> None:
        """注册场景"""
        self.scenes.append(scene)
        print(f"[SceneManager] 注册场景: {scene.name} - {scene.description}")

    def list_scenes(self) -> List[Dict]:
        """列出所有场景（用于显示给用户）"""
        return [
            {
                "index": i + 1,
                "name": scene.name,
                "description": scene.description
            }
            for i, scene in enumerate(self.scenes)
        ]

    def get_scene_by_index(self, index: int):
        """通过索引获取场景"""
        if 1 <= index <= len(self.scenes):
            return self.scenes[index - 1]
        return None

    def get_scene_by_name(self, name: str):
        """通过名称获取场景"""
        for scene in self.scenes:
            if scene.name == name:
                return scene
        return None


def show_scene_menu(manager: InteractiveSceneManager) -> None:
    """显示场景菜单"""
    print("\n" + "=" * 70)
    print("可用场景".center(70))
    print("=" * 70)

    scenes = manager.list_scenes()
    for scene_info in scenes:
        print(f"  {scene_info['index']}. {scene_info['name']}")
        print(f"     {scene_info['description']}")
        print()

    print("=" * 70)
    print("提示：输入场景编号或名称选择场景")
    print("      输入 'q' 退出")
    print("=" * 70)


def select_scene(manager: InteractiveSceneManager, user_input: str):
    """让用户选择场景

    Args:
        manager: 场景管理器
        user_input: 用户输入

    Returns:
        选中的场景，如果退出返回 None
    """
    user_input = user_input.strip()

    # 退出命令
    if user_input.lower() in ['q', 'quit', 'exit', '退出']:
        return None

    # 尝试按索引选择
    try:
        index = int(user_input)
        scene = manager.get_scene_by_index(index)
        if scene:
            print(f"\n✓ 已选择场景: {scene.name}")
            return scene
        else:
            print(f"\n✗ 无效的场景编号: {index}")
            return None
    except ValueError:
        pass

    # 尝试按名称选择
    scene = manager.get_scene_by_name(user_input.lower())
    if scene:
        print(f"\n✓ 已选择场景: {scene.name}")
        return scene
    else:
        print(f"\n✗ 未找到场景: {user_input}")
        return None


# ============================================================================
# 使用示例
# ============================================================================

if __name__ == "__main__":
    from scenes.base import BaseScene
    from typing import Generator

    # 创建两个示例场景
    class MockVerifyScene(BaseScene):
        def __init__(self, services):
            super().__init__(
                name="verify",
                description="验证模块是否达到设计目标",
                keywords=[],
                services=services
            )

        def match(self, user_input: str) -> float:
            return 0.0  # 不需要

        def run(self, user_input: str) -> Generator:
            yield {"type": "info", "content": f"执行验证场景，输入: {user_input}"}

    class MockReportScene(BaseScene):
        def __init__(self, services):
            super().__init__(
                name="report",
                description="生成和导出设计报告",
                keywords=[],
                services=services
            )

        def match(self, user_input: str) -> float:
            return 0.0

        def run(self, user_input: str) -> Generator:
            yield {"type": "info", "content": f"执行报告场景，输入: {user_input}"}

    # 创建管理器
    services = {}
    manager = InteractiveSceneManager(services)
    manager.register_scene(MockVerifyScene(services))
    manager.register_scene(MockReportScene(services))

    # 模拟交互流程
    print("\n" + "=" * 70)
    print("交互式场景选择演示")
    print("=" * 70)

    # 步骤1：显示场景菜单
    show_scene_menu(manager)

    # 步骤2：用户选择场景
    print("\n请选择场景（输入 1 或 2）：")

    # 模拟用户输入 "1"
    scene = select_scene(manager, "1")

    if scene:
        # 步骤3：用户在场景内输入任务
        print(f"\n已进入场景: {scene.name}")
        print("请输入任务描述（或 'q' 退出）：")

        # 模拟用户输入任务
        task_input = "验证模块A的时序<10ns"
        print(f"你的输入: {task_input}")

        # 步骤4：场景处理任务
        # 这里会调用 LLM 生成执行计划，然后执行
        for msg in scene.run(task_input):
            print(f"[场景输出] {msg}")

    print("\n演示完成")
