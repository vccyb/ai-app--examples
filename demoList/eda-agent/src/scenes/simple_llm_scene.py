"""简化的 LLM 场景 - 避免复杂的 f-string"""
from typing import Dict, Generator
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from scenes.base import BaseScene


class SimpleLLMScene(BaseScene):
    """简化的 LLM 场景"""

    def __init__(self, services: Dict):
        super().__init__(
            name="simple_llm",
            description="简化的 LLM 场景",
            keywords=[],
            services=services
        )

    def match(self, user_input: str) -> float:
        return 0.0

    def run(self, user_input: str) -> Generator[Dict, None, None]:
        yield self._create_info_message(f"\n[{self.name.upper()}] 场景启动")
        yield self._create_info_message(f"用户输入: {user_input}")

        if self.llm_service:
            yield self._create_info_message("有 LLM 服务可用")

            # 简化：只调用 LLM chat，不解析返回
            try:
                messages = [{"role": "user", "content": f"任务: {user_input}"}]
                response = self.llm_service.chat(messages, temperature=0.5)

                # 显示响应
                if hasattr(response, 'content'):
                    content = response.content
                    if isinstance(content, str):
                        yield self._create_info_message(f"LLM 响应: {content}")
                    elif isinstance(content, list) and len(content) > 0:
                        text = content[0].get('text', str(content[0]))
                        yield self._create_info_message(f"LLM 响应: {text}")
                else:
                    yield self._create_info_message(f"LLM 响应: {response}")

            except Exception as e:
                yield self._create_info_message(f"LLM 调用出错: {str(e)}")

        yield self._create_done_message({"message": "场景执行完成"})


if __name__ == "__main__":
    from services.llm_service import LLMService
    from services.rag_service import RAGService
    from services.eda_service import EDAService
    from services.state_service import StateService

    services = {}
    services["llm"] = LLMService(client_type="mock")
    services["rag"] = RAGService()
    services["eda"] = EDAService()
    services["state"] = StateService()

    scene = SimpleLLMScene(services)

    print("=" * 70)
    print("简化的 LLM 场景测试")
    print("=" * 70)

    for msg in scene.run("验证模块A的时序<10ns"):
        if msg.get("type") == "info":
            print(f"\n{msg.get('content')}")
