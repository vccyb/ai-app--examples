"""EDA Tools - 将现有 Agent 转换为 Claude Tool 格式

所有 EDA 相关的工具定义和实现
"""
from typing import Dict, Any, Optional
from anthropic.types import ToolParam
import random


# =============================================================================
# 工具实现
# =============================================================================

def query_knowledge(module: str, keywords: Optional[list] = None) -> Dict:
    """查询设计规范和知识

    Args:
        module: 模块名称（如"模块A"）
        keywords: 可选的关键词列表

    Returns:
        包含设计规范的字典
    """
    # 这里调用原来的 RAG Agent
    from src.agents.rag_agent import RAGAgent
    rag = RAGAgent()

    if keywords:
        result = rag.query(keywords)
        spec = rag.get_specification(module)
        return {**result, "specification": spec}
    else:
        spec = rag.get_specification(module)
        return {
            "knowledge": f"已获取{module}的设计规范",
            "specification": spec,
            "sources": ["RAG知识库"]
        }


def run_simulation(module: str, parameters: Optional[Dict] = None) -> Dict:
    """运行 EDA 仿真

    Args:
        module: 模块名称（如"模块A"）
        parameters: 可选的仿真参数

    Returns:
        仿真结果字典，包含 timing, power, area 等指标
    """
    # 这里调用原来的 EDA Agent
    from src.agents.eda_agent import EDAToolAgent
    eda = EDAToolAgent()

    result = eda.run_simulation(module, parameters)
    return {
        "tool_name": "MockEDA",
        "status": "SUCCESS",
        **result
    }


def evaluate_result(goal: Dict, actual: Dict) -> Dict:
    """评判仿真结果是否达标

    Args:
        goal: 目标指标，如 {"metric": "timing", "operator": "<", "value": "10ns"}
        actual: 实际结果，如 {"timing": "12ns", "power": "50mW"}

    Returns:
        评判结果，包含 status (PASS/FAIL), reason, suggestion
    """
    # 这里调用原来的 Evaluation Agent
    from src.agents.evaluation_agent import EvaluationAgent
    evaluator = EvaluationAgent()

    result = evaluator.evaluate(goal, actual)
    return result


def save_result(data: Dict, data_type: str = "task") -> Dict:
    """保存结果到数据库

    Args:
        data: 要保存的数据字典
        data_type: 数据类型（"task", "simulation", "evaluation"）

    Returns:
        保存结果，包含记录 ID
    """
    # 这里调用原来的 General Agent
    from src.agents.general_agent import GeneralAgent
    general = GeneralAgent()

    record_id = general.save(data)
    return {
        "status": "SUCCESS",
        "record_id": record_id,
        "data_type": data_type
    }


def query_history(filters: Optional[Dict] = None) -> Dict:
    """查询历史记录

    Args:
        filters: 过滤条件，如 {"module": "模块A"}

    Returns:
        历史记录列表
    """
    # 这里调用原来的 General Agent
    from src.agents.general_agent import GeneralAgent
    general = GeneralAgent()

    result = general.query(filters)
    return result


def optimize_design(module: str, target: Dict) -> Dict:
    """执行完整的设计优化流程

    这是一个复合工具，会依次调用：
    1. 查询规范
    2. 运行仿真
    3. 评判结果
    4. 保存数据

    Args:
        module: 模块名称
        target: 优化目标，如 {"metric": "timing", "operator": "<", "value": "10ns"}

    Returns:
        完整的优化结果
    """
    # 1. 查询规范
    spec_result = query_knowledge(module)
    spec = spec_result["specification"]

    # 2. 运行仿真
    sim_result = run_simulation(module)

    # 3. 评判结果
    eval_result = evaluate_result(target, sim_result)

    # 4. 保存所有结果
    save_result({"task": f"优化{module}", "module": module}, "task")
    save_result({"simulation_result": sim_result, "module": module}, "simulation")
    save_result({"evaluation": eval_result, "module": module}, "evaluation")

    return {
        "status": "completed",
        "module": module,
        "specification": spec,
        "simulation": sim_result,
        "evaluation": eval_result
    }


# =============================================================================
# Claude Tool Schema 定义
# =============================================================================

query_knowledge_schema = ToolParam(
    name="query_knowledge",
    description="查询 EDA 设计规范和相关知识。当用户需要了解某个模块的设计规范、时序要求、功耗限制、面积预算等信息时使用此工具。可以返回模块的完整设计规范文档，包括时序约束、功耗上限、面积预算等关键指标。",
    input_schema={
        "type": "object",
        "properties": {
            "module": {
                "type": "string",
                "description": "要查询的模块名称，如'模块A'、'模块B'、'模块C'等"
            },
            "keywords": {
                "type": "array",
                "items": {"type": "string"},
                "description": "可选的关键词列表，用于更精确的查询，如['时序', '优化']"
            }
        },
        "required": ["module"]
    }
)


run_simulation_schema = ToolParam(
    name="run_simulation",
    description="执行 EDA 仿真并获取结果。当用户需要运行某个模块的仿真测试，获取时序、功耗、面积等实际指标时使用此工具。仿真会返回模块的实际性能数据，包括时序（纳秒）、功耗（毫瓦）、面积（平方微米）等关键指标。",
    input_schema={
        "type": "object",
        "properties": {
            "module": {
                "type": "string",
                "description": "要仿真的模块名称，如'模块A'、'模块B'、'模块C'等"
            },
            "parameters": {
                "type": "object",
                "description": "可选的仿真参数，用于调整仿真配置，如电压、频率等"
            }
        },
        "required": ["module"]
    }
)


