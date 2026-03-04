#!/usr/bin/env python3
"""
Master Agent 环境检查脚本 (SDK 版本)

检查基于 Claude Agent SDK 的单 Agent + 双 Skill 架构
"""
import sys
import os
from pathlib import Path
from typing import List

# 颜色输出
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'


def print_header(text: str):
    """打印标题"""
    print(f"\n{Colors.BLUE}{Colors.BOLD}{'='*60}{Colors.END}")
    print(f"{Colors.BLUE}{Colors.BOLD}{text:^60}{Colors.END}")
    print(f"{Colors.BLUE}{Colors.BOLD}{'='*60}{Colors.END}\n")


def print_success(text: str):
    """打印成功信息"""
    print(f"{Colors.GREEN}✓ {text}{Colors.END}")


def print_error(text: str):
    """打印错误信息"""
    print(f"{Colors.RED}✗ {text}{Colors.END}")


def print_warning(text: str):
    """打印警告信息"""
    print(f"{Colors.YELLOW}⚠ {text}{Colors.END}")


def print_info(text: str):
    """打印信息"""
    print(f"{Colors.BLUE}ℹ {text}{Colors.END}")


def check_python_version() -> bool:
    """检查 Python 版本"""
    print(f"Python 版本: {sys.version.split()[0]}")

    version = sys.version_info
    if version >= (3, 10):
        print_success("Python 版本符合要求 (>=3.10)")
        return True
    else:
        print_error("Python 版本过低，需要 3.10 或更高版本")
        return False


def check_files() -> List[bool]:
    """检查必需文件"""
    print("\n检查必需文件...")
    results = []

    required_files = [
        ("Master Agent 主入口", "master_main.py"),
        ("EDA Skill 定义", ".claude/skills/eda-skill/SKILL.md"),
        ("HimaQA Skill 定义", ".claude/skills/himaqa-skill/SKILL.md"),
        ("SDK 工具实现", "tools/sdk_tools.py"),
        ("EDA 工具实现", "tools/eda_tools.py"),
        ("HimaQA 工具实现", "tools/himaqa_tools.py"),
        ("配置管理", "config/settings.py"),
        ("项目存储", "storage/project_store.py"),
        ("结果存储", "storage/result_store.py"),
    ]

    for name, path in required_files:
        if Path(path).exists():
            print_success(f"{name}: {path}")
            results.append(True)
        else:
            print_error(f"{name}: {path} 不存在")
            results.append(False)

    return results


def check_dependencies() -> List[bool]:
    """检查 Python 依赖"""
    print("\n检查 Python 依赖...")
    results = []

    required_packages = {
        "anthropic": "Anthropic API SDK",
        "dotenv": "环境变量管理",
        "pydantic": "数据验证",
        "yaml": "YAML 解析",
    }

    # 检查 SDK（可选）
    print_info("Claude Agent SDK (推荐)")

    for package, description in required_packages.items():
        try:
            __import__(package.replace("-", "_"))
            print_success(f"{description} ({package})")
            results.append(True)
        except ImportError:
            print_error(f"{description} ({package}) 未安装")
            results.append(False)

    return results


def check_sdk_installation() -> bool:
    """检查 Claude Agent SDK 安装"""
    print("\n检查 Claude Agent SDK...")

    try:
        import claude_agent_sdk
        print_success("Claude Agent SDK 已安装")
        return True
    except ImportError:
        print_warning("Claude Agent SDK 未安装")
        print_info("安装命令: pip install claude-agent-sdk")
        return False


def check_config() -> bool:
    """检查配置文件"""
    print("\n检查配置...")

    env_file = Path(".env")
    if not env_file.exists():
        print_error(".env 文件不存在")
        print_info("请创建 .env 文件并设置 API Key")
        return False

    print_success(".env 文件存在")

    # 检查环境变量
    from dotenv import load_dotenv
    load_dotenv()

    api_key = os.getenv("ANTHROPIC_API_KEY")
    base_url = os.getenv("ANTHROPIC_BASE_URL")
    model = os.getenv("MODEL")

    checks = []

    if api_key and api_key != "your_api_key_here":
        print_success(f"API Key 已设置: {api_key[:10]}...")
        checks.append(True)
    else:
        print_error("API Key 未设置或为默认值")
        checks.append(False)

    if base_url:
        print_success(f"Base URL: {base_url}")
        checks.append(True)
    else:
        print_warning("Base URL 未设置（使用默认值）")
        checks.append(True)

    if model:
        print_success(f"模型: {model}")
        checks.append(True)
    else:
        print_warning("模型未设置（将使用默认值）")
        checks.append(True)

    return all(checks)


def check_skills() -> bool:
    """检查 Skills 定义（文件系统方式）"""
    print("\n检查 Skills 定义...")

    skills_dir = Path(".claude/skills")
    if not skills_dir.exists():
        print_error(".claude/skills 目录不存在")
        return False

    skills = []
    for skill_path in skills_dir.glob("*/SKILL.md"):
        skill_name = skill_path.parent.name
        skills.append(skill_name)

        # 读取并验证 YAML frontmatter
        try:
            content = skill_path.read_text(encoding='utf-8')
            if content.startswith("---"):
                print_success(f"{skill_name}: 有 YAML frontmatter")
            else:
                print_warning(f"{skill_name}: 缺少 YAML frontmatter")
        except Exception as e:
            print_warning(f"{skill_name}: 读取失败 - {e}")

    if not skills:
        print_error("没有找到任何 Skill 定义")
        return False

    print_success(f"已找到 {len(skills)} 个 Skills: {', '.join(skills)}")
    return True


