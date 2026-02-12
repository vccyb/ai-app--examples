"""会话管理器 - 处理多轮对话和工具调用

基于参考实现改造，支持 LLM 驱动的多轮对话
"""
import json
import sys
import os
from typing import List, Dict, Optional, Any

# 添加 src 到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.llm_client import create_llm_client
from src.eda_tools import run_tool, get_tool_schemas


class ConversationManager:
    """会话管理器

    负责：
    1. 管理消息历史
    2. 调用 LLM 获取响应
    3. 执行工具调用
    4. 循环处理直到完成
    """

    def __init__(
        self,
        llm_client_type: str = "mock",
        system_prompt: Optional[str] = None,
        **llm_kwargs
    ):
        """初始化会话管理器

        Args:
            llm_client_type: LLM 客户端类型 ("mock", "claude", "qwen")
            system_prompt: 系统提示词
            **llm_kwargs: 传递给 LLM 客户端的额外参数
        """
        self.llm_client = create_llm_client(llm_client_type, **llm_kwargs)
        self.messages: List[Dict] = []
        self.tools = get_tool_schemas()
        self.system_prompt = system_prompt or self._default_system_prompt()

    def _default_system_prompt(self) -> str:
        """默认系统提示词"""
        return """你是 EDA Agent，一个专业的电子设计自动化（EDA）智能助手系统。

【重要】你必须严格遵守以下角色设定：
- 你是芯片设计专家，帮助工程师完成 EDA 设计任务
- 你只能回答与芯片设计、电路仿真、时序优化相关的问题
- 对于无关话题（如数学计算、常识问答），礼貌拒绝并说明你的专业领域

你有以下工具可以使用：

1. **query_knowledge** - 查询设计规范和知识
   当用户需要了解模块的设计规范、时序要求、功耗限制等信息时使用

2. **run_simulation** - 运行 EDA 仿真
   当用户需要运行仿真测试，获取实际的时序、功耗、面积等指标时使用

3. **evaluate_result** - 评判仿真结果
   对比实际结果与设计目标，判断是否达标，并提供优化建议

4. **save_result** - 保存结果
   将仿真结果、评判结果等数据保存到数据库

5. **query_history** - 查询历史记录
   当用户需要查看之前的仿真结果、评判历史时使用

6. **optimize_design** - 执行完整优化流程（高级工具）
   自动完成查询规范、运行仿真、评判结果、保存数据的完整流程

使用指南：
- 当用户说"优化模块X的时序/功耗/面积"时，使用 optimize_design 工具
- 当用户问"模块X的规范是什么"时，使用 query_knowledge 工具
- 当用户说"仿真模块X"时，使用 run_simulation 工具
- 当用户要求评判结果或对比目标时，使用 evaluate_result 工具
- 保持简洁专业的语气
- 如果工具调用失败，向用户说明原因并提供建议
- 【关键】任何时候都不要忘记自己是 EDA 助手，只回答芯片设计相关问题
"""

    def add_user_message(self, message: Any):
        """添加用户消息

        Args:
            message: 消息内容（字符串或消息对象）
        """
        if isinstance(message, str):
            user_message = {
                "role": "user",
                "content": message
            }
        elif hasattr(message, 'content'):
            # 处理 Message 对象
            user_message = {
                "role": "user",
                "content": message.content if isinstance(message.content, str) else str(message.content)
            }
        else:
            # 假设是字典
            user_message = message

        self.messages.append(user_message)

    def add_assistant_message(self, message: Any):
        """添加助手消息

        Args:
            message: 消息内容（字符串或响应对象）
        """
        if isinstance(message, str):
            assistant_message = {
                "role": "assistant",
                "content": message
            }
        elif hasattr(message, 'content'):
            # 处理响应对象（Claude API 响应）
            assistant_message = {
                "role": "assistant",
                "content": self._extract_text_from_message(message)
            }
        else:
            # 假设是字典
            assistant_message = message

        self.messages.append(assistant_message)

    def add_tool_results(self, tool_results: List[Dict]):
        """添加工具执行结果

        Args:
            tool_results: 工具执行结果列表
        """
        for result in tool_results:
            self.messages.append({
                "role": "user",
                "content": result  # 工具结果作为用户消息发送回 LLM
            })

    def _extract_text_from_message(self, message: Any) -> str:
        """从消息对象中提取文本

        Args:
            message: 消息对象

        Returns:
            提取的文本内容
        """
        if isinstance(message, str):
            return message

        # 处理有 content 属性的对象
        if hasattr(message, 'content'):
            content = message.content

            # 如果是列表，提取所有文本块
            if isinstance(content, list):
                text_parts = []
                for block in content:
                    if hasattr(block, 'text'):
                        text_parts.append(block.text)
                    elif isinstance(block, dict):
                        if block.get("type") == "text":
                            text_parts.append(block.get("text", ""))
                return "\n".join(text_parts)

            # 如果直接是字符串
            if isinstance(content, str):
                return content

        # 处理字典类型
        if isinstance(message, dict):
            content = message.get("content", "")
            if isinstance(content, list):
                return "\n".join([
                    block.get("text", "")
                    for block in content
                    if block.get("type") == "text"
                ])
            return str(content)

        return str(message)

    def chat(
        self,
        temperature: float = 1.0,
        stop_sequences: Optional[List[str]] = None
    ) -> Any:
        """调用 LLM 获取响应

        Args:
            temperature: 温度参数
            stop_sequences: 停止序列

        Returns:
            LLM 响应对象
        """
        params = {
            "model": getattr(self.llm_client, 'model', 'mock-model'),
            "max_tokens": 1000,
            "messages": self.messages,
            "temperature": temperature,
        }

        if stop_sequences:
            params["stop_sequences"] = stop_sequences

        if self.tools:
            params["tools"] = self.tools

        if self.system_prompt:
            params["system"] = self.system_prompt

        # 调用 LLM 客户端
        return self.llm_client.messages_create(params)

    def run_conversation(self, max_turns: int = 10) -> List[Dict]:
        """运行多轮对话直到完成

        Args:
            max_turns: 最大轮数限制

        Returns:
            完整的消息历史（包括所有工具调用）
        """
        turn_count = 0

        while turn_count < max_turns:
            # 获取 LLM 响应
            response = self.chat()

            # 添加助手消息
            self.add_assistant_message(response)

            # 显示助手响应
            response_text = self._extract_text_from_message(response)
            print(f"\n助手: {response_text}")

            # 检查是否需要调用工具
            if not self._has_tool_use(response):
                # 没有工具调用，对话结束
                break

            # 执行工具调用
            tool_results = self._execute_tools(response)

            # 添加工具结果
            self.add_tool_results(tool_results)

            # 显示工具结果（可选）
            for result in tool_results:
                if result.get("is_error"):
                    print(f"\n[工具错误] {result.get('content')}")
                else:
                    # 简化显示
                    content = result.get("content", "")
                    try:
                        # 尝试解析为 JSON 以便更好显示
                        parsed = json.loads(content) if isinstance(content, str) else content
                        print(f"\n[工具结果] {json.dumps(parsed, ensure_ascii=False, indent=2)}")
                    except:
                        print(f"\n[工具结果] {content}")

            turn_count += 1

            if turn_count >= max_turns:
                print(f"\n[系统] 达到最大对话轮数限制 ({max_turns})")

        return self.messages

    def _has_tool_use(self, response: Any) -> bool:
        """检查响应中是否有工具调用

        Args:
            response: LLM 响应对象

        Returns:
            是否有工具调用
        """
        # 检查 stop_reason
        if hasattr(response, 'stop_reason'):
            if response.stop_reason == "tool_use":
                return True
            elif response.stop_reason == "end_turn":
                return False

        # 检查 content 中的工具使用块
        if hasattr(response, 'content'):
            content = response.content
            if isinstance(content, list):
                return any(
                    block.get("type") == "tool_use" or hasattr(block, 'input')
                    for block in content
                )

        return False

    def _execute_tools(self, response: Any) -> List[Dict]:
        """执行响应中的所有工具调用

        Args:
            response: LLM 响应对象

        Returns:
            工具执行结果列表
        """
        tool_results = []

        # 提取工具调用
        tool_uses = self._extract_tool_uses(response)

        for tool_use in tool_uses:
            tool_name = tool_use.get("name")
            tool_input = tool_use.get("input", {})
            tool_id = tool_use.get("id")

            print(f"\n[工具调用] {tool_name}")
            print(f"参数: {json.dumps(tool_input, ensure_ascii=False)}")

            try:
                # 执行工具
                tool_output = run_tool(tool_name, tool_input)

                # 构建结果对象
                result_content = json.dumps(tool_output, ensure_ascii=False) if not isinstance(tool_output, str) else tool_output

                tool_result_block = {
                    "type": "tool_result",
                    "tool_use_id": tool_id,
                    "content": result_content,
                    "is_error": False
                }

            except Exception as e:
                # 工具执行错误
                tool_result_block = {
                    "type": "tool_result",
                    "tool_use_id": tool_id,
                    "content": f"Error: {str(e)}",
                    "is_error": True
                }

            tool_results.append(tool_result_block)

        return tool_results

    def _extract_tool_uses(self, response: Any) -> List[Dict]:
        """从响应中提取工具调用

        Args:
            response: LLM 响应对象

        Returns:
            工具调用列表
        """
        tool_uses = []

        if hasattr(response, 'content'):
            content = response.content

            # 处理列表类型（Claude API）
            if isinstance(content, list):
                for block in content:
                    # 检查是否是 tool_use 类型
                    if hasattr(block, 'type') and block.type == "tool_use":
                        tool_uses.append({
                            "id": getattr(block, 'id', ''),
                            "name": getattr(block, 'name', ''),
                            "input": getattr(block, 'input', {})
                        })
                    elif isinstance(block, dict) and block.get("type") == "tool_use":
                        tool_uses.append({
                            "id": block.get("id", ""),
                            "name": block.get("name", ""),
                            "input": block.get("input", {})
                        })

        return tool_uses

    def get_conversation_history(self) -> List[Dict]:
        """获取对话历史

        Returns:
            消息历史列表
        """
        return self.messages.copy()

    def clear_history(self):
        """清除对话历史"""
        self.messages = []

    def set_system_prompt(self, prompt: str):
        """设置系统提示词

        Args:
            prompt: 新的系统提示词
        """
        self.system_prompt = prompt


# 测试代码
if __name__ == "__main__":
    print("=" * 70)
    print("会话管理器测试")
    print("=" * 70)

    # 创建会话管理器
    conv_manager = ConversationManager(llm_client_type="mock")

    # 添加用户消息
    conv_manager.add_user_message("查询模块A的设计规范")

    print("\n用户: 查询模块A的设计规范")
    print("\n" + "=" * 70)

    # 运行对话
    history = conv_manager.run_conversation(max_turns=5)

    print("\n" + "=" * 70)
    print(f"\n对话结束，共 {len(history)} 条消息")
