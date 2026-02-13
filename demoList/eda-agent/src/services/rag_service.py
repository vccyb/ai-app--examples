"""RAG Service - 知识查询服务

负责：
- 知识库查询
- 模块设计规范获取
- 预留向量检索接口
"""
from typing import Dict, List, Optional
import sys
import os

# 导入现有的 RAG Agent
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from agents.rag_agent import RAGAgent


class RAGService:
    """知识查询服务

    封装现有的 RAG Agent，提供统一接口
    """

    def __init__(self):
        """初始化 RAG 服务"""
        self.rag_agent = RAGAgent()

    def query(self, keywords: List[str]) -> Dict:
        """查询知识库

        Args:
            keywords: 关键词列表

        Returns:
            查询结果
        """
        result = self.rag_agent.query(keywords)
        return {
            "keywords": keywords,
            "results": result,
            "source": "RAG Knowledge Base"
        }

    def get_specification(self, module: str) -> Dict:
        """获取模块的设计规范

        Args:
            module: 模块名称

        Returns:
            设计规范字典
        """
        spec = self.rag_agent.get_specification(module)
        return {
            "module": module,
            "specification": spec,
            "source": "RAG Knowledge Base"
        }

    def search_by_topic(self, topic: str) -> Dict:
        """按主题搜索相关知识

        Args:
            topic: 主题关键词

        Returns:
            相关知识
        """
        # 使用关键词查询
        result = self.rag_agent.query([topic])

        return {
            "topic": topic,
            "results": result,
            "source": "RAG Knowledge Base"
        }


# ============================================================================
# 测试代码
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("RAG Service 测试")
    print("=" * 70)

    # 创建服务实例
    rag_service = RAGService()

    # 测试 query
    print("\n测试1：查询关键词")
    result1 = rag_service.query(["时序", "优化"])
    print(f"查询结果: {result1['results']}")

    # 测试 get_specification
    print("\n测试2：获取模块A的设计规范")
    result2 = rag_service.get_specification("模块A")
    print(f"规范信息: {result2['specification']}")

    # 测试 search_by_topic
    print("\n测试3：按主题搜索")
    result3 = rag_service.search_by_topic("功耗")
    print(f"搜索结果数: {len(result3['results']) if isinstance(result3['results'], list) else 1}")

    print("\n测试完成")
