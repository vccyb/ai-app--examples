#!/usr/bin/env python3
"""EDA Agent 简单启动

直接运行即可，会从 .env 读取 API Key
"""
import sys
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 添加 src 到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.conversation_manager import ConversationManager


def main():
    """主函数"""
    # 检查 API Key
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("错误：请在 .env 文件中设置 ANTHROPIC_API_KEY")
        print("示例：ANTHROPIC_API_KEY=sk-ant-xxxxx")
        return

    # 读取配置
    base_url = os.getenv("BASE_URL")  # 智谱等兼容接口
    model = os.getenv("MODEL", "claude-sonnet-4-5")  # 默认用 Claude

    # 创建会话管理器
    print(f"🚀 正在连接 EDA Agent 系统...")
    print(f"   模型: {model}")
    if base_url:
        print(f"   端点: {base_url}")

    conv = ConversationManager(
        llm_client_type="claude",
        api_key=api_key,
        base_url=base_url,
        model=model
    )

    print("\n" + "=" * 60)
    print(" EDA Agent - 智能设计助手".center(60))
    print("=" * 60)
    print("\n我可以帮您：")
    print("  • 查询设计规范")
    print("  • 运行仿真")
    print("  • 评判结果")
    print("  • 优化设计")
    print("\n直接输入你的需求即可，输入 'q' 退出\n")

    # 对话循环
    while True:
        try:
            user_input = input("你： ").strip()

            if not user_input:
                continue

            if user_input.lower() in ['q', '退出', 'exit', 'quit']:
                print("\n再见！👋")
                break

            # 处理用户输入
            conv.add_user_message(user_input)

            # 运行对话
            print("\n助手：", end="", flush=True)
            conv.run_conversation(max_turns=5)

            # 提取并显示响应
            messages = conv.get_conversation_history()
            for msg in reversed(messages):
                if msg.get("role") == "assistant":
                    for block in msg.get("content", []):
                        if hasattr(block, 'text'):
                            print(block.text)
                    break

            print()

        except KeyboardInterrupt:
            print("\n\n再见！👋")
            break
        except Exception as e:
            print(f"\n错误：{e}\n")


if __name__ == "__main__":
    main()