def check_sdk_tools() -> bool:
    """检查 SDK 工具定义"""
    print("\n检查 SDK 工具...")

    try:
        from tools.sdk_tools import eda_tools_server, himaqa_tools_server
        print_success("SDK 工具模块加载成功")
        print_success("  - eda_tools_server (5 tools)")
        print_success("  - himaqa_tools_server (4 tools)")
        return True
    except ImportError as e:
        print_error(f"SDK 工具加载失败: {e}")
        return False


def check_eda_tools() -> bool:
    """检查 EDA 工具"""
    print("\n检查 EDA 工具...")

    try:
        from tools.eda_tools import (
            eda_create_project,
            eda_add_component,
            eda_connect,
            eda_simulate,
            eda_export
        )
        print_success("EDA 工具模块加载成功")
        return True
    except ImportError as e:
        print_error(f"EDA 工具加载失败: {e}")
        return False


def check_himaqa_tools() -> bool:
    """检查 HimaQA 工具"""
    print("\n检查 HimaQA 工具...")

    try:
        from tools.himaqa_tools import (
            himaqa_upload_netlist,
            himaqa_notify_manager,
            himaqa_query_history,
            himaqa_get_report
        )
        print_success("HimaQA 工具模块加载成功")
        return True
    except ImportError as e:
        print_error(f"HimaQA 工具加载失败: {e}")
        return False


def check_storage() -> bool:
    """检查存储系统"""
    print("\n检查存储系统...")

    try:
        from storage.project_store import project_store
        from storage.result_store import result_store

        print_success("项目存储模块加载成功")
        print_success("结果存储模块加载成功")

        # 测试存储目录创建
        project_store.storage_dir.mkdir(parents=True, exist_ok=True)
        result_store.storage_dir.mkdir(parents=True, exist_ok=True)

        print_success(f"项目存储目录: {project_store.storage_dir}")
        print_success(f"结果存储目录: {result_store.storage_dir}")

        return True
    except Exception as e:
        print_error(f"存储系统检查失败: {e}")
        return False


def test_tools() -> bool:
    """测试工具功能"""
    print("\n测试工具功能...")

    import asyncio
    from tools.eda_tools import eda_create_project
    from storage.project_store import project_store

    async def run_test():
        try:
            # 测试创建项目（会触发持久化）
            result = await eda_create_project({"name": "_test_project"})
            if result.get("status") == "success":
                print_success("创建项目测试通过")

                # 验证持久化
                if project_store.project_exists("_test_project"):
                    print_success("项目持久化测试通过")
                    project_store.delete_project("_test_project")
                    return True
                else:
                    print_error("项目持久化测试失败")
                    return False
            else:
                print_error(f"创建项目测试失败: {result}")
                return False
        except Exception as e:
            print_error(f"测试过程出错: {e}")
            import traceback
            traceback.print_exc()
            return False

    return asyncio.run(run_test())


def print_summary(results: List[bool]):
    """打印检查结果总结"""
    print_header("检查结果总结")

    total = len(results)
    passed = sum(results)
    failed = total - passed

    print(f"总计: {total} 项检查")
    print(f"{Colors.GREEN}通过: {passed} 项{Colors.END}")
    print(f"{Colors.RED}失败: {failed} 项{Colors.END}")

    if all(results):
        print(f"\n{Colors.GREEN}{Colors.BOLD}✓ 所有检查通过！可以启动 Master Agent{Colors.END}\n")
        print(f"运行命令: {Colors.BLUE}python3 master_main.py{Colors.END}\n")
        return 0
    else:
        print(f"\n{Colors.YELLOW}⚠ 部分检查失败或需要安装 SDK{Colors.END}\n")
        if not any("Claude Agent SDK" in str(r) for r in results):
            print(f"安装 SDK: {Colors.BLUE}pip install claude-agent-sdk{Colors.END}\n")
        return 1


def main():
    """主函数"""
    print_header("Master Agent 环境检查 (SDK 版本)")

    results = []

    # 检查 Python 版本
    results.append(check_python_version())

    # 检查必需文件
    results.extend(check_files())

    # 检查 Python 依赖
    results.extend(check_dependencies())

    # 检查 SDK 安装（可选）
    results.append(check_sdk_installation())

    # 检查配置
    results.append(check_config())

    # 检查 Skills（文件系统方式）
    results.append(check_skills())

    # 检查 SDK 工具
    results.append(check_sdk_tools())

    # 检查 EDA 工具
    results.append(check_eda_tools())

    # 检查 HimaQA 工具
    results.append(check_himaqa_tools())

    # 检查存储系统
    results.append(check_storage())

    # 测试工具功能
    results.append(test_tools())

    # 打印总结
    exit_code = print_summary(results)

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
