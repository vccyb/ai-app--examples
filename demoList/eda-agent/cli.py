"""EDA Agent系统 - 交互式命令行界面

最简单的交互方式：用户输入指令 → 查看结果 → 继续下一条
"""
import sys
import os

# 添加src到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.agents.master_agent import MasterAgent


class EDARepl:
    """简单的REPL（Read-Eval-Print Loop）交互界面"""

    def __init__(self):
        """初始化"""
        self.master_agent = MasterAgent()
        self.history = []  # 对话历史

        print("=" * 70)
        print("🤖 EDA Agent系统 - 交互式界面")
        print("提示: 输入'帮助'查看命令，或直接输入EDA指令")
        print("=" * 70)
        print()

    def show_help(self):
        """显示帮助信息"""
        print("""
📋 可用命令:
  帮助          - 显示此帮助信息
  退出/quit/q  - 退出系统

🎯 使用示例:
  优化模块A时序<10ns
  查询模块A的设计规范
  仿真模块C，目标功耗<60mW
  帮助

💡 提示: 输入EDA指令后按回车查看结果
        """)

    def run(self, user_input: str):
        """执行用户指令"""
        print(f"\n🔄 正在处理: {user_input}")

        # 调用Master Agent
        result = self.master_agent.process(user_input)

        # 保存到历史
        self.history.append({
            "user_input": user_input,
            "result": result
        })

        # 显示结果
        self.display_result(result)

        # 提示继续
        print("\n" + "-" * 70)
        print("💡 继续对话: 输入下一条EDA指令，或'退出'结束")
        print()

    def display_result(self, result: dict):
        """格式化显示结果"""
        print("\n📊 处理结果")
        print(f"状态: {result.get('status', 'N/A')}")

        # 显示仿真结果
        if 'simulation' in result:
            sim = result['simulation']
            print(f"\n📈 仿真数据:")
            print(f"  模块: {sim.get('module', 'N/A')}")
            if 'metrics' in sim:
                for metric, value in sim['metrics'].items():
                    print(f"  {metric}: {value}")

        # 显示评判结果
        if 'evaluation' in result:
            eval = result['evaluation']
            print(f"\n⚖️  评判结果:")
            print(f"  状态: {eval.get('status', 'N/A')}")
            if eval.get('reason'):
                print(f"  原因: {eval.get('reason', 'N/A')}")
            if eval.get('suggestion'):
                print(f"  建议: {eval.get('suggestion', 'N/A')}")

        print("\n" + "=" * 70)

    def show_history(self):
        """显示对话历史"""
        if not self.history:
            print("📭 暂无对话历史")
            return

        print("\n📜 对话历史 (最近5条):")
        print("-" * 70)

        for i, item in enumerate(reversed(self.history[-5:])):
            print(f"\n[{i+1}] 用户: {item['user_input']}")
            if 'result' in item:
                result = item['result']
                status = result.get('status', 'N/A')
                status_icon = "✅" if status == "success" else "❌"
                print(f"  状态: {status_icon} {status}")

        print("=" * 70)
        print()


def main():
    """主入口"""
    # 创建REPL实例
    repl = EDARepl()

    print("🚀 EDA Agent系统启动成功！")
    print(f"Python版本: {sys.version}")
    print(f"工作目录: {os.getcwd()}")
    print("=" * 70)
    print()

    # 主循环
    while True:
        try:
            # 获取用户输入
            user_input = input("\n🎯 EDA > ").strip()

            # 处理退出命令
            if user_input.lower() in ['exit', 'quit', 'q']:
                print("\n👋 再见！感谢使用EDA Agent系统！")
                break

            # 处理帮助命令
            elif user_input.lower() == 'help':
                repl.show_help()
                continue

            # 处理历史查询
            elif user_input.lower() == 'history':
                repl.show_history()
                continue

            # 执行EDA指令
            else:
                repl.run(user_input)

        except KeyboardInterrupt:
            print("\n\n⚠️  检测到中断信号")
            print("💡 输入'exit'或'quit'正常退出")
            print()

        except Exception as e:
            print(f"\n❌ 错误: {str(e)}")
            continue


if __name__ == "__main__":
    main()
