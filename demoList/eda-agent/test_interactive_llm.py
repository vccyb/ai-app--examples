"""测试交互式场景选择 + LLM 规划"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from interactive_scene_manager import InteractiveSceneManager, show_scene_menu, select_scene
from scenes.llm_agent_scene import LLMAgentScene
from controller import Controller
from services.llm_service import LLMService
from services.rag_service import RAGService
from services.eda_service import EDAService
from services.state_service import StateService


def interactive_demo():
    """演示交互式场景选择和 LLM 规划"""
    print("=" * 70)
    print("交互式场景选择 + LLM 规划演示")
    print("=" * 70)

    print("\n新架构流程：")
    print("  1. 启动系统")
    print("  2. 显示所有可用场景")
    print("  3. 用户选择场景（输入编号或名称）")
    print("  4. 进入场景后，用户输入任务")
    print("  5. LLM 分析任务，生成执行步骤")
    print("  6. 场景按步骤调用服务")
    print("  7. 返回结果")

    # 创建服务
    print("\n创建服务...")
    services = {}
    services["llm"] = LLMService(client_type="mock")
    services["rag"] = RAGService()
    services["eda"] = EDAService()
    services["state"] = StateService()

    # 创建交互式场景管理器
    print("\n创建场景管理器...")
    manager = InteractiveSceneManager(services)

    # 注册场景
    print("\n注册场景...")
    manager.register_scene(LLMAgentScene(services))

    # 创建控制器
    controller = Controller()

    # 显示场景菜单
    show_scene_menu(manager)

    # 模拟用户选择场景
    print("\n" + "─" * 70)
    print("模拟用户交互")
    print("─" * 70)

    # 步骤1：用户选择场景
    print("\n[步骤 1] 用户选择场景")
    print("你：1")

    scene = select_scene(manager, "1")

    if not scene:
        print("用户取消选择")
        return

    # 步骤2：用户输入任务
    print("\n[步骤 2] 用户在场景内输入任务")
    task_input = "验证模块A的时序是否小于10ns"
    print(f"你：{task_input}")

    # 步骤3：场景执行（LLM 生成计划并执行）
    print("\n[步骤 3] 场景处理（LLM 生成执行计划）")

    result = controller.execute_scene(
        scene.run(task_input),
        auto_confirm=True
    )

    print(f"\n执行结果: {result.get('status')}")


if __name__ == "__main__":
    interactive_demo()
