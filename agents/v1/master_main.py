"""
Master Agent 主入口 - 使用 Claude Agent SDK

符合 SDK 标准的实现：
- 使用 SDK 的 ClaudeSDKClient 接口（保持会话连续性）
- Skills 自动从文件系统加载
- 配置 setting_sources 和 allowed_tools
"""
import asyncio
import json
from dataclasses import asdict, is_dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional

from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions
from claude_agent_sdk import AssistantMessage, TextBlock

from config.settings import config
from tools.sdk_tools import eda_tools_server, himaqa_tools_server


def now_iso() -> str:
    """UTC ISO8601 时间戳"""
    return datetime.now(timezone.utc).isoformat()


def serialize_sdk_message(message: Any) -> Dict[str, Any]:
    """尽量保留 SDK 标准字段结构"""
    payload: Dict[str, Any] = {
        "timestamp": now_iso(),
        "message_class": type(message).__name__,
    }

    if hasattr(message, "type"):
        payload["type"] = getattr(message, "type")
    if hasattr(message, "subtype"):
        payload["subtype"] = getattr(message, "subtype")
    if hasattr(message, "session_id"):
        payload["session_id"] = getattr(message, "session_id")

    if is_dataclass(message):
        payload["data"] = asdict(message)
    else:
        payload["data"] = str(message)

    return payload


def extract_session_id(message_payload: Dict[str, Any]) -> Optional[str]:
    """从 SDK message payload 中提取 session_id"""
    session_id = message_payload.get("session_id")
    if session_id:
        return session_id

    data = message_payload.get("data")
    if isinstance(data, dict):
        if data.get("session_id"):
            return data["session_id"]
        nested = data.get("data")
        if isinstance(nested, dict) and nested.get("session_id"):
            return nested["session_id"]

    return None


async def main():
    """主入口函数"""
    # 验证配置
    try:
        config.validate()
    except ValueError as e:
        print(f"配置错误: {e}")
        print("请确保 .env 文件中已设置 ANTHROPIC_API_KEY")
        return

    print("=" * 70)
    print("Master Agent - EDA & HimaQA 统一入口")
    print("=" * 70)
    print(f"模型: {config.llm.model}")
    print(f"工作目录: {Path.cwd()}")
    print("\n可用功能:")
    print("  EDA 设计:")
    print("    - 创建项目、添加元件、连接电路")
    print("    - 运行仿真、导出网表")
    print("  HimaQA 平台:")
    print("    - 上传网表、通知经理")
    print("    - 查询历史、获取报告")
    print("\nSkills 会根据上下文自动调用")
    print("输入消息开始对话，输入 quit 退出\n")

    # SDK 配置
    options = ClaudeAgentOptions(
        cwd=str(Path.cwd()),  # 项目根目录
        # NOTE: user source may include incompatible local settings that
        # can block MCP initialization; project source is enough for this repo.
        setting_sources=["project"],  # 从项目目录加载 Skills
        allowed_tools=[
            "Skill",  # 启用 Skills
            "Read",   # 读取文件
            # 显式放开全部 MCP 工具，避免重复权限阻塞
            "mcp__eda-tools__eda_create_project",
            "mcp__eda-tools__eda_add_component",
            "mcp__eda-tools__eda_connect",
            "mcp__eda-tools__eda_simulate",
            "mcp__eda-tools__eda_export",
            "mcp__himaqa-tools__himaqa_upload_netlist",
            "mcp__himaqa-tools__himaqa_notify_manager",
            "mcp__himaqa-tools__himaqa_query_history",
            "mcp__himaqa-tools__himaqa_get_report",
        ],
        disallowed_tools=[
            "Bash",
            "Write",
            "Edit",
            "AskUserQuestion",
        ],
        # 注册自定义工具的 MCP 服务器
        mcp_servers={
            "eda-tools": eda_tools_server,
            "himaqa-tools": himaqa_tools_server,
        },
    )

    # 使用 ClaudeSDKClient 保持会话连续性
    try:
        client_cm = ClaudeSDKClient(options=options)
        await client_cm.connect()
    except Exception as e:
        print(f"\n❌ Agent 初始化失败: {e}")
        print("建议检查 ~/.claude 下的用户级设置，或仅使用 project setting source。")
        return

    async with client_cm as client:
        session_dir = Path(config.session.session_dir)
        session_dir.mkdir(parents=True, exist_ok=True)
        session_file: Optional[Path] = None
        session_data: Dict[str, Any] = {
            "format": "claude-agent-sdk-session-v1",
            "created_at": now_iso(),
            "updated_at": now_iso(),
            "model": config.llm.model,
            "cwd": str(Path.cwd()),
            "events": [],
        }

        def persist_session() -> None:
            if not session_file:
                return
            session_data["updated_at"] = now_iso()
            session_file.write_text(
                json.dumps(session_data, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )

        def append_event(event: Dict[str, Any]) -> None:
            session_data["events"].append(event)
            persist_session()

        print("✓ Agent 已启动")
        print("You: ", end="", flush=True)

        # 主对话循环
        try:
            while True:
                user_input = input().strip()

                if not user_input:
                    continue

                # 处理特殊命令
                if user_input.lower() in ['quit', 'exit', '/quit', '/exit']:
                    print("\n👋 再见！")
                    break

                # 发送请求
                print("Agent: ", end="", flush=True)
                append_event({
                    "timestamp": now_iso(),
                    "message_class": "UserInput",
                    "data": {"text": user_input},
                })
                await client.query(user_input)

                # 接收响应
                async for message in client.receive_response():
                    message_payload = serialize_sdk_message(message)
                    sid = extract_session_id(message_payload)
                    if sid and not session_file:
                        session_data["session_id"] = sid
                        session_file = session_dir / f"{sid}.json"
                        print(f"\n📁 Session 已保存: {session_file}", flush=True)
                    append_event(message_payload)

                    # 处理不同类型的消息
                    if isinstance(message, AssistantMessage):
                        for block in message.content:
                            if isinstance(block, TextBlock):
                                print(block.text, end="", flush=True)
                            elif hasattr(block, 'name'):
                                # 工具调用
                                print(f"\n\n🔧 [{block.name}]", end="", flush=True)
                    elif hasattr(message, 'type'):
                        if message.type == "tool_result":
                            result = message.content if hasattr(message, 'content') else ""
                            if result and ("✓" in result or "成功" in result or "已" in result):
                                print(" ✓", end="", flush=True)
                            elif result and ("✗" in result or "错误" in result or "失败" in result):
                                print(" ✗", end="", flush=True)
                        elif message.type == "error":
                            print(f"\n❌ 错误: {message.content}")

                print()  # 换行
                print("You: ", end="", flush=True)

        except KeyboardInterrupt:
            print("\n\n用户中断")


if __name__ == "__main__":
    asyncio.run(main())
