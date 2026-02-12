"""Evaluation Agent - 评判Agent（MVP简化版）

职责：对比用户目标和仿真结果，给出PASS/FAIL判断
"""
from typing import Dict, Optional


class EvaluationAgent:
    """评判Agent - 最简化版本，只做单指标数值对比"""

    def evaluate(self, goal: Dict, actual: Dict) -> Dict:
        """
        对比目标和实际结果

        参数:
            goal: {"metric": "timing", "operator": "<", "value": "10ns"}
            actual: {"timing": "12ns", "power": "50mW"}

        返回:
            {
                "status": "PASS" | "FAIL",
                "reason": str,
                "comparison": {"target": str, "actual": str, "gap": str}
            }
        """
        # 提取指标
        metric = goal.get("metric")
        target_value_str = goal.get("value")
        operator = goal.get("operator")

        # 提取实际值
        actual_value_str = actual.get(metric)

        if not actual_value_str:
            return {
                "status": "ERROR",
                "reason": f"缺少指标{metric}的实际值",
                "comparison": {"target": target_value_str, "actual": "N/A"}
            }

        # 解析数值（去掉单位）
        target_value = float(target_value_str[:-2])  # "10ns" -> 10.0
        actual_value = float(actual_value_str[:-2])  # "12ns" -> 12.0

        # 根据操作符对比
        passed = self._compare(actual_value, operator, target_value)

        # 生成原因
        if passed:
            reason = f"实际{actual_value_str}满足目标{target_value_str}"
            suggestion = None
        else:
            gap = actual_value - target_value
            gap_ratio = (gap / target_value) * 100
            reason = f"实际{actual_value_str}未达目标{target_value_str}，差距{gap:+.1f}({gap_ratio:+.1f}%)"

            # 生成简单建议
            if gap_ratio > 20:  # 差距>20%
                suggestion = f"差距较大({gap_ratio:.1f}%)，建议检查参数或工具配置"
            elif gap_ratio > 10:  # 差距10-20%
                suggestion = f"接近目标，微调参数可能达标（差距{gap:.1f}）"
            else:  # 差距<10%
                suggestion = f"基本达标，微调即可（差距{gap:.1f}）"

        return {
            "status": "PASS" if passed else "FAIL",
            "reason": reason,
            "comparison": {
                "target": target_value_str,
                "actual": actual_value_str,
                "gap": f"{gap:+.1f}" if operator in ["<", "<="] else f"{abs(gap):.1f}"
            },
            "suggestion": suggestion
        }

    def _compare(self, actual: float, operator: str, target: float) -> bool:
        """
        数值对比

        参数:
            actual: 实际值
            operator: 操作符（<, <=, >, >=, ==）
            target: 目标值

        返回:
            True/False
        """
        if operator == "<":
            return actual < target
        elif operator == "<=":
            return actual <= target
        elif operator == ">":
            return actual > target
        elif operator == ">=":
            return actual >= target
        elif operator == "==":
            return actual == target
        else:
            raise ValueError(f"不支持的操作符: {operator}")


# 测试代码
if __name__ == "__main__":
    # 创建Evaluation Agent实例
    evaluator = EvaluationAgent()

    # 测试1：达标情况
    print("=== 测试1：达标情况 ===")
    goal1 = {"metric": "timing", "operator": "<", "value": "10ns"}
    actual1 = {"timing": "9ns", "power": "50mW"}
    result1 = evaluator.evaluate(goal1, actual1)
    print(f"状态: {result1['status']}")
    print(f"原因: {result1['reason']}")
    print(f"建议: {result1.get('suggestion', '无')}")

    # 测试2：未达标（差距大）
    print("\n=== 测试2：未达标（差距大）===")
    goal2 = {"metric": "timing", "operator": "<", "value": "10ns"}
    actual2 = {"timing": "13ns", "power": "55mW"}
    result2 = evaluator.evaluate(goal2, actual2)
    print(f"状态: {result2['status']}")
    print(f"原因: {result2['reason']}")
    print(f"建议: {result2['suggestion']}")

    # 测试3：未达标（差距小）
    print("\n=== 测试3：未达标（差距小）===")
    goal3 = {"metric": "timing", "operator": "<", "value": "10ns"}
    actual3 = {"timing": "11ns", "power": "48mW"}
    result3 = evaluator.evaluate(goal3, actual3)
    print(f"状态: {result3['status']}")
    print(f"原因: {result3['reason']}")
    print(f"建议: {result3['suggestion']}")
