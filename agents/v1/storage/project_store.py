"""
项目数据存储

管理 EDA 项目数据的持久化存储
"""
import json
from pathlib import Path
from typing import Dict, Optional, List
from datetime import datetime


class ProjectStore:
    """项目数据存储"""

    def __init__(self, storage_dir: str = "data/projects"):
        """
        初始化项目存储

        Args:
            storage_dir: 存储目录路径
        """
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)

    def save_project(self, project_data: Dict) -> str:
        """
        保存项目数据

        Args:
            project_data: 项目数据字典

        Returns:
            项目ID
        """
        project_id = project_data.get('project_id') or project_data.get('name', 'unknown')
        file_path = self.storage_dir / f"{project_id}.json"

        # 添加时间戳
        project_data['saved_at'] = datetime.now().isoformat()

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(project_data, f, ensure_ascii=False, indent=2)

        return project_id

    def load_project(self, project_id: str) -> Optional[Dict]:
        """
        加载项目数据

        Args:
            project_id: 项目ID

        Returns:
            项目数据字典，如果不存在则返回 None
        """
        file_path = self.storage_dir / f"{project_id}.json"

        if not file_path.exists():
            return None

        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def list_projects(self) -> List[str]:
        """
        列出所有项目

        Returns:
            项目ID列表
        """
        return [f.stem for f in self.storage_dir.glob("*.json")]

    def delete_project(self, project_id: str) -> bool:
        """
        删除项目

        Args:
            project_id: 项目ID

        Returns:
            是否成功删除
        """
        file_path = self.storage_dir / f"{project_id}.json"

        if file_path.exists():
            file_path.unlink()
            return True
        return False

    def project_exists(self, project_id: str) -> bool:
        """
        检查项目是否存在

        Args:
            project_id: 项目ID

        Returns:
            项目是否存在
        """
        return (self.storage_dir / f"{project_id}.json").exists()


# 全局存储实例
project_store = ProjectStore()
