"""
配置管理

从 .env 文件和环境变量读取配置
.env 文件的优先级高于系统环境变量
"""
import os
from pathlib import Path
from dataclasses import dataclass
from dotenv import load_dotenv

# 强制加载 .env 文件（覆盖系统环境变量）
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path, override=True)


@dataclass
class LLMConfig:
    """LLM 配置"""
    api_key: str
    base_url: str
    model: str
    max_tokens: int
    temperature: float


@dataclass
class SessionConfig:
    """会话配置"""
    session_dir: str
    max_turns: int


@dataclass
class AppConfig:
    """应用配置"""
    llm: LLMConfig
    session: SessionConfig

    @classmethod
    def load_from_env(cls) -> "AppConfig":
        """从环境变量加载配置"""
        # LLM 配置（优先使用 .env 文件）
        llm = LLMConfig(
            api_key=os.getenv("ANTHROPIC_API_KEY", ""),
            base_url=os.getenv("ANTHROPIC_BASE_URL", "https://open.bigmodel.cn/api/anthropic"),
            model=os.getenv("MODEL", "glm-4.7"),
            max_tokens=int(os.getenv("MAX_TOKENS", "4096")),
            temperature=float(os.getenv("TEMPERATURE", "0.7"))
        )

        # 会话配置
        session = SessionConfig(
            session_dir=os.getenv("SESSION_DIR", "data/sessions"),
            max_turns=int(os.getenv("MAX_TURNS", "20"))
        )

        return cls(llm=llm, session=session)

    def validate(self) -> None:
        """验证配置"""
        if not self.llm.api_key:
            raise ValueError("ANTHROPIC_API_KEY 未设置，请在 .env 文件中配置")


# 全局配置实例
config = AppConfig.load_from_env()
