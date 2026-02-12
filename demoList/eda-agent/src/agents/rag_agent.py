"""RAG Agent - 知识查询Agent（MVP简化版）

职责：提供知识查询接口，当前用10条固定Mock数据
"""
from typing import Dict, List, Optional


# 固定知识库（10条Mock数据）
KNOWLEDGE_BASE = {
    # 时序相关
    "时序优化": "降低时钟频率可以减少传播延迟，但可能影响吞吐量",
    "关键路径": "时序主要受组合逻辑深度和时钟频率影响",
    "100MHz": "典型时钟频率，时序约10ns",
    "80MHz": "降低频率后，时序可改善至8.9ns",

    # 功耗相关
    "功耗优化": "降低供电电压和时钟频率可减少动态功耗",
    "低功耗": "功耗<50mW为低功耗设计",

    # 面积相关
    "面积预算": "芯片面积直接影响成本，需控制在预算内",
    "面积优化": "优化布局可减少芯片面积",

    # 通用
    "默认": "根据最佳实践选择参数"
}


class RAGAgent:
    """RAG知识查询Agent - 最简化版本"""

    def query(self, keywords: List[str]) -> Dict[str, str]:
        """
        查询知识库，返回匹配的知识条目

        参数:
            keywords: 关键词列表，如 ["模块A", "时序优化"]

        返回:
            {
                "knowledge": str,  # 匹配到的知识
                "sources": List[str],  # 来源列表
                "matched_keywords": List[str]  # 匹配到的关键词
            }
        """
        # 简单匹配逻辑
        matched_knowledge = []
        matched_keywords = []

        for key in keywords:
            # 遍历所有知识条目
            for knowledge_key, knowledge_value in KNOWLEDGE_BASE.items():
                # 检查关键词是否在知识中
                if key in knowledge_key.lower() or knowledge_key.lower() in key.lower():
                    matched_knowledge.append(knowledge_value)
                    if key not in matched_keywords:
                        matched_keywords.append(key)

        if matched_knowledge:
            # 合并所有匹配的知识
            combined = "；".join(matched_knowledge)
            return {
                "knowledge": combined,
                "sources": list(KNOWLEDGE_BASE.keys()),
                "matched_keywords": matched_keywords
            }

        # 未找到匹配
        return {
            "knowledge": "未找到相关知识",
            "sources": [],
            "matched_keywords": []
        }

    def get_specification(self, module: str) -> Dict:
        """
        获取模块的设计规范（简化版，返回固定规范）

        参数:
            module: 模块名称，如 "模块A"

        返回:
            固定的设计规范字典
        """
        # 固定规范（Mock）
        specifications = {
            "模块A": {
                "timing": {"max_clock": "100MHz", "typical_timing": "10ns"},
                "power": {"max": "100mW"},
                "area": {"max": "1000um²"}
            },
            "模块B": {
                "timing": {"max_clock": "120MHz", "typical_timing": "8ns"},
                "power": {"max": "80mW"},
                "area": {"max": "1200um²"}
            }
        }

        return specifications.get(module, {"timing": {}, "power": {}, "area": {}})


# 测试代码
if __name__ == "__main__":
    # 创建RAG Agent实例
    rag_agent = RAGAgent()

    # 测试1：查询时序优化知识
    print("=== 测试1：查询时序优化 ===")
    result1 = rag_agent.query(["模块A", "时序优化"])
    print(f"结果: {result1['knowledge']}")

    # 测试2：查询功耗知识
    print("\n=== 测试2：查询功耗 ===")
    result2 = rag_agent.query(["功耗", "优化"])
    print(f"结果: {result2['knowledge']}")

    # 测试3：获取模块A规范
    print("\n=== 测试3：获取模块A规范 ===")
    spec = rag_agent.get_specification("模块A")
    print(f"规范: {spec}")
