"""
主入口文件 - 通用自动化 Agent

演示多轮对话、工具执行和会话持久化
使用智谱 API (Claude API 兼容)
支持从 Markdown 文件加载 Agent 定义
"""
import asyncio
import sys
from pathlib import Path
from datetime import datetime

from config.settings import config
from services.conversation_manager import ConversationManager
from tools.process_tools import (
    start_process, stop_process,
    list_processes, get_process_status
)


async def tool_executor(tool_name: str, tool_input: dict) -> dict:
    """
    执行工具并返回结果

    由 ConversationManager 在需要时调用

    Args:
        tool_name: 工具名称
        tool_input: 工具输入参数

    Returns:
        工具执行结果字典
    """
    # 工具映射
    tool_map = {
        "start_process": start_process,
        "stop_process": stop_process,
        "list_processes": list_processes,
        "get_process_status": get_process_status,
        # 兼容带前缀的名称
        "mcp__process_tools__start_process": start_process,
        "mcp__process_tools__stop_process": stop_process,
        "mcp__process_tools__list_processes": list_processes,
        "mcp__process_tools__get_process_status": get_process_status,
    }

    # 提取基础工具名称
    base_name = tool_name.split("__")[-1] if "__" in tool_name else tool_name

    tool_func = tool_map.get(tool_name) or tool_map.get(base_name)

    if not tool_func:
        return {
            "status": "error",
            "error": f"未知工具: {tool_name}"
        }

    try:
        return await tool_func(tool_input)
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }


async def interactive_conversation():
    """交互式对话循环"""
    # 验证配置
    try:
        config.validate()
    except ValueError as e:
        print(f"配置错误: {e}")
        print("请确保 .env 文件中已设置 ANTHROPIC_API_KEY")
        return

    # 检查 Agent 定义文件
    agent_file = Path(".claude/agents/general_agent.md")
    if not agent_file.exists():
        print(f"⚠ 警告: Agent 定义文件不存在: {agent_file}")
        print("将使用默认 Agent prompt")

    # 创建对话管理器（自动从 .md 文件加载 Agent prompt）
    manager = ConversationManager(
        agent_name="general_agent",
        tools_callback=tool_executor
    )

    # 生成会话 ID
    session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    # 启动对话
    manager.start_conversation(
        session_id=session_id,
        initial_context={
            "user": "User",
            "session_type": "interactive"
        }
    )

    print("=" * 70)
    print("通用自动化 Agent - 交互模式")
    print("=" * 70)
    print(f"会话 ID: {session_id}")
    print(f"模型: {config.llm.model}")
    print(f"Agent: {manager.agent_name}")
    print("可用命令: /sessions (列出所有会话), /quit (退出)")
    print("输入消息开始对话\n")

    # 主对话循环
    try:
        while True:
            user_input = input("You: ").strip()

            if not user_input:
                continue

            # 处理特殊命令
            if user_input.lower() in ['/quit', '/exit', 'quit', 'exit']:
                print("\n再见！")
                break

            if user_input.lower() == '/sessions':
                sessions = manager.list_sessions()
                print(f"\n已保存的会话: {len(sessions)}")
                for s in sessions:
                    print(f"  - {s}")
                print()
                continue

            # 处理对话轮次
            print("\nAgent: ", end="", flush=True)

            try:
                async for event in manager.process_turn(
                    session_id,
                    user_input,
                ):
                    if event["type"] == "text":
                        print(event["content"], end="", flush=True)
                    elif event["type"] == "tool_use":
                        # 显示工具调用（带颜色和图标）
                        print(f"\n\n🔧 [调用工具: {event['tool_name']}]", end="", flush=True)
                    elif event["type"] == "tool_result":
                        # 显示工具结果（简洁）
                        result = event['result']
                        if result.startswith('✓') or '成功' in result or '启动' in result:
                            print(f" ✅", end="", flush=True)
                        elif result.startswith('✗') or '错误' in result or '失败' in result:
                            print(f" ❌", end="", flush=True)
                        else:
                            print(f" {result}", end="", flush=True)
                    elif event["type"] == "error":
                        print(f"\n❌ 错误: {event['error']}")

                print()  # 换行

            except Exception as e:
                print(f"\n发生错误: {e}")
                import traceback
                traceback.print_exc()

    except KeyboardInterrupt:
        print("\n\n用户中断")
    finally:
        # 清理
        manager.end_conversation(session_id)
        await manager.close()


async def resume_session(session_id: str):
    """
    恢复现有会话

    Args:
        session_id: 要恢复的会话 ID
    """
    # 验证配置
    try:
        config.validate()
    except ValueError as e:
        print(f"配置错误: {e}")
        return

    manager = ConversationManager(
        agent_name="general_agent",
        tools_callback=tool_executor
    )

    manager.start_conversation(
        session_id=session_id
    )

    print(f"✓ 已恢复会话: {session_id}\n")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ['/quit', '/exit', 'quit']:
            break

        if not user_input:
            continue

        print("\nAgent: ", end="", flush=True)
        try:
            async for event in manager.process_turn(
                session_id,
                user_input,
            ):
                if event["type"] == "text":
                    print(event["content"], end="", flush=True)
                elif event["type"] == "tool_use":
                    print(f"\n\n🔧 [调用工具: {event['tool_name']}]", end="", flush=True)
                elif event["type"] == "tool_result":
                    result = event['result']
                    if result.startswith('✓') or '成功' in result or '启动' in result:
                        print(f" ✅", end="", flush=True)
                    elif result.startswith('✗') or '错误' in result or '失败' in result:
                        print(f" ❌", end="", flush=True)
                    else:
                        print(f" {result}", end="", flush=True)
                elif event["type"] == "error":
                    print(f"\n❌ 错误: {event['error']}")
            print()
        except Exception as e:
            print(f"\n发生错误: {e}")

    manager.end_conversation(session_id)
    await manager.close()


def main():
    """主入口"""
    if len(sys.argv) > 1:
        if sys.argv[1] == "resume" and len(sys.argv) > 2:
            # 恢复指定会话
            asyncio.run(resume_session(sys.argv[2]))
        elif sys.argv[1] == "list":
            # 列出所有会话
            session_dir = Path(config.session.session_dir)
            if session_dir.exists():
                sessions = [f.stem for f in session_dir.glob("*.json")]
                print(f"已保存的会话 ({len(sessions)}):")
                for s in sessions:
                    print(f"  - {s}")
            else:
                print("没有找到已保存的会话")
        else:
            print("用法:")
            print("  python main.py              # 启动新会话")
            print("  python main.py list         # 列出所有会话")
            print("  python main.py resume <id>  # 恢复指定会话")
    else:
        # 启动新会话
        asyncio.run(interactive_conversation())


if __name__ == "__main__":
    main()
