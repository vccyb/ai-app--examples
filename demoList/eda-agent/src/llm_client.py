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
