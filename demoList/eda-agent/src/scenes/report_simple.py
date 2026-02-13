"""简化的 ReportScene - 只保留框架"""
from typing import Dict, Generator
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from scenes.base import BaseScene


class ReportScene(BaseScene):
    """简化的报告场景"""

    def __init__(self, services: Dict):
        super().__init__(
            name="report",
            description="报告场景 - 框架版本（无具体实现）",
            keywords=[],
            services=services
        )

    def match(self, user_input: str) -> float:
        return 0.0

    def run(self, user_input: str) -> Generator[Dict, None, None]:
        yield self._create_info_message(f"\n[{self.name.upper()}] 报告场景启动")
        yield self._create_info_message(f"[{self.name}] 收到输入: {user_input}")
        yield self._create_done_message({
            "scene": self.name,
            "message": "简化的报告场景，没有实际业务逻辑"
        })
