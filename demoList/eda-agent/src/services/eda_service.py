"""EDA Service - EDA 仿真服务

负责：
- EDA 工具执行
- 仿真任务管理
- 预留真实 EDA 工具对接接口
"""
from typing import Dict, List, Optional
import sys
import os
import random

# 导入现有的 EDA Agent
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from agents.eda_agent import EDAToolAgent


class EDAService:
    """EDA 仿真服务

    封装现有的 EDA Tool Agent，提供统一接口
    """

    def __init__(self):
        """初始化 EDA 服务"""
        self.eda_agent = EDAToolAgent()

    def simulate(self, module: str, parameters: Optional[Dict] = None) -> Dict:
        """运行仿真

        Args:
            module: 模块名称
            parameters: 可选的仿真参数

        Returns:
            仿真结果
        """
        result = self.eda_agent.run_simulation(module, parameters)

        return {
            "module": module,
            "parameters": parameters or {},
            "result": result,
            "status": "SUCCESS"
        }

    def get_status(self, task_id: Optional[str] = None) -> Dict:
        """获取仿真状态

        Args:
            task_id: 任务 ID（可选）

        Returns:
            仿真状态信息
        """
        # 当前版本是同步执行，状态直接返回
        return {
            "task_id": task_id or "unknown",
            "status": "completed",
            "message": "仿真已完成（同步执行）"
        }

    def batch_simulate(
        self,
        modules: List[str],
        parameters: Optional[Dict] = None
    ) -> List[Dict]:
        """批量运行仿真

        Args:
            modules: 模块列表
            parameters: 可选的仿真参数

        Returns:
            仿真结果列表
        """
        results = []
        for module in modules:
            result = self.simulate(module, parameters)
            results.append(result)

        return results

    def compare_results(self, result1: Dict, result2: Dict) -> Dict:
        """对比两个仿真结果

        Args:
            result1: 第一个结果
            result2: 第二个结果

        Returns:
            对比分析
        """
        comparison = {}

        # 对比各个指标
        for key in result1:
            if key in result2:
                val1 = self._extract_numeric_value(result1[key])
                val2 = self._extract_numeric_value(result2[key])

                if val1 is not None and val2 is not None:
                    diff = val2 - val1
                    pct_change = (diff / val1 * 100) if val1 != 0 else 0

                    comparison[key] = {
                        "result1": result1[key],
                        "result2": result2[key],
                        "difference": diff,
                        "percent_change": f"{pct_change:+.1f}%"
                    }

        return comparison

    def _extract_numeric_value(self, value: str) -> Optional[float]:
        """从字符串中提取数值"""
        import re

        if isinstance(value, (int, float)):
            return float(value)

        if isinstance(value, str):
            # 提取数字和单位
            match = re.search(r'([\d.]+)', value)
            if match:
                return float(match.group(1))

        return None


# ============================================================================
# 测试代码
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("EDA Service 测试")
    print("=" * 70)

    # 创建服务实例
    eda_service = EDAService()

    # 测试 simulate
    print("\n测试1：运行模块A仿真")
    result1 = eda_service.simulate("模块A")
    print(f"仿真结果: {result1['result']}")

    # 测试 get_status
    print("\n测试2：获取仿真状态")
    result2 = eda_service.get_status("test_task_1")
    print(f"状态: {result2['status']}")

    # 测试 batch_simulate
    print("\n测试3：批量仿真")
    result3 = eda_service.batch_simulate(["模块A", "模块B", "模块C"])
    print(f"批量仿真结果数: {len(result3)}")

    # 测试 compare_results
    print("\n测试4：对比结果")
    result4a = eda_service.simulate("模块A")["result"]
    result4b = eda_service.simulate("模块A")["result"]
    comparison = eda_service.compare_results(result4a, result4b)
    print(f"对比指标数: {len(comparison)}")

    print("\n测试完成")
