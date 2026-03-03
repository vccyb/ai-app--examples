"""
Agent 定义加载器

从 Markdown 文件（YAML frontmatter）加载 Agent 定义
"""
import yaml
import glob
from pathlib import Path
from typing import Dict, Optional, List
from dataclasses import dataclass


@dataclass
class AgentDefinition:
    """Agent 定义"""
    name: str
    description: str
    prompt: str
    tools: List[str]
    metadata: Dict
    file_path: Path


class AgentLoader:
    """Agent 加载器"""

    def __init__(self, agents_dir: Optional[Path] = None):
        """
        初始化加载器

        Args:
            agents_dir: Agent 定义目录，默认为 .claude/agents/
        """
        if agents_dir is None:
            # 查找 .claude/agents/ 目录
            current_dir = Path.cwd()
            agents_dir = current_dir / ".claude" / "agents"

            # 如果不存在，尝试使用 agents/ 目录
            if not agents_dir.exists():
                agents_dir = current_dir / "agents"

        self.agents_dir = Path(agents_dir)
        self._agents_cache: Dict[str, AgentDefinition] = {}

    def load_all_agents(self) -> Dict[str, AgentDefinition]:
        """
        加载所有 Agent 定义

        Returns:
            Agent 名称 -> Agent 定义的映射
        """
        if self._agents_cache:
            return self._agents_cache

        pattern = str(self.agents_dir / "**/*.md")
        md_files = glob.glob(pattern, recursive=True)

        for md_file in md_files:
            md_path = Path(md_file)

            try:
                agent_def = self._parse_agent_file(md_path)
                if agent_def:
                    self._agents_cache[agent_def.name] = agent_def
                    print(f"✓ 加载 Agent: {agent_def.name} from {md_path.name}")
            except Exception as e:
                print(f"⚠ 跳过文件 {md_path.name}: {e}")

        print(f"\n共加载 {len(self._agents_cache)} 个 Agent")
        return self._agents_cache

    def _parse_agent_file(self, file_path: Path) -> Optional[AgentDefinition]:
        """
        解析 Agent 定义文件

        Args:
            file_path: Markdown 文件路径

        Returns:
            AgentDefinition，如果解析失败则返回 None
        """
        content = file_path.read_text(encoding='utf-8')

        # 检查是否有 YAML frontmatter
        if not content.startswith("---"):
            # 没有 YAML frontmatter，整个文件作为 prompt
            return AgentDefinition(
                name=file_path.stem,
                description=f"Agent from {file_path.name}",
                prompt=content,
                tools=[],
                metadata={},
                file_path=file_path
            )

        # 分离 frontmatter 和内容
        parts = content.split("---", 2)

        if len(parts) < 3:
            return None

        frontmatter = parts[1].strip()
        prompt = parts[2].strip()

        # 解析 YAML
        try:
            metadata = yaml.safe_load(frontmatter)
        except yaml.YAMLError as e:
            print(f"⚠ YAML 解析失败: {e}")
            return None

        # 提取字段
        name = metadata.get('name', file_path.stem)
        description = metadata.get('description', '')
        tools = metadata.get('tools', [])

        # 处理 tools 字段（可能是字符串或列表）
        if isinstance(tools, str):
            tools = [t.strip() for t in tools.split(',')]

        return AgentDefinition(
            name=name,
            description=description,
            prompt=prompt,
            tools=tools,
            metadata=metadata,
            file_path=file_path
        )

    def get_agent(self, name: str) -> Optional[AgentDefinition]:
        """
        获取指定 Agent 的定义

        Args:
            name: Agent 名称

        Returns:
            AgentDefinition，如果不存在则返回 None
        """
        if not self._agents_cache:
            self.load_all_agents()

        return self._agents_cache.get(name)

    def list_agents(self) -> List[str]:
        """
        列出所有可用的 Agent 名称

        Returns:
            Agent 名称列表
        """
        if not self._agents_cache:
            self.load_all_agents()

        return list(self._agents_cache.keys())

    def reload(self) -> Dict[str, AgentDefinition]:
        """
        重新加载所有 Agent 定义

        Returns:
            Agent 名称 -> Agent 定义的映射
        """
        self._agents_cache = {}
        return self.load_all_agents()


# 便捷函数
_loader: Optional[AgentLoader] = None


def get_agent_loader(agents_dir: Optional[Path] = None) -> AgentLoader:
    """
    获取 Agent 加载器实例（单例模式）

    Args:
        agents_dir: Agent 定义目录

    Returns:
        AgentLoader 实例
    """
    global _loader

    if _loader is None:
        _loader = AgentLoader(agents_dir)

    return _loader


def load_agent_prompt(agent_name: str, agents_dir: Optional[Path] = None) -> Optional[str]:
    """
    快捷函数：加载 Agent 的 prompt

    Args:
        agent_name: Agent 名称
        agents_dir: Agent 定义目录

    Returns:
        Agent prompt，如果不存在则返回 None
    """
    loader = get_agent_loader(agents_dir)
    agent_def = loader.get_agent(agent_name)

    if agent_def:
        return agent_def.prompt

    return None
