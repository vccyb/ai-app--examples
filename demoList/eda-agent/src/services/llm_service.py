"""LLM Service - 统一的 LLM 调用接口

负责：
- 统一的模型调用接口
- 支持不同模型切换
- 提供结构化输出和分类功能
"""
import json
from typing import Dict, List, Optional, Any
from abc import ABC, abstractmethod

# 导入现有的 LLM 客户端
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from llm_client import create_llm_client, LLMClient


class LLMService:
    """LLM 调用服务

    封装不同的 LLM 实现，提供统一接口
    """

    def __init__(
        self,
        client_type: str = "mock",
        model: str = "claude-sonnet-4-5",
        **kwargs
    ):
        """初始化 LLM 服务

        Args:
            client_type: 客户端类型 ("mock", "claude", "qwen")
            model: 模型名称
            **kwargs: 传递给 LLM 客户端的额外参数
        """
        self.client_type = client_type
        self.model = model
        self.client: LLMClient = create_llm_client(client_type, model=model, **kwargs)

    def chat(
        self,
        messages: List[Dict],
        temperature: float = 1.0,
        max_tokens: int = 1000,
        **kwargs
    ) -> Any:
        """调用 LLM 进行对话

        Args:
            messages: 消息历史列表
            temperature: 温度参数
            max_tokens: 最大 token 数
            **kwargs: 其他参数

        Returns:
            LLM 响应对象
        """
        params = {
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            **kwargs
        }

        return self.client.messages_create(params)

    def structured_output(
        self,
        messages: List[Dict],
        output_schema: Dict,
        temperature: float = 0.7,
        **kwargs
    ) -> Any:
        """获取结构化输出

        Args:
            messages: 消息历史列表
            output_schema: 输出 schema（JSON Schema 格式）
            temperature: 温度参数（结构化输出通常用较低温度）
            **kwargs: 其他参数

        Returns:
            结构化的 LLM 响应
        """
        # 添加结构化输出提示
        system_prompt = kwargs.pop('system_prompt', '')
        system_prompt += f"\n\n请按照以下 JSON 格式返回结果：\n{json.dumps(output_schema, ensure_ascii=False)}"

        params = {
            "messages": messages,
            "temperature": temperature,
            "system": system_prompt,
            **kwargs
        }

        return self.client.messages_create(params)

    def classify(
        self,
        text: str,
        categories: List[str],
        **kwargs
    ) -> Dict:
        """对文本进行分类

        Args:
            text: 待分类的文本
            categories: 类别列表
            **kwargs: 其他参数

        Returns:
            分类结果 {"category": "...", "confidence": ...}
        """
        prompt = f"""请将以下文本分类到这些类别之一：{', '.join(categories)}

文本：{text}

只返回类别名称，不要其他内容。"""

        messages = [{"role": "user", "content": prompt}]

        response = self.chat(messages, temperature=0.3, **kwargs)

        # 提取类别
        # 这里需要根据不同 LLM 客户端处理响应
        # 简化版本：直接返回字符串
        if isinstance(response, str):
            category = response.strip()
        elif hasattr(response, 'content'):
            content = response.content
            if isinstance(content, str):
                category = content.strip()
            elif isinstance(content, list) and len(content) > 0:
                category = str(content[0].get('text', '')).strip()
            else:
                category = str(content).strip()
        else:
            category = str(response).strip()

        # 检查是否在类别列表中
        if category in categories:
            return {"category": category, "confidence": 1.0}
        else:
            # 如果不在列表中，返回最接近的或未知
            return {"category": "unknown", "confidence": 0.0}

    def generate_plan(
        self,
        task_description: str,
        context: Optional[Dict] = None,
        **kwargs
    ) -> Dict:
        """生成执行计划

        Args:
            task_description: 任务描述
            context: 上下文信息
            **kwargs: 其他参数

        Returns:
            生成的计划 {"steps": [...], "reasoning": "..."}
        """
        context_str = ""
        if context:
            context_str = f"\n\n上下文信息：\n{json.dumps(context, ensure_ascii=False)}"

        prompt = f"""请为以下任务生成执行计划：

任务描述：{task_description}{context_str}

请生成详细的执行步骤，每个步骤应该：
1. 有明确的步骤编号
2. 说明要做什么
3. 列出所需的关键信息

返回 JSON 格式：
{{
  "steps": [
    {{"step": 1, "action": "...", "description": "..."}},
    ...
  ],
  "reasoning": "生成这个计划的原因"
}}"""

        messages = [{"role": "user", "content": prompt}]

        response = self.structured_output(
            messages,
            output_schema={
                "type": "object",
                "properties": {
                    "steps": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "step": {"type": "integer"},
                                "action": {"type": "string"},
                                "description": {"type": "string"}
                            }
                        }
                    },
                    "reasoning": {"type": "string"}
                }
            },
            temperature=0.5,
            **kwargs
        )

        # 解析响应
        # 简化版本：尝试解析 JSON
        response_text = self._extract_response_text(response)

        try:
            plan = json.loads(response_text)
            return plan
        except:
            # 如果解析失败，返回默认结构
            return {
                "steps": [
                    {"step": 1, "action": "analyze", "description": task_description}
                ],
                "reasoning": "LLM 响应解析失败，使用默认计划"
            }

    def suggest_optimization(
        self,
        current_result: Dict,
        target: Dict,
        **kwargs
    ) -> Dict:
        """建议优化方案

        Args:
            current_result: 当前结果
            target: 目标指标
            **kwargs: 其他参数

        Returns:
            优化建议 {"suggestion": "...", "params": {...}}
        """
        prompt = f"""当前仿真结果未达到目标，请建议优化方案：

当前结果：
{json.dumps(current_result, ensure_ascii=False, indent=2)}

目标：
{json.dumps(target, ensure_ascii=False, indent=2)}

请分析：
1. 当前值与目标值的差距
2. 可能的原因
3. 具体的优化建议（如调整参数、修改设计等）

返回 JSON 格式：
{{
  "analysis": "差距和原因分析",
  "suggestion": "优化建议描述",
  "recommended_params": {{"param_name": "value"}},
  "expected_improvement": "预期改善效果"
}}"""

        messages = [{"role": "user", "content": prompt}]

        response = self.structured_output(
            messages,
            output_schema={
                "type": "object",
                "properties": {
                    "analysis": {"type": "string"},
                    "suggestion": {"type": "string"},
                    "recommended_params": {"type": "object"},
                    "expected_improvement": {"type": "string"}
                }
            },
            temperature=0.7,
            **kwargs
        )

        # 解析响应
        response_text = self._extract_response_text(response)

        try:
            suggestion = json.loads(response_text)
            return suggestion
        except:
            return {
                "analysis": "无法解析 LLM 响应",
                "suggestion": "请检查仿真参数和设计",
                "recommended_params": {},
                "expected_improvement": "未知"
            }

    def _extract_response_text(self, response: Any) -> str:
        """从响应中提取文本"""
        if isinstance(response, str):
            return response

        if hasattr(response, 'content'):
            content = response.content
            if isinstance(content, str):
                return content
            elif isinstance(content, list):
                texts = []
                for block in content:
                    if hasattr(block, 'text'):
                        texts.append(block.text)
                    elif isinstance(block, dict):
                        texts.append(block.get('text', ''))
                return '\n'.join(texts)

        return str(response)


# ============================================================================
# 测试代码
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("LLM Service 测试")
    print("=" * 70)

    import json

    # 创建服务实例
    llm_service = LLMService(client_type="mock")

    # 测试 chat
    print("\n测试1：基础对话")
    messages = [{"role": "user", "content": "你好"}]
    response1 = llm_service.chat(messages)
    print(f"响应类型: {type(response1)}")

    # 测试 classify
    print("\n测试2：文本分类")
    result2 = llm_service.classify(
        "优化模块A的时序",
        categories=["verify", "report", "optimize", "unknown"]
    )
    print(f"分类结果: {result2}")

    # 测试 generate_plan
    print("\n测试3：生成执行计划")
    result3 = llm_service.generate_plan("验证模块A时序<10ns")
    print(f"生成的计划步骤数: {len(result3.get('steps', []))}")

    # 测试 suggest_optimization
    print("\n测试4：建议优化方案")
    result4 = llm_service.suggest_optimization(
        current_result={"timing": "12ns", "power": "50mW"},
        target={"metric": "timing", "operator": "<", "value": "10ns"}
    )
    print(f"优化建议: {result4.get('suggestion', 'N/A')}")

    print("\n测试完成")
