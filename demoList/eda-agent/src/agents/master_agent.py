"""Master Agent - 主控Agent（MVP简化版）

职责：接收用户指令，分派给子Agent，聚合结果返回用户
"""
from typing import Dict, Optional

from .rag_agent import RAGAgent
from .eda_agent import EDAToolAgent
from .evaluation_agent import EvaluationAgent
from .general_agent import GeneralAgent


class MasterAgent:
    """主控Agent - 最简化版本，只做任务分派和结果聚合"""

    def __init__(self):
        """初始化子Agent"""
        self.rag_agent = RAGAgent()
        self.eda_agent = EDAToolAgent()
        self.evaluator = EvaluationAgent()
        self.general_agent = GeneralAgent()

    def process(self, user_input: str) -> Dict:
        """
        处理用户输入的主方法

        参数:
            user_input: 用户自然语言输入，如"优化模块A的时序，目标<10ns"

        返回:
            处理结果字典，包含status, result, trace等
        """
        # 打印分隔线
        print("\n" + "=" * 60)
        print(f"[Master] 收到用户指令: {user_input}")

        # 1. 解析意图（最简化版：假设所有输入都是"优化"操作）
        # 格式："优化[模块] [指标]<[值]"
        task_info = self._parse_simple_input(user_input)

        # 2. 调用RAG查询知识
        print("[Master] 步骤1：查询RAG知识...")
        spec = self.rag_agent.get_specification(task_info["module"])
        print(f"[Master] 查询到规范: {spec}")

        # 3. 调用EDA工具执行仿真
        print("[Master] 步骤2：执行EDA仿真...")
        simulation_result = self.eda_agent.run_simulation(
            task_info["module"],
            parameters=task_info.get("parameters")
        )
        print(f"[Master] 仿真完成: {simulation_result}")

        # 4. 调用Evaluation Agent评判
        print("[Master] 步骤3：评判结果...")
        evaluation_result = self.evaluator.evaluate(
            goal=task_info["goal"],
            actual=simulation_result
        )
        print(f"[Master] 评判结果: {evaluation_result['status']}")

        # 5. 保存到通用Agent
        print("[Master] 步骤4：保存数据...")
        self.general_agent.save({"task": user_input, "module": task_info["module"]})
        self.general_agent.save({"simulation": simulation_result})
        self.general_agent.save({"evaluation": evaluation_result})

        # 6. 聚合结果返回
        result = {
            "status": "success",
            "task": user_input,
            "module": task_info["module"],
            "simulation": simulation_result,
            "evaluation": evaluation_result,
            "trace": [
                "查询RAG知识",
                "执行EDA仿真",
                "评判结果",
                "保存数据"
            ]
        }

        print(f"\n[Master] === 最终结果 ===")
        print(f"状态: {result['status']}")
        print(f"仿真结果: {result['simulation']}")
        print(f"评判: {result['evaluation']['status']} - {result['evaluation']['reason']}")

        if evaluation_result["status"] == "PASS":
            print("\n✅ 任务达标！")
        else:
            print(f"\n❌ 任务未达标")
            if evaluation_result.get("suggestion"):
                print(f"建议: {evaluation_result['suggestion']}")

        return result

    def _parse_simple_input(self, user_input: str) -> Dict:
        """
        解析简单的用户输入（MVP版本）

        假设格式：优化[模块] [指标]<[值]
        例如：优化模块A时序<10ns
        """
        # 默认值
        result = {
            "action": "optimize",
            "module": "未知",
            "goal": {"metric": "timing", "operator": "<", "value": "10ns"},
            "parameters": {}
        }

        # 提取模块名（查找"优化"后的词）
        if "优化" in user_input:
            parts = user_input.split("优化")
            if len(parts) > 1:
                # 提取下一个词作为模块名
                module_name = parts[1].strip()

                # 检查是否包含指标目标
                if "<" in user_input:
                    # 提取目标值（如"10ns"）
                    target_parts = user_input.split("<")
                    if len(target_parts) > 1:
                        target_value = target_parts[1].strip().split("，")[0].strip()
                        result["module"] = module_name
                        result["goal"] = {
                            "metric": "timing",
                            "operator": "<",
                            "value": target_value
                        }

        return result


# 测试代码
if __name__ == "__main__":
    # 创建Master Agent实例
    master = MasterAgent()

    # 测试1：完整流程
    print("=== 测试1：完整流程 ===")
    result1 = master.process("优化模块A时序<10ns")
    print("\n")

    # 测试2：缺少目标值
    print("=== 测试2：缺少目标值 ===")
    result2 = master.process("优化模块B")
    print("\n")

    # 测试3：不同格式
    print("=== 测试3：不同模块 ===")
    result3 = master.process("查询模块A的信息")
    print("\n")