evaluate_result_schema = ToolParam(
    name="evaluate_result",
    description="评判仿真结果是否达到设计目标。对比仿真结果与目标指标，判断是否达标，并提供优化建议。支持多种运算符（小于、大于、等于等）和多个指标（时序、功耗、面积）的评判。",
    input_schema={
        "type": "object",
        "properties": {
            "goal": {
                "type": "object",
                "description": "设计目标，包含指标名称、运算符和目标值",
                "properties": {
                    "metric": {
                        "type": "string",
                        "description": "指标名称，如'timing'（时序）、'power'（功耗）、'area'（面积）"
                    },
                    "operator": {
                        "type": "string",
                        "description": "比较运算符，支持'<', '<=', '>', '>=', '=='",
                        "enum": ["<", "<=", ">", ">=", "=="]
                    },
                    "value": {
                        "type": "string",
                        "description": "目标值，如'10ns'、'50mW'、'1000um²'"
                    }
                },
                "required": ["metric", "operator", "value"]
            },
            "actual": {
                "type": "object",
                "description": "实际仿真结果，包含各项指标的实际值"
            }
        },
        "required": ["goal", "actual"]
    }
)


save_result_schema = ToolParam(
    name="save_result",
    description="保存仿真结果、评判结果或任务信息到数据库。用于持久化存储设计任务、仿真数据和评判历史，支持后续查询和分析。",
    input_schema={
        "type": "object",
        "properties": {
            "data": {
                "type": "object",
                "description": "要保存的数据对象，可以包含任务信息、仿真指标、评判结果等"
            },
            "data_type": {
                "type": "string",
                "description": "数据类型，用于分类存储，可选值: 'task', 'simulation', 'evaluation'",
                "enum": ["task", "simulation", "evaluation"]
            }
        },
        "required": ["data"]
    }
)


query_history_schema = ToolParam(
    name="query_history",
    description="查询历史记录和保存的数据。当用户需要查看之前的仿真结果、评判历史或任务记录时使用此工具。可以按模块名等条件过滤查询。",
    input_schema={
        "type": "object",
        "properties": {
            "filters": {
                "type": "object",
                "description": "查询过滤条件，如 {'module': '模块A'} 用于筛选特定模块的记录"
            }
        }
    }
)


optimize_design_schema = ToolParam(
    name="optimize_design",
    description="执行完整的设计优化流程。这是一个高级工具，会自动完成：1)查询设计规范，2)运行仿真，3)评判结果，4)保存所有数据。当用户说'优化模块A的时序'、'改进模块B的功耗'等需求时使用。",
    input_schema={
        "type": "object",
        "properties": {
            "module": {
                "type": "string",
                "description": "要优化的模块名称，如'模块A'、'模块B'、'模块C'等"
            },
            "target": {
                "type": "object",
                "description": "优化目标，包含指标名称、运算符和目标值",
                "properties": {
                    "metric": {
                        "type": "string",
                        "description": "要优化的指标，如'timing'（时序）、'power'（功耗）、'area'（面积）"
                    },
                    "operator": {
                        "type": "string",
                        "description": "比较运算符，支持'<', '<=', '>', '>=', '=='"
                    },
                    "value": {
                        "type": "string",
                        "description": "目标值，如'10ns'、'50mW'、'1000um²'"
                    }
                },
                "required": ["metric", "operator", "value"]
            }
        },
        "required": ["module", "target"]
    }
)


# =============================================================================
# 工具注册和辅助函数
# =============================================================================

def get_tool_schemas() -> list:
    """获取所有工具的 schema 列表"""
    return [
        query_knowledge_schema,
        run_simulation_schema,
        evaluate_result_schema,
        save_result_schema,
        query_history_schema,
        optimize_design_schema,
    ]


def run_tool(tool_name: str, tool_input: Dict) -> Any:
    """执行指定的工具

    Args:
        tool_name: 工具名称
        tool_input: 工具输入参数

    Returns:
        工具执行结果
    """
    tools_map = {
        "query_knowledge": query_knowledge,
        "run_simulation": run_simulation,
        "evaluate_result": evaluate_result,
        "save_result": save_result,
        "query_history": query_history,
        "optimize_design": optimize_design,
    }

    tool_func = tools_map.get(tool_name)
    if not tool_func:
        raise ValueError(f"未知的工具: {tool_name}")

    return tool_func(**tool_input)


# 测试代码
if __name__ == "__main__":
    print("=== 测试 EDA Tools ===\n")

    # 测试1：查询知识
    print("测试1：查询模块A的设计规范")
    result1 = query_knowledge("模块A")
    print(f"规范: {result1['specification']}")

    # 测试2：运行仿真
    print("\n测试2：运行模块A仿真")
    result2 = run_simulation("模块A")
    print(f"仿真结果: {result2}")

    # 测试3：评判结果
    print("\n测试3：评判结果")
    goal = {"metric": "timing", "operator": "<", "value": "10ns"}
    actual = {"timing": "12ns", "power": "50mW"}
    result3 = evaluate_result(goal, actual)
    print(f"评判结果: {result3}")

    # 测试4：保存结果
    print("\n测试4：保存结果")
    result4 = save_result({"test": "data", "module": "模块A"})
    print(f"保存结果: {result4}")

    # 测试5：查询历史
    print("\n测试5：查询历史")
    result5 = query_history({"module": "模块A"})
    print(f"历史记录数: {result5.get('count', 0)}")

    # 测试6：完整优化流程
    print("\n测试6：完整优化流程")
    target = {"metric": "timing", "operator": "<", "value": "10ns"}
    result6 = optimize_design("模块A", target)
    print(f"优化结果: {result6['status']}")
    print(f"评判: {result6['evaluation']['status']}")
