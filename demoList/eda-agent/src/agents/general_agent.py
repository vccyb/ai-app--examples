"""General Agent - 通用处理Agent（MVP简化版）

职责：数据保存和查询，当前用Python内存字典存储
"""
from typing import Dict, List, Optional


class GeneralAgent:
    """通用Agent - 最简化版本，只做内存存储"""

    def __init__(self):
        """初始化内存数据库"""
        # 任务列表（内存存储）
        self.tasks = []
        # 仿真结果列表
        self.simulation_results = []
        # 评判历史列表
        self.evaluations = []

    def save(self, data: Dict) -> str:
        """
        保存数据到内存

        参数:
            data: 要保存的数据字典

        返回:
            保存ID字符串
        """
        # 生成ID
        record_id = f"record_{len(self.tasks) + 1}"

        # 保存到相应列表
        if "task" in str(data) or "module" in data:
            self.tasks.append({**data, "id": record_id})
        elif "simulation_result" in data or "metrics" in data:
            self.simulation_results.append({**data, "id": record_id})
        elif "evaluation" in data or "status" in data:
            self.evaluations.append({**data, "id": record_id})
        else:
            self.tasks.append({**data, "id": record_id})

        print(f"[General] 已保存，ID: {record_id}")
        return f"已保存，ID: {record_id}"

    def query(self, filters: Optional[Dict] = None) -> List[Dict]:
        """
        查询内存数据

        参数:
            filters: 可选的过滤条件，如 {"module": "模块A"}

        返回:
            匹配的数据列表
        """
        print(f"[General] 查询数据，过滤: {filters}")

        # 没有过滤条件，返回所有
        if not filters:
            return {
                "count": len(self.tasks),
                "records": self.tasks
            }

        # 简单过滤（只支持module过滤）
        module = filters.get("module")
        if not module:
            return {"count": 0, "records": []}

        # 过滤并返回
        filtered = [t for t in self.tasks if t.get("module") == module]
        return {
            "count": len(filtered),
            "records": filtered
        }

    def get_stats(self) -> Dict:
        """
        获取统计信息

        返回:
            各类数据的统计
        """
        return {
            "total_tasks": len(self.tasks),
            "total_simulations": len(self.simulation_results),
            "total_evaluations": len(self.evaluations),
            "total_records": len(self.tasks)
        }


# 测试代码
if __name__ == "__main__":
    # 创建General Agent实例
    general_agent = GeneralAgent()

    # 测试1：保存任务
    print("=== 测试1：保存任务 ===")
    id1 = general_agent.save({"task": "优化模块A时序", "module": "模块A", "target": "10ns"})
    print(id1)

    # 测试2：保存仿真结果
    print("\n=== 测试2：保存仿真结果 ===")
    id2 = general_agent.save({"simulation_result": "已完成", "metrics": {"timing": "12ns", "power": "50mW"}})
    print(id2)

    # 测试3：保存评判结果
    print("\n=== 测试3：保存评判结果 ===")
    id3 = general_agent.save({"evaluation": "FAIL", "reason": "未达目标", "module": "模块A"})
    print(id3)

    # 测试4：查询数据
    print("\n=== 测试4：查询数据 ===")
    result = general_agent.query({"module": "模块A"})
    print(f"找到 {result['count']}条记录:")
    for record in result["records"][:3]:  # 只打印前3条
        print(f"  - {record.get('task', record.get('simulation_result', 'N/A'))}")

    # 测试5：获取统计
    print("\n=== 测试5：获取统计 ===")
    stats = general_agent.get_stats()
    print(f"总任务数: {stats['total_tasks']}")
    print(f"总仿真数: {stats['total_simulations']}")
    print(f"总评判数: {stats['total_evaluations']}")
