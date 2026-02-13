"""EDA Agent System - 主入口

新的架构实现，支持：
- 多场景管理
- 人机协作交互
- 基础服务可复用
"""
import sys
import os

# 添加 src 到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

import argparse
from config import Config
from controller import Controller


def create_services():
    """创建所有服务实例

    Returns:
        服务字典
    """
    from services.state_service import StateService
    from services.llm_service import LLMService
    from services.rag_service import RAGService
    from services.eda_service import EDAService

    # 创建服务实例
    services = {}

    # State Service
    services["state"] = StateService(state_file=Config.STATE_FILE)

    # LLM Service
    llm_kwargs = {}
    if Config.LLM_PROVIDER == "claude":
        llm_kwargs["api_key"] = Config.ANTHROPIC_API_KEY
        llm_kwargs["base_url"] = Config.LLM_BASE_URL
    elif Config.LLM_PROVIDER == "qwen":
        llm_kwargs["api_key"] = Config.QWEN_API_KEY
        llm_kwargs["base_url"] = Config.LLM_BASE_URL

    services["llm"] = LLMService(
        client_type=Config.LLM_PROVIDER,
        model=Config.LLM_MODEL,
        **llm_kwargs
    )

    # RAG Service
    services["rag"] = RAGService()

    # EDA Service
    services["eda"] = EDAService()

    return services


def create_scene_manager(services):
    """创建场景管理器并注册所有场景

    Args:
        services: 服务字典

    Returns:
        SceneManager 实例
    """
    from scene_manager import SceneManager
    from scenes.verify import VerifyScene
    from scenes.report import ReportScene

    # 创建场景管理器
    manager = SceneManager(services)

    # 注册场景
    manager.register_scene(VerifyScene(services))
    manager.register_scene(ReportScene(services))

    return manager


def print_welcome():
    """打印欢迎信息"""
    print("\n" + "=" * 70)
    print(" EDA Agent 系统启动 ".center(70))
    print("=" * 70)
    print()
    print("我是 EDA 设计助手，可以帮您：")
    print("  ✓ 验证模块是否达到设计目标")
    print("  ✓ 查询设计规范和知识")
    print("  ✓ 运行仿真获取实际指标")
    print("  ✓ 生成设计验证报告")
    print()
    print("使用示例：")
    print("  你：验证模块A的时序是否<10ns")
    print("  你：查询模块B的设计规范")
    print("  你：生成验证报告")
    print()
    print("命令：")
    print("  帮助/help    - 显示帮助信息")
    print("  场景/scenes   - 列出所有场景")
    print("  退出/quit/q - 退出系统")
    print()
    print("=" * 70)


def print_help(manager):
    """打印帮助信息

    Args:
        manager: 场景管理器
    """
    print("\n" + "-" * 70)
    print("可用命令和场景：")
    print()

    print("命令：")
    print("  帮助/help    - 显示此帮助")
    print("  场景/scenes   - 列出所有可用场景")
    print("  退出/quit/q   - 退出系统")
    print()

    print("可用场景：")
    scenes_list = manager.list_scenes()
    for scene_info in scenes_list:
        keywords = ', '.join(scene_info['keywords'])
        print(f"  - {scene_info['name']}: {scene_info['description']}")
        print(f"    触发词: {keywords}")
    print()
    print("使用示例：")
    print("  你：验证模块A的时序<10ns")
    print("  你：查询模块B的设计规范")
    print("  你：生成验证报告")
    print("-" * 70)


def run_interactive_mode(manager, controller, auto_confirm=False):
    """运行交互模式

    Args:
        manager: 场景管理器
        controller: 交互控制器
        auto_confirm: 是否自动确认所有提示
    """
    print("\n准备就绪！请开始提问...\n")

    while True:
        try:
            # 获取用户输入
            user_input = input("你： ").strip()

            # 跳过空输入
            if not user_input:
                continue

            # 处理命令
            lower_input = user_input.lower()

            # 退出命令
            if lower_input in ['exit', '退出', 'quit', 'q']:
                print("\n" + "=" * 70)
                print("感谢使用 EDA Agent 系统！再见！")
                print("=" * 70)
                print()
                break

            # 帮助命令
            elif lower_input in ['help', '帮助']:
                print_help(manager)
                continue

            # 列出场景命令
            elif lower_input in ['scenes', '场景']:
                print("\n已注册的场景：")
                scenes_list = manager.list_scenes()
                for scene_info in scenes_list:
                    print(f"  - {scene_info['name']}: {scene_info['description']}")
                continue

            # 普通输入：路由到场景并执行
            else:
                scene = manager.route(user_input)

                if scene:
                    # 执行场景
                    scene_generator = scene.run(user_input)
                    result = controller.execute_scene(scene_generator, auto_confirm=auto_confirm)

                    # 显示结果
                    if result.get("status") == "DONE":
                        print(f"\n✓ {scene.name} 执行完成！")
                    elif result.get("status") == "ERROR":
                        print(f"\n✗ 执行出错：{result.get('message', '未知错误')}")
                else:
                    print(f"\n[系统] 抱歉，我没有理解您的需求。")
                    print("提示：输入'帮助'查看可用场景和示例")

        except KeyboardInterrupt:
            print("\n\n检测到中断信号 (Ctrl+C)")
            print("输入'退出'或'q'正常退出\n")

        except Exception as e:
            print(f"\n[错误] {str(e)}\n")


def main():
    """主函数"""
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="EDA Agent 系统 - 新架构")
    parser.add_argument(
        '--llm',
        type=str,
        default=Config.LLM_PROVIDER,
        choices=['mock', 'claude', 'qwen'],
        help='选择 LLM 提供商（默认从配置或环境变量读取）'
    )
    parser.add_argument(
        '--auto-confirm',
        action='store_true',
        help='自动确认所有提示（用于测试）'
    )

    args = parser.parse_args()

    # 更新配置
    Config.LLM_PROVIDER = args.llm

    # 打印欢迎信息
    print_welcome()

    # 打印配置
    Config.print_config()

    # 验证配置
    if not Config.validate():
        print("[主程序] 配置验证失败，使用 mock 模式继续运行")
        Config.LLM_PROVIDER = "mock"

    # 创建服务
    print("[主程序] 正在初始化服务...")
    services = create_services()

    # 创建场景管理器
    print("[主程序] 正在加载场景...")
    scene_manager = create_scene_manager(services)

    # 创建控制器
    controller = Controller()

    # 运行交互模式
    print("[主程序] 初始化完成！\n")
    run_interactive_mode(scene_manager, controller, auto_confirm=args.auto_confirm)


if __name__ == "__main__":
    main()
