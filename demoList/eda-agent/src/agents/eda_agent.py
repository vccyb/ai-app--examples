"""EDA Tool Agent - EDA工具执行Agent（MVP简化版）

职责：执行EDA仿真（当前Mock版本，返回固定结果）
"""
import random
from typing import Dict, Optional


class EDAToolAgent:
    """EDA工具执行Agent - 最简化版本"""

    def run_simulation(self, module: str, parameters: Optional[Dict] = None) -> Dict:
        """
        运行EDA仿真，返回结果

        参数:
            module: 模块名称，如 "模块A"
            parameters: 可选参数（MVP阶段忽略，后期对接真实工具时使用）

        返回:
            仿真结果字典，包含timing, power, area等指标
        """
        print(f"[EDA Tool] 开始仿真: {module}")

        # 固定基准结果（可以加一点随机变化模拟"优化效果"）
        base_results = {
            "模块A": {"timing": "12ns", "power": "50mW", "area": "1000um²"},
            "模块B": {"timing": "8ns", "power": "70mW", "area": "1200um²"},
            "模块C": {"timing": "15ns", "power": "40mW", "area": "800um²"}
        }

        # 获取基准结果
        result = base_results.get(module, base_results["模块A"])

        # 加一点随机变化（±5%），模拟"优化"效果
        variation = random.uniform(0.95, 1.05)

        # 应用变化
        result_timing = float(result['timing'][:-2]) * variation
        result_power = float(result['power'][:-2]) * variation

        result = {
            "timing": f"{result_timing:.1f}ns",
            "power": f"{result_power:.1f}mW",
            "area": result["area"]
        }

        print(f"[EDA Tool] 仿真完成: {result}")
        return result

    def get_tool_status(self) -> Dict:
        """
        获取工具状态（简化版，返回固定状态）

        返回:
            工具状态字典
        """
        return {
            "tool_name": "MockEDA",
            "status": "ready",
            "supported_modules": ["模块A", "模块B", "模块C"],
            "version": "1.0.0-mvp"
        }


# 测试代码
if __name__ == "__main__":
    # 创建EDA Tool Agent实例
    eda_agent = EDAToolAgent()

    # 测试1：仿真模块A
    print("=== 测试1：仿真模块A ===")
    result1 = eda_agent.run_simulation("模块A")
    print(f"时序: {result1['timing']}, 功耗: {result1['power']}, 面积: {result1['area']}")

    # 测试2：仿真模块B（带参数）
    print("\n=== 测试2：仿真模块B（带参数）===")
    result2 = eda_agent.run_simulation("模块B", parameters={"voltage": "0.9V"})
    print(f"时序: {result2['timing']}, 功耗: {result2['power']}")

    # 测试3：获取工具状态
    print("\n=== 测试3：获取工具状态 ===")
    status = eda_agent.get_tool_status()
    print(f"工具状态: {status['status']}, 支持模块: {status['supported_modules']}")
