"""State Service - 状态持久化服务

负责：
- JSON 文件持久化
- 数据的保存、查询、历史记录
"""
import json
import os
from typing import Dict, List, Optional, Any
from datetime import datetime


class StateService:
    """状态持久化服务

    使用 JSON 文件存储所有状态数据
    """

    def __init__(self, state_file: str = "data/state.json"):
        """初始化状态服务

        Args:
            state_file: 状态文件路径
        """
        self.state_file = state_file
        self._ensure_state_file()
        self._data = self._load_state()

    def _ensure_state_file(self):
        """确保状态文件存在"""
        os.makedirs(os.path.dirname(self.state_file), exist_ok=True)
        if not os.path.exists(self.state_file):
            self._save_state({
                "tasks": [],
                "simulations": [],
                "evaluations": []
            })

    def _load_state(self) -> Dict:
        """加载状态数据"""
        try:
            with open(self.state_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {
                "tasks": [],
                "simulations": [],
                "evaluations": []
            }

    def _save_state(self, data: Dict):
        """保存状态数据到文件"""
        with open(self.state_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    # ========================================================================
    # 公共 API
    # ========================================================================

    def save(self, data: Dict, data_type: str = "task") -> Dict:
        """保存数据到状态

        Args:
            data: 要保存的数据字典
            data_type: 数据类型 ("task", "simulation", "evaluation")

        Returns:
            保存结果，包含记录 ID
        """
        # 生成唯一 ID
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        record_id = f"{data_type}_{timestamp}_{len(self._data[data_type + 's'])}"

        # 创建记录
        record = {
            "id": record_id,
            "created_at": datetime.now().isoformat(),
            **data
        }

        # 保存到对应列表
        self._data[data_type + "s"].append(record)
        self._save_state(self._data)

        return {
            "status": "SUCCESS",
            "record_id": record_id,
            "data_type": data_type
        }

    def query(self, filters: Optional[Dict] = None) -> Dict:
        """查询历史记录

        Args:
            filters: 过滤条件，如 {"module": "模块A"}

        Returns:
            查询结果
        """
        results = {
            "tasks": self._data["tasks"],
            "simulations": self._data["simulations"],
            "evaluations": self._data["evaluations"]
        }

        # 应用过滤条件
        if filters:
            for key, value in filters.items():
                for data_type in ["tasks", "simulations", "evaluations"]:
                    results[data_type] = [
                        record for record in self._data[data_type]
                        if record.get(key) == value
                    ]

        # 统计数量
        results["count"] = {
            "tasks": len(results["tasks"]),
            "simulations": len(results["simulations"]),
            "evaluations": len(results["evaluations"]),
            "total": len(results["tasks"]) + len(results["simulations"]) + len(results["evaluations"])
        }

        return results

    def get_history(self, limit: int = 10) -> Dict:
        """获取最近的历史记录

        Args:
            limit: 返回记录数量限制

        Returns:
            最近的历史记录
        """
        # 获取最近的任务
        recent_tasks = sorted(
            self._data["tasks"],
            key=lambda x: x.get("created_at", ""),
            reverse=True
        )[:limit]

        # 关联的仿真和评估结果
        task_ids = {task["id"] for task in recent_tasks}

        related_simulations = [
            sim for sim in self._data["simulations"]
            if sim.get("task_id") in task_ids
        ]

        related_evaluations = [
            eva for eva in self._data["evaluations"]
            if eva.get("task_id") in task_ids
        ]

        return {
            "tasks": recent_tasks,
            "simulations": related_simulations,
            "evaluations": related_evaluations,
            "count": len(recent_tasks)
        }

    def clear_all(self) -> Dict:
        """清空所有数据"""
        self._data = {
            "tasks": [],
            "simulations": [],
            "evaluations": []
        }
        self._save_state(self._data)

        return {
            "status": "SUCCESS",
            "message": "所有历史数据已清空"
        }


# ============================================================================
# 测试代码
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("State Service 测试")
    print("=" * 70)

    # 创建服务实例
    state_service = StateService("data/test_state.json")

    # 测试保存
    print("\n测试1：保存任务记录")
    result1 = state_service.save({
        "input": "测试输入",
        "scene": "verify",
        "status": "done"
    }, data_type="task")
    print(f"保存结果: {result1}")

    # 测试查询
    print("\n测试2：查询历史")
    result2 = state_service.query({"scene": "verify"})
    print(f"查询结果数量: {result2['count']}")

    # 测试获取历史
    print("\n测试3：获取最近历史")
    result3 = state_service.get_history(limit=5)
    print(f"最近任务数: {result3['count']}")

    # 清理测试文件
    import os
    if os.path.exists("data/test_state.json"):
        os.remove("data/test_state.json")
    print("\n测试完成，测试文件已清理")
