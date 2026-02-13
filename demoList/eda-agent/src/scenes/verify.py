"""Verify Scene - 验证场景

负责：
- 解析验证目标（模块 + 指标 + 阈值）
- 生成执行计划
- 执行验证流程（查询 → 仿真 → 评估 → 保存）
- 失败时询问是否迭代优化
"""
from typing import Dict, List, Optional, Generator
import re
import sys
import os

# 导入基类和服务
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from scenes.base import BaseScene
from agents.evaluation_agent import EvaluationAgent


class VerifyScene(BaseScene):
    """验证场景

    解析用户的验证需求并执行验证流程
    """

    def __init__(self, services: Dict):
        """初始化验证场景

        Args:
            services: 服务字典
        """
        super().__init__(
            name="verify",
            description="验证场景 - 验证模块是否达到设计目标",
            keywords=["验证", "verify", "优化", "optimize", "测试", "test"],
            services=services
        )
        self.evaluation_agent = EvaluationAgent()

    def match(self, user_input: str) -> float:
        """计算匹配度"""
        # 使用关键词匹配
        base_score = self._keyword_match_score(user_input)

        # 额外检查是否包含模块名和目标
        has_module = any(f"模块{chr(c)}" in user_input or f"module{chr(c+32)}" in user_input.lower() for c in range(ord('A'), ord('D')+1))
        has_target = any(op in user_input for op in ["<", ">", "<=", ">=", "=="])

        # 如果包含目标格式，大幅提高匹配度
        if has_target and has_module:
            # 完整的验证格式（模块+目标）应该有很高的匹配度
            base_score = min(base_score * 2.5, 1.0)
        elif has_target:
            base_score = min(base_score * 2.0, 1.0)

        return base_score

    def run(self, user_input: str) -> Generator[Dict, None, None]:
        """执行验证场景

        Args:
            user_input: 用户输入

        Yields:
            执行过程中的消息
        """
        # 1. 解析任务
        yield self._create_info_message("正在解析验证任务...")
        task = self._parse_task(user_input)

        if not task:
            yield self._create_error_message(f"无法解析任务：{user_input}")
            return

        yield self._create_info_message(f"解析任务：")
        yield self._create_info_message(f"  - 模块: {task['module']}")
        yield self._create_info_message(f"  - 指标: {task['goal']['metric']}")
        yield self._create_info_message(f"  - 目标: {task['goal']['operator']} {task['goal']['value']}")

        # 2. 生成执行计划
        yield self._create_info_message("\n正在生成执行计划...")
        plan = self._generate_plan(task)
        yield self._create_plan_message(plan["steps"], plan.get("need_confirm", True))

        # 3. 执行验证流程
        result = yield from self._execute_verification(task)
        yield self._create_done_message(result)

    def _parse_task(self, user_input: str) -> Optional[Dict]:
        """解析用户输入为任务

        Args:
            user_input: 用户输入

        Returns:
            任务字典或 None
        """
        # 首先尝试简单的正则解析
        task = self._simple_parse(user_input)

        # 如果简单解析失败，使用 LLM 进行智能解析
        if not task and self.llm_service:
            print(f"[VerifyScene] 简单解析失败，尝试使用 LLM 进行智能解析...")
            task = self._llm_parse(user_input)

        return task

    def _simple_parse(self, user_input: str) -> Optional[Dict]:
        """使用正则表达式进行简单解析

        Args:
            user_input: 用户输入

        Returns:
            任务字典或 None
        """
        task = {
            "action": "verify",
            "module": None,
            "goal": None
        }

        # 提取模块名（寻找"模块X"或"moduleX"，允许有空格）
        module_match = re.search(r'模块\s*([A-D])', user_input)
        if module_match:
            task["module"] = f"模块{module_match.group(1)}"

        # 提取目标（寻找"指标<值"格式）
        # 支持格式：timing<10ns, power<50mW, area<1000um²
        # 允许中间有"是否"等分隔词
        # 正则：指标名 + 可选的"是否" + 运算符 + 值
        # 为了分组清晰，使用 (?:...) 不捕获"是否"
        goal_pattern = r'(timing|power|area|时序|功耗|面积)(?:是否)?\s*([<>=!]+)\s*(\S+)'
        goal_match = re.search(goal_pattern, user_input)

        if goal_match:
            metric_map = {
                "timing": "timing", "时序": "timing",
                "power": "power", "功耗": "power",
                "area": "area", "面积": "area"
            }

            metric = goal_match.group(1)  # 指标名
            operator = goal_match.group(2)  # 运算符（组2）
            value = goal_match.group(3).strip()  # 值（组3）

            task["goal"] = {
                "metric": metric_map.get(metric, metric),
                "operator": operator,
                "value": value
            }

        # 验证必要字段
        if task["module"]:
            # 有模块名就算部分成功（可能是查询规范）
            return task

        return None

    def _llm_parse(self, user_input: str) -> Optional[Dict]:
        """使用 LLM 进行智能解析

        Args:
            user_input: 用户输入

        Returns:
            任务字典或 None
        """
        import json

        prompt = f"""请将以下用户输入解析为 EDA 验证任务。

用户输入：{user_input}

请返回 JSON 格式，只返回 JSON，不要其他内容：
{{
  "module": "模块名称（如：模块A、模块B、模块C）",
  "goal": {{
    "metric": "指标名称（timing/power/area）",
    "operator": "比较符（<, <=, >, >=, ==）",
    "value": "目标值（如：10ns, 50mW, 1000um²）"
  }}
}}

注意：
1. 如果用户没有提到具体目标值（如"查询模块B的设计规范"），则 goal 字段为 null
2. 模块名必须提取
3. 如果无法确定模块或指标，返回 null
"""

        messages = [{"role": "user", "content": prompt}]

        try:
            response = self.llm_service.chat(messages, temperature=0.3)
            response_text = self.llm_service._extract_response_text(response)

            # 尝试解析 JSON
            try:
                parsed = json.loads(response_text)

                # 验证和标准化返回的结果
                task = {
                    "action": "verify",
                    "module": None,
                    "goal": None
                }

                # 处理模块名
                if "module" in parsed:
                    module = parsed["module"]
                    # 标准化模块名格式
                    if re.match(r'^[A-D]$', module):
                        task["module"] = f"模块{module}"
                    elif re.match(r'^模块[A-D]$', module):
                        task["module"] = module
                    else:
                        task["module"] = module

                # 处理目标
                if "goal" in parsed and parsed["goal"]:
                    goal = parsed["goal"]

                    # 标准化指标名
                    metric_map = {
                        "时序": "timing", "timing": "timing",
                        "功耗": "power", "power": "power",
                        "面积": "area", "area": "area"
                    }
                    metric = metric_map.get(goal.get("metric"), goal.get("metric"))

                    # 标准化单位
                    value = goal.get("value", "")
                    if not re.search(r'\d+[a-z]+$', value):
                        # 尝试添加单位（如果是数字）
                        if metric == "timing":
                            value = f"{value}ns"
                        elif metric == "power":
                            value = f"{value}mW"
                        elif metric == "area":
                            value = f"{value}um²"

                    task["goal"] = {
                        "metric": metric,
                        "operator": goal.get("operator", "<"),
                        "value": value
                    }

                # 验证至少有模块名
                if task["module"]:
                    print(f"[VerifyScene] ✓ LLM 智能解析成功")
                    return task
                else:
                    print(f"[VerifyScene] ✗ LLM 解析结果缺少模块名")
                    return None

            except json.JSONDecodeError as e:
                print(f"[VerifyScene] ✗ 无法解析 LLM 返回的 JSON: {e}")
                print(f"[VerifyScene]   LLM 响应: {response_text[:200]}...")
                return None

        except Exception as e:
            print(f"[VerifyScene] ✗ LLM 解析调用失败: {str(e)}")
            return None

    def _generate_plan(self, task: Dict) -> Dict:
        """生成执行计划

        Args:
            task: 任务字典

        Returns:
            计划字典
        """
        module = task["module"]
        goal = task["goal"]

        # 使用 LLM 生成计划（如果可用）
        if self.llm_service:
            try:
                plan = self.llm_service.generate_plan(
                    task_description=f"验证{module}的{goal['metric']}是否{goal['operator']}{goal['value']}",
                    context={"task": task}
                )
                return plan
            except:
                pass  # LLM 调用失败，使用默认计划

        # 默认计划
        steps = [
            {"step": 1, "action": "查询规范", "description": f"查询{module}的设计规范"},
            {"step": 2, "action": "运行仿真", "description": f"运行{module}仿真获取实际指标"},
            {"step": 3, "action": "评估结果", "description": f"判断{goal['metric']}是否{goal['operator']}{goal['value']}"}
        ]

        return {"steps": steps, "need_confirm": True}

    def _execute_verification(self, task: Dict) -> Generator[Dict, None, None]:
        """执行验证流程

        Args:
            task: 任务字典

        Yields:
            步骤结果消息
        """
        module = task["module"]
        goal = task["goal"]
        results = {}

        # 步骤1：查询规范
        yield self._create_info_message(f"\n[执行] 步骤1: 查询规范...")
        spec_result = self.rag_service.get_specification(module)
        results["specification"] = spec_result["specification"]

        yield self._create_step_result_message(
            step=1,
            result={"规范": f"已获取{module}设计规范"},
            status="SUCCESS"
        )

        # 步骤2：运行仿真
        yield self._create_info_message(f"\n[执行] 步骤2: 运行仿真...")
        sim_result = self.eda_service.simulate(module)
        results["simulation"] = sim_result["result"]

        actual_result = sim_result["result"]
        yield self._create_step_result_message(
            step=2,
            result=actual_result,
            status="SUCCESS"
        )

        # 步骤3：评估结果
        yield self._create_info_message(f"\n[执行] 步骤3: 评估结果...")
        eval_result = self.evaluation_agent.evaluate(goal, actual_result)
        results["evaluation"] = eval_result

        yield self._create_step_result_message(
            step=3,
            result=eval_result,
            status=eval_result.get("status", "UNKNOWN")
        )

        # 保存结果
        task_id = f"{module}_{goal['metric']}_verify"
        self.state_service.save({
            "task_id": task_id,
            "input": f"验证{module}{goal['metric']}",
            "module": module,
            "scene": "verify",
            "status": eval_result.get("status", "UNKNOWN")
        }, data_type="task")

        self.state_service.save({
            "task_id": task_id,
            "module": module,
            **actual_result
        }, data_type="simulation")

        self.state_service.save({
            "task_id": task_id,
            "goal": goal,
            "actual": actual_result,
            **eval_result
        }, data_type="evaluation")

        # 检查是否达标
        if eval_result.get("status") == "FAIL":
            # 失败时询问是否迭代
            yield self._create_ask_message(
                question=eval_result.get("reason", "") + "\n是否调整参数重试？",
                options=["是", "否", "建议"]
            )
            # 注意：这里的响应需要由控制器处理并返回给场景
            # 当前简化版本暂时不处理响应

        return results


