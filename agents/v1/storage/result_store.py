"""
工具执行结果存储

管理工具执行结果的持久化存储
"""
import json
from pathlib import Path
from typing import Dict, Optional, List
from datetime import datetime


class ResultStore:
    """工具执行结果存储"""

    def __init__(self, storage_dir: str = "data/results"):
        """
        初始化结果存储

        Args:
            storage_dir: 存储目录路径
        """
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)

    def save_result(self, tool_name: str, inputs: Dict, outputs: Dict, project_id: str = None) -> str:
        """
        保存工具执行结果

        Args:
            tool_name: 工具名称
            inputs: 输入参数
            outputs: 输出结果
            project_id: 关联的项目ID（可选）

        Returns:
            结果ID
        """
        timestamp = datetime.now()
        result_id = f"res_{tool_name}_{timestamp.strftime('%Y%m%d%H%M%S')}"

        result_data = {
            "result_id": result_id,
            "tool_name": tool_name,
            "timestamp": timestamp.isoformat(),
            "inputs": inputs,
            "outputs": outputs,
            "project_id": project_id
        }

        file_path = self.storage_dir / f"{result_id}.json"

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(result_data, f, ensure_ascii=False, indent=2)

        return result_id

    def load_result(self, result_id: str) -> Optional[Dict]:
        """
        加载结果数据

        Args:
            result_id: 结果ID

        Returns:
            结果数据字典，如果不存在则返回 None
        """
        file_path = self.storage_dir / f"{result_id}.json"

        if not file_path.exists():
            return None

        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def list_results(self, tool_name: str = None, project_id: str = None) -> List[Dict]:
        """
        列出结果

        Args:
            tool_name: 过滤工具名称（可选）
            project_id: 过滤项目ID（可选）

        Returns:
            结果数据列表
        """
        results = []

        for file_path in self.storage_dir.glob("*.json"):
            with open(file_path, 'r', encoding='utf-8') as f:
                result = json.load(f)

            # 应用过滤条件
            if tool_name and result.get('tool_name') != tool_name:
                continue
            if project_id and result.get('project_id') != project_id:
                continue

            results.append(result)

        # 按时间排序
        results.sort(key=lambda x: x.get('timestamp', ''), reverse=True)

        return results

    def get_results_by_project(self, project_id: str) -> List[Dict]:
        """
        获取项目的所有结果

        Args:
            project_id: 项目ID

        Returns:
            该项目的所有结果
        """
        return self.list_results(project_id=project_id)

    def get_results_by_tool(self, tool_name: str) -> List[Dict]:
        """
        获取工具的所有结果

        Args:
            tool_name: 工具名称

        Returns:
            该工具的所有结果
        """
        return self.list_results(tool_name=tool_name)


# 全局存储实例
result_store = ResultStore()
