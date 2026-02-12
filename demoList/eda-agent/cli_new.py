"""EDA Agent 系统 - 新一代交互式 CLI（LLM 驱动）

支持多轮对话、AI 自动判断调用工具
"""
import sys
import os

# 添加 src 到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.conversation_manager import ConversationManager


class EDAChatCLI:
    """EDA 对话式 CLI"""

    def __init__(self, llm_client_type: str = "mock"):
        """初始化 CLI

        Args:
            llm_client_type: LLM 客户端类型 ("mock", "claude", "qwen")
        """
        self.conv_manager = ConversationManager(llm_client_type=llm_client_type)
        self.conversation_count = 0

        self._print_welcome()

    def _print_welcome(self):
        """打印欢迎信息"""
        print("\n" + "=" * 70)
        print(" EDA Agent 系统 - 新一代对话式界面 ".center(70))
        print("=" * 70)
        print()
        print("我是一个专业的 EDA 设计助手，可以帮您：")
        print("  查询设计规范 | 运行仿真 | 评判结果 | 优化设计")
        print()
        print("使用示例：")
        print("  你：查询模块A的设计规范")
        print("  你：优化模块B的时序，目标小于10ns")
        print("  你：运行模块C的仿真")
        print("  你：查看之前的历史记录")
        print()
        print("命令：")
        print("  清空/clear  - 清除对话历史")
        print("  帮助/help    - 显示此帮助")
        print("  退出/quit/q - 退出系统")
        print()
        print("=" * 70)
        print()

    def show_help(self):
        """显示帮助信息"""
        print("\n" + "-" * 70)
        print("可用命令：")
        print("  清空/clear - 清除当前对话历史，重新开始")
        print("  帮助/help   - 显示帮助信息")
        print("  退出/quit/q - 退出系统")
        print()
        print("对话示例：")
        print("  你：查询模块A的时序要求")
        print("  你：优化模块B，功耗要小于50mW")
        print("  你：上次仿真的结果怎么样？")
        print("  你：帮我评判一下时序12ns是否达到目标10ns")
        print("-" * 70)
        print()

    def clear_conversation(self):
        """清空对话"""
        self.conv_manager.clear_history()
        self.conversation_count = 0
        print("\n对话历史已清空，可以重新开始了！\n")

    def process_user_input(self, user_input: str):
        """处理用户输入

        Args:
            user_input: 用户输入的文本
        """
        # 添加用户消息
        self.conv_manager.add_user_message(user_input)

        # 运行对话
        print("\n" + "-" * 70)
        print(f"[你] {user_input}")
        print("-" * 70)

        try:
            history = self.conv_manager.run_conversation(max_turns=5)
            self.conversation_count += 1
        except Exception as e:
            print(f"\n[错误] 处理请求时出错: {str(e)}")
            print("\n你可以：")
            print("  1. 重新描述你的需求")
            print("  2. 输入'清空'清除历史")
            print("  3. 输入'帮助'查看更多示例")

    def run(self):
        """运行主循环"""
        print("准备就绪！请开始提问...\n")

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
                    self.show_help()
                    continue

                # 清空命令
                elif lower_input in ['clear', '清空']:
                    self.clear_conversation()
                    continue

                # 普通对话输入
                else:
                    self.process_user_input(user_input)

            except KeyboardInterrupt:
                print("\n\n检测到中断信号 (Ctrl+C)")
                print("输入'退出'或'q'正常退出\n")

            except Exception as e:
                print(f"\n[错误] {str(e)}\n")


def main():
    """主入口"""
    import argparse

    parser = argparse.ArgumentParser(description="EDA Agent 系统 - LLM 驱动的对话式 CLI")
    parser.add_argument(
        '--llm',
        type=str,
        default='mock',
        choices=['mock', 'claude', 'qwen'],
        help='选择 LLM 客户端类型（默认: mock）'
    )
    parser.add_argument(
        '--api-key',
        type=str,
        help='API 密钥（根据选择的 LLM 类型，设置对应的环境变量或参数）'
    )

    args = parser.parse_args()

    # 创建 CLI 实例
    kwargs = {}
    if args.api_key:
        if args.llm == 'claude':
            kwargs['api_key'] = args.api_key
        elif args.llm == 'qwen':
            kwargs['api_key'] = args.api_key

    cli = EDAChatCLI(llm_client_type=args.llm, **kwargs)

    # 运行主循环
    cli.run()


if __name__ == "__main__":
    main()