# ============================================================================
# 测试代码
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("Verify Scene 测试")
    print("=" * 70)

    # 创建模拟服务
    class MockLLMService:
        def generate_plan(self, task_description, context):
            return {
                "steps": [
                    {"step": 1, "action": "query", "description": "查询规范"},
                    {"step": 2, "action": "simulate", "description": "运行仿真"},
                    {"step": 3, "action": "evaluate", "description": "评估结果"}
                ],
                "need_confirm": True
            }

    services = {
        "llm": MockLLMService(),
        "rag": None,  # 需要真实实例
        "eda": None,  # 需要真实实例
        "state": None  # 需要真实实例
    }

    # 创建验证场景
    verify_scene = VerifyScene(services)

    # 测试 match
    print("\n测试1：匹配度计算")
    score1 = verify_scene.match("验证模块A时序<10ns")
    print(f"匹配分数: {score1}")

    score2 = verify_scene.match("今天天气怎么样")
    print(f"匹配分数: {score2}")

    # 测试解析任务
    print("\n测试2：解析任务")
    task1 = verify_scene._parse_task("验证模块A时序<10ns")
    print(f"解析结果: {task1}")

    task2 = verify_scene._parse_task("优化模块B的功耗")
    print(f"解析结果: {task2}")

    print("\n测试完成（完整测试需要真实服务）")
