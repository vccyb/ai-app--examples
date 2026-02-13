"""LLM Client - 统一的模型调用接口

支持：Claude (官方)
"""
import os
from typing import Dict, Optional, Any
from abc import ABC, abstractmethod

try:
    from anthropic import Anthropic
except ImportError:
    Anthropic = None


class LLMClient(ABC):
    """LLM 客户端抽象基类"""

    @abstractmethod
    def create_message(self, **kwargs) -> Any:
        """创建消息（具体实现由子类完成）"""
        pass

    @abstractmethod
    def messages_create(self, params: Dict) -> Any:
        """发送消息请求"""
        pass


class MockLLMClient(LLMClient):
    """Mock LLM 客户端 - 用于测试和演示

    返回预设的模拟响应，支持智能分类
    """

    def __init__(self, model: str = "mock-model"):
        self.model = model

    def create_message(self, **kwargs) -> Dict:
        """创建 Mock 消息（简单返回输入）"""
        return {"mock": True, "input": kwargs}

    def messages_create(self, params: Dict) -> Any:
        """发送 Mock 消息请求"""
        messages = params.get("messages", [])
        if messages:
            last_message = messages[-1]
            content = last_message.get("content", "")

            # 检测不同类型的请求
            # 1. classify 请求
            if "分类" in content and "类别" in content:
                # 提取类别列表
                import re
                category_match = re.search(r'类别之一[：:]\s*([^\n]*?)(?:\n|文本：)', content)
                if category_match:
                    categories_text = category_match.group(1).strip('，、')

                    # 简单的类别列表解析
                    if '，' in categories_text:
                        categories = [c.strip() for c in categories_text.split('，')]
                    elif ',' in categories_text:
                        categories = [c.strip() for c in categories_text.split(',')]
                    else:
                        categories = [categories_text]

                    # 提取待分类的文本（在"文本："之后）
                    text_match = re.search(r'文本[：:]\s*([^\n]*?)(?:\n|$)', content)
                    if text_match:
                        text = text_match.group(1).strip()

                        # 简单的关键词匹配分类
                        best_category = self._classify_by_keywords(text, categories)

                        return MockResponse(best_category)

            # 2. task 解析请求（返回 JSON）
            elif "解析为 EDA 验证任务" in content or "解析为" in content:
                return MockResponse(self._mock_parse_task(content))

            # 其他类型的请求：返回 mock 响应
            return MockResponse(content)

        return MockResponse("")

    def _classify_by_keywords(self, text: str, categories: list) -> str:
        """通过简单关键词匹配进行分类

        Args:
            text: 待分类的文本
            categories: 候选类别列表

        Returns:
            最佳匹配的类别
        """
        # 定义每个类别对应的关键词
        category_keywords = {
            "verify": ["验证", "verify", "测试", "test", "检查", "是否满足", "是否达到"],
            "report": ["报告", "report", "生成", "导出", "export", "汇总", "总结"],
            "optimize": ["优化", "optimize", "改进", "improve", "调整", "提升"]
        }

        # 计算每个类别的匹配分数
        scores = {}
        text_lower = text.lower()

        for category in categories:
            score = 0.0
            keywords = category_keywords.get(category, [])

            # 如果类别名称直接出现在文本中，给予高分
            if category.lower() in text_lower:
                score += 0.5

            # 关键词匹配
            for kw in keywords:
                if kw.lower() in text_lower:
                    score += 0.3

            scores[category] = score

        # 返回分数最高的类别
        if scores:
            best_category = max(scores, key=scores.get)
            if scores[best_category] > 0:
                return best_category

        # 如果没有匹配，返回第一个类别
        return categories[0] if categories else "unknown"

    def _mock_parse_task(self, prompt: str) -> str:
        """模拟任务解析，返回 JSON 格式的结果

        Args:
            prompt: 用户输入的提示文本

        Returns:
            JSON 格式的字符串
        """
        import re
        import json

        # 提取用户输入（在"用户输入："之后）
        user_input_match = re.search(r'用户输入[：:]\s*([^\n]+?)(?:\n|请返回)', prompt)
        if not user_input_match:
            # 如果找不到，返回空结果
            return json.dumps({"module": None, "goal": None}, ensure_ascii=False)

        user_input = user_input_match.group(1).strip()

        # 解析模块名
        module = None
        module_match = re.search(r'模块\s*([A-D])', user_input)
        if module_match:
            module = f"模块{module_match.group(1)}"

        # 解析目标
        goal = None
        # 检测"时序/timing"和比较符
        timing_match = re.search(r'(时序|timing)\s*(?:是否)?\s*([<>=!]+)\s*(\d+[a-z]+)?', user_input)
        power_match = re.search(r'(功耗|power)\s*(?:是否)?\s*([<>=!]+)\s*(\d+[a-z]+)?', user_input)
        area_match = re.search(r'(面积|area)\s*(?:是否)?\s*([<>=!]+)\s*(\d+[a-z]+)?', user_input)

        if timing_match:
            goal = {
                "metric": "timing",
                "operator": timing_match.group(2) or "<",
                "value": timing_match.group(3) or "10ns"
            }
        elif power_match:
            goal = {
                "metric": "power",
                "operator": power_match.group(2) or "<",
                "value": power_match.group(3) or "50mW"
            }
        elif area_match:
            goal = {
                "metric": "area",
                "operator": area_match.group(2) or "<",
                "value": area_match.group(3) or "1000um²"
            }

        # 构建结果
        result = {"module": module}
        if goal:
            result["goal"] = goal

        return json.dumps(result, ensure_ascii=False)


class MockResponse:
    """Mock 响应对象"""

    def __init__(self, content: str):
        self.content = content
        self.stop_reason = "end_turn"
        self.model = "mock-model"

    def __str__(self):
        return f"MockResponse(content='{self.content}')"


class ClaudeLLMClient(LLMClient):
    """Claude LLM 客户端 - 使用 Anthropic 官方 SDK

    支持通过 base_url 接入智谱 AI 等兼容接口
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "claude-sonnet-4-5",
        base_url: Optional[str] = None
    ):
        if Anthropic is None:
            raise ImportError("请先安装 anthropic: pip install anthropic")

        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("需要提供 ANTHROPIC_API_KEY 环境变量")

        # 创建客户端（支持自定义 base_url）
        client_kwargs = {"api_key": self.api_key}
        if base_url:
            client_kwargs["base_url"] = base_url

        self.client = Anthropic(**client_kwargs)
        self.model = model

    def create_message(self, **kwargs) -> Dict:
        """创建 Claude 消息"""
        return self.client.messages.create(**kwargs)

    def messages_create(self, params: Dict) -> Any:
        """发送消息到 Claude API"""
        return self.client.messages.create(**params)


def create_llm_client(
    client_type: str = "claude",
    **kwargs
) -> LLMClient:
    """工厂函数：创建 LLM 客户端"""
    clients = {
        "mock": MockLLMClient,
        "claude": ClaudeLLMClient,
        }

    client_class = clients.get(client_type.lower())
    if not client_class:
        raise ValueError(f"不支持的客户端类型: {client_type}，支持的类型: {list(clients.keys())}")

    return client_class(**kwargs)


if __name__ == "__main__":
    print("=== 测试 Claude LLM 客户端 ===")
    client = create_llm_client("claude", api_key="test")

    print(f"客户端类型: {type(client).__name__}")
    print(f"模型: {client.model}")
