"""
多轮对话管理器（含持久化）

使用 Anthropic SDK 管理对话，支持智谱 API
支持从 Markdown 文件加载 Agent prompt
"""
import asyncio
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, AsyncIterator, List, Dict
from dataclasses import dataclass, field, asdict

from anthropic import AsyncAnthropic

from config.settings import config
from utils.agent_loader import load_agent_prompt
from tools.process_tools import get_tool_definitions


def _sanitize_for_json(obj):
    """
    清理对象中的非法 Unicode 字符（如孤立的代理项对）

    这可以防止 JSON 序列化时出现 UnicodeEncodeError
    """
    if isinstance(obj, str):
        # 移除或替换孤立的 UTF-16 代理项
        try:
            # 先尝试编码，如果失败则清理
            obj.encode('utf-8')
            return obj
        except UnicodeEncodeError:
            # 移除代理项范围内的字符
            return ''.join(
                c for c in obj
                if not (0xD800 <= ord(c) <= 0xDFFF)
            )
    elif isinstance(obj, dict):
        return {k: _sanitize_for_json(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [_sanitize_for_json(item) for item in obj]
    else:
        return obj


@dataclass
class Message:
    """单条消息"""
    role: str  # "user" or "assistant"
    content: str
    timestamp: str
    tool_calls: List[Dict] = field(default_factory=list)


@dataclass
class ConversationSession:
    """对话会话"""
    session_id: str
    agent_name: str
    started_at: str
    messages: List[Message] = field(default_factory=list)
    context: Dict = field(default_factory=dict)

    def add_message(self, role: str, content: str, tool_calls: List[Dict] = None):
        """添加消息"""
        self.messages.append(Message(
            role=role,
            content=content,
            timestamp=datetime.now().isoformat(),
            tool_calls=tool_calls or []
        ))

    def to_dict(self):
        """转换为字典（用于序列化）"""
        return {
            "session_id": self.session_id,
            "agent_name": self.agent_name,
            "started_at": self.started_at,
            "messages": [asdict(msg) for msg in self.messages],
            "context": self.context
        }


class ConversationManager:
    """管理多轮对话（支持持久化 + Agent prompt 加载）"""

    def __init__(self, agent_name: str = "general_agent", tools_callback=None):
        """
        初始化对话管理器

        Args:
            agent_name: Agent 名称（从 .claude/agents/ 加载）
            tools_callback: 工具执行回调
        """
        self.agent_name = agent_name
        self.tools_callback = tools_callback
        self.sessions = {}  # session_id -> ConversationSession
        self.client = None
        self.session_dir = Path(config.session.session_dir)
        self.session_dir.mkdir(parents=True, exist_ok=True)

        # 从 .md 文件加载 Agent prompt
        self.agent_prompt = self._load_agent_prompt(agent_name)
        if not self.agent_prompt:
            print(f"⚠ 警告: 未找到 Agent '{agent_name}' 的定义，使用默认 prompt")
            self.agent_prompt = "你是一个有帮助的助手。"

    def _load_agent_prompt(self, agent_name: str) -> Optional[str]:
        """
        从 Markdown 文件加载 Agent prompt

        Args:
            agent_name: Agent 名称

        Returns:
            Agent prompt，如果未找到则返回 None
        """
        # 尝试从 .claude/agents/ 加载
        try:
            prompt = load_agent_prompt(agent_name)
            if prompt:
                print(f"✓ 已加载 Agent: {agent_name}")
                return prompt
        except Exception as e:
            print(f"⚠ 从 .claude/agents/ 加载失败: {e}")

        # 回退到 agents/ 目录
        try:
            agents_dir = Path("agents")
            for md_file in agents_dir.glob("**/*.md"):
                if md_file.stem == agent_name or md_file.parent.name == agent_name:
                    content = md_file.read_text(encoding='utf-8')

                    # 解析 YAML frontmatter
                    if content.startswith("---"):
                        parts = content.split("---", 2)
                        if len(parts) >= 3:
                            prompt = parts[2].strip()
                            print(f"✓ 从 {md_file} 加载 Agent: {agent_name}")
                            return prompt
                    else:
                        # 没有 frontmatter，整个文件是 prompt
                        print(f"✓ 从 {md_file} 加载 Agent: {agent_name}")
                        return content
        except Exception as e:
            print(f"⚠ 从 agents/ 加载失败: {e}")

        return None

    def _get_session_file(self, session_id: str) -> Path:
        """获取会话文件路径"""
        return self.session_dir / f"{session_id}.json"

    def _save_session(self, session: ConversationSession):
        """保存会话到文件"""
        session_file = self._get_session_file(session.session_id)
        with open(session_file, 'w', encoding='utf-8') as f:
            # 清理可能存在的非法 Unicode 字符
            session_dict = _sanitize_for_json(session.to_dict())
            json.dump(session_dict, f, ensure_ascii=False, indent=2)

    def _load_session(self, session_id: str) -> Optional[ConversationSession]:
        """从文件加载会话"""
        session_file = self._get_session_file(session_id)
        if not session_file.exists():
            return None

        with open(session_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # 重建 ConversationSession 对象
        session = ConversationSession(
            session_id=data['session_id'],
            agent_name=data['agent_name'],
            started_at=data['started_at'],
            context=data.get('context', {})
        )

        # 重建消息列表
        for msg_data in data.get('messages', []):
            msg = Message(**msg_data)
            session.messages.append(msg)

        return session

    def start_conversation(
        self,
        session_id: str,
        initial_context: Optional[dict] = None
    ) -> ConversationSession:
        """开始新对话或恢复现有对话"""
        # 尝试从文件加载现有会话
        session = self._load_session(session_id)

        if session:
            print(f"✓ 已恢复会话: {session_id}（{len(session.messages)} 条历史消息）")
            self.sessions[session_id] = session
        else:
            # 创建新会话
            session = ConversationSession(
                session_id=session_id,
                agent_name=self.agent_name,
                started_at=datetime.now().isoformat(),
                context=initial_context or {}
            )
            self.sessions[session_id] = session
            print(f"✓ 已创建新会话: {session_id}")

        # 初始化客户端（如果还没有）
        if not self.client:
            self.client = AsyncAnthropic(
                api_key=config.llm.api_key,
                base_url=config.llm.base_url
            )

        return session

    async def process_turn(
        self,
        session_id: str,
        user_message: str,
    ) -> AsyncIterator[Dict]:
        """处理单个对话轮次（流式，支持工具调用）"""
        session = self.sessions.get(session_id)
        if not session:
            raise ValueError(f"会话 {session_id} 不存在")

        # 添加用户消息
        session.add_message("user", user_message)

        # 构建消息历史（仅发送最近的消息）
        messages = []
        for msg in session.messages[-20:]:  # 最近 20 条消息
            if msg.role == "user":
                messages.append({"role": "user", "content": msg.content})
            else:
                # 助手消息 - 重建带工具调用的消息
                if msg.tool_calls:
                    # 有工具调用的消息
                    tool_use_blocks = []
                    for tc in msg.tool_calls:
                        tool_use_blocks.append({
                            "type": "tool_use",
                            "id": tc.get("id", ""),
                            "name": tc.get("name", ""),
                            "input": tc.get("input", {})
                        })
                    messages.append({
                        "role": "assistant",
                        "content": tool_use_blocks
                    })
                elif msg.content:
                    # 普通文本消息
                    messages.append({"role": "assistant", "content": msg.content})

        # 获取工具定义
        tools = get_tool_definitions()

        try:
            # 工具调用循环
            max_iterations = 10  # 防止无限循环
            iteration = 0

            while iteration < max_iterations:
                iteration += 1

                # 调用 API（流式）
                current_response = ""
                current_tool_use = None
                current_tool_input_json = ""  # 收集工具输入的 JSON 片段
                tool_calls = []

                async with self.client.messages.stream(
                    model=config.llm.model,
                    max_tokens=config.llm.max_tokens,
                    temperature=config.llm.temperature,
                    system=self.agent_prompt,
                    messages=messages,
                    tools=tools if tools else None,
                ) as stream:
                    async for event in stream:
                        if event.type == "text":
                            # TextEvent - 直接访问 text 属性
                            current_response += event.text
                            yield {
                                "type": "text",
                                "content": event.text
                            }
                        elif event.type == "content_block_start":
                            # RawContentBlockStartEvent - 检查是否是工具调用
                            if hasattr(event.content_block, 'type') and event.content_block.type == "tool_use":
                                current_tool_use = {
                                    "id": event.content_block.id,
                                    "name": event.content_block.name,
                                    "input": event.content_block.input or {}
                                }
                                current_tool_input_json = ""  # 重置 JSON 收集器
                        elif event.type == "content_block_delta":
                            # RawContentBlockDeltaEvent - 处理增量
                            if hasattr(event.delta, 'type') and event.delta.type == "input_json_delta":
                                # 收集工具输入的 JSON 片段
                                current_tool_input_json += event.delta.partial_json

                                # 尝试解析 JSON
                                import json
                                try:
                                    parsed_input = json.loads(current_tool_input_json)
                                    if current_tool_use:
                                        current_tool_use["input"] = parsed_input
                                except json.JSONDecodeError:
                                    # JSON 还未完成，继续收集
                                    pass
                        elif event.type == "content_block_stop":
                            # 内容块结束
                            if current_tool_use:
                                tool_calls.append(current_tool_use)
                                current_tool_use = None

                # 如果有工具调用，执行它们
                if tool_calls:
                    # 保存助手的响应（包含工具调用）
                    session.add_message("assistant", current_response, tool_calls)

                    # 执行每个工具调用
                    for tool_call in tool_calls:
                        tool_name = tool_call["name"]
                        tool_id = tool_call["id"]
                        tool_input = tool_call["input"]

                        yield {
                            "type": "tool_use",
                            "tool_name": tool_name,
                            "tool_id": tool_id
                        }

                        # 执行工具
                        try:
                            from tools.process_tools import (
                                start_process, stop_process,
                                list_processes, get_process_status
                            )

                            tool_map = {
                                "start_process": start_process,
                                "stop_process": stop_process,
                                "list_processes": list_processes,
                                "get_process_status": get_process_status,
                            }

                            tool_func = tool_map.get(tool_name)
                            if tool_func:
                                result = await tool_func(tool_input)

                                # 格式化结果
                                if result.get("status") == "success":
                                    result_msg = result.get("message", "操作成功")
                                    yield {
                                        "type": "tool_result",
                                        "tool_id": tool_id,
                                        "result": f"✓ {result_msg}"
                                    }
                                    tool_result_content = str(result)
                                else:
                                    error_msg = result.get("error", "操作失败")
                                    yield {
                                        "type": "tool_result",
                                        "tool_id": tool_id,
                                        "result": f"✗ {error_msg}"
                                    }
                                    tool_result_content = str(result)
                            else:
                                tool_result_content = f"错误：未知工具 {tool_name}"
                                yield {
                                    "type": "tool_result",
                                    "tool_id": tool_id,
                                    "result": f"✗ {tool_result_content}"
                                }
                        except Exception as e:
                            import traceback
                            error_details = traceback.format_exc()
                            tool_result_content = f"工具执行异常: {str(e)}"
                            yield {
                                "type": "tool_result",
                                "tool_id": tool_id,
                                "result": f"✗ {tool_result_content}"
                            }

                        # 将工具结果添加到消息历史
                        messages.append({
                            "role": "assistant",
                            "content": [
                                {
                                    "type": "tool_use",
                                    "id": tool_id,
                                    "name": tool_name,
                                    "input": tool_input
                                }
                            ]
                        })
                        messages.append({
                            "role": "user",
                            "content": [
                                {
                                    "type": "tool_result",
                                    "tool_use_id": tool_id,
                                    "content": tool_result_content
                                }
                            ]
                        })

                    # 继续循环，让 API 处理工具结果
                    current_response = ""
                    continue
                else:
                    # 没有工具调用，结束对话轮次
                    session.add_message("assistant", current_response, [])

                    # 保存会话
                    self._save_session(session)

                    yield {
                        "type": "turn_complete",
                        "session_id": session_id,
                        "message_count": len(session.messages)
                    }
                    break

        except Exception as e:
            import traceback
            traceback.print_exc()
            yield {
                "type": "error",
                "error": str(e)
            }

    def end_conversation(self, session_id: str):
        """结束对话"""
        if session_id in self.sessions:
            # 最终保存
            self._save_session(self.sessions[session_id])
            del self.sessions[session_id]

    def list_sessions(self):
        """列出所有已保存的会话"""
        return [f.stem for f in self.session_dir.glob("*.json")]

    async def close(self):
        """关闭客户端"""
        if self.client:
            # AsyncAnthropic 不需要显式关闭，直接删除引用即可
            self.client = None
