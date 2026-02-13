"""EDA Agent - 交互式主程序

用户选择场景 → 输入任务 → LLM 规划执行步骤 → 完成
"""
import sys
import os

# 添加 src 到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from interactive_scene_manager import InteractiveSceneManager, show_scene_menu, select_scene
from controller import Controller
from services.llm_service import LLMService
from services.rag_service import RAGService
from services.eda_service import EDAService
from services.state_service import StateService


def create_services():
    """创建所有服务实例"""
    services = {}

    # LLM Service
    services["llm"] = LLMService(client_type="mock")

    # RAG Service
    services["rag"] = RAGService()

    # EDA Service
    services["eda"] = EDAService()

    # State Service
    services["state"] = StateService()

    return services


def main():
    """主程序"""
    print("\n" + "=" * 70)
    print("EDA Agent 系统启动".center(70))
    print("=" * 70)

    # 创建服务
    print("[主程序] 正在初始化服务...")
    services = create_services()

    # 创建场景管理器
    print("[主程序] 正在加载场景...")
    manager = InteractiveSceneManager(services)

    # 注册所有场景
    print("[主程序] 注册场景...")

    # 导入场景
    from scenes.verify_simple import VerifyScene
    from scenes.report_simple import ReportScene

    manager.register_scene(VerifyScene(services))
    manager.register_scene(ReportScene(services))

    # 创建控制器
    controller = Controller()

    # 主循环
    while True:
        try:
            # 显示场景菜单
            show_scene_menu(manager)

            # 获取用户输入
            user_input = input("\n你： ").strip()

            # 空输入，继续
            if not user_input:
                continue

            # 退出命令
            if user_input.lower() in ['q', 'quit', 'exit', '退出', 'q']:
                print("\n" + "=" * 70)
                print("感谢使用 EDA Agent 系统！再见！")
                print("=" * 70 + "\n")
                break

            # 帮助命令
            if user_input.lower() in ['help', '帮助', 'h']:
                print("\n帮助信息：")
                print("  输入场景编号或名称选择场景")
                print("  输入 'q' 退出系统")
                print("  输入 'scenes' 查看所有场景")
                continue

            # 列出场景命令
            if user_input.lower() in ['scenes', '场景']:
                print("\n可用场景：")
                for scene_info in manager.list_scenes():
                    print(f"  {scene_info['index']}. {scene_info['name']}")
                    print()
                continue

            # 尝试选择场景
            scene = select_scene(manager, user_input)

            if scene:
                # 进入场景，处理任务
                print(f"\n{'─' * 70}")
                print(f"进入场景：{scene.name}")
                print(f"{'─' * 70}")

                print("\n请输入任务描述（或 'q' 返回到主菜单）：")
                print("提示：输入如 '验证模块A的时序<10ns'")

                # 场景内循环
                while True:
                    task_input = input(f"[{scene.name}] > ").strip()

                    if not task_input:
                        continue

                    if task_input.lower() == 'q':
                        print(f"\n退出场景：{scene.name}")
                        break

                    # 执行场景
                    result = controller.execute_scene(
                        scene.run(task_input),
                        auto_confirm=True  # 自动确认，简化交互
                    )

                    status = result.get("status", "UNKNOWN")
                    if status == "DONE":
                        print(f"\n✓ {scene.name} 执行完成")
                    elif status == "ERROR":
                        print(f"\n✗ 执行出错：{result.get('message', '未知错误')}")
                    else:
                        print(f"\n⚠️ 执行状态：{status}")

                    # 询问是否继续
                    print(f"\n[{scene.name}] 继续处理任务？(y/n/q)")

                    continue_input = input(f"[{scene.name}] > ").strip().lower()

                    if continue_input in ['y', 'yes', '是', '']:
                        continue  # 继续循环
                    else:
                        print(f"\n退出场景：{scene.name}")
                        break  # 退出场景循环

        except KeyboardInterrupt:
            print("\n\n检测到中断信号 (Ctrl+C)")
            print("输入 'q' 正常退出\n")
        except Exception as e:
            print(f"\n[错误] {str(e)}\n")


if __name__ == "__main__":
    main()
