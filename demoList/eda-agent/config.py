"""Configuration - 全局配置

包含：
- API 密钥配置
- 模型配置
- 路径配置
"""
import os
from typing import Optional


class Config:
    """全局配置类"""

    # ============================================================================
    # LLM 配置
    # ============================================================================

    # LLM 提供商：默认使用 mock，可设置为 "claude", "qwen"
    LLM_PROVIDER: str = os.getenv("EDA_LLM_PROVIDER", "mock")

    # API 密钥
    ANTHROPIC_API_KEY: Optional[str] = os.getenv("ANTHROPIC_API_KEY")
    QWEN_API_KEY: Optional[str] = os.getenv("QWEN_API_KEY")

    # 模型配置
    LLM_MODEL: str = os.getenv("EDA_LLM_MODEL", "claude-sonnet-4-5")

    # API Base URL（可选，用于兼容接口）
    LLM_BASE_URL: Optional[str] = os.getenv("EDA_LLM_BASE_URL")

    # ============================================================================
    # 路径配置
    # ============================================================================

    # 项目根目录
    PROJECT_ROOT: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # 数据目录
    DATA_DIR: str = os.path.join(PROJECT_ROOT, "data")

    # 状态文件路径
    STATE_FILE: str = os.path.join(DATA_DIR, "state.json")

    # ============================================================================
    # 场景配置
    # ============================================================================

    # 最低匹配分数阈值
    MIN_MATCH_SCORE: float = 0.3

    # 最大对话轮数
    MAX_CONVERSATION_TURNS: int = 10

    # ============================================================================
    # 辅助方法
    # ============================================================================

    @classmethod
    def get_llm_api_key(cls) -> Optional[str]:
        """获取当前 LLM 提供商的 API 密钥"""
        if cls.LLM_PROVIDER == "claude":
            return cls.ANTHROPIC_API_KEY
        elif cls.LLM_PROVIDER == "qwen":
            return cls.QWEN_API_KEY
        return None

    @classmethod
    def validate(cls) -> bool:
        """验证配置是否有效"""
        # 如果使用非 mock LLM，需要 API 密钥
        if cls.LLM_PROVIDER != "mock":
            api_key = cls.get_llm_api_key()
            if not api_key:
                print(f"[Config] 警告：LLM_PROVIDER={cls.LLM_PROVIDER} 但未设置对应的 API 密钥")
                return False

        return True

    @classmethod
    def print_config(cls):
        """打印当前配置"""
        print("\n" + "=" * 70)
        print("EDA Agent 配置")
        print("=" * 70)
        print(f"LLM 提供商: {cls.LLM_PROVIDER}")
        print(f"LLM 模型: {cls.LLM_MODEL}")
        print(f"数据目录: {cls.DATA_DIR}")
        print(f"状态文件: {cls.STATE_FILE}")
        print(f"最低匹配分数: {cls.MIN_MATCH_SCORE}")
        print("=" * 70 + "\n")


# ============================================================================
# 测试代码
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("Config 测试")
    print("=" * 70)

    # 打印配置
    Config.print_config()

    # 验证配置
    is_valid = Config.validate()
    print(f"\n配置有效: {is_valid}")

    # 获取 API 密钥
    api_key = Config.get_llm_api_key()
    print(f"API 密钥: {'已设置' if api_key else '未设置'}")
