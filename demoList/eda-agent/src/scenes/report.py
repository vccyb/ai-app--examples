"""Report Scene - 报告场景（示例场景）

负责：
- 查询历史记录
- 汇总数据
- 生成报告
"""
from typing import Dict, List, Optional, Generator
import sys
import os

# 导入基类
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from scenes.base import BaseScene


class ReportScene(BaseScene):
    """报告场景

    生成设计验证和优化报告
    """

    def __init__(self, services: Dict):
        """初始化报告场景

        Args:
            services: 服务字典
        """
        super().__init__(
            name="report",
            description="报告场景 - 生成和导出设计报告",
            keywords=["报告", "report", "导出", "export", "总结", "summary"],
            services=services
        )

    def match(self, user_input: str) -> float:
        """计算匹配度"""
        return self._keyword_match_score(user_input)

    def run(self, user_input: str) -> Generator[Dict, None, None]:
        """执行报告场景

        Args:
            user_input: 用户输入

        Yields:
            执行过程中的消息
        """
        # 1. 解析报告类型
        yield self._create_info_message("正在解析报告需求...")
        report_type = self._parse_report_type(user_input)

        # 2. 查询历史数据
        yield self._create_info_message("\n正在查询历史数据...")
        history = self.state_service.get_history(limit=10)

        total_count = history["count"]
        yield self._create_info_message(f"找到 {total_count} 条记录")

        # 3. 汇总并生成报告
        yield self._create_info_message("\n正在生成报告...")
        report = self._generate_report(history, report_type)

        yield self._create_done_message({
            "report_type": report_type,
            "summary": {
                "total_tasks": total_count,
                "tasks": len(history["tasks"]),
                "simulations": len(history["simulations"]),
                "evaluations": len(history["evaluations"])
            }
        })

    def _parse_report_type(self, user_input: str) -> str:
        """解析报告类型

        Args:
            user_input: 用户输入

        Returns:
            报告类型
        """
        user_input_lower = user_input.lower()

        if any(word in user_input_lower for word in ["验证", "verify"]):
            return "verification"
        elif any(word in user_input_lower for word in ["优化", "optimize"]):
            return "optimization"
        elif any(word in user_input_lower for word in ["汇总", "summary", "全部", "all"]):
            return "summary"
        else:
            return "general"

    def _generate_report(self, history: Dict, report_type: str) -> Dict:
        """生成报告内容

        Args:
            history: 历史数据
            report_type: 报告类型

        Returns:
            报告内容
        """
        report = {
            "type": report_type,
            "generated_at": history.get("generated_at", "N/A"),
            "sections": []
        }

        # 根据类型生成不同报告
        if report_type == "verification":
            report["sections"] = self._generate_verification_report(history)
        elif report_type == "optimization":
            report["sections"] = self._generate_optimization_report(history)
        else:
            report["sections"] = self._generate_general_report(history)

        return report

    def _generate_verification_report(self, history: Dict) -> List[Dict]:
        """生成验证报告"""
        sections = []

        # 任务列表
        sections.append({
            "title": "验证任务列表",
            "content": [
                {
                    "task_id": task["id"],
                    "module": task.get("module"),
                    "status": task.get("status"),
                    "created_at": task.get("created_at")
                }
                for task in history["tasks"]
            ]
        })

        # 评估结果统计
        eval_results = history["evaluations"]
        pass_count = sum(1 for e in eval_results if e.get("status") == "PASS")
        fail_count = sum(1 for e in eval_results if e.get("status") == "FAIL")

        sections.append({
            "title": "评估结果统计",
            "content": {
                "总计": len(eval_results),
                "通过": pass_count,
                "失败": fail_count,
                "通过率": f"{pass_count/len(eval_results)*100:.1f}%" if eval_results else "N/A"
            }
        })

        return sections

    def _generate_optimization_report(self, history: Dict) -> List[Dict]:
        """生成优化报告"""
        sections = []

        # 仿真结果汇总
        sim_results = history["simulations"]

        # 按模块分组
        module_stats = {}
        for sim in sim_results:
            module = sim.get("module", "unknown")
            if module not in module_stats:
                module_stats[module] = []

            module_stats[module].append(sim.get("result", {}))

        sections.append({
            "title": "模块仿真统计",
            "content": [
                {
                    "module": module,
                    "仿真次数": len(results),
                    "最新结果": results[-1] if results else {}
                }
                for module, results in module_stats.items()
            ]
        })

        return sections

    def _generate_general_report(self, history: Dict) -> List[Dict]:
        """生成通用报告"""
        sections = []

        # 概览
        sections.append({
            "title": "数据概览",
            "content": {
                "任务总数": len(history["tasks"]),
                "仿真总数": len(history["simulations"]),
                "评估总数": len(history["evaluations"])
            }
        })

        # 最近活动
        sections.append({
            "title": "最近任务",
            "content": history["tasks"][:5]
        })

        return sections


# ============================================================================
# 测试代码
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("Report Scene 测试")
    print("=" * 70)

    # 创建模拟服务
    class MockStateService:
        def get_history(self, limit=10):
            return {
                "tasks": [
                    {"id": "t1", "module": "模块A", "status": "done", "created_at": "2024-01-01"},
                    {"id": "t2", "module": "模块B", "status": "done", "created_at": "2024-01-02"}
                ],
                "simulations": [],
                "evaluations": [],
                "count": 2
            }

    services = {"state": MockStateService()}

    # 创建报告场景
    report_scene = ReportScene(services)

    # 测试 match
    print("\n测试1：匹配度计算")
    score1 = report_scene.match("生成设计报告")
    print(f"匹配分数: {score1}")

    score2 = report_scene.match("验证模块A")
    print(f"匹配分数: {score2}")

    # 测试解析报告类型
    print("\n测试2：解析报告类型")
    type1 = report_scene._parse_report_type("生成验证报告")
    print(f"报告类型: {type1}")

    type2 = report_scene._parse_report_type("导出所有数据")
    print(f"报告类型: {type2}")

    # 测试生成报告
    print("\n测试3：生成报告")
    history = services["state"].get_history()
    report = report_scene._generate_report(history, "verification")
    print(f"报告章节数: {len(report['sections'])}")

    print("\n测试完成")
